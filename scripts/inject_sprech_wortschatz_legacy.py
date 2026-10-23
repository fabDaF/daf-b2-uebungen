"""Sonderroutine: Sprech-Trainer Wortschatz in Alt-Nav-Dateien (ohne nav-btn/onclick fn(i)).
Nutzt die Bausteine von inject_sprech_wortschatz.py. Zwei Muster:
 A) .nav > <button onclick="showTab(i)"> + .tab-content#tabN   → Button+Tab ans Ende
 B) .nav-btn[data-section=i] + .section (indexbasiert)           → vor den schreib-last-Button/-Section
"""
import re, sys, json, base64
sys.path.insert(0, 'scripts'); import inject_sprech_wortschatz as I

def common(s, k):
    banner = base64.b64encode(I.lies('banner.svg').strip().encode()).decode()
    sec = I.SECTION.format(banner=banner, intro=I.INTRO)
    s = s.replace('</style>', '</style>\n<style>/* FB-SPRECH-WORTSCHATZ-CSS */\n' + I.lies('sprech.css') + I.EXTRA_CSS + '</style>', 1)
    js = 'var SP_TEXTE = ' + json.dumps(I.TEXTE, ensure_ascii=False) + ';\nvar SP_DATA = ' + json.dumps(k, ensure_ascii=False, indent=1) + ';\n'
    i = s.rfind('</body>')
    s = s[:i] + '<script>/* FB-SPRECH-WORTSCHATZ-JS */\n' + js + I.lies('sprech.js') + '</script>\n' + s[i:]
    return s, sec

def main(p, dry):
    s = open(p, encoding='utf-8').read(); s = I.entfernen(s)
    data = I.find_data(s); assert data, 'keine Daten'
    k = I.karten(data[1]); assert len(k) >= 4, 'zu wenige Karten'
    if 'data-section=' in s:   # Muster B
        btns = list(re.finditer(r'<button[^>]*class="nav-btn[^"]*"[^>]*data-section="(\d+)"[^>]*>', s))
        last = btns[-1]; assert 'schreib-last' in last.group(0), 'letzter Button nicht schreib-last'
        n = int(last.group(1))
        btn = '<button class="nav-btn" data-section="%d"><!-- FB-SPRECH-WORTSCHATZ --><span class="nav-emoji">🗣️</span><span class="nav-label">Sprechen</span></button>\n' % n
        s = s[:last.start()] + btn + s[last.start():]
        s = s[:last.start()+len(btn)] + s[last.start()+len(btn):].replace('data-section="%d"' % n, 'data-section="%d"' % (n+1), 1)
        secs = list(I.SEC_TAG.finditer(s)); assert len(secs) == n+1, 'Sections %d != %d' % (len(secs), n+1)
        s, sec = common(s, k)
        secs = list(I.SEC_TAG.finditer(s)); pos = secs[n].start()
        s = s[:pos] + sec.lstrip('\n') + '\n' + s[pos:]
        tabs = len(I.SEC_TAG.findall(s))
    else:                      # Muster A
        btns = list(re.finditer(r'<button[^>]*onclick="showTab\((\d+)\)"[^>]*>', s)); assert btns, 'keine showTab-Buttons'
        n = max(int(b.group(1)) for b in btns) + 1
        assert s.count('class="tab-content') == n, 'tab-content %d != %d' % (s.count('class="tab-content'), n)
        last = btns[-1]; end = s.index('</button>', last.start()) + len('</button>')
        s = s[:end] + '\n    <button onclick="showTab(%d)"><!-- FB-SPRECH-WORTSCHATZ -->🗣️ Sprechen</button>' % n + s[end:]
        s, sec = common(s, k)
        lt = list(re.finditer(r'<div class="tab-content[^"]*" id="tab\d+">', s))[-1]
        le = I.element_end(s, lt.start())
        sec = sec.replace('<div class="section" id="sec-sprechen">', '<div class="tab-content" id="tab%d"><div class="section" id="sec-sprechen">' % n, 1).replace('<!-- /FB-SPRECH-WORTSCHATZ -->', '</div><!-- /FB-SPRECH-WORTSCHATZ -->', 1)
        s = s[:le] + sec + s[le:]
        tabs = n + 1
    assert s.count('id="sec-sprechen"') == 1
    if not dry: open(p, 'w', encoding='utf-8').write(s)
    print('eingebaut' + (' [dry]' if dry else ''), p, '·', len(k), 'Karten ·', tabs, 'Tabs')

if __name__ == '__main__':
    dry = '--dry-run' in sys.argv
    for f in [a for a in sys.argv[1:] if not a.startswith('--')]:
        try: main(f, dry)
        except (AssertionError, ValueError, IndexError) as e: print('FEHLER', f, '→', e)
