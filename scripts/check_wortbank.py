#!/usr/bin/env python3
"""check_wortbank.py — Sicherheitsnetz gegen Lückentext-Lektionen OHNE Wort-Hilfe.

Hintergrund: Ein Lückentext ohne sichtbare Wortbank ist im Unterricht unlösbar
(der Lerner weiß nicht, welche Wörter gefragt sind). daf-kern §7 macht die Wortbank
deshalb zur Pflicht. Dieses Skript findet alle HTML-Dateien mit einem Lückentext-Tab,
denen JEDE Form von Wort-Hilfe fehlt — weder die universelle FB-Wortbank-Komponente
(scripts/wortbank-module.js), noch eine §7-Wortbank, noch ein alter Wortkasten.

Nutzung:
    python3 scripts/check_wortbank.py            # gesamtes Repo (ohne daf-archiv)
    python3 scripts/check_wortbank.py datei.html # einzelne Dateien

Exit-Code 1, wenn Verstöße gefunden werden — geeignet als Pre-Commit-/CI-Gate.
"""
import os, re, sys

TAB_RE = re.compile(r'nav-label[^>]*>\s*Lückentext|<h2[^>]*>[^<]*Lückentext')
# Irgendeine Wort-Hilfe vorhanden?
HELP_RE = re.compile(
    r'FB-WORTBANK-MODULE'                     # universelle Komponente
    r'|class="[^"]*(?:wortbank|wortkasten|wort-kasten|wordbank|wordbox|wortliste)[^"]*"'
    r'|id="[^"]*(?:wortbank|wortkasten|wordbank|wortliste)[^"]*"'
    r"|\.join\(\s*['\"] · "                    # alter Wortkasten via join
    r'|wk\.textContent', re.I)


def scan(paths):
    bad = []
    for p in paths:
        try:
            s = open(p, encoding="utf-8", errors="replace").read()
        except Exception:
            continue
        if not TAB_RE.search(s):
            continue
        if not HELP_RE.search(s):
            bad.append(p)
    return bad


def collect_repo():
    out = []
    for dp, dn, fn in os.walk("."):
        if "/daf-archiv" in dp or "/.git" in dp:
            continue
        for f in fn:
            if f.endswith(".html") and ".bak" not in f:
                out.append(os.path.join(dp, f))
    return out


if __name__ == "__main__":
    args = sys.argv[1:]
    files = args if args else collect_repo()
    bad = scan(files)
    if bad:
        print(f"✗ {len(bad)} Lückentext-Datei(en) OHNE Wort-Hilfe (daf-kern §7 verletzt):")
        for p in bad:
            print("   ", p)
        print("\nFix: scripts/wortbank-module.js injizieren oder §7-Wortbank ergänzen.")
        sys.exit(1)
    print(f"✓ Alle {len(files)} geprüften Dateien haben eine Wort-Hilfe (oder keinen Lückentext-Tab).")
    sys.exit(0)
