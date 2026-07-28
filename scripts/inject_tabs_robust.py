#!/usr/bin/env python3
"""inject_tabs_robust.py — FB-TABS-ROBUST

Produzent fuer die robuste Tab-Umschaltung in DaF-Lektionen.

Warum:
  Die Tab-Umschaltung haengt in den Lektionen an zwei fragilen Saeulen:
    1. Inline-Attribute  onclick="showSection(n)"  bzw.  onclick="showTab(n)"
    2. Eine positionsbasierte Funktion, die  sections[n] / buttons[n]  blind
       indiziert und bei jeder Abweichung (fehlende Section, verschobener
       Tab, ausgetauschtes Attribut) still nichts tut.
  Faellt eine der beiden aus — Inline-Handler von einem Browser-Blocker
  entfernt, Index verschoben, Funktion durch einen Fehler in ihrem
  Script-Block nie definiert — passiert beim Klick GAR NICHTS. Genau dieses
  Symptom ist am 2026-07-28 in Safari an A2 2057G aufgetreten (in Chrome
  war dieselbe Datei einwandfrei).

Was das Modul tut (selbst-installierend, vor </body>):
  * definiert showSection/showTab defensiv neu (Bereichspruefung, frische
    DOM-Abfrage bei jedem Aufruf, keine harten Indizes ueber die Laenge)
  * haengt zusaetzlich einen DELEGIERTEN Klick-Listener an document
    (Capture-Phase). Damit funktionieren die Tabs auch dann, wenn die
    Inline-onclick-Attribute fehlen oder entfernt wurden.
  * macht die Tab-Buttons per Tastatur bedienbar (role/tabindex, Enter/Space)
  * stellt sicher, dass immer genau eine Section aktiv ist

Doppel-Ausloesung ist unschaedlich: Delegierter Listener und Inline-Handler
rufen dieselbe idempotente Funktion mit demselben Index auf.

Aufruf:
    python3 scripts/inject_tabs_robust.py DATEI.html [DATEI2.html ...]

Idempotent — Marker FB-TABS-ROBUST. Ein vorhandener Block wird ersetzt.
"""

import io
import re
import sys

MARKER = "FB-TABS-ROBUST"

MODULE = """
<!-- FB-TABS-ROBUST -->
<script>
(function () {
  if (window.__fbTabsRobust) { return; }
  window.__fbTabsRobust = true;

  function sections() { return document.querySelectorAll('.section'); }
  function buttons()  { return document.querySelectorAll('.nav-btn'); }

  function activate(idx) {
    var secs = sections();
    var btns = buttons();
    if (!secs.length) { return false; }
    idx = parseInt(idx, 10);
    if (isNaN(idx) || idx < 0 || idx >= secs.length) { return false; }
    for (var i = 0; i < secs.length; i++) { secs[i].classList.remove('active'); }
    for (var k = 0; k < btns.length; k++) { btns[k].classList.remove('active'); }
    secs[idx].classList.add('active');
    if (btns[idx]) { btns[idx].classList.add('active'); }
    return true;
  }

  window.showSection = function (idx) { return activate(idx); };
  window.showTab     = function (idx) { return activate(idx); };

  function navBtnOf(node) {
    while (node && node !== document) {
      if (node.classList && node.classList.contains('nav-btn')) { return node; }
      node = node.parentNode;
    }
    return null;
  }

  document.addEventListener('click', function (e) {
    var btn = navBtnOf(e.target);
    if (!btn) { return; }
    var list = buttons();
    for (var i = 0; i < list.length; i++) {
      if (list[i] === btn) { activate(i); return; }
    }
  }, true);

  document.addEventListener('keydown', function (e) {
    if (e.key !== 'Enter' && e.key !== ' ' && e.key !== 'Spacebar') { return; }
    var btn = navBtnOf(document.activeElement);
    if (!btn) { return; }
    e.preventDefault();
    btn.click();
  });

  function init() {
    var list = buttons();
    for (var i = 0; i < list.length; i++) {
      if (!list[i].hasAttribute('role'))     { list[i].setAttribute('role', 'button'); }
      if (!list[i].hasAttribute('tabindex')) { list[i].setAttribute('tabindex', '0'); }
    }
    if (!document.querySelector('.section.active')) { activate(0); }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
</script>
<!-- /FB-TABS-ROBUST -->
"""

BLOCK_RE = re.compile(
    r"\n?<!-- FB-TABS-ROBUST -->.*?<!-- /FB-TABS-ROBUST -->\n?",
    re.S,
)


def patch(path):
    html = io.open(path, encoding="utf-8").read()

    # Nur Lektionen mit Tab-Navigation und Sections anfassen.
    if "nav-btn" not in html or 'class="section' not in html:
        return "SKIP (keine Tab-Struktur)"

    replaced = MARKER in html
    if replaced:
        html = BLOCK_RE.sub("\n", html)

    idx = html.lower().rfind("</body>")
    if idx < 0:
        return "FEHLER (kein </body>)"

    out = html[:idx] + MODULE + html[idx:]
    io.open(path, "w", encoding="utf-8").write(out)
    return "ERSETZT" if replaced else "EINGEBAUT"


def main(argv):
    if not argv:
        print(__doc__)
        return 1
    rc = 0
    for path in argv:
        try:
            status = patch(path)
        except Exception as exc:  # pragma: no cover
            status = "FEHLER %s" % exc
        if status.startswith("FEHLER"):
            rc = 1
        print("%-12s %s" % (status, path))
    return rc


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
