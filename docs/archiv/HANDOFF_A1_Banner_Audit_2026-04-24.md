# Handoff: A1 Bild-Audit — Phase 1 erledigt, Phase 2 ausstehend

**Stand:** 2026-04-24 · Commit `ca32e1a` im Repo `daf-a1-uebungen`
**Zweck dieser Datei:** Kontext für einen frischen Claude-Thread, damit nicht bei Null begonnen wird.

---

## TL;DR

Im A1-Ordner (`htmlS/A1.1 NEW/`) waren 362 Banner-Bilder an thematisch falscher Stelle. Phase 1 (11 R-Dateien, 143 Banner) ist erledigt — aber die Audit-Diagnose war irreführend: Es war kein Austauschproblem, sondern ein Cleanup-Problem. Diese Erkenntnis ist zentral für Phase 2.

---

## Der Audit-Report im Original

Automatisierter Audit aller 188 HTML-Dateien im Ordner `htmlS/A1.1 NEW/`.
Befund: 83 Dateien mit 362 Banner-Fehlzuordnungen.

### Die fünf generischen Banner

| Hash | Motiv | Gesamt | Legitim | Fehl am Platz |
|---|---|---|---|---|
| `a15f1503bf` | Wörterbuch-Foto (Wortschatz) | 167 | 101 | 66 |
| `2e0dbb5872` | Holz-Puzzle (Satzbau) | 107 | 100 | 7 |
| `6f44101748` | Tafel + Schülerin (Vorentlastung/Alphabet) | 82 | 13 | 69 |
| `b9397b0d3d` | Lehrerin an Tafel (Grammatik) | 79 | 2 | 77 |
| `2616198d76` | Buchrücken (Geschichte) | 155 | 12 | 143 |

### Phasen-Aufteilung laut Audit

- **Phase 1 — 11 R-Dateien:** 143 Buchrücken-Banner (ERLEDIGT ✓)
- **Phase 2a — G-Dateien (Grammatik):** Banner durch thematische ersetzen
- **Phase 2b — V/C/X-Dateien:** Wortschatz/Lerncheck/Textarbeit

Zusammen **72 Dateien mit 219 Fehlzuordnungen** in Phase 2.

---

## Was Phase 1 wirklich war — wichtige Erkenntnis

Der Audit empfahl: „pro Geschichte 13 thematische Pexels-Banner suchen" — das war falsch.

**Echte Struktur pro R-Datei (vor Fix):**

```
7 Nav-Tabs: Vorentlastung, Geschichte, Genus, Lückentext, MC, Satzbau, Wortschatz
20 <img class="tab-banner">-Elemente   ← 13 zu viel

sec-0 (Vorentlastung):  [Vorentlastung] [Geschichte]    [Genus]
sec-1 (Geschichte):     [Lückentext]    [MC]
sec-2 (Genus):          [Satzbau]       [Wortschatz]    [Tab 8]
sec-3 (Lückentext):     [Tab 9]         [Tab 10]        [Tab 11]
sec-4 (MC):             [Tab 12]        [Tab 13]        [Tab 14]
sec-5 (Satzbau):        [Tab 15]        [Tab 16]        [Tab 17]
sec-6 (Wortschatz):     [Tab 18]        [Tab 19]        [Tab 20]
```

Banner waren Cruft aus fehlgeschlagenem Bulk-Insert, teilweise mitten in `<div class="section-title">`-Blöcke gestopft. Fix-Strategie war **Cleanup statt Replacement** — alle 20 raus, dann 7 korrekte pro Datei an den richtigen Ort (direkt nach `<div class="section" id="sec-N">`).

**Für Phase 2 heißt das:** Erst die tatsächliche Struktur der G/V/C/X-Dateien prüfen, bevor man Pexels-Bilder besorgt. Möglicherweise liegt auch dort strukturelles Cruft vor, das erst raus muss.

---

## Phase 1: Die 11 R-Dateien — was hineinkam

Alle haben jetzt genau 7 Banner. 6 davon Kategorie-Banner (wiederverwendet aus 1014R), einer story-spezifisch per Pexels.

| Code | Datei | Story-Banner (Pexels-Titel) | ID |
|---|---|---|---|
| 1014R | montag-in-berlin | Lights on Berlin Street, Cathedral and Fernsehturm | 19615598 |
| 1024R | die-party | People Having A Party (Konfetti) | 5970895 |
| 1034R | omas-geburtstag | Mother and Grandmother With a Boy | 27176987 |
| 1054R | ein-wochenende-in-berlin | Brandenburg Gate in Berlin, Iconic Landmark | 37120347 |
| 1064R | glueckliche-huehner | Flock of Colorful Chickens on a Farmyard | 30973422 |
| 2014R | alex-der-schriftsteller | Close-up Photography of Typewriter („Only a Writer Knows") | 1576302 |
| 2024R | ein-besuch | Two Women at Home | 7128344 |
| 2034R | der-arzttermin | Doctor Checking the Heart of a Woman | 5214992 |
| 2044R | freundinnen-beim-shoppen | Woman Smiling While Choosing Clothes with a Friend | 8387129 |
| 2054R | cooler-urlaub-in-new-york | Sunset Over Brooklyn Bridge and NYC Skyline | 33619969 |
| 2064R | feste | Oktoberfest Beer Steins Display in Munich | 28702296 |

Commit-Nachricht: `A1 R-Dateien: 20→7 Banner-Cleanup — Buchrücken-Cruft entfernt, 7 korrekte Banner pro Datei (1 story-spezifisch + 6 Kategorie)`
Commit-Hash: `ca32e1a53717a3c4192b15c747f82e40ecd925fc` (main in `fabDaF/daf-a1-uebungen`)

---

## Phase 2 — Was noch ansteht

### Phase 2a: G-Dateien (Grammatik), Top-20 Übeltäter

| Datei | Anzahl | Beispiel-Alts |
|---|---|---|
| 1000G-der-die-das-genus | 6 | „der · die · das?", „der Löwe", „die Frau" |
| 1023G-regelmaessige-verben-im-praesens | 6 | „Entdeckung", „Pronomen", „Pronomen einsetzen" |
| 1053G-verben-mit-vokalwechsel | 5 | „Entdeckung", „Vokaltyp", „du-Form" |
| 1093G-die-verneinung-im-deutschen | 5 | „Entdecken", „nicht oder kein?" |
| 1103G-nominativ-und-akkusativ | 5 | „Entdecken", „Nom. oder Akk.?" |
| 2021V-meine-stadt + -uebungen | 5 je | „Kulturorte", „Himmelsrichtungen" |
| 2031V-geschaefte + -uebungen | 5 je | „Geschäfte & Dienstleistungen", „bei oder zu?" |
| 1071V-die-wochentage | 4 | „Werktag / Wochenende", „am + Wochentag" |
| 1073G-monate-daten-und-jahre | 4 | „Ordnungszahlen", „Datum schreiben" |
| 1083G-die-wortstellung-im-deutschen | 4 | „Satztypen", „Zwei Verben" |
| 1091V-hobbys-und-freizeit | 4 | „Hobby-Kategorien", „spielen + Akk." |
| 1101V-essen-und-trinken | 4 | „essen/trinken/mögen", „Lieblings-" |
| 1111V-verkehrsmittel | 4 | „Öffentlich oder privat?", „nehmen konjugieren" |
| 1113G-der-dativ-nach-praepositionen | 4 | „Nom. / Dat.", „mit + Dativ" |
| 1121V-beim-buergeramt | 4 | „brauchen oder müssen?" |
| 1123G-die-modalverben | 4 | „Bedeutung", „Konjugation" |
| 1124C-to-do-liste-schreiben | 4 | „Possessivartikel", „Modalverben" |
| 2012G-possessivartikel + -uebungen | 4 je | „sein oder ihr?", „Possessivartikel" |

(vollständige Liste aus dem Audit-Report sollte 72 Dateien umfassen)

### Phase 2b: V/C/X-Dateien

Vokabular/Lerncheck/Textarbeit — meist 1–3 Fehlzuordnungen pro Datei.

---

## Assets und Werkzeuge

### Wiederverwendbare Banner (für Phase 2 relevant)

- `~/Cowork/Projekte/fabDaF/outputs/r_category_banners.json` (ephemer, nur diese Session) enthält die 6 Kategorie-Banner als Base64-Data-URLs:
  Vorentlastung, Genus, Lückentext, Multiple Choice, Satzbau, Wortschatz

- Die 6 Kategorie-Banner sind auch **in jeder der 11 R-Dateien** als base64 embedded — ein neuer Thread kann sie also aus einer beliebigen R-Datei extrahieren (z.B. aus `DE_A1_1014R-montag-in-berlin.html`).

### Cleanup-Skript-Pattern

`outputs/cleanup_r_banners.py` (ephemer). Kernlogik:

```python
# 1. Alle bestehenden tab-banner imgs entfernen
remove_pat = re.compile(r'\n[ \t]+<img class="tab-banner"[^>]*?>', re.DOTALL)
cleaned, n1 = remove_pat.subn('', content)
fallback_pat = re.compile(r'<img class="tab-banner"[^>]*?>', re.DOTALL)
cleaned, n2 = fallback_pat.subn('', cleaned)

# 2. Pro Section genau einen neuen Banner einfügen
for sec_idx, (alt, data_url) in enumerate(per_section_banners):
    new_banner = f'\n  <img class="tab-banner" src="{data_url}" alt="{alt}">'
    section_open_pat = re.compile(
        r'(<div class="section(?:[^"]*)"\s+id="sec-' + str(sec_idx) + r'">)'
    )
    cleaned = section_open_pat.subn(r'\1' + new_banner, cleaned, count=1)[0]
```

### Pexels-Workflow (bewährt)

1. Downloads-Ordner mounten: `mcp__cowork__request_cowork_directory` mit `~/Downloads`
2. Chrome-Tab auf pexels.com navigieren
3. **Suche** per `Promise.all`-fetch: Kandidaten-IDs aus Search-HTML extrahieren
4. **Titel-Verifikation** per `Promise.all`-fetch: Pexels-Seitentitel matchen
   - Regex-Pflicht: `/<title[^>]*>([^<]+)<\/title>/` (NICHT `<title>`)
5. Beste Treffer auswählen, **visuell im Browser verifizieren** (Titel allein reichen nicht)
6. Batch-Download als Base64 → JSON-Blob → `a.click()` in Downloads
7. Base64-Bilder aus JSON ins HTML einsetzen (semantische Keys, nicht numerische IDs)

### Git-Workflow

```bash
cd "htmlS/A1.1 NEW"  # oder anderes Repo-Root
/sessions/wonderful-festive-faraday/mnt/fabDaF/scripts/safe-commit.sh \
  "Commit-Message" datei1 datei2 ...
```

Das Skript umgeht APFS-Locks. Der `.git/objects/*/tmp_obj_*`-Warnings sind kosmetisch.

### Browser-Test auf GitHub Pages

Nach Commit ~30s warten, dann:

```
https://fabdaf.github.io/daf-a1-uebungen/DE_A1_XXXX.html
```

Cache-buster mit `?v=N` falls nötig.

---

## Skills, die relevant sind

Zu laden beim Start:

1. **daf-kern** — Layout-Fundament, Banner-Pflicht, Anführungszeichen
2. **daf-lesetext** — Für R-Dateien (Serifenschrift, R/F-Layout, Vokabel-Hervorhebung)
3. **daf-grammatik** — Für G/V/C-Dateien (Grammatik/Vokabelübungen)
4. **pexels-bild-check** — Batch-Verifikation von Pexels-IDs per Chrome-MCP
5. **daf-audit** (NACH Abschluss) — Qualitätsprüfung

---

## Offene Befunde, die außerhalb des aktuellen Scopes lagen

- `DE_A1_1044R-neuanfang.html` hat 7 Banner, 1 davon Buchrücken (Geschichte-Tab). Nicht im Audit-Report gelistet, also wahrscheinlich bereits einmal anders strukturiert. Könnte man aufräumen, gehörte aber nicht zu Phase 1.
- `DE_A1_103V-eins-zwei-drei` (im Audit mit 1 Fehlzuordnung): Dateiname anders als normale V-Dateien (fehlendes 1. Zeichen?), prüfen.

---

## Empfohlener Einstieg für neuen Thread

```
Lies ~/Cowork/Projekte/fabDaF/HANDOFF_A1_Banner_Audit_2026-04-24.md
für den vollen Kontext. Wir setzen mit Phase 2a fort: die G-Dateien
mit den stärksten Fehlzuordnungen. Starte mit 1000G-der-die-das-genus
(6 Banner) und analysiere ZUERST die tatsächliche Struktur (wie in Phase 1
gelernt: nicht blind replacement, erst prüfen ob cleanup nötig ist).
```
