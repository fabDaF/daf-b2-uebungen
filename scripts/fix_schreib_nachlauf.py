#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""fix_schreib_nachlauf.py — Pflicht-Nachlauf zu add-schreibwerkstatt-v2.py.

Der Produzent stammt aus der Zeit vor mehreren heute geltenden Regeln und hat
drei Defekte, die jede frisch gepatchte Lektion mitbringt. Alle drei sind hier
gebündelt und idempotent — nach dem Produzenten IMMER dieses Skript laufen
lassen (Fund 2026-08-24 beim Nachrüsten der B1-Grammatik-Lektionen).

  A) VERFRÜHTER INIT-AUFRUF
     Der Produzent hängt `initSchreibwerkstatt();` in die BESTEHENDE Init-Kette
     der Datei, definiert die Funktion aber in einem SPÄTEREN <script>-Block.
     Function Declarations werden nur innerhalb ihres eigenen Blocks gehoben —
     der Aufruf wirft daher beim Laden „ReferenceError: initSchreibwerkstatt is
     not defined" und bricht die restliche Init-Kette ab (Timer, Wortzähler,
     Autosave). Der Aufruf bekommt einen typeof-Guard; ausgeführt wird die
     Initialisierung ohnehin vom Hook am Dateiende (FB-SCHREIB-INIT-FIX aus
     scripts/fix_schreib_init.py, das VORHER laufen muss).

  B) NICHT-NUMERISCHE SECTION-ID
     Der Produzent vergibt die Ersatz-Id "sec-schreib". Harmlos, solange die
     Tab-Funktion positionell umschaltet (forEach mit Index). Sucht sie dagegen
     per getElementById('sec-' + n), zeigt der neue Tab ins Leere und wirft beim
     Klick einen TypeError — der Tab ist tot (Fund an B1 1015G).

  C) FALSCHE TAB-POSITION
     „Schreiben ist IMMER der letzte Tab" gilt seit 2026-06-29, der Produzent
     ist älter und setzt den Tab VOR einen vorhandenen Wortschatz-Tab
     (check_schreib_last.py meldet das). Nav-Button und Section wandern ans
     Ende, die Nav-Indizes werden nach DOM-Reihenfolge neu vergeben. Bei
     ID-basierten Tab-Funktionen bricht dieser Schritt bewusst ab: dort müssten
     auch alle JS-Selektoren mitgezogen werden — Handarbeit.

Aufruf:  python3 scripts/fix_schreib_nachlauf.py datei1.html [datei2.html …]
"""
import re
import sys

ID_BASIERT = re.compile(r"getElementById\(\s*['\"](?:sec|tab)-?['\"]\s*\+\s*\w+\s*\)")
EARLY_CALL = re.compile(r'^([ \t]*)initSchreibwerkstatt\(\);[ \t]*$', re.M)
DEF = 'function initSchreibwerkstatt('
# Achtung: class="section-title"/"section-sub" dürfen NICHT mitmatchen —
# sonst schneidet der Verschiebe-Schritt an der falschen Stelle
# (Fund 2026-08-24 an B1 1052G).
SECTION = r'[ \t]*<(?:div|section) class="section(?:\s+[^"]*)?"[^>]*>'


TAG = re.compile(r'<(/?)(div|section)\b[^>]*?(/?)>|<script\b[^>]*>|</script>', re.I)


def _matched_block(t, start):
    """(start, ende) des Elements, das bei `start` öffnet — mit Tag-Zählung.

    Nötig, weil ein Schnitt „bis zur nächsten Section" die schließenden </div>
    der laufenden Section abschneidet: die verschobene Section landet dann
    verschachtelt im Nachbarn und check_nested_sections.py schlägt an
    (Fund 2026-08-24 an B1 1052G/1055G). Inhalte von <script> werden
    übersprungen — dort steht HTML in Strings.
    """
    tiefe = 0
    im_script = False
    for m in TAG.finditer(t, start):
        roh = m.group(0).lower()
        if roh.startswith('<script'):
            im_script = True
            continue
        if roh == '</script>':
            im_script = False
            continue
        if im_script:
            continue
        if m.group(3):          # selbstschließend
            continue
        if m.group(1):          # schließend
            tiefe -= 1
            if tiefe == 0:
                return start, m.end()
        else:
            tiefe += 1
    return None


def _sections(t):
    return list(re.finditer(SECTION, t))


def _schreib_section(t):
    """(start, ende) der Section, die die Schreibfelder enthält — tag-genau."""
    secs = _sections(t)
    for i, s in enumerate(secs):
        grenze = secs[i + 1].start() if i + 1 < len(secs) else len(t)
        if 'schreib-mini-textarea' not in t[s.start():grenze]:
            continue
        # Beginn des Öffnungs-Tags (ohne Einrückung liefert _sections bereits
        # die Zeile mit); für die Tag-Zählung genau auf das '<' setzen.
        oeffnung = t.index('<', s.start())
        block = _matched_block(t, oeffnung)
        if not block:
            return None
        return s.start(), block[1]
    return None


def guard_early_call(t):
    """A) verfrühten initSchreibwerkstatt()-Aufruf in einen typeof-Guard hüllen."""
    d = t.find(DEF)
    if d < 0:
        return t, None
    treffer = [m for m in EARLY_CALL.finditer(t) if m.start() < d]
    if not treffer:
        return t, None
    for m in reversed(treffer):
        e = m.group(1)
        t = t[:m.start()] + (
            f"{e}// Guard: die Funktion steht in einem späteren <script>-Block und ist\n"
            f"{e}// hier noch nicht definiert. Initialisiert wird am Dateiende\n"
            f"{e}// (FB-SCHREIB-INIT-FIX).\n"
            f"{e}if (typeof initSchreibwerkstatt === 'function') initSchreibwerkstatt();"
        ) + t[m.end():]
    return t, f'{len(treffer)} verfrühte(r) Init-Aufruf(e) entschärft'


def numerische_id(t):
    """B) id="sec-schreib" numerisch machen, wo die Tab-Funktion per ID sucht."""
    if 'id="sec-schreib"' not in t or not ID_BASIERT.search(t):
        return t, None
    ids = re.findall(r'<(?:div|section) class="section(?:\s+[^"]*)?" id="([^"]+)"', t)
    if 'sec-schreib' not in ids:
        return t, None
    ziel = f'sec-{ids.index("sec-schreib")}'
    if f'id="{ziel}"' in t:
        return t, f'ABBRUCH: {ziel} ist schon vergeben — Handarbeit'
    t = (t.replace('id="sec-schreib"', f'id="{ziel}"')
          .replace('#sec-schreib', f'#{ziel}')
          .replace("'sec-schreib'", f"'{ziel}'"))
    return t, f'sec-schreib -> {ziel}'


def _nav_button(t):
    for pat in (r'[ \t]*<button class="nav-btn"[^>]*>\s*<span class="nav-emoji">\U0001F4E8</span>'
                r'\s*<span class="nav-label">Schreib\w*</span>\s*</button>\n?',
                r'[ \t]*<div class="nav-btn"[^>]*>\s*<span class="nav-emoji">\U0001F4E8</span>'
                r'\s*<span class="nav-label">Schreib\w*</span>\s*</div>\n?'):
        m = re.search(pat, t)
        if m:
            return m
    return None


def schreiben_ans_ende(t):
    """C) Nav-Button und Section ans Ende; Nav-Indizes neu vergeben."""
    m = _nav_button(t)
    if not m:
        return t, None
    # Schon letzter Tab? Dann nichts tun.
    navs = list(re.finditer(r'<(?:button|div) class="nav-btn"[^>]*>.*?</(?:button|div)>', t, re.S))
    if navs and 'Schreib' in navs[-1].group(0):
        return t, None
    if ID_BASIERT.search(t):
        return t, 'ABBRUCH: ID-basierte Tab-Funktion — Verschieben ist Handarbeit'

    original = t
    btn = m.group(0).strip()
    t = t[:m.start()] + t[m.end():]

    # Einfügepunkt = HINTER dem letzten Nav-Button-ELEMENT. Nicht per
    # rfind('nav-btn') suchen: dieser String steht auch im JavaScript
    # (querySelectorAll('.nav-btn')), der Button landete dann mitten im
    # <script> und die Seite starb mit einem SyntaxError (Fund 2026-08-24).
    letzte = None
    for mm in re.finditer(r'<(?:button|div) class="nav-btn[^"]*"[^>]*>.*?</(?:button|div)>', t, re.S):
        letzte = mm
    if letzte is None:
        return original, 'ABBRUCH: kein Nav-Button gefunden'
    za = t.rfind('\n', 0, letzte.start()) + 1
    einr = re.match(r'[ \t]*', t[za:]).group(0) or '    '
    t = t[:letzte.end()] + '\n' + einr + btn + t[letzte.end():]

    ziel = _schreib_section(t)
    if not ziel:
        return original, 'ABBRUCH: Schreiben-Section nicht gefunden'
    a, b = ziel
    block = t[a:b]
    t = t[:a] + t[b:]

    fuss = t.find('<div class="author-footer">')
    if fuss < 0:
        fuss = t.rfind('</div><!-- /container -->')
    if fuss < 0:
        return original, 'ABBRUCH: kein Einfügepunkt vor dem Footer'
    za = t.rfind('\n', 0, fuss) + 1
    t = t[:za] + block.rstrip('\n') + '\n\n' + t[za:]

    fn = 'showSection' if 'showSection(' in t else 'showTab'
    zaehler = [0]

    def neu(mm):
        i = zaehler[0]
        zaehler[0] += 1
        return f'{mm.group(1)}{fn}({i})"'

    t = re.sub(r'(<(?:button|div) class="nav-btn[^"]*"\s+onclick=")' + fn + r'\(\d+\)"', neu, t)
    return t, f'Schreiben ans Ende, {zaehler[0]} Nav-Indizes neu vergeben'


def transform(t):
    meldungen = []
    for schritt in (guard_early_call, numerische_id, schreiben_ans_ende):
        t, msg = schritt(t)
        if msg:
            meldungen.append(msg)
    return t, meldungen


def main():
    dateien = [a for a in sys.argv[1:] if a.endswith('.html')]
    if not dateien:
        print('Aufruf: python3 scripts/fix_schreib_nachlauf.py datei.html …')
        return 2
    fehler = 0
    for p in dateien:
        s = open(p, encoding='utf-8').read()
        neu, meldungen = transform(s)
        if neu != s:
            open(p, 'w', encoding='utf-8').write(neu)
        name = p.split('/')[-1]
        if meldungen:
            for m in meldungen:
                print(f'  {name}: {m}')
                if m.startswith('ABBRUCH'):
                    fehler += 1
        else:
            print(f'  {name}: nichts zu tun')
    return 1 if fehler else 0


if __name__ == '__main__':
    sys.exit(main())
