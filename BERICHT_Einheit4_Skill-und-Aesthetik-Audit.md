# Einheit 4 „Sprachen & Linguistik" — Skill- und Ästhetik-Audit

**Audit-Datum:** 2026-04-21
**Prüfer:** Claude (skeptisch-analytisch, mit den Augen eines DaF-Lerners und eines Lektors)
**Dateien:** 3041X, 3042G, 3043R, 3044X, 3045G, 3046R, 3047X, 3048S

Dieser Bericht fährt denselben Doppel-Audit wie für Einheit 3: einmal gegen die Pflicht-Skills (daf-kern shared-rules, daf-lesetext, daf-audit), einmal gegen das literarisch-ästhetische Maßband, das mit 3036R „Durch Wurmlöcher reisen" und 3034X gesetzt wurde. Frank hat dort formuliert: „B2-Material ist noch kein C1-Material, aber seine gute Gestaltung kann dem Lerner Türen öffnen, nämlich durch die Erfahrung sprachlicher Ästhetik."

---

## Gesamturteil vorweg

Einheit 4 ist **auf einem deutlich höheren Durchschnittsniveau als Einheit 3 im Ausgangszustand**. Die beiden Lesetexte (3043R Sapir-Whorf, 3046R Sprachfamilien), der Lesetext 3041X („Sieben Tausend Stimmen") und der Lesetext 3044X („Eine zweite Sprache hinter der Sprache") gehören journalistisch-didaktisch zum Besten, was das Repo zeigt — 3046R mit Schleicher 1861/Grimm 1822/Kurgan-Hypothese ist sogar eine kleine Perle. 3048S ist eine sorgfältig durchdachte Sprech-Datei mit 5 Tabs, 50+ Redemitteln und einem Rollenspiel „Anhörung zur Sprachenpolitik" mit 4 gezeichneten Rollen. Die Grammatik-Dateien (3042G, 3045G) haben thematisch-konsistente Beispielsätze — Mehrsprachigkeit, Berlin, MIT-Studien, Brücke/Puente-Experiment — die das Textthema der Einheit aufnehmen.

**Aber zwei klar benennbare Skill-Verstöße**, die Frank am 2026-04-18 explizit angemahnt hatte, treten erneut auf:

1. **vocab-hl-Lücke in 3041X und 3044X.** Je 3 vorentlastete Wörter erscheinen in der Pre-Card-Vorentlastung, sind aber **nicht als `<span class="vocab-hl">` im Lesetext markiert**. Das ist eine direkte Verletzung der Memory-Regel `feedback_vocab_hl_lesetext.md` („R/X-Dateien mit Vorentlastung MÜSSEN Wörter im Text per `<span class="vocab-hl">` gelb markieren"). 3047X dagegen ist mit 10/10 korrekt.
2. **Kleinere thematische Trockenstellen** — aber keine gravierenden inhaltlichen Bugs wie „den Frage" in 3033R oder V3 in 3035G.

Die beiden R-Dateien 3043R und 3046R arbeiten mit einem eleganten dynamischen `VORENTLASTUNG`-Array + `highlightVocabInText()`-Funktion, die die vocab-hl-Spans zur Laufzeit erzeugt; das ist technisch in Ordnung und liefert die gelbe Hervorhebung korrekt.

---

## Pro Datei — These, Antithese, Synthese

### 3041X · „Durch die Sprachen der Welt"

**These (Stärken).**
Lesetext „Sieben Tausend Stimmen" ist dicht und faktenreich: 800 Sprachen auf Papua-Neuguinea, 150 Gebärdensprachen weltweit, DGS-Anerkennung 2002, UNESCO-Befund „alle zwei Wochen stirbt eine Sprache", Pirahã ohne Zahlwörter, Khoisan-Klicks, Finnisch mit 15 Kasus, das lateinische _amavî_ als Musterbeispiel flektierender Verdichtung. Der Schlussabsatz „Jede Sprache löst die Aufgabe, menschliche Erfahrung auszudrücken, auf ihre eigene Weise" setzt einen lakonischen, würdigen Schlussakkord. Pre-Cards sauber formuliert, 10 Begriffe.

**Antithese (Schwächen).**
- **Skill-Bug.** 3 von 10 Pre-Cards haben **keine** entsprechende vocab-hl-Markierung im Lesetext: `die Sprachfamilie`, `der Dialekt`, `das Sprachsterben`. Die Pre-Cards versprechen den Leser darauf vor — der Lesetext liefert die Spur nicht.
- Die Vorentlastungs-Einführung „💡 Wichtige Begriffe" ist schlichter als das JS-gestützte „📚 Vorentlastung: Schlüsselbegriffe" in 3043R/3046R. Kein Bug, aber eine Bruchstelle im Einheits-Duktus.

**Synthese.**
Der Text braucht nichts Neues — er braucht nur die drei fehlenden vocab-hl-Spans nachgezogen. Dialekt ließe sich im bestehenden typologischen Absatz unterbringen, Sprachfamilie im ersten Absatz zum indogermanischen Zusammenhang, Sprachsterben im UNESCO-Absatz. Eine reine 3-Span-Korrektur, kein Text-Rewrite nötig.

---

### 3042G · „Konjunktiv — Erweiterter Gebrauch"

**These.**
Beispielsätze durchgängig thematisch verankert in der Einheit: _„Der Linguist erklärte, Mehrsprachigkeit sei der Normalfall."_ — _„Wenn es keine Sprachen gäbe, wüsste niemand etwas vom anderen."_ — _„Hätte ich früher angefangen, wäre ich fließend geworden."_ — _„Wäre ich doch mit zwei Muttersprachen aufgewachsen!"_. Alle 9 Regelkategorien decken systematisch K I, K II, würde-Form, Vergangenheits-K II, höfliche Bitte, Wunschsatz und irrealen Vergleich ab. Deutsche Anführungszeichen korrekt (23 × U+201E, 23 × U+201C).

**Antithese.**
- Die Regel-Tabelle ist inhaltlich sauber, aber sehr tabellarisch. Bei 3035G (Adversativsätze) arbeitet das Ausgangsmaterial mit Karten und ästhetischen Einschüben („Die Dunkle Energie beschleunigt die Expansion, jedoch wirkt die Gravitation bremsend"). Hier in 3042G ist der Regel-Tab noch klassisch-schulisch: Form / Funktion / Beispiel. Kein Bug, aber ein stilistischer Unterschied zur Einheit 3 nach Aufwertung.
- Das „als ob" + KII-Beispiel _„Er tut, als ob er alle Sprachen beherrschen würde"_ ist grammatisch grenzwertig — präskriptiv wäre „beherrsche" (K I) oder „beherrschte" (K II) erwartet, das „würde"-Ersatz innerhalb „als ob" ist eher gesprochene Norm. Als Beispielsatz akzeptabel, als einziges Beispiel für die Regel minimal irritierend.

**Synthese.**
Keine Pflicht-Korrekturen. Optional: beim „als ob"-Beispiel eine Variante mit „als ob … beherrsche" aufnehmen, damit die Regel nicht auf der umgangssprachlichen würde-Variante ruht.

---

### 3043R · „Die Sapir-Whorf-Hypothese"

**These.**
Einer der journalistisch stärksten Texte der Einheit. Whorf 1940, Malotki 1983 „Hopi Time" (ironischer Titel, fast 700 Seiten), Jonathan Winawer 2007 MIT-Studie zu _goluboj_/_sinij_, Stephen Levinson + Guugu Yimithirr in Australien („Pass auf deinen nördlichen Fuß auf"), Lera Boroditsky / Stanford / Brücke-Puente-Experiment (feminin/maskulin → unterschiedliche Adjektivassoziationen), die Inuit-Schnee-Legende als Franz-Boas-Missverständnis sauber entzaubert, am Ende Guy Deutscher: „Sprache … keine Gefängnismauer, sondern eine Linse: Sie schließt nichts aus, aber sie bestimmt, was scharf und was unscharf gesehen wird." — das ist die Bildschlussformel, die Einheit 4 als ganze zusammenhalten könnte. Vorentlastung mit 10 Termen + dynamischer Highlight-Funktion. Anführungszeichen korrekt.

**Antithese.**
- In den Beispielsätzen innerhalb des Textes werden die eingeführten Forschernamen durchgängig mit Vorname + Nachname zitiert („Jonathan Winawer", „Lera Boroditsky"). Das ist korrekt, aber im zweiten Auftauchen könnte der Nachname allein journalistischer wirken. Sehr feinschliffig — kein Bug.
- Das Zitat aus dem Boroditsky-Experiment _„elegant", „zerbrechlich", „schön"_ und _„stark", „groß", „lang"_ ist perfekt gesetzt. Keine Anmerkung.

**Synthese.**
Nichts anzupassen. Dieser Text ist das ästhetische Maßband für die Einheit.

---

### 3044X · „Redewendungen und Idiome"

**These.**
Lesetext „Eine zweite Sprache hinter der Sprache" beginnt lebendig: _„Wer im Deutschkurs zum ersten Mal hört, man habe jemandem ‚den Kopf gewaschen', zuckt zusammen."_ Dann ein kluger Durchgang: Ursprünge aus der Bibel (Perlen vor die Säue, Hände in Unschuld waschen), aus der Handwerks- und Seemannssprache (Der rote Faden aus der britischen Marine, Fähnlein in den Wind, Rotwelsch der Fahrenden), dazu die Unterscheidung _transparent_ vs _opak_ anhand von „schwarz auf weiß" (durchsichtig) und „einen Bären aufbinden" (undurchsichtig). 10 Pre-Cards sauber definiert.

**Antithese.**
- **Skill-Bug.** 3 von 10 Pre-Cards haben **keine** vocab-hl-Markierung im Lesetext: `die Metapher`, `wörtlich / übertragen`, `sprichwörtlich`. Gerade bei diesen drei wäre es didaktisch besonders wertvoll, da sie Schlüsselbegriffe für das Verständnis des ganzen Themas sind.
- Kleinigkeit: Der Text ist durchweg präsent und gut, aber etwas Konkretes zur _Wendungen_-Herkunft am Ende der Einheit könnte noch stärker auf das Thema Metaphernlogik führen — das ist aber Kosmetik.

**Synthese.**
Prio: 3 fehlende vocab-hl-Spans nachziehen. „Metapher" gehört in den Absatz mit „Berg von Arbeit" oder „schwarz auf weiß". „wörtlich / übertragen" passt in den Absatz über „Kopf waschen" oder die transparent/opak-Unterscheidung. „sprichwörtlich" lässt sich leicht im ersten oder Schlussabsatz einbauen.

---

### 3045G · „Nebensätze mit Subjunktionen"

**These.**
Die Regel-Tabelle ordnet Subjunktionen nach 9 semantischen Gruppen (temporal, kausal, konzessiv, konditional, final, konsekutiv, modal, Aussage, indirekte Frage). Alle Beispielsätze sind thematisch konsistent zu Einheit 4: _„Während sie Deutsch lernte, entdeckte sie auch das Land."_ — _„Obwohl das Deutsche schwer gilt, lernen es viele gern."_ — _„Man lernt Sprachen am besten, indem man sie spricht."_ — _„Die Studie zeigt, dass Mehrsprachigkeit das Gehirn trainiert."_ Deutsche Anführungszeichen 38×/38×. 5 Tabs (Entdecken, Regeln, Lückentext, MC, Satzbau) vollständig.

**Antithese.**
- Keine gravierenden Punkte. Der Tab „Entdecken" könnte — wie in 3035G nach der Aufwertung — etwas mehr mit einem greifbaren Kontrastpaar einsteigen (Hauptsatz vs. Nebensatz-Verbstellung), falls das didaktisch nützlich ist. Dafür müsste ich den Entdecken-Inhalt erst vollständig lesen.

**Synthese.**
Kein akuter Eingriff nötig. Datei erfüllt Pflicht.

---

### 3046R · „Sprachfamilien"

**These.**
Journalistisch wie ein guter Zeit-Wissens-Artikel. Eröffnung: „Ethnologen zählen heute etwa 7000 Sprachen …". Dann August Schleicher, _Compendium der vergleichenden Grammatik_ 1861, der Stammbaum als Biologie-Analogie, die _vergleichende Methode_ mit dem Musterbeispiel pater/Vater, piscis/Fisch, pes/Fuß. Weiter: Proto-Indoeuropäisch (Jungsteinzeit, 4500-2500 v.Chr.), Kurgan-Hypothese (pontisch-kaspische Steppe), Jacob Grimm 1822 und die Grimm'sche Lautverschiebung. Dann Uralisch (Finnisch/Estnisch/Ungarisch mit Vokalharmonie), Sino-Tibetisch, Afroasiatisch, Niger-Kongo, Austronesisch. Schließlich _Sprachisolate_ — Baskisch, Koreanisch (umstritten), Ayacucho-Quechua — und der Schlussgedanke, dass die vergleichende Methode an eine zeitliche Grenze stößt: „Der Stammbaum der Sprachen … hat einen festen Horizont — und hinter diesem Horizont beginnt die Spekulation." Das ist B2-Prosa mit Würde.

**Antithese.**
- Nichts Gravierendes. Vorentlastung mit 10 Termen + Highlight-JS. Anführungszeichen korrekt.
- Sehr gelegentlich ist die Satzrhythmik lang (drei Kommas in einem Satz) — das ist aber eine bewusste Eigenschaft journalistischer Sachprosa und bei B2+ angemessen.

**Synthese.**
Nichts zu tun. Dieser Text ist — gemeinsam mit 3043R — das zweite Maßband der Einheit.

---

### 3047X · „Passiversatz mit ‚sich lassen'"

**These.**
Inhaltlich präzise und pädagogisch klar: Das werden-Passiv → _sich lassen + Inf._ → _sein + zu + Inf._ → _-bar-Adjektive_ → _man + Aktiv_. Konkrete Paare durchgehend: „Das Problem kann gelöst werden" ↔ „Das Problem lässt sich lösen". „Der Antrag ist bis Freitag zu stellen" als Verwaltungsregister, „Die Klinge lässt sich mit einem Handgriff wechseln" als Werbeslogan. Die Grenzen werden sauber gezogen (kein „*gehbar", „man" nur mit menschlichem Agens). 10 Pre-Cards, und — anders als 3041X/3044X — **alle 10** haben die entsprechende vocab-hl-Markierung im Lesetext. Vorbildlich.

**Antithese.**
- Nichts Substanzielles. Der Text ist etwas länger als 3043R/3046R und könnte in einem finalen Lektorat noch 20–30 Zeilen enger gefasst werden, aber das ist Geschmackssache.

**Synthese.**
Nichts zu tun. Die Datei erfüllt sowohl Skill als auch Ästhetik.

---

### 3048S · „Von Sprachen sprechen"

**These.**
Fünf Tabs: Redemittel (6 Themenblöcke), Sprechanlässe (6 mit unterschiedlichen Zugängen — Sprachbiografie, unübersetzbare Wörter, Sprache und Identität, Code-Switching, Redewendungen), Diskussionsfragen (6 gesellschaftliche Themen — Sprachtod, Englisch als Lingua franca, gendergerechte Sprache, maschinelle Übersetzung, Dialekt vs. Hochsprache, Herkunftssprachen), Pro & Contra „Englisch als alleinige Wissenschaftssprache" und ein durchkomponiertes Rollenspiel „Anhörung zur Sprachenpolitik" mit 4 Rollen: Prof. Dr. Melike Öztürk (Sprachwissenschaftlerin), Stefan Wagner (Bildungspolitiker), Aysel Demir (Elternbeirätin), Dr. Christine Meyer (Grundschulrektorin). Der soziolinguistische Bogen vom Persönlichen (Sprachbiografie) zum Politischen (Anhörung) ist gut gebaut.

**Antithese.**
- Nichts Skill-Relevantes. Die Redemittel-Listen sind Listen — naturgemäß kein Ort für sprachliche Ästhetik im journalistischen Sinn. Dafür ist der Rahmen (h2-Titel, h3-Unterteilungen, nav-Labels) klar.
- Sehr kleiner Punkt: die Anzahl der li-Elemente (50+) könnte einzelne Lernende überfordern, wenn alles in einem Tab sichtbar ist. Das ist aber ein didaktisches Designdetail, kein Bug.

**Synthese.**
Nichts zu korrigieren. Eine saubere Abschluss-Datei der Einheit.

---

## Skill-Compliance-Matrix (9 Regeln × 8 Dateien)

| Regel | 3041X | 3042G | 3043R | 3044X | 3045G | 3046R | 3047X | 3048S |
|-------|:-----:|:-----:|:-----:|:-----:|:-----:|:-----:|:-----:|:-----:|
| 1 Anführungszeichen | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| 2 Author-Footer | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| 3 Quasthoff-Basis | ≈ | ≈ | n/a | ≈ | ≈ | n/a | ≈ | n/a |
| 4 Kein Prüfen-Button | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| 5 Keine Nummerierung | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| 6 Saubere Tab-Namen | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| 7 Antwort versteckt | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | n/a |
| 8 Direct-Feedback | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | n/a |
| vocab-hl vs. pre-card | ⚠️ 7/10 | n/a | ✅ (dyn.) | ⚠️ 7/10 | n/a | ✅ (dyn.) | ✅ 10/10 | n/a |

_≈ = Lesetext-Quellen, nicht Kollokationswörterbuch-basiert — für R/X akzeptiert, vorbildlich wäre Quasthoff-Anbindung._

---

## Prioritätenliste — was zu tun wäre

**Priorität A (kritische Skill-Bugs, müssen gefixt werden).**
1. **3041X:** 3 vocab-hl-Spans ergänzen (`die Sprachfamilie`, `der Dialekt`, `das Sprachsterben`).
2. **3044X:** 3 vocab-hl-Spans ergänzen (`die Metapher`, `wörtlich / übertragen`, `sprichwörtlich`).

**Priorität B (stilistisch-ästhetisch, optional).**
3. **3042G:** „als ob"-Beispiel um eine normkonforme K I-Variante erweitern.
4. **3042G + 3045G:** Entdecken-Tabs prüfen, ob sie das Niveau der neu aufgewerteten 3032G/3035G aus Einheit 3 erreichen; ggf. einen greifbareren Einstieg setzen.

**Priorität C (nicht nötig, nur zur Dokumentation).**
5. **3043R, 3046R, 3047X, 3048S, 3041X-Lesetext, 3044X-Lesetext:** inhaltlich und stilistisch in Ordnung — ästhetisch auf Augenhöhe mit 3036R/3034X aus Einheit 3.

**Banner-Prüfung:** alle 8 Dateien haben 5–7 Bilder vollständig als Base64 eingebettet, keine placehold.co-Platzhalter mehr, keine toten URLs. Einheit 4 ist an dieser Stelle bereits sauber — im Gegensatz zum Ausgangszustand von Einheit 3.

---

## Empfehlung

Wenn du „leg los" sagst, setze ich Priorität A um — die 6 vocab-hl-Spans nachziehen — und gehe dann optional an Priorität B, wenn der Audit nicht bereits alles erfasst hat, was dir wichtig ist. Die Substanz der Lesetexte ist hier, anders als bei Einheit 3, von Anfang an hoch; eine vergleichbare Substanzarbeit wie an 3031X/3032G ist nicht nötig.
