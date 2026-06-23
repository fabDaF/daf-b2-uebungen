#!/usr/bin/env python3
"""
check_schreib_pad.py — Sicherheitsnetz für das Schreibwerkstatt-Padding.

Regel (daf-kern §1): Der Inhalt jedes Tabs steht eingerückt (sec-inner,
padding 28px 30px), der Banner bleibt randlos. Schreibwerkstatt-Tabs, die als
nackte `<div class="section" id="…">` ohne `.sec-inner` angehängt wurden, kleben
randlos am Container — das Layout wirkt „an den Rand gequetscht". Genau dieser
Fehler ist Frank am 2026-06-19 UND erneut am 2026-06-23 (A2 2014R) im Unterricht
aufgefallen, obwohl ein erster Reparatur-Lauf am 2026-06-19 „erledigt" gemeldet
hatte — er hatte schlicht Dateien übersehen, und es gab kein Sicherheitsnetz.
Dieses Skript IST das Sicherheitsnetz.

Logik (zentral in schreib_pad_lib.py, von Prüfer und Reparateur geteilt):
  Ein Schreibwerkstatt-Tab ist in Ordnung, wenn ENTWEDER sein Inhalt in einem
  `.sec-inner`-Wrapper liegt ODER eine CSS-Regel `#<sid> { … padding … }` der
  Section horizontales Padding gibt. Sonst -> Treffer, Exit-Code 1.

Aufruf:
  python3 scripts/check_schreib_pad.py                 # ganzes Repo ab CWD
  python3 scripts/check_schreib_pad.py datei.html …    # einzelne Dateien

Vor jedem Lektions-Commit laufen lassen — zusammen mit check_serif.py,
check_wortbank.py und check_genus.py.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from schreib_pad_lib import classify  # noqa: E402

EXCLUDE_DIRS = {'.git', 'daf-archiv', 'backup', 'termin-redirect',
                'node_modules', 'ir'}


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
    offenders = []   # (path, sid)
    noid = []        # (path,)
    checked = 0
    for p in files:
        try:
            t = open(p, encoding='utf-8', errors='replace').read()
        except OSError:
            continue
        kind, sid = classify(t)
        if kind == 'none':
            continue
        checked += 1
        if kind == 'offender':
            offenders.append((p, sid))
        elif kind == 'no-id':
            noid.append(p)

    if offenders or noid:
        if offenders:
            print(f"❌ {len(offenders)} Schreibwerkstatt-Tab(s) OHNE Padding "
                  f"(Inhalt klebt am Container-Rand):")
            for p, sid in sorted(offenders):
                print(f"   {p}   (id={sid})")
            print("\nFix: python3 scripts/inject_schreib_pad.py <dateien>")
        if noid:
            print(f"\n⚠ {len(noid)} Schreibwerkstatt-Tab(s) OHNE id-Attribut "
                  f"(Handarbeit nötig):")
            for p in sorted(noid):
                print(f"   {p}")
        sys.exit(1)

    print(f"✅ Alle Schreibwerkstatt-Tabs sind korrekt eingerückt "
          f"({checked} Tabs geprüft).")
    sys.exit(0)


if __name__ == '__main__':
    main()
