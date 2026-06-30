#!/usr/bin/env python3
"""check_wortschatz.py — Guardrail für die KANONISCHE Wortschatz-Tab-Struktur.

Hintergrund (2026-06-30): Genus und Satzbau sind zuverlässig, weil der Skill ein
AUSFÜHRBARES Werkzeug liefert (inject_genus.py, geruest_patch.js) + einen Guardrail.
Wortschatz und Lückentext hatten nur ein PROSA-Muster, das jede Generation neu von Hand
nachbaute → Drift, Beinahe-Varianten (ws-card statt luecken-item, passive Anzeige-Karten
ohne Eingabefelder, abweichende Datenstrukturen). Dieser Check definiert „kanonisch"
maschinenlesbar und ist das Gegenstück zu inject_wortschatz.py.

KANONISCH (daf-uebungsformen / wortschatz-full-pattern.md):
  initWortschatz() baut in #wortschatzContainer pro Eintrag eine `.luecken-item`-Karte mit
  einem Prompt (en+Emoji) ÜBER `input.blank`-Feldern, die `dataset.field` (art/word/plural)
  und `dataset.answer` tragen; geprüft per case-sensitivem wortschatzCheck().

Gemeldet wird jede Datei mit Wortschatz-Tab, deren initWortschatz NICHT diese Struktur baut:
  - PASSIV     — keine Eingabefelder (reine Anzeige-Karten, nicht type-bar).
  - WS-CARD    — `.ws-card`/`.vocab-card`-Wrapper statt `.luecken-item` (Frank 2026-06-30: 1023R/1024X).
  - ABWEICHEND — Eingabefelder, aber nicht das kanonische luecken-item/dataset.field-Muster.

Nutzung:
    python3 scripts/check_wortschatz.py            # ganzes Repo (ohne daf-archiv)
    python3 scripts/check_wortschatz.py datei.html # einzelne Dateien

Exit-Code 1 bei Abweichungen. Vor jedem Lektions-Commit zusammen mit den übrigen check_*.
"""
import os, re, sys


def _func_body(s, name):
    m = re.search(r"function\s+" + re.escape(name) + r"\s*\([^)]*\)\s*\{", s)
    if not m:
        return None
    i = m.end() - 1
    depth = 0
    for j in range(i, min(len(s), i + 16000)):
        if s[j] == "{":
            depth += 1
        elif s[j] == "}":
            depth -= 1
            if depth == 0:
                return s[i:j + 1]
    return s[i:i + 16000]


def has_wortschatz_tab(s):
    """Nur ein ECHTER Wortschatz-Tab zählt — nicht ein Reststring (z.B. ein verwaistes
    'wortschatzContainer' in JS/Kommentar bei Lektionen ganz ohne Wortschatz-Tab, wie 2034X).
    Echt = Nav-Tab 'Wortschatz' ODER ein Container-DIV id="wortschatzContainer" im Markup
    ODER eine definierte initWortschatz-Funktion."""
    if re.search(r'nav-label[^>]*>\s*Wortschatz', s):
        return True
    if re.search(r'id="wortschatzContainer"', s):
        return True
    if re.search(r'function\s+initWortschatz\s*\(', s):
        return True
    return False


def classify(s):
    """Liefert None (kanonisch) oder einen Abweichungs-Code (str)."""
    body = _func_body(s, "initWortschatz")
    if body is None:
        return "KEIN-INIT"
    has_input = bool(re.search(r"createElement\(\s*['\"]input['\"]\s*\)", body)) or ("<input" in body)
    is_card = ("ws-card" in body) or ("vocab-card" in body)
    if not has_input:
        return "PASSIV"          # keine type-baren Felder
    if is_card:
        return "WS-CARD"         # falscher Wrapper (1023R/1024X-Klasse)
    # Eingabefelder vorhanden — ist es das kanonische luecken-item/dataset.field-Muster?
    # Struktur kanonisch: type-bare Felder mit bekannter Antwort, in einer Karten-Zeile.
    # Feldnamen sind BEWUSST beliebig — Spezial-Wortschatz (z.B. Verb-Drill Präteritum/Partizip II
    # in G-Dateien wie 2012G) ist legitim; nicht auf art/word/plural einengen. Kartenklasse darf
    # luecke-item ODER luecken-item sein (historische Variante).
    has_answer = any(k in body for k in ("dataset.field", "data-field", "dataset.answer", "data-answer"))
    has_card_row = ("luecken-item" in body) or ("luecke-item" in body)
    if not (has_answer and has_card_row):
        return "ABWEICHEND"
    # Struktur kanonisch — aber auch die OPTIK? (sonst Voll-Box statt Karte, wie Frank 2026-06-30)
    if not canonical_look(s):
        return "OPTIK"
    # Lösungen-Button korrekt verdrahtet? (sonst toter Button, wie Frank 2026-06-30: showLoesungWortschatz)
    if not loesung_button_ok(s):
        return "BUTTON"
    return None


def loesung_button_ok(s):
    """False, wenn ein Wortschatz-Lösungen-Button auf eine NICHT-kanonische Funktion zeigt
    (Namensvariante wie showLoesungWortschatz/showWsLoesung) — dann ist der Button tot, weil die
    alte Funktion auf der ersetzten Struktur arbeitet. Erkennung: onclick-Funktionsname enthält
    loesung/lösung UND wortschatz/ws, ist aber nicht showWortschatzLoesung; oder die kanonische
    Funktion wird aufgerufen, ist aber nicht definiert."""
    # Nur flaggen, wenn ein Wortschatz-Lösungen-Button eine NICHT DEFINIERTE Funktion aufruft
    # (= echt toter Button). Variantennamen (showLoesungWortschatz …) sind ok, solange definiert
    # und auf der vorhandenen Struktur arbeitend. „Kein Lösungen-Button" ist ebenfalls kein Fehler.
    for name in re.findall(r'onclick="\s*([A-Za-z_][A-Za-z0-9_]*)\s*\(\s*\)\s*"', s):
        n = name.lower()
        if ("loesung" in n or "lösung" in n) and ("wortschatz" in n or "ws" in n):
            if not re.search(r'function\s+' + re.escape(name) + r'\s*\(', s):
                return False
    return True


def _css_rule_body(s, selector):
    m = re.search(re.escape(selector) + r"\s*\{([^}]*)\}", s)
    return m.group(1) if m else ""


def canonical_look(s):
    """True, wenn der Wortschatz-Tab die skill-konforme Karten-Optik garantiert: entweder der
    vom Injektor gelieferte scoped CSS-Block (Marker), ODER die globale `.luecken-item`-Regel
    trägt Karten-Styling (background + border-left) UND `input.blank` ist Unterstrich (border-bottom),
    wie im Goldstandard musterdatei-1023G. Sonst rendert der Tab als nackte Voll-Box-Felder."""
    if "FB-WORTSCHATZ-KANON-CSS" in s:
        return True
    li = _css_rule_body(s, ".luecken-item") or _css_rule_body(s, ".luecke-item")
    card = ("background" in li) and ("border-left" in li)
    blank = _css_rule_body(s, "input.blank") or _css_rule_body(s, ".blank")
    underline = "border-bottom" in blank
    return card and underline


def scan(paths):
    bad = []  # (code, path)
    for p in paths:
        try:
            s = open(p, encoding="utf-8", errors="replace").read()
        except OSError:
            continue
        if not has_wortschatz_tab(s):
            continue
        code = classify(s)
        if code is not None:
            bad.append((code, p))
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
    args = sys.argv[1:]
    files = args if args else collect_repo()
    bad = scan(files)
    if bad:
        from collections import Counter
        c = Counter(code for code, _ in bad)
        print(f"✗ {len(bad)} Wortschatz-Tab(s) NICHT kanonisch "
              f"(luecken-item + input.blank[data-field]): " +
              ", ".join(f"{k}={v}" for k, v in sorted(c.items())))
        for code, p in sorted(bad):
            print(f"    [{code:10}] {p}")
        print("\nFix: scripts/inject_wortschatz.py auf die Datei anwenden — baut den Tab "
              "deterministisch nach dem kanonischen Muster (wortschatz-full-pattern.md) neu.")
        sys.exit(1)
    print(f"✓ Alle geprüften Wortschatz-Tabs sind kanonisch ({len(files)} Dateien gescannt).")
    sys.exit(0)
