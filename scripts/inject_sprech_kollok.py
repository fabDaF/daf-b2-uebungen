#!/usr/bin/env python3
"""Sprech-Trainer (FB-SPRECH-KOLLOK) für die Kollokationen-Serie (daf-materialien/Grundlagen/Kollokationen).

Adapter zu inject_sprech_generic.py für Lektionen OHNE Schreibwerkstatt/sec-inner-Layout:
Engine, CSS und Didaktik kommen 1:1 aus scripts/sprech_trainer/ (eine Quelle der Wahrheit);
der Tab wird als LETZTER Tab angehängt (Nav-Button + Section vor dem author-footer).
Markup folgt dem Hausstil dieser Serie (.section-title / .intro statt sec-inner / h2 / Banner).

Aufruf:
  python3 scripts/inject_sprech_kollok.py DATEI.html DATEN.json
DATEN.json wie bei inject_sprech_generic.py ({ intro, karten:[{cue, ok, loesung, beispiel, hint?}] }).
Idempotent: vorhandener Block wird ersetzt.
"""
import sys, json, re, os

HIER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sprech_trainer')
def lies(n): return open(os.path.join(HIER, n), encoding='utf-8').read()

M = 'FB-SPRECH-KOLLOK'
SECTION = '''        <!-- ==================== TAB {i}: Sprech-Trainer ({m}) ==================== -->
        <div class="section" id="sec-sprechen">

            <div class="section-title">🗣️ Sprech-Trainer &ndash; Kollokationen unter Zeitdruck</div>

            <div class="intro" style="margin-bottom: 20px;">
                <p>{intro}</p>
            </div>

            <div class="sp-steuerung">
                <label>Aufgabe <select id="sp-modus">
                    <option value="kurz">Nomen + Verb</option>
                    <option value="satz">Ganzer Satz</option>
                </select></label>
                <label>Zeit <select id="sp-zeit">
                    <option value="8">8 Sekunden</option>
                    <option value="5" selected>5 Sekunden</option>
                    <option value="3">3 Sekunden</option>
                </select></label>
                <button class="sp-btn" id="sp-mic" onclick="spMicToggle()" title="Klicken zum Ein- oder Ausschalten" hidden>🎤 Mikrofon ist aus</button>
            </div>
            <div class="sp-stand" id="sp-stand"></div>
            <div class="sp-karte" id="sp-karte"></div>
            <div class="sp-tipp">Tipp: Leertaste zeigt die Lösung bzw. geht weiter. Mit Mikrofon hört die Seite mit und prüft, ob das richtige Verb gefallen ist (Chrome, Safari).</div>
        </div>

'''

def entfernen(s):
    s = re.sub(r'[ \t]*<div class="nav-btn" onclick="showSection\(\d+\)"><!-- %s -->🗣️ Sprechen</div>\n' % M, '', s)
    s = re.sub(r'[ \t]*<!-- =+ TAB \d+: Sprech-Trainer \(%s\) =+ -->\n.*?\n        </div>\n\n' % M, '', s, count=1, flags=re.S)
    s = re.sub(r'<style>/\* %s-CSS \*/.*?</style>\n' % M, '', s, flags=re.S)
    s = re.sub(r'<script>/\* %s-JS \*/.*?</script>\n' % M, '', s, flags=re.S)
    return s

def pruefe_daten(d):
    for c in d['karten']:
        assert c['cue'] and c['loesung'] and c['ok'], c
        for x in c['ok']:
            st = x.split('|')[0]
            assert len(st) >= (3 if '|' in x else 4), ('Wortanfang zu kurz (mind. 4, mit |Partikel mind. 3)', x)
        if c.get('hint'):
            assert not any(x.split('|')[0].lower() in c['hint'].lower() for x in c['ok']), ('Hinweis verrät Lösung', c)
        assert not any(x.split('|')[0].lower() in c['cue'].lower() for x in c['ok']), ('Karte verrät Lösung', c)
    cues = [c['cue'] for c in d['karten']]
    assert len(cues) == len(set(cues)), ('Nomen doppelt', cues)

def main(datei, daten):
    d = json.load(open(daten, encoding='utf-8'))
    pruefe_daten(d)
    s = open(datei, encoding='utf-8').read(); o = s
    s = entfernen(s)
    # Nav: Button ans Ende der .nav
    nav_i = s.index('<div class="nav">')
    m = re.compile(r'\n([ \t]*)</div>').search(s, nav_i)
    assert m, 'Nav-Ende fehlt'
    nav_html = s[nav_i:m.start()]
    n = len(re.findall(r'class="nav-btn', nav_html))
    assert n >= 2, ('zu wenige Nav-Buttons', n)
    # Seit 2026-10-19 hat die Serie eine Schreibwerkstatt als LETZTEN Tab (FB-SCHREIB-KOLLOK):
    # dann kommt „Sprechen" davor (Nav-Button vor dem Schreibwerkstatt-Button, Section vor sec-schreiben).
    schreib = re.search(r'\n([ \t]*)<div class="nav-btn" onclick="showSection\(\d+\)">📨 Schreibwerkstatt</div>', s[nav_i:m.start()])
    if schreib:
        n = len(re.findall(r'class="nav-btn', s[nav_i:nav_i + schreib.start()]))
        btn = '\n' + schreib.group(1) + '<div class="nav-btn" onclick="showSection(%d)"><!-- %s -->🗣️ Sprechen</div>' % (n, M)
        s = s[:nav_i + schreib.start()] + btn + s[nav_i + schreib.start():]
        # alle Nav-Indizes nach DOM-Reihenfolge neu nummerieren (showSection = Index)
        m3 = re.compile(r'\n([ \t]*)</div>').search(s, nav_i); k = [0]
        def rn(mm): v = 'showSection(%d)' % k[0]; k[0] += 1; return v
        s = s[:nav_i] + re.sub(r'showSection\(\d+\)', rn, s[nav_i:m3.start()]) + s[m3.start():]
        f = s.index('<!-- ==================== TAB 5: Schreibwerkstatt (FB-SCHREIB-KOLLOK)')
        f = s.rfind('\n', 0, f) + 1
        s = s[:f] + SECTION.format(i=n, m=M, intro=d['intro']) + s[f:]
    else:
        btn = '\n' + m.group(1) + '    <div class="nav-btn" onclick="showSection(%d)"><!-- %s -->🗣️ Sprechen</div>' % (n, M)
        s = s[:m.start()] + btn + s[m.start():]
        # Section vor dem Footer
        f = s.index('<div class="author-footer">')
        f = s.rfind('\n', 0, f) + 1
        s = s[:f] + SECTION.format(i=n, m=M, intro=d['intro']) + s[f:]
    # CSS + JS
    s = s.replace('</style>', '</style>\n<style>/* %s-CSS */\n' % M + lies('sprech.css') + '</style>', 1)
    data = 'var SP_DATA = ' + json.dumps(d['karten'], ensure_ascii=False, indent=1) + ';\n'
    s = s.replace('</body>', '<script>/* %s-JS */\n' % M + data + lies('sprech.js') + '</script>\n</body>', 1)
    # Prüfungen
    assert s.count('id="sec-sprechen"') == 1 and s.count('%s-JS' % M) == 1 and s.count('%s-CSS' % M) == 1
    nav_i = s.index('<div class="nav">'); m2 = re.compile(r'\n[ \t]*</div>').search(s, nav_i)
    navs = re.findall(r'class="nav-btn', s[nav_i:m2.start()])
    secs = re.findall(r'<div class="section[ "]', s)
    assert len(navs) == len(secs), ('Nav/Section-Anzahl ungleich', len(navs), len(secs))
    order = re.findall(r'<div class="section[^"]*" id="([^"]+)"', s)
    assert order[-1] == 'sec-sprechen' or (order[-1] == 'sec-schreiben' and order[-2] == 'sec-sprechen'), order
    idx = [int(x) for x in re.findall(r'onclick="showSection\((\d+)\)"', s[nav_i:m2.start()])]
    assert idx == list(range(len(idx))), ('Nav-Indizes nicht lückenlos', idx)
    open(datei, 'w', encoding='utf-8').write(s)
    print(('aktualisiert' if M in o else 'eingebaut'), os.path.basename(datei), '·', len(d['karten']), 'Karten ·', len(secs), 'Tabs')

if __name__ == '__main__':
    if len(sys.argv) != 3: print(__doc__); sys.exit(2)
    main(sys.argv[1], sys.argv[2])
