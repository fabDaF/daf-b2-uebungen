# Übergabe: A1-Drill-Serie abgeschlossen (Stand 2026-04-23)

Dieses Dokument ist das Gegenstück zu `HANDOVER_A1_DRILLS.md`. Das alte
HANDOVER beschreibt, was offen war. Dieses hier beschreibt, was jetzt
steht, was dabei gelernt wurde und was für eine spätere Session sinnvoll
anzugehen wäre. Lies es zuerst, wenn du nach dieser Session neu einsteigst.

## Was automatisch schon da ist

CLAUDE.md im fabDaF-Root ist projekt-globale Pflichtlektüre und wird
automatisch geladen. Ebenso `~/.auto-memory/MEMORY.md` — inzwischen mit
drei neuen Einträgen, die aus dieser Session entstanden sind
(`feedback_drill-badge-verrat.md`, `feedback_drill-karten-mischen.md`,
`feedback_franks-drill-pattern.md`). Alle Skills sind verfügbar. Das
alte HANDOVER (`HANDOVER_A1_DRILLS.md`) kann weiterhin als historisches
Referenzdokument gelesen werden, ist aber in seiner Funktion abgelöst.

## Wer Frank ist und wie er arbeitet

Unverändert: DaF-Lehrer, kein Entwickler, bevorzugt Prosa-Antworten ohne
Präambel, keine Bullet-Listen in normalen Antworten, keine Subagenten
für DaF-Dateien. Dialektisches Denken (These/Antithese/Synthese) und
Selbstreflexion werden geschätzt. Datensicherheit > Git-Eleganz.
Commit/Push läuft automatisch über `scripts/safe-commit.sh` plus
post-commit-Hook. Eine neue Beobachtung aus dieser Session: Frank
erwartet von dir, dass du Chrome-MCP-Probleme selbst löst, statt ihn um
Manipulationen am Browser zu bitten. Das ist deine Aufgabe, nicht seine.

## Was jetzt steht — die komplette Serie FD01 bis FD41

Die ursprüngliche morphologische Arbeit (FD01 bis FD29) war bei
Session-Beginn schon fertig. In dieser Session sind zwölf weitere
Einheiten dazugekommen. Der morphologische Abschluss FD30 bis FD34
schließt die Lücken, die im alten HANDOVER als Pflicht-Restarbeit
beschrieben waren: FD30 Plural der Nomen, FD31 Komparativ und
Superlativ, FD32 Ordinalzahlen mit Datumsangaben, FD33 Konjunktiv II
als Höflichkeit (hätte, wäre, könnte, möchte), FD34 Reflexivpronomen
mit A1-Kernverben. Der pragmatische Block, der im alten HANDOVER nur
als Skizze existierte, ist jetzt als FD35 bis FD41 vollständig
ausgearbeitet: FD35 ja/nein/doch, FD36 schon/noch/erst/nur, FD37
kein/nicht, FD38 Indefinitpronomen (etwas/nichts/jemand/niemand/viel/
viele/ein paar/ein bisschen), FD39 Länder mit und ohne Artikel plus
Präpositionen (in/nach/aus), FD40 Uhrzeit umgangssprachlich und
offiziell im Kontrast, FD41 Mengen- und Verpackungsangaben. Alle zwölf
neuen Dateien sind committed, gepusht, im Dashboard verlinkt und auf
`fabdaf.github.io/daf-a1-uebungen/franks-drill/` live.

## Qualitätssicherung — was geprüft ist und was nicht

Jede neue Datei hat zwei Test-Stufen bestanden. Stufe eins ist ein
statischer Code-Audit: 48 Items in drei Runden, Tally-Keys konsistent
zu HTML-IDs, keine ASCII-Anführungszeichen hinter deutschen
Anführungen, Hide-Regel für Cat-Badges vor Lösung vorhanden, catLabel
ohne Spoiler, leere Placeholder, korrekter Halbgeviertstrich im
Untertitel. Stufe zwei ist ein Browser-Test über Chrome-MCP gegen die
live-deployte Version: DRILL-Objekt existiert, Sections lassen sich
wechseln, Header ist zentriert, Badge ist vor Lösung per
getComputedStyle unsichtbar, Input-Simulation mit falscher Eingabe
setzt `.wrong`, mit korrekter `.correct`, resetRunde setzt zurück.
Protokoll siehe `htmlS/A1.1 NEW/franks-drill/TEST_PROTOKOLL_FD30-39.md`
(Name historisch, Inhalt erfasst FD30 bis FD41). Was explizit nicht
maschinell geprüft wurde und für eine spätere Stichprobe offen bleibt:
inhaltliche Natürlichkeit der 576 neuen Beispielsätze, Timer-Laufzeit
über die ersten Sekunden, Streak-Reset bei falscher Eingabe,
Fisher-Yates-Mischung bei jedem Laden, Mobile-Darstellung unter 600 px.

## Die Spoiler-Regel — neu in dieser Session

Eine wichtige Design-Regel ist erst in dieser Session scharf geworden
und muss für alle zukünftigen FDxx-Dateien und vergleichbare Drills
gelten: Das Cat-Badge an einer Karte darf die Antwort nicht verraten,
bevor die Aufgabe gelöst ist. Konkret zwei Maßnahmen. Erstens muss die
CSS-Regel `.pf-card[data-solved="0"] .cat-badge { visibility: hidden; }`
vorhanden sein, damit das Badge vor der Lösung unsichtbar ist und erst
nach dem Lösen erscheint. Zweitens darf die `catLabel()`-Funktion
keine konkreten Antwort-Informationen in den Badge-Text schreiben —
kein „sein → war", kein „mask./neutr. → dem", keine Artikel,
Partizipien, Formen oder Umlaut-Hinweise. Erlaubt sind nur Kategorie-
Namen, die auch ohne gelöste Aufgabe keine Hilfe geben (zum Beispiel
„mask.", „fem.", „Plural", „schwaches Verb"). Diese Regel ist als
Memory-Eintrag `feedback_drill-badge-verrat.md` gesichert; sie ist in
den alten FDxx-Dateien (unter FD20) inzwischen nachgezogen und gilt
für alle neuen.

## Was als nächstes sinnvoll wäre — und was nicht

Die ursprünglich im HANDOVER skizzierten Pragmatik-Kandidaten sind
abgearbeitet. Was theoretisch noch käme: gern/lieber/am liebsten als
Präferenzketten, Höflichkeitsfloskeln (Könnten Sie …, Würden Sie …,
Dürfte ich …) als Satzbau- statt Lücken-Drill, Konnektoren (weil, denn,
aber, oder, und, deshalb, trotzdem) als Entscheidungsübung zwischen
Haupt- und Nebensatz-Logik. Das sind aber keine A1-Lücken mehr,
sondern Brücken zu A2 und darüber hinaus. Meine Empfehlung: die
bestehenden einundvierzig Einheiten erst im Unterricht ausprobieren
lassen, dann sehen, welche Themen in der Praxis wackeln. Drill-Material
zu bauen, bevor der Bedarf klar ist, ist teurer als es nachträglich zu
ergänzen. Eine mögliche nicht-neue Arbeit wäre, einzelne FDxx-Drills
aus den jeweiligen R/G/V/X-Lektionen heraus als weiterführendes
Training zu verlinken, wenn thematisch passend — das ist eine
Integrations-Aufgabe in den Lesetext-, Grammatik- und Textarbeits-
Dateien, nicht in der Drill-Serie selbst.

## Commit-Workflow in Kürze

Unverändert zum alten HANDOVER. FDxx-Dateien liegen im A1-Subrepo
(`htmlS/A1.1 NEW`), das Dashboard liegt im B2-Root. Also zwei Commits
pro neuer oder geänderter Drill-Datei:

```bash
cd "/Users/frankburkert/Cowork/Projekte/fabDaF/htmlS/A1.1 NEW"
/Users/frankburkert/Cowork/Projekte/fabDaF/scripts/safe-commit.sh \
  "FDxx — Titel" franks-drill/DE_A1_FDxx-*.html

cd "/Users/frankburkert/Cowork/Projekte/fabDaF"
./scripts/safe-commit.sh "dashboard: add FDxx" htmlS/dashboard.html
```

Niemals mit Write-Tool in `.git/` schreiben. Kosmetische Lock-Warnungen
beim Commit sind normal, solange `git rev-parse HEAD origin/main`
gleiche SHAs liefert.

## Pflicht-Skills bei Arbeit an bestehenden FDxx-Dateien

`daf-kern` als Fundament, `daf-grammatik` für Übungsformen, `daf-audit`
als Qualitätskontrolle vor dem Commit. Plus die in dieser Session
gefestigten Memory-Einträge zum Drill-Pattern und zur Spoiler-Regel.
`daf-test` lohnt sich, wenn ein Browser-Test gegen Live-Deployment
gemacht werden soll — Chrome muss dafür laufen, `createIfEmpty:true`
beim Tab-Anlegen verwenden.

## Was Frank beim Start eines neuen Threads sinnvoll schreiben könnte

Wenn es um die A1-Drill-Serie als Ganzes geht: „Lies
HANDOVER_A1_DRILLS_COMPLETE.md." Dann weißt du, wo die Serie steht, was
geprüft ist, welche Regeln gelten. Wenn Frank eine einzelne FDxx-Datei
nachschärfen will (Beispiele austauschen, Items neu mischen,
Kategorie-Balance korrigieren), reicht der Hinweis auf die Datei —
Design-Pattern und Spoiler-Regel sind dann über die Memory-Einträge
abrufbar. Für neue Drill-Einheiten außerhalb des A1-Horizonts wäre ein
neues HANDOVER der sauberere Weg, statt dieses hier weiterzuschreiben.
