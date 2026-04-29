---
name: daf-schreibwerkstatt
description: >
  Verbindliches Pattern für den Schreibwerkstatt-Tab in DaF-HTML-Lektionen
  (R, X, C — nicht V, G, FDxx). Definiert: 5 Mikroaufgaben statt einer
  großen Schreibaufgabe, Name als Pflichtfeld oben, Button „📨 An Frank
  senden", Web3Forms-Mailversand mit body.success-Check, Customer-Success-
  Error-UX (📧/📋/🔄), LocalStorage-Persistenz, Niveau-Skalierung A1–C2.
  Verwende diesen Skill IMMER wenn ein Schreibtab erstellt, geprüft oder
  migriert wird, ODER wenn ein Versand-Problem (stille Fehler, Aktivierung,
  Mailto-Fallback, Sponsor-Block) zu lösen ist. Auch bei „Schreibwerkstatt",
  „Schreibtab", „Mikroaufgaben", „An Frank senden", „Web3Forms",
  „formsubmit", „body.success", „NOT_ACTIVATED", „schreibZeigeFehler",
  „Customer-Success-Error", „Versand-Fehler-UI", „Schreibtab-Rollout",
  „stille Failures", „access_key", „Sponsor-Block", „Mailto-Fallback".
---

# DaF-Schreibwerkstatt — Verbindliches Pattern

**Pflicht-Skills:** Vor dem Anlegen eines Schreibtabs immer **daf-kern** lesen (Layout, Container, Footer). Bei C2-Lektionen ergänzend **daf-c2** lesen.

**Pilot-Goldstandard:** `https://fabdaf.github.io/daf-b2-uebungen/htmlS/C2/DE_C2_0708R-jugendsprache.html`

---

## 1. WARUM Schreibwerkstatt

Frank stellte fest: produktives Schreiben ist die größte Schwachstelle im Online-Unterricht. Lerner überspringen große Schreibaufgaben — die psychologische Hürde ist zu hoch. Der C2-Pilot 0708R hat das Pattern etabliert, das funktioniert: **fünf Mikroaufgaben statt einer großen**, jede mit eigenem Sendebutton an Frank, **Web3Forms** als Endpoint (seit 2026-04-29; vorher formsubmit.co), LocalStorage zur Persistenz, Customer-Success-Error-UX im Fehlerfall.

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

## 5. TECHNIK — Web3Forms + LocalStorage + Customer-Success-Error-UX

**Stand seit 2026-04-29:** Versand wurde von formsubmit.co auf **Web3Forms** umgestellt — Auslöser war ein Supergau-Vorfall, bei dem die formsubmit-Aktivierungsmail untergegangen war (stille Failures, Karten als „gesendet" markiert, aber keine Mails kamen an), zusätzlich nervte der Sponsor-Werbeblock in jeder Mail. Web3Forms im Free-Tier hat keinen Sponsor-Block.

### Endpoint und Body-Schema

```js
var FORMSUBMIT_ENDPOINT  = 'https://api.web3forms.com/submit';
var FORMSUBMIT_ACCESS_KEY = 'e96ea83f-67e2-4fff-81df-76fee86a09ff';
var FORMSUBMIT_MAILTO    = 'unterricht@fabdaf.onmicrosoft.com';
```

Body: `{ access_key, name, subject, from_name: 'fabDaF Schreibwerkstatt', lektion, message }`. **KEINE** formsubmit-Felder mehr (`_subject`, `_template`, `_captcha` sind weg).

### Verpflichtende Sicherheitschecks

1. **`r.ok`-Check** — HTTP-Status muss 2xx sein. Wenn nicht → `throw new Error('HTTP_' + r.status)`.
2. **`body.success`-Check** — NACH `r.json()` muss geprüft werden, ob `data.success === true || data.success === 'true'`. Sonst HTTP-200-mit-failure-Body wird als Erfolg interpretiert. Beispiel-Code:

```js
.then(function (r) { if (!r.ok) throw new Error('HTTP_' + r.status); return r.json(); })
.then(function (data) {
  var ok = data && (data.success === true || data.success === 'true');
  if (!ok) {
    var code = 'API_ERROR'; var apiMsg = (data && data.message) || '';
    if (/[Aa]ctivat|domain|access[\s_-]?key/.test(apiMsg)) code = 'NOT_ACTIVATED';
    var err = new Error(code); err.apiMessage = apiMsg; throw err;
  }
  onOk(data);
})
.catch(onErr);
```

3. **`sent_N`-Marker erst bei bestätigtem Erfolg setzen.** Niemals im `try`-Block oder vor dem body-Check.

### Customer-Success-Error-UX (Pflicht in jeder Datei)

Bei JEDEM Fehler im Versand erscheint ein `.schreib-fb`-Block mit:

* **Titel:** „⚠ Online-Versand hat nicht geklappt — dein Text ist sicher im Browser gespeichert."
* **Erklärung:** Kontextspezifischer Text aus `schreibFehlerErklaerung(err)` — abhängig vom Fehlercode (`NOT_ACTIVATED`, `HTTP_*`, `API_ERROR`, sonst Netzfehler).
* **Drei Aktionspfade als Buttons:**
  * `📧 In Mail-Programm öffnen` — Mailto-Link mit vorausgefülltem Empfänger, Betreff, Body.
  * `📋 In Zwischenablage` — kopiert Lektion + Name + Text.
  * `🔄 Nochmal versuchen` — ruft `schreibSendenEinzeln(nr)` neu auf.
* **Hilfe-Hinweis:** „Wenn nichts klappt: sag Frank im Unterricht Bescheid — er muss den Versand auf seiner Seite einmal aktivieren."

Helper-Funktionen verpflichtend in jeder Datei: `schreibFehlerErklaerung`, `schreibKopierenEinzeln`, `schreibZeigeFehler` (per-Karte), `schreibZeigeFehlerSammel` (Sammel-Versand). CSS-Klassen: `.schreib-fb`, `.schreib-fb-titel`, `.schreib-fb-text`, `.schreib-fb-actions`, `.schreib-fb-btn`, `.schreib-fb-btn-prim`, `.schreib-fb-hilfe`.

Vollständiger Reference-Code: `outputs/patch_schreib_web3forms.py` (Konstanten `NEW_POST_FN`, `HELPER_FNS`, `CSS_BLOCK`).

### Subject- und Storage-Konventionen

* **Subject-Format:** `<NIVEAU> <CODE> · Aufgabe N · <Titel> · <Name>` für Einzelversand; `<NIVEAU> <CODE> · N Antworten · <Name>` für Sammelversand.
* **LocalStorage-Keys:**
  * `schreibwerkstatt_<NIVEAU>_<CODE>_name` — Name persistent
  * `schreibwerkstatt_<NIVEAU>_<CODE>_<N>` — Antworttext pro Aufgabe
  * `schreibwerkstatt_<NIVEAU>_<CODE>_sent_<N>` — Sende-Marker pro Aufgabe (NUR setzen wenn `data.success === true` bestätigt!)
* **Niveau-Prefix Pflicht** — sonst überschreiben sich Antworten zwischen Niveaus.

### Mailto-Fallback NIE auf Primäradresse

`FORMSUBMIT_MAILTO` ist immer der Alias `unterricht@fabdaf.onmicrosoft.com`. Niemals `FrankBurkert@…` hardcoden — selbst nicht, wenn Quellcode aus älteren C1-Dateien das suggeriert. Memory `feedback_schreibwerkstatt-mail-aus-footer.md` und `reference_schreibwerkstatt-web3forms.md` erzwingen das. Bei Alias-Rotation: im Patcher `MAILTO_FALLBACK` ändern und idempotent re-laufen lassen.

### Access-Key-Rotation

Bei Bedarf neuen Key auf web3forms.com generieren (an `unterricht@fabdaf.onmicrosoft.com` binden), in `outputs/patch_schreib_web3forms.py` Konstante `ACCESS_KEY` aktualisieren, Patcher idempotent über alle 477 Dateien laufen lassen — pro-Datei-Diff ist eine Zeile.

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

Die Schablone testet jetzt sowohl den Erfolgs-Pfad (mock-success) als auch den Fehler-Pfad (mock-needs-activation), weil der `body.success`-Check Pflicht ist und beide Codepfade abgedeckt sein müssen. Vollständige Test-Datei: `outputs/test_patched_jsdom.js`.

```js
NODE_PATH=/tmp/jsdom-install/node_modules node -e "
const { JSDOM } = require('jsdom');
const fs = require('fs');
const file = 'DE_<NIVEAU>_<CODE>-...html';
const html = fs.readFileSync(file,'utf8');
class LS { constructor(){this.s={}} getItem(k){return this.s[k]||null} setItem(k,v){this.s[k]=String(v)} removeItem(k){delete this.s[k]} clear(){this.s={}} }

async function runMode(mode) {
  const dom = new JSDOM(html, { runScripts:'outside-only', pretendToBeVisual:true });
  const w = dom.window;
  Object.defineProperty(w,'localStorage',{value:new LS(),configurable:true});
  let lastBody = null;
  w.fetch = (u, o) => {
    lastBody = o && o.body;
    if (mode === 'success') return Promise.resolve({ok:true, json:() => Promise.resolve({success: true, message: 'OK'})});
    return Promise.resolve({ok:true, json:() => Promise.resolve({success: 'false', message: 'This form needs Activation'})});
  };
  w.confirm = () => true;
  const scripts = Array.from(html.matchAll(/<script[^>]*>([\\s\\S]*?)<\\/script>/g)).map(m => m[1]).join('\\n');
  w.eval(scripts);
  w.document.dispatchEvent(new w.Event('DOMContentLoaded'));
  await new Promise(r => setTimeout(r, 100));
  const d = w.document;
  d.getElementById('sw-name').value = 'Maria';
  d.getElementById('sw-name').dispatchEvent(new w.Event('input', {bubbles:true}));
  const ta = d.querySelector('.schreib-mini-textarea[data-aufgabe=\"1\"]');
  ta.value = 'Genug Zeichen für die Mindestlänge.';
  ta.dispatchEvent(new w.Event('input', {bubbles:true}));
  w.schreibSendenEinzeln(1);
  await new Promise(r => setTimeout(r, 200));
  const st = d.getElementById('sw-status-1') || d.getElementById('status-1');
  return {
    mode,
    bodyHasAccessKey: lastBody && lastBody.includes('e96ea83f'),
    hasFallbackUI: st && st.innerHTML.includes('schreib-fb'),
    sentMarkerSet: !!(Object.keys(w.localStorage.s).find(k => k.includes('_sent_'))),
  };
}

(async () => {
  console.log(await runMode('needs-activation'));  // sollte hasFallbackUI=true, sentMarkerSet=false
  console.log(await runMode('success'));            // sollte hasFallbackUI=false, sentMarkerSet=true
})();
"
```

Erwartete Resultate: bei `needs-activation` muss der Fallback-Block erscheinen UND der `sent_N`-Marker im LocalStorage darf NICHT gesetzt sein (Stille-Failure verhindert). Bei `success` umgekehrt.

---

## 7. STOLPERSTELLEN — was bisher Zeit gekostet hat

* **Pre-existing JS-Bugs.** Manche Dateien haben Tippfehler aus früheren Edits (z. B. `timerReset(4)` statt `timerReset(timers.ws)`, oder ein orphan `);` mitten im Skript). JSDOM deckt das auf. Vor Schreibwerkstatt-Patch reparieren — sonst läuft `init()` nicht durch und `initSchreibwerkstatt()` wird nie erreicht.
* **Doppelte `</script>`/`</body>` am Dateiende.** Einzelne A2-Dateien hatten zwei abschließende Tag-Sequenzen. `rfind('</script>')` injiziert dann in den falschen Bereich (außerhalb des Parser-aktiven Scripts). Datei vorher konsolidieren.
* **Niveau-Prefix vergessen.** Ohne `schreibwerkstatt_<NIVEAU>_…` kollidieren LocalStorage-Keys zwischen Lektionen verschiedener Niveaus.
* **Generische Aufgaben.** Wenn Aufgaben nicht lektionsgebunden sind, springt Frank zurecht. Lieber zehn Minuten extra für Inhalt investieren.
* **Wortschatz nicht mehr letzter.** Wenn der Patcher die Section in den falschen Slot einfügt, ist die Tab-Reihenfolge kaputt. Patcher v2 prüft das automatisch — bei manueller Edition aufpassen.
* **Stille-Failure-Falle (Supergau-Vorfall 2026-04-29).** Wenn der Versand-Endpoint mit HTTP 200 antwortet, aber im Body `success: "false"` steht (Aktivierung fehlt, Quota überschritten, Domain-Mismatch), markierte der alte Code die Karte als „gesendet", obwohl nichts ankam. Kunde war komplett im Dunkeln. Lösung: `body.success`-Check + Customer-Success-Error-UX in jeder Datei. Nie wieder nur `r.ok` allein prüfen.
* **Sponsor-Block-Footer.** formsubmit.co Free-Tier hängt einen Werbe-Footer an jede Mail. Customer-facing nicht akzeptabel. Web3Forms hat das nicht.
* **Pre-existing Quote-Bugs in C2.** 0703S, 0705S, 0707R hatten unbalanced ASCII/curly Anführungszeichen in JSON-ähnlichen Datenstrukturen, die JS-Syntax-Fehler verursachten — die Schreibwerkstatt war komplett tot, Versand unmöglich. Beim Patch-Rollout entdeckt und repariert. Bei Patcher-Failures mit „SyntaxError: Unexpected identifier" zuerst die Datendefinitionen oben in der Datei prüfen.
* **Alias-Drift.** Die 44 C1-Dateien aus Einheit 1 hatten beim ersten Schreibwerkstatt-Rollout noch `FrankBurkert@…` (Primäradresse) im Mailto und im formsubmit-Endpoint hardcoded. Memory `feedback_schreibwerkstatt-mail-aus-footer.md` verbietet das — alle Mailtos müssen auf den aktuellen Alias zeigen. Patcher v3 erzwingt das automatisch.

---

## 8. NACH DEM EINBAU — Audit & Push

* **`daf-audit`-Skill** danach laufen lassen — er prüft Ladung der Pflicht-Skills, Layout-Konformität und Pattern-Verletzungen.
* **Patcher `outputs/patch_schreib_web3forms.py` idempotent drüberlaufen lassen** — stellt sicher, dass Endpoint, body.success-Check, Helper-Funktionen, CSS und Mailto-Alias auf dem aktuellen Stand sind. Idempotent: keine Änderung, wenn nichts zu tun ist.
* **JSDOM-Test im needs-activation- UND success-Modus** (siehe Schablone in §6) — beide Codepfade müssen die erwartete UI zeigen.
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

**Kurz:** 5 Mikroaufgaben. Niveau-skaliert. Name oben pflicht. Button „📨 An Frank senden". Web3Forms-Endpoint mit body.success-Check. Customer-Success-Error-UX (📧/📋/🔄). Mailto-Fallback auf aktuellen Alias. JSDOM-getestet vor Commit (needs-activation- UND success-Modus). Wortschatz bleibt letzter Tab.
