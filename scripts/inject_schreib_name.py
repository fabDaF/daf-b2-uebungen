#!/usr/bin/env python3
"""inject_schreib_name.py — Namensfeld-Pflicht für die Schreibwerkstatt.

Problem: 369 ältere Schreibwerkstatt-Lektionen haben KEIN Namensfeld
(`#schreib-name`) und senden deshalb zwangsläufig als „Anonymer Einsender".
Die 147 modernen Lektionen haben Feld + harte Sperre (schreibNameOk ≥2 Zeichen).

Statt HTML in 369 heterogene Layouts zu injizieren (Anker variiert stark),
hängt dieses Skript EIN selbst-installierendes JS-Modul (Marker FB-NAME-REQUIRED)
vor </body> an. Das Modul, layout- und generationsunabhängig:
  1. Baut zur Laufzeit ein Namensfeld in den Schreib-Bereich ein, falls keins da
     ist (inline-Styles, keine CSS-Abhängigkeit).
  2. Kapselt den Sende-Choke-Point `schreibPostFormsubmit` per Monkey-Patch:
     Name < 2 Zeichen ⇒ kein Versand, Fokus + Hinweis, onErr('NAME_MISSING')
     (die Aufrufer setzen den Button in onErr zurück).
  3. Macht die Fehlermeldung für NAME_MISSING freundlich.
Zusätzlich wird der Fallback-String im `schreibAktuellerName`-Return entfernt
(`.trim() || '…Einsender…'` → `.trim()`), damit „Anonymer Einsender" komplett
verschwindet.

Idempotent: FB-NAME-REQUIRED-Marker verhindert Doppel-Einbau. Läuft gefahrlos
auch auf den 147 modernen Dateien (Feld existiert → nicht doppelt eingebaut,
Patch harmlos redundant).

Aufruf:  python3 scripts/inject_schreib_name.py datei1.html [datei2 …]
"""
import re
import sys
import os

MARKER = 'FB-NAME-REQUIRED'

MODULE = r'''<!-- FB-NAME-REQUIRED: Namensfeld-Pflicht (2026-07-16) -->
<script>
(function(){
  if (window.__fbNameRequired) return; window.__fbNameRequired = true;
  var NAME_ID = 'schreib-name';
  function nameVal(){ var i=document.getElementById(NAME_ID); return i ? (i.value||'').trim() : ''; }
  if (typeof window.schreibNameOk !== 'function') {
    window.schreibNameOk = function(){ return nameVal().length >= 2; };
  }
  if (typeof window.schreibPostFormsubmit === 'function') {
    var _origPost = window.schreibPostFormsubmit;
    window.schreibPostFormsubmit = function(subject, message, onOk, onErr){
      if (nameVal().length < 2){
        var inp = document.getElementById(NAME_ID);
        if (inp){ try{ inp.focus(); }catch(e){} if (inp.scrollIntoView) inp.scrollIntoView({behavior:'smooth', block:'center'}); }
        var hint = document.getElementById('fb-name-hint');
        if (hint){ hint.textContent = '⚠️ Bitte trage oben deinen Namen ein — ohne Namen kann der Text nicht gesendet werden.'; hint.style.color = '#c0392b'; }
        if (typeof onErr === 'function') onErr(new Error('NAME_MISSING'));
        return;
      }
      return _origPost.apply(this, arguments);
    };
  }
  if (typeof window.schreibFehlerErklaerung === 'function') {
    var _origFehler = window.schreibFehlerErklaerung;
    window.schreibFehlerErklaerung = function(err){
      if (err && err.message === 'NAME_MISSING') return 'Bitte trage oben im Namensfeld deinen Namen ein — ohne Namen kann der Text nicht gesendet werden.';
      return _origFehler.apply(this, arguments);
    };
  }
  function insertNameField(){
    if (document.getElementById(NAME_ID)) return;
    var ta = document.querySelector('.schreib-mini-textarea');
    if (!ta) return;
    var sec = ta.closest('.section, .tab-content, section') || ta.parentNode;
    var host = sec.querySelector('.sec-inner') || sec;
    var block = document.createElement('div');
    block.className = 'schreib-name-block';
    block.style.cssText = 'margin:0 0 18px; padding:14px 16px; background:#fff5f5; border:1px solid #f3c6c6; border-radius:10px;';
    block.innerHTML =
      '<label for="' + NAME_ID + '" style="display:block; font-weight:600; color:#b71c1c; margin-bottom:6px;">Dein Name — Pflicht, damit Frank weiß, wer schreibt:</label>'
      + '<input type="text" id="' + NAME_ID + '" placeholder="Dein Vor- und Nachname" autocomplete="name" style="width:100%; max-width:360px; padding:10px 14px; border:2px solid #e74c3c; border-radius:8px; font-family:inherit; font-size:0.98em; outline:none; box-sizing:border-box;">'
      + '<div id="fb-name-hint" style="font-size:0.85em; color:#777; margin-top:6px;">Ohne Namen wird der Text nicht gesendet.</div>';
    var h2 = host.querySelector('h2');
    if (h2 && h2.parentNode === host) host.insertBefore(block, h2.nextSibling);
    else host.insertBefore(block, host.firstChild);
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', insertNameField);
  else insertNameField();
})();
</script>
'''

# Fallback-String im schreibAktuellerName-Return entfernen.
RE_FALLBACK = re.compile(r"\.trim\(\)\s*\|\|\s*'(?:Anonymer Einsender|Anonyme Einsenderin / anonymer Einsender)'")


def process(path):
    s = open(path, encoding='utf-8').read()
    orig = s
    changed = []
    # 1) Fallback-String weg
    s2, n = RE_FALLBACK.subn('.trim()', s)
    if n:
        s = s2
        changed.append(f'Fallback×{n} entfernt')
    # 2) Modul anhängen (idempotent)
    if MARKER not in s:
        idx = s.rfind('</body>')
        if idx == -1:
            changed.append('KEIN </body> — Modul NICHT eingebaut')
        else:
            s = s[:idx] + MODULE + '\n' + s[idx:]
            changed.append('Modul eingebaut')
    else:
        changed.append('Modul bereits vorhanden')
    if s != orig:
        open(path, 'w', encoding='utf-8').write(s)
    return changed


def main(argv):
    if not argv:
        print('Usage: inject_schreib_name.py datei.html …'); return 1
    for p in argv:
        if not os.path.isfile(p):
            print(f'  MISSING {p}'); continue
        ch = process(p)
        print(f'  {os.path.basename(p)}: {", ".join(ch)}')
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
