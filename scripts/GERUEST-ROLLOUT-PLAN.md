# Gerüst-Modus-Rollout (Satzbau B1+) — Stand & Plan

## Erledigt (2026-06-09)
- **C2 komplett (71 Dateien, Commits 8084208 + 339f1e9):** Gerüst-Add-on additiv injiziert,
  532/546 Sätze mit konservativ berechneten Ankern, 14 auf Manuell-Liste (unter 2 sichere Anker).
  Pro Satz eigene Buttons „Lösen" (duplikatfest, setzt alle Chips korrekt) + „↺ Neustart".
- **Werkzeug:** `scripts/geruest_patch.js` (Node). Konservative Ankerwahl: nie Verben
  (AUX-Liste + starke Präterita + Endungs-Heuristiken inkl. -te/-ern/-eln), Wort 2 jeder
  valid-Reihenfolge gebannt (V2), kleingeschriebenes Wort 3 gebannt (mehrteiliges Vorfeld),
  Verbpräfixe gebannt, nur invariante Positionen, round(W/3) geklammert 2–4.
  Satzzeichen-Chips (Komma!) sind beweglich in der Bank, nie Anker. Re-Patch idempotent
  (alter Add-on-Block wird ersetzt). Zwei Familien: A (chips-/builder-/sfb-, Klick+Drag,
  flaches valid) und B (sb-bank-/sb-row-/sb-fb-, kanonisch).

## Frank-Direktive für B1+ (2026-06-09)
**Ab B1 Nebensatz-Training:** Komma-Chip + entsprechend längere Sätze (12+ Wörter,
Nebensätze; deckt sich mit daf-registry canonical_values.satzbau_words_per_sentence).
→ Der Rollout für B1.1/B2/C1 ist daher ZWEISTUFIG pro Datei:
1. **Inhalt:** satzbauData prüfen; zu kurze/einfache Sätze durch themengebundene
   12+-Wort-Sätze MIT Nebensätzen (Komma als eigener Chip in parts UND valid) ersetzen.
   Quellen-/Stilregeln wie immer (Quasthoff, Lektionsthema). KEINE Subagenten (daf-satzbau!).
2. **Technik:** `node scripts/geruest_patch.js DATEI.html --write`, danach Syntax-Check
   des Add-on-Blocks; Batch-Commit via safe-commit.sh; Browser-Stichprobe.

## Erledigt (2026-06-10) — B1.1 Hauptbestand
**87 von 101 satzbauData-Dateien komplett zweistufig umgestellt** (10 Batches,
je Batch: Inhalt → geruest_patch.js → Verify → safe-commit). Alle ~640 Sätze
auf 12+ Wörter mit Nebensatz + Komma-Chip gehoben; 0 Patcher-Flags.
Nebenbei bereinigt: Punkt-Chips (2033R), Kleinschreibungs-Bugs
(2046R/2053R/2054X/2055G/2056R/konnektor-insofern), Mehr-Wort-Chips
(1023R „der Wind", partizip2, 1063R/1064X Datums-Chips), elliptischer Satz
(2057X), fehlende Kommas (2027X), ~50 Alt-Quote-Fehler (ASCII-Schließer).
Werkzeuge der Session: `/outputs/apply_lib.js` (Batch-Apply mit Pre-Checks:
12W-Minimum, Komma-Pflicht, valid-Längen/Multiset, Ein-Wort-Chips) +
`verify_geruest.js` (Script-Syntax, Quote-Regex mit `<`-Ausschluss,
SBGAP-Konsistenz: Lücken==parts, Anker invariant, nie Komma als Anker).

## Offene Bestände B1.1 (14 Dateien)
1. **8 Piloten 1011X–1018S:** haben inline-`row`, aber Sätze noch 7–11 Wörter.
   Inhalt neu schreiben UND `row` von Hand neu berechnen (Patcher überspringt
   Sätze mit row) — ODER row-Felder entfernen, dann normale Zweistufen-Route.
2. **6 Sonderschema-Dateien** (`chip-bank-N` + `satzbau-container`, Patcher
   meldet „unbekanntes ID-Schema"): 3044X, 3045G, 3046R, 3047X, 3048S —
   Inhalt noch alt; 2054X Inhalt schon neu. Option: Familie C im Patcher
   ergänzen (Render ist dynamisch, analog Familie B).
3. **B1_1013R_Neue_Berufe.html + DE_B1_1013R-neue-berufe.html:** Altdateien
   ohne satzbauContainer, vermutlich Legacy — prüfen, ob 1013R-Pilot sie ersetzt.

## Offene Bestände gesamt
- B2-Root: 143 · C1: 165
- Manuell-Liste C2 (14 Sätze „unter 2 sichere Anker") + ~10 Sonderdateien
  (sbShowSolution fehlt / abweichende Struktur) — einzeln nacharbeiten.
- Spezialordner (Architektur, Mattmüller, schueler/, ir/, daf-materialien): zuletzt, separat.
- Danach: geruest_patch.js + diese Erkenntnisse in den daf-satzbau-Skill übernehmen.
