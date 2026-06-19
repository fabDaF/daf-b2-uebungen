#!/usr/bin/env python3
"""
audit_genus.py — Pflicht-Audit NACH jeder Genus-Tab-Injektion.

Prüft die EINZIG entscheidende Korrektheitsbedingung für Tab-Navigation:
showSection(idx) schaltet die idx-te .section und den idx-ten .nav-btn aktiv.
Damit jeder Klick die richtige Sektion zeigt, MUSS gelten:

  1. Der nav-btn an DOM-Position i trägt onclick="showSection(i)"
     -> die onclick-Ziele in DOM-Reihenfolge sind exakt 0,1,2,…,n-1.
  2. Anzahl echter .nav-btn == Anzahl echter .section.

Hintergrund (2026-06-19): Eine frühe inject_genus-Version renummerierte nur
`class="nav-btn"` und übersah den ersten Button `class="nav-btn active"` —
Ergebnis: onclick-Ziele 0,0,1,2,… → jeder Klick zeigte die falsche Sektion.
Ein JSDOM-Test, der showSection(i) per Schleifenindex (statt über das echte
onclick) aufrief, hat den Bug MASKIERT. Dieser strukturelle Check tut das nicht.

  python3 scripts/audit_genus.py datei.html …      # einzelne Dateien
  python3 scripts/audit_genus.py *.html             # nur Genus-Dateien werden geprüft

Exit 1, sobald eine Datei BROKEN ist.
"""
import re, sys

def nav_targets(t):
    return [int(m.group(1)) for m in re.finditer(r'onclick="showSection\((\d+)\)"', t)]

def section_count(t):
    # echte .section: Klassen-Token exakt "section" (nicht "schreib-section" o.ä.)
    return len(re.findall(r'class="(?:[^"]*\s)?section(?:\s[^"]*)?"', t))

def main():
    bad = 0
    for p in sys.argv[1:]:
        try:
            t = open(p, encoding='utf-8', errors='ignore').read()
        except OSError:
            continue
        if 'sec-genus' not in t and 'GENUS_DATA' not in t:
            continue
        tg = nav_targets(t)
        secs = section_count(t)
        seq_ok = tg == list(range(len(tg)))
        cnt_ok = len(tg) == secs
        if seq_ok and cnt_ok:
            print("OK      ", p.split('/')[-1])
        else:
            bad += 1
            info = ""
            if not seq_ok: info += " onclick-Ziele=" + str(tg)
            if not cnt_ok: info += " nav=%d sec=%d" % (len(tg), secs)
            print("BROKEN  ", p.split('/')[-1], info)
    sys.exit(1 if bad else 0)

if __name__ == "__main__":
    main()
