#!/usr/bin/env python3
"""Injiziert FB-WORTBANK-SHUFFLE (CSS + JS) — mischt eine vorhandene statische Wortbox
(Grundform-Anzeige) bei jedem Laden. Idempotent (Marker FB-WORTBANK-SHUFFLE)."""
import sys, os

HERE = os.path.dirname(os.path.abspath(__file__))
MODULE_JS = open(os.path.join(HERE, "wortbank-shuffle-module.js"), encoding="utf-8").read()

CSS = """
/* FB-WORTBANK-SHUFFLE — gemischte Grundform-Wortbank */
.fb-wb-label{font-weight:700;color:#667eea;font-size:0.85em;margin:0 0 8px;}
.fb-wb-chips{display:flex;flex-wrap:wrap;gap:8px;}
.fb-wb-chip{background:#fff;border:2px solid #667eea;color:#667eea;padding:5px 12px;border-radius:14px;font-weight:500;font-size:0.9em;user-select:none;}
"""

SCRIPT_BLOCK = "\n<script>\n" + MODULE_JS + "\n</script>\n"

def inject(path):
    s = open(path, encoding="utf-8", errors="replace").read()
    if "FB-WORTBANK-SHUFFLE" in s:
        return "skip-exists"
    idx = s.find("</style>")
    if idx != -1:
        s = s[:idx] + CSS + s[idx:]
    else:
        h = s.find("</head>")
        block = "<style>" + CSS + "</style>\n"
        s = (s[:h] + block + s[h:]) if h != -1 else block + s
    pos = s.rfind("</body>")
    if pos == -1:
        pos = s.rfind("</html>")
    s = (s[:pos] + SCRIPT_BLOCK + s[pos:]) if pos != -1 else s + SCRIPT_BLOCK
    open(path, "w", encoding="utf-8").write(s)
    return "injected"

if __name__ == "__main__":
    for p in sys.argv[1:]:
        print(inject(p), p)
