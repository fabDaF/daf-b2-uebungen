#!/usr/bin/env python3
"""check_wortbank.py — Sicherheitsnetz gegen Lückentext-Lektionen OHNE Wort-Hilfe.

Hintergrund: Ein Lückentext ohne sichtbare Wortbank ist im Unterricht unlösbar
(der Lerner weiß nicht, welche Wörter gefragt sind). daf-kern §7 macht die Wortbank
deshalb zur Pflicht. Dieses Skript findet alle HTML-Dateien mit einem Lückentext-Tab,
denen JEDE Form von Wort-Hilfe fehlt — weder die universelle FB-Wortbank-Komponente
(scripts/wortbank-module.js), noch eine §7-Wortbank, noch ein alter Wortkasten.

Zwei Fehlerklassen werden gemeldet:
  (A) FEHLT      — gar keine Wort-Hilfe im Markup.
  (B) NIE BEFÜLLT — eine eigene Wortbank (#wortbank-luecken / .wortbank) ist zwar
                     da, aber `initWortbank()` wird definiert und NIE aufgerufen,
                     d.h. die Box bleibt zur Laufzeit leer. Genau dieser Bug ist
                     2026-06-01 in DE_B2_1033R aufgefallen — statische
                     Markup-Prüfung allein erkennt ihn nicht.

Ausgenommen sind Buchstaben-/Fragment-Gitter (letter-input): dort ergänzt der
Lerner einzelne fehlende Buchstaben mit sichtbarem Wortkontext — eine Wortbank aus
Fragmenten wäre sinnlos. Reine Diktate ohne Wort-Lücken brauchen ebenfalls keine.

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

# Buchstaben-/Fragment-Gitter — kein Wort-Lückentext, daher von der Pflicht ausgenommen.
LETTER_RE = re.compile(r'class="letter-input"|\bletter-group\b')

# Eigener Wortbank-Container im Markup (skill-konforme §7-Wortbank).
CONTAINER_RE = re.compile(r'id="wortbank-luecken"|class="[^"]*wortbank[^"]*"', re.I)


def initwortbank_defined_but_unused(s):
    """True, wenn initWortbank() definiert, aber nirgends referenziert/aufgerufen wird.
    Das universelle Modul (FB-WORTBANK-MODULE) befüllt eigenständig — dann irrelevant."""
    if "FB-WORTBANK-MODULE" in s:
        return False
    defs = len(re.findall(r"function\s+initWortbank\b", s))
    if defs == 0:
        return False
    total = len(re.findall(r"\binitWortbank\b", s))
    # total zählt Definition(en) + jede Referenz. Bleibt nach Abzug der
    # Definitionszeilen nichts übrig, wird die Funktion nie aufgerufen.
    return (total - defs) <= 0


def scan(paths):
    missing = []   # (A) gar keine Hilfe
    empty = []     # (B) Container da, aber nie befüllt
    for p in paths:
        try:
            s = open(p, encoding="utf-8", errors="replace").read()
        except Exception:
            continue
        if not TAB_RE.search(s):
            continue
        # Buchstaben-/Fragment-Gitter: ausgenommen.
        if LETTER_RE.search(s):
            continue
        if not HELP_RE.search(s):
            missing.append(p)
            continue
        # Hilfe im Markup vorhanden — aber bleibt sie zur Laufzeit leer?
        if CONTAINER_RE.search(s) and initwortbank_defined_but_unused(s):
            empty.append(p)
    return missing, empty


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
    missing, empty = scan(files)
    if missing or empty:
        if missing:
            print(f"✗ {len(missing)} Lückentext-Datei(en) OHNE Wort-Hilfe (daf-kern §7 verletzt):")
            for p in missing:
                print("   ", p)
        if empty:
            print(f"✗ {len(empty)} Datei(en) mit Wortbank-Container, der NIE befüllt wird "
                  f"(initWortbank definiert, aber nicht aufgerufen):")
            for p in empty:
                print("   ", p)
        print("\nFix: scripts/wortbank-module.js injizieren, §7-Wortbank ergänzen, "
              "oder initWortbank() in der Init-Sequenz aufrufen.")
        sys.exit(1)
    print(f"✓ Alle {len(files)} geprüften Dateien haben eine befüllte Wort-Hilfe "
          f"(oder keinen Wort-Lückentext-Tab).")
    sys.exit(0)
