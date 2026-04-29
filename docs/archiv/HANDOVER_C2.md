# C2-Projekt — Übergabe an die nächste Session

Stand: 2026-04-26 · Verfasst von Claude für Claude (nächster Chat)

Du übernimmst ein laufendes Projekt: 75 C2-Lektionen für Frank, basierend auf Lingoda-PDFs in `htmlS/C2/`. **27 von 75** sind fertig. Du machst nahtlos weiter bei **0407S**, ohne Frank zu fragen, was zu tun ist — er hat alles delegiert und erwartet, dass du autonom durchziehst.

Lies diese Datei vollständig, bevor du irgendetwas tust. Sie ist dein einziger Kontext.

## Was Frank will (Kern in einem Satz)

Hochwertige, **interaktive HTML-Lektionen auf C2-Niveau** mit voll umfänglichem essayistischem Schreibstil (Hypotaxen, Nominalstil, Fachvokabular), inhaltlich **auf Stand 2025/26 aktualisiert**, weil die Lingoda-Vorlagen teils 10 Jahre alt sind. Pro Lektion 8 Tabs nach festem Schema, Schreibwerkstatt mit 5 Mikroaufgaben + Per-Card-Send-Buttons an `frankburkert@gmx.net`.

## Wo du dich befindest

| Ort | Bedeutung |
|---|---|
| `/Users/frankburkert/Cowork/Projekte/fabDaF/` | Projekt-Root (Mac-Pfad), in Bash: `/sessions/.../mnt/fabDaF/` |
| `htmlS/C2/` | Alle C2-Lektionen liegen hier als `DE_C2_NNNNT.html` |
| `htmlS/dashboard.html` | Das **einzige** Dashboard. C2-Karten unter Sektion "C2" |
| `outputs/c2_gen.py` | Generator-Pipeline (Bash-Pfad: `/sessions/.../mnt/outputs/c2_gen.py`) |
| `outputs/spec_NNNNT.py` | Pro Lektion eine Spec-Datei (Eingabe für Generator) |
| `scripts/safe-commit.sh` | Pflicht-Commit-Workflow (umgeht Sandbox-Locks) |

Repo: `daf-b2-uebungen` (das Hauptrepo, das auch C2 trägt — siehe `MANIFEST.yaml`).

## Status: was ist fertig

Kapitel 1–3 komplett (24 Lektionen) plus Kapitel 4 angefangen (3 von 8). Kapitel 7 hat bereits den Pilot 0708R Jugendsprache.

Fertig: 0101S, 0102R, 0103S, 0104R, 0105S, 0106R, 0107S, 0108R, 0201S, 0202R, 0203S, 0204R, 0205S, 0206R, 0207S, 0208R, 0301S, 0302R, 0303S, 0304R, 0305S, 0306R, 0307S, 0308R, 0401R, 0402S, 0403R, 0404S, 0405S, 0406R, 0708R.

Tatsächlicher Stand vor Übernahme prüfen: `ls htmlS/C2/DE_C2_*.html | sort` — vertraue der Liste, nicht meiner Zählung.

## Was noch zu tun ist (48 Lektionen)

Reihenfolge: erst Kapitel 4 fertig, dann 5, 6, 7 (ohne 0708R), 8, 9, 10.

| Kapitel | Lektionen | Thema |
|---|---|---|
| 4 Rest | 0407S, 0408S | Politik / Macht (Themen aus PDFs ablesen) |
| 5 | 0501R, 0502S, 0503R, 0504S, 0505R, 0506S, 0507R, 0508S | Religion, Steuerflucht, Jagd, Zoos, Billigflüge, Frauenquote, Textilindustrie, Multikulti |
| 6 | 0601S, 0602R, 0603S, 0604R, 0605S, 0606R, 0607S | Erziehung |
| 7 (ohne 0708R) | 0701R, 0702S, 0703R, 0704S, 0705R, 0706S, 0707R | Sprache & Kultur |
| 8 | 0801S, 0802R, 0803S, 0804R, 0805S, 0806R, 0807R | Wirtschaft / Arbeit |
| 9 | 0901S, 0902R, 0903S, 0904R, 0905S, 0906R, 0907S, 0908R | Wissenschaft / Forschung |
| 10 | 1001S, 1002R, 1003S, 1004R, 1005S, 1006R, 1007S | Abschluss |

Themen pro Lektion stehen im jeweiligen Lingoda-PDF unter `htmlS/C2/`. R = Lesen, S = Sprechen — beide werden hier zu Lese-Lektionen mit allen 8 Tabs umgewandelt. Die Lingoda-Themen sind nur Inspirationsrahmen; aktualisiere Inhalte auf 2025/26.

## Pipeline-Architektur

Drei-Datei-System pro Lektion:

1. **`outputs/spec_NNNNT.py`** — du schreibst sie. Enthält: `LESETEXT` (str), `VORENTLASTUNG` (list of dicts), `GENUS_DATA` (list), `LUECKE_DATA` (list), `MC_DATA` (list), `SATZBAU_DATA` (list), `MIKROAUFGABEN` (list of 5 dicts), `WORTSCHATZ` (list), `SPEC` (dict mit Metadaten).
2. **`outputs/c2_gen.py`** — bereits vorhanden. Hat `HTML_TEMPLATE`, `MIKROAUFGABE_TEMPLATE`, `fix_quotes()`, `render_lektion(spec)`. Liest die Spec, rendert HTML, schreibt nach `htmlS/C2/DE_C2_NNNNT.html`.
3. **`scripts/safe-commit.sh`** — committed und pusht.

### Workflow pro Lektion (3 Schritte)

```bash
# 1. Spec schreiben (Write-Tool, Bash-Pfad outputs/spec_NNNNT.py)

# 2. Generator laufen lassen
cd /sessions/.../mnt/outputs && python3 c2_gen.py NNNNT

# 3. Commit + Push (vom fabDaF-Root)
cd /sessions/.../mnt/fabDaF && \
  scripts/safe-commit.sh "C2 NNNNT: <Thema>" htmlS/C2/DE_C2_NNNNT.html htmlS/dashboard.html
```

Das Dashboard musst du parallel pflegen: pro neuer Lektion einen Karten-Eintrag in der C2-Sektion hinzufügen (Format wie bestehende C2-Karten — schau dir `htmlS/dashboard.html` an, kopiere das Muster).

## C2-Schreibstil (verbindlich)

Frank hat dies am 0708R-Pilot ausdrücklich bestätigt:

- **Hypotaxen** statt parataktischer Schlichtheit
- **Nominalstil** wo angemessen ("die Verstetigung postdemokratischer Tendenzen")
- **Fachvokabular** ohne Scheu (Phänomenologie, Ambivalenz, Diskursverschiebung)
- **Essayistische Argumentation** mit These/Antithese/Synthese-Struktur
- Lesetext-Länge: ~600–900 Wörter, in 4–6 Absätze
- Keine pädagogische Vereinfachung, keine "leichte Sprache"

Memory-Eintrag: `feedback_c2-schreibstil.md`.

## Schreibwerkstatt-Format (verbindlich)

5 Mikroaufgaben pro Lektion. Jede Karte enthält:

- Knackige Aufgabenstellung (40–80 Wörter Erwartung)
- Kurzer Anreiz / Kontext (1–2 Sätze)
- Eigenes `<textarea>`
- Eigener "An Frank senden"-Button (`mailto`-basiert oder `formsubmit.co/frankburkert@gmx.net`)
- LocalStorage merkt "gesendet"-Zustand pro Karte

Frank hat den großen Sammelbutton "Alle senden" abgelehnt — pro Karte ein Button, weil das Schreibverhalten kleinteilig motiviert wird. Memory: `feedback_schreibwerkstatt-mikroaufgaben.md`.

## Tab-Reihenfolge (verbindlich, 8 Tabs)

1. Vorentlastung
2. Lesetext
3. Genus
4. Lückentext
5. Verständnis (MC)
6. Satzbau
7. Schreibwerkstatt
8. Wortschatz (immer letzter Tab — Memory: `feedback_wortschatz-letzter-tab.md`)

## Pexels-Bilder

Verwende ausschließlich **bereits in C1/C2-Lektionen verifizierte IDs** aus dem Pool. Kein Neusuchen für jede Lektion. Schau in fertige C2-Lektionen, wähle 8 thematisch passende IDs aus dem bestehenden Inventar. Wenn du wirklich neue brauchst: per Chrome-MCP Batch-Fetch verifizieren (Memory: `feedback_pexels-chrome.md`), Titel-Check **plus** Body-Scan auf `data:text/html` (Memory: `feedback_pexels-404-fallback.md`).

## Inhaltliche Aktualisierung (2025/26)

Lingoda-Vorlagen sind teils veraltet. Aktualisiere mit Stand 2025/26. Bereits in fertigen Lektionen verwendete und damit konsistent zu haltende Fakten:

- ChatGPT-Effekt seit Ende 2022
- Cambridge Analytica 2018 als Referenz für Datenmissbrauch
- Reichelt-Skandal 2024 (Bild)
- KKR-Springer-Übernahme 2025
- Klimaprotest-Welle abgeebbt seit 2024 (Letzte Generation aufgelöst)
- Energiekrise nach 2022 als Strukturbruch
- KI in Bildung als 2025-Topos
- Wahlen 2025 in Deutschland (Merz-Kanzlerschaft)

Wenn du neue Fakten einbringst: faktencheckbar, datierbar, nicht spekulativ. Im Zweifel WebSearch nutzen.

## Anführungszeichen — der Linter-Bug

**Kritisch.** Der Linter ersetzt nach `„` automatisch das nächste ASCII-`"` durch U+201C. In Python-Specs bricht das JS-Strings, wenn der Lückentext-Satz `„WORT"` enthält und `WORT` zwischen zwei `"` steht.

Lösung: Lücken **nicht** zwischen `„` und `"` setzen. Stattdessen: Lücke außerhalb der Anführungszeichen platzieren oder den ganzen Satz so umformulieren, dass die Lücke nicht im Zitat liegt.

Generator hat `fix_quotes()` — vor jedem Commit Regex-Check: kein `„…"` mit ASCII-U+0022 schließen. Memory: `feedback_anfuehrungszeichen-u201c.md`.

## highlightVocabInText — der Bug von 0708R

Bereits gefixt im daf-lesetext Skill. Falls du eigene Highlighting-Logik schreibst: NIEMALS `replace(regex, '\x01\x02')` — das frisst das Wort. Korrekt:

```javascript
text.replace(regex, function(match) { return '\x01' + match + '\x02'; });
```

Frank hat diesen Bug in einer h3-Überschrift entdeckt ("Vom Mythos der zur komplexen" — "Jugendsprache" war verschwunden).

## Commit-Workflow (Pflicht)

`scripts/safe-commit.sh` ist der einzige dialog-freie Weg. NIEMALS Write-Tool für `.git/*` benutzen — Cowork-Permission-Dialoge blockieren im Hintergrund unbemerkt.

Niemals SHAs, Commit-Hashes oder Push-Status im Chat berichten — Memory: `feedback_git-plumbing-silent.md`. Stumm committen, weitermachen.

## Stilregeln gegenüber Frank

- Prosa statt Bullet-Listen in der Antwort (außer er fragt explizit)
- Direkte Antworten, keine Präambel ("Lass mich das mal …")
- Selbstreflexion / dialektisches Denken willkommen
- Bei "weiter" / "mach" / Continue: stumm weiterarbeiten, kein "Okay, ich fange jetzt an" — Memory: `feedback_nie-auf-frank-warten.md`
- Cowork-Nachrichten poppen bei Frank nicht auf — wenn du wartest, wartest du allein

## Skills, die du laden musst

Vor der ersten Lektion:

- `daf-kern` (Layout, Container, Header)
- `daf-lesetext` (Lesetext-Formatierung, highlightVocabInText)
- `daf-c2` (C2-spezifisch — falls noch nicht installiert: in `outputs/daf-c2.skill` als Paket vorhanden)
- `daf-satzbau` (Drag-Drop-Pattern, niemals selbst erfinden — Memory: `feedback_satzbau-skill-pflicht.md`)
- `daf-audit` nach jeder Datei

Memory: `feedback_skill-nach-dateityp.md` — vor erstem Edit Typ-Skills laden + Inhalt prüfen.

## Header-Konvention

Untertitel **immer** mit Lektionscode: `C2 – Lektion 0407S · Sprechen` (analog für R: `· Lesen`). Memory: `feedback_header-lektionscode.md`.

Header zentrieren (text-align:center im `.header`) — häufigster Audit-Fehler. Memory: `feedback_header-zentrierung.md`.

## Was du NICHT tust

- Keine Subagenten / Task-Tool für DaF-Dateien — alles selbst, Qualität vor Geschwindigkeit. Memory: `feedback_keine-subagenten.md`
- Keine parallelen Arbeitskopien (kein "0407S_v2", kein "Entwurf")
- Keine Schreibaufgabe "schreibe einen Aufsatz von 300 Wörtern" — nur Mikroaufgaben
- Keine veralteten Kulturreferenzen (Lingoda-Texte oft 2014–2017)
- Keine ASCII-Anführungszeichen `"` in deutschen Texten
- Kein Write-Tool auf `.git/*`
- Keine Bullet-Listen in deinen Chat-Antworten an Frank

## Erste konkrete Aktion

1. `ls /sessions/.../mnt/fabDaF/htmlS/C2/DE_C2_*.html` — bestätige den IST-Stand
2. `cat /sessions/.../mnt/outputs/c2_gen.py` — vergewissere dich, dass die Pipeline noch läuft
3. `cat /sessions/.../mnt/outputs/spec_0406R.py` — Vorlage für die Spec-Struktur
4. PDF zur nächsten Lektion in `htmlS/C2/` finden (Lingoda-Datei zu 0407S)
5. Spec schreiben, generieren, committen — wie oben beschrieben
6. Weitermachen, ohne zu fragen

Frank ist DaF-Lehrer, nicht Entwickler. Er möchte ein fertiges Produkt sehen, keine Statusupdates. Pingt dich nur, wenn etwas Inhaltliches falsch ist.

Viel Erfolg. Du machst gute Arbeit.
