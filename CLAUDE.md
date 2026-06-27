# fabDaF — Projekt-Instruktionen für Claude

Diese Datei wird automatisch geladen, wenn eine Claude-Session im
fabDaF-Ordner arbeitet. Sie enthält die verbindlichen Spielregeln für
dieses Projekt. Bei Widersprüchen zwischen dieser Datei und allgemeinen
Gewohnheiten gilt diese Datei.

## Was ist fabDaF?

Deutsch-als-Fremdsprache-Projekt von Frank Burkert. Unterrichtsmaterialien
und interaktive HTML-Übungen für die Niveaus A1 bis C1. Das Projekt ist
auf neun Git-Repos verteilt, die im `MANIFEST.yaml` am Root vollständig
dokumentiert sind.

## Erste Maßnahme bei jeder strukturellen Arbeit

**Bevor** du an der Repo-Struktur, am Dashboard, an Ordner-Layouts oder
an mehreren Niveaus gleichzeitig arbeitest:

```bash
./scripts/verify_manifest.sh
```

Wenn das Skript nicht grün ist, zuerst klären, warum — nicht
drüberbauen. Jeder Fehler dort ist ein Signal, dass die IST-Welt nicht
mehr zur SOLL-Welt passt.

Bei rein inhaltlichen Arbeiten an einer einzelnen HTML-Datei (typischer
DaF-Lektion) ist das nicht nötig.

## Die Grundregeln dieses Projekts

Diese Regeln sind maschinenlesbar in `MANIFEST.yaml` unter `rules:`
definiert. Hier ist die menschliche Fassung:

**Ein Niveau, ein Repo.** Für A1, A2, B1, B2, C1 existiert je genau ein
aktives Repo. Niemals parallele Versionen wie "A2.1" und "A2.2" oder
"B1.2 NEU". Wer so etwas braucht, nutzt Git-Branches oder legt den
Ordner im `daf-archiv` ab.

**Keine parallelen Arbeitskopien.** Kein "Kopie", kein "Entwurf", kein
"OLD" auf derselben Ebene. Genau diese Parallelität hat am 2026-04-10
eine mehrstündige Konsolidierung nötig gemacht.

**Das Archiv ist eingefroren.** `daf-archiv` darf erweitert, aber nicht
verändert werden. Inhalte dort sind historisch.

**Dashboards zeigen nur auf Manifest-Repos.** Jede `basis:`-URL in
einem `dashboard.html` muss auf ein Repo zeigen, das im Manifest
gelistet ist. Tote Links sind Fehler, keine Platzhalter.

**Keine Secrets in committeten Dateien.** Remote-URLs im Manifest und
in Dokumentation enthalten nie PATs. Seit 2026-04-27 sind auch die
`.git/config`-URLs der zehn Repos tokenfrei (`https://github.com/fabDaF/<repo>.git`).
Der Token lebt nur noch an zwei Orten: macOS-Keychain für den Mac-Workflow,
und `.git-credentials-fabdaf` (chmod 600, in `.gitignore`) für die
Cowork-Sandbox. Details siehe Memory-Eintrag `reference_token-haltung.md`.

## Die neun Repos in Kurzform

| Schlüssel | Lokaler Pfad | Rolle |
|---|---|---|
| `daf-a1-uebungen` | `htmlS/A1.1 NEW` | A1 aktiv |
| `daf-a2-uebungen` | `htmlS/A2.1` | A2 aktiv |
| `daf-b1-uebungen` | `htmlS/B1.1` | B1 aktiv |
| `daf-b2-uebungen` | `.` (Root) | B2 aktiv — trägt dieses CLAUDE.md und das Manifest |
| `daf-c1-uebungen` | `htmlS/C1` | C1 aktiv |
| `daf-materialien` | `daf-materialien` | Niveau-übergreifendes Material |
| `daf-architektur` | `htmlS/Architektur` | Architektur-Kurs für Privatschüler:innen |
| `daf-lueckentexte` | `htmlS/Lückentexte Mattmüller` | Lückentexte nach Mattmüller |
| `daf-archiv` | `daf-archiv` | Historische Kopien, FROZEN |

Vollständige Details inklusive Remote-URLs, Dashboard-Zuordnungen und
Erwartungen: siehe `MANIFEST.md` (generiert aus `MANIFEST.yaml`).

## Betriebs-Warnungen — was in der Vergangenheit Zeit gekostet hat

**Post-commit-Hook pusht automatisch.** Mehrere Repos haben einen Hook,
der nach jedem Commit sofort `git push` ausführt. Wenn du manuell
`git push` hinterherschickst, bekommst du Race Conditions und
"cannot lock ref"-Fehler. Stattdessen: kurz warten, dann prüfen mit
`git rev-parse HEAD origin/main` — wenn beide gleich sind, ist alles
gut.

**api.github.com ist in Cowork-Sessions blockiert.** Repos auf GitHub
anzulegen geht nicht über `gh` oder `curl`. Workaround: Chrome MCP auf
github.com/new navigieren. Dokumentiert im Konsolidierungs-Bericht
`backup/KONSOLIDIERUNG_20260410.md`.

**Cowork-Sandbox: einmaliger Auth-Setup pro Session.**

Beim ersten Push aus einer frischen Cowork-Session ist die Sandbox-Home
leer und enthält keine Git-Credentials. Auth-Failure ist die Folge.
Reaktivierung in einem Befehl aus dem Repo-Root:

```bash
bash scripts/setup-sandbox-credentials.sh
```

Das Skript kopiert den Token aus der persistenten Datei
`.git-credentials-fabdaf` in die Sandbox-Home und konfiguriert den
globalen `credential.helper`. Ende: ein echter `push --dry-run`-Test
bestätigt, dass die Auth wirklich funktioniert.

**Stale git locks — der Cowork-Commit-Workflow (2026-04-17).**

Zwei Sandbox-Einschränkungen müssen gleichzeitig umgangen werden:

1. `.git/index.lock` und `.git/HEAD.lock` können aus der Cowork-Sandbox
   **nicht gelöscht** werden (APFS-Mount-Einschränkung,
   `Operation not permitted`). `rm -f` und `os.unlink` scheitern.
2. Das Cowork-**Write-Tool** löst Permission-Dialoge aus, wenn nach
   `.git/…` geschrieben wird. Diese Dialoge blockieren unbemerkt, wenn
   Cowork im Hintergrund liegt — und Claude wartet dann stundenlang.

Deshalb gilt: **Niemals das Write-Tool für Pfade unter `.git/` benutzen.
Niemals.** Bash-Befehle lösen diese Dialoge nicht aus und sind der
einzige dialog-freie Weg, Refs zu aktualisieren.

Der komplette Commit+Push-Workflow ist in `scripts/safe-commit.sh`
gekapselt:

```bash
scripts/safe-commit.sh "Commit-Nachricht" datei1 [datei2 …]
```

Das Skript erledigt intern:

```bash
export GIT_INDEX_FILE=/tmp/alt-index-$$        # alt-Index statt .git/index.lock
git read-tree HEAD
git update-index --add DATEI1 DATEI2 …
TREE=$(git write-tree)
PARENT=$(git rev-parse HEAD)
COMMIT=$(git commit-tree $TREE -p $PARENT -m "msg")
echo "$COMMIT" > .git/refs/heads/main          # per Bash, NICHT Write-Tool
git push origin main
echo "$COMMIT" > .git/refs/remotes/origin/main # per Bash, NICHT Write-Tool
```

Für Unter-Repos wie `htmlS/A2.1` genauso aus dem jeweiligen Repo-Root
aufrufen. `COMMIT_BRANCH` und `COMMIT_REMOTE` lassen sich per env
überschreiben.

Die `warning: unable to unlink '.git/objects/*/tmp_obj_*'`-Meldungen
sind kosmetisch — die Objekte liegen korrekt im Store.

## Wenn du etwas Neues hinzufügst

Ein neues Repo, eine neue Niveau-Kategorie, ein neuer Ordner mit
eigenem Git-Status → **erst ins `MANIFEST.yaml` eintragen, dann
physisch anlegen.** In dieser Reihenfolge. Anschließend
`python3 scripts/render_manifest.py` laufen lassen, damit `MANIFEST.md`
nachzieht. Sonst ist der neue Zustand Drift und das verify-Skript
schlägt Alarm.

## Wenn du ein known_issue behebst

In `MANIFEST.yaml` unter `known_issues:` den Eintrag löschen, dann
`render_manifest.py` laufen lassen, dann committen. Nicht umgekehrt.

## E-Mail-Adresse in Lektionen — Alias-Rotation

Die formsubmit-Endpunkte und mailto-Footer in den Lektions-HTMLs
verwenden absichtlich NICHT Franks Microsoft-Primäradresse, sondern
einen rotierbaren Alias auf derselben Domain
(`fabdaf.onmicrosoft.com`). Aktueller Alias: **`unterricht@frankburkert-daf.de`**.

Wenn der aktive Alias zu sehr verspammt ist (Trigger: Frank merkt es),
ist der Rotations-Workflow:

1. Frank legt im Microsoft 365 Admin Center einen neuen Alias an
   (z.B. `unterricht-2027@fabdaf.onmicrosoft.com` oder kryptisch).
2. Claude tauscht in einem `sed`-Lauf alle Vorkommen von altem
   Alias gegen neuen Alias (typischerweise 250+ Dateien — formsubmit-
   Variablen UND mailto-Footer).
3. Frank deaktiviert den alten Alias in Microsoft 365 — die Spam-Quote
   im Postfach geht damit sofort zurück.

Wichtig: NIEMALS Franks Primäradresse `FrankBurkert@…` in Lektionen
hardcoden. Die Primärin ist seine Login-Identität und kann nicht
rotiert werden. Sie soll nicht öffentlich exponiert sein.

## Recovery: wenn GitHub stirbt

Seit dem 2026-04-28-Rollout existiert für jeden der zehn Manifest-Repos
ein Codeberg-Mirror unter `codeberg.org/fabbuLos/<repo>`, automatisch
synchronisiert via GitHub Action. Codeberg Pages serviert dieselben
Inhalte unter `fabbulos.codeberg.page/<repo>/`. Die Mirror-Action wird
allerdings AUF GITHUB ausgeführt — fällt GitHub aus, läuft kein Sync
mehr.

Wenn GitHub jemals nicht mehr erreichbar ist (Account-Sperre, längerer
Pages-Ausfall etc.), ist das vorbereitete Vorgehen:

1. **Dashboard-URLs umschalten:**
   ```bash
   bash scripts/switch-dashboard-to-codeberg.sh
   ```
   Ersetzt alle `fabdaf.github.io/`-Vorkommen durch
   `fabbulos.codeberg.page/`. Backup wird angelegt. Bisher 21 URLs in
   `htmlS/dashboard.html`.

2. **Direkt zu Codeberg pushen** (regulärer Push hängt, weil github tot):
   ```bash
   git add htmlS/dashboard.html
   git commit -m "switch: Dashboard auf Codeberg"
   git push https://fabbuLos:<TOKEN>@codeberg.org/fabbuLos/daf-b2-uebungen.git main
   git push https://fabbuLos:<TOKEN>@codeberg.org/fabbuLos/daf-b2-uebungen.git main:pages
   ```

3. **Schüler:innen die neue Dashboard-URL nennen:**
   `https://fabbulos.codeberg.page/daf-b2-uebungen/htmlS/dashboard.html`

4. **Bei GitHub-Wiederkehr Switchback:**
   ```bash
   bash scripts/switch-dashboard-to-github.sh
   ```
   Ersetzt zurück, normales Commit + Push.

Voraussetzung für Schritt 2 ist, dass der Codeberg-Token in der
Sandbox-Credentials-Datei vorhanden ist (siehe Cowork-Sandbox-Setup
oben). Auf dem Mac mit Keychain ist das ohnehin gegeben.

Langfristig saubere Alternative (nicht eingerichtet, nur dokumentiert):
eine eigene Domain wie `daf.frankburkert.de` mit DNS-Eintrag auf
`fabdaf.github.io`. Im Ernstfall DNS-Update auf `fabbulos.codeberg.page`,
keine Dashboard-Edits, keine Schüler-Kommunikation nötig. Ca. 10 EUR
Domain pro Jahr, einmalig 30 Min Setup.

## Lückentext braucht IMMER eine Wortbank (Pflicht, daf-kern §7)

Ein Lückentext ohne sichtbare Wortbank ist im Unterricht unlösbar — der
Lerner sieht nicht, welche Wörter gefragt sind. Genau dieser Fehler ist
Frank am 2026-05-29 mitten im Unterricht passiert. Deshalb gilt
ausnahmslos: **jede HTML-Datei mit einem Lückentext-Tab MUSS eine
Wort-Hilfe haben** — entweder eine skill-konforme Wortbank (§7) oder die
universelle Komponente.

Es gibt eine fertige, format-agnostische Lösung im Repo:

- `scripts/wortbank-module.js` — selbst-installierende Wortbank. Liest die
  Antworten zur Laufzeit aus den gerenderten Lücken-Inputs
  (`dataset.ans/answer/...`) bzw. aus einem globalen Daten-Array, rendert
  eine nicht-klickbare, gemischte Wortbank und gibt `.used`-Feedback. Sie
  **deaktiviert sich selbst**, wenn schon eine Wortbank/ein Wortkasten da
  ist — kann also gefahrlos überall eingespielt werden.
- `scripts/inject_wortbank.py datei.html …` — injiziert CSS + Modul
  idempotent (Marker `FB-WORTBANK-MODULE`).
- `scripts/check_wortbank.py` — Sicherheitsnetz. Scannt das Repo (oder
  einzelne Dateien) und meldet jeden Lückentext-Tab ohne Wort-Hilfe mit
  Exit-Code 1. **Vor jedem Lektions-Commit laufen lassen.**

Am 2026-05-29 wurden so 277 Dateien repariert. Es bleiben **16
Altfälle** offen, deren Lückentext-Lösungen in `const`-Arrays oder gar
nicht im DOM stehen — die brauchen Handarbeit (eigene §7-Wortbank aus
ihren Antwort-Arrays). `check_wortbank.py` listet sie.

## Fließtext braucht IMMER Serifenschrift (Pflicht, daf-lesetext §1)

Der `<body>` jeder Lektion trägt eine **Sans-Serif**-Schrift (`Segoe UI`)
— richtig für UI, Navigation, Buttons. Aber: Wenn eine `.story-text`-
oder `.lese-text`-Base-Regel **keine eigene `font-family` setzt, erbt der
gesamte Lesetext diese Sans-Serif-Schrift** und sieht nackt aus. Genau
dieser Fehler ist Frank am 2026-06-02 mitten im Unterricht passiert
(A2 „Die Arbeitswelt“); projektweit waren 25 Dateien betroffen.

Deshalb gilt ausnahmslos: **Jeder Fließtext-Container MUSS Serifenschrift
tragen** — `font-family: Georgia, 'Times New Roman', serif;` als erste
Deklaration der `.story-text`- bzw. `.lese-text`-Base-Regel. Override-
Regeln (`@media`, zweite `max-width`-Regel) brauchen sie nicht erneut;
eine Serif-Setzung pro Container genügt.

- `scripts/check_serif.py` — Sicherheitsnetz. Scannt das Repo (oder
  einzelne Dateien) und meldet jeden Fließtext-Container, der Sans-Serif
  vom `<body>` erbt, mit Exit-Code 1. Aggregiert korrekt — Override-
  Regeln lösen keinen Fehlalarm aus. **Vor jedem Lektions-Commit laufen
  lassen**, zusammen mit `check_wortbank.py`.

## JEDE Lektion braucht einen Genus-Tab (Pflicht seit 2026-06-19)

Genus ist integraler Bestandteil des Deutschlernens und muss strukturell
**überall** präsent sein. Deshalb gilt ausnahmslos: **Jede neu erstellte
oder migrierte Lektion bekommt einen Genus-Tab** — alle Niveaus (A1–C2),
alle Dateitypen (R/G/V/X/C/S/W). **Einzige Ausnahme: die expliziten
Drill-Aufgaben (FDxx)** — die sind selbst schon Genus-/Formentraining.

Der Genus-Tab (🏷️, Drag-&-Drop + Klick, Kategorien der/die/das/Plural)
gehört **direkt vor den Wortschatz-Tab** (Wortschatz bleibt letzter Tab).
Banner: die gemeinsame Spezialgrafik `htmlS/genus-banner.svg` als
eingebetteter `data:image/svg+xml;base64`-URI (NICHT pro Datei ein neues
Pexels-Bild). Bestehende Genus-Tabs behalten ihr Bild.

Werkzeug: `scripts/inject_genus.py DATEI.html woerter.json` baut den Tab
generationsrobust ein (Nav, CSS, Section, JS; Guards brechen sicher ab,
wenn das Layout abweicht). Beim Neubau einer Lektion den Genus-Tab gleich
mitbauen. Vollständiger Kampagnen-Stand: `GENUS-ROLLOUT.md`.

### Mindestens 20 Wörter

**GENUS_DATA muss mindestens 20 Einträge haben.** Empfohlen: 24,
aufgeteilt auf alle vier Kategorien (der / die / das / pl), mit thematisch
passenden Common Nouns aus der Lektion. Keine Eigennamen, keine Marken,
keine Akronyme, keine doppelten Wortformen.

Dieser Fehler ist Frank am 2026-06-17 bei 7011R aufgefallen (8 statt 24
Wörter). Die Mindestanzahl gilt für alle Niveaus und alle Dateitypen, die
einen Genus-Tab haben.

- `scripts/check_genus.py` — Sicherheitsnetz. Scannt das Repo (oder
  einzelne Dateien) und meldet jeden echten Genus-Tab mit weniger als 20
  Wörtern mit Exit-Code 1. Filtert Nicht-Genus-Arrays, die nur den Namen
  `GENUS_DATA` wiederverwenden (z. B. Konjunktiv-II-Klassen, Verbgruppen),
  korrekt heraus — keine Fehlalarme. **Vor jedem Lektions-Commit laufen
  lassen**, zusammen mit `check_serif.py` und `check_wortbank.py`.

## Vokabel-Vorentlastung — verbindliches Muster (Pflicht seit 2026-06-19)

Wenn eine Lektion ihre Schlüsselbegriffe vorab präsentiert, ist das eine
**Vorentlastung** — niemals ein zweiter, an den Anfang gestellter
„Wortschatz“-Tab. Genau dieser Fehler ist Frank am 2026-06-19 bei der
B1-Lektion 2011X (Werbekampagne) aufgefallen: Der erste Tab hieß
„💡 Wortschatz“ und zeigte eine ungestylte Begriffs-„Mindmap“, während
„🔠 Wortschatz“ am Ende ohnehin schon das Wortschatz-Training trägt — zwei
Tabs gleichen Namens, falsches Konzept.

Deshalb gilt ausnahmslos: **Der vokabel-vorentlastende erste Tab heißt
📖 Vorentlastung und folgt dem kanonischen Vokabelkarten-Muster.**
„Wortschatz“(-Training) bleibt der **letzte** Tab (siehe
`feedback_wortschatz-letzter-tab`).

Verbindliche Struktur (Goldstandard: `htmlS/C1/DE_C1_1024S-sisyphos.html`;
Pilot: `htmlS/B1.1/DE_B1_2011X-werbekampagne.html`):

- **Nav:** `<span class="nav-emoji">📖</span><span class="nav-label">Vorentlastung</span>`
  als erster Tab (nie 💡/Wortschatz an Position 0).
- **Section:** `<div class="section-title">📖 Vorentlastung</div>`, darunter
  eine kurze `<div class="section-sub">`-Zusammenfassung (ein Satz, neutrales
  Material-Register, keine Schüler-Ansprache), dann
  `<div id="vorentlastungGrid" class="vocab-grid"></div>`.
- **CSS:**
  ```css
  .vocab-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 14px; margin-top: 4px; }
  .vocab-card { background: #f8f9ff; border: 1px solid #dde3ff; border-radius: 10px; padding: 14px 16px; }
  .vocab-term { font-weight: 700; color: #667eea; font-size: 1.05em; margin-bottom: 5px; }
  .vocab-def  { color: #555; font-size: 0.92em; line-height: 1.5; }
  ```
- **JS:** Array `VORENTLASTUNG = [{ term, def }, …]` (Begriff inkl. Artikel
  und Pluralendung im `term`, z. B. `"die Werbekampagne, -en"`, Singularia
  als `"(Sg.)"`) plus `buildVorentlastung()`, aufgerufen in `DOMContentLoaded`.
- Hat die Lektion einen Lesetext, werden die Vorentlastungs-Vokabeln dort
  per `highlightVocabInText()` gelb markiert (daf-lesetext §6); reine
  Sach-/Struktur-Lektionen ohne Lesetext (wie 2011X) brauchen das nicht.

Fotokarten (Pexels) sind **optional** und nur nach ausdrücklicher Ansage
zu ergänzen — das Basismuster ist banner + Vokabelkarten ohne Foto-pro-Karte.

Skill-Bezug: Das Muster ist in `daf-lesetext` §5 (Vorentlastung) verankert.
Die Skill-Datei selbst wird über den `skill-verwaltung`-Workflow gepflegt,
nicht aus der laufenden Cowork-Session heraus.

## Schreibwerkstatt-Tab braucht IMMER Innen-Padding (Pflicht seit 2026-06-23)

Der Inhalt jedes Tabs muss vom Container-Rand eingerückt sein (daf-kern §1:
`.sec-inner`, padding 28px 30px; Banner bleibt randlos). Der Schreibwerkstatt-
Patcher hängte den Tab aber lange als nackte Section OHNE Innen-Padding an —
Folge: Name-Box, Aufgaben-Karten und Textareas kleben randlos am Container, das
Layout wirkt „an den Rand gequetscht". Frank am 2026-06-19 UND erneut am
2026-06-23 (A2 2014R) mitten im Unterricht passiert — obwohl ein erster
Reparatur-Lauf „erledigt" gemeldet hatte. Ursache der Wiederkehr: es gab **kein
Sicherheitsnetz** wie bei Serif/Wortbank/Genus, also fielen übersehene und neu
erzeugte Dateien immer wieder durch.

Es gibt zwei reale Tab-Architekturen, und nur EINE ist betroffen:

- R/X/V/W/C-Dateien: Tabs sind `<div class="section">`, und `.section` hat KEIN
  Padding (`.section { display:none }`). Der Inhalt wird über `.sec-inner`
  eingerückt — fehlt der Wrapper, klebt er. **Das ist der Bug.**
- G-Dateien: Tabs sind `<section class="section">`, und `.section` trägt das
  Padding selbst (`.section { display:none; padding:28px 30px }`) — automatisch
  eingerückt, kein Bug. (Manche B1-Dateien nutzen analog `.tab-content`.)

Ein Schreibwerkstatt-Tab ist korrekt, wenn EINES gilt: Inhalt in `.sec-inner`,
ODER eine `#<sid> { … padding … }`-Regel (der FB-SCHREIB-PAD-Fix), ODER die
Container-Klasse setzt selbst horizontales Padding. Sonst ist er kaputt.

- `scripts/schreib_pad_lib.py` — gemeinsame, architektur-agnostische
  Erkennungslogik (Tab-Klassen aus den `display:none`-Regeln gelesen, nicht
  geraten). Quelle der Wahrheit für Prüfer UND Reparateur — so driften sie nie.
- `scripts/inject_schreib_pad.py datei.html …` — idempotenter Reparateur.
  Fügt id-bewusst den FB-SCHREIB-PAD-CSS-Block ein
  (`#<sid> { padding:28px 30px }` + randloser Banner via Negativ-Margin).
  Überspringt Dateien, die bereits eingerückt sind (kein Doppel-Padding).
- `scripts/check_schreib_pad.py` — Sicherheitsnetz. Scannt das ganze Repo
  (inkl. B2-Root-Lektionen, die `check_serif.py` übersieht!) und meldet jeden
  Schreibwerkstatt-Tab ohne Padding mit Exit-Code 1. **Vor jedem Lektions-Commit
  laufen lassen**, zusammen mit `check_serif.py`, `check_wortbank.py` und
  `check_genus.py`.

## Banner dürfen KEIN abgeschnittenes Gesicht zeigen (Pflicht seit 2026-06-26)

Tab-Banner werden per `object-fit: cover` auf eine feste, niedrige Höhe
(`max-height: 180px`, mobil `120px`) beschnitten, `object-position` ist
„center". Ein Porträtfoto, dessen Gesicht oben sitzt, verliert dadurch Stirn
und **Augen** — ein „kopfloses", demotivierendes Banner. Genau das ist Frank am
2026-06-26 mitten im Unterricht passiert (B2 1011X, Lückentext-Tab). Ein
zweites Banner derselben Datei (Vorentlastung) war noch schlimmer: dort fehlten
die Augen schon **im Quellbild** — kein Crop-Trick kann sie zurückholen.

Deshalb gilt ausnahmslos: **Zeigt ein Banner einen Menschen, MUSS das ganze
Gesicht (mit Augen) im sichtbaren Crop-Band liegen.** Banner, die nur durch
glückliches Zuschneiden funktionieren, sind verboten.

**Bevorzugter Fix (Franks Methode, 2026-06-27): den Ausschnitt nach oben
schieben, nicht das Bild ersetzen.** Die meisten Köpfe sitzen oben im Bild;
`style="object-position: top"` am `<img class="tab-banner">` zeigt das obere
Band (mit Augen) und schneidet stattdessen unten den Rumpf weg, was niemanden
stört. Das rettet praktisch jedes Foto, dessen Augen im Quellbild vorhanden
sind — chirurgisch, ohne Bildtausch. **Nur gezielt auf die betroffenen Banner
setzen, nie global** auf `.tab-banner`: mittig komponierte Porträts und
Sach-/Landschaftsbilder sind bei „center" richtig, oberbündig würden sie Kinn
oder Motiv verlieren. (Mathematisch kann `object-position: top` nie ein Auge
über den oberen Bandrand schieben — der Guardrail wird damit grün.)

Erst wenn das Schieben die Augen NICHT hereinholt — d. h. die Augen fehlen schon
**im Quellbild** (wie 1011X-Vorentlastung) — wird das Foto durch ein
**selbstgebautes, gesichtsfreies SVG-Banner** ersetzt (so in 1011X: zwei flache
Reise-Grafiken, viewBox `1200×200`, also breiter als die Crop-Box → der Crop
trimmt nur die Seiten, vertikal bleibt alles sichtbar). Ein Banner ohne Gesicht
kann baulich nicht geköpft werden.

Das 100-%-Vorgehen hat drei Ebenen, weil **kein** klassischer CV-Detektor allein
100 % schafft (ein im Quellbild bereits kopflos beschnittenes, zusätzlich
getöntes Porträt liefert der Gesichtserkennung null Gesichter):

1. **Guardrail `scripts/check_banner_faces.py`** — dekodiert jedes Banner,
   erkennt frontale/seitliche Gesichter, liest die `object-position` des `<img>`
   und simuliert das tatsächlich sichtbare `cover`-Band. **Blockt (Exit 1)** jedes
   Banner, dessen Augenlinie über dem oberen Bandrand liegt (Augen weg); ein nur
   unten beschnittenes Kinn ist kosmetisch und wird nicht geblockt — so passt ein
   korrekt nach oben geschobenes Banner durch. Verdacht auf ein bereits kopflos
   beschnittenes Porträt wird als ⚠ zur Sicht-Prüfung
   gemeldet (`--strict` blockt auch das). SVG-Banner werden übersprungen
   (selbstgebaut, gesichtsfrei). **Vor jedem Lektions-Commit laufen lassen**,
   zusammen mit `check_serif.py`, `check_wortbank.py`, `check_genus.py` und
   `check_schreib_pad.py`. Braucht `opencv-python-headless`; fehlt sie,
   überspringt das Skript mit Warnung (Exit 0), blockiert also nie den Workflow.
2. **Regel** (dieser Abschnitt) — schließt die Lücke, die der Detektor nicht
   automatisch fassen kann: voll im Bild komponieren oder ersetzen.
3. **Struktur-Default** — bei neuen Lektionen im Zweifel gleich ein
   selbstgebautes SVG-Banner oder ein menschenfreies Motiv wählen.

Inventar-Stand 2026-06-26: ein Erst-Scan meldet rund **190 Dateien über alle
Niveaus** mit mindestens einem verdächtig beschnittenen Gesichts-Banner
(B2-Root 47, C1 42, B1 42, A1 34, C2 22, A2 5; heuristisch, mit Fehlalarmen).
Die Bereinigung ist eine eigene Kampagne wie der Genus-/Serif-Rollout — Datei
für Datei mit `check_banner_faces.py` als Wahrheit.

## Ergänzende Dokumente in diesem Repo

- `MANIFEST.yaml` — die SOLL-Welt, maschinenlesbar
- `MANIFEST.md` — dieselbe Info, menschenlesbar (generiert)
- `scripts/verify_manifest.sh` — IST-gegen-SOLL-Prüfung
- `scripts/render_manifest.py` — MD aus YAML erzeugen
- `scripts/check_serif.py` — Fließtext-Serif-Prüfung (vor Lektions-Commit)
- `scripts/check_wortbank.py` — Lückentext-Wortbank-Prüfung (vor Lektions-Commit)
- `scripts/check_genus.py` — Genus-Tab-Mindestanzahl-Prüfung (≥20, vor Lektions-Commit)
- `scripts/check_schreib_pad.py` — Schreibwerkstatt-Innen-Padding-Prüfung (vor Lektions-Commit)
- `scripts/check_banner_faces.py` — Banner-Gesichts-Prüfung: blockt angeschnittene Gesichter (vor Lektions-Commit)
- `scripts/schreib_pad_lib.py` — geteilte Erkennung + `scripts/inject_schreib_pad.py` — Reparateur
- `backup/KONSOLIDIERUNG_20260410.md` — Geschichte der
  11-zu-9-Konsolidierung, warum die heutige Struktur so ist
- `backup/INSTALL.md` — launchd-Backup-Aktivierung

## Franks Arbeitsweise — was ich aus früheren Sessions weiß

Frank ist DaF-Lehrer, nicht Software-Entwickler. Er bevorzugt Prosa
statt Bullet-Listen, will direkte Antworten ohne Präambel, und schätzt
Selbstreflexion und dialektisches Denken (These/Antithese/Synthese).
Er hat einen post-commit-Hook installiert, damit nichts verloren geht —
Datensicherheit ist ihm wichtiger als Git-Eleganz.

Weitere projekt-übergreifende Präferenzen liegen im Auto-Memory-System
unter `~/.auto-memory/MEMORY.md`.
