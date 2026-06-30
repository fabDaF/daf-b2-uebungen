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


def js_builder_defined_and_called(s, name):
    """True, wenn eine JS-Wortbank-Baufunktion `name` DEFINIERT UND auch AUFGERUFEN
    wird. Viele Lektionen bauen ihre §7-Wortbank rein dynamisch — der Container
    bekommt seine Klasse via `.className = 'wort-bank'` (kein literales class=/id=),
    deshalb greifen HELP_RE/CONTAINER_RE nicht. Eine definierte UND aufgerufene
    Baufunktion ist ein verlässliches Signal für eine zur Laufzeit befüllte Wortbank.
    Nur-definiert-aber-nie-aufgerufen zählt NICHT (dann bliebe die Box leer)."""
    defs = len(re.findall(r"function\s+" + re.escape(name) + r"\b", s))
    if defs == 0:
        return False
    total = len(re.findall(r"\b" + re.escape(name) + r"\b", s))
    # total = Definition(en) + echte Referenzen. Bleibt nach Abzug der Definitionen
    # mindestens eine Referenz übrig, wird die Funktion tatsächlich aufgerufen.
    return (total - defs) > 0


def has_js_wortbank(s):
    """Eine zur Laufzeit befüllte JS-Wortbank über das selbst-genügsame B1-Generikum
    `buildWordBank` — diese Funktion erzeugt Container UND Chips selbst und setzt die
    Klasse via `.className='wort-bank'` (kein literales class=/id=, daher von HELP_RE
    nicht erfasst). Definiert UND aufgerufen = verlässliches Signal für eine befüllte
    Wortbank (browser-verifiziert an DE_B1_1013R).

    Bewusst NICHT als Signal: das §7-`initWortbank`. Es baut nur in einen bereits
    vorhandenen Container `#wortbank-luecken`; fehlt der (oder ist LUECKEN_DATA leer),
    läuft die Funktion ins Leere und rendert NICHTS — genau dieser stille Leerlauf trat
    bei Hoefliche_Modalverben_B1B2 auf (initWortbank() aufgerufen, aber 0 Chips im DOM).
    Eine bloße initWortbank-Referenz darf also keine Datei freigeben."""
    return js_builder_defined_and_called(s, "buildWordBank")


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


# (D) DOPPELTE Wort-Hilfe: eine hardcodierte statische §7-Zeile („<strong>Wörter:</strong> …")
# UND ein dynamischer `buildWordBank`, der einen ZWEITEN Kasten (.wort-bank) erzeugt, ohne sich
# abzuschalten. Folge: im Lückentext-Tab erscheinen ZWEI Wortbanken übereinander. Genau dieser
# Fehler ist Frank am 2026-06-30 bei 3042G (und 25 weiteren B1.3-Dateien) aufgefallen — das
# bisherige Netz erkannte ihn nicht, weil JEDE der beiden Banken den §7-Pflicht-Check erfüllt.
STATIC_WOERTER_RE = re.compile(r'<strong>\s*W(?:ö|&ouml;)rter\s*:\s*</strong>')


def has_double_wortbank(s):
    """True, wenn eine statische §7-Zeile UND ein ungeschützter buildWordBank-Zweitkasten
    koexistieren. Der Selbstabschalt-Guard (FB-DOPPELBANK-GUARD bzw. ein early-return gegen
    eine bestehende `.wortkasten`) macht die Datei wieder konform — dann KEIN Treffer."""
    if not STATIC_WOERTER_RE.search(s):
        return False
    if not js_builder_defined_and_called(s, "buildWordBank"):
        return False
    body = _func_body(s, "buildWordBank")
    creates_second = ("'wort-bank'" in body) or ('"wort-bank"' in body)
    if not creates_second:
        return False
    guarded = ("FB-DOPPELBANK-GUARD" in body) or ("querySelector('.wortkasten')" in body)
    return not guarded


def scan(paths):
    missing = []   # (A) gar keine Hilfe
    empty = []     # (B) Container da, aber nie befüllt
    suspect = []   # (C) G-Datei: Wortbank aus Lösungen abgeleitet (Infinitiv-Wortkasten nötig)
    double = []    # (D) zwei Wortbanken gleichzeitig sichtbar
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
        if not (HELP_RE.search(s) or has_js_wortbank(s)):
            missing.append(p)
            continue
        # Hilfe im Markup vorhanden — aber bleibt sie zur Laufzeit leer?
        if CONTAINER_RE.search(s) and initwortbank_defined_but_unused(s):
            empty.append(p)
        # G-Datei: Wortbank verrät evtl. die konjugierte Zielform?
        if gfile_wortbank_from_answers(p, s):
            suspect.append(p)
        # Zwei Wortbanken gleichzeitig sichtbar?
        if has_double_wortbank(s):
            double.append(p)
    return missing, empty, suspect, double


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
    missing, empty, suspect, double = scan(files)
    if missing or empty or suspect or double:
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
        if double:
            print(f"✗ {len(double)} Datei(en) mit ZWEI Wortbanken gleichzeitig "
                  f"(statische §7-Zeile + ungeschützter buildWordBank-Zweitkasten):")
            for p in double:
                print("   ", p)
            print("\nFix (DOPPELT): in buildWordBank einen Selbstabschalt-Guard ergänzen — "
                  "`if (document.querySelector('.wortkasten')) return;` (FB-DOPPELBANK-GUARD).")
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
