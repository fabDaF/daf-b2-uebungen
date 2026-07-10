#!/usr/bin/env python3
"""check_nested_sections.py — Sicherheitsnetz gegen ineinander verschachtelte Tabs.

Fehlerklasse (Frank-Fund 2026-07-10, 15 Dateien über A1/A2/B1/B2):
Ein FEHLENDES </div> (oft ein doppeltes Öffnungs-<div>, z. B. control-bar)
schließt eine Tab-Section nicht — die folgenden Sections rutschen als Kinder
IN diese Section hinein. Sie bleiben im .container (deshalb schlägt
check_container.py NICHT an), aber beim Tab-Klick wird die umschließende
Section per display:none versteckt und nimmt alle verschachtelten Tabs mit:
„nach Tab X öffnet kein Tab mehr". JS-Parse und Render-Tests bleiben grün,
weil die Sections im DOM existieren — nur ihre Sichtbarkeit stirbt.

Abgrenzung: check_container.py fängt das GEGENTEIL (überzähliges </div>,
Sections fallen AUS dem Container). Dieses Gate fängt zu WENIGE </div>
(Sections verschachteln sich ineinander).

Erkennung: Tag-Strom von <div>/<section> mit Stack. Öffnet sich eine
Section (class enthält "section"), während bereits eine Section im Stack
offen ist, ist sie verschachtelt.

Nutzung:
    python3 scripts/check_nested_sections.py            # ganzes Repo (ohne daf-archiv)
    python3 scripts/check_nested_sections.py datei.html # einzelne Dateien

Exit 1 bei Treffern — läuft als blockierendes Gate in check_all.py.
"""
import os
import re
import sys

TAG_RE = re.compile(r'<(/?)(?:div|section)\b([^>]*)>', re.I)
CLASS_RE = re.compile(r'class\s*=\s*"([^"]*)"', re.I)
ID_RE = re.compile(r'id\s*=\s*"([^"]*)"', re.I)


def is_section(attrs):
    m = CLASS_RE.search(attrs)
    if not m:
        return False
    return "section" in m.group(1).split()


def nested_sections(path):
    try:
        s = open(path, encoding="utf-8", errors="replace").read()
    except OSError:
        return None
    stack = []  # bool je offenem div/section: ist es eine .section?
    bad = []
    for m in TAG_RE.finditer(s):
        closing = m.group(1) == "/"
        attrs = m.group(2)
        if not closing:
            sec = is_section(attrs)
            if sec and any(stack):  # ein Vorfahr ist bereits .section
                idm = ID_RE.search(attrs)
                bad.append(idm.group(1) if idm else "(ohne id)")
            stack.append(sec)
        else:
            if stack:
                stack.pop()
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
    files = sys.argv[1:] or collect_repo()
    bad = []
    for p in files:
        nested = nested_sections(p)
        if nested:
            bad.append((p, nested))
    if bad:
        print(f"✗ {len(bad)} Datei(en) mit ineinander verschachtelten Tab-Sections "
              f"(Tabs dahinter öffnen nicht):")
        for p, ids in bad:
            print(f"    {p}  (verschachtelt: {', '.join(ids)})")
        print("\nFix: fehlendes </div> an der Verschachtelungsgrenze ergänzen "
              "(oft doppeltes Öffnungs-<div>, z. B. control-bar). Danach müssen "
              "alle .section direkte Kinder von .container sein.")
        sys.exit(1)
    print(f"✓ Keine verschachtelten Tab-Sections ({len(files)} Dateien geprüft).")
    sys.exit(0)
