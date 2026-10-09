#!/usr/bin/env python3
"""Satzbau-Timer stoppt im Gerüst-Modus nicht (Fund 2026-10-09).
Ursache: Der Gerüst-Add-on (geruest_patch.js) ruft sbCheckAllDone() nur auf, wenn die Datei es
definiert — in ~230 Lektionen fehlt es, der Timer läuft nach vollständiger Lösung weiter.
Fix: im Add-on-Block direkt nach `var CFG = …;` eine Rückfall-Definition einsetzen, die den
Satzbau-Timer der Datei (CFG.tab) stoppt, sobald alle Zeilen grün sind. Idempotent (Marker).
Aufruf: python3 scripts/fix_sb_timer.py DATEI.html [...]   (--dry-run: nur melden)"""
import sys, re
MARK = '/* FB-SB-TIMER-FALLBACK */'
ZEILE = ('  ' + MARK + ' if (typeof sbCheckAllDone !== "function") window.sbCheckAllDone = function(){'
         ' var ok = satzbauData.every(function(_, i){ var r = document.getElementById(CFG.row + i); return r && r.classList.contains("correct"); });'
         ' if (ok && typeof stopTimer === "function") stopTimer(CFG.tab); };')
dry = '--dry-run' in sys.argv
for f in [a for a in sys.argv[1:] if not a.startswith('--')]:
    s = open(f, encoding='utf-8').read()
    if MARK in s: print('schon da   ', f); continue
    if re.search(r'function sbCheckAllDone\b|sbCheckAllDone\s*=\s*function', s): print('hat eigene', f); continue
    m = re.search(r'(/\* ── Gerüst-Modus Add-on[\s\S]*?\n  var CFG = \{[^\n]*\};\n)', s)
    if not m: print('KEIN BLOCK ', f); continue
    s = s[:m.end()] + ZEILE + '\n' + s[m.end():]
    if not dry: open(f, 'w', encoding='utf-8').write(s)
    print('repariert  ', f)
