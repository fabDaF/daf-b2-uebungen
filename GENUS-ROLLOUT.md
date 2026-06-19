# Genus-Tab-Ausrollung — Kampagnenplan

**Ziel (Frank, 2026-06-19):** Der Genus-Tab ist integraler Bestandteil des
Deutschlernens und soll **strukturell überall** vorhanden sein. Zu wenige
Lektionen haben ihn aktuell. Diese Kampagne baut ihn in alle Lektionstypen
ein — **außer die expliziten Drill-Aufgaben (FDxx)**.

**Wortquelle (Entscheidung):** Lektionsspezifisch, skill-konform nach
daf-kern — pro Datei 20–24 thematisch passende Common Nouns aus dem
Lektionsfeld (empf. 24: 6 der / 6 die / 6 das / 4–6 pl). Keine Eigennamen,
Marken, Akronyme. Genus jedes Nomens vor Einbau verifizieren.

## Ausgangslage (Inventar 2026-06-19)

816 Lektionen mit Lektionscode; davon **570 ohne Genus-Tab**. Die Lücken
sind nicht zufällig — ganze Typen sind praktisch unversorgt.

| Typ | mit Genus | ohne |
|-----|-----------|------|
| R (Lesen)        | 105 | 100 |
| S (Sprechen)     |  91 |  51 |
| X (Textarbeit)   |  40 | 151 |
| G (Grammatik)    |   2 | 157 |
| V (Vokabular)    |   2 |  61 |
| C                |   2 |  34 |
| W (Schreibwerkstatt) | 4 | 16 |

Größte Lücken: **G, V, C, X**. R und S sind dort gut versorgt, wo es schon
frühere Kampagnen gab (C1/C2-S, viele R).

## Kanonisches Genus-Tab-Muster (Referenz)

Quelle: daf-kern §2 + daf-grammatik (`references/js-patterns.md`,
Selektor `.genus-cat`/`.genus-drop`). Lebende Referenz mit Text-Chips:
bestehende 305 Genus-Tabs. Bestandteile pro Tab:

1. **Nav-Button** im `.nav` (Emoji 🏷️, Label „Genus") — Index passend zur
   Datei-Tab-Mechanik (`showTab`/`showSection`).
2. **Section** mit eigenem **Banner** (daf-kern §2) → Vorentlastungs-Box →
   `genus-pool` → drei (bzw. vier mit Plural) Drop-Kategorien
   der/die/das(/pl) → Feedback-Zeile.
3. **`GENUS_DATA`** (≥20 Einträge, `{word, cat}`), `initGenus()`,
   `checkGenusChip()`, `updateGenusFeedback()`, Drag-Drop + Klick-Variante.
4. **Verdrahtung:** `initGenus()` beim Tab-Wechsel + im Init-Block;
   Timer-Auto-Start im `dragstart`; `resetTimer` im Reset.

⚠️ **Heterogene Tab-Mechanik:** Dateien stammen aus verschiedenen
Generationen (`showTab` vs. `showSection`, `sec-N` vs. `sec-schreib`).
Einfügung ist **pro Datei chirurgisch**, kein blindes Massen-Skript.

⚠️ **Wortschatz bleibt letzter Tab** (Projektregel) — Genus-Tab davor
einordnen.

## Offene strategische Entscheidung: Banner

daf-kern §2 verlangt ein eigenes Bild pro Tab (kein Bild doppelt). Bei 570
neuen Genus-Tabs bedeutet das 570 einzelne Pexels-Fetches über Chrome —
der dominierende Zeitfaktor der Kampagne. Optionen siehe Chat-Rückfrage.

## Wellen-Plan (Vorschlag)

1. **Pilot** (1 Datei je Kerntyp G + V) → Browser-Test → Abnahme durch Frank.
2. **Welle 1:** G + V + C (~252) — größte strukturelle Lücke.
3. **Welle 2:** X (~151).
4. **Welle 3:** R-Rest + S-Rest + W (~167).

Pro Datei: themed Nomen + Genus-Check → Banner → chirurgische Einfügung →
`check_genus.py` grün → Browser-Test → safe-commit + push.

## Sicherheitsnetz

`scripts/check_genus.py` (2026-06-19) erzwingt ≥20 Wörter pro echtem
Genus-Tab. Vor jedem Lektions-Commit laufen lassen.
