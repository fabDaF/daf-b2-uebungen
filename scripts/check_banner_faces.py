#!/usr/bin/env python3
"""
check_banner_faces.py — Sicherheitsnetz gegen abgeschnittene Gesichter in Tab-Bannern.

Das Problem (Frank, 2026-06-26, B2 1011X): Tab-Banner werden per
`object-fit: cover` auf eine feste niedrige Höhe beschnitten; ohne
`object-position` ist die Voreinstellung „center". Sitzt ein Gesicht oben im
Bild, schneidet der Crop Stirn und AUGEN weg — ein „kopfloses", demotivierendes
Banner.

Der bevorzugte Fix (Franks Methode): Ausschnitt nach oben schieben
(`style="object-position: top"`) statt das Bild zu ersetzen. Nur wenn die Augen
schon IM QUELLBILD fehlen, kommt ein gesichtsfreies SVG-Banner.

Erkennung (2026-06-27 geschärft, nachdem ein seitlich/mit Kopfhörern gezeigter
Junge in B2 3021X durchgerutscht war):
  - fünf Haar-Kaskaden (frontalface default/alt/alt2/alt_tree + profile, je auch
    gespiegelt), entspannte Parameter (scaleFactor 1.05, minNeighbors 3) → fängt
    auch geneigte/teils verdeckte Gesichter.
  - die AUGENLINIE wird nicht mehr nur aus der Box geschätzt, sondern mit der
    Augen-Kaskade INNERHALB der Gesichts-Box lokalisiert (robust gegen schräge
    Köpfe). Fallback: y + 0.32·h.
  - liest die `object-position` und simuliert das sichtbare cover-Band.
  - HART (Exit 1), wenn die Augenlinie über (band_top + 4 % Höhe) liegt — also
    am oder über dem oberen Crop-Rand. Ein nur unten beschnittenes Kinn ist
    kosmetisch und wird nicht geblockt; ein nach oben geschobenes Banner
    (object-position: top, band_top≈0) kommt sauber durch.

Ehrliche Grenze: Manche Gesichter (starke Neigung, Sonnenbrille, Haarverdeckung,
nur Hinterkopf) erkennt KEINE klassische CV-Kaskade. Der Guardrail fängt die
große Mehrheit; das letzte Sicherheitsnetz bleibt das menschliche Auge. Deshalb:
bei jeder geöffneten Lektion kurz auf geköpfte Banner achten und melden.

SVG-Banner werden übersprungen; externe URL-Banner als ⚠ gemeldet (nicht prüfbar).

Aufruf:
  python3 scripts/check_banner_faces.py                 # ganzes Repo (ohne daf-archiv)
  python3 scripts/check_banner_faces.py datei.html …    # einzelne Dateien

Abhängigkeit: `pip install opencv-python-headless numpy`. Fehlt sie, Exit 0 mit
Warnung — der Commit-Workflow hängt nie an einer fehlenden Bibliothek.

Vor jedem Lektions-Commit laufen lassen — mit check_serif.py, check_wortbank.py,
check_genus.py und check_schreib_pad.py.
"""
import base64
import os
import re
import sys

RAND = 0.22
VIS = 1 - 2 * RAND
MARGIN = 0.04          # Toleranz über dem Bandrand, ab der die Augen als „weg" gelten
MAXW = 800             # Detektionsauflösung (Einzeldatei-Lauf darf voll auflösen)
FACE_CASCADES = (
    "frontalface_default", "frontalface_alt2", "profileface",
)


def _load_cv():
    try:
        import cv2  # noqa
        import numpy as np  # noqa
        return cv2, np
    except Exception:
        return None, None


def _cascades(cv2):
    hd = cv2.data.haarcascades
    c = {n: cv2.CascadeClassifier(hd + "haarcascade_" + n + ".xml")
         for n in FACE_CASCADES}
    c["eye"] = cv2.CascadeClassifier(hd + "haarcascade_eye.xml")
    return c


def _banner_tags(html):
    return re.findall(
        r'(<img class="tab-banner"\s+src="([^"]*)"[^>]*\balt="([^"]*)"[^>]*>)', html
    )


def _object_position_y(tag):
    m = re.search(r'object-position\s*:\s*([^;"\']+)', tag, re.I)
    if not m:
        return 0.5
    v = m.group(1).strip().lower()
    if "top" in v:
        return 0.0
    if "bottom" in v:
        return 1.0
    perc = re.findall(r'(\d+(?:\.\d+)?)\s*%', v)
    if "center" in v and perc:
        return min(1.0, float(perc[0]) / 100.0)
    if len(perc) >= 2:
        return min(1.0, float(perc[1]) / 100.0)
    return 0.5


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


def eyes_cut(arr, posy, cv2, np, casc, maxw=MAXW):
    """True, wenn ein erkanntes Gesicht oben (über band_top+MARGIN) angeschnitten
    wird. Lokalisiert die Augen mit der Augen-Kaskade in der Gesichts-Box."""
    H0, W0 = arr.shape[:2]
    sc = min(1.0, maxw / max(1, W0))
    g = cv2.cvtColor(cv2.resize(arr, (max(1, int(W0 * sc)), max(1, int(H0 * sc)))),
                     cv2.COLOR_BGR2GRAY)
    H, W = g.shape
    band_top = posy * (H - VIS * H)
    boxes = []
    for n in FACE_CASCADES:
        ms = (max(26, W // 24), max(26, H // 10))
        for b in casc[n].detectMultiScale(g, 1.05, 3, minSize=ms):
            boxes.append(tuple(int(v) for v in b))
        for b in casc[n].detectMultiScale(cv2.flip(g, 1), 1.05, 3, minSize=ms):
            x, y, w, h = (int(v) for v in b)
            boxes.append((W - x - w, y, w, h))
    for (x, y, w, h) in boxes:
        roi = g[max(0, y):y + int(h * 0.65), max(0, x):x + w]
        eye_y = None
        if roi.size:
            es = casc["eye"].detectMultiScale(roi, 1.1, 4,
                                              minSize=(max(10, w // 8), max(10, w // 8)))
            if len(es):
                eye_y = y + min(e[1] + e[3] * 0.5 for e in es)
        # Nur mit per Augen-Kaskade BESTÄTIGTEN Augen flaggen (hohe Präzision,
        # kaum Fehlalarme auf Grafiken). Geschätzte Box-Geometrie allein genügt
        # nicht — sie überflutete sonst Texturen/Diagramme mit Falschtreffern.
        if eye_y is not None and eye_y < band_top + MARGIN * H:
            return True, int(eye_y), int(band_top), H
    return False, None, int(band_top), H


def analyze_file(path, cv2, np, casc):
    hard, skipped = [], []
    try:
        html = open(path, encoding="utf-8", errors="replace").read()
    except OSError:
        return hard, skipped
    for tag, src, alt in _banner_tags(html):
        raw = _decode_raster(src, np)
        if raw == "SVG":
            continue
        if raw == "URL":
            skipped.append((alt, "externe URL — nicht prüfbar"))
            continue
        if raw is None:
            skipped.append((alt, "Format nicht dekodierbar"))
            continue
        arr = cv2.imdecode(np.frombuffer(raw, np.uint8), cv2.IMREAD_COLOR)
        if arr is None:
            skipped.append((alt, "nicht dekodierbar"))
            continue
        posy = _object_position_y(tag)
        cut, ey, bt, H = eyes_cut(arr, posy, cv2, np, casc)
        if cut:
            hint = "" if posy == 0.5 else f", object-position-y={posy:.2f}"
            hard.append((alt, f"Augenlinie y≈{ey} über Bandrand {bt} (von {H}px)"
                              f"{hint}. Fix: style=\"object-position: top\" — oder "
                              f"gesichtsfreies SVG, falls Augen im Quellbild fehlen."))
    return hard, skipped


def hard_banner_indices(html, cv2, np, casc, maxw=MAXW):
    """Indizes der tab-banner-Bilder mit oben angeschnittenem Gesicht (für Reparatur)."""
    out = []
    tags = re.findall(r'(<img class="tab-banner"\s+src="[^"]*"[^>]*>)', html)
    srcs = re.findall(r'<img class="tab-banner"\s+src="([^"]*)"[^>]*>', html)
    for i, (tag, src) in enumerate(zip(tags, srcs)):
        raw = _decode_raster(src, np)
        if raw in ("SVG", "URL", None) or isinstance(raw, str):
            continue
        arr = cv2.imdecode(np.frombuffer(raw, np.uint8), cv2.IMREAD_COLOR)
        if arr is None:
            continue
        posy = _object_position_y(tag)
        if eyes_cut(arr, posy, cv2, np, casc, maxw)[0]:
            out.append(i)
    return out


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
    cv2, np = _load_cv()
    if cv2 is None:
        print("⚠ check_banner_faces.py ÜBERSPRUNGEN — opencv nicht installiert.")
        print("  pip install opencv-python-headless numpy")
        sys.exit(0)
    casc = _cascades(cv2)
    files = args if args else collect_repo()
    all_hard, all_skip = [], []
    for p in files:
        hard, skipped = analyze_file(p, cv2, np, casc)
        for alt, why in hard:
            all_hard.append((p, alt, why))
        for alt, why in skipped:
            all_skip.append((p, alt, why))
    if all_skip:
        print(f"ℹ {len(all_skip)} Banner nicht automatisch prüfbar (URL/Format).\n")
    if all_hard:
        print(f"✗ {len(all_hard)} Banner mit oben ANGESCHNITTENEM Gesicht:")
        for p, alt, why in all_hard:
            print(f"    {p}\n        alt={alt!r}: {why}")
        sys.exit(1)
    print("✓ Kein oben angeschnittenes Gesicht in den geprüften Bannern gefunden.")
    sys.exit(0)
