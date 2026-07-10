#!/usr/bin/env python3
"""check_orphan_init.py — Sicherheitsnetz gegen verwaiste Init-Aufrufe.

Fehlerklasse (Frank-Fund 2026-07-10, 16 Dateien über A1/A2/B2):
Bei Migrationen (Lückentext-Story-Engine, Wortschatz-Kanon) blieben im
Init-Block Aufrufe auf Funktionen stehen, die es nicht mehr gibt —
z. B. `initLuecken();`, `initVocab();`, `buildVocab();`, `vocabInit();`.
Ein solcher Aufruf wirft zur Laufzeit `ReferenceError: X is not defined`
und bricht die GESAMTE restliche Init-Kette ab: alle danach initialisierten
Tabs (Satzbau, Multiple Choice, Wortschatz, Schreibwerkstatt) bleiben leer.
JS-Parse (node --check) bleibt grün, weil der Aufruf syntaktisch gültig ist —
der Fehler entsteht erst beim Ausführen.

Erkennung (rein statisch): Ein Statement, das nur aus einem parameterlosen
Aufruf `name();` auf niedriger Einrückung besteht (Top-Level-Init), dessen
`name` NIRGENDS in den Inline-Scripts definiert ist (weder als function,
noch als Variable/Zuweisung/Arrow/window-Property).

Nutzung:
    python3 scripts/check_orphan_init.py            # ganzes Repo (ohne daf-archiv)
    python3 scripts/check_orphan_init.py datei.html # einzelne Dateien

Exit 1 bei Treffern — läuft als blockierendes Gate in check_all.py.
"""
import os
import re
import sys

SCRIPT_RE = re.compile(r'<script(?![^>]*\bsrc=)[^>]*>(.*?)</script>', re.S | re.I)
# Aufruf-Statement: nur `name();` (+ optional Kommentar). Ob es TOP-LEVEL ist,
# entscheidet zusätzlich die Klammertiefe 0 (siehe orphan_calls).
CALL_RE = re.compile(r'^[ \t]*([A-Za-z_$][\w$]*)\(\)\s*;\s*(?://.*)?$')


def blank_strings_comments(js):
    """Ersetzt String-/Kommentar-Inhalte durch Leerzeichen, erhält Zeilenumbrüche
    und Klammern AUSSERHALB von Strings. Damit wird die Klammertiefe verlässlich,
    ohne dass geschweifte Klammern in Strings/Kommentaren sie verfälschen."""
    out = []
    i, n = 0, len(js)
    mode = None  # None | 'line' | 'block' | '"' | "'" | '`'
    while i < n:
        c = js[i]
        nxt = js[i + 1] if i + 1 < n else ""
        if mode is None:
            if c == "/" and nxt == "/":
                mode = "line"; out.append("  "); i += 2; continue
            if c == "/" and nxt == "*":
                mode = "block"; out.append("  "); i += 2; continue
            if c in "\"'`":
                mode = c; out.append(" "); i += 1; continue
            out.append(c); i += 1; continue
        # innerhalb String/Kommentar
        if mode == "line":
            if c == "\n": mode = None; out.append("\n")
            else: out.append(" ")
            i += 1; continue
        if mode == "block":
            if c == "*" and nxt == "/": mode = None; out.append("  "); i += 2; continue
            out.append("\n" if c == "\n" else " "); i += 1; continue
        # String
        if c == "\\":
            out.append("  "); i += 2; continue
        if c == mode:
            mode = None; out.append(" "); i += 1; continue
        out.append("\n" if c == "\n" else " "); i += 1; continue
    return "".join(out)

# In JS eingebaute/globale parameterlose Aufrufe, die legitim sein können.
BUILTINS = {
    "print", "alert", "blur", "focus", "stop", "close", "clear",
}


def defined_names(js):
    names = set()
    names |= set(re.findall(r'\bfunction\s+([A-Za-z_$][\w$]*)', js))
    names |= set(re.findall(r'(?:var|let|const)\s+([A-Za-z_$][\w$]*)', js))
    names |= set(re.findall(r'\b([A-Za-z_$][\w$]*)\s*=\s*function', js))
    names |= set(re.findall(r'\b([A-Za-z_$][\w$]*)\s*=\s*\([^)]*\)\s*=>', js))
    names |= set(re.findall(r'\b([A-Za-z_$][\w$]*)\s*=\s*[A-Za-z_$][\w$]*\s*=>', js))
    names |= set(re.findall(r'window\.([A-Za-z_$][\w$]*)\s*=', js))
    return names


def orphan_calls(path):
    try:
        s = open(path, encoding="utf-8", errors="replace").read()
    except OSError:
        return None
    blocks = SCRIPT_RE.findall(s)
    if not blocks:
        return []
    all_js = "\n".join(blocks)
    defined = defined_names(all_js)
    orphans = []
    for b in blocks:
        orig_lines = b.split("\n")
        skel_lines = blank_strings_comments(b).split("\n")
        depth = 0  # Klammertiefe zu BEGINN der aktuellen Zeile
        for orig, skel in zip(orig_lines, skel_lines):
            start_depth = depth
            depth += skel.count("{") - skel.count("}")
            if start_depth != 0:
                continue  # nur ECHTE Top-Level-Aufrufe (nicht in Funktionskörpern)
            m = CALL_RE.match(orig)
            if not m:
                continue
            name = m.group(1)
            if name in defined or name in BUILTINS:
                continue
            orphans.append(name)
    # Reihenfolge erhalten, Duplikate raus
    seen = []
    for n in orphans:
        if n not in seen:
            seen.append(n)
    return seen


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
        orph = orphan_calls(p)
        if orph:
            bad.append((p, orph))
    if bad:
        print(f"✗ {len(bad)} Datei(en) mit verwaisten Init-Aufrufen "
              f"(ReferenceError bricht Init-Kette ab, Tabs dahinter leer):")
        for p, names in bad:
            print(f"    {p}  ->  {', '.join(n + '()' for n in names)}")
        print("\nFix: den verwaisten Aufruf entfernen, WENN eine Ersatz-Engine "
              "die Aufgabe übernimmt (z. B. Story-Lückentext / Wortschatz-Kanon). "
              "Vorher prüfen, dass der zugehörige Tab anderweitig befüllt wird.")
        sys.exit(1)
    print(f"✓ Keine verwaisten Init-Aufrufe ({len(files)} Dateien geprüft).")
    sys.exit(0)
