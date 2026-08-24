#!/usr/bin/env python3
"""test_nav_lib.py — Regressionstest für nav_lib.normalize().

Warum es diesen Test gibt (Fund 2026-08-24, B1 1012G mitten im Unterricht):
normalize() entfernte seine Ziel-Regeln per blankem re.sub. Das Muster
`\\.nav-label\\s*\\{[^}]*\\}` matcht aber auch MITTEN in einer
Nachfahren-Regel `.nav-btn .nav-label { … }`. Entfernt wurde dann nur das
hintere Stück; zurück blieb die nackte Zeile

    .nav-btn

Für den Browser ist das kein Fehler, sondern der ANFANG eines Selektors: er
liest weiter bis zur nächsten `{` und macht daraus `.nav-btn .section`. Damit
war `.section { display: none }` verschluckt — alle Tabs standen gleichzeitig
untereinander. Neun Lektionen waren betroffen, kein einziges Gate hat es
gesehen.

Aufruf:  python3 scripts/test_nav_lib.py    (Exit 0 = grün)
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import nav_lib  # noqa: E402

VORHER = """<style>
.nav { display:flex; padding:6px; }
.nav-btn { padding:12px; border-radius:10px; display:flex; flex-direction:column; }
.nav-btn:hover { background:#e1e5fb; }
.nav-btn.active { background:#fff; box-shadow:0 1px 4px rgba(0,0,0,.2); }
.nav-btn .nav-emoji { font-size: 1.3em; }
.nav-btn .nav-label { font-size: 0.78em; }
/* Sections */
.section { display: none; padding: 28px; }
.section.active { display: block; }
</style>"""


def verwaiste_zeilen(css):
    """Zeilen, die wie ein Selektor aussehen, aber keine Regel öffnen."""
    treffer = []
    for zeile in css.split('\n'):
        s = zeile.strip()
        if not s or '{' in s or '}' in s:
            continue
        if s.startswith(('/*', '*', '<')) or s.endswith((';', ',', '*/')):
            continue
        treffer.append(s)
    return treffer


def main():
    fehler = []

    neu, changed, grund = nav_lib.normalize(VORHER)
    if not changed:
        fehler.append(f'normalize() hat nichts geändert ({grund}).')

    if '.section { display: none; padding: 28px; }' not in neu:
        fehler.append('Die .section-Regel wurde verschluckt — genau der 1012G-Fehler.')

    waisen = verwaiste_zeilen(neu)
    if waisen:
        fehler.append(f'Verwaiste Selektor-Zeile(n) zurückgelassen: {waisen}')

    nochmal, _, _ = nav_lib.normalize(neu)
    if nochmal != neu:
        fehler.append('normalize() ist nicht idempotent.')

    if fehler:
        for f in fehler:
            print(f'✗ {f}')
        sys.exit(1)
    print('✓ nav_lib.normalize(): Folgeregel intakt, keine Waisen, idempotent.')
    sys.exit(0)


if __name__ == '__main__':
    main()
