# BERICHT: A1 Bild-Audit vom 2026-04-24
Automatisierter Audit aller 188 HTML-Dateien im Ordner `htmlS/A1.1 NEW/`.

**Befund: 83 Dateien mit 362 Banner-Fehlzuordnungen**, wo ein generischer
Kategorie-Banner anstelle eines thematischen Banners steht.

## Methodik

Jedes `<img>`-Tag im A1-Ordner wurde analysiert: Base64-Inhalt wurde per MD5
gehasht, um identische Bilder zu identifizieren. Fünf Bilder treten besonders oft
auf und sind als „Kategorie-Banner" erkennbar (jeweils ein generisches Motiv).

Die Banner sind **legitim**, wenn der `alt`-Text zur Kategorie passt — z.B.
das Wörterbuch-Foto auf allen Tabs mit alt „Wortschatz". Sie sind **fehl am Platz**,
wenn sie auf inhaltsspezifischen Tabs landen (z.B. alt „Uhrzeit als Text" mit
Wörterbuch-Bild statt Uhr).

## Die fünf generischen Banner

| Hash | Motiv | Gesamt | Legitim | Fehl am Platz |
|------|-------|-------:|--------:|--------------:|
| `a15f1503bf` | Wörterbuch-Foto (Wortschatz-Banner) | 167 | 101 | **66** |
| `2e0dbb5872` | Holz-Puzzle (Satzbau-Banner) | 107 | 100 | **7** |
| `6f44101748` | Tafel + Schülerin (Vorentlastung/Alphabet-Banner) | 82 | 13 | **69** |
| `b9397b0d3d` | Lehrerin an Tafel (Grammatik-Banner generisch) | 79 | 2 | **77** |
| `2616198d76` | Buchrücken in Händen (Geschichte-Banner) | 155 | 12 | **143** |

## Phase 1 — Die 11 Lesetext-Geschichten (R-Dateien)

Jede R-Geschichte hat 13 Tabs mit `alt="Tab 1"`, `alt="Tab 2"`, …, `alt="Tab 13"`
als Platzhalter und dem Buchrücken-Banner. Die Tab-Titel im UI sind aussagekräftig,
nur der `alt`-Text ist generisch — was bedeutet, dass beim Einbetten der Bilder
kein thematisches Bild ausgesucht wurde.

| Datei | betroffene Tabs | Thema der Geschichte |
|-------|----------------:|----------------------|
| 1014R-montag-in-berlin | 13 | Berlin, Montagsroutine |
| 1024R-die-party | 13 | Party, Freunde |
| 1034R-omas-geburtstag | 13 | Geburtstag, Familie |
| 1054R-ein-wochenende-in-berlin | 13 | Wochenende, Berlin |
| 1064R-glueckliche-huehner | 13 | Bauernhof, Tiere |
| 2014R-alex-der-schriftsteller | 13 | Schriftsteller, Beruf |
| 2024R-ein-besuch | 13 | Besuch, Wohnung |
| 2034R-der-arzttermin | 13 | Arzt, Gesundheit |
| 2044R-freundinnen-beim-shoppen | 13 | Einkaufen, Kleidung |
| 2054R-cooler-urlaub-in-new-york | 13 | Urlaub, New York |
| 2064R-feste | 13 | Feste, Feiern |

**Phase-1-Summe:** 143 Banner zu ersetzen

## Phase 2 — G/V/C/X-Dateien mit inhaltsspezifischen Tabs

72 Dateien mit zusammen 219 Fehlzuordnungen.
Hier ist der `alt`-Text informativ (z.B. „Pronomen einsetzen", „Tageszeit", „Uhrzeit als Text"),
aber das eingebettete Bild ist ein generischer Kategorie-Banner.

### Top-20 Übeltäter (nach Anzahl Fehlzuordnungen)

| Datei | Anzahl | Beispiel-Alts |
|-------|-------:|---------------|
| 1000G-der-die-das-genus | 6 | „der · die · das?“ · „der Löwe“ · „die Frau“ |
| 1023G-regelmaessige-verben-im-praesens | 6 | „Entdeckung“ · „Pronomen“ · „Pronomen einsetzen“ |
| 1053G-verben-mit-vokalwechsel | 5 | „Entdeckung“ · „Vokaltyp“ · „du-Form“ |
| 1093G-die-verneinung-im-deutschen | 5 | „Entdecken“ · „nicht oder kein?“ · „nicht“ |
| 1103G-nominativ-und-akkusativ | 5 | „Entdecken“ · „Nom. oder Akk.?“ · „der oder den?“ |
| 2021V-meine-stadt | 5 | „Kulturorte“ · „Kultur oder Richtung?“ · „Himmelsrichtungen“ |
| 2021V-uebungen | 5 | „Kulturorte“ · „Kultur oder Richtung?“ · „Himmelsrichtungen“ |
| 2031V-geschaefte-und-besorgungen | 5 | „Geschäfte & Dienstleistungen“ · „Geschäft oder Dienst?“ · „bei oder zu?“ |
| 2031V-uebungen | 5 | „Geschäfte & Dienstleistungen“ · „Geschäft oder Dienst?“ · „bei oder zu?“ |
| 1071V-die-wochentage | 4 | „Werktag / Wochenende“ · „am + Wochentag“ · „gestern / heute / morgen“ |
| 1073G-monate-daten-und-jahre | 4 | „Entdecken“ · „Ordnungszahlen“ · „Datum schreiben“ |
| 1083G-die-wortstellung-im-deutschen | 4 | „Entdecken“ · „Satztypen“ · „Zwei Verben“ |
| 1091V-hobbys-und-freizeit | 4 | „Hobby-Kategorien“ · „spielen + Akk.“ · „Verben -ern/-eln“ |
| 1101V-essen-und-trinken | 4 | „Essen oder Trinken?“ · „essen/trinken/mögen“ · „Lieblings-“ |
| 1111V-verkehrsmittel | 4 | „Öffentlich oder privat?“ · „nehmen konjugieren“ · „Nehmen Sie den/die/das...“ |
| 1113G-der-dativ-nach-praepositionen | 4 | „Entdecken“ · „Nom. / Dat.“ · „mit + Dativ“ |
| 1121V-beim-buergeramt | 4 | „Beim Amt / Im Alltag“ · „brauchen oder müssen?“ · „müssen konjugieren“ |
| 1123G-die-modalverben | 4 | „Entdecken“ · „Bedeutung“ · „Konjugation“ |
| 1124C-ich-kann-eine-to-do-liste-schreiben | 4 | „Bürokratie“ · „Possessivartikel“ · „Nomen oder Verb?“ |
| 2012G-possessivartikel-im-singular | 4 | „Entdecken“ · „sein oder ihr?“ · „Possessivartikel“ |

### Komplette Liste aller Phase-2-Dateien

- **1000G-der-die-das-genus** (6×): „der · die · das?“, „der Löwe“, „die Frau“, „das Wasser“, „Practice Makes Perfect“, „3 neue Freunde“
- **1023G-regelmaessige-verben-im-praesens** (6×): „Entdeckung“, „Pronomen“, „Pronomen einsetzen“, „Die vier „sie““, „Konjugation“, „CH-Laut“
- **1053G-verben-mit-vokalwechsel** (5×): „Entdeckung“, „Vokaltyp“, „du-Form“, „er/sie-Form“, „ich → du“
- **1093G-die-verneinung-im-deutschen** (5×): „Entdecken“, „nicht oder kein?“, „nicht“, „kein(e)“, „Mix“
- **1103G-nominativ-und-akkusativ** (5×): „Entdecken“, „Nom. oder Akk.?“, „der oder den?“, „ein oder einen?“, „kein oder keinen?“
- **2021V-meine-stadt** (5×): „Kulturorte“, „Kultur oder Richtung?“, „Himmelsrichtungen“, „Kunst & Kultur“, „es gibt ...“
- **2021V-uebungen** (5×): „Kulturorte“, „Kultur oder Richtung?“, „Himmelsrichtungen“, „Kunst & Kultur“, „es gibt ...“
- **2031V-geschaefte-und-besorgungen** (5×): „Geschäfte & Dienstleistungen“, „Geschäft oder Dienst?“, „bei oder zu?“, „Was kaufst du wo?“, „Nomen auf -ei“
- **2031V-uebungen** (5×): „Geschäfte & Dienstleistungen“, „Geschäft oder Dienst?“, „bei oder zu?“, „Was kaufst du wo?“, „Nomen auf -ei“
- **1071V-die-wochentage** (4×): „Werktag / Wochenende“, „am + Wochentag“, „gestern / heute / morgen“, „vorgestern / übermorgen“
- **1073G-monate-daten-und-jahre** (4×): „Entdecken“, „Ordnungszahlen“, „Datum schreiben“, „am + Datum“
- **1083G-die-wortstellung-im-deutschen** (4×): „Entdecken“, „Satztypen“, „Zwei Verben“, „Was passt?“
- **1091V-hobbys-und-freizeit** (4×): „Hobby-Kategorien“, „spielen + Akk.“, „Verben -ern/-eln“, „Was machst du gern?“
- **1101V-essen-und-trinken** (4×): „Essen oder Trinken?“, „essen/trinken/mögen“, „Lieblings-“, „lecker oder eklig?“
- **1111V-verkehrsmittel** (4×): „Öffentlich oder privat?“, „nehmen konjugieren“, „Nehmen Sie den/die/das...“, „Wie komme ich...?“
- **1113G-der-dativ-nach-praepositionen** (4×): „Entdecken“, „Nom. / Dat.“, „mit + Dativ“, „Verschmelzungen“
- **1121V-beim-buergeramt** (4×): „Beim Amt / Im Alltag“, „brauchen oder müssen?“, „müssen konjugieren“, „Komposita bilden“
- **1123G-die-modalverben** (4×): „Entdecken“, „Bedeutung“, „Konjugation“, „Welches Verb?“
- **1124C-ich-kann-eine-to-do-liste-schreiben** (4×): „Bürokratie“, „Possessivartikel“, „Nomen oder Verb?“, „Modalverben“
- **2012G-possessivartikel-im-singular** (4×): „Entdecken“, „sein oder ihr?“, „Possessivartikel“, „sein(e) / ihr(e)“
- **2012G-uebungen** (4×): „Entdecken“, „sein oder ihr?“, „Possessivartikel“, „sein(e) / ihr(e)“
- **2051V-essen-und-trinken** (4×): „Pflanzlich oder tierisch?“, „Essen gern / nicht gern“, „schmecken + mir/dir“, „Geschmack“
- **2051V-uebungen** (4×): „Pflanzlich oder tierisch?“, „Essen gern / nicht gern“, „schmecken + mir/dir“, „Geschmack“
- **2052G-praeteritum-von-sein-und-haben** (4×): „Präsens oder Präteritum?“, „war-Formen“, „hatte-Formen“, „war oder hatte?“
- **2052G-uebungen** (4×): „Präsens oder Präteritum?“, „war-Formen“, „hatte-Formen“, „war oder hatte?“
- **2054C-lerncheck-im-restaurant** (4×): „Essen & Geschmack“, „war/hatte im Restaurant“, „Kellner:in oder Gast?“, „Tisch reservieren“
- **2054C-uebungen** (4×): „Essen & Geschmack“, „war/hatte im Restaurant“, „Kellner:in oder Gast?“, „Tisch reservieren“
- **1024C-ich-kann-mich-vorstellen** (3×): „Verben“, „Vorstellen“, „Personen“
- **1041V-wichtige-regelmaessige-verben** (3×): „Speisekarte“, „Kellner oder Gast?“, „Aussprache“
- **1043G-alles-ueber-fragen** (3×): „Entdeckung“, „W- oder Ja/Nein?“, „Fragen bilden“
- **1054C-ich-kann-ueber-meine-arbeit-sprechen** (3×): „Adjektiv-Gegenteile“, „Negation“, „Vokalwechsel“
- **1061V-die-zeit-im-24-stunden-format** (3×): „Tageszeit“, „Uhrzeit als Text“, „schon / erst“
- **1063G-wann-machst-du** (3×): „Entdecken“, „am / in der“, „von...bis / ab / um“
- **1074C-ich-kann-ein-treffen-vereinbaren** (3×): „Datum & Ordnungszahlen“, „Treffen vereinbaren“, „gestern / heute / morgen“
- **1081V-trennbare-verben-im-alltag** (3×): „Präfix ergänzen“, „Satz & Präfix“, „Im Alltag“
- **1094C-ich-kann-sagen-was-ich-mag** (3×): „Hobbys & Verben“, „nicht oder kein?“, „Verneinung“
- **1104C-ich-kann-lebensmittel-einkaufen** (3×): „Im Supermarkt“, „Nominativ oder Akkusativ?“, „Akkusativ ergänzen“
- **1114C-ich-kann-verkehrsmittel-nutzen** (3×): „Welcher Artikel?“, „Akkusativ oder Dativ?“, „Am Schalter“
- **1131C-lernziele-a1.1-erreicht** (3×): „Treffen vereinbaren“, „drinnen oder draußen?“, „Im Café & Supermarkt“
- **2032G-lokale-praepositionen-mit-dativ** (3×): „Präposition oder Verb?“, „Kontraktionen“, „Wo ist was?“
- **2032G-uebungen** (3×): „Präposition oder Verb?“, „Kontraktionen“, „Wo ist was?“
- **2034C-lerncheck-in-der-stadt-erledigen** (3×): „Wo erledige ich das?“, „Geschäft oder Post?“, „Brief schicken“
- **2034C-uebungen** (3×): „Wo erledige ich das?“, „Geschäft oder Post?“, „Brief schicken“
- **2042G-uebungen** (3×): „Positiv oder negativ?“, „Adjektivendungen“, „welch- / dies-“
- **2042G-welch-und-dies** (3×): „Positiv oder negativ?“, „Adjektivendungen“, „welch- / dies-“
- **2044C-lerncheck-kleidung-kaufen** (3×): „welch- / dies-“, „Verkäufer oder Kunde?“, „Im Geschäft“
- **2044C-uebungen** (3×): „welch- / dies-“, „Verkäufer oder Kunde?“, „Im Geschäft“
- **1012X-wie-schreibt-man-das** (2×): „Buchstabieren“, „Umlaute & ß“
- **1033G-die-verben-sein-und-haben** (2×): „Entdeckung“, „Konjugation“
- **1034C-ich-kann-persoenliche-daten-angeben** (2×): „Sprachen“, „sein & haben“
- **1044C-ich-kann-einen-kaffee-bestellen** (2×): „Fragen im Café“, „Café-Wörter“
- **1051V-mein-beruf** (2×): „Aussprache ch“, „Weibliche Form“
- **1064C-ich-kann-ueber-die-zeit-sprechen** (2×): „Informell“, „Tagesablauf“
- **1112X-am-bahnhof** (2×): „Was passt?“, „Komposita bilden“
- **2011V-uebungen** (2×): „Zimmer“, „Komposita“
- **2011V-wohnung-und-moebel** (2×): „Zimmer“, „Komposita“
- **2014C-lerncheck-wohnung-und-moebel** (2×): „sein / ihr“, „Zuordnung“
- **2014C-uebungen** (2×): „sein / ihr“, „Zuordnung“
- **2022G-uebungen** (2×): „Ort oder Richtung?“, „Imperativ“
- **2022G-wegbeschreibung-und-imperativ** (2×): „Ort oder Richtung?“, „Imperativ“
- **2024C-lerncheck-stadt-und-wegbeschreibung** (2×): „Orte“, „Zuordnung“
- **2024C-uebungen** (2×): „Orte“, „Zuordnung“
- **1014C-ich-kann-im-deutschunterricht-klarkommen** (1×): „Singular & Artikel“
- **1021V-wie-geht-es-dir** (1×): „Singular & Plural“
- **103V-eins-zwei-drei** (1×): „Z oder ZW?“
- **1042X-zahlen-bitte** (1×): „Zuordnung“
- **1052X-ueber-meine-arbeit-sprechen** (1×): „Negation“
- **1082X-mein-arbeitstag** (1×): „Welches Verb?“
- **1084C-ich-kann-ueber-meinen-zeitplan-sprechen** (1×): „Häufigkeit“
- **1133G-nebensaetze-weil-und-dass** (1×): „Entdecken“
- **2041V-kleidung-und-farben** (1×): „Verb: tragen“
- **2041V-uebungen** (1×): „Verb: tragen“

## Empfohlene Fix-Reihenfolge

1. **Phase 1** (Lesetext-Geschichten): 11 Dateien, 143 Banner — höchste didaktische Priorität,
   weil `Tab 1`..`Tab 13`-Platzhalter den Schülern nichts anbieten. Pro Geschichte 13
   thematische Pexels-Banner suchen, als Base64 einbetten.
2. **Phase 2a** (G-Dateien): Grammatik-Banner durch thematische ersetzen — z.B.
   „der Löwe" bekommt ein Löwen-Foto statt der Tafel-Szene.
3. **Phase 2b** (V/C/X-Dateien): Wortschatz/Lerncheck/Textarbeit — meist weniger
   Fehlzuordnungen pro Datei, deshalb zuletzt.

## Technische Anmerkung

Alle Bilder im A1-Ordner sind base64-embedded (keine externen Pexels-URLs mehr).
Das heißt: jeder Fix braucht einen Pexels-Download-Schritt + base64-Einbettung.
Pipeline steht im Skill `pexels-bild-check` dokumentiert.
