#!/usr/bin/env python3
"""check_lueckentext.py — strenges Gate für die KANONISCHE Lückentext-Form.

Kanonische Form (mit Frank 2026-06-30 abgenommen, Piloten 1057X + 3065G):
  - zusammenhängende STORY (durchlaufender Serif-Fließtext mit Inline-Lücken),
    KEINE isolierten Einzelsätze, KEINE Nummerierung;
  - Serifenschrift im Fließtext inkl. Eingabefelder;
  - §7-Wortbank (gemischt, nicht klickbar, .used-Durchstreichen);
  - case-sensitives Live-Feedback, kein Prüfen-Button;
  - GENAU 10 Lücken;
  - Variante V/R/X: Wortbank = Vollformen (data-answer);
  - Variante G: Wortbank = Grundform (data-base), Zielform nie sichtbar.

Marker der kanonischen Engine/CSS: FB-LT-STORY.

Anders als das alte, permissive check_wortbank.py (das JEDE Wort-Hilfe durchwinkte)
erzwingt dieses Gate GENAU EINE Form. Jede Abweichung ist ein Treffer.

Nutzung:
    python3 scripts/check_lueckentext.py            # ganzes Repo (ohne daf-archiv)
    python3 scripts/check_lueckentext.py datei.html # einzelne Dateien
    python3 scripts/check_lueckentext.py --inventur # nur Inventur-Übersicht, Exit 0

Exit-Code 1, wenn KANONISCHE Dateien Verstöße haben (Pre-Commit-Gate).
Nicht-kanonische Altbestände werden als Backlog GEZÄHLT, lösen aber für sich
allein keinen Fehler aus (sie werden im Rollout Spur A/B abgearbeitet) — außer
mit --strict.
"""
import os
import re
import sys

# Lückentext-Tab vorhanden? (auch HTML-entity-kodiert: L&uuml;ckentext)
TAB_RE = re.compile(
    r'nav-label[^>]*>\s*L(?:ü|&uuml;)ckentext'
    r'|<(?:h2|div)[^>]*>\s*[^<]*L(?:ü|&uuml;)ckentext', re.I)

MARKER = "FB-LT-STORY"
# konkurrierende Alt-Engines
COMPETITORS = ("FB-WORTBANK-MODULE", "FB-LT-V1")
GAP_RE = re.compile(r'<input\s+class="blank"\s+data-answer="([^"]*)"([^>]*)>')
GFILE_RE = re.compile(r'_\d{4}G[-_.]')
# Story-Container: <div id="lueckenContainer" class="luecken-story"> … </div>
# (Inhalt sind nur <p>…</p>, kein verschachteltes <div> → das erste </div> schließt.)
STORY_RE = re.compile(r'id="lueckenContainer"[^>]*>(.*?)</div>', re.S)


def story_region(s):
    """Nur der Story-Container. Lücken/Nummern werden NUR hier gezählt, NIE dateiweit
    (sonst zählen Eingaben anderer Tabs mit — Fund am Test 1013R: 11 statt 10)."""
    m = STORY_RE.search(s)
    return m.group(1) if m else ""


def gaps(s):
    return GAP_RE.findall(story_region(s))


def has_numbering(s):
    region = story_region(s)
    if re.search(r'<ol\b', region):
        return True
    if re.search(r'<p>\s*\d+\.\s', region):
        return True
    return False


LEGACY_WORDBANK_FN_RE = re.compile(r'function\s+(\w*[Ww]ort[bB]ank\w*)\s*\([^)]*\)\s*\{\s*')


def has_active_legacy_wordbank(s):
    """Datei-lokale Alt-Wortkasten-Funktion — Sammelbegriff für ALLE Funktionen,
    deren NAME 'wortbank'/'wordbank' enthält (buildWordBank, initWortbank,
    buildWortbank, …), unabhängig davon, wie sie verdrahtet sind. Fund
    2026-06-30 (B1 1013R, buildWordBank mit Anweisungstext) und erneut
    2026-07-01 (B2 1036R: initWortbank() wird per eigenem
    '<script>window.addEventListener("load", …)</script>'-Block NACH der
    kanonischen Engine aufgerufen und überschreibt deren korrekt gefüllte
    #wortbank-luecken mit den alten 12 LUECKEN_DATA-Wörtern — 12 statt 10 Chips
    im Browser-Test). Die kanonische Engine (lt-story-engine.js) hat bewusst
    KEINE Funktion mit 'wortbank' im Namen (dort heißt es schlicht 'bank'/
    'build'/'update'), daher ist der Namensfilter kollisionsfrei.

    WICHTIG (2026-07-01 nachgeschärft): nur eine tatsächlich AUFGERUFENE
    Funktion ist ein Leak. Viele Dateien haben eine solche Funktion nur
    DEFINIERT, aber nie aufgerufen (totes Overhead aus einer früheren
    Migration) — das ist harmlos und KEIN Fehler. Deshalb zählen wir alle
    Vorkommen von 'NAME(' im Dateitext; mehr als 1 Vorkommen (Definition +
    mindestens ein Call, z. B. direkt oder per addEventListener) heißt aktiv.

    ZWEITE Nachschärfung (2026-07-01, Fund an den Piloten 1057X/3065G): eine
    aktiv aufgerufene wortbank-benannte Funktion ist NUR dann ein Leak, wenn
    sie NEBEN der echten, eingespielten Shared-Engine (lt-story-engine.js)
    existiert — erkennbar am literalen Fingerabdruck 'window.__fbLtStory'.
    Die beiden Piloten wurden VOR der Shared-Engine von Hand gebaut; ihre
    initWortbank()/buildWortbankG() & Co. sind dort die EINZIGE, korrekte
    Implementierung (liest live aus dem DOM, keine Alt-Daten) — kein Leak,
    obwohl der Name 'wortbank' enthält und die Funktion aktiv verdrahtet ist.
    Reines Namens-/Aufruf-Matching hätte hier einen funktionierenden Pilot
    kaputt „repariert" (Buttons auf nicht-existente fbLtShowLoesung/fbLtReset
    umgebogen, echte Wortbank-Builder stillgelegt) — genau das ist im ersten
    Anlauf passiert und wurde erst durch Franks Live-Meldung bemerkt.
    Neutralisierung ist ein UNBEDINGTES 'return;' als allererste Anweisung im
    Funktionskörper — ein 'if (!containerEl) return;'-Guard (im Original oft
    vorhanden) zählt NICHT, sonst erkennt der Check die unneutralisierte
    Originalfunktion fälschlich als sauber (genau dieser Fehler ist im ersten
    Anlauf passiert)."""
    if "window.__fbLtStory" not in s:
        return False  # keine Shared-Engine im Spiel -> kein Konkurrenz-Leak möglich
    for m in LEGACY_WORDBANK_FN_RE.finditer(s):
        name = m.group(1)
        start = m.end()
        if re.match(r'return;', s[start:start + 20]):
            continue  # bereits neutralisiert
        occurrences = len(re.findall(r'\b' + re.escape(name) + r'\s*\(', s))
        if occurrences <= 1:
            continue
        # DRITTE Nachschärfung (2026-07-05, Fund an C1 7001V): eine aktive
        # wortbank-benannte Funktion ist NUR dann ein Leak, wenn sie in den
        # Container der Engine ('wortbank-luecken') schreibt. V-Dateien mit
        # zweitem Übungs-Tab (z. B. Kollokationen) haben eigene, legitime
        # wortbank-Funktionen mit EIGENEM Container ('wortbank-koll' o. ä.) —
        # deren Neutralisierung würde eine funktionierende Übung töten.
        naechste = s.find('\nfunction ', start)
        body = s[start:naechste if naechste > -1 else start + 2000]
        if 'wortbank-luecken' in body:
            return True
    return False


def check_canonical(path, s):
    """Liefert Liste von Verstoß-Strings für eine FB-LT-STORY-Datei."""
    problems = []
    if has_active_legacy_wordbank(s):
        problems.append("aktive Alt-Wortbank (buildWordBank mit Anweisungstext) "
                         "nicht neutralisiert — Leak in die Story (Fund 2026-06-30)")
    g = gaps(s)
    n = len(g)
    if n != 10:
        problems.append(f"{n} Lücken (kanonisch sind GENAU 10)")
    if has_numbering(s):
        problems.append("Nummerierung in der Story (verboten)")
    for c in COMPETITORS:
        if c in s:
            problems.append(f"konkurrierende Alt-Engine vorhanden: {c}")
    if 'class="wortkasten"' in s:
        problems.append("statischer wortkasten vorhanden (Leak-/Doppelbank-Gefahr)")
    # Variante INHALTSGETRIEBEN (nicht per Dateiname): keine data-base = Wortschatz,
    # alle = Grammatik. Nur GEMISCHT ist ein Fehler. (G-Dateiname erzwingt NICHT
    # data-base — z. B. 1015G temporaladverbien ist Vokabel-Einsetzung ohne
    # Transformation, also korrekt Wortschatz-Variante.)
    with_base = sum(1 for _, rest in g if "data-base=" in rest)
    if 0 < with_base < n:
        problems.append(f"gemischte Variante: {with_base}/{n} Lücken mit data-base "
                        f"(entweder alle = Grammatik/Grundform, oder keine = Wortschatz)")
    return problems


def missing_loesungen_button(s):
    """True, wenn der LT-Abschnitt einer kanonischen Datei KEINEN Lösungen-Button
    trägt (statische Näherung; tote Alt-Buttons erkennt nur scripts/lt_verify.js).
    Frank-Fund 2026-07-04 an 1013R: Engine-Hook fbLtShowLoesung existiert, aber
    kein Button war je darauf verdrahtet. Adapter-Dateien (zweiter LT-Tab) sind
    ausgenommen — dort gelten dateilokale Handler."""
    if ("lueckenContainer2" in s) or ("blank2" in s):
        return False
    i = s.find('id="wortbank-luecken"')
    if i < 0:
        return False
    sec = max(s.rfind('<div class="section"', 0, i), s.rfind('<section', 0, i))
    if sec < 0:
        return False
    env = s[sec:i]
    if "fbLtShowLoesung" in env:
        return False
    return not re.search(r'<button[^>]*>[^<]*L(?:ö|&ouml;)sung', env)


def scan(paths):
    canonical_ok = []
    canonical_bad = []   # (problems, path)
    backlog = []         # Lückentext-Tab, aber noch nicht kanonisch
    nobtn = []           # kanonisch, aber ohne Lösungen-Button (warnend)
    for p in paths:
        try:
            s = open(p, encoding="utf-8", errors="replace").read()
        except OSError:
            continue
        if not TAB_RE.search(s):
            continue
        if MARKER not in s:
            backlog.append(p)
            continue
        probs = check_canonical(p, s)
        if probs:
            canonical_bad.append((probs, p))
        else:
            canonical_ok.append(p)
        if missing_loesungen_button(s):
            nobtn.append(p)
    return canonical_ok, canonical_bad, backlog, nobtn


def collect_repo():
    out = []
    for dp, dn, fn in os.walk("."):
        if "/daf-archiv" in dp or "/.git" in dp:
            continue
        for f in fn:
            if f.endswith(".html") and ".bak" not in f:
                out.append(os.path.join(dp, f))
    return out


def level_of(p):
    b = os.path.basename(p)
    m = re.search(r'DE_(A1|A2|B1|B2|C1|C2)_', b)
    if m:
        return m.group(1)
    for lvl in ("A1", "A2", "B1", "B2", "C1", "C2"):
        if f"/{lvl}" in p or f"{lvl}." in p:
            return lvl
    return "?"


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    flags = {a for a in sys.argv[1:] if a.startswith("--")}
    files = args if args else collect_repo()
    ok, bad, backlog, nobtn = scan(files)

    total = len(ok) + len(bad) + len(backlog)
    print(f"Lückentext-Inventur: {total} Dateien mit Lückentext-Tab")
    print(f"  ✓ kanonisch (FB-LT-STORY, konform): {len(ok)}")
    print(f"  ✗ kanonisch, aber fehlerhaft:        {len(bad)}")
    print(f"  ⧗ Backlog (noch nicht kanonisch):    {len(backlog)}")

    # Backlog pro Niveau (= Rollout-Umfang)
    if backlog:
        per = {}
        for p in backlog:
            per[level_of(p)] = per.get(level_of(p), 0) + 1
        order = sorted(per.items())
        print("    Backlog pro Niveau: " + ", ".join(f"{k}={v}" for k, v in order))

    if bad:
        print("\nFehlerhafte kanonische Dateien:")
        for probs, p in bad:
            print(f"  ✗ {p}")
            for pr in probs:
                print(f"       - {pr}")

    if nobtn:
        print(f"\n⚠ {len(nobtn)} kanonische Datei(en) ohne Lösungen-Button im LT-Abschnitt "
              f"(Fix: scripts/fix_lt_buttons.py, dynamischer Test: scripts/lt_verify.js):")
        for p in nobtn[:15]:
            print(f"    {p}")
        if len(nobtn) > 15:
            print(f"    … und {len(nobtn) - 15} weitere")

    if "--inventur" in flags:
        sys.exit(0)

    # Gate: kanonische Dateien MÜSSEN konform sein. Backlog blockt nur mit --strict.
    # Fehlende Lösungen-Buttons blocken nur mit --strict-buttons — solange der
    # C1-Rollout läuft, bleibt das eine Warnung (Kalibrierung 2026-07-04).
    fail = (bool(bad)
            or ("--strict" in flags and bool(backlog))
            or ("--strict-buttons" in flags and bool(nobtn)))
    sys.exit(1 if fail else 0)
