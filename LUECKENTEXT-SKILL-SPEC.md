# Lückentext — verbindlicher Ziel-Spec (Entwurf zur Abstimmung)

Stand: 2026-06-19. Grundlage: **daf-kern §7**, **daf-uebungsformen**, **shared-rules**.
Ziel: EIN einziger, skill-konformer Lückentext-Stil, der über alle Niveaus (A1–C1)
ausgerollt wird. Dieser Entwurf hält fest, was der Skill ohnehin vorschreibt, und
markiert die wenigen Punkte, über die wir uns noch einig werden müssen.

## Soll-Elemente

| # | Element | Verbindliche Vorgabe | Quelle | Status |
|---|---------|----------------------|--------|--------|
| 1 | Eingabe-Modus | **Tippen** — kein Klick-Einsetzen, kein Drag-and-Drop | daf-kern §7 | fest |
| 2 | Wortbank | Pflicht: sichtbare Wortbank über dem Lückentext | daf-kern §7 | fest |
| 3 | Position | direkt vor `#lueckenContainer` | daf-kern §7 | fest |
| 4 | **Technik** | **native Wortbank, per JS aus den Antworten gerendert (`initWortbank`)** — kein nachträglich injiziertes Fremd-Modul (das graue „Universal-Modul" wird abgelöst) | daf-kern §7 | **abstimmen (D1)** |
| 5 | Reihenfolge | Fisher-Yates-Shuffle bei jedem Init, nie sortiert | daf-kern §7 | fest |
| 6 | Klickbarkeit | **nicht klickbar** (kein `cursor:pointer`, kein Click-Handler) | daf-kern §7 | fest |
| 7 | `.used`-Feedback | Pflicht: korrekt getipptes Wort → Chip `opacity .35` + Durchstreichen; pro Vorkommen genau ein Chip (`remaining`-Liste, **kein** `Set`) | daf-kern §7 | fest |
| 8 | Dubletten | gleiche Antwort mehrfach = mehrere Chips (einer je Lücke) | daf-kern §7 | **abstimmen (D3)** |
| 9 | Inhalt R/V/X | **Vollformen** = die Antwortwörter | daf-kern §7 | fest |
| 10 | Inhalt G (Transformation) | **Grundform-/Infinitiv-Kasten** — Zielform nie sichtbar; hier kein `.used` | daf-grammatik / shared-rules R7 | **abstimmen (D2)** |
| 11 | Input-Element | `input.blank` mit `data-answer` | daf-kern §7 | fest |
| 12 | Feldbreite | dynamisch in `ch` aus `max(Antwort, Hint)+Puffer`; **keine** festen px / Größenklassen `.s/.m/.l/.xl` | daf-uebungsformen | fest |
| 13 | Placeholder | **leer** | daf-uebungsformen | fest |
| 14 | Feedback-Mechanik | Live bei jedem Tastendruck (`input`-Event), **kein „Prüfen"-Button** | daf-uebungsformen / daf-kern §7 | fest |
| 15 | Vergleich | **case-sensitive**, ohne `trim`; `val === ans` | daf-kern §7 | fest |
| 16 | Drei Zustände | neutral (leer/korrektes Präfix), grün `.correct`, rot `.wrong` (Präfix-Regel) | daf-kern §7 / shared-rules §8a | fest |
| 17 | Farben | grün `#27ae60`, rot `#e74c3c`, neutral grauer Unterstrich | daf-uebungsformen | fest |
| 18 | Buttons | „Lösung zeigen" + „Reset"; `initWortbank`/`updateWortbankChips` an den 4 Pflicht-Stellen (Tabwechsel, korrekte Eingabe, Lösung zeigen, Reset) | daf-kern §7 | fest |
| 19 | Label | „🔤 Wortbank – die richtigen Wörter, in zufälliger Reihenfolge. Tipp sie selbst … achte auf Groß- und Kleinschreibung." | daf-kern §7 | fest |
| 20 | CSS-Klassen | `.wortbank`, `.wortbank-label`, `.wortbank-chip`, `.wortbank-chip.used` exakt nach Skill-CSS | daf-kern §7 | fest |
| 21 | Anführungszeichen | deutsche Quotes „…", restliche shared-rules | daf-kern §4 | fest |

## Offene Entscheidungen (das müssen wir gemeinsam festlegen)

**D1 — Ziel-Stil.** Verbindlicher Stil = die native §7-Wortbank (lila Chips, JS-gerendert,
gemischt, Durchstreichen). Alle abweichenden Stile (graues Universal-Modul, statische
wb-chip-/Wortkasten-Boxen, Drag-Lückentexte) werden Schritt für Schritt darauf umgestellt.
*Mein Vorschlag: ja — es ist der Skill-Original-Stil und C1 nutzt ihn schon durchgängig.*

**D2 — Grammatik-Dateien (G).** Wortbank zeigt die **Grundform** (Infinitiv / Nominativ /
Grundform des Adjektivs), Aufgabe ist Konjugieren/Deklinieren; die Lösung wird nie gezeigt,
deshalb dort kein Durchstreichen. *Das hatten wir schon so besprochen (Variante A).*

**D3 — Dubletten.** Kommt eine Antwort mehrfach vor, zeigt die Wortbank sie mehrfach
(ein Chip je Lücke), und Durchstreichen trifft pro richtiger Eingabe genau einen.
*Mein Vorschlag: so lassen (Skill-Vorgabe) — Alternative wäre, jedes Wort nur einmal zu zeigen.*

## Nächster Schritt

Sobald D1–D3 stehen, baue ich **eine** Beispiel-Lektion exakt nach diesem Spec,
schaue sie selbst im Browser an und zeige sie dir zur Abnahme. Erst wenn die sitzt,
rollen wir Stil für Stil aus.
