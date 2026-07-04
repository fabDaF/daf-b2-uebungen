#!/usr/bin/env python3
"""check_hilfebox.py — Gate gegen Aufgaben-/Tipp-Kästen (hilfe-box/help-box).

Franks Grundsatzregel (mehrfach eingeschärft, endgültig 2026-07-04): KEINE
Anweisungs-Platzhalter in Übungen — „Jeder sieht, was er machen soll."
Am 2026-07-04 wurden 1572 Kästen in 532 Dateien entfernt; dieses Gate
verhindert, dass Generatoren oder Kopiervorlagen sie wieder einschleppen.

Geprüft wird das ELEMENT (<div class="hilfe-box"…>) — auch innerhalb von
<script>-Strings (runtime-generierte Kästen rendern genauso). Tote
CSS-Regeln (.hilfe-box{…}) sind erlaubt und werden ignoriert.

Nutzung: python3 scripts/check_hilfebox.py [datei.html …]   (ohne Args: Repo)
Exit 1 bei Treffern — blockierendes Gate in check_all.py.
"""
import os
import re
import sys

BOX_RE = re.compile(r'<div class=(?:"|\\")(?:hilfe-box|help-box)')


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
    files = sys.argv[1:] or collect_repo()
    bad = []
    for p in files:
        try:
            s = open(p, encoding="utf-8", errors="replace").read()
        except OSError:
            continue
        n = len(BOX_RE.findall(s))
        if n:
            bad.append((p, n))
    if bad:
        print(f"✗ {len(bad)} Datei(en) mit verbotenen Hilfe-/Aufgaben-Kästen:")
        for p, n in bad:
            print(f"   {n:3}  {p}")
        print("\nFix: Kästen ersatzlos entfernen (Frank-Regel: keine Anweisungs-Platzhalter).")
        sys.exit(1)
    print(f"✓ Keine Hilfe-Kästen ({len(files)} Dateien geprüft).")
    sys.exit(0)
