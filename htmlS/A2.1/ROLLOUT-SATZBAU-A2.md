# Satzbau-Rollout A2 — verbindliche Spezifikation

Beschlossen am 2026-06-12 (Frank + Claude). Gilt für alle **93** A2-Dateien mit
kanonischem `satzbauData` (+ `sbMakeChip`/`sbRegisterZone`) im Repo
`daf-a2-uebungen` (htmlS/A2.1). Zusätzlich **15 Sonderfall-Dateien** auf
abweichenden Satzbau-Patterns (siehe Vorstufe 0), die erst migriert werden
müssen, bevor die Staffel auf sie anwendbar ist. Ergänzt den Skill
**daf-satzbau**; bei Widersprüchen gilt diese Spec, bis der Skill-Text
nachgezogen ist.

## Staffel (ersetzt die bisherige A1/A2-Zeile „8–12")

| Niveau | Wörter | Modus |
|---|---|---|
| A1 | 5–9 | freier Bau, nur einfache Hauptsätze und Fragen, KEINE Kommasätze |
| A2 einfache Sätze | 6–10 | freier Bau |
| A2 Kommasätze | 9–14 (14 hart) | **Hybrid:** bis 10 Wörter freier Bau, ab 11 Wörtern geführter Gerüst-Modus (`geruest_patch.js`) |

Satzzeichen-Chips zählen nicht mit. Zu kurze Sätze mit Zeit-/Ortsangaben
verlängern, nie künstlich aufblähen.

## Kommasatz-Quote

Pro Satzbau-Tab (üblich 7–8 Sätze): **mindestens 2 Kommasätze**, sobald die
Lektion mindestens einen Nebensatz-Konnektor oder aber/sondern kennt.
Darunter immer mindestens eine Frage (`punct: '?'`). Einfacher Kommasatz =
genau EINE Verzweigung (HS + NS oder HS, aber HS) — nie geschachtelt.

## Konnektoren — nur Gelerntes

Drei Familien, jeweils erst ab der Lektion erlaubt, in der sie eingeführt
sind (Freigabetabelle siehe unten, Schritt 1 des Rollouts):

1. **Position 0:** und, oder (KEIN Komma davor), aber, denn, sondern (Komma davor)
2. **Adverb Position 1 + Inversion, kein Komma:** dann, danach, deshalb, trotzdem
3. **Nebensatz + Komma, Verb-Ende:** weil, dass, wenn, (spät-A2: als)

Komma ist eigener Chip (`','` in parts UND valid), CSS `.punct-chip`-Regel
muss in der Datei stehen (daf-satzbau §Komma als Chip).

## Beide Stellungen als Lösung

Wo grammatisch sauber, akzeptiert `valid` beide Reihenfolgen — Nebensatz
vorn und hinten („Weil ich krank bin, bleibe ich zu Hause." / „Ich bleibe
zu Hause, weil ich krank bin."). Der Komma-Chip wandert in den
valid-Arrays mit.

## Rollout-Schritte

0. **Vorstufe — Pattern-Vereinheitlichung (Pflicht vor Schritt 3).** 15
   Satzbau-Dateien laufen nicht auf dem kanonischen `satzbauData`-Schema und
   reagieren daher weder auf `check_satzbau_laenge.py` noch auf
   `geruest_patch.js`. Erst auf `satzbauData` + `sbMakeChip`/`sbRegisterZone`
   migrieren, dann erst Staffel anwenden:
   - **11× Alt-Pattern `var/const SATZBAU`:** `A2_101x_G1_G2_R_Meine_Freunde`,
     `A2_101x_V1_X1_V2_X2_Meine_Freunde`, `A2_102x_V1_X1_V2_X2_Bewerbungen`,
     `A2_104x_G1_G2_R_Stadtleben`, `A2_104x_V1_X1_V2_X2_Stadtleben`,
     `A2_105x_G1_G2_R_Sport`, `A2_105x_V1_X1_V2_X2_Sport`,
     `A2_106x_G1_G2_R_Futur`, `A2_106x_V1_X1_V2_X2_Zukunft`,
     `A2_107x_W_Wiederholung`, `brief-an-eine-maschine`.
   - **1× primitives `satzbau3`-Exaktstring-Match (kein `valid[][]`, keine
     Großschreibungs-Behandlung):** `DE_A2_2043G-konjunktiv-II`.
   - **3× Satzbau-Tab ohne Datenquelle im erwarteten Format** (Datenvariable
     anders benannt — vor Migration verifizieren): `A2_102x_G1_G2_R_Bewerbungen`,
     `A2_103x_G1_G2_R_Wohnen`, `A2_103x_V1_X1_V2_X2_Wohnen`.

1. **Konnektoren-Freigabetabelle** aus den 93 Dateien + Quell-PDFs
   extrahieren → `references/a2-konnektoren.md` (Lektionscode → erlaubte
   Konnektoren). Vor dem Schreiben neuer Sätze IMMER konsultieren.
2. **`scripts/check_satzbau_laenge.py`** (B2-Root) um die A1/A2-Staffel
   erweitern, inkl. Minima und Kommasatz-Quote.
3. **Batch pro Einheit** (101x → 106x, dann 201x → 206x): Sätze auf
   Staffel bringen, Kommasatz-Quote herstellen, valid-Varianten ergänzen.
   Kein Subagent (Skill-Schwur).
4. **Gerüst-Patcher** nur für Kommasätze ab 11 Wörtern:
   `node scripts/geruest_patch.js DATEI.html --write`, danach PFLICHT
   Anker-Review (suspectVerb-Lücke: 1.-Person--e-Formen!) + `caps:true`
   prüfen. Verben, Konnektoren (= Zielform!) und Komma-Chips NIE als Anker.
5. **Pro Datei:** JSDOM-Erstlade-Test (nackter Pfad, URL-Option gegen
   localStorage-Artefakt). **Pro Einheit:** Browser-Stichprobe mit
   sbShowSolution.
6. Vor jedem Commit: check_satzbau_laenge, check_wortbank, check_serif,
   Anführungszeichen-Regex. Commit via safe-commit.sh.
7. **Skill-Update daf-satzbau** (Staffel-Tabelle + Hybrid-Regel + neue
   Reference) als .skill verpacken → Frank installiert.

## Randbefunde (beim Rollout miterledigen)

- `DE_A2_1014R-die-hochzeit.html`: **kein Defekt.** Frühere Meldung „parts
  leer" war ein Fehlbefund eines Quote-Stil-Scans — die Datei schreibt ihre
  `parts` mit ASCII-Doppelquotes (`["Alex", "war", …]`) statt einfachen
  Anführungszeichen; ein Scan, der nur `'…'` erkennt, zählt 0. Tatsächlich 8
  saubere Sätze mit 7–9 Wörtern. Nichts reparieren; höchstens Quote-Stil auf
  einfache Anführungszeichen normalisieren (Kanon).
- Bestand 2026-06-12 (unabhängig nachgezählt): kürzester Satz 3 Wörter; **232
  von 744 Sätzen (31 %) unter 6 Wörtern** → Hauptarbeit ist Verlängern, nicht
  Kürzen (0 Sätze über 14). Kommasätze: **67 Sätze in 24 von 93 Dateien**
  (9 %) — Kommasatz-Quote muss fast überall erst hergestellt werden.
