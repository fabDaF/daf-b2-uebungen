#!/usr/bin/env python3
"""inject_sprech_wortschatz.py — Sprech-Trainer für den Wortschatz (FB-SPRECH-WORTSCHATZ).

Didaktik (Frank, 2026-10-19): eigener Tab „🗣️ Sprechen". Das ENGLISCHE Wort erscheint allein,
der Lerner sagt laut das DEUTSCHE Wort MIT ARTIKEL (Nomen) bzw. das Verb/den Ausdruck.
Mikrofon prüft Wortanfang + Artikel als eigenes Wort (Engine-Format "stamm|partikel").
Engine, CSS, Banner: 1:1 aus scripts/sprech_trainer/ (eine Quelle der Wahrheit) — nur die
Verb-Formulierungen werden über SP_TEXTE (Engine-Hook seit 2026-10-19) ersetzt.

Daten: liest das Wortschatz-Array der Lektion (WORTSCHATZ, WORTSCHATZ_STATIC, WS_DATA, vocabData,
vocabItems, …), schema-adaptiv wie inject_wortschatz.py (en|prompt, artikel|art, de|wort|word,
plural|pl, type). Keys mit oder ohne Anführungszeichen.
Einbau (generationsrobust, 2026-10-19 v2): Nav-Button als LETZTER Eintrag des Nav-Containers
(Tag-Balancer, keine Einrückungs-Anker; Schreibwerkstatt bleibt per CSS order:99 / schreib-last
optisch letzter), Section direkt NACH der letzten .section (Attributreihenfolge egal);
showSection-Index = DOM-Reihenfolge, alle Nav-Indizes werden neu nummeriert.
Idempotent: vorhandener FB-SPRECH-WORTSCHATZ-Block wird ersetzt. Bricht ab, wenn die Datei schon
einen anderen Sprech-Trainer hat (gleiche Element-IDs). --dry-run: nur prüfen, nichts schreiben.

Aufruf:  python3 scripts/inject_sprech_wortschatz.py [--dry-run] DATEI.html [...]
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

NAV = '<div class="nav-btn" onclick="showSection(0)"><!-- FB-SPRECH-WORTSCHATZ --><span class="nav-emoji">🗣️</span><span class="nav-label">Sprechen</span></div>'

SECTION = '''
<!-- TAB: Sprech-Trainer Wortschatz (FB-SPRECH-WORTSCHATZ) -->
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
<!-- /FB-SPRECH-WORTSCHATZ -->'''
EXTRA_CSS = ('.sp-intro { color: var(--sp-muted); line-height: 1.6; margin: 0 0 14px; }\n'
             '.sp-cue .sp-luecke:empty { display: none; }\n'
             '#sec-sprechen { padding: 0 0 10px; }\n')

CLS = lambda tok: r'class="(?:[^"]*\s)?%s(?:\s[^"]*)?"' % tok
SEC_TAG = re.compile(r'<(div|section)\b[^>]*' + CLS('section') + r'[^>]*>')
NAV_TAG = re.compile(r'<(div|nav)\b[^>]*' + CLS('nav') + r'[^>]*>')
NAVBTN = re.compile(r'<(div|button|a)\b[^>]*' + CLS('nav-btn'))
TAG = re.compile(r'<(/?)(div|section|nav|main|article)\b[^>]*>')


def element_end(s, start):
    """Index hinter dem schließenden Tag des Elements, dessen Start-Tag bei `start` beginnt."""
    depth = 0
    for m in TAG.finditer(s, start):
        if m.group(0).endswith('/>'): continue
        depth += -1 if m.group(1) else 1
        if depth == 0: return m.end()
    raise ValueError('Element nicht geschlossen')


def entfernen(s):
    s = re.sub(r'\n?[ \t]*<(div|button) class="nav-btn" onclick="\w+\(\d+(?:,\s*this)?\)"><!-- FB-SPRECH-WORTSCHATZ -->.*?</\1>', '', s, count=1, flags=re.S)
    s = re.sub(r'\n?<!-- TAB: Sprech-Trainer Wortschatz \(FB-SPRECH-WORTSCHATZ\) -->.*?<!-- /FB-SPRECH-WORTSCHATZ -->', '', s, count=1, flags=re.S)
    # v1-Block (Pilot 3061X, ohne End-Marker): bis zum schließenden </div> nach .sp-tipp
    s = re.sub(r'\n?[ \t]*<!-- TAB: Sprech-Trainer Wortschatz \(FB-SPRECH-WORTSCHATZ\) -->.*?<div class="sp-tipp">[^\n]*\n[ \t]*</div>\n', '', s, count=1, flags=re.S)
    s = re.sub(r'<style>/\* FB-SPRECH-WORTSCHATZ-CSS \*/.*?</style>\n', '', s, flags=re.S)
    s = re.sub(r'<script>/\* FB-SPRECH-WORTSCHATZ-JS \*/.*?</script>\n', '', s, flags=re.S)
    return s


def unescape_js(v):
    v = re.sub(r'\\u([0-9a-fA-F]{4})', lambda mm: chr(int(mm.group(1), 16)), v)
    try: v = v.encode('utf-16', 'surrogatepass').decode('utf-16')  # Surrogat-Paare (Emoji) zusammenfuegen
    except UnicodeError: v = ''.join(ch for ch in v if not 0xD800 <= ord(ch) <= 0xDFFF)
    return v.replace("\\'", "'").replace('\\"', '"').replace('\\\\', '\\')


def js_obj_rows(blk):
    """Objekt-Literale { k: 'v', "k": "v", ... } → dicts (nur String-Werte)."""
    rows = []
    for obj in re.finditer(r'\{([^{}]*)\}', blk):
        d = {}
        for k, v in re.findall(r'''["']?(\w+)["']?\s*:\s*'((?:[^'\\]|\\.)*)\'''', obj.group(1)): d[k] = unescape_js(v)
        for k, v in re.findall(r'''["']?(\w+)["']?\s*:\s*"((?:[^"\\]|\\.)*)"''', obj.group(1)): d[k] = unescape_js(v)
        if d: rows.append(d)
    return rows


def find_data(s):
    """Erstes Array, dessen Variablenname nach Wortschatz/Vokabeln klingt; Inhalt per Klammer-Balance."""
    best = None
    for m in re.finditer(r'(?:(?:var|const|let)\s+|^[ \t]*)(\w+)\s*=\s*\[', s, re.M):
        name = m.group(1)
        if not re.search(r'wortschatz|vocab|vokab|ws_data|words', name, re.I): continue
        i = m.end() - 1; depth = 0; j = None
        for k in range(i, min(len(s), i + 400000)):
            c = s[k]
            if c == '[': depth += 1
            elif c == ']':
                depth -= 1
                if depth == 0: j = k; break
        if j is None: continue
        rows = js_obj_rows(s[i:j + 1])
        if rows and (best is None or len(rows) > len(best[1])): best = (name, rows)
    return best


def norm(r):
    en = r.get('en') or r.get('eng') or r.get('prompt') or r.get('english') or r.get('frage') or r.get('translation') or ''
    en = re.sub(r'^\((.*)\)$', r'\1', en.strip())
    art = (r.get('artikel') or r.get('art') or r.get('article') or '').strip()
    de = (r.get('de') or r.get('wort') or r.get('word') or r.get('german') or r.get('term') or '').strip()
    pl = (r.get('plural') or r.get('pl') or '').strip()
    typ = (r.get('type') or ('n' if art else 'p')).strip()
    return en.strip(), art, de, pl, typ


FUNKTIONSWOERTER = {'sich', 'auf', 'an', 'in', 'im', 'am', 'mit', 'von', 'vom', 'zu', 'zum', 'zur', 'für', 'über', 'unter', 'bei', 'beim', 'nach', 'aus', 'um', 'vor', 'der', 'die', 'das', 'den', 'dem', 'des', 'ein', 'eine', 'einen', 'einem', 'einer', 'etwas', 'jemanden', 'jemandem', 'jmdn', 'jmdm', 'etw', 'und', 'oder', 'nicht', 'kein', 'keine', 'sein', 'haben', 'werden', 'lassen', 'machen', 'sehr'}

def stamm(wort):
    """Prüf-Wortanfang: bei Mehrwort-Ausdrücken das längste Inhaltswort (nicht „auf"/„sich"/Artikel)."""
    w = wort.lower().split('(')[0].split(',')[0].split('/')[0]
    woerter = [re.sub(r'[^a-zäöüß]', '', x) for x in w.split()]
    inhalt = [x for x in woerter if x and x not in FUNKTIONSWOERTER and len(x) >= 4]
    w = max(inhalt, key=len) if inhalt else (woerter[0] if woerter else '')
    return w[:5] if len(w) >= 5 else w


def karten(rows):
    out, seen = [], set()
    for r in rows:
        en, art, de, pl, typ = norm(r)
        if not en or not de: continue
        en = re.sub(r'\s*\[[A-Z]\]\s*$', '', en)  # Marker wie „[T]" am Ende
        st = stamm(de)
        if len(st) < 3 or (st, art) in seen: continue
        seen.add((st, art))
        if art and typ in ('n', 'noun', 'nomen'):
            ok = [st + '|' + art.lower()]
            if pl.startswith('-'): loes = art + ' ' + de + ', ' + pl
            elif pl and pl.lower() not in ('pl.', de.lower()) and not re.fullmatch(r'[-–—\s]*|kein plural|nur sg\.?|sg\.?', pl.lower()): loes = art + ' ' + de + ', Pl. ' + pl
            else: loes = art + ' ' + de
        else:
            ok = [st]; loes = de
        out.append({'cue': en, 'luecke': '', 'ok': ok, 'loesung': loes})
    return out


def main(datei, dry=False):
    s = open(datei, encoding='utf-8').read(); o = s
    s = entfernen(s)
    for other in ('FB-SPRECH-GENERIC-JS', 'FB-SPRECH-KOLLOK-JS', 'FB-SPRECH-TRAINER-JS', 'id="sec-sprechen"'):
        assert other not in s, 'hat schon einen anderen Sprech-Trainer (' + other + ', gleiche Element-IDs)'
    fm = None
    for bt in re.finditer(r'<(?:div|button|a)\b[^>]*' + CLS('nav-btn') + r'[^>]*>', s):
        fm = re.search(r'onclick="(\w+)\((\d+)(,\s*this)?\)"', bt.group(0))
        if fm: break
    assert fm, 'Nav-Buttons ohne onclick="fn(index)" — Tab-Funktion unbekannt'
    fn, this_arg = fm.group(1), (fm.group(3) or '')
    assert re.search(r'function\s+' + fn + r'\b|' + fn + r'\s*=\s*function', s), 'Tab-Funktion %s nicht gefunden' % fn
    data = find_data(s); assert data, 'keine Wortschatz-Datenvariable gefunden'
    k = karten(data[1]); assert len(k) >= 4, 'zu wenige Karten (%d aus %s)' % (len(k), data[0])
    # Nav-Container (Tag-Balancer) → Button als letztes Kind
    nm = NAV_TAG.search(s); assert nm, 'kein Nav-Container'
    nav_end = element_end(s, nm.start())
    close = s.rfind('</', nm.start(), nav_end)
    nav_html = s[nm.start():close]
    n_before = len(NAVBTN.findall(nav_html)); assert n_before >= 2, 'zu wenige Nav-Buttons (%d)' % n_before
    indent = re.search(r'\n([ \t]*)<[^>]*nav-btn', nav_html)
    ind = indent.group(1) if indent else '  '
    tag = 'button' if re.search(r'<button\b[^>]*' + CLS('nav-btn'), nav_html) else 'div'
    nav_btn = NAV.replace('showSection(0)', fn + '(0' + this_arg + ')').replace('<div class="nav-btn"', '<' + tag + ' class="nav-btn"').replace('</div>', '</' + tag + '>')
    # Regel (CLAUDE.md): Schreibwerkstatt ist immer der LETZTE Tab. Ist der DOM-letzte Nav-Button der
    # Schreib-Tab, kommt „Sprechen" DAVOR (Nav + Section am gleichen Index); sonst ans Ende.
    btns = [m for m in re.finditer(r'<(div|button|a)\b[^>]*' + CLS('nav-btn') + r'[^>]*>', nav_html)]
    last = btns[-1]; last_html = nav_html[last.start():nav_html.index('</' + last.group(1) + '>', last.start())]
    last_label = re.sub(r'<[^>]+>', '', last_html)
    vor_schreib = bool(re.search(r'schreib', last_label, re.I) or 'schreib-last' in last.group(0))
    if vor_schreib:
        ins = nm.start() + last.start()
        line_start = s.rfind('\n', 0, ins) + 1
        s = s[:line_start] + ind + nav_btn + '\n' + s[line_start:]
    else:
        s = s[:close].rstrip(' \t') + ('' if s[:close].endswith('\n') else '\n') + ind + nav_btn + '\n' + s[close:]
    # Nav-Indizes nach DOM-Reihenfolge neu nummerieren
    nm = NAV_TAG.search(s); nav_end = element_end(s, nm.start()); c = [0]
    def rn(mm): v = fn + '(%d' % c[0] + (mm.group(2) or '') + ')'; c[0] += 1; return v
    s = s[:nm.start()] + re.sub(r'\b' + fn + r'\((\d+)(,\s*this)?\)', rn, s[nm.start():nav_end]) + s[nav_end:]
    # Section: vor der Schreib-Section (gleicher DOM-Index wie der Nav-Button) oder nach der letzten .section
    secs = list(SEC_TAG.finditer(s)); assert secs, 'keine .section gefunden'
    banner = base64.b64encode(lies('banner.svg').strip().encode()).decode()
    if vor_schreib:
        assert len(secs) == n_before, 'Nav/Section-Anzahl vor Einbau ungleich (%d/%d)' % (n_before, len(secs))
        pos = secs[-1].start()   # exakt an der Tag-Position (das Tag kann hinter einem </div> in derselben Zeile stehen)
        s = s[:pos] + SECTION.format(banner=banner, intro=INTRO).lstrip('\n') + '\n' + s[pos:]
    else:
        last_end = element_end(s, secs[-1].start())
        s = s[:last_end] + SECTION.format(banner=banner, intro=INTRO) + s[last_end:]
    # CSS + Daten + Engine
    assert '</style>' in s and '</body>' in s, 'style/body fehlt'
    s = s.replace('</style>', '</style>\n<style>/* FB-SPRECH-WORTSCHATZ-CSS */\n' + lies('sprech.css') + EXTRA_CSS + '</style>', 1)
    js = 'var SP_TEXTE = ' + json.dumps(TEXTE, ensure_ascii=False) + ';\nvar SP_DATA = ' + json.dumps(k, ensure_ascii=False, indent=1) + ';\n'
    i = s.rfind('</body>')
    s = s[:i] + '<script>/* FB-SPRECH-WORTSCHATZ-JS */\n' + js + lies('sprech.js') + '</script>\n' + s[i:]
    # Prüfungen
    assert s.count('id="sec-sprechen"') == 1 and s.count('FB-SPRECH-WORTSCHATZ-JS') == 1
    nm = NAV_TAG.search(s); nav_end = element_end(s, nm.start())
    navs = len(NAVBTN.findall(s[nm.start():nav_end])); nsec = len(SEC_TAG.findall(s))
    assert navs == nsec, 'Nav/Section-Anzahl ungleich (%d/%d)' % (navs, nsec)
    if not dry: open(datei, 'w', encoding='utf-8').write(s)
    print(('aktualisiert' if M in o else 'eingebaut') + (' [dry]' if dry else ''), datei, '·', len(k), 'Karten ·', nsec, 'Tabs ·', data[0])


if __name__ == '__main__':
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    DRY = '--dry-run' in sys.argv
    if args == ['-']: args = [l.rstrip('\n') for l in sys.stdin if l.strip()]
    if not args: print(__doc__); sys.exit(2)
    ok = fail = 0
    for f in args:
        try:
            main(f, dry=DRY); ok += 1
        except (AssertionError, ValueError) as e:
            fail += 1; print('FEHLER', f, '→', str(e)[:160])
    print('— %d ok, %d Fehler%s' % (ok, fail, ' (Trockenlauf, nichts geschrieben)' if DRY else ''))
