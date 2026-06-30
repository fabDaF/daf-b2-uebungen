#!/usr/bin/env python3
"""
check_nav.py — Sicherheitsnetz für den kanonischen Nav-Header (Variante C, Aktiv-Pille).

Meldet jede DaF-HTML-Datei, deren Nav nicht der Variante C entspricht (Exit 1).
Quelle der Wahrheit: nav_lib.py (geteilt mit fix_nav.py).

  python3 scripts/check_nav.py DATEI.html [DATEI2.html ...]   # einzelne Dateien
  python3 scripts/check_nav.py                                # ganzes Repo (htmlS/, Root)

VOR JEDEM LEKTIONS-COMMIT laufen lassen — zusammen mit check_serif.py,
check_wortbank.py, check_genus.py, check_schreib_pad.py, check_banner_faces.py.

Dateien ohne .nav-Leiste (z. B. reine Index-/Dashboard-Seiten) werden übersprungen.
"""
import sys, os, glob
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import nav_lib


def find_files():
    files = []
    for base in ('htmlS', '.'):
        for f in glob.glob(os.path.join(base, '**', '*.html'), recursive=True):
            if 'daf-archiv' in f:        # Archiv ist eingefroren
                continue
            files.append(f)
    return sorted(set(files))


def main(argv):
    targets = argv[1:] if len(argv) > 1 else find_files()
    bad = 0
    skipped = 0
    for f in targets:
        try:
            text = open(f, encoding='utf-8').read()
        except Exception as e:
            print(f'  ?? {f}: {e}')
            continue
        # Nur Dateien mit echter Tab-Nav prüfen.
        if 'class="nav-btn' not in text and "class='nav-btn" not in text:
            skipped += 1
            continue
        problems = nav_lib.verify(text)
        if problems:
            bad += 1
            print(f'✗ {f}')
            for p in problems:
                print(f'    - {p}')
    total = len(targets) - skipped
    if bad:
        print(f'\n{bad} von {total} Nav-Dateien NICHT konform zu Variante C.')
        return 1
    print(f'✓ Alle {total} geprüften Nav-Dateien konform zu Variante C (Aktiv-Pille).')
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
