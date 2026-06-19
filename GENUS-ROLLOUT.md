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

## Banner (Entscheidung Frank, 2026-06-19)

**Eine** wiederverwendbare Spezialgrafik fürs Genus-Üben statt 570
Einzelbilder: `htmlS/genus-banner.svg` (der/die/das, projektfarben,
editorial-typografisch, abgenommen). Wird als
`data:image/svg+xml;base64,…` in jeden neuen Genus-Tab eingebettet
(SVG muss embedded sein — die Niveau-Repos sind getrennt, ein relativer
Pfad bräche). Bestehende Genus-Tabs behalten ihr Bild.

## Insertion-Rezept (am Piloten 1101V verifiziert)

1. **Nav:** Genus-`nav-btn` (🏷️, „Genus") direkt VOR dem Wortschatz-Button
   einfügen; `onclick=showSection(N)` mit N = alter Wortschatz-Index;
   Wortschatz-Button auf N+1 hochzählen.
2. **Section:** `id="sec-genus"` direkt VOR der Wortschatz-Section. DOM-
   Reihenfolge = showSection-Index (rein positionsbasiert).
3. **CSS:** Genus-Block vor `</style>`.
4. **JS:** `GENUS_DATA` (≥20) + initGenus/checkGenusChip/updateGenusFeedback/
   createGenusChip + eigener Shuffle vor dem INIT-Block; `initGenus()` in den
   INIT-Block; `initTimer`-Schleife um den Genus-Timer-Index erweitern.
5. **⚠️ Timer-Funktionsname variiert pro Generation!** `timerAutoStart` ist
   NICHT überall definiert (im Piloten gar nicht — Alt-Bug der Datei). Daher
   `genusTimerStart/Stop/Reset`-Helfer mit `typeof`-Guard, Fallback auf
   `startTimer`/`stopTimer`/`resetTimer`.
6. **Test (PFLICHT, in dieser Reihenfolge):**
   a. `scripts/audit_genus.py DATEI` — onclick-Ziele == 0..n-1 UND nav==sec.
      **Ohne diesen Check NICHT committen.** (Siehe Vorfall unten.)
   b. `scripts/check_genus.py DATEI` — ≥20 Wörter.
   c. JS-`node --check` + optional JSDOM-Funktionstest (Chips/Feedback).

## ⚠️ Vorfall 2026-06-19 — Nav-Renummerierung

Eine frühe `inject_genus`-Version renummerierte nur `class="nav-btn"` und
übersah den ersten Button `class="nav-btn active"` → onclick-Ziele wurden
`0,0,1,2,…` statt `0,1,2,…`. Folge: **jeder Tab-Klick zeigte die falsche
Sektion** (18 A1-Dateien betroffen, von Frank im Unterricht entdeckt).
Der JSDOM-Test rief `showSection(i)` per Schleifenindex auf statt über das
echte `onclick` — und **maskierte den Bug**. Lehre: Tab-Korrektheit IMMER
über die tatsächlichen `onclick`-Werte prüfen → `audit_genus.py`. Die
aktuelle `inject_genus.py` renummeriert ALLE `onclick`-Attribute (klassen-
unabhängig); die 18 Dateien wurden per Renummerierung repariert.

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
