#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Gate: tokenisierte Dateien muessen den vollstaendigen Dark-Mode-Bau tragen.
Dateien OHNE FB-DESIGN-TOKENS werden ignoriert (Rollout inkrementell).
Exit 1 bei jedem tokenisierten Teilausbau."""
import re, sys, glob

def check(fn):
    h = open(fn, encoding='utf-8', errors='ignore').read()
    if 'FB-DESIGN-TOKENS' not in h: return []
    fehler = []
    if 'FB-DARK-MODE' not in h: fehler.append('FB-DARK-MODE-Block fehlt')
    if ':root:not([data-theme="light"])' not in h: fehler.append('Media-Dark-Selektor fehlt')
    if ':root[data-theme="dark"]' not in h: fehler.append('manueller Dark-Selektor fehlt')
    hat_header = re.search(r'<div class="header"[^>]*>|<header[^>]*>', h)
    if 'id="themeToggle"' not in h and hat_header: fehler.append('Schalter fehlt trotz Header')
    if 'FB-THEME-INIT' not in h: fehler.append('Theme-Init-Script fehlt')
    if not re.search(r'color:\s*#c6cade', h): fehler.append('Dark-Default-Textfarbe fehlt')
    return fehler

if __name__ == '__main__':
    args = sys.argv[1:] or sorted(glob.glob('**/*.html', recursive=True))
    args = [f for f in args if 'daf-archiv' not in f and 'backup' not in f]
    kaputt = 0
    for fn in args:
        f = check(fn)
        if f:
            kaputt += 1
            print('FEHLER %s: %s' % (fn, '; '.join(f)))
    print('%d Datei(en) mit Teilausbau' % kaputt)
    sys.exit(1 if kaputt else 0)
