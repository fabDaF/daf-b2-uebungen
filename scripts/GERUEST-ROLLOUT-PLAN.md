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

## Frank-Direktive für B1+ (2026-06-09, präzisiert 2026-06-10)
**Ab B1 Nebensatz-Training:** Komma-Chip + Sätze mit **12 bis maximal 14 Wörtern**
(ohne Satzzeichen-Chips gezählt). 14 ist hartes Maximum — Deutschlerner neigen zu
überlangen Sätzen, die Übungen dürfen das nicht vorleben. Sätze mit 15+ Wörtern
sind ein Fehler, auch wenn sie grammatisch sauber sind. (Die daf-registry sagt
nur „12+" — beim nächsten Skill-Update auf „12–14" präzisieren.)
**Satzlängen-Staffel (Frank, 2026-06-10):** B1: 12–14 Wörter (14 = hartes
Maximum) · B2: max. 16 · C1 und C2: max. 18. C2-Bestand NICHT kürzen
(15–18 dort ausdrücklich in Ordnung). Prüfskripte beim B2/C1-Rollout auf
die jeweilige Grenze einstellen.

**Geführter Modus (2026-06-10, Franks didaktische Auflösung der Komplexität):**
Sofort-Feedback pro Chip-Platzierung. Richtig (konsistent mit mind. einer
valid-Reihenfolge unter Berücksichtigung aller schon platzierten Chips) →
Chip wird grün und fixiert (nicht mehr beweglich). Falsch → Chip wird rot,
Feedback „✗ Das passt hier nicht!", nach 800 ms Rücksprung in die Bank.
Letzter richtiger Chip → Punkt + „✓ Korrekt!". Implementiert im Add-on
(placeJudge/consistent/finishRow/toBank in geruest_patch.js); Guards gegen
Verschieben fixierter Chips in dragstart, Slot-Drop und Bank-Drop.
toBank() stellt bei jedem Chip-Rücksprung die Kleinschreibung wieder her —
ein an Position 0 großgeschriebener Chip darf in der Bank den Satzanfang
nicht verraten (Frank, 2026-06-10; Skill-Fallstrick „Großbuchstabe bleibt
in Bank").
JSDOM-Test: /outputs/jsdom_test_geruest.js (5 Testfälle, Drag-Pfad).
ERLEDIGT 2026-06-10: C2-Bestand (71 Dateien, Familie A) re-gepatcht —
geführter Modus + toBank überall; JSDOM-Klick-Pfad-Test grün; Satzlängen
unangetastet.
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
**Patcher-Fix:** `ensureButtons` erkennt jetzt native Lösen/Neustart-Buttons
im `.satzbau-item` und legt kein zweites Paar mehr an (B1.1-Dateien erzeugen
ihre Buttons selbst in initSatzbau — C2 nicht; vor B2/C1-Rollout beachten).
Browser-Test 1021X + 3038S: 1 Buttonpaar/Satz, Lösen/Neustart/Komma-Chips ok.
Werkzeuge der Session: `/outputs/apply_lib.js` (Batch-Apply mit Pre-Checks:
12W-Minimum, Komma-Pflicht, valid-Längen/Multiset, Ein-Wort-Chips) +
`verify_geruest.js` (Script-Syntax, Quote-Regex mit `<`-Ausschluss,
SBGAP-Konsistenz: Lücken==parts, Anker invariant, nie Komma als Anker).

## B1.1 KOMPLETT (2026-06-10, Session 3) — 101/101 Dateien
1. **Piloten 1011X–1018S:** 65 Sätze neu (12–14W), inline-row entfernt,
   Add-on mit geführtem Modus übernimmt (JSDOM 6/6 grün, auch 1016R-Relativsätze).
2. **Sonderschema gelöst:** 3044X–3048S nutzten intern längst Familie-B-IDs
   (Fehlalarm der Verdachtsliste) — 35 Sätze neu, direkt patchbar. 2054X auf
   Familie-B-IDs konvertiert (bank/builder/feedback bekommen sb-*-IDs in
   initSatzbau, Add-on ersetzt das native Free-Build-Rendering).
   ensureButtons hat jetzt parentNode-Fallback für Container ohne .satzbau-item.
3. **Legacy bereinigt:** B1_1011X/B1_1013R (nirgends verlinkt) ins
   daf-archiv/B1.1-legacy überführt und aus dem B1.1-Repo entfernt.

## Erledigt (2026-06-10, Session 2) — B2 begonnen
**B2 fast komplett: 127 von 142 Satzbau-Dateien (~760 Sätze), Session 3:**
Einheiten 101–106, 201–206, 301–306 inkl. 3013R-Syntaxreparatur (CSS war in
Script-Block gerutscht) und Patcher-Lockerung (fehlendes natives
sbShowSolution nicht mehr fatal — Add-on-Buttons übernehmen).
B2 KOMPLETT (2026-06-10, Session 4): alle 141 patchbaren Dateien fertig
(inkl. 9013R, GEHIRN_08S, WCO01–13 mit ~200 Sätzen). 1047X bleibt bewusst
ohne Gerüst (Satzglieder-Übung). JSDOM-Stichproben grün.
Ursprünglich (Session 2, 82/143):** B2 war
inhaltlich schon nah dran (Nebensätze + Komma-Chips vorhanden, aber meist
10–11 Wörter) → chirurgische Verlängerung auf 12–16 statt Komplett-Neuschreibung.
Werkzeuge: `/outputs/apply_lib2.js` (applyFix = Index-genauer Ersatz mit
min/max-Checks pro Niveau) + `/outputs/triage.js` (zeigt nur defiziente Sätze).
Nebenbei: Quote-Altlast GLOBAL beseitigt (995 ASCII-Schließer in 238 B2/C1-
Dateien, alle in Single-Quote-JS-Strings = gefahrlos), als-ob-Indikativ-Fix
(1046R), defekter Satz 1055G#0, fehlendes „uns" 1052G#5, Gedankenstrich-Chip
1048S, Serif-Fixes 1056R/1063R, sbData→satzbauData-Rename 1053R,
Mehr-Wort-Chips 2035G/2036R, Semikolon-Chip 2022G, Kleinschreibung 2026R.

**B2-Sonderfälle:**
- 1047X-satzglieder-erkennen: satzbauData OHNE valid (Satzglieder-Übung,
  kein Wortstellungs-Training) → bekommt KEIN Gerüst, ist korrekt so.
- 3013R-die-geschichte-der-mythologie: JS-Syntaxfehler schon in HEAD
  (wie die A2-Fälle vom 2026-06-03) → vor dem Gerüst-Patch reparieren.

## Erledigt (2026-06-10, Session 5) — C1 Einheiten 204–207 + 301–303
**50 Dateien, 300 Sätze auf 12–18W mit Nebensatz + Komma-Chip** (7 Batches,
je Batch Inhalt → geruest_patch → verify → safe-commit):
- 204 (8 Dateien, Commit adf7c8f): Wortstellung/Beschwerde/Guillotine/Wall-Street/
  Urheberrecht/Freemium/Menschenrechte/Datenschutz.
- 205 (8, c9f5add): Ausdruck/Ethik/Ökolandbau/inform. Kommunikation/Tiny-Houses/
  Minimalismus/Robinson/Trampen.
- 206+207 (10, e538ca5): Konj. II Vergangenheit/Etymologie/alte Zivilisationen/
  Vorstellungsgespräch/Frauenwahlrecht/Titanic/Thoreau/Konsumismus/Rede/Essay.
- 301 (8, ed6ce66): Genitiv-Verben/Diagramm/Null-Emissions/Abholzung/Vogelschutz/
  Polarkappen/Humboldt/Nachhaltigkeit.
- 302 (8, 0bfb0e7): Nominalisierung/Textabschnitt/Kreativität/Placebo/Projektmgmt/
  Konfliktmgmt/Naturwiss. 19. Jh./Recycling.
- 303 (8, ad15cea): Konnektoren/effizient schreiben/Zwillingsparadoxon/Eiszeitalter/
  wiss. Artikel/schwarzes Loch/Mars/Verhandlungstaktiken.
Alle Patcher-Läufe flag-frei, verify_geruest grün, check_wortbank + check_serif grün.
JSDOM-Stichprobe Familie B (3021G/3031G) grün; Familie-A-Dateien sind vom
JSDOM-Test (nur sb-*-IDs) erwartungsgemäß nicht abgedeckt — SBGAP-Konsistenz
deckt sie ab.

## Offene Bestände gesamt
- B2-Root: KOMPLETT · C1: 122 von 162 Dateien fertig (Einheiten 101–106 + 201–207
  + 301–303, ~730 Sätze auf 12–18W). C1-Befund: fast alle Sätze waren <12W ohne
  Komma → volle Fix-Route pro Einheit. Weiter ab Einheit 304 (DE_C1_304x ff.,
  dann 305–308 sowie die Blöcke 700 und 901–907), gleiche Werkzeugkette
  (triage.js → applyFix mit min 12 / max 18 → geruest_patch → verify).
- Manuell-Liste C2 (14 Sätze „unter 2 sichere Anker") + ~10 Sonderdateien
  (sbShowSolution fehlt / abweichende Struktur) — einzeln nacharbeiten.
- Spezialordner (Architektur, Mattmüller, schueler/, ir/, daf-materialien): zuletzt, separat.
- Danach: geruest_patch.js + diese Erkenntnisse in den daf-satzbau-Skill übernehmen.
