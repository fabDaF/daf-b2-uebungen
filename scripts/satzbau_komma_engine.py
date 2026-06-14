#!/usr/bin/env python3
"""satzbau_komma_engine.py — rüstet Gen-A-Satzbau-Dateien (Chip-Klasse `.chip`)
mit Komma-Chip-Unterstützung nach (zwei chirurgische Eingriffe, idempotent).

Hintergrund: A2-Satzbau zerfaellt in zwei Engine-Generationen. Gen-B
(`.sb-chip`) kann Komma-Chips bereits darstellen. Gen-A (`.chip`, aeltere
A2-Dateien) NICHT — `sbMakeChip` kennt `punct-chip` nicht, das CSS fehlt.
Komma-Saetze sind dort nicht darstellbar, bis die Engine nachgeruestet ist.
Das ist die Voraussetzung fuer die A2-Kommasatz-Quote (ROLLOUT-SATZBAU-A2.md).

Eingriff 1 (JS): in `sbMakeChip`, direkt nach `<var>.className='chip';`
    if(word===','||word===';')<var>.classList.add('punct-chip');
  <var> ist 'chip' oder 'c' (wird aus dem Funktionskoerper gelesen).
  Erster Parameter von sbMakeChip ist projektweit 'word'.

Eingriff 2 (CSS): vier Regeln direkt nach der ersten vorhandenen Chip-Status-
  Regel (Anker-Fallback: .chip.selected -> .chip.incorrect -> .chip.wrong
  -> .chip.correct). Verifiziert an DE_A2_1011V und DE_A2_1061V.

Beide Eingriffe sind unabhaengig idempotent: schon vorhandene Teile werden
nicht erneut eingefuegt (Marker: 'punct-chip' im sbMakeChip-Koerper bzw.
'.chip.punct-chip' im Dokument).

Aufruf:
  satzbau_komma_engine.py datei.html [datei2.html ...]        # Dry-Run (Report)
  satzbau_komma_engine.py --write datei.html [datei2.html ...] # schreibt
Exit 0 wenn alle Dateien sauber verarbeitet; Exit 1 bei einem Problemfall.
"""
import re
import sys

CSS_BLOCK = (
    "\n.chip.punct-chip { background: #f8f8f8; color: #333; font-weight: 700; "
    "min-width: 14px; padding-left: 8px; padding-right: 8px; }"
    "\n.chip.punct-chip.correct   { background: #27ae60; border-color: #27ae60; color: white; }"
    "\n.chip.punct-chip.incorrect { background: #e74c3c; border-color: #e74c3c; color: white; }"
    "\n.sentence-builder .chip.punct-chip { margin-left: -6px; }"
)

CSS_ANCHORS = [
    r"\.chip\.selected\s*\{[^}]*\}",
    r"\.chip\.incorrect\s*\{[^}]*\}",
    r"\.chip\.wrong\s*\{[^}]*\}",
    r"\.chip\.correct\s*\{[^}]*\}",
]


def extract_func_span(t, name):
    """Gibt (start, end) des Funktionskoerpers (inkl. Signatur bis schliessende
    Klammer) per Brace-Matching zurueck, oder None."""
    m = re.search(r"function\s+" + name + r"\s*\([^)]*\)\s*\{", t)
    if not m:
        m = re.search(name + r"\s*=\s*function\s*\([^)]*\)\s*\{", t)
    if not m:
        return None
    brace = t.index("{", m.start())
    depth = 0
    for i in range(brace, len(t)):
        if t[i] == "{":
            depth += 1
        elif t[i] == "}":
            depth -= 1
            if depth == 0:
                return (m.start(), i + 1)
    return None


def patch_js(t):
    """Fuegt den Komma-Check in sbMakeChip ein. Gibt (neuer_text, status) zurueck.
    status: 'js-added' | 'js-skip' (schon da) | 'js-fail' (kein Anker)."""
    span = extract_func_span(t, "sbMakeChip")
    if not span:
        return t, "js-fail"
    fs, fe = span
    body = t[fs:fe]
    if "punct-chip" in body:
        return t, "js-skip"
    mv = re.search(r"(\w+)\.className\s*=\s*'chip'\s*;", body)
    if not mv:
        return t, "js-fail"
    var = mv.group(1)
    insert = " if(word===','||word===';')%s.classList.add('punct-chip');" % var
    new_body = body[: mv.end()] + insert + body[mv.end():]
    return t[:fs] + new_body + t[fe:], "js-added"


def patch_css(t):
    """Fuegt die vier punct-chip-Regeln ein. Gibt (neuer_text, status) zurueck.
    status: 'css-added' | 'css-skip' | 'css-fail'."""
    if re.search(r"\.chip\.punct-chip", t):
        return t, "css-skip"
    for pat in CSS_ANCHORS:
        m = re.search(pat, t)
        if m:
            return t[: m.end()] + CSS_BLOCK + t[m.end():], "css-added"
    return t, "css-fail"


def process(path, write):
    with open(path, encoding="utf-8") as f:
        orig = f.read()
    t, js = patch_js(orig)
    t, css = patch_css(t)
    ok = "fail" not in (js, css)
    if write and t != orig and ok:
        with open(path, "w", encoding="utf-8") as f:
            f.write(t)
    return js, css, ok, (t != orig)


def main(argv):
    write = "--write" in argv
    files = [a for a in argv if a != "--write"]
    if not files:
        print(__doc__)
        return 0
    bad = 0
    for p in files:
        js, css, ok, changed = process(p, write)
        flag = "OK " if ok else "FAIL"
        verb = "geschrieben" if (write and changed and ok) else ("waere geaendert" if changed else "unveraendert")
        print(f"  [{flag}] {js:9s} {css:10s} {verb:16s} {p}")
        if not ok:
            bad += 1
    print(f"\n{len(files)} Dateien, {bad} Problemfaelle." + ("" if write else "  (DRY-RUN — nichts geschrieben; --write zum Anwenden)"))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
