#!/usr/bin/env python3
"""check_quotes.py — Gate: deutsche Anführungszeichen (daf-audit Showstopper).

Findet „…"-Paare, die mit ASCII U+0022 statt U+201C schließen.
Gehärtete Fassung des kanonischen Regex aus daf-audit/SKILL.md: HTML-Tags
werden als Ganzes konsumiert (`<[^>]*>`), damit Zitate, die über Inline-
Elemente laufen (z. B. Lückentext-Inputs: „… für <input …> gehalten!“),
keine Falsch-Positiven erzeugen und Attribut-Delimiter nie als schließendes
Anführungszeichen missdeutet werden. Vor jedem Lektions-Commit laufen
lassen, zusammen mit den übrigen check_*-Skripten.

Bekannte Grenze: In JS-Daten kann ein Zitat absichtlich über zwei String-
Literale laufen (pre/ans/post-Muster) — das meldet der Check als Treffer,
obwohl es korrekt ist. Lösung: Glosse ohne Anführungszeichen formulieren.

Aufruf:
    python3 scripts/check_quotes.py            # ganzes Repo
    python3 scripts/check_quotes.py a.html b/  # einzelne Dateien/Ordner

Exit 0 = sauber. Exit 1 = Befunde (Commit blockiert).
"""
import os
import re
import sys

BAD = re.compile(r'„((?:[^„"“”\n<]|<[^>]*>){1,80})"')
SKIP_DIRS = {'daf-archiv', '.git', 'node_modules', 'backup', 'quelltexte'}


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
    findings = []
    total = 0
    for path in html_files(argv):
        try:
            content = open(path, encoding='utf-8').read()
        except (OSError, UnicodeDecodeError):
            continue
        hits = BAD.findall(content)
        if hits:
            findings.append((path, len(hits)))
            total += len(hits)
    if not findings:
        print('✓ Anführungszeichen sauber — kein „…"-Paar mit ASCII-Schluss.')
        return 0
    findings.sort(key=lambda x: -x[1])
    print(f'✗ {len(findings)} Datei(en) mit ASCII-schließenden Anführungszeichen '
          f'({total} Treffer, daf-audit-Showstopper):')
    for path, n in findings:
        print(f'  {n:4d}  {path}')
    print('\nFix: schließendes U+0022 durch U+201C (“) ersetzen — '
          'Auto-Fix-Regex siehe daf-audit/SKILL.md.')
    return 1


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
