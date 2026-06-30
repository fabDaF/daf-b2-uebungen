#!/usr/bin/env python3
"""
fix_genus_buttons.py — Idempotenter Reparateur für nicht-kanonische Control-Buttons.

Die Klassen `btn btn-show` / `btn btn-reset` sind in fast keiner Lektion als CSS
definiert -> der Browser rendert hässliche graue Default-Buttons (Frank, 2026-06-30,
B1.1 1022G im Unterricht). Diese Buttons stehen in Genus-, Lückentext-, Zuordnungs-
und Satzbau-Tabs (Tab-Steuerleiste „Lösungen/Neu starten" UND per-Item-„Lösung").

Ersetzt sie durch kanonische inline-Pill-Buttons (CSS-unabhängig, generationsrobust).
Bestehende inline-Styles (z. B. margin-top) bleiben erhalten (Pill wird vorangestellt).

Beschriftung — NIE aus der Klasse ableiten (sie ist unzuverlässig: hunderte Dateien
haben btn-show auf dem Reset-Button und umgekehrt), sondern aus onclick + Original-
label:
  - onclick reset/neu  -> „↺ Neustart"
  - Originallabel „Lösungen"/„Lösungen zeigen"/„Lösung zeigen" -> „💡 Lösungen"
  - Originallabel „Lösung" (per-Item) + show-onclick           -> „💡 Lösung"
  - Originallabel „Neu starten"/„Reset"/„Neustart"             -> „↺ Neustart"
  - sonst: Originallabel bleibt, nur Restyle.
onclick und Timer-IDs bleiben immer unangetastet.

Aufruf:  python3 scripts/fix_genus_buttons.py [--dry-run] <Datei|Ordner> …
"""
import sys, re, glob, os

PILL = ("background:#f5f7ff;border:1px solid #c5cff5;border-radius:8px;"
        "padding:6px 16px;font-size:0.85em;color:#667eea;cursor:pointer;font-weight:600;")

RE_BTN     = re.compile(r'<button\b([^>]*)>(.*?)</button>', re.S)
RE_HASCLS  = re.compile(r'class="btn btn-(?:show|reset)"')
RE_ONCLICK = re.compile(r'onclick="([^"]*)"')
RE_STYLE   = re.compile(r'\s*style="([^"]*)"')
RE_CLSTOK  = re.compile(r'\s*class="btn btn-(?:show|reset)"')

_ENT = {'&ouml;':'ö','&Ouml;':'Ö','&auml;':'ä','&Auml;':'Ä','&uuml;':'ü','&Uuml;':'Ü','&szlig;':'ß','&amp;':'&'}
def _decode(s):
    for k,v in _ENT.items(): s = s.replace(k,v)
    return s

def label_for(onclick, original):
    oc = onclick.lower()
    if re.search(r'reset|neu', oc):
        return '↺ Neustart'
    norm = re.sub(r'^[\s💡👁🔄↺🔍✓]+', '', _decode(original)).strip().lower()
    if norm in ('lösungen', 'lösungen zeigen', 'lösung zeigen', 'lösungen anzeigen', 'alle lösungen'):
        return '💡 Lösungen'
    if norm in ('neu starten', 'neustart', 'reset', 'zurücksetzen', 'nochmal'):
        return '↺ Neustart'
    if norm == 'lösung' and re.search(r'show|loesung|lösung|solution', oc):
        return '💡 Lösung'
    return original  # unklar: Beschriftung erhalten, nur Restyle

def _repl(m):
    attrs, inner = m.group(1), m.group(2)
    if not RE_HASCLS.search(attrs):
        return m.group(0)
    onclick = (RE_ONCLICK.search(attrs) or (None,)) and (RE_ONCLICK.search(attrs).group(1) if RE_ONCLICK.search(attrs) else '')
    sm = RE_STYLE.search(attrs)
    existing = sm.group(1).strip() if sm else ''
    a = RE_STYLE.sub('', attrs)
    a = RE_CLSTOK.sub('', a)
    a = re.sub(r'\s+', ' ', a).rstrip()
    style = PILL + (' ' + existing if existing else '')
    label = label_for(onclick, inner)
    return '<button%s style="%s">%s</button>' % (a, style, label)

def fix(html):
    return RE_BTN.sub(_repl, html)

def iter_files(args):
    for a in args:
        if os.path.isdir(a):
            yield from glob.glob(os.path.join(a, '**', '*.html'), recursive=True)
        else:
            yield a

def main():
    dry = '--dry-run' in sys.argv
    args = [a for a in sys.argv[1:] if not a.startswith('-')]
    if not args:
        print("Aufruf: fix_genus_buttons.py [--dry-run] <Datei|Ordner> …"); sys.exit(2)
    changed = []
    for f in iter_files(args):
        try:
            html = open(f, encoding='utf-8').read()
        except Exception:
            continue
        new = fix(html)
        if new != html:
            changed.append(f)
            if not dry:
                open(f, 'w', encoding='utf-8').write(new)
    print("%s: %d Datei(en)." % ("Würde ändern" if dry else "Geändert", len(changed)))
    for f in changed:
        print("   " + f)

if __name__ == '__main__':
    main()
