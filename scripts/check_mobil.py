#!/usr/bin/env python3
"""check_mobil.py — Gate für garantierte Handy-Bedienbarkeit (Pflicht seit 2026-07-07).

Vier Defektklassen, die Lektionen am iPhone real unbedienbar gemacht haben
(Funde 2026-07-04 an 2034R; Rest-Bestände von 159 Dateien am 2026-07-07 bereinigt):

  1. Inline-Grid am wortschatzContainer — ein Inline-Style schlägt JEDE
     Media-Query, das iPhone bleibt zweispaltig (Injektor-Bug seit 2026-06-30).
     Fix: style-Attribut entfernen, Grid kommt aus FB-WORTSCHATZ-KANON-CSS
     (inject_wortschatz.py, inkl. @media-1-Spalten-Query).
  2. Satzbau-Gerüst mit "click":false — HTML5-Drag&Drop ist auf iOS-Touch
     prinzipiell tot; ohne Tipp-Modus (Tap→Lücke) unbedienbar. Franks
     iPhone-Abnahme 2026-07-05: click:true ist der Standard.
  3. nowrap-Basis-Chip + chip-bank/drop-zone ohne Wrap-Override — Chips mit
     ganzen Sätzen laufen aus dem Viewport. Erkennungslogik kommt aus
     fb_chipwrap_swinit.py (geteilte Wahrheit, Reparateur = derselbe Runner).
  4. Fehlendes Viewport-Meta in einer Lektionsdatei — ohne
     width=device-width rendert das Handy die Desktop-Breite verkleinert.

Nutzung: python3 scripts/check_mobil.py [datei.html …]   (ohne Args: Repo)
Exit 1 bei Treffern — blockierendes Gate in check_all.py (Backlog = 0 seit 2026-07-07).
"""
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from fb_chipwrap_swinit import check_fix_a  # geteilte Chip-Wrap-Erkennung

GRID_RE = re.compile(r'id="wortschatzContainer"[^>]*style="[^"]*grid-template-columns')
CLICK_RE = re.compile(r'"click"\s*:\s*false')


def collect_repo():
    out = []
    for dp, dn, fn in os.walk("."):
        if "/daf-archiv" in dp or "/.git" in dp or "/backup" in dp:
            continue
        for f in fn:
            if f.endswith(".html") and ".bak" not in f:
                out.append(os.path.join(dp, f))
    return out


def check(path):
    try:
        s = open(path, encoding="utf-8", errors="replace").read()
    except OSError:
        return []
    probleme = []
    if GRID_RE.search(s):
        probleme.append("Inline-Grid am wortschatzContainer (schlägt Media-Query)")
    if CLICK_RE.search(s) and "placeJudge" in s:
        probleme.append('Satzbau-Gerüst mit "click":false (iOS-Drag&Drop tot)')
    if check_fix_a(s):
        probleme.append("nowrap-Chips ohne Wrap-Override (chip-bank/drop-zone)")
    if 'class="container"' in s and 'name="viewport"' not in s:
        probleme.append("Viewport-Meta fehlt")
    return probleme


if __name__ == "__main__":
    files = sys.argv[1:] or collect_repo()
    bad = 0
    for p in files:
        for prob in check(p):
            bad += 1
            print(f"  ✗ {p}: {prob}")
    if bad:
        print(f"\n✗ {bad} Mobil-Problem(e). Fixes: style-Attribut strippen + "
              "inject_wortschatz.py-CSS · click:true · fb_chipwrap_swinit.py apply · Viewport-Meta.")
        sys.exit(1)
    sys.exit(0)
