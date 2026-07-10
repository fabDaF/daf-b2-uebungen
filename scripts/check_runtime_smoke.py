#!/usr/bin/env python3
"""check_runtime_smoke.py — Laufzeit-Smoke-Gate (node + jsdom, optional).

Führt scripts/smoke_test.js aus: lädt jede Lektion in jsdom und meldet
Lade-Zeit-Laufzeitfehler (ReferenceError/TypeError), die die Init-Kette
abbrechen — die Klasse, die node --check NICHT sieht.

Dieses Gate ist eine ERGÄNZUNG zu den rein statischen Gates
check_nested_sections.py (Verschachtelung) und check_orphan_init.py
(verwaiste Init-Aufrufe). Es fängt zusätzlich die TypeError-Klasse
(z. B. getElementById(...).innerHTML auf fehlendem Container).

Optionale Abhängigkeit — wie check_banner_faces.py mit opencv:
Fehlt node oder das Modul jsdom, ÜBERSPRINGT das Gate mit Hinweis und
Exit 0 (blockiert also nie). Aktivieren mit:  npm install jsdom
(im Repo-Root oder global, dann NODE_PATH setzen).

Nutzung:
    python3 scripts/check_runtime_smoke.py            # ganzes Repo (ohne daf-archiv)
    python3 scripts/check_runtime_smoke.py datei.html # einzelne Dateien
"""
import os
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SMOKE = os.path.join(HERE, "smoke_test.js")


def collect_repo():
    out = []
    for dp, dn, fn in os.walk("."):
        if "/daf-archiv" in dp or "/.git" in dp:
            continue
        for f in fn:
            if f.endswith(".html") and ".bak" not in f:
                out.append(os.path.join(dp, f))
    return out


def node_bin():
    for c in ("node", "nodejs"):
        p = shutil.which(c)
        if p:
            return p
    return None


def jsdom_available(node):
    try:
        r = subprocess.run([node, "-e", "require.resolve('jsdom')"],
                           capture_output=True, text=True, timeout=30)
        return r.returncode == 0
    except Exception:
        return False


def main():
    files = [f for f in sys.argv[1:] if f.endswith(".html")] or collect_repo()
    node = node_bin()
    if not node:
        print("⚠ übersprungen: node nicht gefunden (Laufzeit-Smoke inaktiv).")
        sys.exit(0)
    if not jsdom_available(node):
        print("⚠ übersprungen: Modul jsdom nicht installiert "
              "(aktivieren mit: npm install jsdom).")
        sys.exit(0)
    try:
        r = subprocess.run([node, SMOKE] + files, capture_output=True, text=True, timeout=1200)
    except Exception as e:
        print(f"⚠ übersprungen: smoke_test.js nicht ausführbar: {e}")
        sys.exit(0)
    out = (r.stdout + r.stderr).strip()
    print(out)
    sys.exit(r.returncode)


if __name__ == "__main__":
    main()
