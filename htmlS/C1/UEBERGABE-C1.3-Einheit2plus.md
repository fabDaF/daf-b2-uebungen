# Übergabe: C1.3 ab Einheit 2 — Pipeline ist gebaut

**Stand:** 2026-04-28, ca. 23:30 Uhr · Adressat: nächste Cowork-Session

## Was diese Session geliefert hat

**Einheit 1 komplett** (8/8 Lektionen, alle 16/16 JSDOM-Tests grün):
- 3011G · Verben mit Genitiv (war schon fertig)
- 3012X · Ein Diagramm beschreiben
- 3013R · Null-Emissions-Städte bauen
- 3014S · Abholzung
- 3015R · Vögel und Vogelschutz
- 3016S · Das Abschmelzen der Polarkappen
- 3017R · Alexander von Humboldt
- 3018S · Nachhaltigkeit

Dashboard-Eintrag `301x` ist vollständig. Alle Dateien sind gepushed.

**Offen: 42 Lektionen**
- Einheit 2 (3021G–3028S): 8 Lektionen
- Einheit 3 (3031G–3038S): 8 Lektionen
- Einheit 4 (3041G–3048S): 8 Lektionen
- Einheit 5 (3051G–3058S): 8 Lektionen
- Einheit 6 (3061G–3068S): 8 Lektionen
- Schreibwerkstatt (3071W, 3072W): 2 Lektionen

## Pipeline — wie die nächste Session vorgehen sollte

Diese Session hat das Build-System modularisiert. Die nächste Session
braucht NICHT mehr alles selbst zu bauen — sie kann das vorhandene
Template wiederverwenden.

### Verzeichnisstruktur in der Sandbox

```
/sessions/cool-admiring-bardeen/mnt/outputs/
├── tmpl_html.html           # HTML-Template mit Platzhaltern (45 KB)
├── build_lesson.py          # Generic Builder: build(spec, output_path)
├── test_C1.js               # JSDOM-Smoke-Test (16 Checks)
├── spec_3012X.py            # Beispiel-Spec (Kommunikation/X)
├── spec_3013R.py            # Beispiel-Spec (Lesetext/R)
├── spec_3014S.py            # Beispiel-Spec (Sprechen/S)
├── spec_3015R.py            # Beispiel-Spec
├── spec_3016S.py            # Beispiel-Spec
├── spec_3017R.py            # Beispiel-Spec
├── spec_3018S.py            # Beispiel-Spec
├── pdf_3012X/               # Bilder pro Lektion (verworfen nach Session)
├── pdf_3013R/
└── ...
```

**WICHTIG:** Diese Sandbox-Dateien werden zwischen Sessions verworfen.
Beim Start der nächsten Session musst du sie aus den vorhandenen
HTMLs neu rekonstruieren — oder noch besser: dieses Übergabe-Dokument
hat alle wichtigen Bestandteile dokumentiert.

### Re-Setup zu Sessionbeginn

Falls die outputs/-Sandbox leer ist (immer der Fall):

1. **`tmpl_html.html` rekonstruieren**: Aus einer vorhandenen
   3013R-3018S-Datei das HTML extrahieren und Lektions-spezifische
   Inhalte mit Platzhaltern ersetzen — siehe `build_3012X.py` aus
   der vorherigen Session als Vorlage. Die Platzhalter:
   `__LEK__`, `__TITEL__`, `__UNTERTITEL__`, `__EMOJI__`,
   `__B_VORENT__` … `__B_WORT__` (8 Banner),
   `__VORENT_GRID__`, `__LESETEXT__`, `__QUELLE__`,
   `__VORENT_DATA__`, `__GENUS_DATA__`, `__LUECKE_DATA__`,
   `__MC_DATA__`, `__SATZBAU_DATA__`, `__WORT_DATA__`,
   `__SCHREIB_KARTEN__`.

2. **`build_lesson.py` rekonstruieren**: Sehr kurz (~100 Zeilen),
   im wesentlichen `out = open(TMPL).read(); for k,v in repls.items():
   out = out.replace(k, v); open(output, 'w').write(out)`.
   Plus Helper `b64img(path)` für Base64-Embedding.
   Plus Anführungszeichen-Regex `re.sub(r'„([^„"\n]{1,80})"', ...)`.

3. **`test_C1.js`**: 16-Check JSDOM-Skript (8 nav-btns, vocab-hl≥4,
   5 Schreibkarten, 7 MC, 14 Wortschatz, etc.).

Optimaler Weg: Prüfe als ERSTES, ob die folgenden vorhandenen
Lektions-HTMLs eine identifizierbare Struktur haben, aus der
sich tmpl/build rekonstruieren lassen — und kopiere-modifiziere:

```
htmlS/C1/DE_C1_3013R-null-emissions-staedte.html  (1.9 MB)
htmlS/C1/DE_C1_3014S-abholzung.html              (3.0 MB)
htmlS/C1/DE_C1_3015R-vogelschutz.html            (2.1 MB)
htmlS/C1/DE_C1_3016S-polarkappen.html            (2.5 MB)
htmlS/C1/DE_C1_3017R-humboldt.html               (1.0 MB)
htmlS/C1/DE_C1_3018S-nachhaltigkeit.html         (2.7 MB)
```

Diese Dateien enthalten die kanonische Struktur. Die Bilder sind
als Base64 eingebettet und können ignoriert werden (regex
`data:image/[^;]+;base64,[A-Za-z0-9+/=]+` zum Stripping).

### Pipeline pro Lektion (eingespielt)

```bash
# 1. PDF-Inhalt lesen
pdftotext -layout "lingoda c1/C 1.3/C1_NNNNT_DE.pdf" outputs/NNNNT.txt

# 2. Bilder extrahieren + Previews
mkdir -p outputs/pdf_NNNNT
pdfimages -j -p "lingoda c1/C 1.3/C1_NNNNT_DE.pdf" outputs/pdf_NNNNT/img
# Top-8 nach Dateigröße als Previews 360px breit per PIL skalieren

# 3. 4-6 Bilder visuell inspizieren mit Read auf preview-*.jpg
# Banner-Zuordnung für die 8 Tabs notieren

# 4. spec_NNNN.py schreiben (Vorlage: spec_3013R.py oder spec_3014S.py)
#    Inhalt frei essayistisch erweitern aus dem Lingoda-PDF
#    - 8 VORENTLASTUNG-Karten
#    - 8 GENUS_DATA (3-2-2-1: der/die/das/pl)
#    - 7 LUECKE_DATA
#    - 7 MC_DATA mit "correct" Index
#    - 6 SATZBAU_DATA mit parts, valid, punct
#    - 14 WORTSCHATZ (Mix Nomen/Adj/Verb)
#    - 5 SCHREIB_AUFGABEN (Mikroaufgaben, kein großer Aufsatz)
#    - LESETEXT mit MIND. 4 vocab-hl Span-Markierungen aus VORENTLASTUNG

# 5. Build und Test
python3 outputs/spec_NNNNT.py
node outputs/test_C1.js DE_C1_NNNNT-slug.html  # 16/16 erwartet

# 6. Commit (NIE Write-Tool auf .git/!)
cd /sessions/cool-admiring-bardeen/mnt/fabDaF
bash scripts/safe-commit.sh "C1.3 Lektion NNNNT: <Thema>" htmlS/C1/DE_C1_NNNNT-*.html
```

### Pro Einheit: Dashboard-Block ergänzen

Nach jeder fertigen Einheit einen `30Xx`-Block ins
`htmlS/dashboard.html` einfügen — Vorlage ist der `301x`-Block,
der bereits gepusht ist. Reihenfolge: G→X→R→S→R→S→R→S.
Tags reichhaltig wählen (Personen, Daten, Schlagworte für die
Volltextsuche).

## Inhaltliche Erkenntnisse aus Einheit 1

**Themenkern Einheit 1:** Umweltschutz, Klimawandel, Nachhaltigkeit,
Wissenschaftsgeschichte. Die nächsten Einheiten haben andere Themen
— PDFs einzeln lesen, Lingoda-Themen NICHT paraphrasieren, sondern
mit reichhaltigem Hintergrund frei erweitern.

**Lesetext-Stil:** akademisch-essayistisch, 800-1500 Wörter, mit
h3-Zwischentiteln, konkreten Daten, historischen Bezügen, prominenten
Personen. Lingoda nur als Themenanker — der Lesetext kommt aus dem
Hintergrund-Wissen, nicht aus der Lingoda-Vorlage.

**Quellenangabe:** `Quelle: Hintergrundanalyse für den DaF-Unterricht
· C1.3 – Lektion NNNNT · nach Lingoda C1_NNNNT, frei erweitert ·
[3-5 Bezugspersonen mit Daten] · Stand April 2026`

**vocab-hl Markierungen:** mindestens 4 — sonst Test rot. Tipp:
Beim Schreiben des Lesetextes direkt mit `<span class="vocab-hl"
title="📖 Vokabel aus der Vorentlastung">Wort</span>` markieren,
nicht nachträglich suchen. Idealerweise auf Begriffe aus der
VORENTLASTUNG-Liste verweisen.

**Schreibwerkstatt:** 5 Mikroaufgaben (jeweils 40-80 Wörter).
Nie eine große Schreibaufgabe — diese überspringen Lerner.

**Anführungszeichen:** ASCII-`"` als Schließer ist verboten.
Build-Skript hat schon den Regex eingebaut: `re.sub(r'„([^„"\n]{1,80})"',
lambda m: '„' + m.group(1) + '"', out)`. Falls weggelassen, manuell
ergänzen.

## Push und Codeberg-Sync

Der post-commit-Hook pusht im Hintergrund. Aus der Sandbox lief
gelegentlich ein `fatal: could not read Username` — das `safe-commit.sh`
gibt am Ende `OK: <SHA>` aus, der Mac-seitige Hook übernimmt den
eigentlichen Push. Bei Auth-Failure einmal pro Session:

```bash
bash scripts/setup-sandbox-credentials.sh
git push origin main
```

## Konkrete erste Schritte für die nächste Session

1. Diese Übergabe lesen.
2. `git pull` falls nötig (wir sind auf `1765578cde642a` Stand).
3. PDF von 3021G lesen:
   ```bash
   pdftotext -layout "lingoda c1/C 1.3/C1_3021G_DE.pdf" /tmp/3021G.txt
   head -40 /tmp/3021G.txt
   ```
4. Aus `DE_C1_3013R-null-emissions-staedte.html` per Python das
   `tmpl_html.html` rekonstruieren (Platzhalter zurückbauen).
5. `build_lesson.py` neu schreiben (~100 Zeilen, siehe oben).
6. `test_C1.js` neu schreiben (siehe Repository-Historie commit
   12cbd9b2 für den Inhalt).
7. spec_3021G.py schreiben (G-Datei: 5-Tab-Struktur, kein Lesetext,
   Vorlage ist `DE_C1_3011G-verben-genitiv.html`).
   ⚠ G-Lektionen brauchen ein ANDERES Template — 5 Tabs statt 8,
   keine Schreibwerkstatt, Entdeckungs-Tab statt Vorentlastung.

## Hinweis zum G-Template (Grammatik-Lektionen)

Die G-Datei (3021G, 3031G, 3041G, 3051G, 3061G) folgt nicht dem
RXSW-8-Tab-Pattern. Vorlage: `DE_C1_3011G-verben-genitiv.html`,
5 Tabs:
- Entdeckung (MC-Steps + Regelkarte)
- Zuordnung (12 Items, aktiv/passiv-Drag-Drop)
- Lückentext (10 Items)
- Satzbau (6 Sätze)
- Wortschatz (14 Items)

Für G-Dateien sollte ein zweites Template `tmpl_g.html` und ein
zweiter Builder erstellt werden. Oder: man baut sie ad-hoc, da nur
6 G-Lektionen anfallen.

## Realistischer Zeitplan

Pro Lektion: ca. 12-18 Minuten echte Bauzeit (PDF lesen,
Bilder prüfen, spec schreiben, testen, committen). Plus Dashboard-
Eintrag pro Einheit. → 8 Lektionen einer Einheit = 2-3 Stunden.
6 Einheiten + 2 W-Lektionen = ca. 15-20 Stunden Gesamt-Bauzeit.

Bei Cowork-Sessions sollte man 4-8 Lektionen pro Session anstreben.
Bei diesem Tempo: 5-8 weitere Sessions bis C1.3 fertig.

## Pipeline-Notizen aus Einheit 1

- **PDF-Bilder Top-Auswahl** läuft per Sortierung nach Dateigröße.
  Die größten 8 sind meist die thematisch besten.
- **Bilder visuell prüfen** ist Pflicht — Lingoda hat manchmal
  generische Bilder (Kind mit Baum, Konsumentin im Supermarkt),
  die nur teilweise zum Thema passen. Verwerten lassen sich diese
  meist als Banner für Schreibwerkstatt oder Wortschatz, wo der
  thematische Bezug nicht stringent sein muss.
- **vocab-hl Count** hängt von Lesetext-Länge ab. Bei 5+ thematisch
  relevanten Vorentlastungsbegriffen lassen sich die 4 Markierungen
  meist mühelos unterbringen.
- **MC mit "correct"-Index 0..3** — entspricht den HTML-Buttons A-D.
- **Satzbau mit "punct"-Feld** — meist `.`, gelegentlich `?` oder `!`.

## Memory-Update

Nach Abschluss aller Einheiten neuen Memory-Eintrag schreiben:
`project_c13_komplett.md` mit Datum, 50/50 Lektionen, Pipeline-
Notizen. Index in `MEMORY.md` ergänzen.

## Was schiefgehen kann

- **Test scheitert mit `vocab-hl ≥ 4 (count=3)`** → mehr `<span
  class="vocab-hl">…</span>` im Lesetext einbauen.
- **Test scheitert mit `Schreibkarten = 5`** → exakt 5 Mikroaufgaben.
- **Push-Reject wegen Codeberg-Mirror-Workflow** → kosmetisch,
  post-commit-Hook fängt es ab. `sleep 3 && git rev-parse HEAD
  origin/main` zeigt den Status.
- **`could not read Username`** → einmal pro Session
  `bash scripts/setup-sandbox-credentials.sh`.
- **`Operation not permitted` bei `.git/index`** → erwartbar,
  `safe-commit.sh` umgeht das.
- **Fehlender pdftotext/pdfimages** → `apt-get install poppler-utils`
  ist in der Sandbox bereits drin.

Viel Erfolg!

— Claude (28. April 2026, ca. 23:30 Uhr)
