#!/usr/bin/env python3
"""check_schreib_name.py — Gate: Schreibwerkstatt darf nicht namenlos senden.

Franks Regel (2026-07-16): Kein Schülertext darf ohne Namensangabe abgeschickt
werden können. Erzwungen wird das durch das selbst-installierende Modul
FB-NAME-REQUIRED (siehe scripts/inject_schreib_name.py), das die Sende-Trigger
und den Choke-Point umschließt und über ALLE Generationen die Namenspflicht
(≥ 2 Zeichen) durchsetzt — generationsunabhängig, ohne je ein zweites Feld zu
bauen.

Dieses Gate blockt jede Schreibwerkstatt-Datei (erkannt an `schreib-mini-textarea`),
der der FB-NAME-REQUIRED-Marker fehlt. Backlog bei Scharfschaltung: 0 (alle 635
Formulare nachgerüstet).

Fix bei rotem Gate:  python3 scripts/inject_schreib_name.py DATEI.html

Aufruf:
    python3 scripts/check_schreib_name.py            # ganzes Repo
    python3 scripts/check_schreib_name.py a.html b/  # einzelne Dateien/Ordner
Exit 0 = sauber. Exit 1 = Befunde (Commit blockiert).
"""
import os
import sys

SKIP_DIRS = {'daf-archiv', '.git', 'node_modules', 'backup', 'quelltexte'}
FORM_MARK = 'schreib-mini-textarea'
GUARD_MARK = 'FB-NAME-REQUIRED'


def html_files(paths):
    if not paths:
        paths = ['.']
    for p in paths:
        if os.path.isfile(p):
            yield p
            continue
        for root, dirs, files in os.walk(p):
            dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
            for f in files:
                if f.endswith('.html'):
                    yield os.path.join(root, f)


def main(argv):
    missing = []
    for path in html_files(argv):
        try:
            s = open(path, encoding='utf-8').read()
        except (OSError, UnicodeDecodeError):
            continue
        if FORM_MARK in s and GUARD_MARK not in s:
            missing.append(path)
    if not missing:
        print('✓ Schreibwerkstatt: alle Formulare haben die Namenspflicht (FB-NAME-REQUIRED).')
        return 0
    print(f'✗ {len(missing)} Schreibwerkstatt-Datei(en) OHNE Namenspflicht — Commit blockiert:')
    for p in missing:
        print(f'  {p}')
    print('\nFix: python3 scripts/inject_schreib_name.py <datei> — baut das '
          'FB-NAME-REQUIRED-Modul ein (kein namenloses Senden mehr).')
    return 1


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
