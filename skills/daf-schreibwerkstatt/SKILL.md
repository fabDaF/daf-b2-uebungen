---
name: daf-schreibwerkstatt
description: >
  Verbindliches Pattern für den Schreibwerkstatt-Tab in DaF-HTML-Lektionen
  (R, X, C — nicht V, G, FDxx). Definiert: 5 Mikroaufgaben statt einer großen
  Schreibaufgabe, Name als Pflichtfeld oben, Button-Text „📨 An Frank senden",
  formsubmit-Mailversand, LocalStorage-Persistenz, Niveau-Skalierung A1–C2.
  Verwende diesen Skill IMMER wenn ein Schreibtab erstellt, geprüft oder
  migriert werden soll. Auch bei „Schreibwerkstatt", „Schreibtab",
  „Mikroaufgaben", „An Frank senden", „formsubmit", „Schreibaufgabe
  kleinteilig", „Mailversand an Frank", „sec-schreib", „schreibSendenEinzeln",
  „SCHREIB_MIN_CHARS", „Niveau-Skalierung Schreibtab", „Schreibtab einbauen",
  „Schreibwerkstatt-Pattern", „A1/A2/B1/B2-Schreibtab", „Lerner schreiben
  lassen", „produktives Schreiben üben", „Schreibtab-Rollout".
---

# DaF-Schreibwerkstatt — Verbindliches Pattern

**Pflicht-Skills:** Vor dem Anlegen eines Schreibtabs immer **daf-kern** lesen (Layout, Container, Footer). Bei C2-Lektionen ergänzend **daf-c2** lesen.

**Pilot-Goldstandard:** `https://fabdaf.github.io/daf-b2-uebungen/htmlS/C2/DE_C2_0708R-jugendsprache.html`

---

## 1. WARUM Schreibwerkstatt

Frank stellte fest: produktives Schreiben ist die größte Schwachstelle im Online-Unterricht. Lerner überspringen große Schreibaufgaben — die psychologische Hürde ist zu hoch. Der C2-Pilot 0708R hat das Pattern etabliert, das funktioniert: **fünf Mikroaufgaben statt einer großen**, jede mit eigenem Sendebutton an Frank, formsubmit.co als Endpoint, LocalStorage zur Persistenz.

**Reichweite:** R-, X-, C-Dateien aller Niveaus von A1 bis C2. Nicht in V (Vokabular), G (Grammatik) oder FDxx (Drills) einbauen.

---

## 2. NIVEAU-SKALIERUNG (verbindlich)

| Niveau | Wörter pro Aufgabe | `SCHREIB_MIN_CHARS` | Aufgabencharakter |
|---|---|---|---|
| **A1** | 1–15  | 5  | Geführt, Beispiel-orientiert: Sätze nach Muster, Liste, Mini-Dialog |
| **A2** | 10–30 | 8  | Postkarte, Tagesablauf, einfache E-Mail, kurze Beschreibung |
| **B1** | 30–50 | 12 | Erfahrung schildern, Meinung mit „weil", kurze Stellungnahme, Erzählung |
| **B2** | 50–70 | 14 | Argumentation, Pro/Contra, formell vs. informell, Mini-Essay |
| **C1** | 40–80 | 15 | Stellungnahme, Vergleich, kohärente Argumentation |
| **C2** | 40–80 | 15 | Essayistische Hypotaxe, fachspezifische Wendungen, Nominalstil |

Die Skalierung wird im Skript automatisch über `--niveau` gesetzt.

---

## 3. STRUKTUR — Genau 5 Mikroaufgaben

**Niemals** vier oder sechs. Genau **fünf**. Jede Aufgabe hat:

* **`titel`** — kurz, prägnant; wird zum Mail-Subject
* **`frage`** — klare Anweisung mit Wortzahl-Hinweis
* **`beispiel`** — Format `Beispiel: „..."` als Anker

**Bewährte Aufgabentypen** (Reihenfolge variieren!):

1. **Persönlicher Bezug** — Stell dich vor / Deine Familie / Dein Beruf
2. **Beobachtung / Beschreibung** — Wie ist X bei dir? Was machst du oft?
3. **Eine Frage formulieren** — an einen Charakter aus dem Lesetext
4. **Eine Liste / Aufzählung** (A1/A2) ODER **Vergleich** (B1+) ODER **Mikro-Stellungnahme** (B2+)
5. **Mini-Dialog** — 2 Fragen + 2 Antworten (beste Aufgabe für gesprächs-orientierten Output)

**Lektionsspezifisch.** Wenn du dasselbe Aufgabenset für mehrere Lektionen verwenden würdest, hast du falsch designt. Bind jede Aufgabe an Lesetext / Lektionsthema.

---

## 4. UI-PATTERN — Verbindlich, nicht verhandelbar

* **Name-Eingabe ist PFLICHT** (orange-gelbe Box `.schreib-name-box`) und steht **OBEN** vor der ersten Aufgabe — niemals optional, niemals unten.
* **Send-Button-Text** je Karte: **„📨 An Frank senden"** (NICHT „Diese Antwort senden" — Wiederholung war Frank zu viel).
* **Sammelbutton-Text** unten: **„📨 Alle noch nicht gesendeten Antworten schicken"**.
* **Send-Button validiert Name:** leer → Shake-Animation, Fokus, Status-Hinweis pro Karte.
* **Wortschatz bleibt LETZTER Tab.** Schreibwerkstatt ist VORLETZTER Tab. Ausnahme: Datei hat keinen Wortschatz-Tab oder Wortschatz steht nicht am Ende — dann wird Schreibwerkstatt LETZTER Tab.
* **Anführungszeichen** im Beispiel: öffnend `„` (U+201E), schließend `"` (U+201C). Niemals ASCII `"`.

---

## 5. TECHNIK — formsubmit + LocalStorage

* **Endpoint:** `https://formsubmit.co/ajax/unterricht@fabdaf.onmicrosoft.com` (ALIAS — nicht Franks Primäradresse, niemals `frankburkert@…` hardcoden; siehe `CLAUDE.md` zur Alias-Rotation).
* **Subject-Format:** `<NIVEAU> <CODE> · Aufgabe N · <Titel> · <Name>` für Einzelversand; `<NIVEAU> <CODE> · N Antworten · <Name>` für Sammelversand.
* **LocalStorage-Keys:**
  * `schreibwerkstatt_<NIVEAU>_<CODE>_name` — Name persistent
  * `schreibwerkstatt_<NIVEAU>_<CODE>_<N>` — Antworttext pro Aufgabe
  * `schreibwerkstatt_<NIVEAU>_<CODE>_sent_<N>` — Sende-Marker pro Aufgabe
* **Niveau-Prefix Pflicht** — sonst überschreiben sich Antworten zwischen Niveaus.

---

## 6. WORKFLOW — Wie ein neuer Schreibtab eingebaut wird

### Werkzeuge

`scripts/add-schreibwerkstatt-v2.py` (im fabDaF-B2-Repo) ist der Patcher. Er erkennt automatisch:

* Nav-Struktur: `<div>`/`<button>` × `showSection`/`showTab`/`switchTab`/`zeigeSec` × `data-section`
* Section-IDs: `sec-N`, `secN`, `tab-N`, `tabN`
* Wortschatz-Position (last → INSERT before; otherwise → APPEND)

Konfigs liegen pro Niveau in `scripts/configs_<niveau>.py` (z. B. `configs_a2.py`).

### Pro Datei

1. **Inhalt sichten** — Lesetext oder Lektionsthema lesen.
2. **5 Aufgaben designen** — niveau-skaliert, lektionsgebunden, mit Beispiel.
3. **Config in `configs_<niveau>.py` ergänzen** — Lektionscode als Schlüssel.
4. **Patcher laufen lassen:**
   ```bash
   python3 scripts/add-schreibwerkstatt-v2.py --niveau A2 --basis "htmlS/A2.1" 1014R 1024R …
   ```
5. **JSDOM-Test** (Pflicht vor Commit) — verifiziert: 5 Karten, Button-Text, Name-Validierung, fetch-Aufruf nach Ausfüllen.
6. **Commit + Push** mit `scripts/safe-commit.sh` (Sandbox-sicher).

### JSDOM-Test-Schablone

```js
NODE_PATH=/tmp/jsdom-install/lib/node_modules node -e "
const { JSDOM } = require('jsdom');
const fs = require('fs');
const file = 'DE_<NIVEAU>_<CODE>-...html';
const html = fs.readFileSync(file,'utf8');
class LS { constructor(){this.s={}} getItem(k){return this.s[k]||null} setItem(k,v){this.s[k]=String(v)} removeItem(k){delete this.s[k]} clear(){this.s={}} }
const dom = new JSDOM(html, { runScripts:'outside-only', pretendToBeVisual:true });
const w = dom.window;
Object.defineProperty(w,'localStorage',{value:new LS(),configurable:true});
let lastFetch=null;
w.fetch=(u,o)=>{lastFetch={u,o};return Promise.resolve({ok:true,json:()=>Promise.resolve({})})};
w.confirm=()=>true;
const scripts = Array.from(html.matchAll(/<script>([\\s\\S]*?)<\\/script>/g));
const all = scripts.map(m=>m[1]).join('\\n');
w.eval(all);
const d = w.document;
console.log('cards:', d.querySelectorAll('.schreib-aufgabe-karte').length === 5 ? '✓' : '✗');
const btn = d.querySelector('.schreib-mini-btn');
console.log('btn-text:', btn && btn.textContent.trim() === '📨 An Frank senden' ? '✓' : '✗');
console.log('sec:', d.getElementById('sec-schreib') ? '✓' : '✗');
const ta = d.querySelector('.schreib-mini-textarea[data-aufgabe=\"1\"]');
ta.value='Test mit genug Zeichen.';
ta.dispatchEvent(new w.Event('input',{bubbles:true}));
lastFetch=null;
w.schreibSendenEinzeln(1);
console.log('blocked-without-name:', !lastFetch ? '✓' : '✗');
d.getElementById('sw-name').value='Maria';
d.getElementById('sw-name').dispatchEvent(new w.Event('input',{bubbles:true}));
w.schreibSendenEinzeln(1);
console.log('sent-with-name:', lastFetch ? '✓' : '✗');
"
```

---

## 7. STOLPERSTELLEN — was bisher Zeit gekostet hat

* **Pre-existing JS-Bugs.** Manche Dateien haben Tippfehler aus früheren Edits (z. B. `timerReset(4)` statt `timerReset(timers.ws)`, oder ein orphan `);` mitten im Skript). JSDOM deckt das auf. Vor Schreibwerkstatt-Patch reparieren — sonst läuft `init()` nicht durch und `initSchreibwerkstatt()` wird nie erreicht.
* **Doppelte `</script>`/`</body>` am Dateiende.** Einzelne A2-Dateien hatten zwei abschließende Tag-Sequenzen. `rfind('</script>')` injiziert dann in den falschen Bereich (außerhalb des Parser-aktiven Scripts). Datei vorher konsolidieren.
* **Niveau-Prefix vergessen.** Ohne `schreibwerkstatt_<NIVEAU>_…` kollidieren LocalStorage-Keys zwischen Lektionen verschiedener Niveaus.
* **Generische Aufgaben.** Wenn Aufgaben nicht lektionsgebunden sind, springt Frank zurecht. Lieber zehn Minuten extra für Inhalt investieren.
* **Wortschatz nicht mehr letzter.** Wenn der Patcher die Section in den falschen Slot einfügt, ist die Tab-Reihenfolge kaputt. Patcher v2 prüft das automatisch — bei manueller Edition aufpassen.

---

## 8. NACH DEM EINBAU — Audit & Push

* **`daf-audit`-Skill** danach laufen lassen — er prüft Ladung der Pflicht-Skills, Layout-Konformität und Pattern-Verletzungen.
* **Immer pushen** (Memory `feedback_immer-pushen.md`). Schreibwerkstatt nutzt nur dann etwas, wenn die Datei live ist.
* **Memory aktualisieren** wenn ein neuer Niveau-Block fertig ist (z. B. `project_a2_komplett.md`).

---

## 9. SCHNELLREFERENZ — Niveau-Aufgaben

**A1-Beispiel** (1–15 Wörter):
> *„Schreib deinen Namen und Nachnamen, jeden Buchstaben einzeln, getrennt durch Bindestriche. Beispiel: M-A-R-I-A   L-O-P-E-Z."*

**A2-Beispiel** (10–30 Wörter):
> *„Wie ist deine Wohnung? Beschreib sie in zwei oder drei Sätzen: Größe, Stockwerk, hell oder dunkel. Beispiel: „Ich wohne in einer Drei-Zimmer-Wohnung im zweiten Stock. Sie ist hell und hat einen kleinen Balkon."*

**B1-Beispiel** (30–50 Wörter):
> *„Erzähle von einer Reise, die dich verändert hat. Was hast du dort erlebt? Warum hat sie dich verändert?"*

**B2-Beispiel** (50–70 Wörter):
> *„Soll Home-Office Pflicht für Bürojobs werden? Gib zwei Argumente dafür und zwei dagegen. Schließe mit deiner Position ab."*

**C2-Beispiel** (40–80 Wörter, essayistisch):
> *„Reflektieren Sie in einem konzentrierten Absatz die These, dass Jugendsprache ein Indikator soziolinguistischer Dynamik darstellt. Verwenden Sie mindestens zwei Hypotaxen."*

---

## 10. DATEIEN, AN DENEN SICH ALLES ENTSCHEIDET

* **Patcher:** `~/Cowork/Projekte/fabDaF/scripts/add-schreibwerkstatt-v2.py` (universell, niveau-parameterisiert).
* **Konfigurationen:** `~/Cowork/Projekte/fabDaF/scripts/configs_<niveau>.py`.
* **Sandbox-Setup:** `~/Cowork/Projekte/fabDaF/scripts/setup-sandbox-credentials.sh` — vor erstem Push aus einer neuen Cowork-Session.
* **Commit-Wrapper:** `~/Cowork/Projekte/fabDaF/scripts/safe-commit.sh` — umgeht `.git/index.lock`-Sandbox-Restriktion.
* **JSDOM:** vorinstalliert unter `/tmp/jsdom-install/lib/node_modules/`. Falls fehlend: `npm install -g jsdom --prefix /tmp/jsdom-install`.

---

**Kurz:** 5 Mikroaufgaben. Niveau-skaliert. Name oben pflicht. Button „📨 An Frank senden". formsubmit zum Alias. JSDOM-getestet vor Commit. Wortschatz bleibt letzter Tab.
