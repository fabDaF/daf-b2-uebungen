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

# „Lückentext" kommt auch HTML-entity-kodiert vor (ältere Dateien: „L&uuml;ckentext").
# Beide Formen erkennen, sonst rutschen entity-kodierte Dateien komplett durch das Netz.
TAB_RE = re.compile(r'nav-label[^>]*>\s*L(?:ü|&uuml;)ckentext|<h2[^>]*>[^<]*L(?:ü|&uuml;)ckentext')

# Irgendeine Wort-Hilfe vorhanden?
HELP_RE = re.compile(
    r'FB-WORTBANK-MODULE|FB-LT-V1'            # universelle Komponente / FB-LT-V1-Engine
    r'|class="[^"]*(?:wortbank|wortkasten|wort-kasten|wordbank|wordbox|wortliste)[^"]*"'
    r'|id="[^"]*(?:wortbank|wortkasten|wordbank|wortliste)[^"]*"'
    r"|\.join\(\s*['\"] · "                    # alter Wortkasten via join
    r'|wk\.textContent', re.I)

# Buchstaben-/Fragment-Gitter — kein Wort-Lückentext, daher von der Pflicht ausgenommen.
LETTER_RE = re.compile(r'class="letter-input"|\bletter-group\b')

# Eigener Wortbank-Container im Markup (skill-konforme §7-Wortbank).
CONTAINER_RE = re.compile(r'id="wortbank-luecken"|class="[^"]*wortbank[^"]*"', re.I)

# G-Datei am Dateinamen erkennen (z. B. DE_B2_1032G-..., DE_A1_1033G_...).
GFILE_RE = re.compile(r'_\d{4}G[-_.]')


def _func_body(s, name):
    """Funktionskörper {…} per Klammerzählung extrahieren (defensiv begrenzt)."""
    m = re.search(r"function\s+" + re.escape(name) + r"\s*\([^)]*\)\s*\{", s)
    if not m:
        return ""
    i = m.end() - 1  # Position der öffnenden '{'
    depth = 0
    for j in range(i, min(len(s), i + 8000)):
        if s[j] == "{":
            depth += 1
        elif s[j] == "}":
            depth -= 1
            if depth == 0:
                return s[i:j + 1]
    return s[i:i + 8000]


def gfile_wortbank_from_answers(path, s):
    """True bei G-Dateien, deren Lückentext-Wortbank aus den LÖSUNGEN (.answer)
    gebaut wird. Das verrät bei Grammatik-/Transformationsübungen die konjugierte
    Zielform — daf-grammatik verlangt stattdessen einen Infinitiv-Wortkasten
    (G-Datei-Ausnahme zur Wortbank-Pflicht, daf-kern §7). VERDACHT, kein Beweis:
    reine Wort-/Präpositions-Lückentexte sind ggf. unkritisch und vom Menschen
    zu bestätigen."""
    if not GFILE_RE.search(os.path.basename(path)):
        return False
    # Vom Lehrer bestätigte Ausnahme (Wort-Auswahl/Deklination: Vollform zulässig).
    if "WORTBANK-VOLLFORM-OK" in s:
        return False
    return bool(re.search(r"\.answer\b", _func_body(s, "initWortbank")))


def initwortbank_defined_but_unused(s):
    """True, wenn initWortbank() definiert, aber nirgends referenziert/aufgerufen wird.
    Das universelle Modul (FB-WORTBANK-MODULE) befüllt eigenständig — dann irrelevant."""
    if "FB-WORTBANK-MODULE" in s or "FB-LT-V1" in s:
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
    suspect = []   # (C) G-Datei: Wortbank aus Lösungen abgeleitet (Infinitiv-Wortkasten nötig)
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
        # G-Datei: Wortbank verrät evtl. die konjugierte Zielform?
        if gfile_wortbank_from_answers(p, s):
            suspect.append(p)
    return missing, empty, suspect


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
    missing, empty, suspect = scan(files)
    if missing or empty or suspect:
        if missing:
            print(f"✗ {len(missing)} Lückentext-Datei(en) OHNE Wort-Hilfe (daf-kern §7 verletzt):")
            for p in missing:
                print("   ", p)
        if empty:
            print(f"✗ {len(empty)} Datei(en) mit Wortbank-Container, der NIE befüllt wird "
                  f"(initWortbank definiert, aber nicht aufgerufen):")
            for p in empty:
                print("   ", p)
        if suspect:
            print(f"⚠ {len(suspect)} G-Datei(en) mit Wortbank AUS DEN LÖSUNGEN abgeleitet "
                  f"(verrät evtl. die konjugierte/transformierte Zielform — daf-grammatik "
                  f"verlangt einen Infinitiv-Wortkasten). VERDACHT, bitte pro Datei prüfen:")
            for p in suspect:
                print("   ", p)
        if missing or empty:
            print("\nFix: scripts/wortbank-module.js injizieren, §7-Wortbank ergänzen, "
                  "oder initWortbank() in der Init-Sequenz aufrufen.")
        if suspect:
            print("\nFix (VERDACHT): Wortbank-Quelle von .answer auf einen festen "
                  "Infinitiv-Wortkasten umstellen; konjugierte Zielformen nie sichtbar.")
        sys.exit(1)
    print(f"✓ Alle {len(files)} geprüften Dateien haben eine befüllte Wort-Hilfe "
          f"(oder keinen Wort-Lückentext-Tab).")
    sys.exit(0)
