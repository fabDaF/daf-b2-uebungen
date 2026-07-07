#!/usr/bin/env python3
"""check_all.py — Orchestrator für alle Lektions-Gates.

Bisher mussten die check_*-Skripte einzeln und aus dem Gedächtnis aufgerufen
werden („vor jedem Lektions-Commit laufen lassen"). Dieses Skript bündelt sie:

    python3 scripts/check_all.py datei1.html [datei2.html …]   # Per-Datei (schnell)
    python3 scripts/check_all.py                               # ganzes Repo

Zwei Kategorien:
  BLOCKING — Showstopper-Regeln, die für JEDE Datei gelten (Quotes, Serif,
             Wortbank, Genus-Mindestanzahl, Schreib-Padding, Pill-Buttons,
             fehlerhafte kanonische Lückentexte, Banner-Gesichter).
             Ein Fehler hier ⇒ Exit 1 (Commit stoppen).
  WARN     — Rollout-Zustände mit bekanntem Backlog (Nav Variante C,
             Schreiben-letzter-Tab, Wortschatz-Kanon). Werden gemeldet,
             blockieren aber nicht — sonst wäre jeder Commit an einer
             Backlog-Datei unmöglich.

safe-commit.sh ruft dieses Skript automatisch über die benannten HTML-Dateien
auf (SKIP_CHECKS=1 zum Überspringen).
"""
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))

BLOCKING = [
    "check_quotes.py",
    "check_serif.py",
    "check_wortbank.py",
    "check_genus.py",
    "check_schreib_pad.py",
    "check_genus_buttons.py",
    "check_lueckentext.py --strict-buttons",  # seit 2026-07-05 blockierend inkl. Buttons (C1 nachgezogen)
    "check_banner_faces.py",  # überspringt sich selbst ohne opencv (Exit 0)
    "check_container.py",     # vorzeitig schließender .container (Fund 2026-07-04)
    "check_hilfebox.py",      # verbotene Aufgaben-/Tipp-Kästen (Frank-Regel, 2026-07-04)
]

WARN = [
    "check_nav.py",
    "check_schreib_last.py",
    "check_wortschatz.py",
    "check_dark.py",  # Dark-Mode-Backlog (~220 Dateien ohne FB-DESIGN-TOKENS), seit 2026-07-07
]

def run(script, files):
    teile = script.split()
    cmd = [sys.executable, os.path.join(HERE, teile[0])] + teile[1:] + files
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
    except Exception as e:  # Skript fehlt/kaputt: melden, nicht heimlich schlucken
        return 2, f"[{script}] nicht ausführbar: {e}"
    out = (r.stdout + r.stderr).strip()
    return r.returncode, out


def main():
    files = [f for f in sys.argv[1:] if f.endswith(".html")]
    label = f"{len(files)} Datei(en)" if files else "ganzes Repo"
    print(f"─── check_all: {label} ───")

    failed = []
    for script in BLOCKING:
        code, out = run(script, files)
        if code == 0:
            print(f"  ✓ {script}")
        else:
            failed.append(script)
            print(f"  ✗ {script}")
            for line in out.splitlines():
                print(f"      {line}")

    for script in WARN:
        code, out = run(script, files)
        if code == 0:
            print(f"  ✓ {script}")
        else:
            print(f"  ⚠ {script} (Backlog-Gate, blockiert nicht)")
            # Nur die Kopfzeilen zeigen, nicht die komplette Datei-Liste.
            for line in out.splitlines()[:6]:
                print(f"      {line}")

    if failed:
        print(f"\n✗ {len(failed)} blockierende(s) Gate(s) rot: {', '.join(failed)}")
        sys.exit(1)
    print("\n✓ Alle blockierenden Gates grün.")
    sys.exit(0)


if __name__ == "__main__":
    main()
