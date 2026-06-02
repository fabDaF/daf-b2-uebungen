#!/usr/bin/env python3
"""
check_serif.py — Sicherheitsnetz für Fließtext-Serifenschrift.

Regel (daf-lesetext §1): Jeder Fließtext-Container (.story-text / .lese-text)
MUSS eine Serifenschrift tragen. Fehlt die font-family in ALLEN Base-Regeln
eines Containers, erbt der Lesetext die Sans-Serif-Schrift des <body> — genau
der Fehler, den Frank am 2026-06-02 im Unterricht gesehen hat.

Logik (bewusst aggregierend):
  - Pro Datei und pro Selektor werden ALLE Base-Regeln gesammelt
    (z. B. Primärregel + Media-Query-Override + zweite max-width-Regel).
  - Setzt MINDESTENS EINE dieser Regeln eine Serifenschrift, ist der
    Container in Ordnung. Override-Regeln (nur max-width, nur font-size in
    @media) brauchen die font-family nicht erneut.
  - Setzt KEINE Regel eine Serifenschrift -> Treffer, Exit-Code 1.

Aufruf:
  python3 scripts/check_serif.py                # ganzes Repo (htmlS + daf-materialien)
  python3 scripts/check_serif.py datei.html …   # einzelne Dateien

Vor jedem Lektions-Commit laufen lassen (analog check_wortbank.py).
"""
import re
import sys
import os

TARGETS = ('.story-text', '.lese-text')


def has_serif(value: str) -> bool:
    v = value.lower()
    if 'sans-serif' in v and 'serif' not in v.replace('sans-serif', ''):
        # nur sans-serif genannt -> KEINE Serifenschrift
        return False
    return ('georgia' in v) or ('times' in v) or ('serif' in v.replace('sans-serif', ''))


def style_css(txt: str) -> str:
    return '\n'.join(re.findall(r'<style[^>]*>(.*?)</style>', txt, re.S | re.I))


def file_offenders(path: str):
    """Liefert Liste der Selektoren ohne jede Serif-Base-Regel in dieser Datei."""
    try:
        txt = open(path, encoding='utf-8', errors='replace').read()
    except OSError:
        return []
    css = style_css(txt)
    bad = []
    for sel in TARGETS:
        # alle Base-Regeln "SELECTOR { … }" (exakter Selektor, keine .sel p / .sel .x)
        blocks = re.findall(re.escape(sel) + r'\s*\{([^{}]*)\}', css)
        if not blocks:
            continue  # Container kommt nicht vor -> nichts zu prüfen
        serif_found = False
        for body in blocks:
            fam = re.search(r'font-family\s*:\s*([^;}]+)', body)
            if fam and has_serif(fam.group(1)):
                serif_found = True
                break
        if not serif_found:
            bad.append(sel)
    return bad


def collect_files(args):
    if args:
        return args
    files = []
    for base in ('htmlS', 'daf-materialien'):
        for root, dirs, names in os.walk(base):
            if '/.git' in root or 'daf-archiv' in root:
                continue
            for n in names:
                if n.endswith('.html'):
                    files.append(os.path.join(root, n))
    return files


def main():
    files = collect_files(sys.argv[1:])
    offenders = {}
    for p in files:
        bad = file_offenders(p)
        if bad:
            offenders[p] = bad

    if offenders:
        print(f"❌ {len(offenders)} Datei(en) mit Fließtext-Container OHNE Serifenschrift:")
        for p in sorted(offenders):
            print(f"   {p}  ->  {', '.join(offenders[p])} (erbt Sans-Serif vom <body>)")
        print("\nFix: font-family: Georgia, 'Times New Roman', serif;  in die Base-Regel.")
        sys.exit(1)

    print(f"✅ Alle Fließtext-Container tragen Serifenschrift ({len(files)} Dateien geprüft).")
    sys.exit(0)


if __name__ == '__main__':
    main()
