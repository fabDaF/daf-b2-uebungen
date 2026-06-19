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
    # Tab-Umschaltung heißt showSection ODER showTab (gleiche Index-Mechanik)
    return [int(m.group(1)) for m in re.finditer(r'onclick="(?:showSection|showTab)\((\d+)\)"', t)]

def section_count(t):
    # echte .section: Klassen-Token exakt "section" (nicht "schreib-section" o.ä.)
    return len(re.findall(r'class="(?:[^"]*\s)?section(?:\s[^"]*)?"', t))

def is_id_based(t):
    # showSection nutzt getElementById('sec-' + n) -> ID-basiert (n = ID-Suffix UND Nav-Index)
    return bool(re.search(r"getElementById\(\s*['\"]sec-['\"]\s*\+", t))

def section_ids(t):
    return set(re.findall(r'id="(sec-[0-9A-Za-z]+)"', t))

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
        n = len(tg)
        cnt_ok = n == secs
        info = ""
        if is_id_based(t):
            # ID-basiert: jedes onclick-Ziel N braucht eine Section id="sec-N",
            # und N muss ein gültiger Nav-Index sein (0..n-1) für nav[N].
            ids = section_ids(t)
            map_ok = all(0 <= N < n and ('sec-%d' % N) in ids for N in tg)
            uniq_ok = len(set(tg)) == n
            ok = map_ok and uniq_ok and cnt_ok
            if not map_ok: info += " ID-Mapping defekt onclick=%s ids=%s" % (tg, sorted(ids))
            if not uniq_ok: info += " doppelte onclick-Ziele=%s" % tg
        else:
            # Index-basiert: onclick-Ziele in DOM-Reihenfolge == 0..n-1.
            ok = (tg == list(range(n))) and cnt_ok
            if tg != list(range(n)): info += " onclick-Ziele=" + str(tg)
        if not cnt_ok: info += " nav=%d sec=%d" % (n, secs)
        if ok:
            print("OK      ", p.split('/')[-1])
        else:
            bad += 1
            print("BROKEN  ", p.split('/')[-1], info)
    sys.exit(1 if bad else 0)

if __name__ == "__main__":
    main()
