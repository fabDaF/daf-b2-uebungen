#!/usr/bin/env python3
"""inject_sprech_wortschatz.py — Sprech-Trainer für den Wortschatz (FB-SPRECH-WORTSCHATZ).

Didaktik (Frank, 2026-10-19): eigener Tab „🗣️ Sprechen". Das ENGLISCHE Wort erscheint allein,
der Lerner sagt laut das DEUTSCHE Wort MIT ARTIKEL (Nomen) bzw. das Verb/den Ausdruck.
Mikrofon prüft Wortanfang + Artikel als eigenes Wort (Engine-Format "stamm|partikel").
Engine, CSS, Banner: 1:1 aus scripts/sprech_trainer/ (eine Quelle der Wahrheit) — nur die
Verb-Formulierungen werden über SP_TEXTE (Engine-Hook seit 2026-10-19) ersetzt.

Daten: liest `var WORTSCHATZ = [...]` (bzw. WORTSCHATZ_DATA / vocabData …) aus der Lektion,
schema-adaptiv wie inject_wortschatz.py (en|prompt, artikel|art, de|wort|word, plural|pl, type).
Einbau: Nav-Button als LETZTER Nav-Eintrag (Schreibwerkstatt bleibt per CSS order:99 / schreib-last
optisch letzter), Section vor dem author-footer; showSection-Index = DOM-Reihenfolge.
Idempotent: vorhandener FB-SPRECH-WORTSCHATZ-Block wird ersetzt. Bricht ab, wenn die Datei schon
einen anderen Sprech-Trainer (FB-SPRECH-GENERIC/-KOLLOK/-TRAINER) hat — gleiche Element-IDs.

Aufruf:  python3 scripts/inject_sprech_wortschatz.py DATEI.html [...]
"""
import base64, json, os, re, sys

HIER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sprech_trainer')
def lies(n): return open(os.path.join(HIER, n), encoding='utf-8').read()
M = 'FB-SPRECH-WORTSCHATZ'

TEXTE = {
    'start': 'Das englische Wort erscheint – dann laut das deutsche Wort mit Artikel sagen, bevor der Balken abgelaufen ist.',
    'kurz': 'Laut das deutsche Wort mit Artikel sagen.',
    'satz': 'Laut einen ganzen Satz mit dem deutschen Wort sprechen.',
    'frage': 'Kam das Wort sofort?',
    'erkannt': '✓ richtiges Wort erkannt',
    'dabei': '✓ Richtig – Wort und Artikel waren dabei!',
    'nichtDabei': '– das richtige Wort (mit Artikel) war nicht dabei.',
}
INTRO = ('Das englische Wort erscheint allein – du sagst <strong>laut</strong> das deutsche Wort '
         '<strong>mit Artikel</strong>, bevor der Balken abgelaufen ist. Erst wer Wort und Artikel ohne '
         'Nachdenken abrufen kann, hat sie wirklich gespeichert.')

NAV = '        <div class="nav-btn" onclick="showSection({i})"><!-- FB-SPRECH-WORTSCHATZ -->\n            <span class="nav-emoji">🗣️</span>\n            <span class="nav-label">Sprechen</span>\n        </div>\n'

SECTION = '''        <!-- TAB: Sprech-Trainer Wortschatz (FB-SPRECH-WORTSCHATZ) -->
        <div class="section" id="sec-sprechen">
  <img class="tab-banner" src="data:image/svg+xml;base64,{banner}" alt="Sprech-Trainer: Mikrofon und ablaufender Zeitbalken">
            <h2>🗣️ Sprechen &ndash; Wortschatz unter Zeitdruck</h2>
            <p class="sp-intro">{intro}</p>
            <div class="sp-steuerung">
                <label>Aufgabe <select id="sp-modus">
                    <option value="kurz">Wort mit Artikel</option>
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
            <div class="sp-tipp">Tipp: Leertaste zeigt die Lösung bzw. geht weiter. Mit Mikrofon hört die Seite mit und prüft, ob das richtige Wort mit Artikel gefallen ist (Chrome, Safari).</div>
        </div>
'''
EXTRA_CSS = '.sp-intro { color: var(--sp-muted); line-height: 1.6; margin: 0 0 14px; }\n.sp-cue .sp-luecke:empty { display: none; }\n'

DATA_VARS = r'(?:var|const|let)\s+(WORTSCHATZ(?:_DATA)?|wortschatzData|WS_DATA|VOCAB_DATA|vocabData|vocabulary)\s*=\s*\['


def entfernen(s):
    s = re.sub(r'        <div class="nav-btn" onclick="showSection\(\d+\)"><!-- FB-SPRECH-WORTSCHATZ -->\n.*?\n        </div>\n', '', s, flags=re.S)
    s = re.sub(r'        <!-- TAB: Sprech-Trainer Wortschatz \(FB-SPRECH-WORTSCHATZ\) -->\n.*?<div class="sp-tipp">[^\n]*\n        </div>\n', '', s, count=1, flags=re.S)
    s = re.sub(r'<style>/\* FB-SPRECH-WORTSCHATZ-CSS \*/.*?</style>\n', '', s, flags=re.S)
    s = re.sub(r'<script>/\* FB-SPRECH-WORTSCHATZ-JS \*/.*?</script>\n', '', s, flags=re.S)
    return s


def js_obj_rows(blk):
    """Zeilenweise Objekt-Literale { k: 'v', ... } → dicts (nur einfache String-Werte)."""
    rows = []
    for obj in re.finditer(r'\{([^{}]*)\}', blk):
        d = {}
        for k, v in re.findall(r"(\w+)\s*:\s*'((?:[^'\\]|\\.)*)'", obj.group(1)):
            d[k] = re.sub(r'\\u([0-9a-fA-F]{4})', lambda mm: chr(int(mm.group(1), 16)), v).replace("\\'", "'")
        for k, v in re.findall(r'(\w+)\s*:\s*"((?:[^"\\]|\\.)*)"', obj.group(1)):
            d[k] = v
        if d: rows.append(d)
    return rows


def norm(r):
    en = r.get('en') or r.get('prompt') or r.get('english') or ''
    art = (r.get('artikel') or r.get('art') or '').strip()
    de = (r.get('de') or r.get('wort') or r.get('word') or '').strip()
    pl = (r.get('plural') or r.get('pl') or '').strip()
    typ = (r.get('type') or ('n' if art else 'p')).strip()
    return en.strip(), art, de, pl, typ


def stamm(wort):
    w = wort.lower().replace('sich ', '').strip()
    w = re.split(r'[\s,/(]', w)[0]
    w = re.sub(r'[^a-zäöüß]', '', w)
    return w[:5] if len(w) >= 5 else w


def karten(rows):
    out = []
    for r in rows:
        en, art, de, pl, typ = norm(r)
        if not en or not de: continue
        st = stamm(de)
        if len(st) < 3: continue
        if art and typ == 'n':
            ok = [st + '|' + art.lower()]
            loes = art + ' ' + de + (', Pl. ' + pl if pl and pl != de else (', Pl. ' + pl if pl else ''))
        else:
            ok = [st]
            loes = de
        out.append({'cue': en, 'luecke': '', 'ok': ok, 'loesung': loes})
    return out


def main(datei):
    s = open(datei, encoding='utf-8').read(); o = s
    s = entfernen(s)
    for other in ('FB-SPRECH-GENERIC-JS', 'FB-SPRECH-KOLLOK-JS', 'FB-SPRECH-TRAINER-JS', 'id="sec-sprechen"'):
        assert other not in s, datei + ': hat schon einen anderen Sprech-Trainer (' + other + ', gleiche Element-IDs)'
    m = re.search(DATA_VARS, s); assert m, datei + ': keine Wortschatz-Datenvariable gefunden'
    i = m.end(); j = s.index('\n];', i) if '\n];' in s[i:] else s.index('];', i)
    rows = js_obj_rows(s[i:j]); k = karten(rows)
    assert len(k) >= 6, (datei, 'zu wenige Karten', len(k))
    # Nav: letzter Eintrag im .nav-Block, dann neu nummerieren nach DOM-Reihenfolge
    nav_i = s.index('<div class="nav">'); nav_j = s.index('\n    </div>', nav_i)
    s = s[:nav_j] + '\n' + NAV.format(i=0).rstrip('\n') + s[nav_j:]
    nav_i = s.index('<div class="nav">'); nav_j = s.index('\n    </div>', nav_i)
    nav = s[nav_i:nav_j]; c = [0]
    def rn(mm): v = 'showSection(%d)' % c[0]; c[0] += 1; return v
    nav = re.sub(r'showSection\(\d+\)', rn, nav); s = s[:nav_i] + nav + s[nav_j:]
    # Section vor dem author-footer (innerhalb .content → letztes .section-Element)
    foot = s.index('<div class="author-footer">')
    content_end = s.rfind('\n    </div>\n', 0, foot)  # schließendes </div> von .content
    assert content_end > 0, datei + ': .content-Ende nicht gefunden'
    banner = base64.b64encode(lies('banner.svg').strip().encode()).decode()
    s = s[:content_end] + '\n' + SECTION.format(banner=banner, intro=INTRO).rstrip('\n') + s[content_end:]
    # CSS + Daten + Engine
    s = s.replace('</style>', '</style>\n<style>/* FB-SPRECH-WORTSCHATZ-CSS */\n' + lies('sprech.css') + EXTRA_CSS + '</style>', 1)
    data = 'var SP_TEXTE = ' + json.dumps(TEXTE, ensure_ascii=False) + ';\nvar SP_DATA = ' + json.dumps(k, ensure_ascii=False, indent=1) + ';\n'
    s = s.replace('</body>', '<script>/* FB-SPRECH-WORTSCHATZ-JS */\n' + data + lies('sprech.js') + '</script>\n</body>', 1)
    # Prüfungen
    assert s.count('id="sec-sprechen"') == 1 and s.count('FB-SPRECH-WORTSCHATZ-JS') == 1
    nav_i = s.index('<div class="nav">'); nav_j = s.index('\n    </div>', nav_i)
    navs = re.findall(r'class="nav-btn[^"]*"', s[nav_i:nav_j]); secs = re.findall(r'<div class="section[ "]', s)
    assert len(navs) == len(secs), (datei, 'Nav/Section-Anzahl ungleich', len(navs), len(secs))
    open(datei, 'w', encoding='utf-8').write(s)
    print(('aktualisiert' if M in o else 'eingebaut'), datei, '·', len(k), 'Karten ·', len(secs), 'Tabs')


if __name__ == '__main__':
    if len(sys.argv) < 2: print(__doc__); sys.exit(2)
    for f in sys.argv[1:]: main(f)
