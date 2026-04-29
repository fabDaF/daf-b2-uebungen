#!/usr/bin/env python3
"""
Dashboard-Refactoring (2026-04-29):

1. C1-Mega-Karte (id 'c1', 23 Einheiten) splitten in drei Karten:
   - c11 (C1.1): nr 101x..107x
   - c12 (C1.2): nr 201x..207x
   - c13 (C1.3): nr 301x..308x plus 90xx (Vertiefungsblock)

2. niveau-Feld an alle Niveau-Kurse anhängen:
   - a11, a12 → 'A1'
   - a21, a22 → 'A2'
   - b11, b12, b13 → 'B1'
   - b21, b22, b23, b2x → 'B2'
   - c11, c12, c13 → 'C1'
   - c2 → 'C2'
   - alle übrigen Top-Level-Kurse (a1drill, grund, lueck, arch, vertragssprache, devops) bleiben ohne niveau-Feld.

3. render()-Funktion + CSS für Niveau-Gruppen-Akkordeon erweitern (eigener Schritt — siehe injectGroups()).
"""
import re
import sys
from pathlib import Path

DASHBOARD = Path(__file__).resolve().parent.parent / "htmlS" / "dashboard.html"


def split_c1_block(text: str) -> str:
    """Splitte den existierenden c1-Block in c11/c12/c13."""
    # Den C1-Header lokalisieren
    pat_header = re.compile(
        r"  \{\n"
        r"    id: 'c1', label: 'C1 Grammatik',\n"
        r"    titel: 'Deutsch C1 – Grammatik für Fortgeschrittene',\n"
        r"    basis: 'https://fabdaf\.github\.io/daf-c1-uebungen/',\n"
        r"    einheiten: \[\n",
        re.M,
    )
    m = pat_header.search(text)
    if not m:
        raise SystemExit("FATAL: c1-Header nicht gefunden — abgebrochen, kein Schreibvorgang.")
    new_header_c11 = (
        "  {\n"
        "    id: 'c11', label: 'C1.1', niveau: 'C1',\n"
        "    titel: 'Deutsch C1.1 – Redewiedergabe, Konjunktiv II Vergangenheit, Nominalstil & mehr',\n"
        "    basis: 'https://fabdaf.github.io/daf-c1-uebungen/',\n"
        "    einheiten: [\n"
    )
    text = text[: m.start()] + new_header_c11 + text[m.end():]

    # Vor '{ nr: '201x'' den C1.1→C1.2-Trennblock einfügen
    sep_12 = (
        "    ]\n"
        "  },\n"
        "  {\n"
        "    id: 'c12', label: 'C1.2', niveau: 'C1',\n"
        "    titel: 'Deutsch C1.2 – Konnektoren, Modalverben, Partizipialkonstruktionen & raffiniertere Ausdrucksformen',\n"
        "    basis: 'https://fabdaf.github.io/daf-c1-uebungen/',\n"
        "    einheiten: [\n"
    )
    pat_201 = re.compile(r"      \{ nr: '201x',", re.M)
    m2 = pat_201.search(text)
    if not m2:
        raise SystemExit("FATAL: 201x-Einheit nicht gefunden.")
    text = text[: m2.start()] + sep_12 + text[m2.start():]

    # Vor '{ nr: '301x'' den C1.2→C1.3-Trennblock einfügen
    sep_23 = (
        "    ]\n"
        "  },\n"
        "  {\n"
        "    id: 'c13', label: 'C1.3', niveau: 'C1',\n"
        "    titel: 'Deutsch C1.3 – Genitiv, Nominalisierung, Stilistik, Geistesgeschichte & Prüfungsvorbereitung',\n"
        "    basis: 'https://fabdaf.github.io/daf-c1-uebungen/',\n"
        "    einheiten: [\n"
    )
    pat_301 = re.compile(r"      \{ nr: '301x',", re.M)
    m3 = pat_301.search(text)
    if not m3:
        raise SystemExit("FATAL: 301x-Einheit nicht gefunden.")
    text = text[: m3.start()] + sep_23 + text[m3.start():]

    return text


def add_niveau_field(text: str) -> str:
    """An jede Niveau-Karte das niveau-Feld anhängen (idempotent — 'niveau:' wird nicht doppelt gesetzt)."""
    mapping = {
        "a11": "A1",
        "a12": "A1",
        "a21": "A2",
        "a22": "A2",
        "b11": "B1",
        "b12": "B1",
        "b13": "B1",
        "b21": "B2",
        "b22": "B2",
        "b23": "B2",
        "b2x": "B2",
        "c2": "C2",
        # c11, c12, c13 sind bereits beim Split mit niveau: 'C1' versehen
    }
    for kurs_id, niveau in mapping.items():
        # Replace `id: 'a11', label: 'A1.1',` → `id: 'a11', label: 'A1.1', niveau: 'A1',`
        old = re.compile(
            rf"id: '{re.escape(kurs_id)}', label: '([^']+)',\n"
        )
        m = old.search(text)
        if not m:
            print(f"  WARN: Karte id={kurs_id} nicht gefunden — übersprungen.")
            continue
        # Idempotenz: prüfe, ob niveau-Feld schon da ist
        next_block = text[m.end(): m.end() + 200]
        if "niveau:" in next_block.split("titel:", 1)[0]:
            print(f"  SKIP: id={kurs_id} hat bereits niveau-Feld.")
            continue
        new = f"id: '{kurs_id}', label: '{m.group(1)}', niveau: '{niveau}',\n"
        text = text[: m.start()] + new + text[m.end():]
        print(f"  OK: id={kurs_id} → niveau: '{niveau}'")
    return text


def main():
    text = DASHBOARD.read_text(encoding="utf-8")
    print("=== Schritt 1: C1-Block splitten ===")
    text = split_c1_block(text)
    print("  OK: c1 → c11 + c12 + c13")
    print()
    print("=== Schritt 2: niveau-Feld an alle Niveau-Karten ===")
    text = add_niveau_field(text)
    DASHBOARD.write_text(text, encoding="utf-8")
    print()
    print(f"=== Datei geschrieben: {DASHBOARD} ===")


if __name__ == "__main__":
    main()
