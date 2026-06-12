#!/usr/bin/env python3
"""Prüft Satzbau-Satzlängen gegen die Niveau-Staffel (Wortzahl ohne Satzzeichen-Chips).

Staffel (Stand 2026-06-12):
  A1: 5-9  (KEINE Kommasätze erlaubt)
  A2: einfacher Satz 6-10  |  Kommasatz 9-14 (14 hart)   [ROLLOUT-SATZBAU-A2.md]
  B1: 12-14 (14 hart) | B2: max 16 | C1: max 18 | C2: 14-18 (min seit 2026-06-11)

Ein "Kommasatz" ist ein Satz mit Komma-Chip (',' eigenes parts-Element).

A2-Zusatzprüfung (Kommasatz-Quote pro Satzbau-Tab):
  mind. 2 Kommasätze und mind. 1 Frage (punct '?') pro Datei.
  Standardmäßig WARNUNG (blockiert Exit-Code nicht — frühe Lektionen ohne
  freigegebene Konnektoren dürfen kommafrei sein). Mit --strict-quote werden
  Quote-Verstöße zu harten Fehlern.

Die frühere Prüfung kannte nur Maxima — zu kurze Sätze rutschten durch.
Aufruf: check_satzbau_laenge.py NIVEAU [--strict-quote] datei.html [...]  oder  NIVEAU verzeichnis
Exit 1 bei Verstößen.
"""
import json, os, re, sys

# (lo_einfach, hi_einfach, lo_komma, hi_komma) — Komma-Korridor None = wie einfach
KORRIDORE = {
    "A1": (5, 9, None, None),       # Kommasätze verboten -> Sonderbehandlung
    "A2": (6, 10, 9, 14),
    "B1": (12, 14, 12, 14),
    "B2": (None, 16, None, 16),
    "C1": (None, 18, None, 18),
    "C2": (14, 18, 14, 18),
}
PUNCT = {".", ",", "!", "?", ";", ":"}


def satz_infos(html):
    """Liste von dicts {n, komma, frage} pro Satz; None=kein Tab; 'PARSE'=Fehler."""
    m = re.search(r'var satzbauData\s*=\s*(\[.*?\]);', html, re.S)
    if not m:
        return None
    raw = m.group(1)
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
        parts = item.get("parts") or woerter
        komma = "," in parts or "," in woerter
        frage = (item.get("punct") or ".") == "?"
        out.append({
            "n": len([w for w in woerter if w not in PUNCT]),
            "komma": komma,
            "frage": frage,
        })
    return out


def main():
    args = [a for a in sys.argv[1:] if a != "--strict-quote"]
    strict_quote = "--strict-quote" in sys.argv
    if len(args) < 2 or args[0].upper() not in KORRIDORE:
        sys.exit(__doc__)
    niveau = args[0].upper()
    lo_e, hi_e, lo_k, hi_k = KORRIDORE[niveau]
    dateien = []
    for arg in args[1:]:
        if os.path.isdir(arg):
            dateien += [os.path.join(arg, f) for f in sorted(os.listdir(arg)) if f.endswith(".html")]
        else:
            dateien.append(arg)
    fehler = 0
    warnungen = 0
    for pfad in dateien:
        with open(pfad, encoding="utf-8") as fh:
            infos = satz_infos(fh.read())
        if infos is None:
            continue  # kein Satzbau-Tab
        if infos == "PARSE":
            print(f"FEHLER {pfad}: satzbauData nicht parsbar")
            fehler += 1
            continue
        for i, info in enumerate(infos):
            n, komma = info["n"], info["komma"]
            if niveau == "A1" and komma:
                print(f"FEHLER {pfad}: Satz {i} ist ein Kommasatz — auf A1 nicht erlaubt")
                fehler += 1
                continue
            if komma and lo_k is not None:
                lo, hi = lo_k, hi_k
            else:
                lo, hi = lo_e, hi_e
            if (lo and n < lo) or (hi and n > hi):
                art = "Kommasatz" if komma else "Satz"
                print(f"FEHLER {pfad}: {art} {i} hat {n} Wörter (Korridor {niveau} "
                      f"{'Komma' if komma else 'einfach'}: {lo or '-'}–{hi})")
                fehler += 1
        # Kommasatz-Quote (nur A2)
        if niveau == "A2":
            n_komma = sum(1 for x in infos if x["komma"])
            n_frage = sum(1 for x in infos if x["frage"])
            mangel = []
            if n_komma < 2:
                mangel.append(f"nur {n_komma} Kommasätze (<2)")
            if n_frage < 1:
                mangel.append("keine Frage (punct '?')")
            if mangel:
                stufe = "FEHLER" if strict_quote else "WARNUNG"
                print(f"{stufe} {pfad}: Kommasatz-Quote — {', '.join(mangel)}")
                if strict_quote:
                    fehler += 1
                else:
                    warnungen += 1
    if fehler:
        print(f"\n{fehler} Verstöße" + (f", {warnungen} Warnungen." if warnungen else "."))
        sys.exit(1)
    if warnungen:
        print(f"OK (Länge) — {warnungen} Quote-Warnungen (kein Exit-Fehler ohne --strict-quote).")
    else:
        print(f"OK — alle Satzbau-Sätze im {niveau}-Korridor.")


if __name__ == "__main__":
    main()
