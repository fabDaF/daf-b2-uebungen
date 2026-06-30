#!/usr/bin/env python3
"""inject_lt.py — spielt die KANONISCHE FB-LT-STORY-Engine + CSS in eine Lektion ein.

Eine Quelle der Wahrheit:
  - scripts/lt-story.css        (CSS)
  - scripts/lt-story-engine.js  (JS-Engine, variantenerkennend V/R/X + G)

Was der Produzent macht (idempotent, je eigener Marker):
  1. CSS vor das letzte </style>            (Marker FB-LT-STORY-CSS),
  2. Engine vor </body>                      (Marker FB-LT-STORY-ENGINE),
  3. Timer-Hooks vor </body>                 (Marker FB-LT-STORY-HOOKS),
     verdrahtet auf den Lückentext-Tab-Index (aus showSection/showTab des
     Lückentext-Nav-Buttons; erkennt <div> UND <button>, mehrzeilig).

Die drei Marker sind unabhängig: ein erneuter Lauf trägt fehlende Teile nach
(z. B. Timer-Hooks, falls der Tab-Index beim ersten Lauf nicht erkannt wurde).

Was der Produzent BEWUSST NICHT macht: den Story-INHALT erzeugen oder alte
Inhalte herausreißen. Die Story ist Autorenarbeit (Markup-Vertrag siehe
lt-story-engine.js). Die Engine bleibt untätig, solange kein
<div id="lueckenContainer" class="luecken-story"> mit <input class="blank"
data-answer="…"> da ist — Einspielen ist also gefahrlos.

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
HOOK_MARK = "FB-LT-STORY-HOOKS"

# Nav-Button (div ODER button, mehrzeilig) mit showSection/showTab(N), dessen
# Beschriftung „Lückentext" enthält (auch entity-kodiert).
NAV_RE = re.compile(
    r'<(?:div|button)\s+class="nav-btn[^"]*"[^>]*onclick="show(?:Section|Tab)\((\d+)\)"[^>]*>(.*?)</(?:div|button)>',
    re.S)


def luecken_tab_index(s):
    for m in NAV_RE.finditer(s):
        if re.search(r'L(?:ü|&uuml;)ckentext', m.group(2)):
            return m.group(1)
    return None


def _insert_before_end(s, block):
    p = s.rfind("</body>")
    if p == -1:
        p = s.rfind("</html>")
    if p == -1:
        return None
    return s[:p] + block + s[p:]


def inject(path):
    s = open(path, encoding="utf-8", errors="replace").read()
    orig = s
    actions = []

    # 0) Konkurrierende graue Alt-Engine entfernen (genau EINE Engine pro Datei).
    # Das FB-WORTBANK-MODULE ist ein selbst-enthaltener <script>-Block; bounded
    # entfernen (Marker steht nur im Script, nicht in einer CSS). Das Gate verbietet
    # konkurrierende Engines — ohne Entfernung bliebe die Datei rot.
    while "FB-WORTBANK-MODULE" in s:
        idx = s.find("FB-WORTBANK-MODULE")
        start = s.rfind("<script", 0, idx)
        end = s.find("</script>", idx)
        if start < 0 or end < 0:
            break
        end += len("</script>")
        if not (200 < end - start < 20000):
            break  # unplausibel -> Finger weg, lieber manuell
        s = s[:start] + s[end:]
        if "Alt-Engine entfernt" not in actions:
            actions.append("Alt-Engine entfernt")

    # 1) CSS
    if CSS_MARK not in s:
        i = s.rfind("</style>")
        if i == -1:
            return "SKIP (kein </style>): " + path
        s = s[:i] + "\n/* " + CSS_MARK + " */\n" + CSS + "\n" + s[i:]
        actions.append("CSS")

    # 2) Engine
    if ENGINE_MARK not in s:
        block = "\n<!-- " + ENGINE_MARK + " -->\n<script>\n" + ENGINE + "\n</script>\n"
        ns = _insert_before_end(s, block)
        if ns is None:
            return "SKIP (kein </body>): " + path
        s = ns
        actions.append("Engine")

    # 3) Timer-Hooks (unabhängig — werden nachgetragen, sobald der Index erkannt wird)
    if HOOK_MARK not in s:
        n = luecken_tab_index(s)
        if n is not None:
            block = ("\n<!-- " + HOOK_MARK + " --><script>"
                     "window.fbLtTimerStart=function(){if(typeof timerAutoStart==='function')timerAutoStart(%s);};"
                     "window.fbLtTimerStop=function(){if(typeof timerStop==='function')timerStop(%s);};"
                     "</script>\n" % (n, n))
            ns = _insert_before_end(s, block)
            if ns is not None:
                s = ns
                actions.append("Hooks(N=%s)" % n)
        else:
            actions.append("Hooks(N=?-nicht erkannt)")

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
