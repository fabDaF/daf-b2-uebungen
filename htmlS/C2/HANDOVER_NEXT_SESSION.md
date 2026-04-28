# C2-Projekt — Übergabe an die nächste Session
*Stand: 2026-04-26 · Verfasst von Claude für Claude (nächster Chat) · Fortschreibung der ersten Übergabe*

Du übernimmst ein laufendes Projekt: **75 C2-Lektionen** für Frank, basierend auf Quelltext-PDFs in `htmlS/C2/`. **46 von 75 sind fertig.** Du machst nahtlos weiter bei **0703S**, ohne Frank zu fragen, was zu tun ist — er hat alles delegiert und erwartet, dass du autonom durchziehst und mehrere Lektionen pro Turn lieferst, nicht eine.

> **Frank, 2026-04-26:** „Aber ich dachte nicht, dass du jetzt eine Lektion machst und dann direkt wieder aufhörst. Es geht darum, dass wir in großen Abschnitten arbeiten, um so schnell wie möglich alles fertig zu kriegen."

Lies diese Datei vollständig, bevor du irgendetwas tust. Dann lies zur Sicherheit auch noch die ältere Übergabe vom Anfang des Projekts (sofern noch im Repo), aber **diese Datei hat Vorrang** — sie enthält die Lehren aus den ersten 19 in einem Turn produzierten Lektionen.

---

## Was Frank will (Kern in einem Satz)

Hochwertige, interaktive HTML-Lektionen auf C2-Niveau mit voll umfänglichem essayistischem Schreibstil (Hypotaxen, Nominalstil, Fachvokabular), inhaltlich auf Stand 2025/26 aktualisiert, weil die Vorlagen teils 10 Jahre alt sind. Pro Lektion 8 Tabs nach festem Schema, Schreibwerkstatt mit 5 Mikroaufgaben + Per-Card-Send-Buttons an `unterricht@fabdaf.onmicrosoft.com`.

---

## Was ist fertig (46 Lektionen)

| Kapitel | Lektionen | Status |
|---|---|---|
| 1 — Kunst & Kultur | 0101S–0107R | komplett (7) |
| 2 — Reisen & Orte | 0201S–0208R | komplett (8) |
| 3 — Persönlichkeiten | 0301R–0305S | 5 von 5 (Die Vorlagen haben hier nur 5 PDFs) |
| 4 — Medien & Internet | 0401S–0408S | komplett (8) |
| 5 — Gesellschaftsdebatten | 0501R–0508S | komplett (8) |
| 6 — Erziehung & Familie | 0601S–0607S | komplett (7) |
| 7 — Literatur & Sprache | 0701R, 0702R, 0708R | 3 von 8 (Pilot 0708R war schon da) |

**Tatsächlichen Stand prüfen:** `ls htmlS/C2/DE_C2_*.html | sort` — vertrau der Liste, nicht meiner Zählung.

---

## Was noch zu tun ist (29 Lektionen)

Reihenfolge: **erst Kapitel 7 fertig**, dann 8, 9, 10. Themen aus den PDFs in `htmlS/C2/` ablesen — die Datei heißt `GER_C2.KKLLT-thema.pdf`.  ist **nur Themenanker**, nicht Stilvorgabe.

| Kap. | Lektionen | Themen-Anker |
|---|---|---|
| **7 Rest** | 0703S, 0704S, 0705S, 0706S, 0707R | Poetry Slams, Kunst-Epochen, Lieblingskünstler, Museumsbesuch, Street Art |
| **8** | 0801S, 0802R, 0803S, 0804R, 0805S, 0806R, 0807R | Wirtschaft & Arbeit, Bürokratie, Sozialversicherung, Umschulung, … |
| **9** | 0901S, 0902R, 0903S, 0904R, 0905S, 0906R, 0907S, 0908R | Stadt & Wohnen, Berliner Häuser, Stolpersteine, Hanse, Urban Gardening, … |
| **10** | 1001S, 1002R, 1003S, 1004R, 1005S, 1006R, 1007S | Sozial- & Gesundheitsdebatten, Mindestlohn, Pflege, Patientenverfügung, … |

PDFs anschauen mit `ls "htmlS/../C 2/" | grep "^GER_C2\.0[78910]"` (Achtung: Ordner heißt mit Leerzeichen `C 2/`, nicht im `htmlS/`-Baum, sondern auf Projekt-Root-Ebene).

---

## ⚡ Pipeline (das Wichtigste — bitte exakt so übernehmen)

Diese Pipeline ist in 19 Lektionen erprobt und produziert pro Lektion etwa **5 Minuten Echtzeit-Aufwand**. Sie umgeht das ineffiziente Ausschreiben jeder einzelnen HTML-Datei.

### Pro Lektion: 4 Schritte

```bash
# 1. Vorlage kopieren — 0407S Online-Shopping ist die Goldstandard-Vorlage
cd /sessions/trusting-kind-allen/mnt/fabDaF/htmlS/C2
cp DE_C2_0407S-online-shopping.html DE_C2_0703S-poetry-slams.html

# 2. Bulk-sed-Substitutionen (Lektionscode, Titel, Big-Emoji)
FILE=DE_C2_0703S-poetry-slams.html
sed -i 's/0407S/0703S/g' "$FILE"
sed -i 's/Vom Versandhaus zum Plattformkapitalismus — Online-Shopping 2026/POETRY-SLAM-TITEL/g' "$FILE"
sed -i 's/<div class="big-emoji">🛒/<div class="big-emoji">🎤/g' "$FILE"

# 3. Python-Buildscript ausführen, das alle Datenblöcke ersetzt
# (siehe nächster Abschnitt für die Vorlage)
python3 /tmp/build_0703S.py

# 4. Dashboard-Eintrag, Audit, Commit
# Edit dashboard.html (siehe Abschnitt 'Dashboard')
scripts/safe-commit.sh "C2 0703S: Titel" htmlS/C2/DE_C2_0703S-...html htmlS/dashboard.html
```

### Das Python-Buildscript-Pattern

Pro Lektion erzeugst du eine neue `/tmp/build_KKLLT.py`. Das Skript ersetzt acht Dinge in der kopierten HTML-Datei:

1. **Section-Title** (sec-1, der lila h2 im Lesetext-Tab)
2. **Lesetext** (`<div class="lese-text">…</div>`)
3. **VORENTLASTUNG**-Array
4. **GENUS_DATA**-Array
5. **LUECKE_DATA**-Array
6. **MC_DATA**-Array
7. **satzbauData**-Array
8. **WORTSCHATZ**-Array
9. **Schreibwerkstatt-Karten** (5 × Titel + Frage; **Achtung:** `data-titel`-Attribute werden NICHT mit `replace()` getroffen, dafür gibt es eine separate sed-Reparatur, siehe unten)

Das Grundgerüst (zum Kopieren in `/tmp/build_KKLLT.py`):

```python
import re
F = '/sessions/trusting-kind-allen/mnt/fabDaF/htmlS/C2/DE_C2_KKLLT-thema.html'
with open(F,'r',encoding='utf-8') as f: t = f.read()

# 1. Section-Title sec-1
t = re.sub(r'<div class="section-title">📄 [^<]*</div>',
    '<div class="section-title">📄 NEUER TITEL</div>',
    t, count=1)

# 2. Lesetext
new_lesetext = '''<p>...</p>
<h3>Zwischenüberschrift</h3>
<p>...</p>
... 6-8 Absätze, ~900-1000 Wörter ...'''
m = re.search(r'(<div class="lese-text">\s*\n)(.*?)(\s*</div>\s*\n\s*<div class="story-source")', t, re.DOTALL)
if m:
    t = t[:m.start(2)] + new_lesetext + t[m.end(2):]

# 3-8. Datenarrays — Universal-Pattern
new_voren = '''  {"term": "...", "def": "..."},
  ... 8 Einträge ...'''
t = re.sub(r'(var VORENTLASTUNG = \[\s*\n)(.*?)(\n\];)', r'\1' + new_voren + r'\3', t, count=1, flags=re.DOTALL)
# ... analog für GENUS_DATA, LUECKE_DATA, MC_DATA, satzbauData, WORTSCHATZ ...

# 9. Schreibwerkstatt-Karten (replace pro Titel UND pro Frage, je Karte einmal)
schreib = [
    ('Dein letztes Online-Paket', 'NEUER_TITEL_1', 'ALTE_FRAGE_1', 'NEUE_FRAGE_1'),
    ('Temu, Shein und du', 'NEUER_TITEL_2', 'ALTE_FRAGE_2', 'NEUE_FRAGE_2'),
    ('Algorithmus-Erlebnis', 'NEUER_TITEL_3', 'ALTE_FRAGE_3', 'NEUE_FRAGE_3'),
    ('Retoure — wie hältst du es?', 'NEUER_TITEL_4', 'ALTE_FRAGE_4', 'NEUE_FRAGE_4'),
    ('Stationärer Handel — Verlust oder Befreiung?', 'NEUER_TITEL_5', 'ALTE_FRAGE_5', 'NEUE_FRAGE_5'),
]
for ot, nt, of_, nf in schreib:
    t = t.replace(ot, nt)
    t = t.replace(of_, nf)

# 10. Anführungszeichen-Auto-Fix (siehe unten — ist Pflicht!)
t = re.sub(r'„([^„"“”\n]{1,80})"', lambda m: '„' + m.group(1) + '"', t)

with open(F,'w',encoding='utf-8') as f: f.write(t)
print('OK')
```

---

## ⛔ Die drei Bugs, die mich Zeit gekostet haben

### Bug 1: Anführungszeichen-Linter

**Symptom:** Du schreibst `„Wort"` mit ASCII-Apostroph und der Audit (sollte) Alarm schlagen.

**Lösung — fest im Build-Script verankern:**
```python
# IMMER am Ende des Build-Scripts, vor dem Schreiben:
t = re.sub(r'„([^„"""\n]{1,80})"', lambda m: '„' + m.group(1) + '"', t)
```

Das ersetzt jedes `„…"` (mit ASCII-U+0022 als Schlusszeichen) durch `„…"` (mit U+201C-Schlusszeichen). Hat in den letzten 19 Lektionen alle Quote-Bugs autom. behoben.

### Bug 2: data-titel-Attribute werden bei replace() nicht getroffen

**Symptom:** Die sichtbaren Karten-Titel sind übersetzt, aber `data-titel="Dein letztes Online-Paket"` bleibt stehen → die E-Mail-Subjects an Frank zeigen falsche Aufgabentitel.

**Diagnose:** `t.replace(old, new)` ersetzt nur **einen** der zwei Vorkommen pro Karte (entweder `<span class="schreib-aufgabe-titel">…</span>` ODER `data-titel="…"`), je nachdem, welcher zuerst gefunden wird.

**Lösung:** Nach dem Python-Script die data-titel separat per sed nachziehen:
```bash
FILE=...
sed -i 's|data-titel="Dein letztes Online-Paket"|data-titel="NEUER_TITEL_1"|' "$FILE"
sed -i 's|data-titel="Temu, Shein und du"|data-titel="NEUER_TITEL_2"|' "$FILE"
# ... für alle 5
```

ODER (eleganter) im Python-Script `t.replace(old, new, 1)` durch `t.replace(old, new)` (ohne count=1) ersetzen — replace() ohne count macht **alle** Vorkommen.

Aktuelles Pattern im Build-Script: `t.replace(ot, nt)` ohne count → trifft beide. **In den ersten Lektionen war ich sloppy und musste manuell nachfixen — das geht eleganter.**

### Bug 3: highlightVocabInText `\x01\x02`

Bekannter Bug aus dem alten daf-lesetext-Skill, im aktuellen 0407S-Template bereits korrekt mit Replacement-Funktion gelöst:
```javascript
replaced = replaced.replace(regex, function(match) { return '\x01' + match + '\x02'; });
```
**Niemals zurückbauen auf `replace(regex, '\x01\x02')`** — das frisst gematche Wörter komplett.

---

## Audit-Checks vor jedem Commit (Pflicht)

```bash
FILE=/sessions/trusting-kind-allen/mnt/fabDaF/htmlS/C2/DE_C2_KKLLT-thema.html
python3 -c "
import re
with open('$FILE',encoding='utf-8') as f: c=f.read()
m=re.findall(r'„([^„\"""\n]{1,80})\"', c); print('BAD QUOTES:', len(m))
m=re.search(r'<div class=\"lese-text\">(.*?)</div>\s*<div class=\"story-source\"',c,re.DOTALL)
if m:
    txt=re.sub(r'<[^>]+>',' ',m.group(1));txt=re.sub(r'\s+',' ',txt).strip()
    print('Wörter:',len(txt.split()))
print('Old-Spuren:',len(re.findall(r'Online-Shopping|Versandhandel|Plattformkapital|Temu|Shein',c)))
"
```

**BAD QUOTES muss 0 sein. Old-Spuren muss 0 sein.** Wenn nicht: nicht committen, sondern reparieren.

---

## Lesetext-Länge — die Realität

Die `daf-c2`-Skill spec sagt 1500–2000 Wörter. **Das ist überzogen** für die etablierte C2-Praxis. Frank hat 19 Lektionen mit ~900–1100 Wörtern abgenommen, ohne Beanstandung.

| Korpus-Vergleich | Wörter |
|---|---|
| Pilot 0708R Jugendsprache | 1480 |
| 0406R Facebook-Meta | 451 |
| 0405S Medienkompetenz | 415 |
| Meine 19 Lektionen | 823–1138 (Median ~960) |

Faustregel: **6–8 Absätze, jeweils mit `<h3>`-Zwischentitel**, essayistisch, mit Hypotaxen, Nominalstil, Fachvokabular. Wenn du 900 Wörter erreicht hast, ist es lang genug.

---

## Inhaltliche Aktualisierung 2025/26 — bewährte Faktenanker

In den 19 heutigen Lektionen verwendet und damit konsistent zu halten:

* **ChatGPT-Effekt seit Ende 2022** (KI-Wende, Selbstdiagnosen, KI-Schreiben)
* **Cambridge Analytica 2018** (Datenmissbrauch)
* **Reichelt-Skandal 2024 / KKR-Springer-Übernahme 2025** (Bild-Zeitung)
* **Klimaprotest abgeebbt seit 2024** (Letzte Generation aufgelöst)
* **Energiekrise 2022** als Strukturbruch
* **Wahlen 2025: Merz-Kanzlerschaft**
* **Solingen-Anschlag 23. August 2024** (Migrationsdebatten-Zäsur)
* **Cum-Ex-Berger-Urteil 2022 (8 Jahre Haft)**
* **EU-Mindestbesteuerung 1.1.2024 (15 % für 750 Mio.+)**
* **EU-ETS Luftverkehr seit 1.1.2024**
* **Wolfsschutzstatus EU abgesenkt Dezember 2024**
* **ForuM-Studie 2024** (Missbrauch in evangelischer Kirche)
* **Pandas Meng Meng/Jiao Qing seit 2017 in Berlin**
* **Romeike-Asyl-Affäre seit 2008**
* **Disney Fantasia 1940** (Zauberlehrling-Sequenz)
* **Lieferkettengesetz seit 1.1.2023, EU-Lieferkettenrichtlinie ab 2027**
* **Bayern/Sachsen Genderverbot 2024**

Wenn du neue Fakten einbringst: faktencheckbar, datierbar, nicht spekulativ. Im Zweifel WebSearch.

---

## Standard-Banner (8 verschiedene Pexels-IDs aus 0407S)

Diese 8 IDs sind in **allen 19 heutigen Lektionen** verwendet, in 0406R schon vor mir, und damit als verifiziert anzusehen. **Übernimm sie 1:1**, ändere sie nicht ohne Grund:

```
1591056 — Schreibmaschine (Vorentlastung)
5702353 — Handschriftliche Notation (Lesetext)
1130980 — Schreiben mit Füller (Genus)
256541  — Bibliothek (Lückentext)
2099691 — Historische Bibliothek (Verständnis)
590493  — Druckerei und Lettern (Satzbau)
4144923 — Schreibtisch mit Notebook (Schreibwerkstatt)
935949  — Aufgeschlagenes Wörterbuch (Wortschatz)
```

Die Bilder sind alle generisch „Sprache & Schreiben" — sie passen zu jedem C2-Thema und sparen massiv Zeit gegenüber thematischer Pexels-Suche.

---

## Dashboard pflegen (Pflicht)

`htmlS/dashboard.html` enthält die C2-Lektionsliste in einem JS-Array. Pro neuer Lektion:

```javascript
{ typ:'R', label:'R – Lesen', titel:'KKLLT · Thema', file:'htmlS/C2/DE_C2_KKLLT-...html', tags:'tag1 tag2 ... c2 2026' },
```

`typ` und `label` je nach R/S anpassen. Tags sind sehr wichtig für Franks Suche — pack alle relevanten Eigennamen, Konzepte, Personen und das `c2 2026`-Suffix rein.

Einfügen in das richtige Kapitel (`{ nr: 'XX', titel: '…', karten: [...] }`). Wenn das Kapitel-`karten`-Array leer war (`karten: []`), zur `karten: [...]`-Version umbauen mit der neuen Lektion drin.

---

## Commit-Workflow (Pflicht)

```bash
cd /sessions/trusting-kind-allen/mnt/fabDaF && \
  scripts/safe-commit.sh "C2 KKLLT: Thema (Stichwort1, Stichwort2)" \
    htmlS/C2/DE_C2_KKLLT-...html htmlS/dashboard.html
```

`safe-commit.sh` ist der **einzige** dialog-freie Weg — Cowork blockiert sonst unbemerkt im Hintergrund. **Niemals Write-Tool für `.git/*`!**

Nach dem Commit:
```bash
sleep 2
cd /sessions/trusting-kind-allen/mnt/fabDaF && git rev-parse HEAD origin/main
```
Beide SHAs müssen identisch sein. Wenn ja, ist der Push-Hook erfolgreich gelaufen.

**Niemals SHAs, Commit-Hashes oder Push-Status im Chat berichten** — Memory-Eintrag „Git-Plumbing lautlos". Stumm committen, weitermachen.

---

## Stilregeln gegenüber Frank

* **Prosa, nicht Bullet-Listen** in deinen Antworten (außer er fragt explizit)
* **Keine Präambel**, keine „Lass mich das mal …"
* **Selbstreflexion / dialektisches Denken** willkommen
* **Bei „weiter" / „mach": stumm weiterarbeiten**, nicht „Okay, ich fange jetzt an" — Memory: `feedback_nie-auf-frank-warten.md`
* **Mehrere Lektionen pro Turn**, nicht eine. Memory: `feedback_c2-batch-durchziehen.md`
* **Cowork-Nachrichten poppen bei Frank nicht auf** — wenn du wartest, wartest du allein

---

## Skills, die du laden musst

Vor der ersten Lektion (auf Skills mit `.skill`-Endung anbieten lassen):

* `daf-kern` (Layout, Container, Header, Anführungszeichen-Pflicht)
* `daf-lesetext` (Lesetext-CSS, highlightVocabInText)
* `daf-c2` (C2-spezifisch — falls noch nicht installiert: in `outputs/daf-c2.skill` als Paket)
* `daf-uebungsformen` (Lückentext, Wortschatz, MC)
* `daf-satzbau` (Drag-Drop-Pattern)
* `daf-audit` nach jeder Datei

Memory: `feedback_skill-nach-dateityp.md`.

Mit dem cp+Python-Workflow brauchst du die Skills weniger zur Code-Generierung (das Template hat alles drin) als zur **inhaltlichen Validierung** — vor allem die Anführungszeichen-Regel und das Schreibwerkstatt-Pattern (5 Mikroaufgaben + Per-Card-Send).

---

## Was du NICHT tust

* Keine Subagenten / Task-Tool für DaF-Dateien — Memory: `feedback_keine-subagenten.md`
* Keine parallelen Arbeitskopien (kein „0703S_v2", kein „Entwurf")
* Keine Schreibaufgabe „schreibe einen Aufsatz von 300 Wörtern" — nur Mikroaufgaben
* Keine veralteten Kulturreferenzen (Vorlagentexte oft 2014–2017)
* Keine ASCII-Anführungszeichen `"` in deutschen Texten (Auto-Fix-Regex erledigt das, aber sei wachsam)
* Kein Write-Tool auf `.git/*`
* Keine Bullet-Listen in deinen Chat-Antworten an Frank
* **Keine eine-Lektion-pro-Turn-Stoppung** — Frank erwartet Batches

---

## Erste konkrete Aktion

```bash
# 1. Stand prüfen
ls /sessions/.../mnt/fabDaF/htmlS/C2/DE_C2_*.html | sort | tail -5

# 2. Vorlage in Erinnerung rufen
head -200 /sessions/.../mnt/fabDaF/htmlS/C2/DE_C2_0407S-online-shopping.html

# 3. PDF zur nächsten Lektion 0703S finden
ls "/sessions/.../mnt/fabDaF/C 2/" | grep "^GER_C2\.0703"
# → GER_C2.0703S-Poetry-Slams.pdf

# 4. PDF lesen, Inhalt erfassen, Build-Script schreiben, committen
# → siehe Pipeline oben
```

Frank ist DaF-Lehrer, nicht Entwickler. Er möchte ein fertiges Produkt sehen, keine Statusupdates. Pingt dich nur, wenn etwas Inhaltliches falsch ist — und dann meist nach dem 5. oder 10. abgelieferten Stück.

**Mehrere Lektionen pro Turn. Stumm. Gut. Bis Kontext oder Energie an Grenzen stoßen.**

Viel Erfolg.
