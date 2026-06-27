#!/usr/bin/env python3
"""
check_banner_faces.py — Sicherheitsnetz gegen abgeschnittene Gesichter in Tab-Bannern.

Das Problem (Frank, 2026-06-26, B2 1011X mitten im Unterricht):
  Tab-Banner werden per CSS `object-fit: cover` auf eine feste, niedrige Höhe
  (max-height 180px, mobil 120px) beschnitten. Ohne `object-position` ist die
  Voreinstellung „center" — ein Porträtfoto, dessen Gesicht oben sitzt, verliert
  dadurch Stirn und AUGEN: ein „kopfloses", demotivierendes Banner.

Der bevorzugte Fix (Franks Idee, 2026-06-27):
  Statt das Bild zu ersetzen, den **Ausschnitt nach oben schieben** —
  `style="object-position: top"` am <img>. Dann zeigt der Crop das obere Band
  des Bildes (wo der Kopf sitzt) und schneidet stattdessen unten den Rumpf weg.
  Das rettet praktisch jedes Foto, bei dem die Augen im Quellbild vorhanden sind.
  Nur Bilder, denen die Augen schon im Quellbild fehlen (z. B. 1011X-
  Vorentlastung), brauchen ein gesichtsfreies SVG-Banner als Ersatz.

Was dieses Skript prüft:
  Es liest pro Banner die `object-position` (top / bottom / "50% NN%" / center),
  simuliert das sichtbare Crop-Band und blockt (Exit 1) jedes Banner, dessen
  erkanntes Gesicht **oben angeschnitten** wird (Augenlinie über dem Bandrand =
  Augen weg). Ein nur unten beschnittenes Kinn ist kosmetisch und wird nicht
  geblockt. So passt ein korrekt nach oben geschobenes Banner durch — und der
  Prüfer bleibt mit der Realität konsistent.

Ehrliche Grenze: ein im Quellbild bereits kopflos beschnittenes, zusätzlich
getöntes Porträt liefert der Gesichtserkennung null Gesichter — kein klassischer
CV-Detektor erkennt das zu 100 %. Solche Fälle meldet das Skript als ⚠ (Verdacht)
zur Sicht-Prüfung; `--strict` lässt auch das fehlschlagen. Die 100-%-Garantie
liegt im Vorgehen (CLAUDE.md): Guardrail + Regel (schieben, sonst ersetzen) +
Struktur-Default (im Zweifel gesichtsfreies SVG).

SVG-Banner (data:image/svg+xml…) werden übersprungen — selbstgebaut, gesichtsfrei.
Externe URL-Banner (http…) sind in der Sandbox nicht prüfbar -> als ⚠ gemeldet.

Aufruf:
  python3 scripts/check_banner_faces.py                 # ganzes Repo (ohne daf-archiv)
  python3 scripts/check_banner_faces.py datei.html …    # einzelne Dateien
  python3 scripts/check_banner_faces.py --strict …      # Verdachtsfälle blocken auch

Abhängigkeit: `pip install opencv-python-headless numpy`. Fehlt sie, überspringt
das Skript mit deutlicher Warnung (Exit 0) — der Commit-Workflow hängt nie an
einer fehlenden Bibliothek.

Vor jedem Lektions-Commit laufen lassen — zusammen mit check_serif.py,
check_wortbank.py, check_genus.py und check_schreib_pad.py.
"""
import base64
import os
import re
import sys

RAND = 0.22  # Anteil oben/unten, den der cover-Crop bei max-height 180 verschluckt
VIS = 1 - 2 * RAND  # sichtbarer vertikaler Anteil (~0.56)


def _load_cv():
    try:
        import cv2  # noqa
        import numpy as np  # noqa
        return cv2, np
    except Exception:
        return None, None


def _cascades(cv2):
    hd = cv2.data.haarcascades
    name = lambda n: cv2.CascadeClassifier(hd + "haarcascade_" + n + ".xml")
    return {
        "front1": name("frontalface_default"),
        "front2": name("frontalface_alt2"),
        "profile": name("profileface"),
        "eye": name("eye"),
        "smile": name("smile"),
    }


def _banner_tags(html: str):
    """(ganzer img-Tag, src, alt) je Tab-Banner."""
    return re.findall(
        r'(<img class="tab-banner"\s+src="([^"]*)"[^>]*\balt="([^"]*)"[^>]*>)', html
    )


def _object_position_y(tag: str):
    """Liefert die vertikale object-position als Anteil 0..1 (0=oben,1=unten)
    oder 0.5 (center) als Default."""
    m = re.search(r'object-position\s*:\s*([^;"\']+)', tag, re.I)
    if not m:
        return 0.5
    v = m.group(1).strip().lower()
    if "top" in v:
        return 0.0
    if "bottom" in v:
        return 1.0
    # Formen wie "50% 0%", "center 20%", "0%"
    perc = re.findall(r'(\d+(?:\.\d+)?)\s*%', v)
    if "center" in v and perc:
        return min(1.0, float(perc[0]) / 100.0)
    if len(perc) >= 2:
        return min(1.0, float(perc[1]) / 100.0)
    if len(perc) == 1:
        # einzelner Wert = horizontale Position; vertikal bleibt center
        return 0.5
    return 0.5


def _band(H, posy):
    """Sichtbares vertikales Band [top, bot] in Bild-Pixeln für object-position posy."""
    vis = VIS * H
    top = posy * (H - vis)
    return top, top + vis


def _decode_raster(src, np):
    if src.startswith("data:image/svg+xml"):
        return "SVG"
    m = re.match(r"data:image/(png|jpe?g|webp);base64,(.+)", src, re.S)
    if m:
        try:
            return base64.b64decode(m.group(2))
        except Exception:
            return None
    if src.startswith("http"):
        return "URL"
    return None


def analyze_file(path, cv2, np, casc):
    hard, soft, skipped = [], [], []
    try:
        html = open(path, encoding="utf-8", errors="replace").read()
    except OSError:
        return hard, soft, skipped
    for tag, src, alt in _banner_tags(html):
        raw = _decode_raster(src, np)
        if raw == "SVG":
            continue
        if raw == "URL":
            skipped.append((alt, "externe URL — in Sandbox nicht prüfbar"))
            continue
        if raw is None:
            skipped.append((alt, "Bildformat nicht dekodierbar"))
            continue
        arr = cv2.imdecode(np.frombuffer(raw, np.uint8), cv2.IMREAD_COLOR)
        if arr is None:
            skipped.append((alt, "Bild nicht dekodierbar"))
            continue
        g = cv2.cvtColor(arr, cv2.COLOR_BGR2GRAY)
        H, W = g.shape
        posy = _object_position_y(tag)
        band_top, band_bot = _band(H, posy)

        faces = []
        for key in ("front1", "front2", "profile"):
            for (x, y, w, h) in casc[key].detectMultiScale(
                g, 1.1, 5, minSize=(max(36, W // 18), max(36, H // 8))
            ):
                faces.append((int(x), int(y), int(w), int(h)))
        for (x, y, w, h) in casc["profile"].detectMultiScale(
            cv2.flip(g, 1), 1.1, 5, minSize=(max(36, W // 18), max(36, H // 8))
        ):
            faces.append((int(W - x - w), int(y), int(w), int(h)))

        # HART: Augenlinie (~ Oberkante + 0.40*Höhe) liegt über dem Band -> Augen weg
        eyes_cut = [f for f in faces if (f[1] + 0.40 * f[3]) < band_top]
        if eyes_cut:
            y0 = min(f[1] for f in eyes_cut)
            hint = "" if posy == 0.5 else f", object-position-y={posy:.2f}"
            hard.append(
                (alt, f"Gesicht ab y={y0} (von {H}px) — Augen über dem sichtbaren "
                      f"Band [{int(band_top)}-{int(band_bot)}]{hint}. "
                      f"Fix: style=\"object-position: top\" — oder, wenn das die "
                      f"Augen nicht hereinholt, gesichtsfreies SVG-Banner.")
            )
            continue
        if faces:
            continue  # Gesicht(er) im sichtbaren Band -> ok (Kinn-Cut ist kosmetisch)

        # kein vollständiges Gesicht: Verdacht auf kopflos beschnittenes Porträt?
        eyes = list(casc["eye"].detectMultiScale(g, 1.1, 6, minSize=(20, 20)))
        smiles = list(casc["smile"].detectMultiScale(g, 1.2, 22, minSize=(40, 24)))
        eyes_top = [e for e in eyes if e[1] < 0.45 * H]
        if eyes_top and smiles:
            for ex, ey, ew, eh in eyes_top:
                ecx = ex + ew / 2
                below = [s for s in smiles if s[1] > ey + eh * 0.5
                         and abs((s[0] + s[1] / 2) - ecx) < W * 0.18]
                if below and 0.25 * W < ecx < 0.75 * W:
                    soft.append(
                        (alt, "Verdacht: Augen+Mund ohne vollständiges Gesicht "
                              "(evtl. bereits kopflos beschnittenes Porträt) — "
                              "bitte visuell prüfen")
                    )
                    break
    return hard, soft, skipped


def collect_repo():
    out = []
    for dp, dn, fn in os.walk("."):
        if "/daf-archiv" in dp or "/.git" in dp:
            continue
        for f in fn:
            if f.endswith(".html") and ".bak" not in f:
                out.append(os.path.join(dp, f))
    return out


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("-")]
    strict = "--strict" in sys.argv[1:]

    cv2, np = _load_cv()
    if cv2 is None:
        print("⚠ check_banner_faces.py ÜBERSPRUNGEN — opencv nicht installiert.")
        print("  Für vollen Banner-Gesichts-Schutz:  "
              "pip install opencv-python-headless numpy")
        sys.exit(0)

    casc = _cascades(cv2)
    files = args if args else collect_repo()

    all_hard, all_soft, all_skip = [], [], []
    for p in files:
        hard, soft, skipped = analyze_file(p, cv2, np, casc)
        for alt, why in hard:
            all_hard.append((p, alt, why))
        for alt, why in soft:
            all_soft.append((p, alt, why))
        for alt, why in skipped:
            all_skip.append((p, alt, why))

    if all_soft:
        print(f"⚠ {len(all_soft)} Banner mit Verdacht auf (kopflos) beschnittenes "
              f"Gesicht — visuell prüfen:")
        for p, alt, why in all_soft:
            print(f"    {p}\n        alt={alt!r}: {why}")
        print()
    if all_skip:
        print(f"ℹ {len(all_skip)} Banner nicht automatisch prüfbar "
              f"(externe URL / Format).")
        print()

    if all_hard:
        print(f"✗ {len(all_hard)} Banner mit oben ANGESCHNITTENEM Gesicht "
              f"(CLAUDE.md-Pflicht verletzt):")
        for p, alt, why in all_hard:
            print(f"    {p}\n        alt={alt!r}: {why}")
        sys.exit(1)

    if strict and all_soft:
        print("✗ --strict: Verdachtsfälle gelten als Fehler.")
        sys.exit(1)

    print("✓ Kein oben angeschnittenes Gesicht in den geprüften Bannern gefunden.")
    sys.exit(0)
