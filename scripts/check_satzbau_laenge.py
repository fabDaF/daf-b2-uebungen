#!/usr/bin/env python3
"""Prüft Satzbau-Satzlängen gegen die Niveau-Staffel (Wortzahl ohne Satzzeichen-Chips).

Staffel (Stand 2026-06-11):
  B1: 12-14 (14 hart) | B2: max 16 | C1: max 18 | C2: 14-18 (min seit 2026-06-11)

Die frühere Prüfung kannte nur Maxima — zu kurze Sätze rutschten durch.
Aufruf: check_satzbau_laenge.py NIVEAU datei.html [...]  oder  NIVEAU verzeichnis
Exit 1 bei Verstößen.
"""
import json, os, re, sys

KORRIDORE = {"B1": (12, 14), "B2": (None, 16), "C1": (None, 18), "C2": (14, 18)}
PUNCT = {".", ",", "!", "?", ";", ":"}


def satz_laengen(html):
    m = re.search(r'var satzbauData\s*=\s*(\[.*?\]);', html, re.S)
    if not m:
        return None
    raw = m.group(1)
    # tolerant: JS -> JSON (unquotierte Keys, einfache Quotes, trailing commas)
    raw = re.sub(r'([{,]\s*)([A-Za-z_]\w*)\s*:', r'\1"\2":', raw)
    raw = re.sub(r",\s*([\]}])", r"\1", raw)
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        try:
            data = json.loads(raw.replace("'", '"'))
        except json.JSONDecodeError:
            return "PARSE"
    out = []
    for item in data:
        woerter = item.get("valid") or item.get("parts") or []
        if woerter and isinstance(woerter[0], list):  # valid[][]
            woerter = woerter[0]
        out.append(len([w for w in woerter if w not in PUNCT]))
    return out


def main():
    if len(sys.argv) < 3 or sys.argv[1].upper() not in KORRIDORE:
        sys.exit(__doc__)
    niveau = sys.argv[1].upper()
    lo, hi = KORRIDORE[niveau]
    dateien = []
    for arg in sys.argv[2:]:
        if os.path.isdir(arg):
            dateien += [os.path.join(arg, f) for f in sorted(os.listdir(arg)) if f.endswith(".html")]
        else:
            dateien.append(arg)
    fehler = 0
    for pfad in dateien:
        with open(pfad, encoding="utf-8") as fh:
            laengen = satz_laengen(fh.read())
        if laengen is None:
            continue  # kein Satzbau-Tab
        if laengen == "PARSE":
            print(f"FEHLER {pfad}: satzbauData nicht parsbar")
            fehler += 1
            continue
        for i, n in enumerate(laengen):
            if (lo and n < lo) or (hi and n > hi):
                print(f"FEHLER {pfad}: Satz {i} hat {n} Wörter (Korridor {niveau}: {lo or '-'}–{hi})")
                fehler += 1
    if fehler:
        print(f"\n{fehler} Verstöße.")
        sys.exit(1)
    print(f"OK — alle Satzbau-Sätze im {niveau}-Korridor.")


if __name__ == "__main__":
    main()
