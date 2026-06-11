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

## Erledigt (2026-06-10, Session 6) — C1 Einheiten 304–308
**37 Dateien, 246 Sätze auf 12–18W mit Nebensatz + Komma-Chip** (4 Batches):
- 304 (8 Dateien, Commit b61f7e4): Partizipialkonstr./akad. Wortschatz/Amazonas/
  7 Weltwunder/Alpen/Sächsische Schweiz/Pangaea/Überleben Wüste.
- 305 (8, d8137f3): Ausdruck/Rhetorik/biolog. Unsterblichkeit/Synästhesie/
  kambrische Explosion/Erkältungsmythen/Darwin/mündliche Prüfungen.
- 306+307 (11, 08d06de): Verbpräfixe/Slang/Gehirn/Sprache&Gesellschaft/Metakognition/
  Bewältigung/Land der Blinden/Präsentation/DevOps (10 Sätze)/Essay/kreatives Schreiben.
  3067R: em-Titel umformuliert (nie als Chip), 3069X mit 10 Sätzen.
- 308 (5, f0a7c3f): Kulturgeschichte (10)/Nominalstil/Merz-Bilanz (10)/Passiv/
  Politik&Geistesgeschichte (3085V mit satzbauData). 3086S ohne satzbauData ausgenommen.
Alle Patcher-Läufe flag-frei, verify/check_wortbank/check_serif grün.
JSDOM-Stichprobe Familie B (3082G/3084G/3061G) grün.
- 900er-Block (8 Dateien, 55 Sätze, Commit 2199679): 9011G Nominalstil/9013R
  Sense-Memory/9021G subj. Modalverben/9031G Sonderstellung/9041G Verbpräfixe/
  9051G Genitiv-Verben/9061G Modalpartikeln/9071G Kommasetzung. Grammatik-Kern
  je Satz erhalten, Gedankenstriche durch Komma-Nebensätze ersetzt (kein —-Chip).
  JSDOM Familie B (9061G/9031G/9051G) grün.

## C1 KOMPLETT (2026-06-10) — Gerüst-Rollout abgeschlossen
**Alle 162 satzbau-tragenden C1-Dateien fertig** (Einheiten 101–106, 201–207,
301–308, 900er-Block; von 164 HTML-Dateien gesamt), rund 1000 Sätze auf 12–18W
mit Nebensatz + Komma-Chip, geführter Modus überall. triage über das ganze C1-Repo
meldet 0 defiziente Sätze. Ohne Gerüst bleiben bewusst:
- DE_C1_3086S-diskussion-bilanz-geistesgeschichte.html (kein satzbauData, Diskussions-S)
- DE_C1_7001V-reiseleitung-urlauberpsychologie.html (kein satzbauData)
Diese brauchen kein Wortstellungs-Training — korrekt so.

## Erledigt (2026-06-10, Session 7) — Berufs-/Privatschüler-Dateien
- **schueler/ (B2-Root-Repo, Commit ae7b351):** ir/DE_B1_7011V-energiewelt (5 Sätze,
  12–14), ir/DE_C1_7010V-investor-relations (7 Sätze, 12–18, Finanzzahlen wörtlich
  aus Bestand übernommen), privat-1/DE_B1_DEVOPS-opencultur-fehler (8, 12–14),
  privat-1/Komposita-FVG (7, 12–16, FVG-Kern erhalten). 27 Sätze gesamt.
- **htmlS/Architektur (eigenes Repo, Commit d183f07):** Bauprojektarten (10),
  Kap08-Bauelemente (8), Kap09-Baustoffe (8), Kap10-Haustechnik (8) — 34 Sätze,
  konservativ B1-Staffel 12–14 (kein Niveau-Marker in den Dateien), Fachwortschatz-
  Kern erhalten. Alle Checks + JSDOM grün.
- privat-omar/ ist leer, Vertragssprache.html/Geschaeftsemail.html ohne satzbauData.

## Erledigt (2026-06-10, Session 7b) — daf-materialien + HOTFIX Erstlade-Bug
**daf-materialien (Commit 2054c17):** konnektoren-kausal-konsekutiv (B1, 12–14,
Ziel-Konnektor je Satz erhalten), modalsaetze-instrumental-komparativ +
modalsaetze-restriktiv-substitutiv (B2, 12–16, Modalstruktur erhalten),
DE_B2_Chinas-Aufstieg + DE_B2_Eskalationsfalle-Iran (12–16, Aussagen am
Textkontext verifiziert) — 46 Sätze. NICHT gepatcht (A-Niveau, außerhalb
B1+-Rollout): adjdekl-nom-akk-familie, partizip2-bildung-100verben, alle 9
Mattmüller-Lückentexte („ich komme aus Deutschland"-Niveau).

**HOTFIX Erstlade-Bug (Frank-Fund an 1062G im Live-Unterricht):** Die Add-on-
Schlussprobe `rowEl(0) || bankEl(0)` + `children.length` schlug fehl, wenn das
native Init die Row LEER lässt (Free-Build) — Gerüst erschien erst nach Klick
auf „Neustart", nie beim Erstladen. JSDOM-Test kaschierte das, weil er
initSatzbau() selbst aufruft. Fix in geruest_patch.js: Probe prüft Row ODER
Bank auf Kinder. **Alle 485 Add-on-Dateien re-gepatcht + committed:**
B2-Root+schueler 143 (88d0043), B1.1 100 (535ab0f), C1 162 (3d23cb4),
C2 71 (e0b4d4c), Architektur 4 (cffc753), daf-materialien 5 (2054c17).
Erstlade-Pfad ohne initSatzbau-Aufruf in allen Familien JSDOM-verifiziert.
Lehre: Browser-Test = Seite laden und Satzbau-Tab SOFORT ansehen, nicht
erst nach Neustart; JSDOM-Test um Erstlade-Pfad ergänzen.

**ZWEITER FUND (gleiche Session): stille Push-Rejects seit 2026-06-01.**
Frank hatte am 1.6. per GitHub-Web-Upload den Mirror-Workflow in mehrere
Repos eingespielt → jeder lokale Push danach non-fast-forward-rejected.
safe-commit.sh verschluckte das (`|| true`) und setzte die lokale
origin/main-Ref selbst → jede HEAD==origin/main-Prüfung war zirkulär.
Betroffen: C1, Architektur, Lückentexte, daf-materialien, daf-archiv —
der GESAMTE C1-Rollout war bis 14:00 nur lokal. Behoben durch Merge-Commits
(`git commit-tree HEAD^{tree} -p HEAD -p <remote>`, lokale Workflow-Version
behalten, sie ist die neuere nicht-destruktive). safe-commit.sh verifiziert
seit d94f80f jeden Push per `git ls-remote` und bricht sonst ab.
Alle 9 Repos per GitHub-API gegen lokalen HEAD abgeglichen: synchron.

## KORREKTUR (2026-06-10, Session 8): „KOMPLETT" war zu früh — Detektions-Blindfleck

Alle bisherigen Vollständigkeits-Zählungen (Patcher, triage, „141 patchbar")
keyten auf `satzbauData`. Dateien mit Satzbau in ANDEREN Datenfamilien waren
für die gesamte Werkzeugkette unsichtbar — Frank fand das live an
DE_B2_3061X (B2.3 E6 „Mein Berufsweg", `var SATZBAU`, 7–11-Wort-Sätze ohne
Komma-Chip, lowercase-Chips).

**Erledigt Session 8:**
- 3061X komplett migriert (Typ B → kanonisches Skill-Pattern, 9 Sätze neu
  12–16W mit Nebensatz + Komma-Chip, check-satzbau-migration ✓, Patcher 9/9
  flag-frei, JSDOM Erstlade-/Drag-/Lösen-/Neustart-Pfad grün).
- **Patcher-Fix:** suspectVerb erkannte Präfix-Präterita nicht (bekam,
  begann, entstand, verließ, übernahm …) → Präfix-Stamm-Check ergänzt,
  `gann`/`nommen` in AUX. Bestand-Audit fand 33 Verb-Anker in 30 bereits
  gepatchten Dateien → alle 30 re-gepatcht (B2 7, B1.1 3, C1 20), Audit
  jetzt 0 über alle 489 gepatchten Dateien.

**Stand nach Session 8b (2026-06-10 nachmittags):**
- ERLEDIGT: 3054X–3057X, 3061X–3065G (Sessions 8a/8b parallel), 3025G
  (sbData→kanonisch, Konnektor-Kern erhalten, sb-label für Prompts),
  NDEKL-PSYCHO (SATZBAU_DATA→satzbauData, N-Dekl-Formen NIE als Anker —
  Zielform gehört in die Bank; 3 Alt-Quote-Fixes). Anker-Audit 0/499.
- GEHIRN 01X–06R: migriert von Parallel-Session, dort noch uncommitted —
  NICHT doppelt anfassen, Commit der anderen Session abwarten.
- B1.1 49 Dateien mit DRITTER Familie `const SATZBAU_DATA` (words:-Schema,
  eigene Klick-Reihen-UI) trotz „101/101 komplett" — Migrationsaufwand prüfen.
- htmlS/A2.1/DE_B2_Eskalationsfalle-Iran.html: NIRGENDS verlinkt, Dashboard
  zeigt nur auf die gepatchte daf-materialien-Version → parallele Arbeitskopie,
  Lösch-/Archiv-Kandidat (Frank entscheidet).
- Vollständigkeits-Checks künftig auf ALLE Familien-Marker keyen:
  `satzbauData` | `var SATZBAU` | `SATZBAU_DATA` | `sbData`.
- Fachregel NEU: In Grammatik-Dateien darf die ZIELFORM des Grammatik-Themas
  nie Anker sein (N-Dekl-Nomen, Ziel-Konnektoren je nach Übungsfokus prüfen).

## Erledigt (2026-06-11, Session 9) — Vollständigkeits-Scan über ALLE Repos + Schnellfälle

**Scan mit allen FÜNF Markern** (`satzbauData` | `var SATZBAU` | `sbData` |
`SATZBAU_DATA` | `SB_DATA`) über alle Repos außer A1/A2/daf-archiv:
**520 Dateien OK** (Add-on + geführter Modus + Erstlade-Fix), 0 alte Add-ons,
0 ohne Erstlade-Fix. GEHIRN 01X–06R: von der Parallel-Session committed (1fc0885),
Remote synchron.

**Schnellfälle erledigt (alle 4 live verlinkt bzw. im Dashboard):**
- `ir/DE_C1_7010V` — gepatchten Stand aus schueler/ir an den Live-Link-Pfad
  übernommen. **Lehre:** Session 7 hatte die schueler/ir-KOPIEN gepatcht, aber
  `BASIS + 'ir/…'` im Lehrer-Dashboard zeigt auf das Root-`ir/`. Root = Wahrheit;
  schueler/ir aufgelöst (archiviert in `daf-archiv/Altkopien-2026-06-11/`).
- `ir/DE_C1_7011R` — 6 Sätze auf C1 12–18W + Nebensatz/Komma, gepatcht (Familie A).
- `ir/DE_B1_7011V-energiewelt` — aus schueler/ir an den Live-Link-Pfad geholt.
- `omar-wco01x-pilot.html` — 8 Sätze auf B2 12–16W + Nebensatz/Komma, gepatcht.
- `htmlS/C1/DE_C1_7001V-reiseleitung` — hatte SEHR WOHL Satzbau (`SB_DATA` mit
  valid; frühere „kein satzbauData"-Notiz war der Marker-Blindfleck). SB_DATA→
  satzbauData, sbInit→initSatzbau, 6 Sätze auf C1-Norm verlängert, gepatcht.
- Alle 5: Syntax-, SBGAP-/Anker-Invarianz-, Quote-, JSDOM-Erstlade-Test grün
  (JSDOM braucht `url:`-Option, sonst stirbt initTimers an localStorage —
  Test-Artefakt, kein Datei-Bug).
- Altkopien archiviert + aus Repos entfernt: `nominalisierung-verbalisierung-b2.html`
  (B2-Root, kanonisch ist GEHIRN_05G) und `htmlS/A2.1/DE_B2_Eskalationsfalle-Iran.html`.
- Entwarnung: `rahaf-sprachbausteine-akzent.html` nutzt `SB_DATA` für
  Multiple-Choice-Sprachbausteine, KEIN Satzbau — braucht kein Gerüst.

## B1.1-Fremdfamilien KOMPLETT (2026-06-11, Session 9b) — GERÜST-ROLLOUT ABGESCHLOSSEN

**Alle 55 Fremdfamilien-Dateien migriert** (6 Batches, je: Inhalt 12–14W mit
Nebensatz + Komma → kanonisches Pattern aus 2046R-Template gespliced →
geruest_patch.js → Syntax/SBGAP/Anker-Invarianz/Quote/JSDOM-Erstlade →
check_wortbank/check_serif → safe-commit). Die 56. Datei
(B1_werden_Tabelle) war ein nie funktionsfähiges Fragment ohne `<body>` →
archiviert in daf-archiv/Altkopien-2026-06-11/.
**Abschluss-Scan: 578 Dateien mit geführtem Gerüst + Erstlade-Fix + caps:true,
0 offen** (außer dokumentierte Ausnahmen: 1047X Satzglieder, Mattmüller +
daf-materialien A-Niveau, rahaf = MC ohne Satzbau).

**Werkzeuge Session 9b** (in /outputs der Session, Muster reproduzierbar):
sb_migrate.py (Brace-balanciertes Excisen der Altfunktionen + Splice von
Daten + 2046R-Template mit Timer-Guards und sb-label-Support),
fix_anchors.py (Zielform/Verb-Anker → '_' + Bank), verify_batch.sh.

**Zielform-nie-Anker durchgesetzt** (Bann-Listen pro G-Datei): indirekte
Fragewörter (2042G), Kausal-/Konsekutiv-Konnektoren (2047X/3014X),
Passiversatz (2045G), Partizip I (3015G), FVG-Nomen (3052G),
Reziprokpronomen (3055G), Komparativ/als/am (3062G), deklinierte
Adjektive (3065G), Nullartikel-Nomen (2015G), zu/um/ohne/statt
(2035G/3012G/komplementsatz), dass/ob/wie (2065G).

**Nebenbefunde gefixt (alle schon in HEAD kaputt):**
- Kommentar-verschlucktes `return chip;` in 6 Dateien (1026R/1033R
  sbMakeChip, 3014X/3017X/3021X/3024X makeGenusChip) — Init-Kette live tot.
- 2061X: vocabGrid-IIFE ohne Element killte Block 0 (alle Tabs tot).
- B1_werden_Tabelle: fehlendes `</style><script>` — JS wurde als CSS geparst.
- 3071W/3072W: Alt-Bridge `var satzbauData=[]` überschrieb Daten nach Splice.
- ~20 Quote-Altlasten (ASCII-Schließer) in 2013R/2016R/2063R/2066R.
- suspectVerb-Lücke: 1.-Person-Formen auf -e (komme/bleibe/besuche/spare/
  verstehe/beherrsche/anpries) werden NICHT erkannt → bei künftigen Patches
  Anker-Review gegen Satz-Verben fahren (fix_anchors-Muster).

**Letzter Schritt (offen):** geruest_patch.js + Session-8/9-Erkenntnisse in
den daf-satzbau-Skill übernehmen (Skill-Update via skill-verwaltung, nicht
aus Cowork heraus möglich).
