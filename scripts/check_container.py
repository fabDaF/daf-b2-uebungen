#!/usr/bin/env python3
"""check_container.py — Sicherheitsnetz gegen vorzeitig schließende Container.

Fehlerklasse (Frank-Fund 2026-07-04 an A2 2034R, insgesamt 4 Dateien):
Ein überzähliges </div> am Ende eines umgebauten Tabs schließt den weißen
.container vorzeitig — alle folgenden Sections (Satzbau, Genus, Wortschatz,
Schreiben) fallen aus dem Container und liegen nackt auf dem lila
Seiten-Hintergrund. JS-Parse, Lückentext-Gate und Render-Tests des einzelnen
Tabs bleiben dabei grün — nur die Optik der NACHFOLGENDEN Tabs stirbt.
Quelle waren LT-Story-Umbauten vom 2026-07-02.

Erkennung: zeilenweiser <div>-Tiefen-Trace ab class="container". Erreicht die
Tiefe 0 VOR der letzten class="section"-Zeile, ist der Container zu früh zu.

Nutzung:
    python3 scripts/check_container.py            # ganzes Repo (ohne daf-archiv)
    python3 scripts/check_container.py datei.html # einzelne Dateien

Exit 1 bei Treffern — läuft als blockierendes Gate in check_all.py.
"""
import os
import re
import sys

DIV_RE = re.compile(r'<div\b')


def premature_close(path):
    try:
        s = open(path, encoding="utf-8", errors="replace").read()
    except OSError:
        return None
    if 'class="container"' not in s:
        return None
    lines = s.split("\n")
    depth = 0
    incont = False
    closed_at = None
    last_section = 0
    for idx, l in enumerate(lines):
        if 'class="container"' in l and not incont:
            incont = True
        if re.search(r'class="section[ "]', l):
            last_section = idx
        if not incont:
            continue
        depth += len(DIV_RE.findall(l)) - l.count("</div>")
        if depth == 0 and closed_at is None:
            closed_at = idx
    if closed_at is not None and closed_at < last_section:
        return closed_at + 1
    return None


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
        line = premature_close(p)
        if line:
            bad.append((p, line))
    if bad:
        print(f"✗ {len(bad)} Datei(en) mit vorzeitig schließendem .container "
              f"(Tabs dahinter fallen aus dem weißen Kasten):")
        for p, line in bad:
            print(f"    {p}  (Container schließt in Zeile {line})")
        print("\nFix: überzähliges </div> an der gemeldeten Stelle entfernen; danach "
              "JSDOM-Check: alle .section im .container.")
        sys.exit(1)
    print(f"✓ Container-Struktur intakt ({len(files)} Dateien geprüft).")
    sys.exit(0)
