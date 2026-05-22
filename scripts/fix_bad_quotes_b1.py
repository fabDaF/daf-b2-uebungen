#!/usr/bin/env python3
"""fix_bad_quotes_b1.py — Phase 1, Skript 1.

Ersetzt deutsche Anführungszeichen-Paare, in denen das schließende
Anführungszeichen ein ASCII-U+0022 statt des typografisch korrekten
U+201C ist:

    „Text"   →   „Text"
    U+201E   →   U+201E (öffnend, korrekt)
    U+0022   →   U+201C (schließend, repariert)

Aufruf:
    python3 scripts/fix_bad_quotes_b1.py --dry-run [DATEI ...]
    python3 scripts/fix_bad_quotes_b1.py [DATEI ...]

Ohne DATEI-Argumente läuft das Skript über alle htmlS/B1.1/DE_B1_*.html.
"""
from __future__ import annotations
import argparse
import glob
import re
import sys
from pathlib import Path

PATTERN = re.compile(r'„([^„"“\n<>]{1,80})"')

REPO_ROOT = Path(__file__).resolve().parent.parent


def fix_text(text: str) -> tuple[str, int]:
    """Ersetze „X" → „X". Gibt neuen Text und Trefferanzahl zurück."""
    count = 0

    def repl(m: re.Match) -> str:
        nonlocal count
        count += 1
        return f'„{m.group(1)}“'

    new = PATTERN.sub(repl, text)
    return new, count


def process(path: Path, dry_run: bool) -> int:
    text = path.read_text(encoding='utf-8')
    new, n = fix_text(text)
    if n == 0:
        return 0
    if not dry_run:
        path.write_text(new, encoding='utf-8')
    return n


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--dry-run', action='store_true',
                    help='Nur Treffer zählen, nichts schreiben')
    ap.add_argument('files', nargs='*', help='Dateien (Default: alle B1)')
    args = ap.parse_args()

    if args.files:
        files = [Path(f) for f in args.files]
    else:
        pattern = str(REPO_ROOT / 'htmlS' / 'B1.1' / 'DE_B1_*.html')
        files = sorted(Path(p) for p in glob.glob(pattern))

    if not files:
        print('Keine Dateien gefunden.', file=sys.stderr)
        return 1

    total_hits = 0
    changed = 0
    for f in files:
        n = process(f, dry_run=args.dry_run)
        if n:
            changed += 1
            total_hits += n
            try:
                display = f.resolve().relative_to(REPO_ROOT)
            except ValueError:
                display = f
            print(f'  {n:>3} × {display}')

    verb = 'würden geändert' if args.dry_run else 'geändert'
    print(f'\n{changed} Dateien {verb}, {total_hits} Anführungszeichen-Paare gefixt.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
