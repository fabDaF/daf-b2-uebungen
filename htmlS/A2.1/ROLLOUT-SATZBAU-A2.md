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
| A2 | 6–14 (14 hart) | **geführter Gerüst-Modus** (wie B1+, `geruest_patch.js`) — NICHT freier Bau. Einfache Sätze UND Kommasätze, alle im Gerüst. Korrigiert 2026-06-12 nach Franks B2-Referenz (1011X): A2-Satzbau soll wie B2 aussehen, mit festen Ankern + gestrichelten Leerfeldern. |

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

## Stand 2026-06-12

- **Schritt 1 erledigt:** Konnektoren-Freigabetabelle liegt in
  `htmlS/A2.1/a2-konnektoren.md` (belegt aus Lektionstiteln). Vor jeder
  Satz-Neuschreibung konsultieren.
- **Schritt 2 erledigt:** `scripts/check_satzbau_laenge.py` kennt jetzt die
  A1/A2-Staffel inkl. Dual-Korridor (einfach 6–10 / Komma 9–14), A1-Komma-
  verbot und A2-Kommasatz-Quote (`--strict-quote` macht die Quote hart).
  Erstlauf gegen Bestand: 284 Längenverstöße (253 einfach, 31 Komma) + 88
  Quote-Warnungen.
- **Schritt 3 angefangen:** `DE_A2_1011V-meine-freunde.html` komplett auf
  Spec gebracht und als **Referenzimplementierung** committet (Engine +
  CSS + Daten + JSDOM-Test grün, `--strict-quote` bestanden). Vorlage für
  den Batch.
- **Schritt 3 — Einheit 101x ERLEDIGT 2026-06-14:** 1012X–1018S auf Staffel
  gebracht (alle Sätze 6–14 W), je Datei ≥2 Kommasätze + 1 Frage, valid-
  Varianten wo Vorfeld flexibel. `--strict-quote` grün, JSDOM-Erstlade +
  Komma-Engine grün. Einheit 101x nutzt nur koordinierende Konnektoren
  (und/oder/aber/denn/sondern) — Kommasätze als „HS, aber/denn HS". Sonder-
  fall **1013G (Plusquamperfekt):** behält die temporalen Nebensätze
  nachdem/bevor (das ist der Grammatikfokus = de-facto-Einführungslektion
  dieser Strukturen), der progressionswidrige weil-Satz (weil erst ab 1043)
  wurde durch eine PQP-Frage ersetzt. **1014R:** parts-Quote-Stil von ASCII-
  Doppel- auf einfache Anführungszeichen normalisiert (Kanon). Gerüst-Modus
  (Schritt 4) für 101x noch offen — bewusst getrennt gehalten.
- **Schritt 3 — Einheit 102x ERLEDIGT 2026-06-14:** 1021V–1028S (Arbeitswelt/
  Bewerbungen) auf Staffel, je ≥2 Kommasätze (aber/denn) + Frage, valid-
  Varianten. `--strict-quote` + JSDOM grün. Didaktische Anker: Dativ-Frage
  „wem" in 1023G (Verben mit Dativ); Telefon-Grußformeln in 1026X bewusst
  ohne Konnektor-Komma (würden den 9–14-W-Kommakorridor verfehlen). Zahl-Chip
  „35" in 1024R durch „viele" ersetzt.
- **Schritt 3+4 ZUSAMMENGEFÜHRT (Frank 2026-06-14): Daten und Gerüst sind EIN
  Schritt, nie getrennt ausliefern.** Freier Bau ist kein auslieferbarer
  Zwischenzustand für A2. `geruest_patch.js` um eine **Konnektoren-Sperre**
  erweitert (und/oder/aber/denn/sondern/weil/dass/wenn/… nie Anker — Zielform
  gehört in die Bank). Gerüst-Modus nachgezogen für **101x + 102x** (16
  Dateien) und direkt mitgebaut für **103x**. daf-satzbau-Skill aktualisiert
  (A2 = Gerüst, „Zweites Versprechen" Daten+Gerüst untrennbar, Konnektoren-
  Sperre) und als .skill zur Installation übergeben.
- **Schritt 3+4 — Einheit 103x ERLEDIGT 2026-06-14:** 1031V–1038S (Wohnen)
  Daten auf Staffel + Quote UND Gerüst in einem Schwung. Komparativ/Superlativ-
  Vergleiche (als/wie), Zahlen ausgeschrieben (achthundert statt 865 etc.).
  7/7 Sätze pro Datei konvertiert, 0 Konnektor-Anker, `--strict-quote` + JSDOM
  grün.
- **ALLE KANONISCHEN EINHEITEN ERLEDIGT 2026-06-15:** 104x, 105x, 106x
  (A2.1) + 201x, 202x, 203x, 204x-kanonisch (2041V/2047G/2048S), 205x, 206x
  (A2.2) — alle Daten auf Staffel + Kommasatz-Quote UND Gerüst in einem
  Schwung, parts==valid konsistent, JSDOM-Erstlade grün. Konnektoren-
  Progression beachtet (deshalb/darum ab 2023, als ab 2033, damit ab 2046).
  Zahlen ausgeschrieben, Caps korrigiert, Wortstellungsfehler behoben.
  Patcher-Verbesserung: NOTVERB um flektierte Artikel/Adjektive/Adverbien
  (-en/-t) erweitert, damit kurze Sätze nicht fälschlich aus dem Gerüst
  fallen. Vereinzelt bleiben kurze Mittel-Sätze (6 W, viele Verben/Partikeln)
  additiv im freien Bau — nie an Position 0.
- **Lückentext-Ästhetik 2026-06-15:** `.luecken-text` projektweit auf
  Serifenschrift + einheitliches Lese-Panel umgestellt (34 Dateien);
  `.luecken-text` in `check_serif.py` aufgenommen.
- **Vorstufe-0-Sonderfälle — 4 von 9 ERLEDIGT 2026-06-15:** 1042X + 1046X
  (waren längst kanonisch parts/valid, nur Gerüst fehlte → gepatcht); 1071W +
  1072S (words-Struktur → JS `.words`→`.parts`, parts/valid, Staffel+Quote,
  Gerüst). Alle 4 live, JSDOM-Erstlade grün.
- **NUR NOCH OFFEN — 5 Sonderfälle mit EIGENEM, nicht-kanonischem Satzbau-JS
  (click-basiert, Exaktstring-Vergleich gegen `.correct`/`words`, KEINE
  sbMakeChip/sbRegisterZone/initSatzbau):** 2042X (`SATZBAU_DATA` chips-Struktur),
  2043G (`satzbau3` parts/correct, click + sb-bank/sb-row), 2044R
  (`SENTENCE_DATA`/`words`), 2045V (`var words`, kein Satzbau-Container),
  2046X (builder-/`.correct`). Diese brauchen je einen **vollständigen
  Satzbau-Tab-Neubau** (eigenes JS entfernen, kanonisches Drag+Gerüst-Pattern
  einsetzen) — eigenes, sorgfältiges Paket, am besten in frischem Kontext
  (kaputter Tab = Unterrichts-Risiko).
- **2043G Tab-Neubau ERLEDIGT 2026-06-15 (Pilot):** eigenes satzbau3/click-JS
  durch kanonisches Drag+Gerüst (aus 1013G) ersetzt; Konjunktiv-II-Sätze auf
  Staffel+Quote, 6/7 geführt, Syntax/Konsistenz/Erstlade grün, live. Weg
  dokumentiert in Memory `reference_satzbau-tab-neubau.md`.
- **NOCH OFFEN — 4 Tab-Neubauten mit JE EIGENER Infrastruktur (nicht uniform!):**
  2042X (`SATZBAU_DATA` chips-Struktur), 2044R (`SENTENCE_DATA`/words),
  2045V (`var words`), 2046X (Sätze als `data-correct` in hardcodierten HTML-
  Chips + eigene Timer `startTimer`/`switchTab` statt timerAutoStart/showSection).
  Jede braucht individuelle Anpassung des Pilot-Wegs (Timer-Index/Funktionsnamen,
  Daten-Ort, Container). In frischem Kontext einzeln sauber bauen.
- **NEUE Voraussetzung entdeckt (Komma-Engine-Lücke):** Die 93 kanonischen
  Dateien zerfallen in **zwei Engine-Generationen**:
  - **Gen-B (35 Dateien):** Chip-Klasse `.sb-chip`, `sbMakeChip` setzt
    `punct-chip` für `','`/`';'`, CSS vorhanden → komma-fähig.
  - **Gen-A (58 Dateien, u. a. 1011V):** Chip-Klasse `.chip`, **kein**
    Komma-Support — `sbMakeChip` kennt `punct-chip` nicht, CSS fehlt.
    Komma-Sätze sind hier nicht darstellbar, bis die Engine nachgerüstet
    ist. **Das ist der eigentliche Grund, warum A2 die Kommasatz-Quote
    nirgends erfüllt.**
  - Minimal-Patch pro Gen-A-Datei (an 1011V verifiziert, zwei chirurgische
    Eingriffe): (1) in `sbMakeChip` nach `chip.className='chip';` einfügen
    `if(word===','||word===';')chip.classList.add('punct-chip');`; (2) CSS
    `.chip.punct-chip{…}` + `.chip.punct-chip.correct/.incorrect` +
    `.sentence-builder .chip.punct-chip{margin-left:-6px;}` direkt nach
    `.chip.selected`. Capitalization-Logik (`i===0`) verträgt Kommas bereits.
  - **ERLEDIGT 2026-06-14:** Patcher `scripts/satzbau_komma_engine.py` gebaut
    (idempotent, var-aware für `chip`/`c`, patcht nur den `sbMakeChip`-Körper
    — nie Q&A-/Kategorie-Chips —, CSS-Anker-Fallback
    `.selected→.incorrect→.wrong→.correct`) und über alle Gen-A-Satzbau-
    Dateien gelaufen. Saubere Neu-Klassifikation per `sbMakeChip`+`satzbauData`
    ergab **54** echte Gen-A-Dateien ohne Komma-JS (nicht 58 — die Differenz
    waren Q&A-only-Dateien und Sonderfälle ohne kanonischen Satzbau). 5 davon
    hatten ein vorbestehendes, unvollständiges punct-chip-CSS (margin-Regel
    fehlte) → gezielt ergänzt. Verifikation: JSDOM-Funktionstest 54/54
    (`sbMakeChip(',')`→`.punct-chip`, Wort→kein punct-chip), Syntax-Check aller
    Script-Blöcke grün, Diff gegen HEAD trägt ausschließlich punct-chip-Zeilen.
    Gen-B (1 Datei) braucht keinen Engine-Patch.
- **Offen:** Vorstufe 0 (15 Sonderfälle), Schritt 3 Rest (101x ff. Daten auf
  Staffel + Kommasatz-Quote), Schritt 4–7.

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
