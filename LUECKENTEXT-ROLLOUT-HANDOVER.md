# Lückentext-Rollout — Übergabe an den nächsten Thread

Stand: 2026-06-30. Dieser Thread wurde sehr lang; hier ist alles, um **nahtlos
weiterzumachen**. Reihenfolge: B1 zuerst, schematisch der Liste nach, **echte Stories**.

## 1. Worum es geht (1 Absatz)

Jeder Lückentext-Tab wird zur **kanonischen Story-Form** gebracht: eine zusammenhängende
**Geschichte** mit Lücken (keine Einzelsätze, keine Nummern), **Serifenschrift** inkl.
Eingabefelder, §7-Wortbank (gemischt, nicht klickbar, `.used`-Durchstreichen),
case-sensitiv, kein Prüfen-Button, **genau 10 Lücken**. Zwei Varianten erkennt die Engine
selbst: **Wortschatz** (Lücke = `data-answer`) und **Grammatik** (zusätzlich
`data-base` = Grundform, Zielform nie sichtbar). Die ganze Disziplin (Regel + ein
Produzent + ein Gate) ist gebaut und bewährt; jetzt läuft der **redaktionelle Rollout**.

## 2. Quelle der Wahrheit (lesen, nicht neu erfinden)

- **Skill `daf-lueckentext`** — die Form + der Workflow + Story-Definition (installiert).
- **CLAUDE.md** (Repo-Root), Abschnitt „Lückentext ist IMMER eine kanonische Story".
- **`LUECKENTEXT-PLAN.md`** — der Gesamtplan/Phasen.
- **Memory:** `project_lueckentext-kanonisierung-2026-06-30`,
  `feedback_lueckentext-story-schreibqualitaet` (Story-Standard + Umbau-Recipe),
  `feedback_keine-nummerierung-lueckentext`.

## 3. DER STORY-STANDARD (das Wichtigste — Frank hat hier zweimal nachjustiert)

Eine Story ist **kein Sachtext / keine Themen-Aufzählung.** „Flüssig zusammenhängend"
genügt NICHT. Verbindlich: **Figur + konkrete Szene + Ereignis/Wendung** — es passiert
etwas, idealerweise mit Pointe. Auch abstrakte Themen (Umwelt, Globalisierung) werden
**durch das Erleben einer Figur** erzählt, nie als Aufsatz. „So originell wie möglich,
**ohne dich zu zerreißen**" (keine erzwungene Künstelei). Das Karim-Universum (Karim,
sein Onkel Hassan in Casablanca, Kollegen Stefan/Petra/Hiroshi) ist ein gutes Reservoir,
aber nicht Pflicht. **Das Gate kann Story-Qualität NICHT prüfen — das ist deine
redaktionelle Verantwortung.** (Gegenbeispiel, das Frank zu Recht stoppte: 1021X war
zuerst „Der Treibhauseffekt erwärmt die Erde. Auch die Abholzung …" = Aufzählung. Jetzt:
Mara hält nervös einen Vortrag, die Fragen ihres Bruders helfen ihr, am Ende eine Pointe.)

## 4. Tooling (eine Quelle, im B2-Root-Repo `scripts/`)

- `scripts/lt-story-engine.js` — die Engine (variantenerkennend). Nie pro Datei kopieren.
- `scripts/lt-story.css` — die CSS.
- `scripts/inject_lt.py DATEI` — Produzent: entfernt graue Alt-Engine `FB-WORTBANK-MODULE`
  UND `FB-LT-V1` automatisch, spielt CSS+Engine+Timer-Hooks idempotent ein (erkennt
  `<div>`- UND `<button>`-Nav, Timer-Index aus der Nav).
- `scripts/check_lueckentext.py [DATEI]` — Gate (+ Inventur). Muss ✓ sein vor Commit.

## 5. Recipe pro Backlog-Lektion (bewährt an 13 Lektionen)

1. **Recon** (eine Datei): `nav` (Lückentext-Tab-Index), Container-ID (variiert:
   `lueckenContainer` / `lueckeContainer` / `luecke-container`), Button-onclick-Namen
   (`showLueckeLoesung`/`showLueckenLoesung`, `resetLuecke`/`resetLuecken`),
   Wortbank-Markup (label+`#wortbank-luecken` ODER `#wordBank.word-bank` ODER `.wortkasten`
   ODER nichts), Daten-Array (`LUECKEN`/`LUECKEN_DATA`, Felder `blank/answer/segs/b`),
   Alt-Engines (`FB-WORTBANK-MODULE`/`FB-LT-V1`). Achtung: lange Banner-`data:`-Zeilen
   sprengen Reads — mit `grep`/`awk … substr` arbeiten, nie blind die ganze Datei lesen.
2. **Story schreiben** (10 Lücken, Vokabeln/Thema aus dem alten Daten-Array; Story-Standard!).
   Wortschatz: `<input class="blank" data-answer="WORT">`. Grammatik: zusätzlich
   `data-base="GRUNDFORM"`. Deutsche Anführungszeichen „…" in Dialogen.
   Adverbien/positionssensible Wörter möglichst **mittig** setzen (Großschreibung am
   Satzanfang verrät sonst die Position).
3. **Ersetzen mit Backup** (`cp DATEI /tmp/x.bak`) per Python, **NUR Exakt-String-Anker**
   (kein DOTALL über unbekannten Inhalt — hat zweimal fremde Tabs zerfetzt, beide Male per
   Span-/Byte-Check abgefangen): container-verankert (`ci=s.find(container)`), den
   davorliegenden Wortbank-Block (`wortbank-label`/`wortkasten`/`wordBank`) bis Container-Ende
   durch **[eine `<div class="wortbank" id="wortbank-luecken"></div>` + Story-`<div
   id="lueckenContainer" class="luecken-story">…</div>`]** ersetzen. Asserts: genau **1**
   `id="wortbank-luecken"` und genau **10** Lücken.
4. **Buttons** onclick exakt auf `fbLtShowLoesung()` / `fbLtReset()` repointen.
5. **Alt-Funktionen** per early-return neutralisieren (Namen variieren: `buildLuecke(n)`,
   `initLuecken`, `lueckeInit`, `initWortbank`, `buildWordBank`) — sonst Crash/Doppel-Render
   auf entfernte Container.
6. `python3 scripts/inject_lt.py DATEI` → `python3 scripts/check_lueckentext.py DATEI` (muss ✓).
7. **JS-Parse** (node --check je `<script>`) + **Browser-Stichprobe** via Control_Chrome
   (Lückentext-Tab klicken, 1 Lücke richtig/falsch, `wb===1`, `chips===10`).
   ⚠️ `execute_javascript` läuft **isoliert** — `typeof window.fbLt…` ist dort immer
   `undefined` (Mess-Artefakt!); funktional über DOM prüfen (Klassen `.correct/.wrong`,
   Timer-Tick).
8. **Commit** (siehe §6). Browser-Tabs am Turn-Ende aufräumen (RAM), echte User-Tabs
   (Pexels/Outlook) NIE anfassen.

## 6. Commit-Workflow (kritisch — B1-Repo hat verschmutzten Worktree!)

- Einmal pro Session: `bash scripts/setup-sandbox-credentials.sh` (aus B2-Root).
- B1-Repo = `htmlS/B1.1` (eigenes Repo, **stark verschmutzter Index** aus Parallel-Session
  → **NIE `git add -A`**, nur benannte Dateien). Commit:
  `bash /sessions/…/mnt/fabDaF/scripts/safe-commit.sh "msg" DATEI1 [DATEI2 …]`
  (aus `htmlS/B1.1` aufgerufen; safe-commit nutzt Alt-Index, ignoriert den Schmutz).
- Tooling-Änderungen in `scripts/` → B2-Root-Repo (aus `fabDaF/`).
- Verifizieren: `git rev-parse HEAD origin/main` (gleich = ok). Post-commit-Hook pusht selbst.

## 7. Stand (28 fertig, B1.1)

ERLEDIGT: 1011X, 1013R, 1015G, 1016R, 1017X, 1018S, 1021X, 1026R, 1027X, 1034X, 1037X,
1057X, 3065G. (1057X/3065G/1011X waren von Anfang an echte Stories; 1015G/1016R/1017X/
1018S/1021X wurden von Sachtext zu Story **umgeschrieben**.)

ERLEDIGT 2026-06-30 (Folge-Thread, 10 Stück, jede mit Browser-Stichprobe + Push verifiziert):
1032G (Lokaladverbien — Maras Umzugstag), 1035G (Infinitivkonstr. haben/sein zu —
Hausmeisterin, **Grammatik-Variante** mit data-base), 1036R (Deutsche Traditionen —
Karims erstes Jahr), 1038S (Kulturelle Vielfalt — Karims Einbürgerung), 1041X (Privatsphäre
— Yaras erstes Profil, 8→10 Vokabeln ergänzt), 1042G (Pronomen — Lenas Paket, Wortschatz-
Variante), 1043R (Partnersuche — Stefans Online-Date, 12→10), 1044X (Online einkaufen —
Opa Werner), 1045G (Negation — Robert im Stromausfall, Wortschatz-Variante), 1046R (Fake
News — Karims Faktencheck-Team, anderer Container `luecken-container`), 1053R (Kulturelle
Angebote — Karims Freizeit-Wochenenden, 6→10 Vokabeln aus Vorentlastung ergänzt), 1055G
(Infinitiv mit zu — Ninas Pläne nach dem Studium, **Grammatik-Variante** mit data-base),
1056R (Leben auf dem Land — Markus zieht aufs Land, 7→10), 1061X (Historische Ereignisse —
Opa Friedrichs Fotoalbum, Inline-`<ul id="lueckenList">`-Format, 8→10), 1062G (Verb lassen
— Mamas Familienfest, **Grammatik-Variante** mit einheitlicher data-base="lassen": die Engine
dedupliziert die Grundform zu EINEM „lassen"-Chip, Zielform produziert der Lerner — sauber).
Merke 1: G-Dateiname ≠ Grammatik-Variante!
Merke 2: Manche Dateien haben eine SEPARATE `buildWordBank()`-Funktion (nicht nur
FB-WORTBANK-MODULE) — die muss auch per early-return neutralisiert werden, sonst meldet das
Gate „aktive Alt-Wortbank … Leak in die Story". In der Recon nach `buildWordBank` greppen. Variante ist **inhaltsgetrieben** (nur echte
Transformation wie 1035G bekommt data-base; Lokaladverbien/Pronomen/Negation = Wortschatz).

## 8. Backlog (117 in B1.1) — Reihenfolge & nächste Schritte

Aktuelle Liste jederzeit neu erzeugen (aus `htmlS/B1.1`):
```bash
for f in $(ls DE_B1_*.html | sort); do
  grep -qE 'nav-label[^>]*>\s*L(ü|&uuml;)ckentext' "$f" && ! grep -q 'FB-LT-STORY' "$f" && echo "$f"
done
```
**Nächste reguläre dran:** 1063R, 1064X, 1065G, 1066R, 1067X … dann 20xx/30xx.
(1032G–1046R, 1053R, 1055G, 1056R, 1061X, 1062G sind ab 2026-06-30 erledigt, siehe §7.)
(1071W/1072W/2071W/… sind **W = Schreibaufgaben** — prüfen, ob sie überhaupt einen
Lückentext-Tab haben; viele tun das nicht und sind dann gar nicht im Backlog.)

## 9. Sonderfälle (GEPARKT — nicht vergessen, brauchen eigenes Konzept)

- **1022G — zweiteilige Präpositionen:** Antworten teils zweiteilig („Von … aus",
  „Auf … hin") → passt nicht ins Eine-Lücke-Modell. Lösung: entweder nur einteilige
  Präpositionen als Lücken, oder zweiteilige als EINE Lücke mit Wort dazwischen neu denken.
- **1025G — Inline-Format:** Lücken stehen als HTML inline im Container (kein JS-Array),
  evtl. verschachtelte `.luecken-item`-divs → Container-Replace braucht sauberes
  Matching der schließenden `</div>`.
- **1031X / 1037X-Klasse — sehr abstrakte/akademische Begriffe** (Wir-Identität, Ethnie,
  Wirtschaftsprozesse, Megatrends …): Story ohne Künstelei ist schwer. 1037X ging über
  Onkel Hassans Werkstatt; für 1031X braucht es einen ähnlich konkreten Rahmen (z. B.
  Einbürgerungs-Szene). Im Zweifel mit Frank kurz abstimmen.

## 10. Offene größere Punkte (nach dem B1-Rollout)

- **Bruchstücke herauslösen** aus `daf-kern §7` / `daf-uebungsformen` / `daf-grammatik`
  und auf `daf-lueckentext` verweisen (Cleanup; Parallel-Session arbeitet evtl. an diesen
  Skills → koordinieren, auf Basis der jeweils neuesten Version).
- Pilot-Inline-Engines von 1057X/3065G auf die zentrale Engine vereinheitlichen (kleiner
  Drift; optional).
- Weitere Niveaus (A1/A2/B2/C1/C2) nach B1 — gleiche Recipe.
