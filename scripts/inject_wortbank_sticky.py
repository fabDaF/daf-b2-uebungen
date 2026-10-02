#!/usr/bin/env python3
"""inject_wortbank_sticky.py — Wortbank bleibt beim Scrollen oben sichtbar (Frank 2026-10-02).

Der Lückentext-Text läuft unter der Wortbank durch. Zwei Teile (Marker FB-WORTBANK-STICKY):
  1. .wortbank { position: sticky; top: 0 } (+ Mobil-Verdichtung),
  2. .container { overflow: clip } — overflow:hidden am Container bricht position:sticky;
     clip behält die runden Ecken, erzeugt aber keinen Scroll-Container.
Der Block wird ans ENDE des letzten <style>, das eine .wortbank-Regel enthält, angehängt
(später = gewinnt gegen jede ältere .container-/.wortbank-Regel, ohne sie zu editieren).
Idempotent. Nutzung: inject_wortbank_sticky.py [--dry] DATEI.html ...
Kanonische Quelle für neue Lektionen: der Block steht auch in lt-story.css (inject_lt.py).
"""
import re, sys

MARK = "FB-WORTBANK-STICKY"
BLOCK = (
    "/* " + MARK + " — Wortbank bleibt beim Scrollen oben sichtbar, Story läuft darunter durch.\n"
    "   Voraussetzung: .container nutzt overflow:clip statt hidden (hidden bricht position:sticky). */\n"
    ".container { overflow: hidden; overflow: clip; }\n"
    ".wortbank { position: sticky; top: 0; z-index: 20; box-shadow: 0 4px 12px rgba(0,0,0,0.08); }\n"
    "@media (max-width: 600px) { .wortbank { padding: 8px; gap: 6px; } .wortbank-chip { padding: 3px 9px; font-size: 0.85em; } }\n"
)
STYLE_RE = re.compile(r"(<style[^>]*>)(.*?)(</style>)", re.S)
RULE_RE = re.compile(r"\.wortbank\s*\{")
# Es muss auch wirklich ein kanonisches .wortbank-Element existieren (HTML oder per JS erzeugt).
# Die Modul-Variante (.fb-wortbank-wrap, eine Riesen-Wortbank für die ganze Seite, z.B. Mattmüller)
# bleibt bewusst ausgenommen — dort wäre eine klebende Wortbank mehrere hundert Pixel hoch.
NEEDS_RE = re.compile(r"""(?:id|class)="wortbank|className\s*=\s*['"]wortbank['"]""")

def patch(s):
    if MARK in s:
        return None, "schon vorhanden"
    if not NEEDS_RE.search(s):
        return None, "kein kanonisches .wortbank-Element (Modul-Variante?)"
    last = None
    for m in STYLE_RE.finditer(s):
        if RULE_RE.search(m.group(2)):
            last = m
    if not last:
        return None, "keine .wortbank-Regel in <style>"
    i = last.start(3)
    return s[:i] + "\n" + BLOCK + s[i:], "ok"

def main(argv):
    dry = "--dry" in argv
    files = [a for a in argv if not a.startswith("--")]
    n_ok = n_skip = 0
    for p in files:
        try:
            s = open(p, encoding="utf-8", newline="").read()
        except Exception as e:
            print("FEHLER", p, e); continue
        new, why = patch(s)
        if new is None:
            n_skip += 1
            if why != "schon vorhanden":
                print("SKIP", p, "-", why)
            continue
        if not dry:
            open(p, "w", encoding="utf-8", newline="").write(new)
        n_ok += 1
    print(("DRY " if dry else "") + "gepatcht: %d, übersprungen: %d" % (n_ok, n_skip))

if __name__ == "__main__":
    main(sys.argv[1:])
