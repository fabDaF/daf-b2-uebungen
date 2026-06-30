#!/usr/bin/env python3
"""
check_genus.py — Sicherheitsnetz für die Genus-Tab-Mindestanzahl.

Regel (CLAUDE.md, Pflicht seit 2026-06-17): Jeder Genus-Tab MUSS mindestens
20 Wörter haben (GENUS_DATA >= 20 Einträge). Empfohlen: 24, aufgeteilt auf
der / die / das / pl. Ein Tab mit 8 Wörtern verschenkt das wichtigste
Training beim Deutschlernen — genau der Fehler, der Frank am 2026-06-17 bei
7011R aufgefallen ist (8 statt 24).

Was als Genus-Tab zählt (wichtig gegen Fehlalarme):
  Manche Dateien benutzen den Variablennamen GENUS_DATA für andere
  Drag-Drop-Übungen (z. B. Konjunktiv-II-Klassen hoeflich/wunsch/… oder
  Verbgruppen 1–7). Das sind KEINE Genus-Tabs. Deshalb zählt ein Array nur
  dann als Genus-Tab, wenn seine cat-Werte echte Genus-Kategorien enthalten
  (der / die / das / pl bzw. m / f / n / plural). Andere Arrays werden
  übersprungen.

Logik:
  - Pro Datei wird der erste GENUS_DATA = [ … ] -Block geklammert gelesen.
  - Ist es kein echter Genus-Tab (keine Genus-Kategorie) -> übersprungen.
  - Sonst: Einträge zählen (ein 'cat:' pro Eintrag). < 20 -> Treffer, Exit 1.

Aufruf:
  python3 scripts/check_genus.py                # ganzes Repo (ohne daf-archiv)
  python3 scripts/check_genus.py datei.html …   # einzelne Dateien

Vor jedem Lektions-Commit laufen lassen — zusammen mit check_serif.py und
check_wortbank.py.
"""
import re
import sys
import os

MINDEST = 20
GENUS_KATEGORIEN = {
    "der", "die", "das", "pl", "plural",
    "m", "f", "n", "maskulinum", "femininum", "neutrum",
}


def genus_block(txt: str):
    """Liefert den Body des ersten GENUS_DATA-Arrays oder None."""
    m = re.search(r"GENUS_DATA\s*=\s*\[", txt)
    if not m:
        return None
    i = m.end() - 1
    depth = 0
    for j in range(i, len(txt)):
        if txt[j] == "[":
            depth += 1
        elif txt[j] == "]":
            depth -= 1
            if depth == 0:
                return txt[i + 1:j]
    return None  # unbalanciert -> behandeln wie "kein Block"


def is_genus_tab(body: str) -> bool:
    cats = {c.lower() for c in re.findall(r"cat\s*:\s*['\"]([^'\"]+)['\"]", body)}
    return bool(cats & GENUS_KATEGORIEN)


def count_entries(body: str) -> int:
    """Ein 'cat:' pro Eintrag — robust gegen Formatierungs-Varianten."""
    return len(re.findall(r"\bcat\s*:", body))


def file_offense(path: str):
    """Liefert (anzahl) wenn echter Genus-Tab mit < MINDEST, sonst None."""
    try:
        txt = open(path, encoding="utf-8", errors="replace").read()
    except OSError:
        return None
    body = genus_block(txt)
    if body is None:
        return None
    if not is_genus_tab(body):
        return None  # kein echter Genus-Tab -> nichts zu prüfen
    n = count_entries(body)
    if n < MINDEST:
        return n
    return None


def genus_style_orphan(txt: str):
    """Liefert den verwaisten Selektor, wenn das Genus-Chip-Pill-Styling an eine
    Section-ID gebunden ist, die es im Dokument NICHT (mehr) gibt — dann rendern die
    Chips als nackter Text statt als Pillen. Genau dieser Fehler ist Frank am
    2026-06-30 bei 3017X aufgefallen: CSS `#sec-genus .chip {…}`, die Genus-Section
    hieß nach der Tab-Umnummerierung aber `id="sec-2"`. Die Drag-Logik (JS nutzte
    `#sec-2`) lief, nur das Styling war tot — check_genus zählte brav 24 Wörter und
    merkte nichts. Fix: id-unabhängiger Selektor (.genus-bank/.genus-zones .chip).

    Nur ID-gebundene Chip-Styling-Regeln sind fragil; klassenbasierte Selektoren
    (.genus-chip, .genus-bank .chip) überstehen jede Umnummerierung und werden ignoriert.
    """
    for sid in re.findall(r"#(sec-[\w-]+)\s+\.(?:genus-)?chip\b", txt):
        if re.search(r'id="' + re.escape(sid) + r'"', txt) is None:
            return sid
    return None


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
    offenders = []
    style_orphans = []
    geprueft = 0
    for p in files:
        try:
            _txt = open(p, encoding="utf-8", errors="replace").read()
            orph = genus_style_orphan(_txt)
            if orph:
                style_orphans.append((orph, p))
        except OSError:
            pass
        n = file_offense(p)
        if n is not None:
            offenders.append((n, p))
        else:
            # Mitzählen, ob es überhaupt ein Genus-Tab war (für die Erfolgsmeldung)
            try:
                body = genus_block(open(p, encoding="utf-8", errors="replace").read())
            except OSError:
                body = None
            if body is not None and is_genus_tab(body):
                geprueft += 1

    if offenders or style_orphans:
        if offenders:
            print(f"✗ {len(offenders)} Genus-Tab(s) mit weniger als {MINDEST} Wörtern "
                  f"(CLAUDE.md-Pflicht verletzt):")
            for n, p in sorted(offenders):
                print(f"    {n:>3}  {p}")
            print(f"\nFix: GENUS_DATA auf mindestens {MINDEST} Einträge erweitern "
                  f"(empf. 24: 6 der / 6 die / 6 das / 4–6 pl). "
                  f"Nur Common Nouns, keine Eigennamen/Marken/Akronyme.")
        if style_orphans:
            print(f"✗ {len(style_orphans)} Genus-Tab(s) mit verwaistem Chip-Styling-Selektor "
                  f"(Chips rendern als nackter Text statt als Pillen):")
            for sid, p in sorted(style_orphans):
                print(f"    #{sid} (keine passende Section-ID)  {p}")
            print("\nFix: ID-gebundenen Selektor auf id-unabhängig umstellen — "
                  "`.genus-bank .chip, .genus-zones .chip` (überlebt Tab-Umnummerierung).")
        sys.exit(1)

    print(f"✓ Alle {geprueft} echten Genus-Tabs haben mindestens {MINDEST} Wörter "
          f"(Nicht-Genus-Arrays mit Namen GENUS_DATA werden übersprungen).")
    sys.exit(0)
