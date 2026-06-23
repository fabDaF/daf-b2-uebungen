#!/usr/bin/env python3
"""
inject_schreib_pad.py — idempotenter Reparateur für das Schreibwerkstatt-Padding.

Fügt den id-bewussten FB-SCHREIB-PAD-CSS-Block vor dem ersten </style> ein:

    /* FB-SCHREIB-PAD: Schreibwerkstatt-Inhalt einruecken, Banner randlos */
    #<sid> { padding: 28px 30px; }
    #<sid> > .tab-banner { width: calc(100% + 60px); max-width: none; margin: -28px -30px 18px; }
    @media (max-width: 600px) {
      #<sid> { padding: 18px 16px; }
      #<sid> > .tab-banner { width: calc(100% + 32px); margin: -18px -16px 14px; }
    }

`<sid>` ist die tatsächliche id des Schreibwerkstatt-Tabs (sec-schreib, sec-5,
tab-schreib, …) — wird zur Laufzeit ermittelt, nicht geraten.

Idempotent: Dateien, deren Schreibwerkstatt-Inhalt bereits eingerückt ist
(`.sec-inner`-Wrapper ODER bestehende Padding-Regel), werden übersprungen.
CSS-only — Markup wird nicht angefasst.

Aufruf:
  python3 scripts/inject_schreib_pad.py datei.html …
  python3 scripts/inject_schreib_pad.py            # ganzes Repo ab CWD
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from schreib_pad_lib import find_schreib_section, is_padded  # noqa: E402

EXCLUDE_DIRS = {'.git', 'daf-archiv', 'backup', 'termin-redirect',
                'node_modules', 'ir'}

BLOCK = (
    "\n/* FB-SCHREIB-PAD: Schreibwerkstatt-Inhalt einruecken, Banner randlos */\n"
    "#{sid} {{ padding: 28px 30px; }}\n"
    "#{sid} > .tab-banner {{ width: calc(100% + 60px); max-width: none; margin: -28px -30px 18px; }}\n"
    "@media (max-width: 600px) {{\n"
    "  #{sid} {{ padding: 18px 16px; }}\n"
    "  #{sid} > .tab-banner {{ width: calc(100% + 32px); margin: -18px -16px 14px; }}\n"
    "}}\n"
)


def fix_one(path: str):
    """Return 'fixed' | 'ok' | 'no-id' | 'none' | 'no-style'."""
    try:
        t = open(path, encoding='utf-8', errors='replace').read()
    except OSError:
        return 'none'
    tag, sid, seg = find_schreib_section(t)
    if seg is None:
        return 'none'
    if is_padded(t, tag, sid, seg):
        return 'ok'
    if not sid:
        return 'no-id'
    pos = t.find('</style>')
    if pos == -1:
        return 'no-style'
    new = t[:pos] + BLOCK.format(sid=sid) + t[pos:]
    with open(path, 'w', encoding='utf-8') as f:
        f.write(new)
    return 'fixed'


def collect_files(args):
    if args:
        return [a for a in args if a.endswith('.html')]
    files = []
    for root, dirs, names in os.walk('.'):
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
        for n in names:
            if n.endswith('.html'):
                files.append(os.path.join(root, n))
    return files


def main():
    files = collect_files(sys.argv[1:])
    counts = {'fixed': [], 'ok': 0, 'no-id': [], 'none': 0, 'no-style': []}
    for p in files:
        r = fix_one(p)
        if r in ('fixed', 'no-id', 'no-style'):
            counts[r].append(p)
        else:
            counts[r] += 1
    print(f"Geprüft: {len(files)} Dateien")
    print(f"  repariert        : {len(counts['fixed'])}")
    print(f"  schon ok         : {counts['ok']}")
    print(f"  kein Schreib-Tab : {counts['none']}")
    if counts['no-id']:
        print(f"  OHNE id (manuell): {len(counts['no-id'])}")
        for p in counts['no-id']:
            print(f"      {p}")
    if counts['no-style']:
        print(f"  OHNE </style>    : {len(counts['no-style'])}")
        for p in counts['no-style']:
            print(f"      {p}")
    for p in counts['fixed']:
        print(f"  ✔ {p}")


if __name__ == '__main__':
    main()
