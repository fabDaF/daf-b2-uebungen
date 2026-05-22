#!/usr/bin/env python3
"""fix_bad_quotes_b1_extended.py — Phase 1.4, repo-weit Bad-Quote-Erweiterung.

Räumt die Reste, die mein erstes Skript (fix_bad_quotes_b1.py mit 80-Zeichen-
Limit und Tag-Block) übrig gelassen hat:

  - Dialoge mit <span>/<strong> Tags innen, die per simple-Regex nicht
    erfassbar waren
  - Schreibwerkstatt-Beispiele (.schreib-beispiel) mit >80 Zeichen Text

Strategie: Line-basiert. Pro Zeile mit `„`-Zeichen suchen wir das letzte
`"` (ASCII-Quote) vor einem schließenden Block-Tag und ersetzen es durch
`"` (U+201C), wenn unbalanciert (Anzahl `„` > Anzahl `"` im davor-Teil).

Aufruf:
    python3 scripts/fix_bad_quotes_b1_extended.py --dry-run [DATEI ...]
    python3 scripts/fix_bad_quotes_b1_extended.py [DATEI ...]
"""
from __future__ import annotations
import argparse
import glob
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

# ASCII " vor schließendem Block-Tag
CLOSING_TAG_PATTERN = re.compile(r'"(\s*</(?:p|div|span|li|em|strong)[\s>])')


def fix_line(line: str) -> tuple[str, int]:
    """Fix all bad-quote endings in a single line. Returns (new_line, count)."""
    if '„' not in line:
        return line, 0
    fixed = 0
    # Iteratively find each match — line might have multiple
    pos = 0
    out = []
    while pos < len(line):
        m = CLOSING_TAG_PATTERN.search(line, pos)
        if not m:
            out.append(line[pos:])
            break
        before = line[:m.start()]
        if before.count('„') > before.count('“'):
            # Unbalanced — this is a bad quote
            out.append(line[pos:m.start()])
            out.append('“')
            pos = m.end() - len(m.group(1))
            out.append(m.group(1))
            pos = m.end()
            fixed += 1
        else:
            # Balanced — leave alone
            out.append(line[pos:m.end()])
            pos = m.end()
    return ''.join(out), fixed


def process(path: Path, dry_run: bool) -> int:
    text = path.read_text(encoding='utf-8')
    lines = text.split('\n')
    total = 0
    for i, line in enumerate(lines):
        new_line, n = fix_line(line)
        if n:
            lines[i] = new_line
            total += n
    if total > 0 and not dry_run:
        path.write_text('\n'.join(lines), encoding='utf-8')
    return total


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--dry-run', action='store_true')
    ap.add_argument('files', nargs='*')
    args = ap.parse_args()
    if args.files:
        files = [Path(f) for f in args.files]
    else:
        pattern = str(REPO_ROOT / 'htmlS' / 'B1.1' / 'DE_B1_*.html')
        files = sorted(Path(p) for p in glob.glob(pattern))

    changed = 0
    total_fixes = 0
    for f in files:
        n = process(f, dry_run=args.dry_run)
        if n:
            changed += 1
            total_fixes += n
            try:
                display = f.resolve().relative_to(REPO_ROOT)
            except ValueError:
                display = f
            print(f'  {n:>3} × {display}')

    verb = 'würden geändert' if args.dry_run else 'geändert'
    print(f'\n{changed} Dateien {verb}, {total_fixes} Bad-Quotes gefixt.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
