# AMDP-Kurs — Übergabe für die nächste Claude-Session

## Worum geht es?

Frank Burkert (DaF-Lehrer) erstellt interaktive HTML-Lernmaterialien für einen
Privatschüler namens **Mert** — Türke, B2-Niveau, in der Ausbildung zum
Psychotherapeuten in Deutschland. Ziel: alle **100 AMDP-Merkmale** lehren,
damit Mert sie im klinischen Alltag verstehen, anwenden, im Befundsatz
formulieren und im Patientengespräch abfragen kann.

AMDP = Arbeitsgemeinschaft für Methodik und Dokumentation in der Psychiatrie.
Das System ist der deutsche Standard zur psychopathologischen Befunddokumentation.

---

## Was bereits fertig ist

| Datei | Inhalt | Status |
|---|---|---|
| `DE_AMDP_000-sprachhinweis.html` | Sprachhinweis für Mert (Gendering-Ablehnung, Warum-Erklärung) | ✅ fertig + gepusht |
| `DE_AMDP_001R-einfuehrung.html` | AMDP-Überblick, 12 Domänen, Entscheidungsbaum, Beurteilungszeitraum | ✅ fertig + gepusht + Register-Verweis |
| `DE_AMDP_002R-bewusstsein.html` | Domäne I (Bewusstsein, 4 Merkmale) + Domäne II (Orientierung, 4 Merkmale) | ✅ fertig + 8 Marginalien #1–#8 |
| `Psych_Fall_A.html` | Fallvignette Delir (Herr A., 82) — Rollenspiel + AMDP-Befund + Diagnose + Therapie | ✅ fertig + 12 Nummer-Badges |
| `DE_AMDP_INDEX.html` | **Schüler-Register**: alle 100 Merkmale, 12 Domänen, Status-Symbole (✅/🎭/⬜), Klicktiefe zur Lektion | ✅ live im Dashboard |
| `AMDP_100_KANON.md` | **Single Source of Truth**: Manual-konforme Liste mit Domänen, S/F/SF-Typen | ✅ Referenz für künftige Lektionen |

---

## Quelltexte (alle in `/quelltexte/`)

| Datei | Art | Inhalt |
|---|---|---|
| `Das-AMDP-System.pdf` | Offizielles Manual (Hogrefe, 10. Aufl. 2018) | Alle 100 Definitionen, Graduierungshinweise, Abgrenzungen — **Hauptquelle** |
| `Praxisbuch AMDP.pdf` | Folienpräsentation Stieglitz (Basel 2018) | Reale Patientenzitate, Literaturbeispiele, ICD-10-Gegenüberstellung, Syndromdiagnostik |
| `AMDP Therapie.pdf` | Noch nicht ausgewertet | Vermutlich klinischer Anwendungsleitfaden |

**Wichtig:** Das eigentliche Hogrefe-Praxisbuch (mit Fallvignetten pro Symptom) liegt
**nicht** vor. Die Stieglitz-Folien sind nützlich, ersetzen es aber nicht vollständig.
Dialoge und Fallbeispiele in den Lektionen werden deshalb selbst geschrieben.

---

## Der Lehrplan — alle 100 Merkmale, 14 Lektionen

| Lektion | Domäne(n) | Merkmale # | Status |
|---|---|---|---|
| 001R ✅ | Einführung | — (Systemüberblick) | fertig |
| 002R ✅ | I Bewusstsein + II Orientierung | 1–8 | fertig |
| 003R | III Gedächtnis | 9–14 | **als nächstes** |
| 004R | IV Formales Denken (1/2) | 15–20 | offen |
| 005R | IV Formales Denken (2/2) | 21–26 | offen |
| 006R | V Befürchtungen & Zwänge | 27–32 | offen |
| 007R | VI Wahn (1/2) | 33–39 | offen |
| 008R | VI Wahn (2/2) | 40–46 | offen |
| 009R | VII Sinnestäuschungen | 47–52 | offen |
| 010R | VIII Ich-Störungen | 53–58 | offen |
| 011R | IX Affektivität (1/2) | 59–66 | offen |
| 012R | IX Affektivität (2/2) | 67–79 | offen |
| 013R | X Antrieb & Psychomotorik + XI Circadiane Besonderheiten | 80–90 | offen |
| 014R | XII Andere Störungen | 91–99 | offen |

---

## Die 100 Merkmale im Überblick (S/F/SF-Typ)

> ⚠️ **Verbindliche Quelle ist `AMDP_100_KANON.md` (Single Source of Truth).**
> Die folgende Kurzfassung ist nur Schnellüberblick. Wenn ein Merkmal in einer
> Marginalie oder einem Index-Badge benutzt wird, immer gegen den Kanon abgleichen.
> Die Schüler-sichtbare Übersicht liegt unter `DE_AMDP_INDEX.html`.

**I. Bewusstseinsstörungen (1–4):** Bewusstseinsverminderung(F), Bewusstseinstrübung(F),
Bewusstseinseinengung(SF), Bewusstseinsverschiebung(S)

**II. Orientierungsstörungen (5–8):** Zeitlich(S), Örtlich(S), Situativ(S),
Über die eigene Person(S)

**III. Aufmerksamkeits- und Gedächtnisstörungen (9–14):** Auffassungsstörungen(SF),
Konzentrationsstörungen(SF), Merkfähigkeitsstörungen(SF), Gedächtnisstörungen(SF),
Konfabulationen(F), Paramnesien(S)

**IV. Formale Denkstörungen (15–26):** Gehemmt(S), Verlangsamt(F), Umständlich(F),
Eingeengt(F), Perseverierend(F), Grübeln(S), Gedankendrängen(S), Ideenflüchtig(F),
Vorbeireden(F), Gesperrt/Gedankenabreißen(SF), Inkohärent/zerfahren(F), Neologismen(F)

**V. Befürchtungen und Zwänge (27–32):** Misstrauen(SF), Hypochondrie(S), Phobien(S),
Zwangsdenken(S), Zwangsimpulse(S), Zwangshandlungen(S)

**VI. Wahn (33–46):** Wahnstimmung(S), Wahnwahrnehmung(S), Wahneinfall(S),
Wahngedanken(S), Systematisierter Wahn(S), Wahndynamik(SF), Beziehungswahn(S),
Beeinträchtigungs- und Verfolgungswahn(S), Eifersuchtswahn(S), **Schuldwahn(S)**,
Verarmungswahn(S), Hypochondrischer Wahn(S), Größenwahn(S), Andere Wahninhalte(S)

**VII. Sinnestäuschungen (47–52):** Illusionen(S), Stimmenhören(S),
Andere akustische Halluzinationen(S), Optische Halluzinationen(S),
Körperhalluzinationen(S), Geruchs- und Geschmackshalluzinationen(S)

**VIII. Ich-Störungen (53–58):** Derealisation(S), Depersonalisation(S),
Gedankenausbreitung(S), Gedankenentzug(S), Gedankeneingebung(S),
Andere Fremdbeeinflussungserlebnisse(S)

**IX. Störungen der Affektivität (59–79):** Ratlos(F), **Gefühl der Gefühllosigkeit(S)**,
Affektarm(F), Störung der Vitalgefühle(S), Deprimiert(SF), Hoffnungslos(S),
Ängstlich(SF), Euphorisch(SF), Dysphorisch(SF), Gereizt(SF), Innerlich unruhig(S),
Klagsam/jammrig(F), Insuffizienzgefühle(S), Gesteigertes Selbstwertgefühl(S),
Schuldgefühle(S), Verarmungsgefühle(S), Ambivalent(S), Parathymie(F),
Affektlabil(SF), Affektinkontinent(SF), Affektstarr(F)

**X. Antriebs- und psychomotorische Störungen (80–88):** **Antriebsarm(SF)**,
Antriebsgehemmt(S), Antriebsgesteigert(SF), Motorisch unruhig(SF), Parakinesen(F),
Manieriert/bizarr(F), Theatralisch(F), Mutistisch(F), Logorrhoisch(F)

**XI. Circadiane Besonderheiten (89–91):** Morgens schlechter(SF),
Abends schlechter(SF), Abends besser(SF)

**XII. Andere Störungen (92–100):** Sozialer Rückzug(SF), Soziale Umtriebigkeit(SF),
Aggressivität(SF), Suizidalität(SF), Selbstbeschädigung(SF),
Mangel an Krankheitsgefühl(S), Mangel an Krankheitseinsicht(S),
Ablehnung der Behandlung(SF), Pflegebedürftigkeit(SF)

**Typ-Legende:** S = Selbstbeurteilung möglich · F = Fremdbeurteilung nötig · SF = beide

> **Korrektur-Hinweise (2026-05-23):** In früheren Versionen dieser Datei standen
> drei nicht-kanonische Begriffe: #42 als „Religiöser Wahn" (korrekt: Schuldwahn),
> #60 fehlte ganz (korrekt: Gefühl der Gefühllosigkeit), #80 als „Nicht
> schwingungsfähig" (korrekt: Antriebsarm). Außerdem war die Domänen-Grenze
> XI/XII verschoben. Alles aus dem Hogrefe-Manual (10. Aufl. 2018) korrigiert.

---

## Aufbau einer AMDP-Lektion (R-Datei)

Jede Lektion folgt dem fabDaF-Standard mit diesen Skills (IMMER in dieser
Reihenfolge lesen, bevor du anfängst):

1. `daf-kern` — Layout, Nav, Footer, Quasthoff, Direct-Feedback
2. `daf-lesetext` — Lesetext-Formatierung, Dialoge, Vorentlastung, Richtig/Falsch
3. `daf-schreibwerkstatt` — 5 Mikroaufgaben, Web3Forms, formsubmit-Fallback
4. `daf-uebungsformen` — Lückentext, Multiple Choice, Zuordnung
5. `daf-satzbau` — wenn Satzbau-Tab vorhanden
6. `daf-audit` — IMMER ZULETZT nach Fertigstellung

### Tab-Struktur (Standard für AMDP-R-Dateien)

1. **Vorentlastung** — Wortschatz-Karten + erste Orientierung im Thema
2. **Lesetext** — Fließtext mit eingebetteten Dialogen (Arzt–Patient-Szenen)
3. **Richtig oder Falsch** — 6–8 Aussagen zum Lesetext
4. **Lückentext** — 8–10 Lücken mit Wortbank
5. **Satzbau** — Chip-Drag-Drop (aus Manual-Sätzen)
6. **Schreibwerkstatt** — 5 Mikroaufgaben, Web3Forms-Versand an Frank
7. **Wortschatz** — IMMER letzter Tab, Vokabelkarten mit Pexels-Bilder

### Was jede Lektion leisten soll (Lernziele für Mert)

- Verstehen: Was bedeutet der Begriff klinisch-präzise?
- Abgrenzen: Wozu ist er NICHT zu verwechseln? (z.B. Zeitgitterstörung ≠ Orientierungsstörung)
- Graduieren: leicht / mittel / schwer
- Befund formulieren: „Der Patient zeigt eine ausgeprägte X, erkennbar an…"
- Interview führen: Welche Fragen stelle ich dem Patienten?

---

## Wichtige inhaltliche Regeln

**Kein Gendern.** Nie. Weder Doppelpunkt, noch Sternchen, noch Binnen-I.
„Therapeuten, Patienten, Behandler" — das ist die Form. Frank hat das explizit
klargestellt. Verstöße dagegen sind ein schwerer Fehler.

**ICD-10-Brücke.** Mert hat einen therapie.de-Link (ICD-10 F00–F99) mitgeschickt —
Signal, dass er den Bezug zur Diagnosestellung braucht. Die relevanten Domänen:
- Wahn + Sinnestäuschungen + Ich-Störungen → F20–F29 (Schizophrenie-Spektrum)
- Affektivität + Antrieb → F30–F39 (affektive Störungen)
- Zwänge → F42, Phobien → F40
Diese Brücke gehört als Infokasten in die jeweiligen Lektionen, **nicht** als
eigene Lektion.

**Quelltexte nutzen.** Vor jeder neuen Lektion die relevanten Abschnitte aus
`Das-AMDP-System.pdf` per `pdftotext` extrahieren und auswerten. Die Stieglitz-Folien
(`Praxisbuch AMDP.pdf`) für Patientenzitate und ICD-10-Querverweise.

**Befundsatz-Sprache.** Immer im klinischen Stil: „Der Patient zeigt…",
„Fremdanamnestisch berichtet…", „Im Gespräch fällt auf…".

**Dialoge.** Jede Lektion hat mindestens eine Arzt–Patient-Dialogszene im Lesetext.
Die Dialoge zeigen die AMDP-Merkmale in Aktion — nicht abstrakt erklären, sondern
zeigen wie sie sich im echten Gespräch äußern.

---

## Git-Workflow (Cowork-Sandbox)

```bash
# Credentials einmalig pro Session aktivieren:
bash /sessions/clever-ferrant-mccarthy/mnt/fabDaF/scripts/setup-sandbox-credentials.sh

# Commit + Push:
bash scripts/safe-commit.sh "Commit-Nachricht" datei1 [datei2 …]
```

Das Repo heißt `daf-amdp` (oder liegt im B2-Repo, je nach Dashboard-Konfiguration).
Vor dem Push JS-Syntax prüfen wenn `dashboard.html` betroffen:
```bash
node -e "const vm=require('vm'); vm.compileFunction(require('fs').readFileSync('...','utf8'))"
```

---

## Was als nächstes zu tun ist

**003R — Domäne III: Gedächtnis (Merkmale 9–14)**

Merkmale: Auffassungsstörungen, Konzentrationsstörungen, Merkfähigkeitsstörungen,
Gedächtnisstörungen, Konfabulationen, Paramnesien

Inhaltliche Schwerpunkte laut Manual:
- Unterschied Merkfähigkeit (Kurzzeit) vs. Gedächtnis (Langzeit)
- Konfabulation: unbewusst falsche Erinnerungen, kein Lügen
- Paramnesien: Déjà-vu, Jamais-vu, Erinnerungsverfälschungen
- Klassisches Patientenbild: Korsakow-Syndrom (Alkohol, Thiaminmangel)
- Abgrenzung zu Konzentrationsstörungen (F→ fremdbeurteilbar)

Vorab Manual-Abschnitte extrahieren:
```bash
pdftotext "/sessions/clever-fervent-mccarthy/mnt/fabDaF/quelltexte/Das-AMDP-System.pdf" - | grep -A 40 "Auffassungsstörung\|Merkfähigkeit\|Konfabulation\|Paramnesie"
```

---

*Erstellt am 2026-05-11 · Übergabe-Dokument für AMDP-Lektionskurs (Mert)*
