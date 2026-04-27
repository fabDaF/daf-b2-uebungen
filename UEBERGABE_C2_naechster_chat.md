# C2-Projekt — Übergabe an die nächste Session

**Stand: 2026-04-27** · Verfasser: Claude (Sonnet 4.6) für Claude (nächster Chat) ·
**Dritte** Fortschreibung — die Schwester-Datei aus dem zweiten Turn (mit der ausführlichen
Pipeline-Erklärung) hat weiterhin Vorrang, sofern dort etwas detaillierter steht. Diese Datei
hier ist die Aktualisierung des Stands plus die in diesem Turn dazugelernten Lehren.

Lies diese Datei vollständig, bevor du irgendetwas tust. Frank hat alles delegiert und
erwartet, dass du autonom durchziehst und mehrere Lektionen pro Turn lieferst, nicht eine.

> Frank, 2026-04-26: „Aber ich dachte nicht, dass du jetzt eine Lektion machst und dann
> direkt wieder aufhörst. Es geht darum, dass wir in großen Abschnitten arbeiten, um so
> schnell wie möglich alles fertig zu kriegen."

## Aktueller Stand: 58 von 72 fertig (statt 75 — siehe Erratum)

Erratum aus den Vorgänger-Übergaben: Das Lingoda-Korpus enthält für Kapitel 3 nur **5**
PDFs (statt 7), und Kapitel 10 hat nur **6** Lektionen (1001S–1004S, 1006S, 1007S — kein
1005). Echte Gesamtzahl: **72**. Tatsächlichen Stand prüfen mit:

```bash
ls /sessions/<dein-mnt>/mnt/fabDaF/htmlS/C2/DE_C2_*.html | sort | wc -l
```

| Kap. | Thema                  | Status                                 |
|------|------------------------|----------------------------------------|
| 1    | Kunst & Kultur         | komplett (7)                           |
| 2    | Reisen & Orte          | komplett (8)                           |
| 3    | Persönlichkeiten       | komplett (5)                           |
| 4    | Medien & Internet      | komplett (8)                           |
| 5    | Gesellschaftsdebatten  | komplett (8)                           |
| 6    | Erziehung & Familie    | komplett (7)                           |
| 7    | Sprache, Kunst & Lit.  | **komplett (8)** — diese Session       |
| 8    | Arbeit & Karriere      | **komplett (7)** — diese Session       |
| 9    | Stadt & Wohnen         | offen (8)                              |
| 10   | Sozial & Gesundheit    | offen (6)                              |

In meinem Turn produziert (12 Lektionen): 0703S, 0704S, 0705S, 0706S, 0707R, 0801S, 0802S,
0803S, 0804S, 0805R, 0806R, 0807R.

**Verbleibend: 14 Lektionen.** Die nächste fällige ist 0901S Town-or-country.

## Die noch offenen 14 Lektionen mit Lingoda-Themen

Wichtig: Die R/S-Endungen aus älteren Übergaben sind teils falsch — orientiere dich an
den echten PDF-Dateinamen, nicht an Memory-Skizzen. Hier die echten Endungen aus
`ls "/sessions/<mnt>/mnt/fabDaF/C 2/" | grep "^GER_C2.0[9]\|^GER_C2.1"`:

**Kapitel 9 — Stadt & Wohnen**

| Code   | Lingoda-Thema                          |
|--------|----------------------------------------|
| 0901S  | Town or country                        |
| 0902S  | What makes a city livable              |
| 0903R  | Berlin houses                          |
| 0904R  | Fair-Trade Cities                      |
| 0905R  | Stumbling blocks — A project (Stolpersteine) |
| 0906S  | Urban Gardening                        |
| 0907S  | Environmental areas                    |
| 0908R  | The Hanseatic League                   |

**Kapitel 10 — Sozial- & Gesundheitsdebatten** (alle S, kein 1005)

| Code   | Lingoda-Thema                          |
|--------|----------------------------------------|
| 1001S  | Minimum wage                           |
| 1002S  | Debate — Child-care subsidy            |
| 1003S  | Taking care of the elderly             |
| 1004S  | Health insurance in Germany            |
| 1006S  | Living wills (Patientenverfügung)      |
| 1007S  | Debate — Fat tax                       |

## ⚡ Pipeline (das Wichtigste — exakt so übernehmen)

Die in der Vorgänger-Übergabe beschriebene Pipeline bleibt unverändert. Pro Lektion sind
das vier Schritte: cp + sed (Lektionscode/Titel/Big-Emoji), Python-Buildscript für die
Datenblöcke, Dashboard-Eintrag, `safe-commit.sh`. Die Goldstandard-Vorlage ist weiterhin
**`DE_C2_0407S-online-shopping.html`**.

```bash
# 1. Vorlage kopieren
cd /sessions/<dein-mnt>/mnt/fabDaF/htmlS/C2
cp DE_C2_0407S-online-shopping.html DE_C2_0901S-stadt-oder-land.html

# 2. Bulk-sed
FILE=DE_C2_0901S-stadt-oder-land.html
sed -i 's/0407S/0901S/g' "$FILE"
sed -i 's/<div class="big-emoji">🛒/<div class="big-emoji">🌆/g' "$FILE"
sed -i 's|Vom Versandhaus zum Plattformkapitalismus — Online-Shopping 2026|DEIN-NEUER-TITEL|g' "$FILE"

# 3. Python-Buildscript ausführen — siehe Vorlage unten
python3 /sessions/<dein-mnt>/mnt/outputs/build_0901S.py

# 4. Dashboard-Eintrag in das richtige Kapitel-Array, dann Commit
scripts/safe-commit.sh "C2 0901S: Titel" htmlS/C2/DE_C2_0901S-...html htmlS/dashboard.html
```

## ⛔ Drei Bugs, die in DIESEM Turn aufgetaucht sind — und die Lehren

### Bug A: `“`-Backslash-Escape im `re.sub`-Replacement-String

Das ältere Pipeline-Pattern `re.sub(pat, r'\1' + new_data + r'\3', t, ...)` interpretiert
das replacement als Template — und stößt sich an Backslash-Escapes wie `\u`, `\g`, `\1`.
**Symptom:**

```
re.error: bad escape \u at position 257
```

**Lösung — von Anfang an Lambdas benutzen, nicht String-Konkatenation:**

```python
# FALSCH (kann an \u, \g, \1 in den Datenblöcken sterben):
t = re.sub(r'(var X = \[\s*\n)(.*?)(\n\];)',
           r'\1' + new_data + r'\3',
           t, count=1, flags=re.DOTALL)

# RICHTIG:
t = re.sub(r'(var X = \[\s*\n)(.*?)(\n\];)',
           lambda mm: mm.group(1) + new_data + mm.group(3),
           t, count=1, flags=re.DOTALL)
```

Das ist die einzige zuverlässige Form — `re.escape()` auf den Datenblock zu legen, würde
die echten Strings kaputtmachen.

### Bug B: Wörtliche `“`-Sequenzen im finalen HTML

Wenn du in einem Python-String mit doppelten Anführungszeichen ein typografisches
Schlusszeichen brauchst und versucht bist, es als `“` zu schreiben, bekommst du in
der HTML-Datei am Ende **wörtlich `“`** stehen — weil `\u`-Escapes im Python-Triple-
Quoted-String-Literal nicht aufgelöst werden, wenn der String aus einem Lambda-`replace`-
Aufruf in `re.sub` zurückkommt. **Symptom:**

```bash
$ grep -c "\\\\u201C" $FILE
1   # ← bedeutet: irgendwo steht „…“ im sichtbaren Text
```

**Lösung — schreib das typografische Schlusszeichen direkt als `“` (U+201C) oder via Auto-
Fix-Regex am Ende des Build-Scripts:**

```python
# Pflicht-Sweep am Ende JEDES Build-Scripts, vor dem Schreiben:
t = re.sub(r'„([^„"“”\n]{1,80})"', lambda m: '„' + m.group(1) + '“', t)
```

Wenn dir doch ein `“` durchgeht: nachträglich mit einem zweiten `re.sub('\\\\u201C', '“', c)`
fixen und nochmal commiten. Mir ist das in 0807R passiert — siehe Commit
`0f890ddb1edc002aa77c8334e226f1bedb792312`.

### Bug C: `data-titel`-Attribute werden bei `replace()` mit `count=1` nicht beide getroffen

Pro Schreibwerkstatt-Karte gibt es den Titel zweimal: einmal sichtbar in
`<span class="schreib-aufgabe-titel">…</span>` und einmal unsichtbar in
`data-titel="…"` (für die Mail-Subjects). Wenn du `t.replace(old, new, 1)` mit `count=1`
verwendest, ersetzt du nur einen der beiden. **Lösung:** `t.replace(old, new)` ohne
`count` macht alle Vorkommen. Pattern, das ich in dieser Session benutzt habe und das
sauber funktioniert:

```python
schreib = [
    ('Dein letztes Online-Paket', 'NEUER_TITEL_1'),
    ('Temu, Shein und du',          'NEUER_TITEL_2'),
    # ... 5 Tupel
]
for ot, nt in schreib:
    t = t.replace(ot, nt)   # KEIN count=1 — sonst data-titel bleibt alt

fragen = [
    (alte_frage_1, neue_frage_1),
    # ... 5 Tupel
]
for of_, nf in fragen:
    t = t.replace(of_, nf)
```

## Build-Script-Vorlage zum Kopieren (sauber, alle Lehren drin)

Speicherort: `/sessions/<dein-mnt>/mnt/outputs/build_KKLLT.py`

```python
import re
F = '/sessions/<dein-mnt>/mnt/fabDaF/htmlS/C2/DE_C2_KKLLT-thema.html'
with open(F, 'r', encoding='utf-8') as f: t = f.read()

# 1. Section-Title sec-1
t = re.sub(r'<div class="section-title">📄 [^<]*</div>',
    '<div class="section-title">📄 NEUER TITEL</div>',
    t, count=1)

# 2. Lesetext (~900–1000 Wörter, 6–8 Absätze, jeweils mit <h3>)
new_lesetext = '''<p>...</p>
<h3>...</h3>
<p>...</p>'''

m = re.search(r'(<div class="lese-text">\s*\n)(.*?)(\s*</div>\s*\n\s*<div class="story-source")', t, re.DOTALL)
if m:
    t = t[:m.start(2)] + new_lesetext + t[m.end(2):]

# 3–8. Datenblöcke — Lambda-Pattern (NIE r'\1' + … + r'\3')
new_voren = '''  {"term": "...", "def": "..."},
  ...'''
t = re.sub(r'(var VORENTLASTUNG = \[\s*\n)(.*?)(\n\];)',
           lambda mm: mm.group(1) + new_voren + mm.group(3),
           t, count=1, flags=re.DOTALL)

# … analog für GENUS_DATA, LUECKE_DATA, MC_DATA, satzbauData, WORTSCHATZ

# 9. Schreibwerkstatt — Titel + Frage über replace() OHNE count
schreib = [
    ('Dein letztes Online-Paket',                  'NEUER TITEL 1'),
    ('Temu, Shein und du',                          'NEUER TITEL 2'),
    ('Algorithmus-Erlebnis',                        'NEUER TITEL 3'),
    ('Retoure — wie hältst du es?',                 'NEUER TITEL 4'),
    ('Stationärer Handel — Verlust oder Befreiung?','NEUER TITEL 5'),
]
for ot, nt in schreib:
    t = t.replace(ot, nt)

fragen = [
    ('Was hast du zuletzt online bestellt — und warum nicht im stationären Geschäft? Schildere konkret in vier Sätzen.', 'NEUE FRAGE 1'),
    ('Hast du schon einmal bei Temu oder Shein bestellt? Wenn ja: wie war es, und würdest du es wiederholen? Wenn nein: warum nicht? Eine ehrliche Mini-Reflexion.', 'NEUE FRAGE 2'),
    ('Wann hast du zuletzt etwas gekauft, das dir der Algorithmus vorgeschlagen hat — und das du sonst nie gefunden hättest? Beschreibe den Moment.', 'NEUE FRAGE 3'),
    ('Bestellst du Mode oft in mehreren Größen, um zurückzuschicken, was nicht passt? Eine kurze, ehrliche Stellungnahme zur Retourenpraxis.', 'NEUE FRAGE 4'),
    ('Stell dir die Innenstadt deiner Stadt in zehn Jahren vor: Welche Geschäfte werden noch da sein, welche nicht? Skizziere kurz dein Bild.', 'NEUE FRAGE 5'),
]
for of_, nf in fragen:
    t = t.replace(of_, nf)

# 10. Anführungszeichen-Auto-Fix (Pflicht — fängt ASCII-Schlusszeichen ab)
t = re.sub(r'„([^„"“”\n]{1,80})"', lambda m: '„' + m.group(1) + '“', t)

with open(F, 'w', encoding='utf-8') as f: f.write(t)
print('OK')
```

## Audit-Check vor jedem Commit

```bash
FILE=/sessions/<dein-mnt>/mnt/fabDaF/htmlS/C2/DE_C2_KKLLT-thema.html
python3 -c "
import re
with open('$FILE',encoding='utf-8') as f: c=f.read()
m=re.findall(r'„([^„\"“”\n]{1,80})\"', c); print('BAD QUOTES:', len(m))
print('Backslash-u201C-Spuren:', c.count('\\\\u201C'))
m=re.search(r'<div class=\"lese-text\">(.*?)</div>\s*<div class=\"story-source\"',c,re.DOTALL)
if m:
    txt=re.sub(r'<[^>]+>',' ',m.group(1));txt=re.sub(r'\s+',' ',txt).strip()
    print('Wörter:',len(txt.split()))
print('Old-Spuren:',len(re.findall(r'Online-Shopping|Versandhandel|Plattformkapital|Temu|Shein',c)))
print('data-titel-old:', len(re.findall(r'data-titel=\"Dein letztes Online-Paket|data-titel=\"Temu, Shein|data-titel=\"Algorithmus-Erlebnis|data-titel=\"Retoure|data-titel=\"Stationärer Handel', c)))
"
```

**Alle vier Werte (BAD QUOTES, Backslash-u201C, Old-Spuren, data-titel-old) müssen 0 sein.**
Wörter sollten zwischen 800 und 1100 liegen. Wenn nicht: nicht commiten, sondern reparieren.

## Pexels-Banner — bewährt, nicht ändern

Die acht Pexels-IDs aus 0407S sind in mittlerweile 31 Lektionen genutzt und gelten als
verifiziert. Übernimm sie 1:1, ändere sie nicht ohne Grund:

```
1591056 — Schreibmaschine                      (Vorentlastung)
5702353 — Handschriftliche Notation            (Lesetext)
1130980 — Schreiben mit Füller                 (Genus)
256541  — Bibliothek                           (Lückentext)
2099691 — Historische Bibliothek               (Verständnis)
590493  — Druckerei und Lettern                (Satzbau)
4144923 — Schreibtisch mit Notebook            (Schreibwerkstatt)
935949  — Aufgeschlagenes Wörterbuch           (Wortschatz)
```

## Dashboard-Eintrag — Fallunterscheidung

Kapitel 9 und 10 haben aktuell `karten: []`. Beim **ersten** Eintrag in ein Kapitel
musst du das `[]` zu einem `[ … ]` umbauen, mit der neuen Lektion drin. Bei den folgenden
Lektionen einfach hinter die letzte Karte einfügen. Beispiel-Pattern für den ersten
Eintrag in Kapitel 9:

```javascript
{ nr: '09', titel: 'Stadt & Wohnen — Berliner Häuser, Stolpersteine, Hanse, Urban Gardening', karten: [
  { typ:'S', label:'S – Sprechen', titel:'0901S · Stadt oder Land', file:'htmlS/C2/DE_C2_0901S-...html', tags:'... c2 2026' },
]},
```

Die Tags müssen alle Eigennamen, Konzepte, Personen und Daten der Lektion enthalten plus
das Suffix `c2 2026` — Frank sucht über die Tags. Lieber zu viele als zu wenige.

## Inhaltliche Aktualisierung 2025/26 — gepflegter Faktenanker

Die in den 31 bisherigen Lektionen verwendeten und damit konsistent zu haltenden
Eckdaten — bitte nur ergänzen, nicht widersprechen:

- ChatGPT-Effekt seit Ende 2022 (KI-Wende)
- Cambridge Analytica 2018
- Reichelt-Skandal 2024 / KKR-Springer 2025
- Letzte Generation 2024 aufgelöst
- Solingen-Anschlag 23. August 2024
- Cum-Ex-Berger-Urteil 2022 (8 Jahre)
- EU-Mindestbesteuerung 1.1.2024 (15 % für 750 Mio.+)
- EU-ETS Luftverkehr seit 1.1.2024
- Wolfsschutzstatus EU abgesenkt Dezember 2024
- ForuM-Studie 2024 (ev. Kirche)
- Lieferkettengesetz seit 1.1.2023 (LkSG), CSDDD ab 2027
- **Pergamonmuseum geschlossen Oktober 2023** (bis 2027/2037)
- **Humboldt Forum eröffnet Juli 2021**
- **Benin-Bronzen-Rückgabe Dezember 2022 durch Baerbock**
- **Bürgergeld 1.1.2023, im April 2024 Sanktionen wieder verschärft**
- **Verbrenner-Aus 2035** / Kohleausstieg Ende 2018 (Steinkohle) / 2030–2038 (Braunkohle)
- **Generalistische Pflegeausbildung Januar 2020**
- **Qualifizierungschancengesetz Januar 2019**, 2023 verschärft
- **OZG 2017, OZG 2.0 Mai 2024 (Frist 2028)**
- **ID-Wallet-Debakel 23.–28. September 2021**
- **Rana Plaza Bangladesch 24. April 2013, 1135 Tote**
- **WeWork Insolvenz November 2023**
- **Brexit-Erasmus-Aus 31. Januar 2020 / UK-Turing-Programm 2021**
- **EU-Jugendgarantie Dezember 2013**
- **ILO Welt-Bericht Juni 2024: 138 Millionen Kinderarbeiter**

Bei neuen Fakten: faktencheckbar, datierbar, nicht spekulativ. Im Zweifel WebSearch.

## Commit-Workflow (Pflicht)

```bash
cd /sessions/<dein-mnt>/mnt/fabDaF && \
  scripts/safe-commit.sh "C2 KKLLT: Thema (Stichwort1, Stichwort2)" \
    htmlS/C2/DE_C2_KKLLT-...html htmlS/dashboard.html
```

`safe-commit.sh` ist der einzige dialog-freie Weg. **Niemals Write-Tool für `.git/*`!**
Niemals SHAs, Commit-Hashes oder Push-Status im Chat berichten — Memory-Eintrag
„Git-Plumbing lautlos". Stumm committen, weitermachen.

## Stilregeln gegenüber Frank

- Prosa, nicht Bullet-Listen in Antworten (außer er fragt explizit)
- Keine Präambel
- Bei „weiter" / „mach": stumm weiterarbeiten, kein „Okay, ich fange jetzt an"
- **Mehrere Lektionen pro Turn, nicht eine.** Memory: `feedback_c2-batch-durchziehen.md`
- Cowork-Nachrichten poppen bei Frank nicht auf — wenn du wartest, wartest du allein

## Pfad-Hinweis (sehr wichtig!)

Der `/sessions/<mnt>/mnt/...`-Pfad ist **pro Session unterschiedlich**. Mein Pfad in
diesem Turn war `/sessions/modest-nifty-archimedes/mnt/fabDaF/...` — deiner ist anders.
Find ihn mit:

```bash
ls /sessions/ 2>/dev/null
```

Stabil bleibt nur: Workspace-Folder = `/Users/frankburkert/Cowork/Projekte/fabDaF/`,
darin `htmlS/C2/` für die Lektionen, `C 2/` (mit Leerzeichen, auf Repo-Root!) für die
PDFs, `htmlS/dashboard.html` für das Dashboard.

## Skills, die du laden solltest

Vor der ersten Lektion (in dieser Reihenfolge):
1. `daf-kern` (Layout, Anführungszeichen-Pflicht)
2. `daf-c2` (8-Tab-Struktur, Schreibwerkstatt-Pattern)
3. `daf-lesetext` (Lesetext-CSS, highlightVocabInText)
4. `daf-uebungsformen` (Lückentext, Wortschatz, MC)
5. `daf-satzbau` (Drag-Drop)
6. `daf-audit` nach jeder Datei

Mit dem cp+Python-Workflow brauchst du die Skills weniger zur Code-Generierung als zur
inhaltlichen Validierung — vor allem für die Anführungszeichen-Regel und das
Schreibwerkstatt-Pattern (5 Mikroaufgaben + Per-Card-Send).

## Was du NICHT tust

- Keine Subagenten / Task-Tool für DaF-Dateien
- Keine parallelen Arbeitskopien (kein „0901S_v2", kein „Entwurf")
- Keine grosse Schreibaufgabe „schreib einen Aufsatz von 300 Wörtern" — nur Mikroaufgaben
- Keine veralteten Kulturreferenzen (Lingoda-Texte sind 2014–2017)
- Keine ASCII-Anführungszeichen `"` in deutschen Texten
- Kein Write-Tool auf `.git/*`
- Keine Bullet-Listen in deinen Chat-Antworten an Frank
- Keine eine-Lektion-pro-Turn-Stoppung

## Erste konkrete Aktion

```bash
# 1. Stand prüfen
MNT=$(ls /sessions/ 2>/dev/null | head -1)
ls /sessions/$MNT/mnt/fabDaF/htmlS/C2/DE_C2_*.html | sort | tail -3
# letzte Datei sollte DE_C2_0807R-umschulung.html sein

# 2. Vorlage in Erinnerung rufen
head -200 /sessions/$MNT/mnt/fabDaF/htmlS/C2/DE_C2_0407S-online-shopping.html

# 3. Erste offene Lektion: 0901S Stadt oder Land
ls "/sessions/$MNT/mnt/fabDaF/C 2/" | grep "^GER_C2.0901"

# 4. PDF lesen, Inhalt erfassen, Build-Script schreiben, committen
```

Frank ist DaF-Lehrer, nicht Entwickler. Er möchte ein fertiges Produkt sehen, keine
Statusupdates. Pingt dich nur, wenn etwas Inhaltliches falsch ist.

**Mehrere Lektionen pro Turn. Stumm. Gut. Bis Kontext oder Energie an Grenzen stoßen.
Idealerweise das ganze Kapitel 9 in einem Turn, danach Kapitel 10 in einem zweiten —
dann ist das C2-Projekt komplett.**

Viel Erfolg.
