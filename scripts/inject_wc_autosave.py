#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""FB-WC-AUTOSAVE (2026-07-13) — Wortzähler und Autosave für ältere Schreibwerkstätten.

BEFUND
------
36 Lektionen stammen aus älteren Schreibwerkstatt-Generationen und haben gar keinen
Wortzähler im Markup; 13 davon (AMDP, dynamisch gebaute Karten) speichern den Text auch
nicht in localStorage. Symptome für den Schüler: keine Wortzahl — und bei den AMDP-Dateien
ist der Text nach dem Schließen des Fensters weg.

FIX
---
Ein selbst-installierendes Modul (Marker FB-WC-AUTOSAVE) ans Dateiende:
  · verkabelt JEDE `.schreib-mini-textarea` — auch dynamisch erzeugte (Re-Scan nach
    Klicks und nach kurzer Verzögerung),
  · hängt einen Wortzähler an, WENN die Karte noch keinen hat (bestehende .wc-N-Zähler
    werden weiterbenutzt, nicht verdoppelt),
  · schaltet Autosave NUR ein, wenn die Datei keinen eigenen hat (erkannt an
    `typeof SCHREIB_KEY_PREFIX === 'undefined'`) — kein doppeltes Speichern,
  · markiert verkabelte Felder mit data-fb-wc, ist also idempotent.

Aufruf:  python3 scripts/inject_wc_autosave.py datei.html …
         python3 scripts/inject_wc_autosave.py --list liste.txt
"""
import sys, pathlib

MARKER = 'FB-WC-AUTOSAVE'

BLOCK = """
<!-- FB-WC-AUTOSAVE: Wortzähler + (falls nötig) Autosave für ältere Schreibwerkstätten.
     Bestehende Zähler und ein bereits vorhandener Autosave werden NICHT verdoppelt. -->
<script>
(function () {
  var SLUG = (location.pathname.split('/').pop() || 'lektion').replace(/\\.html?$/, '');
  // Die moderne Schreibwerkstatt-Generation bringt initSchreibwerkstatt() mit — und damit
  // einen eigenen Autosave. Nur die alten (AMDP: buildSchreibwerkstatt) brauchen unseren.
  var eigenerAutosave = (typeof initSchreibwerkstatt === 'function')
                        || (typeof SCHREIB_KEY_PREFIX !== 'undefined');

  function key(ta, i) { return 'fb-sw-' + SLUG + '-' + (ta.dataset.aufgabe || i); }
  function woerter(t) { t = (t || '').trim(); return t ? t.split(/\\s+/).length : 0; }

  function install() {
    var tas = document.querySelectorAll('.schreib-mini-textarea, .schreibfeld-area');
    Array.prototype.forEach.call(tas, function (ta, i) {
      if (ta.dataset.fbWc) return;                 // schon verkabelt
      ta.dataset.fbWc = '1';

      var karte = ta.closest('.schreib-aufgabe-karte, .schreib-karte, .schreibfeld-block') || ta.parentNode;
      var da = karte.querySelector('[class^="wc-"], [class*=" wc-"], .fb-wc strong, .schreib-count');
      var ziel;
      if (da) {
        ziel = da;
      } else {
        var box = document.createElement('div');
        box.className = 'fb-wc';
        box.style.cssText = 'font-size:0.82em;color:#4a5a8c;margin-top:6px;font-family:"Segoe UI",system-ui,sans-serif;';
        box.innerHTML = 'W\\u00f6rter: <strong>0</strong>';
        if (ta.nextSibling) karte.insertBefore(box, ta.nextSibling); else karte.appendChild(box);
        ziel = box.querySelector('strong');
      }

      if (!eigenerAutosave) {
        try { var s = localStorage.getItem(key(ta, i)); if (s && !ta.value) ta.value = s; } catch (e) {}
      }

      function update() {
        ziel.textContent = woerter(ta.value);
        // nie leere Werte anlegen — sonst füllt sich der Speicher mit Müll-Keys
        if (!eigenerAutosave && ta.value) { try { localStorage.setItem(key(ta, i), ta.value); } catch (e) {} }
      }
      ta.addEventListener('input', update);
      update();
    });
  }

  function start() {
    install();
    setTimeout(install, 400);                       // dynamisch gebaute Karten nachziehen
    document.addEventListener('click', function () { setTimeout(install, 60); }, true);
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', start);
  else start();
})();
</script>
</body>"""


def main():
    args = sys.argv[1:]
    if args and args[0] == '--list':
        args = [l.strip() for l in open(args[1], encoding='utf-8') if l.strip()]

    gefixt, skip = [], []
    for a in args:
        p = pathlib.Path(a)
        t = p.read_text(encoding='utf-8')
        if MARKER in t:
            skip.append((p.name, 'schon gefixt'))
            continue
        if 'schreib-mini-textarea' not in t and 'schreibfeld-area' not in t:
            skip.append((p.name, 'kein Schreibfeld'))
            continue
        if '</body>' not in t:
            skip.append((p.name, 'kein </body>'))
            continue
        i = t.rfind('</body>')
        p.write_text(t[:i] + BLOCK.lstrip('\n') + t[i + len('</body>'):], encoding='utf-8')
        gefixt.append(p.name)

    print('gefixt: %d' % len(gefixt))
    for n, g in skip:
        print('  SKIP %s — %s' % (n, g))
    return 0


if __name__ == '__main__':
    sys.exit(main())
