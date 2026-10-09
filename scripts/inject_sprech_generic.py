#!/usr/bin/env python3
"""Generischer Sprech-Trainer (FB-SPRECH-GENERIC) — Nomen sehen, passendes Verb laut sprechen.

Baustein für Lektionen OHNE die Verben-mit-Präposition-Daten (VAP). Didaktik und
Spracherkennung 1:1 nach der Referenz FB-SPRECH-TRAINER (daf-materialien/…/verben-praep-teil1.html):
8/5/3 Sekunden, Mikrofon optional, Auto-Auflösen bei Treffer, Selbstbewertung, Wiederholungsliste.

Aufruf:
  python3 scripts/inject_sprech_generic.py DATEI.html DATEN.json
DATEN.json:
  { "intro": "Kurzer Erklärtext (HTML erlaubt)",
    "karten": [ { "cue": "eine Einweisung", "ok": ["einford","eingeforder","forder|ein"],
                  "loesung": "eine Einweisung einfordern",
                  "beispiel": "Vor dem Aushub fordert der Polier eine Einweisung ein.",
                  "hint": "optional, darf die Lösung NICHT verraten" } ] }

Einbau: Nav-Button + Section direkt VOR der Schreibwerkstatt (bleibt letzter Tab), CSS vor das
erste </style>, Daten + Engine vor </body>. Idempotent: vorhandener Block wird ersetzt.
"""
import sys, json, re, base64, os, html as H

HIER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sprech_trainer')
def lies(n): return open(os.path.join(HIER, n), encoding='utf-8').read()

M = 'FB-SPRECH-GENERIC'
NAV = '    <div class="nav-btn" onclick="showSection({i})"><!-- FB-SPRECH-GENERIC -->\n      <span class="nav-emoji">🗣️</span>\n      <span class="nav-label">Sprechen</span>\n    </div>\n'

def entfernen(s):
    s = re.sub(r'    <div class="nav-btn" onclick="showSection\(\d+\)"><!-- FB-SPRECH-GENERIC -->\n.*?\n    </div>\n', '', s, flags=re.S)
    s = re.sub(r'  <!-- TAB: Sprech-Trainer \(FB-SPRECH-GENERIC\) -->\n.*?\n    </div>\n  </div>\n', '', s, count=1, flags=re.S)
    s = re.sub(r'<style>/\* FB-SPRECH-GENERIC-CSS \*/.*?</style>\n', '', s, flags=re.S)
    s = re.sub(r'<script>/\* FB-SPRECH-GENERIC-JS \*/.*?</script>\n', '', s, flags=re.S)
    return s

def nav_neu_nummerieren(s):
    nav_i = s.index('<div class="nav">'); nav_j = s.index('\n  </div>', nav_i)
    nav = s[nav_i:nav_j]; k = [0]
    def r(m): v = 'showSection(%d)' % k[0]; k[0] += 1; return v
    nav = re.sub(r'showSection\(\d+\)', r, nav)
    return s[:nav_i] + nav + s[nav_j:], k[0]

def main(datei, daten):
    d = json.load(open(daten, encoding='utf-8'))
    for c in d['karten']:
        assert c['cue'] and c['loesung'] and c['ok'], c
        for x in c['ok']:
            st = x.split('|')[0]
            assert len(st) >= (3 if '|' in x else 4), ('Wortanfang zu kurz (mind. 4, mit |Partikel mind. 3)', x)
        if c.get('hint'):
            assert not any(x.split('|')[0].lower() in c['hint'].lower() for x in c['ok']), ('Hinweis verrät Lösung', c)
        assert not any(x.split('|')[0].lower() in c['cue'].lower() for x in c['ok']), ('Karte verrät Lösung', c)
    s = open(datei, encoding='utf-8').read(); o = s
    s = entfernen(s)
    # Nav vor Schreibwerkstatt
    m = re.search(r'    <div class="nav-btn schreib-last" onclick="showSection\(\d+\)">', s)
    assert m, 'Nav-Anker schreib-last fehlt'
    s = s[:m.start()] + NAV.format(i=0) + s[m.start():]
    s, n = nav_neu_nummerieren(s)
    # Section vor Schreibwerkstatt
    sec = re.search(r'  <!-- TAB \d+: Schreibwerkstatt[^\n]*-->\n  <div class="section" id="sec-schreib">', s) or re.search(r'  <div class="section" id="sec-schreib">', s)
    assert sec, 'Section-Anker sec-schreib fehlt'
    banner = base64.b64encode(lies('banner.svg').strip().encode()).decode()
    block = lies('sprech.html').replace('{{BANNER}}', banner).replace('{{INTRO}}', d['intro'])
    s = s[:sec.start()] + block + s[sec.start():]
    s = s.replace('</style>', '</style>\n<style>/* FB-SPRECH-GENERIC-CSS */\n' + lies('sprech.css') + '</style>', 1)
    data = 'var SP_DATA = ' + json.dumps(d['karten'], ensure_ascii=False, indent=1) + ';\n'
    s = s.replace('</body>', '<script>/* FB-SPRECH-GENERIC-JS */\n' + data + lies('sprech.js') + '</script>\n</body>', 1)
    # Prüfungen
    assert s.count('id="sec-sprechen"') == 1 and s.count('FB-SPRECH-GENERIC-JS') == 1
    navs = re.findall(r'class="nav-btn[^"]*"', s[s.index('<div class="nav">'):s.index('\n  </div>', s.index('<div class="nav">'))])
    secs = len(re.findall(r'<div class="section[ "]', s))
    assert len(navs) == secs, ('Nav/Section-Anzahl ungleich', len(navs), secs)
    order = re.findall(r'<div class="section[^"]*" id="([^"]+)"', s)
    assert order[-1] == 'sec-schreib' and order[-2] == 'sec-sprechen', order
    open(datei, 'w', encoding='utf-8').write(s)
    print(('aktualisiert' if M in o else 'eingebaut'), datei, '·', len(d['karten']), 'Karten ·', secs, 'Tabs')

if __name__ == '__main__':
    if len(sys.argv) != 3: print(__doc__); sys.exit(2)
    main(sys.argv[1], sys.argv[2])
