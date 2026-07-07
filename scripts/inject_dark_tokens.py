#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""FB-DESIGN-TOKENS + Dark Mode + Schalter — generationsrobuster Injektor.
Aufruf: python3 scripts/inject_dark_tokens.py DATEI.html [...]
Idempotent (Marker FB-DESIGN-TOKENS). Pro Datei eine Berichtszeile:
  OK datei | vars=N dark=N specials=... fehlend=... unmapped=a,b
  SKIP datei | grund
"""
import re, sys, os

BG_DARK = {
 'fff':'#262a44','ffffff':'#262a44','white':'#262a44',
 'f8f9fa':'#1d2032','f8f9ff':'#262a44','fafbff':'#262a44','fefefe':'#1a1d2e',
 'f5f7ff':'#2a2e4a','eef0fb':'#1d2032','e1e5fb':'#2e3350','eef0ff':'#262a44',
 'eef1ff':'#262a44','f0f2ff':'#262a44','f0f0f8':'#1d2032','e8eaf6':'#262a44',
 'e8eaff':'#30345a','e8f4fd':'#1e2a3f','e8f5e9':'#1e3328','e8f8f0':'#1e3328',
 'f1f8e9':'#22331e','fdeaea':'#3a2228','ffebee':'#3a2228','fffaf0':'#322c1c',
 'fff5ec':'#322c1c','faf8ff':'#262a44','fafaff':'#262a44','f0f0f0':'#2a2d42',
 'e3f2fd':'#1e2a3f','667eea':'#4a55b8','5568d3':'#5a66cc','4f63c2':'#5a66cc',
 '689f38':'#4e7a2c','e74c3c':'#b0453a','27ae60':'#2f9c5f','2196f3':'#3a86d1',
 'f39c12':'#c67f16','e9ecef':'#2e3250','ccc':'#4a4e6a','c5cff5':'#3a4166',
 'f0ecff':'#2a2547','f0f4ff':'#242a45','e8eaf0':'#262a44','f9f9ff':'#262a44',
 'fff8e1':'#322c1c','fffde7':'#322c1c','ede7f6':'#2a2547','f3e5f5':'#2a2547',
 'e1f5fe':'#1e2a3f','e0f2f1':'#1e3328','fce4ec':'#3a2233','fff3e0':'#322c1c',
}
TX_DARK = {
 '1a1a1a':'#e2e4f0','2c2c2c':'#d6d8e8','333':'#d6d8e8','333333':'#d6d8e8',
 '444':'#c6cade','4a4a4a':'#c6cade','555':'#b6bad0','555555':'#b6bad0',
 '666':'#9ba0bd','666666':'#9ba0bd','6c6c6c':'#979cb8','777':'#979cb8',
 '888':'#8e93b0','888888':'#8e93b0','999':'#7d8199','999999':'#7d8199',
 'aaa':'#6f7390','bbb':'#63677f','ccc':'#5a5e78',
 '667eea':'#93a0f2','3949ab':'#aab4f8','1a237e':'#c3cafd','4a148c':'#c9b5f2',
 '5e35b1':'#b39af0','34206b':'#cbbcf6','241048':'#d9cef8','b15c00':'#e0a860',
 '2e7d32':'#8fd7ae','1b5e20':'#a5d6a7','33691e':'#9ccc65','27ae60':'#58c98b',
 '689f38':'#9ccc65','e74c3c':'#ef7365','c62828':'#ef7365','b71c1c':'#f28b7d',
 'ad1457':'#e57ba1','0d47a1':'#90bff9','1565c0':'#90bff9','e67e22':'#eda15c',
 '2196f3':'#7fb8ef','f39c12':'#edb95e','764ba2':'#b592d8','2e7d59':'#8fd7ae',
 '00695c':'#7fd4c5','01579b':'#90bff9','4e342e':'#d3b8a8','3e2723':'#d3b8a8',
}
BD_DARK = {
 'c5cae9':'#464b70','c5cff5':'#4a5384','c3c9f5':'#4a5384','b9a7f0':'#6b5a9e',
 'dde3ff':'#383d5e','e0e4ff':'#383d5e','e8eaff':'#383d5e','e9ecef':'#2e3250',
 'ffd699':'#7a6335','667eea':'#7b88e8','27ae60':'#3f9d6d','e74c3c':'#b0584d',
 '689f38':'#6d9c47','c62828':'#a04a42','2196f3':'#3a86d1','ccc':'#4a4e6a',
 'f0f0f0':'#3a3e58','e8f5e9':'#3f9d6d','bbb':'#4a4e6a','f39c12':'#c67f16',
 'e67e22':'#c67f16','aaa':'#4a4e6a','ddd':'#3a3e58','eee':'#32365a',
 '764ba2':'#8a63b8','e0e0e0':'#3a3e58','d1c4e9':'#4a4173',
}
SPECIAL_DARK = {
 '--grad-page-a':'#23263e','--grad-page-b':'#2f2440',
 '--grad-head-a':'#4a52a8','--grad-head-b':'#5c4585',
 '--grad-chip-a':'#4a52a8','--grad-chip-b':'#5c4585',
 '--sf-container':'#23263a','--sf-pill':'#343a5e','--sf-input':'#1a1d2e',
}
GRAD_RE = r'linear-gradient\(\s*135deg\s*,\s*#667eea(?:\s+0%)?\s*,\s*#764ba2(?:\s+100%)?\s*\)'
COLOR_RE = re.compile(r'#[0-9a-fA-F]{3}\b|#[0-9a-fA-F]{6}\b|(?<![-\w])white(?![-\w])')

TOGGLE_CSS_TMPL = '''
/* FB-THEME-TOGGLE */
__HEADER_SEL__ { position: relative; }
.theme-toggle {
  position: absolute; top: 14px; right: 14px;
  width: 38px; height: 38px; border-radius: 50%;
  background: rgba(255,255,255,0.18); border: 1px solid rgba(255,255,255,0.4);
  color: white; font-size: 1.05em; cursor: pointer; line-height: 1;
  transition: background 0.2s; z-index: 5;
}
.theme-toggle:hover { background: rgba(255,255,255,0.3); }
'''
TOGGLE_BTN = '<button class="theme-toggle" id="themeToggle" onclick="fbToggleTheme()" aria-label="Hell/Dunkel umschalten">\U0001F319</button>'
INIT_JS = '''<script>/* FB-THEME-INIT */
(function(){
  var saved = null;
  try { saved = localStorage.getItem('fb-theme'); } catch(e) {}
  if (saved === 'dark' || saved === 'light') document.documentElement.dataset.theme = saved;
  function effDark() {
    var t = document.documentElement.dataset.theme;
    if (t === 'dark') return true;
    if (t === 'light') return false;
    return window.matchMedia('(prefers-color-scheme: dark)').matches;
  }
  function paint() {
    var b = document.getElementById('themeToggle');
    if (b) b.textContent = effDark() ? '☀️' : '\U0001F319';
  }
  window.fbToggleTheme = function() {
    var next = effDark() ? 'light' : 'dark';
    document.documentElement.dataset.theme = next;
    try { localStorage.setItem('fb-theme', next); } catch(e) {}
    paint();
  };
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', paint); else paint();
})();
</script>'''

def ctx_of(prop):
    p = prop.strip().lower()
    if p in ('color','caret-color'): return 'tx'
    if p.startswith('background'): return 'bg'
    if p.startswith('border') or p in ('outline','outline-color'): return 'bd'
    return None

import colorsys
def _rgb(c):
    c = c.lstrip('#')
    if c == 'white': return (255,255,255)
    if len(c) == 3: c = ''.join(x*2 for x in c)
    return tuple(int(c[i:i+2],16) for i in (0,2,4))
def _hex(r,g,b): return '#%02x%02x%02x' % (round(r),round(g),round(b))
def auto_dark(ctx, val):
    """Berechneter Dark-Wert fuer unkartierte Farben — Ton bleibt, Helligkeit kippt."""
    try: r,g,b = _rgb(val)
    except Exception: return None
    h,l,sa = colorsys.rgb_to_hls(r/255,g/255,b/255)
    if ctx == 'tx':
        if l >= 0.72: return None            # helle Textfarbe bleibt
        l2 = 0.68 + (0.5-min(l,0.5))*0.3     # dunkel -> pastellhell, Ton erhalten
        r2,g2,b2 = colorsys.hls_to_rgb(h, min(l2,0.86), min(sa,0.75))
    elif ctx == 'bg':
        if l <= 0.45: return None            # dunkle Fills bleiben
        l2 = 0.15 + (1-l)*0.1
        r2,g2,b2 = colorsys.hls_to_rgb(h if sa>0.02 else 0.66, l2, max(sa*0.6, 0.18))
    else:  # bd
        if l >= 0.93 or l <= 0.35: return None
        r2,g2,b2 = colorsys.hls_to_rgb(h if sa>0.02 else 0.66, 0.30, max(sa*0.6, 0.15))
    return _hex(r2*255,g2*255,b2*255)
def dark_of(name):
    ctx, s = name[2:4], name[5:]
    kur = {'bg':BG_DARK,'tx':TX_DARK,'bd':BD_DARK}[ctx].get(s)
    return kur or auto_dark(ctx, s if s=='white' else '#'+s)

def block_sub(css, sel_re, inner_old_re, inner_new, maxblock=4000):
    """Ersetzt inner_old_re nur INNERHALB des ersten Blocks, dessen Selektor sel_re matcht."""
    m = re.search(sel_re + r'\s*\{', css)
    if not m: return css, False
    start = m.end(); end = css.find('}', start)
    if end < 0 or end - start > maxblock: return css, False
    inner = css[start:end]
    inner2, n = re.subn(inner_old_re, inner_new, inner, count=1)
    if not n: return css, False
    return css[:start] + inner2 + css[end:], True

def process(fn):
    html = open(fn, encoding='utf-8').read()
    if 'FB-DESIGN-TOKENS' in html:
        return 'SKIP %s | bereits tokenisiert' % fn
    blocks = list(re.finditer(r'<style[^>]*>(.*?)</style>', html, re.S))
    if not blocks: return 'SKIP %s | kein style-Block' % fn
    m = blocks[0]
    css = m.group(1)
    rest_css = [b.group(1) for b in blocks[1:]]

    specials_ok, specials_fehlend = [], []
    used = {}; special_light = {}

    css, ok = block_sub(css, r'(?<![\w.#-])body', r'(background\s*:\s*)'+GRAD_RE,
        r'\1linear-gradient(135deg, var(--grad-page-a) 0%, var(--grad-page-b) 100%)')
    if not ok:
        return 'SKIP %s | body-Gradient nicht gefunden (fremdes Layout)' % fn
    special_light['--grad-page-a']='#667eea'; special_light['--grad-page-b']='#764ba2'
    specials_ok.append('page')

    css, ok = block_sub(css, r'\.header', r'(background\s*:\s*)'+GRAD_RE,
        r'\1linear-gradient(135deg, var(--grad-head-a), var(--grad-head-b))')
    if ok:
        special_light['--grad-head-a']='#667eea'; special_light['--grad-head-b']='#764ba2'
        specials_ok.append('head')
    else: specials_fehlend.append('head')

    css, ok = block_sub(css, r'\.wort-chip', r'(background\s*:\s*)'+GRAD_RE,
        r'\1linear-gradient(135deg, var(--grad-chip-a), var(--grad-chip-b))')
    if ok:
        special_light['--grad-chip-a']='#667eea'; special_light['--grad-chip-b']='#764ba2'
        specials_ok.append('chip')

    css, ok = block_sub(css, r'\.container', r'(background\s*:\s*)(?:#fff\b|#ffffff\b|white\b)',
        r'\1var(--sf-container)')
    if ok: special_light['--sf-container']='#fff'; specials_ok.append('container')
    else: specials_fehlend.append('container')

    css, ok = block_sub(css, r'\.nav-btn\.active', r'(background\s*:\s*)(?:#fff\b|#ffffff\b|white\b)',
        r'\1var(--sf-pill)')
    if ok: special_light['--sf-pill']='#fff'; specials_ok.append('pill')
    else: specials_fehlend.append('pill')

    css, ok = block_sub(css, r'input\.blank', r'(background\s*:\s*)(?:#fff\b|#ffffff\b|white\b)',
        r'\1var(--sf-input)')
    if ok: special_light['--sf-input']='white'; specials_ok.append('input')

    def decl(mm):
        prop, val = mm.group(1), mm.group(2)
        ctx = ctx_of(prop)
        if ctx is None or 'gradient' in val or 'var(--' in val:
            return mm.group(0)
        def sub(cm):
            name = '--%s-%s' % (ctx, cm.group(0).lstrip('#').lower())
            used[name] = cm.group(0)
            return 'var(%s)' % name
        return prop + mm.group(0)[len(prop):len(prop)+mm.group(0)[len(prop):].index(val)] + COLOR_RE.sub(sub, val)
    css = re.sub(r'([a-zA-Z-]+)\s*:\s*([^;{}]+)', decl, css)
    rest_css = [re.sub(r'([a-zA-Z-]+)\s*:\s*([^;{}]+)', decl, rc) for rc in rest_css]

    light = ['  %s: %s;' % (k,v) for k,v in sorted(special_light.items())]
    light += ['  %s: %s;' % (k,v) for k,v in sorted(used.items())]
    dark, unmapped = [], []
    for k in sorted(special_light):
        dark.append('  %s: %s;' % (k, SPECIAL_DARK[k]))
    for k in sorted(used):
        dv = dark_of(k)
        if dv: dark.append('  %s: %s;' % (k, dv))
        else: unmapped.append(used[k])
    dark_body = '\n'.join(dark)
    root = '/* ===== FB-DESIGN-TOKENS (auto) ===== */\n:root {\n' + '\n'.join(light) + '\n}\n'
    extras_media = '.tab-banner { box-shadow: 0 2px 8px rgba(0,0,0,0.45); }\nbody { color: #c6cade; }\nbutton, input, select, textarea { color: inherit; }'
    extras_manual = 'html[data-theme="dark"] .tab-banner { box-shadow: 0 2px 8px rgba(0,0,0,0.45); }\nhtml[data-theme="dark"] body { color: #c6cade; }\nhtml[data-theme="dark"] button, html[data-theme="dark"] input, html[data-theme="dark"] select, html[data-theme="dark"] textarea { color: inherit; }'
    darkblock = ('\n/* ===== FB-DARK-MODE (System-Default + manueller Schalter) ===== */\n'
      '@media (prefers-color-scheme: dark) {\n:root:not([data-theme="light"]) {\n'+dark_body+'\n}\n'+extras_media+'\n}\n'
      ':root[data-theme="dark"] {\n'+dark_body+'\n}\n'+extras_manual+'\n')

    hat_header = re.search(r'<div class="header"[^>]*>|<header[^>]*>', html)
    header_sel = '.header' if (hat_header and 'class="header"' in hat_header.group(0)) else 'header'
    toggle_css = (TOGGLE_CSS_TMPL.replace('__HEADER_SEL__', header_sel)) if hat_header else ''
    if rest_css:
        # Folgebloecke von hinten nach vorn ersetzen (Offsets bleiben gueltig), Dark-Block in den LETZTEN
        for i in range(len(blocks)-1, 0, -1):
            b = blocks[i]
            neu = rest_css[i-1] + (darkblock if i == len(blocks)-1 else '')
            html = html[:b.start(1)] + neu + html[b.end(1):]
        new_css = root + css + toggle_css
    else:
        new_css = root + css + toggle_css + darkblock
    html = html[:m.start(1)] + new_css + html[m.end(1):]

    if hat_header:
        h2 = re.search(r'<div class="header"[^>]*>|<header[^>]*>', html)
        html = html[:h2.end()] + '\n  ' + TOGGLE_BTN + html[h2.end():]
        specials_ok.append('toggle')
    else:
        specials_fehlend.append('toggle')

    html = html.replace('</style>', '</style>\n' + INIT_JS, 1)

    if '<meta name="theme-color"' not in html:
        mv = re.search(r'<meta name="viewport"[^>]*>', html)
        if mv:
            html = html[:mv.end()] + '\n<meta name="theme-color" content="#667eea" media="(prefers-color-scheme: light)">\n<meta name="theme-color" content="#23263e" media="(prefers-color-scheme: dark)">' + html[mv.end():]

    def inline_repl(mm):
        s = mm.group(1)
        if 'data:' in s: return mm.group(0)
        def d(dm):
            prop, val = dm.group(1), dm.group(2)
            ctx = ctx_of(prop)
            if ctx is None or 'gradient' in val or 'var(--' in val: return dm.group(0)
            def sub(cm):
                name = '--%s-%s' % (ctx, cm.group(0).lstrip('#').lower())
                if name not in used: return cm.group(0)
                return 'var(%s)' % name
            return prop + dm.group(0)[len(prop):len(prop)+dm.group(0)[len(prop):].index(val)] + COLOR_RE.sub(sub, val)
        return 'style="' + re.sub(r'([a-zA-Z-]+)\s*:\s*([^;"]+)', d, s) + '"'
    head, sep, body = html.partition('</style>')
    body = re.sub(r'style="([^"]*)"', inline_repl, body)
    html = head + sep + body

    open(fn, 'w', encoding='utf-8').write(html)
    return 'OK %s | vars=%d dark=%d specials=%s fehlend=%s unmapped=%s' % (
        fn, len(used)+len(special_light), len(dark),
        ','.join(specials_ok), ','.join(specials_fehlend) or '-',
        ','.join(sorted(set(unmapped))) or '-')

if __name__ == '__main__':
    for fn in sys.argv[1:]:
        try: print(process(fn))
        except Exception as e: print('SKIP %s | FEHLER %s' % (fn, e))
