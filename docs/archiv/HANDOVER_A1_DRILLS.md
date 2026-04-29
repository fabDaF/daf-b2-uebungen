# Übergabe: A1-Drill-Serie — Übergang Morphologie → Pragmatik

Dieses Dokument ist eine Thread-Übergabe. Lies es am Anfang einer neuen Session,
bevor du mit Frank weiterarbeitest. Kurz gehalten, damit es kein Token-Budget frisst.

## Was automatisch schon da ist

CLAUDE.md im fabDaF-Root ist projekt-globale Pflichtlektüre und wird automatisch
geladen. Ebenso `~/.auto-memory/MEMORY.md`. Die dortigen Einträge musst du nicht
hier duplizieren. Alle Skills sind verfügbar.

## Wer Frank ist und wie er arbeitet

DaF-Lehrer, kein Entwickler. Will Prosa-Antworten ohne Präambel, keine Bullet-Listen
in normalen Antworten, keine Subagenten für DaF-Dateien. Schätzt dialektisches
Denken (These/Antithese/Synthese) und Selbstreflexion. Datensicherheit > Git-Eleganz.
Commit/Push läuft automatisch über `scripts/safe-commit.sh` und einen post-commit-Hook.

## Der aktuelle Arbeitsblock

A1-Drill-Serie („Franks Drill", FDxx) im Pfad
`htmlS/A1.1 NEW/franks-drill/DE_A1_FDxx-*.html`. Jede Datei 48 Items in drei
Runden à 16, Fisher-Yates-Shuffle, Chip-mit-Emoji-und-Farbe, Auto-Focus,
Live-Feedback, Streak-Zähler, Timer, Bestzeit, Tally-Boxen mit
kategorie-spezifischen Countern. Design-Pattern ist in den Memory-Einträgen
„Franks-Drill Design-Pattern" und „Drill-Karten mischen" dokumentiert.

## Was fertig ist

Die Drills FD01 bis FD29 stehen, committed, gepusht, im Dashboard verlinkt.
Abgedeckt ist damit die morphologische Hauptarbeit für A1:

- FD01–03 Adjektive und Adjektivdeklination
- FD04–06 Akkusativ mit Adjektiv/Possessiv
- FD07–09 Dativ mit Adjektiv/Possessiv
- FD10 Kasus-Mix
- FD11 Präsens unregelmäßig
- FD12 Personalpronomen
- FD13 Modalverben
- FD14 Trennbare Verben
- FD15 Imperativ
- FD16–22 Perfekt in allen Varianten (schwach, stark, trennbar, ohne ge-, Mix, Megamix)
- FD23–25 Präteritum sein/haben, Modalverben, Vergangenheits-Megamix
- FD26–29 Präpositionen (Dativ, Akk, Wechsel, Megamix)

## Was noch zu tun ist — und das konzeptionelle Framing

Wir haben in der letzten Unterhaltung eine Unterscheidung erarbeitet, die dich
leiten sollte: **morphologisch vs. pragmatisch**. Frank hat eingestanden, dass
er sich vor pragmatischem Unterricht drückt, weil er nicht das etablierte
Drill-Material dahinter hat. Meine These — bitte beibehalten: Pragmatik ist
nicht eigentlich schwerer als Morphologie, sie ist nur material-ärmer. Und
genau dieses Material können wir mit der Drill-Pipeline liefern, indem wir das
Item-Format leicht umstellen (Frage → Antwortpartikel statt Lücke → Artikel).

Die Planung daraus:

**Morphologischer Abschluss als FD30–FD34** — fünf Einheiten, die echte Lücken
sind und vor dem Pragmatik-Block geschlossen werden sollten:

- FD30 Plural der Nomen (fünf Klassen: -e, -er, -en/-n, -s, Null mit Umlaut)
- FD31 Komparativ und Superlativ (regulär + Unregelmäßige: gut/besser, groß/größer, hoch/höher, viel/mehr)
- FD32 Ordinalzahlen (der erste/zweite/dritte …, inkl. Datumsangaben „am 5. Mai")
- FD33 Konjunktiv II als Höflichkeit (hätte, wäre, könnte, möchte — als Formen-Paradigma)
- FD34 Reflexivpronomen (mich/mir, dich/dir, sich) mit A1-Kernverben (sich freuen, sich setzen, sich waschen, sich treffen)

**Pragmatischer Block ab FD35** — erste Einheit ist gesetzt:

- FD35 ja / nein / doch — Antwortpartikel bei bejahter vs. verneinter Frage.
  Format: Frage als Item, drei Optionen als Antwort. Entdeckungs-Einstieg
  über Mini-Dialoge, Kontrast-Tabelle, Drill über 48 Items in drei Runden
  (R1 ja/nein-Entscheidung, R2 doch-Kontrast, R3 Megamix).

Weitere Pragmatik-Kandidaten, die wir diskutiert haben und die als FD36ff. in
Frage kommen: schon/noch/erst/nur-Kontraste, kein vs. nicht-Entscheidung,
Indefinit-Feld (etwas/nichts/jemand/niemand/viel/viele/ein paar/ein bisschen),
gern/lieber/am liebsten, Länder/Nationalitäten mit/ohne Artikel, Uhrzeit
umgangssprachlich vs. offiziell, Mengen- und Verpackungsangaben.

## Commit-Workflow in Kürze

FDxx-Dateien liegen im A1-Subrepo (`htmlS/A1.1 NEW`), das Dashboard liegt im
B2-Root. Also zwei Commits pro neuer Datei:

```bash
cd "/sessions/keen-busy-curie/mnt/fabDaF/htmlS/A1.1 NEW"
/sessions/keen-busy-curie/mnt/fabDaF/scripts/safe-commit.sh \
  "FD30 — Plural der Nomen" franks-drill/DE_A1_FD30-plural.html

cd "/sessions/keen-busy-curie/mnt/fabDaF"
./scripts/safe-commit.sh "dashboard: add FD30" htmlS/dashboard.html
```

Niemals mit Write-Tool in `.git/` schreiben. Kosmetische Lock-Warnungen beim
Commit sind normal, solange `git rev-parse HEAD origin/main` gleiche SHAs
liefert.

## Pflicht-Skills pro FDxx-Datei

`daf-kern` als Fundament, `daf-grammatik` für die Übungsformen, `daf-satzbau`
falls ein Drag-Drop-Tab dazu kommt (aktuell nicht der Fall für FDxx), und zum
Schluss `daf-audit` als Qualitätskontrolle. Nach jedem fertigen FDxx immer das
Dashboard-Entry in `htmlS/dashboard.html` ergänzen mit Tags für Suchbarkeit.

## Was Frank beim Start des neuen Threads schreiben könnte

Ein minimaler Einstiegssatz reicht, etwa: „Lies HANDOVER_A1_DRILLS.md und fang
mit FD30 Plural der Nomen an." Dann weißt du alles Nötige und kannst direkt
loslegen. Der Drill-Workflow selbst (Items entwerfen → HTML erstellen nach
Kopier-Vorlage FD29 → JS-Struktur anpassen → Dashboard → Commits) sitzt in den
Skills und im Code der bisherigen FDxx-Dateien.

## Letzter Punkt: autonomes Weiterarbeiten

Laut Memory „Nie auf Frank warten" und „Nächste = nächste": Wenn Frank sagt
„mach weiter" oder „nächste", einfach die nächste Datei in der oben
dokumentierten Reihenfolge angehen, ohne Rückfragen. Bei „FDxx fertig" kurz
den Abschluss bestätigen, dann automatisch zur nächsten Datei übergehen.
