#!/usr/bin/env python3
"""inject_schreib_name.py — Namenspflicht in der Schreibwerkstatt erzwingen.

Ausgangslage (korrekt ermittelt 2026-07-16):
  · ALLE 599 Schreibwerkstatt-Lektionen haben bereits ein Namensfeld
    (147 modern `id="schreib-name"`, 488 älter `id="sw-name"`). KEINE ist feldlos.
  · Beide Generationen sperren meist schon (modern `schreibNameOk`, alt
    `schreibValidiereName`) — ABER ~88 alte Dateien haben KEINEN Namens-Guard im
    Einzel-Versand, ~71 keinen im Alle-Versand: dort ist namenloses Senden möglich.
  · Der String „Anonymer Einsender" steckt nur in den 147 modernen als toter
    Fallback im `schreibAktuellerName`-Return.

Fix (ein selbst-installierendes JS-Modul, Marker FB-NAME-REQUIRED, vor </body>):
  · Kapselt den uniformen Sende-Choke-Point `schreibPostFormsubmit` per
    Monkey-Patch. Name < 2 Zeichen ⇒ KEIN Versand: Fokus + Shake auf das
    bestehende Feld, onErr('NAME_MISSING') (Aufrufer setzen den Button zurück).
    Liest das VORHANDENE Feld (schreib-name ODER sw-name) — baut KEIN neues Feld
    ein (jede Datei hat schon eins; frühere Einbau-Variante erzeugte Doppler).
  · Macht die Fehlermeldung für NAME_MISSING freundlich.
Zusätzlich: Fallback-String im `schreibAktuellerName`-Return entfernen
  (`.trim() || '…Einsender…'` → `.trim()`).

Idempotent: ein vorhandener FB-NAME-REQUIRED-Block wird ERSETZT (nicht gedoppelt),
damit Modul-Updates greifen. Läuft gefahrlos auf allen 599 (redundant, wo schon
ein Trigger-Guard existiert).

Aufruf:  python3 scripts/inject_schreib_name.py datei1.html [datei2 …]
"""
import re
import sys
import os

MARKER = 'FB-NAME-REQUIRED'

MODULE = r'''<!-- FB-NAME-REQUIRED: Namenspflicht beim Senden (2026-07-16) -->
<script>
(function(){
  if (window.__fbNameRequired) return; window.__fbNameRequired = true;
  function nameInput(){ return document.getElementById('schreib-name') || document.getElementById('sw-name') || document.querySelector('input.schreib-name'); }
  function nameVal(){ var i = nameInput(); return i ? (i.value || '').trim() : ''; }
  function blockUI(){
    var inp = nameInput();
    if (!inp) return;
    try { inp.focus(); } catch(e){}
    var box = (inp.closest && inp.closest('.schreib-name-box, .schreib-name-block')) || inp.parentNode;
    if (box){ box.classList.add('shake'); setTimeout(function(){ box.classList.remove('shake'); }, 500); }
    var hint = document.getElementById('fb-name-hint');
    if (hint){ hint.textContent = '⚠️ Bitte trage oben deinen Namen ein — ohne Namen kann der Text nicht gesendet werden.'; hint.style.color = '#c0392b'; }
    if (inp.scrollIntoView) inp.scrollIntoView({behavior:'smooth', block:'center'});
  }
  // Trigger umschließen (deckt ALLE Generationen ab, auch die ohne schreibPostFormsubmit):
  ['schreibSendenEinzeln', 'schreibSendenAlleNochOffenen'].forEach(function(fn){
    if (typeof window[fn] === 'function'){
      var _o = window[fn];
      window[fn] = function(){ if (nameVal().length < 2){ blockUI(); return; } return _o.apply(this, arguments); };
    }
  });
  // Belt-and-suspenders: Choke-Point (falls ein Sende-Pfad nicht über die Trigger läuft):
  if (typeof window.schreibPostFormsubmit === 'function') {
    var _origPost = window.schreibPostFormsubmit;
    window.schreibPostFormsubmit = function(subject, message, onOk, onErr){
      if (nameVal().length < 2){ blockUI(); if (typeof onErr === 'function') onErr(new Error('NAME_MISSING')); return; }
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
})();
</script>
'''

RE_FALLBACK = re.compile(r"\.trim\(\)\s*\|\|\s*'(?:Anonymer Einsender|Anonyme Einsenderin / anonymer Einsender)'")
RE_MODULE = re.compile(r'[ \t]*<!-- FB-NAME-REQUIRED.*?</script>\n?', re.S)


def process(path):
    s = open(path, encoding='utf-8').read()
    orig = s
    changed = []
    s2, n = RE_FALLBACK.subn('.trim()', s)
    if n:
        s = s2
        changed.append(f'Fallback×{n} entfernt')
    # Vorhandenen Modul-Block entfernen (Update statt Doppeln)
    s, r = RE_MODULE.subn('', s)
    if r:
        changed.append('Alt-Modul ersetzt')
    idx = s.rfind('</body>')
    if idx == -1:
        changed.append('KEIN </body> — Modul NICHT eingebaut')
    else:
        s = s[:idx] + MODULE + '\n' + s[idx:]
        if 'Alt-Modul ersetzt' not in changed:
            changed.append('Modul eingebaut')
    if s != orig:
        open(path, 'w', encoding='utf-8').write(s)
    return changed


def main(argv):
    if not argv:
        print('Usage: inject_schreib_name.py datei.html …'); return 1
    for p in argv:
        if not os.path.isfile(p):
            print(f'  MISSING {p}'); continue
        print(f'  {os.path.basename(p)}: {", ".join(process(p))}')
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
