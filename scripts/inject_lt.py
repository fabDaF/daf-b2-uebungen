#!/usr/bin/env python3
"""inject_lt.py — spielt die KANONISCHE FB-LT-STORY-Engine + CSS in eine Lektion ein.

Eine Quelle der Wahrheit:
  - scripts/lt-story.css        (CSS)
  - scripts/lt-story-engine.js  (JS-Engine, variantenerkennend V/R/X + G)

Was der Produzent macht (idempotent, marker-geschützt):
  1. CSS vor das letzte </style> (Marker FB-LT-STORY-CSS),
  2. Engine + Timer-Hooks vor </body> (Marker FB-LT-STORY-ENGINE);
     die Timer-Hooks werden auf den Lückentext-Tab-Index verdrahtet (aus dem
     showSection/showTab des Lückentext-Nav-Buttons).

Was der Produzent BEWUSST NICHT macht: den Story-INHALT erzeugen oder alte
Inhalte herausreißen. Die Story ist Autorenarbeit; sie wird pro Lektion von Hand
geschrieben (Markup-Vertrag siehe lt-story-engine.js). Die Engine bleibt untätig,
solange kein <div id="lueckenContainer" class="luecken-story"> mit <input
class="blank" data-answer="…"> da ist — Einspielen ist also gefahrlos.

Aufruf:
    python3 scripts/inject_lt.py DATEI.html [DATEI2.html …]
"""
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
CSS = open(os.path.join(HERE, "lt-story.css"), encoding="utf-8").read()
ENGINE = open(os.path.join(HERE, "lt-story-engine.js"), encoding="utf-8").read()

CSS_MARK = "FB-LT-STORY-CSS"
ENGINE_MARK = "FB-LT-STORY-ENGINE"


def luecken_tab_index(s):
    """Index N aus dem Lückentext-Nav-Button (onclick=showSection(N)/showTab(N))."""
    for m in re.finditer(r'<div class="nav-btn[^"]*"[^>]*onclick="show(?:Section|Tab)\((\d+)\)"[^>]*>(.*?)</div>', s, re.S):
        if re.search(r'L(?:ü|&uuml;)ckentext', m.group(2)):
            return m.group(1)
    return None


def inject(path):
    s = open(path, encoding="utf-8", errors="replace").read()
    orig = s
    actions = []

    # 1) CSS
    if CSS_MARK not in s:
        i = s.rfind("</style>")
        if i == -1:
            return "SKIP (kein </style>): " + path
        s = s[:i] + "\n/* " + CSS_MARK + " */\n" + CSS + "\n" + s[i:]
        actions.append("CSS")

    # 2) Engine + Timer-Hooks
    if ENGINE_MARK not in s:
        n = luecken_tab_index(s)
        hooks = ""
        if n is not None:
            hooks = ("<script>"
                     "window.fbLtTimerStart=function(){if(typeof timerAutoStart==='function')timerAutoStart(%s);};"
                     "window.fbLtTimerStop=function(){if(typeof timerStop==='function')timerStop(%s);};"
                     "</script>\n" % (n, n))
        block = "\n<!-- " + ENGINE_MARK + " -->\n" + hooks + "<script>\n" + ENGINE + "\n</script>\n"
        p = s.rfind("</body>")
        if p == -1:
            p = s.rfind("</html>")
        if p == -1:
            return "SKIP (kein </body>): " + path
        s = s[:p] + block + s[p:]
        actions.append("Engine(N=%s)" % n)

    if s != orig:
        open(path, "w", encoding="utf-8").write(s)
        return "OK [" + "+".join(actions) + "]: " + path
    return "schon kanonisch (skip): " + path


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Aufruf: inject_lt.py DATEI.html …")
        sys.exit(1)
    for p in sys.argv[1:]:
        print(inject(p))
