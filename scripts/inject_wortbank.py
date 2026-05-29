#!/usr/bin/env python3
"""Injiziert das universelle FB-Wortbank-Modul (CSS + JS) in eine DaF-HTML-Datei.
Idempotent (Marker FB-WORTBANK-MODULE). Rührt vorhandene Logik nicht an."""
import sys, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
MODULE_JS = open(os.path.join(HERE, "wortbank-module.js"), encoding="utf-8").read()

CSS = """
/* FB-WORTBANK — universelle Lueckentext-Wortbank */
.fb-wortbank-wrap{margin:14px 0 18px;}
.fb-wortbank-label{font-weight:700;color:#667eea;font-size:0.85em;margin:0 0 8px;}
.fb-wortbank{display:flex;flex-wrap:wrap;gap:8px;padding:14px;background:#f0f0f8;border-radius:10px;min-height:48px;border:1px dashed #bbb;}
.fb-wortbank-chip{background:#fff;border:2px solid #667eea;color:#667eea;padding:5px 12px;border-radius:14px;font-weight:500;font-size:0.9em;user-select:none;}
.fb-wortbank-chip.used{opacity:0.35;text-decoration:line-through;}
"""

SCRIPT_BLOCK = "\n<script>\n" + MODULE_JS + "\n</script>\n"

def inject(path):
    s = open(path, encoding="utf-8", errors="replace").read()
    if "FB-WORTBANK-MODULE" in s:
        return "skip-exists"
    orig = s

    # 1) CSS vor das erste </style>
    idx = s.find("</style>")
    if idx != -1:
        s = s[:idx] + CSS + s[idx:]
    else:
        # kein <style> -> in <head> einsetzen, sonst vor erstes <script>
        h = s.find("</head>")
        block = "<style>" + CSS + "</style>\n"
        if h != -1:
            s = s[:h] + block + s[h:]
        else:
            s = block + s

    # 2) Modul-Script vor letztem </body> (sonst </html>, sonst ans Ende)
    pos = s.rfind("</body>")
    if pos == -1:
        pos = s.rfind("</html>")
    if pos == -1:
        s = s + SCRIPT_BLOCK
    else:
        s = s[:pos] + SCRIPT_BLOCK + s[pos:]

    if s == orig:
        return "no-change"
    open(path, "w", encoding="utf-8").write(s)
    return "injected"

if __name__ == "__main__":
    for p in sys.argv[1:]:
        print(inject(p), p)
