#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""add_wortschatz_tab.py — legt einer Lektion einen Wortschatz-Tab an (vor Schreiben).

Es gibt bisher nur inject_wortschatz.py — das NORMALISIERT einen vorhandenen
Wortschatz-Tab auf das kanonische Muster, kann aber keinen anlegen. Dieses
Skript erzeugt das Gerüst: Nav-Button, Section, Datenarray und einen minimalen
Bau-Stub. Die kanonische Mechanik spielt danach inject_wortschatz.py ein —
eine Quelle der Wahrheit, hier wird nichts davon kopiert.

Die Wörter kommen aus einer JSON-Datei (Liste von Einträgen im schema-adaptiven
Format, das initWortschatz liest):
    {"type":"n","en":"the note","artikel":"der","de":"Zettel","plural":"Zettel"}
    {"type":"v","en":"to tidy up","de":"aufräumen"}

Aufruf:  python3 scripts/add_wortschatz_tab.py lektion.html woerter.json
Danach:  python3 scripts/inject_wortschatz.py lektion.html
"""
import json
import re
import sys

ID_BASIERT = re.compile(r"getElementById\(\s*['\"]sec-['\"]\s*\+\s*\w+\s*\)")


SEC_TAG = re.compile(r'<(?:div|section)\b[^>]*>')


def _sections(t):
    """Ids aller Tab-Sections in DOM-Reihenfolge — unabhängig von der
    Attribut-Reihenfolge (manche Dateien schreiben id vor class)."""
    ids = []
    for m in SEC_TAG.finditer(t):
        tag = m.group(0)
        klasse = re.search(r'class="([^"]*)"', tag)
        if not klasse or 'section' not in klasse.group(1).split():
            continue
        ident = re.search(r'id="([^"]*)"', tag)
        ids.append(ident.group(1) if ident else '')
    return ids


def transform(t, daten):
    # Prüfen auf das ELEMENT bzw. den Tab — nicht auf irgendein Vorkommen des
    # Namens: mehrere Lektionen tragen verwaiste #wortschatzContainer-CSS-Regeln,
    # obwohl der Tab fehlt (Fund 2026-08-24 an B1 2012G).
    if re.search(r'id="wortschatzContainer"', t) or re.search(
            r'<span class="nav-label">\s*Wortschatz\s*</span>', t):
        return t, 'hat schon einen Wortschatz-Tab'

    m = re.search(r'[ \t]*<(?:button|div) class="nav-btn"[^>]*>\s*<span class="nav-emoji">\U0001F4E8</span>'
                  r'\s*<span class="nav-label">Schreib\w*</span>\s*</(?:button|div)>', t)
    if not m:
        return t, 'ABBRUCH: Schreiben-Nav-Button nicht gefunden (erst Schreibwerkstatt anlegen)'

    IDX = '__WS_IDX__'
    einr = re.match(r'[ \t]*', m.group(0)).group(0) or '    '
    fn = 'showSection' if 'showSection(' in t else 'showTab'
    ws_btn = (f'{einr}<{"button" if "<button" in m.group(0) else "div"} class="nav-btn" '
              f'onclick="{fn}({IDX})"><span class="nav-emoji">\U0001F520</span>'
              f'<span class="nav-label">Wortschatz</span>'
              f'</{"button" if "<button" in m.group(0) else "div"}>\n')
    t = t[:m.start()] + ws_btn + t[m.start():]

    kandidaten = list(re.finditer(r'[ \t]*<(?:div|section) class="section(?:\s+[^"]*)?" id="([^"]+)"[^>]*>', t))
    schreib = None
    for i, mm in enumerate(kandidaten):
        ende = kandidaten[i + 1].start() if i + 1 < len(kandidaten) else len(t)
        if 'schreib-mini-textarea' in t[mm.start():ende]:
            schreib = mm
            break
    if not schreib:
        return t, 'ABBRUCH: Schreiben-Section nicht gefunden'

    ws_sec = ('  <div class="section" id="__WS_ID__">\n'
              '    <h2>\U0001F520 Wortschatz</h2>\n'
              '    <div class="btn-row" style="display:flex;gap:6px;margin-bottom:14px;">\n'
              '      <button class="btn" onclick="showWortschatzLoesung()">\U0001F4A1 Lösungen</button>\n'
              '      <button class="btn" onclick="resetWortschatz()">↺ Neustart</button>\n'
              '    </div>\n'
              '    <div id="wortschatzContainer"></div>\n'
              '  </div>\n\n')
    t = t[:schreib.start()] + ws_sec + t[schreib.start():]

    ids = _sections(t)
    pos = ids.index('__WS_ID__')
    if ID_BASIERT.search(t):
        alt_schreib = ids[pos + 1]
        t = (t.replace(f'id="{alt_schreib}"', f'id="sec-{pos + 1}"')
              .replace(f"'{alt_schreib}'", f"'sec-{pos + 1}'")
              .replace(f'#{alt_schreib}', f'#sec-{pos + 1}'))
        t = t.replace('__WS_ID__', f'sec-{pos}')
    else:
        t = t.replace('__WS_ID__', 'sec-wortschatz')
    # Schreiben-Nav-Button rückt eine Position weiter
    t = re.sub(r'(onclick="' + fn + r'\()\d+(\)"[^>]*><span class="nav-emoji">\U0001F4E8)',
               lambda mm: f'{mm.group(1)}{pos + 1}{mm.group(2)}', t)
    t = t.replace(IDX, str(pos))

    # Hat die Datei die kanonische Mechanik schon (Tab war verlorengegangen,
    # Daten und initWortschatz sind aber noch da), fehlt nur das Gerüst — dann
    # KEINEN zweiten Datensatz und keinen Stub anhängen: der spätere
    # Funktionsblock würde die kanonische Fassung überschreiben.
    if 'function initWortschatz' in t:
        return t, f'Wortschatz-Tab an Position {pos} angelegt (Daten und Mechanik waren schon da)'

    eintraege = ',\n'.join('  ' + json.dumps(d, ensure_ascii=False) for d in daten)
    block = ('\n<script>\n/* ===== Wortschatz ===== */\nvar WORTSCHATZ = [\n' + eintraege + '\n];\n\n'
             'function initWortschatz(){\n'
             '  var c=document.getElementById("wortschatzContainer"); if(!c) return; c.innerHTML="";\n'
             '  WORTSCHATZ.forEach(function(item){\n'
             '    var div=document.createElement("div"); div.className="luecken-item";\n'
             '    div.textContent=item.en+" — "+(item.artikel?item.artikel+" ":"")+item.de;\n'
             '    c.appendChild(div);\n  });\n}\n'
             'function showWortschatzLoesung(){}\n'
             'function resetWortschatz(){ initWortschatz(); }\n'
             'document.addEventListener("DOMContentLoaded", function(){ initWortschatz(); });\n'
             '</script>\n')
    p = t.rfind('</body>')
    if p < 0:
        p = t.rfind('</html>')
    if p < 0:
        return t, 'ABBRUCH: kein </body>'
    return t[:p] + block + t[p:], f'Wortschatz-Tab an Position {pos} angelegt ({len(daten)} Wörter)'


def main():
    if len(sys.argv) != 3:
        print('Aufruf: python3 scripts/add_wortschatz_tab.py lektion.html woerter.json')
        return 2
    p, j = sys.argv[1], sys.argv[2]
    daten = json.load(open(j, encoding='utf-8'))
    s = open(p, encoding='utf-8').read()
    neu, grund = transform(s, daten)
    if neu != s:
        open(p, 'w', encoding='utf-8').write(neu)
    print(f'  {p.split("/")[-1]}: {grund}')
    return 1 if grund.startswith('ABBRUCH') else 0


if __name__ == '__main__':
    sys.exit(main())
