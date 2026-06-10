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

## Offene Bestände
- B1.1: 95 Dateien (8 Piloten haben schon inline-row) · B2-Root: 143 · C1: 165
- Manuell-Liste C2 (14 Sätze „unter 2 sichere Anker") + ~10 Sonderdateien
  (sbShowSolution fehlt / abweichende Struktur) — einzeln nacharbeiten.
- Spezialordner (Architektur, Mattmüller, schueler/, ir/, daf-materialien): zuletzt, separat.
- Danach: geruest_patch.js + diese Erkenntnisse in den daf-satzbau-Skill übernehmen.
