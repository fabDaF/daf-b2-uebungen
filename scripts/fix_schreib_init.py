#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""FB-SCHREIB-INIT-FIX (2026-07-13, Frank: „keine Wortzahl, Text nach dem Schließen weg").

BEFUND
------
In 51 Lektionen wird `initSchreibwerkstatt()` beim Laden NIE aufgerufen. Der Aufruf ist
beim Patchen in eine fremde Funktion gerutscht — typischerweise ans Ende von
`resetSatzbau()` / `sbResetAll()` / `resetWs()` —, statt im DOMContentLoaded-Init bzw. im
Tab-Wechsel zu stehen. Folge: KEIN input-Listener auf den Textareas, also
  · der Wortzähler bleibt bei 0 und
  · der Text wird nie in localStorage gespeichert → beim Schließen des Fensters ist er weg.
Das ist Datenverlust beim Schüler, nicht nur ein Schönheitsfehler.

FIX
---
Ein idempotenter Init-Hook ans Dateiende (Marker FB-SCHREIB-INIT-FIX):
  · ruft `initSchreibwerkstatt()` garantiert einmal beim Laden auf,
  · macht spätere Aufrufe (z. B. aus resetSatzbau) per Once-Guard zu No-Ops,
    damit keine doppelten Listener entstehen.
Die bestehenden Regeln bleiben unangetastet — minimaler Diff, kein Umbau der Datei.

Aufruf:  python3 scripts/fix_schreib_init.py datei1.html datei2.html …
         python3 scripts/fix_schreib_init.py --list liste.txt
Verifikation: der JSDOM-Test (scripts/check_schreib_init.js) muss danach grün sein.
"""
import sys, pathlib

MARKER = 'FB-SCHREIB-INIT-FIX'

BLOCK = """
<!-- FB-SCHREIB-INIT-FIX: garantiert genau EINEN Init-Lauf der Schreibwerkstatt.
     Ohne ihn fehlt der input-Listener → Wortzähler bleibt 0 und der Text wird
     nicht in localStorage gespeichert (Datenverlust beim Schließen des Fensters). -->
<script>
(function () {
  if (typeof initSchreibwerkstatt !== 'function') return;
  var orig = initSchreibwerkstatt;
  var done = false;
  window.initSchreibwerkstatt = function () {
    if (done) return;            // Once-Guard: keine doppelten Listener
    done = true;
    return orig.apply(this, arguments);
  };
  function go() { try { window.initSchreibwerkstatt(); } catch (e) {} }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', go);
  else go();
})();
</script>
</body>"""


def files_from_args(argv):
    if argv and argv[0] == '--list':
        return [l.strip() for l in open(argv[1], encoding='utf-8') if l.strip()]
    return argv


def main():
    args = files_from_args(sys.argv[1:])
    gefixt, skip = [], []
    for a in args:
        p = pathlib.Path(a)
        t = p.read_text(encoding='utf-8')
        if MARKER in t:
            skip.append((p.name, 'schon gefixt'))
            continue
        if 'function initSchreibwerkstatt' not in t:
            skip.append((p.name, 'keine Schreibwerkstatt'))
            continue
        if '</body>' not in t:
            skip.append((p.name, 'kein </body>'))
            continue
        # letztes </body> ersetzen (robust gegen </body> in Strings weiter oben)
        i = t.rfind('</body>')
        p.write_text(t[:i] + BLOCK.lstrip('\n') + t[i + len('</body>'):], encoding='utf-8')
        gefixt.append(p.name)

    print('gefixt: %d' % len(gefixt))
    for n, grund in skip:
        print('  SKIP %s — %s' % (n, grund))
    return 0


if __name__ == '__main__':
    sys.exit(main())
