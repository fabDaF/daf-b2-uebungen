#!/usr/bin/env python3
"""
fix_nav.py — deterministischer Normalisierer für den Nav-Header (Variante C).

Bringt den Nav-Block jeder DaF-HTML-Lektion EXAKT auf die kanonische Aktiv-Pille.
Idempotent: zweiter Lauf ändert nichts mehr. Quelle der Wahrheit: nav_lib.py.

  python3 scripts/fix_nav.py DATEI.html [DATEI2.html ...]
  python3 scripts/fix_nav.py --check DATEI.html       # nur anzeigen, nicht schreiben

Bricht pro Datei sicher ab (lässt sie unberührt), wenn keine .nav-btn-Basisregel
existiert (unbekanntes Layout → Handarbeit). Lässt .nav-btn.schreib-last (order:99)
und sonstige Zusatz-Selektoren unangetastet.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import nav_lib


def main(argv):
    args = argv[1:]
    dry = False
    if args and args[0] == '--check':
        dry = True
        args = args[1:]
    if not args:
        print('Usage: fix_nav.py [--check] DATEI.html ...')
        return 2

    changed_n = 0
    skipped_n = 0
    for f in args:
        try:
            text = open(f, encoding='utf-8').read()
        except Exception as e:
            print(f'  ?? {f}: {e}')
            continue
        new, changed, reason = nav_lib.normalize(text)
        if not changed:
            skipped_n += 1
            print(f'  – {f}: {reason}')
            continue
        if dry:
            print(f'  ~ {f}: würde normalisiert ({reason})')
        else:
            with open(f, 'w', encoding='utf-8') as fh:
                fh.write(new)
            print(f'  ✓ {f}: {reason}')
        changed_n += 1

    print(f'\n{changed_n} geändert, {skipped_n} unberührt.')
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
