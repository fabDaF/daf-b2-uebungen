#!/usr/bin/env python3
"""
check_banner_faces.py — Sicherheitsnetz gegen abgeschnittene Gesichter in Tab-Bannern.

Das Problem (Frank, 2026-06-26, B2 1011X mitten im Unterricht):
  Tab-Banner werden per CSS `object-fit: cover` auf eine feste, niedrige Höhe
  (max-height 180px, mobil 120px) beschnitten. object-position ist „center".
  Ein Porträtfoto, dessen Gesicht oben sitzt, verliert dadurch Stirn und AUGEN —
  ein „kopfloses", demotivierendes Banner. Genau das ist auf dem Lückentext-Tab
  von 1011X passiert.

Was dieses Skript leistet (und was nicht — ehrlich):
  HART (Exit 1): Es erkennt per Haar-Cascade frontale/seitliche Gesichter im
    QUELLBILD jedes Banners, simuliert den `cover`-Crop (zentrales vertikales
    Band) und meldet jedes Gesicht, dessen Box vom Crop ANGESCHNITTEN wird.
    Das fängt zuverlässig den häufigsten Fall (das Foto enthält ein Gesicht,
    der Crop köpft es) — den Fall vom Screenshot.
  WEICH (⚠, nur mit --strict auch Exit 1): Verdacht auf ein bereits IM QUELLBILD
    kopflos beschnittenes Porträt (Augen/Mund-Cluster ohne vollständiges
    Gesicht). Solche Bilder (z. B. 1011X sec-0, zusätzlich farbgetönt) liefern
    der Gesichtserkennung NULL Gesichter — kein klassischer CV-Detektor erkennt
    sie zu 100 %. Deshalb: melden zur Sicht-Prüfung, nicht blind blockieren.

Die 100-%-Garantie liegt NICHT allein im Detektor, sondern im VORGEHEN
(CLAUDE.md, „Banner dürfen keine abgeschnittenen Gesichter zeigen"):
  1. Dieses Skript blockt die erkennbaren Fälle vor jedem Commit.
  2. Regel: Zeigt ein Banner einen Menschen, MUSS das ganze Gesicht (mit Augen)
     im sichtbaren Crop liegen — sonst ersetzen.
  3. Struktur-Default: Im Zweifel ein selbstgebautes, gesichtsfreies
     SVG-Banner (wie die neuen Reise-Banner in 1011X) — dann ist ein
     abgeschnittenes Gesicht baulich unmöglich.

SVG-Banner (data:image/svg+xml…) werden übersprungen — selbstgebaut, gesichtsfrei.
Externe URL-Banner (http…) sind in der Sandbox nicht prüfbar -> als ⚠ gemeldet.

Aufruf:
  python3 scripts/check_banner_faces.py                 # ganzes Repo (ohne daf-archiv)
  python3 scripts/check_banner_faces.py datei.html …    # einzelne Dateien
  python3 scripts/check_banner_faces.py --strict …      # Verdachtsfälle blocken auch

Abhängigkeit: opencv (Kopf-los): `pip install opencv-python-headless numpy`.
Fehlt sie, überspringt das Skript mit deutlicher Warnung (Exit 0) — damit der
Commit-Workflow nie an einer fehlenden Bibliothek hängenbleibt.

Vor jedem Lektions-Commit laufen lassen — zusammen mit check_serif.py,
check_wortbank.py, check_genus.py und check_schreib_pad.py.
"""
import base64
import os
import re
import sys

# --- Crop-Modell (object-fit: cover, object-position center) -----------------
# Sichtbar bleibt das zentrale vertikale Band des Quellbildes. Bei der
# verbindlichen Banner-CSS (Container ~820px + 60px Rand, Höhe 180px) zeigt der
# Desktop-Crop rund 56 % der Bildhöhe; Stirn/Augen fallen weg, wenn das Gesicht
# in den oberen ~22 % oder unteren ~22 % sitzt. Mobil (120px) ist es noch
# enger — wir prüfen konservativ gegen den Desktop-Wert.
RAND = 0.22  # oberer/unterer Rand, der vom Crop verschluckt wird


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


def _banners(html: str):
    """(src, alt) je Tab-Banner."""
    return re.findall(
        r'<img class="tab-banner"\s+src="([^"]*)"\s+alt="([^"]*)"', html
    )


def _decode_raster(src: str, np):
    """Gibt JPEG/PNG-Bytes zurück, oder None für SVG / externe URL / unklar."""
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
    """Liefert (hard, soft, skipped) Listen von (alt, grund)."""
    hard, soft, skipped = [], [], []
    try:
        html = open(path, encoding="utf-8", errors="replace").read()
    except OSError:
        return hard, soft, skipped
    for src, alt in _banners(html):
        raw = _decode_raster(src, np)
        if raw == "SVG":
            continue  # selbstgebaut, gesichtsfrei
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
        top_lim, bot_lim = RAND * H, (1 - RAND) * H

        # Vollständige Gesichter (frontal/seitlich) sammeln
        faces = []
        for key in ("front1", "front2", "profile"):
            for (x, y, w, h) in casc[key].detectMultiScale(
                g, 1.1, 5, minSize=(max(36, W // 18), max(36, H // 8))
            ):
                faces.append((x, y, w, h))
        # auch gespiegelt fürs Profil (nach links gerichtete Gesichter)
        for (x, y, w, h) in casc["profile"].detectMultiScale(
            cv2.flip(g, 1), 1.1, 5, minSize=(max(36, W // 18), max(36, H // 8))
        ):
            faces.append((W - x - w, y, w, h))

        clipped = [f for f in faces if f[1] < top_lim or (f[1] + f[3]) > bot_lim]
        if clipped:
            y0 = min(f[1] for f in clipped)
            y1 = max(f[1] + f[3] for f in clipped)
            where = "oben" if y0 < top_lim else "unten"
            hard.append(
                (alt, f"Gesicht y[{y0}-{y1}] von {H}px wird {where} angeschnitten "
                      f"(sichtbar nur ~{int((1-2*RAND)*H)}px Mitte)")
            )
            continue

        if faces:
            continue  # Gesicht(er) vorhanden, aber voll im sichtbaren Band -> ok

        # Kein vollständiges Gesicht: Verdacht auf kopflos beschnittenes Porträt?
        eyes = list(casc["eye"].detectMultiScale(g, 1.1, 6, minSize=(20, 20)))
        smiles = list(casc["smile"].detectMultiScale(g, 1.2, 22, minSize=(40, 24)))
        eyes_top = [e for e in eyes if e[1] < 0.45 * H]
        # Signatur b0: Augen im oberen Bereich + Mund/Smile darunter, vertikal
        # gestapelt, in der Bildmitte -> sehr wahrscheinlich ein Gesicht, dessen
        # Oberkopf bereits fehlt.
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
              f"(externe URL / Format) — bei Bedarf manuell ansehen.")
        print()

    if all_hard:
        print(f"✗ {len(all_hard)} Banner mit ANGESCHNITTENEM Gesicht "
              f"(CLAUDE.md-Pflicht verletzt):")
        for p, alt, why in all_hard:
            print(f"    {p}\n        alt={alt!r}: {why}")
        print("\nFix: Banner so neu komponieren, dass das ganze Gesicht (mit Augen) "
              "im sichtbaren Band liegt — oder durch ein selbstgebautes, "
              "gesichtsfreies SVG-Banner ersetzen (siehe 1011X Reise-Banner).")
        sys.exit(1)

    if strict and all_soft:
        print("✗ --strict: Verdachtsfälle gelten als Fehler.")
        sys.exit(1)

    print("✓ Kein angeschnittenes Gesicht in den geprüften Bannern gefunden.")
    sys.exit(0)
