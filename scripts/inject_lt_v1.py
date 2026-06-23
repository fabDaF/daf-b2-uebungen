#!/usr/bin/env python3
"""inject_lt_v1.py — installiert FB-LT-V1 (kanonischer Vokabel-Lückentext, Spec v1.0).
NUR für V/R/X-Dateien. Idempotent (Marker FB-LT-V1). CSS + Modul-Script."""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
MODULE_JS = open(os.path.join(HERE, "lt-v1-module.js"), encoding="utf-8").read()

CSS = """
/* FB-LT-V1 — Wortbank + Feedback (LUECKENTEXT-SKILL-SPEC v1.0) */
.wortbank{display:flex;flex-wrap:wrap;gap:8px;padding:14px;background:#f0f0f8;border-radius:10px;min-height:48px;margin:8px 0 18px;border:1px dashed #bbb;}
.wortbank-chip{background:#fff;border:2px solid #667eea;color:#667eea;padding:5px 12px;border-radius:14px;font-weight:500;font-size:0.9em;user-select:none;}
.wortbank-chip.used{opacity:0.35;text-decoration:line-through;}
input.correct{border-bottom:2px solid #27ae60 !important;background:#e8f8f0 !important;color:#27ae60 !important;font-weight:700;}
input.wrong{border-bottom:2px solid #e74c3c !important;background:#fdeaea !important;color:#e74c3c !important;}
"""
SCRIPT = "\n<script>\n" + MODULE_JS + "\n</script>\n"

def inject(path):
    s = open(path, encoding="utf-8", errors="replace").read()
    if "FB-LT-V1" in s:
        return "skip-exists"
    i = s.find("</style>")
    if i != -1:
        s = s[:i] + CSS + s[i:]
    else:
        h = s.find("</head>")
        block = "<style>" + CSS + "</style>\n"
        s = (s[:h] + block + s[h:]) if h != -1 else block + s
    p = s.rfind("</body>")
    if p == -1:
        p = s.rfind("</html>")
    s = (s[:p] + SCRIPT + s[p:]) if p != -1 else s + SCRIPT
    open(path, "w", encoding="utf-8").write(s)
    return "injected"

if __name__ == "__main__":
    for p in sys.argv[1:]:
        print(inject(p), p)
