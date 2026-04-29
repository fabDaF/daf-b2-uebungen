# Übergabe — Schreibwerkstatt-Rollout (A2 / B1 / B2)

> **Hallo, nächster Claude.** Frank arbeitet seit der Session vom 2026-04-28 daran,
> einen **Schreibwerkstatt-Tab** in jede thematische Lektion seines DaF-Materials
> einzubauen. **A1 ist komplett (47 Dateien)**. Du sollst jetzt A2, B1 und B2
> abarbeiten — exakt nach dem etablierten Pattern, ohne kreative Abweichungen.
>
> Lies dieses Dokument einmal komplett, dann ist du arbeitsfähig.

---

## TL;DR (für Eilige)

1. Es gibt ein fertiges Skript: **`scripts/add-schreibwerkstatt.py`**.
2. Du musst die `CONFIGS`-Dict im Skript um die Lektionen des nächsten Niveaus erweitern.
3. Skalierung pro Niveau ist in der Tabelle weiter unten — **nur die Konstanten `SCHREIB_MIN_CHARS` (= Mindestzeichen) und die Aufgaben (Wortanzahl/Komplexität) ändern sich pro Niveau.**
4. Das Skript ist generisch (Regex-Detection für Wortschatz-Tab, drei Init-Marker-Fallbacks). Es funktioniert für R, X und C-Dateien.
5. Pro Datei: 5 Mikroaufgaben mit Beispiel, lektionsspezifisch. Keine generischen Aufgaben verwenden — jede Aufgabe muss thematisch an den Lesetext / die Lektion gebunden sein.
6. Workflow pro Datei: Inhalt sichten → 5 Aufgaben designen → Config in Skript → Skript laufen lassen → JSDOM-Test → `safe-commit.sh`.
7. **Frank ist DaF-Lehrer, nicht Software-Entwickler.** Direkte Antworten in Prosa, keine Bullet-Wüsten, keine Präambeln. Push-Notification senden, wenn auf seinen Input gewartet werden muss.

---

## Was ist die Schreibwerkstatt? (Hintergrund)

Frank stellte 2026-04-28 fest: produktives Schreiben ist die größte Schwachstelle
im Online-Unterricht. Lerner überspringen große Schreibaufgaben — die psychologische
Hürde ist zu hoch. Der C2-Pilot 0708R hatte bereits ein Pattern etabliert, das
funktioniert: **fünf Mikroaufgaben statt einer großen**, jede mit eigenem
Sendebutton an Frank, formsubmit.co als Endpoint, LocalStorage zur Persistenz.

Frank entschied am 2026-04-28: das Pattern wird auf **A1, A2, B1, B2** ausgeweitet,
in **R-, X- und C-Dateien** (nicht in V/G/Drills). A1 ist vollständig durch.

---

## Was ist FERTIG

**A1 — alle 47 thematischen Dateien** im Repo `daf-a1-uebungen` (lokal:
`htmlS/A1.1 NEW/`):

| Typ | Dateien |
|---|---|
| R (Lesetexte) | 12 — 1014R, 1024R, 1034R, 1044R, 1054R, 1064R, 2014R, 2024R, 2034R, 2044R, 2054R, 2064R |
| X (Textarbeit) | 17 — 1012X, 1022X, 1032X, 1042X, 1052X, 1062X, 1072X, 1082X, 1092X, 1102X, 1112X, 1122X, 2013X, 2023X, 2033X, 2043X, 2053X |
| C (Kann-Beschreibungen) | 18 — 1014C bis 1131C (12 in A1.1) plus 2014C bis 2054C (5 in A1.2) plus 1131C |

**Nicht behandelt** (und sollen es auch nicht werden):
- V-Dateien (Vokabular)
- G-Dateien (Grammatik)
- FDxx-Dateien (Drills)
- `*-uebungen.html`-Pendants zu X- und C-Dateien (sind Drill-Pendants)

**Frank-spezifische Korrekturen, die im Pattern eingearbeitet sind:**
- Name-Eingabe ist **PFLICHT** (nicht optional) und steht **OBEN** vor der ersten Aufgabe (orange-gelbe Box `.schreib-name-box`).
- Send-Button validiert den Namen: leer → Shake-Animation, Fokus, Status-Hinweis.
- Button-Text ist **„📨 An Frank senden"** (NICHT „Diese Antwort senden" — Wiederholung war Frank zu viel).
- Sammelbutton bleibt: „📨 Alle noch nicht gesendeten Antworten schicken".

---

## Was du JETZT zu tun hast

**Reihenfolge ist verbindlich**, von Frank am 2026-04-28 explizit bestätigt:

1. **A2** — Repo `daf-a2-uebungen`, lokal `htmlS/A2.1/`. Geschätzt ~50 Dateien.
2. **B1** — Repo `daf-b1-uebungen`, lokal `htmlS/B1.1/`. Geschätzt ~50 Dateien.
3. **B2** — Repo `daf-b2-uebungen`, lokal `.` (Root des Projekts).

C1 und C2 haben bereits Schreibwerkstatt-Tabs (waren der Pilot), werden hier nicht
mehr berührt.

**Wann der Skill `daf-schreibwerkstatt` angelegt wird:**
Frank hatte gesagt „sobald drei Pilots stehen". A1 hat 47 Pilots. Du KÖNNTEST den
Skill jetzt anlegen — aber praktischer ist, ihn **nach der A2-Etappe** zu schreiben,
weil sich dort die Niveau-Skalierung erstmals zeigt und das Pattern dadurch
vollständig erprobt ist. Frag Frank, sobald A2 durch ist.

---

## Niveau-Skalierung (verbindlich)

| Niveau | Wörter pro Aufgabe | Min-Zeichen | Aufgabencharakter |
|---|---|---|---|
| **A1** (✅ fertig) | 1–15 | 5 | Geführt, Beispiel-orientiert: Sätze nach Muster, Liste, Mini-Dialog |
| **A2** | 10–30 | 8 | Postkarte, Tagesablauf, einfache E-Mail, kurze Beschreibung |
| **B1** | 30–50 | 12 | Erfahrung schildern, Meinung mit "weil", kurze Stellungnahme, Erzählung |
| **B2** | 50–70 | 14 | Argumentation, Pro/Contra, formell vs. informell, Mini-Essay |
| C1 | 40–80 | 15 | (bereits etabliert — nicht ändern) |
| C2 | 40–80 | 15 | (bereits etabliert — nicht ändern) |

**Wichtige Konstante im Skript: `SCHREIB_MIN_CHARS`.** Aktuell hartcodiert auf
`5` (für A1). Für A2/B1/B2 musst du diese Konstante parametrisieren — entweder
über die Config oder über einen Niveau-Parameter beim Skript-Aufruf.

Ich empfehle: Skript um Parameter `--niveau A2` erweitern, der drei Konstanten
setzt: `SCHREIB_MIN_CHARS`, den Niveau-Prefix in den LocalStorage-Keys
(`schreibwerkstatt_A2_…` statt `schreibwerkstatt_A1_…`) und den Niveau-String
in `SCHREIB_LEKTION` (`A2 – Lektion …`).

---

## Das Skript: `scripts/add-schreibwerkstatt.py`

### Was es macht

Pro Datei wird in einer Transaktion:

1. Wortschatz-Nav-Button-Position via Regex erkannt → der Schreiben-Button
   übernimmt diesen Index, Wortschatz rückt um eins.
2. CSS-Block (Schreibwerkstatt-Styles) vor `</style>` eingefügt.
3. Section-Block (Hilfebox, Name-Pflicht-Box, 5 Karten, Action-Buttons) vor dem
   Wortschatz-Section-Kommentar eingefügt.
4. `initSchreibwerkstatt()`-Aufruf in den Init-Block eingefügt (drei Marker-Fallbacks:
   `loadBestTimes`, `initWortschatz`, `initVocab`).
5. JS-Block (Init, Send-Logik, LocalStorage-Persistenz) vor `</script>` eingefügt.

**Idempotenz:** Wenn die Datei schon einen Schreibwerkstatt-Tab hat, wird sie
übersprungen (`SKIP …`).

### Konfiguration

In der `CONFIGS`-Dict — pro Lektion ein Eintrag:

```python
'2014R': {
    'lesson_code': '2014R',
    'lesson_title': 'Alex, der Schriftsteller',
    'banner_url': 'https://images.pexels.com/photos/733856/...',
    'banner_alt': 'Notizbuch und Stift, bereit zum Schreiben',
    'intro': 'Fünf kleine Schreibaufgaben rund um „Alex, der Schriftsteller".',
    'tasks': [
        {'titel': '...', 'frage': '...', 'beispiel': '...'},
        # genau 5 Einträge!
    ]
}
```

**Banner-URL:** Ich habe für alle A1-Schreibwerkstatt-Tabs das gleiche Pexels-Bild
verwendet (`733856` — Notizbuch mit Stift). Das schafft visuelle Konsistenz für
den Schreibwerkstatt-Tab über alle Lektionen. Du kannst das beibehalten oder pro
Niveau eine andere ID nehmen — aber **niemals doppelt verifizierte Pexels-IDs**
(Memory-Hinweis: jede Pexels-ID vor Commit per Chrome-MCP prüfen — bei
Beibehaltung der `733856` ist das schon erledigt).

### Aufruf

```bash
python3 scripts/add-schreibwerkstatt.py "htmlS/A2.1" 1014R 1024R 1034R …
```

Das erste Argument ist der Pfad zum Niveau-Ordner relativ zum fabDaF-Root.
Danach die Lektionscodes. Das Skript findet die Datei über
`DE_<NIVEAU>_<CODE>-*.html` (Pattern `DE_A1_…`).

**ACHTUNG:** Die Skript-File-Discovery ist aktuell auf `DE_A1_` fest verdrahtet
(siehe `glob(f"DE_A1_{code}-*.html")` und ähnlich). Das musst du für A2 anpassen.

---

## Workflow pro Datei

Erst der konzeptionelle Teil (kann nicht automatisiert werden), dann der
mechanische Teil (vollautomatisch):

### Schritt 1 — Inhalt sichten

Die Datei hat eine sehr lange Base64-Zeile (Bilder), die das Lesen erschwert.
Vorgehen: per Subagent Inhalt extrahieren (Lesetext, Title, Vokabular) — der
Subagent kann mit `Read offset/limit` durch die Datei navigieren.

Alternativ Python-snippet für die wichtigsten Strukturen:

```bash
python3 -c "
import re
with open('FILE.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()
for i, line in enumerate(lines, 1):
    if 'data:image' in line and len(line) > 5000:
        continue
    for pat in ['nav-btn\"', 'Wortschatz', '<!-- =====', '<h1>']:
        if re.search(pat, line):
            print(f'{i}: {line[:170].rstrip()}')
            break
"
```

### Schritt 2 — 5 Aufgaben designen

Diese Schritt ist der eigentliche didaktische Wert. Jede Aufgabe MUSS:

- thematisch an den Lesetext / die Lektion gebunden sein,
- in der Niveau-Skalierungs-Tabelle (oben) liegen,
- ein Beispiel als Anker enthalten (Format: `Beispiel: „..."`),
- eine eigene `titel` haben (kurz, prägnant — wird zum Mail-Subject),
- in der Reihenfolge variieren (nicht 5x „Schreib eine Beobachtung").

Bewährte Aufgabentypen:
1. **Persönlicher Bezug** (Stell dich vor / Deine Familie / Dein Beruf)
2. **Beobachtung / Beschreibung** (Wie ist X bei dir? Was machst du oft?)
3. **Eine Frage formulieren** (Frage an einen Charakter aus dem Lesetext)
4. **Eine Liste / Aufzählung** (3–5 Sachen)
5. **Mini-Dialog** (2 Fragen + 2 Antworten — beste Aufgabe für gesprächs-orientierten Output)

Auf höheren Niveaus (B1+) ersetze die Liste durch:
- **Vergleich/Übertragung** (Gibt es das in deiner Sprachgemeinschaft auch?)
- **Mikro-Stellungnahme** (3 Sätze pro/contra)

### Schritt 3 — Config in Skript

`CONFIGS`-Dict in `scripts/add-schreibwerkstatt.py` erweitern. Eintrag siehe
oben. Die A1-Configs (47 Stück) sind dort als Vorlage.

### Schritt 4 — Skript laufen lassen

```bash
cd /Users/frankburkert/Cowork/Projekte/fabDaF
python3 scripts/add-schreibwerkstatt.py "htmlS/A2.1" 1014R 1024R …
```

Erwartete Ausgabe: `OK   DE_A2_…html (Schreiben=N, Wortschatz=N+1)`. Falls
`FAIL`: das Skript meldet, welcher Marker fehlte. Häufige Ursachen siehe
„Stolperstellen" weiter unten.

### Schritt 5 — JSDOM-Test

Vor jedem Commit Pflicht:

```bash
NODE_PATH=/tmp/jsdom-install/lib/node_modules node -e "
const { JSDOM } = require('jsdom');
const fs = require('fs');
const files = ['DE_A2_1014R-….html', '…'];
for (const file of files) {
  const html = fs.readFileSync(file,'utf8');
  class LS { constructor(){this.s={}} getItem(k){return this.s[k]||null} setItem(k,v){this.s[k]=String(v)} removeItem(k){delete this.s[k]} clear(){this.s={}} }
  const dom = new JSDOM(html, { runScripts:'outside-only', pretendToBeVisual:true });
  const w = dom.window;
  Object.defineProperty(w,'localStorage',{value:new LS(),configurable:true});
  let lastFetch=null;
  w.fetch=(u,o)=>{lastFetch={u,o};return Promise.resolve({ok:true,json:()=>Promise.resolve({})})};
  w.confirm=()=>true;
  const m = html.match(/<script>([\\s\\S]*?)<\\/script>/);
  try { w.eval(m[1]); } catch(e) { console.log('✗ '+file+' JS:', e.message); continue; }
  const d = w.document;
  const karten = d.querySelectorAll('.schreib-aufgabe-karte').length === 5;
  const btnOk = d.querySelector('.schreib-mini-btn')?.textContent.trim() === '📨 An Frank senden';
  // Send-Test ohne Name → blockiert
  const ta = d.querySelector('.schreib-mini-textarea[data-aufgabe=\"1\"]');
  ta.value='Test mit genug Zeichen.';
  ta.dispatchEvent(new w.Event('input',{bubbles:true}));
  lastFetch=null; w.schreibSendenEinzeln(1);
  const guard = !lastFetch;
  // Mit Name → gesendet
  d.getElementById('sw-name').value='Maria';
  d.getElementById('sw-name').dispatchEvent(new w.Event('input',{bubbles:true}));
  w.schreibSendenEinzeln(1);
  console.log(((karten && btnOk && guard && lastFetch)?'✓':'✗')+' '+file);
}
"
```

JSDOM ist installiert unter `/tmp/jsdom-install/lib/node_modules/`. Falls fehlend:
`npm install -g jsdom --prefix /tmp/jsdom-install`.

### Schritt 6 — Commit + Push

**NIEMALS direkt `git commit` aufrufen** — Sandbox-Locks killen das. Stattdessen
das Wrapper-Skript:

```bash
cd "htmlS/A2.1"
bash ../../scripts/safe-commit.sh "feat(A2): Schreibwerkstatt 1014R-1064R" \
  DE_A2_1014R-….html DE_A2_1024R-….html …
```

Das Skript umgeht die `.git/index.lock`-Sandbox-Restriktion durch alt-Index-Plumbing
und pusht automatisch. Fehler-Output mit `tmp_obj_*` ist kosmetisch, ignorieren.

Bei erstmaligem Push aus Cowork-Session:
```bash
bash scripts/setup-sandbox-credentials.sh
```

---

## Verbindliche Regeln (NICHT verhandelbar)

1. **Name-Eingabe ist Pflicht und oben.** Niemals optional, niemals unten.
2. **Button-Text:** „📨 An Frank senden" (Karten) bzw. „📨 Alle noch nicht gesendeten Antworten schicken" (Sammel).
3. **Wortschatz bleibt letzter Tab.** Schreibwerkstatt ist VORLETZTER Tab.
4. **5 Mikroaufgaben.** Nicht 4, nicht 6. Genau 5.
5. **Jede Aufgabe hat ein Beispiel** (Format: `Beispiel: „..."`).
6. **Aufgaben sind lektionsspezifisch.** Generische Aufgaben sind verboten — wenn du dasselbe Aufgabenset für mehrere Lektionen verwenden würdest, hast du die Aufgaben falsch designt.
7. **Endpoint:** `https://formsubmit.co/ajax/unterricht@fabdaf.onmicrosoft.com` (NICHT die Primäradresse, niemals `frankburkert@gmx.net` o.ä. — siehe CLAUDE.md zur E-Mail-Alias-Rotation).
8. **Pflicht-LocalStorage-Keys:** `schreibwerkstatt_<NIVEAU>_<CODE>_…` — Niveau-Prefix wichtig wegen Cross-Lesson-Isolation.
9. **Anführungszeichen:** öffnend `„` (U+201E), schließend `"` (U+201C). Niemals ASCII `"`.
10. **Vor jedem Commit JSDOM-Test.** Ohne Test kein Commit.

---

## Bekannte Stolperstellen

### A) Pre-existing JS-Bugs in alten Dateien

Manche Dateien haben Tippfehler aus früheren Edits, die JSDOM beim Test aufdeckt.
Beispiel: `2024R` hatte einen 3-zeiligen JS-String (genus-cat-innerHTML), der die
Datei lahmlegte. **Wenn du beim JSDOM-Test einen JS-Eval-Error bekommst**:
suche den Bug, repariere ihn. Mein Reparatur-Skript für 2024R war:

```python
python3 -c "
with open('DE_A2_2024R-….html') as f: lines = f.readlines()
# Problem: lines 916-918 wurden mit Newlines getrennt (kein gültiges JS)
# Lösung: zu einer Zeile zusammenfassen
fix = lines[916].rstrip('\n') + lines[917].rstrip('\n') + lines[918]
lines[916] = fix
del lines[917:919]
with open('DE_A2_2024R-….html', 'w') as f: f.writelines(lines)
"
```

Solche Bugs entstehen durch frühere copy-paste-Operationen. Nicht alle Dateien
betroffen — nur einige. Im Zweifel: Datei reparieren UND in Memory dokumentieren.

### B) Skript-Marker werden nicht gefunden

Das Skript nutzt drei Init-Marker-Fallbacks (`loadBestTimes`, `initWortschatz`,
`initVocab`). Wenn keiner passt, Skript meldet `FAIL — kein bekannter Init-Marker`.
Lösung: ergänze den Fallback im Skript. Schau in der Datei, wie der Init-Block
am Ende des `<script>` aussieht.

### C) Datei-Glob mehrdeutig

Falls `glob(f"DE_A2_{code}-*.html")` mehrere Treffer liefert (z.B. `DE_A2_1042X-uebungen.html`
und `DE_A2_1042X-zahlen.html`), wird das Skript abbrechen. Das Skript schließt
`-uebungen.html` schon aus — falls es noch andere Dubletten gibt, Filter erweitern.

### D) Dashboard-Bug

`htmlS/dashboard.html` enthält ein KURSE-Array. Frank hatte am 2026-04-28 einen
JS-Syntaxfehler dort (escaped Apostroph in einem Tag-String) — das ganze Dashboard
wurde leer. **Vor jedem Dashboard-Commit Node-Syntaxcheck** (siehe Memory
`feedback_dashboard-js-syntaxcheck.md`):

```bash
node -e "
const fs=require('fs'),vm=require('vm');
const m=/<script(?![^>]*src=)[^>]*>([\\s\\S]*?)<\\/script>/.exec(fs.readFileSync('htmlS/dashboard.html','utf8'));
try{vm.compileFunction(m[1]);console.log('OK');}catch(e){console.log('ERROR:',e.message);process.exit(1);}
"
```

### E) Sandbox-Auth + Stale-Locks

Falls `safe-commit.sh` mit „cannot lock ref" oder Auth-Failure abbricht:

```bash
bash scripts/setup-sandbox-credentials.sh
```

Falls eine `.git/index.lock` vorhanden ist und Lockfehler erzeugt: das Skript
umgeht das via `GIT_INDEX_FILE=/tmp/idx-$$` — solange du `safe-commit.sh` nutzt
und nicht direkt `git commit`, hast du das Problem nicht.

---

## Kontextarbeit — Frank's Stil

Aus den Memory-Hinweisen:

- **Frank ist DaF-Lehrer, nicht Software-Entwickler.** Direkte Antworten in Prosa, keine Bullet-Wüsten, keine Präambeln. Selbstreflexion und dialektisches Denken sind willkommen.
- **Push-Notification senden, wenn auf Frank's Input gewartet wird.** ntfy-Topic ist in den User-Preferences hinterlegt. Memory-Skill `push-benachrichtigung` für Details.
- **Niemals Subagent für DaF-Datei-Edits.** Subagents nur für Lese-Aufgaben (Inhaltsextraktion, Code-Suche), niemals für eigentliche Änderungen.
- **Bei „nächste"-Aufträgen** (z.B. „mach jetzt B1.1 1014R"): einfach die Reihe weitermachen, nicht nachfragen.
- **Git-Plumbing immer lautlos.** Keine SHA-Berichte im Chat, keine Erwähnung des `safe-commit.sh`-Verfahrens. Frank will Ergebnisse sehen, nicht Prozess.

---

## Skill `daf-schreibwerkstatt` anlegen — wann

Frank hatte gesagt: „sobald 3 Pilots stehen". A1 hat 47 Pilots. Du KÖNNTEST den
Skill jetzt schon schreiben — aber praktischer ist nach A2, weil sich dort die
Niveau-Skalierung erstmals zeigt.

**Wenn du den Skill schreibst:**
- Skill-Verzeichnis: `~/.claude/plugins/anthropic-skills/daf-schreibwerkstatt/SKILL.md`
- Pflicht-Trigger-Worte: „Schreibwerkstatt", „Schreibtab", „Mikroaufgaben", „Mailversand", „An Frank senden"
- Verweise auf `daf-c2` (für C2-Pattern) und `daf-kern` (Layout)
- Skalierungstabelle aus diesem Doc übernehmen
- Workflow-Anleitung aus diesem Doc übernehmen

Beim Anlegen Skill `skill-verwaltung` lesen für Format/Naming/Verpacken.

---

## Beispiel-Befehle (copy-paste-fertig)

**A2 starten** (sobald Konfigs ergänzt):

```bash
cd /Users/frankburkert/Cowork/Projekte/fabDaF
python3 scripts/add-schreibwerkstatt.py "htmlS/A2.1" 1014R 1024R 1034R 1044R 1054R 1064R
```

**Tests laufen lassen:**

```bash
cd "htmlS/A2.1"
NODE_PATH=/tmp/jsdom-install/lib/node_modules node -e "..."  # siehe Workflow Schritt 5
```

**Commit + Push:**

```bash
cd "htmlS/A2.1"
bash ../../scripts/safe-commit.sh "feat(A2): Schreibwerkstatt 1014R-1064R" DE_A2_*.html
```

**Skript-Repo separat committen** (das Skript lebt im B2-Root-Repo):

```bash
cd /Users/frankburkert/Cowork/Projekte/fabDaF
bash scripts/safe-commit.sh "feat(scripts): A2-Konfigs ergänzt" scripts/add-schreibwerkstatt.py
```

**Push-Notification senden** (wenn Etappe fertig):

```bash
curl -s -H "Title: A2 Schreibwerkstatt fertig" -H "Priority: default" -H "Tags: bell" \
  -d "X von Y A2-Dateien live — siehe Chat." \
  https://ntfy.sh/frank-claude-c46edad954
```

---

## Reihenfolge-Empfehlung für A2

Wenn du chronologisch durchgehst (so wie ich's bei A1 gemacht habe):

1. **A2-R-Dateien zuerst.** Schau ins Verzeichnis `htmlS/A2.1/`, liste alle `DE_A2_*R-*.html` (ohne `-uebungen.html`-Pendants). Das werden vermutlich 10-12 sein. Pro Datei Inhalt extrahieren, 5 Aufgaben mit A2-Skalierung designen, Config in Skript.
2. **A2-X-Dateien danach.**
3. **A2-C-Dateien danach.**
4. **Skript-Anpassung:** Vor dem A2-Lauf musst du das Skript anpassen (siehe „Niveau-Skalierung" oben — Konstante `SCHREIB_MIN_CHARS` und Niveau-Prefix in LocalStorage-Keys).

---

## Was du zur Sicherheit prüfen solltest, bevor du anfängst

```bash
cd /Users/frankburkert/Cowork/Projekte/fabDaF
ls htmlS/A2.1/ | head -20                 # struktur sehen
git log --oneline | head -10              # was ist gerade frisch
./scripts/verify_manifest.sh              # Manifest grün?
```

Falls das verify-Skript rot ist: NICHT drüberbauen — erst klären, was driftet.
Memory-Hinweis dazu: `reference_fabdaf-manifest.md`.

---

## Wenn du blockiert bist

- **Frank's Input nötig** (z.B. Aufgaben-Designentscheidung, Skill-Frage): Push-Notification senden, dann im Chat eine `AskUserQuestion` mit 2-3 konkreten Optionen stellen.
- **Skript versagt**: Logs lesen, fehlenden Marker im Skript ergänzen, dokumentieren.
- **JSDOM-Test rot**: Prüf, ob Pre-existing-Bug oder eigener Fehler. Pre-existing reparieren, eigener: Skript-Diff prüfen.
- **Git-Lock**: `safe-commit.sh` benutzen — nie direkt `git commit`.

Viel Erfolg. Frank ist ein dankbarer Lehrer-Auftraggeber, der gut geschriebenes
DaF-Material wertschätzt. Lieber langsam und richtig als schnell und schlampig.
