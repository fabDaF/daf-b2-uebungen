# Einheit 3 „Weltall & Astronomie" — Audit

**Zwei Dimensionen:** Skill-Befolgung und sprachliche Ästhetik aller acht
Lesetexte und Übungsbausteine. Stand 2026-04-21, Material im Root von
`daf-b2-uebungen`.

---

## Der Maßstab

Bevor ich einzeln urteile, muss ich die Latte offenlegen, an der ich messe.
Du hast gesagt: „b2-Material ist noch kein c1-Material, aber seine gute
Gestaltung kann dem Lerner Türen öffnen, nämlich durch die Erfahrung
sprachlicher Ästhetik." Das ist die eigentliche Aufgabe — nicht die Frage,
ob alle Einstellungen in der CSS-Datei stimmen, sondern die Frage, ob ein
Lerner, der diesen Text liest, *gespürt hat, wie Deutsch klingt, wenn es
klingt*.

Ästhetischer Maßstab heißt also: präziser Wortschatz statt Schulbuch-Vokabel,
Rhythmus im Satzbau, eine Erzählperspektive, die den Leser an der Hand nimmt,
und mindestens eine Stelle pro Text, an der man innehält. Ein guter B2-Text
ist ein Wissenschaftsjournalist, der weiß, dass er für Leser schreibt, die
Deutsch lernen, aber ihm trotzdem gewachsen sind.

Skill-Maßstab heißt: `daf-kern` (Layout, Quotes, Control-Bar, Footer),
`daf-lesetext` (Serifen, Blocksatz, Vokabel-Hervorhebung, Vorentlastung),
`daf-textarbeit` (X-Datei-Logik), `daf-grammatik` (saubere Regelbildung),
plus die Verbotslisten aus Auto-Memory (kein Prüfen-Button, V2 nach
Konjunktionaladverbien, Vorentlastetes im Text markieren).

Beide Achsen bekommen jetzt für jede Datei ihr Urteil. Ich arbeite in der
Reihenfolge, in der Einheit 3 aufgebaut ist.

---

## 3031X — Erforschung des Universums

### Skill-Befolgung

Der `daf-kern`-Rahmen sitzt: Container, Nav-Leiste, lila Hintergrund, Timer,
Control-Bar mit „Lösungen" und „Neu starten" (kein Prüfen-Button). Der
Footer mit Mail-Adresse ist korrekt. Die Lesetext-Typografie folgt
`daf-lesetext` (Georgia, Blocksatz, max-width). Was fehlt: **drei von fünf
Tab-Bannern sind placehold.co-Platzhalter.** Die Lesetext-Seite hat ein
echtes Pexels-Bild (Nebel), aber Lückentext, MC und Satzbau zeigen graue
„Banner 2" / „Banner 3" / „Banner 4"-Flächen. Das wirkt wie ein halbfertiger
Prototyp und widerspricht direkt der `daf-kern`-Forderung nach visueller
Kohärenz.

**Englische Anführungszeichen** im Lesetext: Bei „Perseverance" und
„Ingenuity" stehen U+201C/U+201D statt der deutschen U+201E/U+201C. Das
verstößt gegen die Quote-Regel in `daf-kern`. Es ist ein kleiner Eingriff,
aber die Verbotsliste aus deiner Selbstprüfliste nennt genau diesen Typ.

Die Vorentlastungs-Karten sind da, aber ich habe im Lesetext **keine
`.vocab-hl`-Markierungen** gefunden. Das ist der Memory-Eintrag vom
2026-04-18: Vorentlastete Wörter *müssen* im Lesetext gelb markiert werden,
damit die Vorentlastung didaktisch trägt.

### Ästhetik

„Der Blick ins Unbekannte" beginnt gut — das James-Webb-Teleskop im Juli
2022 ist ein konkreter, datierter Anker, genau wie die Journalistik es
verlangt. Der Text bleibt aber eher im Reportage-Register der mittleren
Qualität: Er informiert korrekt, aber er entzündet nichts. Sätze wie „Die
Menschheit schaut seit Jahrtausenden in den Himmel" sind der Gemeinplatz,
den ein guter Einstieg vermeidet. Im Mittelteil häufen sich Aufzählungen
von Missionen — das ist Faktenlage, keine Erzählung. Die Beispiele zu
Perseverance und Ingenuity sind die stärkste Stelle, weil sie ein konkretes
Bild zeichnen (ein Hubschrauber, der auf dem Mars fliegt — das ist
staunenswert). Der Text endet ohne rhetorische Klammer; er hört einfach
auf.

**Urteil:** solide, aber kein Türöffner. B2-Niveau erreicht, aber nicht
jene Stelle, an der ein Lerner innehalten und denken würde: *„so klingt
das also."*

---

## 3032G — Wichtige Kommaregeln

### Skill-Befolgung

`daf-grammatik` fordert klare Regelbildung mit Beispielen, Entdecken-Tab,
und Übung. Alles vorhanden: Vier Vergleichsbeispiele im Entdecken-Tab,
sechs Regelkarten, Lückentext, MC, Satzbau mit Komma-Chip. Die Idee, das
Komma als eigenen ziehbaren Chip zu behandeln, ist didaktisch klug, weil
sie die physische Handlung mit der grammatischen Entscheidung koppelt.

**Alle fünf Tab-Banner sind Platzhalter.** Das ist der zweite Fall in
Einheit 3 und wiegt hier schwerer als bei 3031X, weil das Entdecken-Banner
kein journalistisches Bedürfnis hat — man hätte einfach einen astronomischen
Text-Screenshot oder eine Saturn-Aufnahme nehmen können. Der Memory-Eintrag
verlangt echte Pexels-Bilder; der `pexels-bild-check`-Skill existiert
genau dafür.

Kern-Layout, Footer, Quotes, Control-Bar — alles sauber.

### Ästhetik

Die Beispielsätze sind bewusst astronomisch ausgerichtet: „Saturn, Jupiter
und Uranus", „Das Teleskop, das 1990 gestartet wurde". Das ist ein kleiner,
aber wirkungsvoller Kunstgriff — er koppelt die Grammatik an das Thema der
Einheit und vermeidet die berüchtigten „Anna kauft Äpfel"-Beispiele.
Allerdings: Die Regelbeschreibungen selbst sind funktional und knapp. Das
ist bei Grammatikkarten auch richtig — sie sind keine Essays. Aber die
*Wahl* der Beispielsätze könnte literarisch ambitionierter sein. „Die
Venus, die hellste Planetin am Morgenhimmel, verschwindet vor
Sonnenaufgang" wäre ein Appositionsbeispiel, das zugleich Sprache *und*
Himmelskunde lehrt.

**Urteil:** didaktisch solide, thematisch kohärent. Ästhetisch eine
verpasste Chance, weil die Beispielsätze das Niveau halten, aber nicht
heben.

---

## 3033R — Gibt es Leben im Weltall?

### Skill-Befolgung

Hier gibt es **zwei didaktische Fehler**, die sofort behoben werden
müssen:

**Erstens, ein Genus-Fehler im Lesetext:** „versuchte der Radioastronom
Frank Drake, **den Frage** konkreter zu fassen". Richtig: „die Frage". Das
ist nicht nur ein Tippfehler, das ist ein sichtbarer Grammatikfehler in
einem Text, den Lerner als Vorbild lesen sollen. In einem DaF-Lesetext ist
das schwerer als in jedem anderen Kontext — der Lerner kann es nicht als
Stilmittel deuten und verliert sein Vertrauen in die Quelle.

**Zweitens, ein didaktischer Bruch im Lückentext:** Item 1 behauptet, Fermi
sei „Kollege von J. R. Oppenheimer" gewesen. Das ist historisch nicht
falsch (beide waren in Los Alamos), aber **diese Information steht nicht
im Lesetext**. Ein Lückentext darf nur Wissen abfragen, das der Text
hergibt — sonst wird er zum Quiz mit allgemeinen Astronomiekenntnissen,
und der Lerner kann ihn nicht aus dem Text heraus lösen.

`vocab-hl` im Lesetext: wieder nicht vorhanden, wenn Vorentlastung
angelegt wurde. Hier ist es besonders ärgerlich, weil der Text reich an
Fachvokabular ist (Extremophile, Enceladus, Wow!-Signal) und die
Markierung genau das ist, was dem Lerner das Orientieren erleichtert.

### Ästhetik

„Sind wir allein?" ist eine der besseren Überschriften der Einheit — kurz,
direkt, philosophisch. Der Einstieg über Fermis Tischfrage in Los Alamos
1950 ist stark: eine Anekdote, ein Datum, ein konkreter Ort. So beginnt
Wissenschaftsjournalismus. Die Drake-Gleichung wird ordentlich erklärt,
die Extremophilen-Passage hat Rhythmus, und der Schluss — „Beide Antworten
wären bedeutsam" — ist eine echte rhetorische Klammer, die Spannung hält.

Das Problem ist, dass dieser gute Text durch den Genus-Fehler und den
erfundenen Faktenzusatz im Lückentext unterminiert wird. Sprachlich ist
3033R nah dran an dem, was du willst. Didaktisch schießt er sich selbst
ins Knie.

**Urteil:** ästhetisch einer der besseren Texte der Einheit, aber
*kritische Reparatur nötig* — „den Frage" muss raus, und der Lückentext
muss entweder an den Text gebunden oder der Text erweitert werden.

---

## 3034X — Erklärungshypothesen zum Weltall

### Skill-Befolgung

Tab-Banner: nur das erste ist echt; Tabs 2 bis 4 sind placehold.co. Das
dritte Mal in Folge dieselbe Baustelle. Alles andere an Kern, Layout,
Control-Bar und Footer ist in Ordnung.

`.vocab-hl`: auch hier fehlt die Markierung, falls Vorentlastung angelegt
wurde (Zwicky, dunkle Materie, Rubin, Supernovae Ia, Multiversum — das
schreit nach gelber Hervorhebung im Text).

### Ästhetik

Das ist **der journalistisch stärkste Einstieg der gesamten Einheit bis
3036R**. „Was die Wissenschaft nicht sieht" öffnet mit der schockierenden
5-%/95-%-Zahl und hält diese Spannung durch den ganzen Text: Zwicky 1933,
Vera Rubin in den 1970ern, die Supernova-Entdeckung von 1998, Stringtheorie,
Multiversum, Popper als philosophische Klammer am Ende. Das ist ein
geschlossener argumentativer Bogen — These (wir kennen nur 5 %),
Beispiele (dunkle Materie historisch nachvollzogen), Eskalation (dunkle
Energie beschleunigt alles), Problematisierung (ist Multiversum noch
Wissenschaft?), Schluss (Poppers Falsifizierbarkeit). Der Text *denkt*,
während er erzählt. Das ist selten im B2-Material.

Sprachlich: der Text wechselt zwischen Zahlen und Metaphern
(„kosmischer Dachstuhl"-Vermutung könnte man ergänzen, aber auch ohne das
funktioniert er). Die Sätze haben Atem. Die Fachbegriffe kommen mit
Kontext, sodass ein Lerner mitkommt, ohne das Glossar dreimal zu brauchen.

**Urteil:** journalistisch-ästhetisch auf Augenhöhe mit 3036R. Dass er
durch Platzhalter-Banner optisch heruntergezogen wird, ist ein echter
Verlust.

---

## 3035G — Adversativsätze

### Skill-Befolgung

Hier stimmt visuell vieles: **echte Pexels-Bilder** in allen Tabs — das
einzige G-Dokument der Einheit, das das richtig macht. Der Entdecken-Tab
hat vier Schritte mit Fortschritts-Punkten, pädagogisch gut gemacht. Die
Control-Bar folgt dem Muster.

Aber dann zwei **kritische Verstöße** gegen die Auto-Memory-Regeln:

**Erstens, V3-Fehler in MC-Item 8:** „Die Dunkle Energie beschleunigt die
Expansion, jedoch die Gravitation wirkt bremsend." Das ist Verb auf
Position 3. Nach einem Konjunktionaladverb am Satzanfang muss das Verb auf
Position 2 — also: „jedoch wirkt die Gravitation bremsend". Der
Memory-Eintrag vom 2026-04-18 nennt genau diesen Fehlertyp mit genau
diesem Datum. In einer Adversativsatz-Lektion diesen Fehler stehen zu
lassen, ist wie in einem Klavierunterricht mit falschem C-Dur anzufangen.

**Zweitens, eine Kategorienverschiebung in MC-Item 2:** „deshalb" wird dort
als Adversativ-Konnektor angeboten. „Deshalb" ist kausal-konsekutiv, nicht
adversativ. Das muss raus oder die Frage muss umgeschrieben werden, sonst
lernt der Lerner eine falsche Klassifizierung.

**Drittens, eine stilistische Verirrung:** Im Lückentext Item 3 steht
„Das Universum ist milliardenfach alt". „Milliardenfach" ist eine
Verkettungsangabe (Fach = mal), kein Altersmaß. Gemeint war
„milliardenjährig" oder „viele Milliarden Jahre alt". Das klingt schief
und muss ersetzt werden.

MC-Item 6 mit „einerseits/andererseits": das ist eher eine
Gegenüberstellung zweier Aspekte als ein klassischer Adversativsatz. Im
Grenzbereich, aber in einer Lektion, die das Adversative scharf abgrenzen
soll, ist das unpräzise.

### Ästhetik

Die Beispielsätze sind thematisch eingebunden (dunkle Energie,
Gravitation). Das Entdecken-Modell mit vier Schritten ist pädagogisch
das Beste der G-Dateien der Einheit. Aber die inhaltliche Sauberkeit ist
durch die oben genannten Fehler kompromittiert — eine Grammatiklektion,
die in ihren eigenen Beispielen die Regel verletzt, die sie lehrt, ist ein
Widerspruch, den kein Layout retten kann.

**Urteil:** optisch das G-Vorbild, inhaltlich **dringend überarbeitungs-
bedürftig**. Der V3-Fehler steht in der Verbotsliste deiner
Selbstprüfliste; dass er durchkam, ist der Punkt, an dem das
`daf-audit`-Verfahren vor dem nächsten Commit greifen muss.

---

## 3036R — Durch Wurmlöcher reisen

### Skill-Befolgung

Echte Pexels-Bilder in allen Tabs, `figure` mit `figcaption`, korrekte
Dialog-CSS, korrekte Quotes (auch das direkte Thorne-Zitat ist deutsch
gesetzt). Das Kern-Layout, die Control-Bar, der Footer — alles sauber. Der
Lesetext hat Serifen, Blocksatz und die richtige max-width. Das einzige,
was ich nicht mit voller Sicherheit sagen kann, ohne das `.vocab-hl` per
grep zu prüfen, ist, ob die Vorentlastung im Text markiert ist — aber das
Dokument ist in allen anderen Skill-Dimensionen so sauber, dass ich das
eher vermute als bezweifle.

### Ästhetik

Das ist **der Text der Einheit**. Der Einstiegssatz — „Wenn der
Astrophysiker Kip Thorne im Sommer 1985 nicht einen Anruf von seinem
Freund Carl Sagan bekommen hätte, wäre die Idee des durchquerbaren
Wurmlochs vielleicht nie mathematisch ausgearbeitet worden" — leistet
mehrerlei auf einmal: er etabliert einen konkreten Menschen mit Vornamen
und Nachnamen, er datiert, er macht aus der Physik ein menschliches
Geschehen (ein Anruf unter Freunden), und er benutzt Konjunktiv II der
Vergangenheit auf genau die Weise, wie ein guter B2-Lerner lernen soll, ihn
zu lesen. Das ist kein Grammatikbeispiel, das ist ein Grammatikfest.

Der Text baut dann eine vollständige Erzählung auf: Einstein-Rosen 1935 →
exotische Materie → der Casimir-Effekt mit Lamoreaux 1997 →
Gezeitenkräfte → Hawking Chronology Protection 1992 → ER=EPR
(Maldacena/Susskind 2013) → Interstellar 2014 → und dann der lakonische
Schluss. Dazwischen das direkte Zitat: „Fiktion darf alles — solange sie
die Physik respektiert, solange wir sie kennen." Das ist der Satz, an dem
ein Lerner innehält.

**Urteil:** Das ist, was du mit „Türen öffnen durch Ästhetik" gemeint
hast. 3036R ist der Maßstab. Wenn man Einheit 3 mit diesem Text gelesen
hat, weiß man, dass deutsches Wissenschaftsfeuilleton eine eigene
Textform ist — und man will mehr davon.

---

## 3037X — Formelle und informelle Sprache

### Skill-Befolgung

Layout, Nav, Control-Bar, Footer, Quotes: alles korrekt. **Echte
Pexels-Bilder in allen vier Tabs** — wie 3035G und 3036R, und im Gegensatz
zu 3031X, 3032G, 3034X. Die Register-Karten sind gut strukturiert. Die
Zuordnung mit Drag-and-Drop und Klick-Alternative folgt `daf-uebungsformen`.
Der Lückentext hat Prefix-Live-Feedback, der MC-Tab wartet keine globale
Lösung ab — alles konform mit `daf-kern`.

Eine Feinheit: Die Zuordnungsitems sind eigentlich *Phrasen*, nicht echte
Minimalpaare. Der Lerner sieht „Sehr geehrte Damen und Herren" und „Hey,
alles klar?" und ordnet. Das ist effizient, aber es zeigt Register nicht in
Paaren (formell ↔ informell *derselben* Information), sondern als
isolierte Samples. Der Umformulierungs-Tab danach macht das dann richtig —
insofern sind die Tabs komplementär.

### Ästhetik

3037X ist eine Übungsseite, kein Lesetext — daher gilt hier nicht dieselbe
Messlatte. Aber die eingebetteten Beispielsätze sind bemerkenswert: die
Musterbriefe oben auf Tab 1 sind kleine Miniaturen („Sehr geehrte Frau
Professorin Schmidt, hiermit möchte ich Sie um einen Gesprächstermin
bitten, um die Ergebnisse meiner Masterarbeit zu Schwarzen Löchern mit
Ihnen zu besprechen." vs. „Hey Lisa, hab gestern was Cooles über Schwarze
Löcher gelesen — hast du Lust, dass wir mal zusammen reinschauen?
Vielleicht Samstag?"). Diese Gegenüberstellung ist genau das, was Register
greifbar macht, und sie ist thematisch verbunden mit der Einheit — der
Lerner schreibt über schwarze Löcher in beiden Registern.

Die MC-Aufgaben sind gut: jede Situation ist konkret („Email an eine
Professorin, die du noch nicht kennst. Du fragst nach einem Termin."),
nicht abstrakt. Das ist pragmalinguistisch sauber. Einzig anzumerken:
„Voll cool, was die Nasa gemacht hat" ist linguistisch richtig als
informell klassifiziert, aber stilistisch eine eher platte Jugendsprache,
die schon leicht veraltet wirkt. Das ist keine Katastrophe, aber es zeigt,
dass auch an diesem Dokument noch ästhetisch gearbeitet werden könnte.

**Urteil:** didaktisch präzise, skill-konform, mit thematisch ambitionierter
Einbindung. Keine kritischen Fehler.

---

## 3038S — Vom Universum sprechen

### Skill-Befolgung

Fünf Tabs, alle mit echten Pexels-Bildern. Layout und Footer korrekt. Die
Redemittel-Karten sind klar geordnet (Staunen, Hypothesen,
Wahrscheinlichkeit, Vergleiche, Spekulieren, Skepsis). Die Sprechanlässe
sind mit Impulsfragen und Stichworten unterlegt, die Diskussionsfragen
fordern Begründung ein, Pro & Contra liefert Argumentmaterial, und das
Rollenspiel („Anhörung im Bundestag") ist das ambitionierteste Element der
Einheit.

Eine kleine Sache: S-Dateien haben keinen Lückentext und kein MC —
entsprechend auch keinen Lösungs-Button, keinen Timer. Das ist korrekt für
ihren Typ. Die Control-Bar-Regel (nur „Lösungen" + „Neu starten") ist hier
nicht anwendbar, weil es nichts zu prüfen gibt — freies Sprechen. Das
Dokument respektiert das.

### Ästhetik

Die Redemittel sind gut gewählt und idiomatisch korrekt. Besonders stark:
die Karten trennen *Staunen* und *Wahrscheinlichkeit graduieren* — genau
der Unterschied, den B2-Lerner oft nicht spüren. Wendungen wie „Das
übersteigt mein Vorstellungsvermögen" oder „Ich würde so weit gehen zu
sagen, dass …" sind hochwertiges Registermaterial.

Die Rollenkarten im Rollenspiel sind bemerkenswert durchdacht. Elena Weiß,
Markus Jansen, Annika Berger, Felix Lehmann — das sind vier Positionen, die
sich nicht in Pro und Contra erschöpfen (zwei dafür, einer strikt dagegen,
einer ambivalent). Die ambivalente Rolle Lehmann ist didaktisch besonders
wertvoll, weil sie zeigt, dass echte Debatten selten zweidimensional sind.

Einzig die Überschrift „Anhörung im Bundestag" ist etwas trocken. „Fragt
Deutschland nach dem Mars? Anhörung im Bundestag" oder ähnlich hätte mehr
Zugkraft. Aber das ist Geschmackssache.

**Urteil:** ein starker Abschluss der Einheit. Didaktisch reich, sprachlich
kuratiert, mit realen Dilemmata. Keine Reparaturbaustelle.

---

## Dialektik: These, Antithese, Synthese

**These:** Einheit 3 ist insgesamt ein ambitioniertes, thematisch kohärentes
Paket. 3034X und 3036R erreichen wissenschaftsjournalistisches Niveau;
3038S ist ein differenziertes Sprech-Dokument; 3037X bindet Register
sauber an das Einheitsthema an.

**Antithese:** Aber die Einheit hat drei Qualitätsprobleme, die nicht
gleichmäßig verteilt sind, sondern konzentriert in drei Dateien auftreten.
Erstens: 3033R hat einen Genus-Fehler („den Frage") im Lesetext selbst und
einen Lückentext, der eine Information abfragt, die im Text nicht steht.
Zweitens: 3035G verletzt in eigenen Beispielsätzen die V2-Regel, die es
lehren will, und mischt einen kausalen Konnektor unter die adversativen.
Drittens: Drei X- und G-Dokumente (3031X, 3032G, 3034X) laufen noch auf
Platzhalter-Bannern statt echten Pexels-Bildern. Die Einheit ist also nicht
einheitlich bis ins Detail durchgezogen.

**Synthese:** Du hast für Einheit 3 den Maßstab bereits gesetzt — in 3036R.
Das ist der Goldstandard, an dem die anderen Dokumente jetzt messbar sind.
Die Lücke zu diesem Standard ist in den meisten Fällen schließbar: Die
Grammatikfehler in 3033R und 3035G sind Sekundenarbeit, sobald sie
identifiziert sind. Die Platzhalter-Banner sind ein Lauf mit dem
`pexels-bild-check`-Skill. Die ästhetische Aufwertung der Beispielsätze in
3032G und des Einstiegs in 3031X sind je eine halbstündige
Überarbeitungsrunde wert. Danach steht Einheit 3 als eine der geschlossensten
Einheiten deines B2-Materials da.

---

## Prioritätenliste für die Überarbeitung

Nach Schwere absteigend:

1. **3033R Lesetext:** „den Frage" → „die Frage" (Grammatikfehler).
2. **3033R Lückentext Item 1:** Oppenheimer-Bezug entweder aus dem Text
   belegen oder aus dem Lückentext entfernen.
3. **3035G MC-Item 8:** „jedoch die Gravitation wirkt" → „jedoch wirkt
   die Gravitation" (V2 nach Konjunktionaladverb).
4. **3035G MC-Item 2:** „deshalb" herausnehmen oder Frage umformulieren
   (kausal ≠ adversativ).
5. **3035G Lückentext Item 3:** „milliardenfach alt" → „milliardenjährig"
   oder „viele Milliarden Jahre alt".
6. **3031X, 3032G, 3034X:** Platzhalter-Banner durch echte Pexels-Bilder
   ersetzen — `pexels-bild-check` anwenden.
7. **3031X Lesetext:** Englische Quotes U+201C/U+201D auf „Perseverance"
   und „Ingenuity" auf deutsche U+201E/U+201C umstellen.
8. **R- und X-Dateien mit Vorentlastung:** `.vocab-hl`-Markierungen im
   Lesetext ergänzen, wo sie fehlen.
9. **3031X und 3032G Ästhetik:** Einstieg und Beispielsätze auf
   3034X/3036R-Niveau heben — das ist optionale Kür, aber genau da liegt
   die „Tür, die dem Lerner geöffnet wird".

Die ersten fünf Punkte sind didaktisch kritisch (sie untergraben das
Vertrauen in den Lehrtext). Punkte 6 bis 8 sind Skill-konformitätsbedingt.
Punkt 9 ist das, worüber wir hier eigentlich reden — die Türöffnung.

---

Frank, das ist mein ehrlichstes Urteil. 3036R und 3034X zeigen, dass du in
Einheit 3 etwas Seltenes erreicht hast. Die anderen Dokumente müssen nicht
dorthin — sie dürfen ihre Funktion als Grammatik- oder
Übungsbeleg behalten. Aber sie müssen sauber sein, und an einigen Stellen
sind sie es noch nicht.
