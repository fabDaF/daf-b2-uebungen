#!/usr/bin/env python3
"""
check_genus_buttons.py — Guardrail gegen nicht-kanonische Genus-Control-Buttons.

Der Genus-Tab nutzte lange die undefinierten CSS-Klassen `btn btn-show` /
`btn btn-reset` für „Lösungen" / „Neu starten". Diese Klassen sind in fast keiner
Lektion definiert -> der Browser rendert hässliche graue Default-Buttons (Frank,
2026-06-30, B1.1 1022G mitten im Unterricht). Kanonisch sind inline-gestylte
Pill-Buttons mit den Beschriftungen „💡 Lösungen" / „↺ Neustart".

Meldet jede Datei mit `class="btn btn-show"` oder `class="btn btn-reset"`
(Exit-Code 1). Vor jedem Lektions-Commit laufen lassen, zusammen mit den übrigen
check_*-Skripten. Reparatur: scripts/fix_genus_buttons.py
"""
import sys, re, glob, os

PAT = re.compile(r'class="btn btn-(?:show|reset)"')

def iter_files(args):
    if args:
        for a in args:
            if os.path.isdir(a):
                yield from glob.glob(os.path.join(a, '**', '*.html'), recursive=True)
            else:
                yield a
    else:
        yield from glob.glob('**/*.html', recursive=True)

def main():
    args = [a for a in sys.argv[1:] if not a.startswith('-')]
    offenders = []
    checked = 0
    for f in iter_files(args):
        try:
            html = open(f, encoding='utf-8').read()
        except Exception:
            continue
        checked += 1
        if PAT.search(html):
            offenders.append(f)
    if offenders:
        print("✗ Nicht-kanonische Genus-Buttons (btn btn-show/btn-reset) in %d Datei(en):" % len(offenders))
        for f in offenders:
            print("   " + f)
        print("Reparatur: python3 scripts/fix_genus_buttons.py <Datei|Ordner> …")
        sys.exit(1)
    print("✓ Alle %d geprüften Dateien nutzen kanonische Genus-Buttons (Pill-Stil)." % checked)
    sys.exit(0)

if __name__ == '__main__':
    main()
