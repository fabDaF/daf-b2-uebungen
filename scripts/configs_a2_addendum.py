#!/usr/bin/env python3
"""Addendum für configs_a2.py — 48 zusätzliche V/G/W-Konfigurationen.

Wird nach dem Schreiben in configs_a2.py eingefügt, vor dem schließenden '}'.
Erzeugt am 22.05.2026 als Teil des Schreibwerkstatt-Rollouts auf A2.
"""

BANNER_URL = 'https://images.pexels.com/photos/733856/pexels-photo-733856.jpeg?auto=compress&cs=tinysrgb&w=800'
BANNER_ALT = 'Notizbuch und Stift, bereit zum Schreiben'


def v(code, title, theme, samples):
    """V-Datei Vokabular-Pattern.

    samples = dict mit Schlüsseln: persoenlich, beobachtung, frage, liste, dialog.
    Jeder Wert ist (titel, frage, beispiel).
    """
    tasks = []
    for key in ('persoenlich', 'beobachtung', 'frage', 'liste', 'dialog'):
        t, f, b = samples[key]
        tasks.append({'titel': t, 'frage': f, 'beispiel': b})
    return {
        'lesson_code': code,
        'lesson_title': title,
        'banner_url': BANNER_URL, 'banner_alt': BANNER_ALT,
        'intro': f'Fünf kleine Schreibaufgaben rund um „{theme}" und deine eigenen Erfahrungen mit dem Thema.',
        'tasks': tasks,
    }


def g(code, title, struct, samples):
    """G-Datei Grammatik-Pattern (Zielstruktur wird erzwungen)."""
    tasks = []
    for key in ('erfahrung', 'beobachtung', 'frage', 'liste', 'dialog'):
        t, f, b = samples[key]
        tasks.append({'titel': t, 'frage': f, 'beispiel': b})
    return {
        'lesson_code': code,
        'lesson_title': title,
        'banner_url': BANNER_URL, 'banner_alt': BANNER_ALT,
        'intro': f'Fünf kleine Schreibaufgaben, bei denen du {struct} aktiv übst. Jede Aufgabe verlangt diese Struktur — nimm sie als Trainingseinheit.',
        'tasks': tasks,
    }


CONFIGS_NEW = {

    # ============================================================
    # EINHEIT 1 — V-Dateien (12)
    # ============================================================

    '1011V': v('1011V', 'Meine Freunde', 'Freunde', {
        'persoenlich': ('Dein bester Freund', 'Wer ist dein bester Freund oder deine beste Freundin? Wie lange kennt ihr euch? Schreib zwei oder drei Sätze.',
                        'Mein bester Freund heißt Carlos. Wir kennen uns seit der Grundschule, also seit 25 Jahren. Er wohnt jetzt in Madrid.'),
        'beobachtung': ('Was Freunde ausmacht', 'Was ist für dich eine gute Freundschaft? Schreib zwei Sätze.',
                        'Eine gute Freundschaft ist für mich, dass man ehrlich ist. Man muss sich auch in schweren Momenten helfen.'),
        'frage': ('Eine Frage an deinen Freund', 'Stell deinem besten Freund oder deiner besten Freundin eine Frage, die du noch nie gestellt hast.',
                  'Lieber Carlos, was war eigentlich dein schönster Moment in den letzten zehn Jahren?'),
        'liste': ('Drei Freunde, drei Eigenschaften', 'Schreib zu drei Freunden je eine Eigenschaft, die dir besonders gefällt.',
                  'Anna ist sehr lustig. Carlos ist immer pünktlich. Maria hört wirklich zu, wenn ich rede.'),
        'dialog': ('Mini-Dialog: Verabredung', 'Schreib einen kurzen Dialog (2 Fragen, 2 Antworten) zwischen dir und einem Freund über ein Treffen.',
                   '— Hast du am Samstag Zeit? — Ja, was möchtest du machen? — Ich gehe ins Kino, kommst du mit? — Gerne, um wie viel Uhr?'),
    }),

    '1015V': v('1015V', 'Gefühle und Stimmungen', 'Gefühle', {
        'persoenlich': ('Wie geht es dir heute?', 'Beschreib in zwei Sätzen, wie du dich heute fühlst und warum.',
                        'Heute bin ich sehr zufrieden. Ich habe gut geschlafen und die Sonne scheint.'),
        'beobachtung': ('Ein Gefühl, das du gut kennst', 'Welches Gefühl hast du oft? Wann kommt es? Zwei Sätze.',
                        'Ich bin oft nervös vor Prüfungen. Mein Bauch tut weh und ich kann nicht schlafen.'),
        'frage': ('Eine Frage an einen Freund', 'Frag einen Freund nach seinen Gefühlen. Schreib zwei Fragen.',
                  'Geht es dir gut? Was macht dich im Moment glücklich oder traurig?'),
        'liste': ('Drei Gefühle in einer Woche', 'Welche drei Gefühle hattest du in dieser Woche? Schreib zu jedem einen kurzen Satz.',
                  'Am Montag war ich gestresst. Am Mittwoch war ich glücklich. Am Samstag war ich entspannt.'),
        'dialog': ('Mini-Dialog: Was ist los?', 'Dein Freund sieht traurig aus. Schreib einen kurzen Dialog (2 Fragen, 2 Antworten).',
                   '— Du siehst heute traurig aus. Was ist los? — Mein Hund ist krank. — Oh nein, das tut mir leid. — Danke, hoffentlich wird er bald wieder gesund.'),
    }),

    '1021V': v('1021V', 'Die Arbeitswelt', 'Arbeit', {
        'persoenlich': ('Dein Beruf', 'Was machst du beruflich? Wo arbeitest du? Schreib zwei oder drei Sätze.',
                        'Ich arbeite als Krankenschwester in einem Krankenhaus in Berlin. Meine Arbeit ist anstrengend, aber wichtig.'),
        'beobachtung': ('Ein typischer Arbeitstag', 'Beschreib einen typischen Tag bei der Arbeit. Zwei Sätze.',
                        'Ich beginne um 7 Uhr und mache zuerst die Morgenrunde. Mittags gibt es eine halbe Stunde Pause.'),
        'frage': ('Eine Frage an einen Kollegen', 'Schreib zwei Fragen, die du einem neuen Kollegen am ersten Tag stellen würdest.',
                  'Seit wann arbeitest du hier? Was magst du an diesem Beruf besonders?'),
        'liste': ('Drei Dinge, die du an deiner Arbeit magst', 'Nenn drei Dinge, die dir an deiner Arbeit gefallen. Je ein Satz.',
                  'Ich mag meine Kollegen. Die Bezahlung ist gut. Ich kann anderen Menschen helfen.'),
        'dialog': ('Mini-Dialog: Beim Mittagessen', 'Schreib einen kurzen Dialog mit einem Kollegen in der Mittagspause.',
                   '— Wie war dein Vormittag? — Sehr stressig, drei Patienten. — Komm, lass uns kurz rausgehen. — Ja, ich brauche frische Luft.'),
    }),

    '1025V': v('1025V', 'Die Firma', 'die Firma', {
        'persoenlich': ('Deine Firma oder dein Studienort', 'Wo arbeitest oder studierst du? Wie groß ist die Firma oder die Universität? Zwei Sätze.',
                        'Ich arbeite bei einer kleinen Marketing-Agentur in Köln. Wir sind zwölf Mitarbeiter und drei Praktikanten.'),
        'beobachtung': ('Die Stimmung in deiner Firma', 'Wie ist die Stimmung an deinem Arbeitsplatz? Zwei Sätze.',
                        'In meiner Firma ist die Stimmung meistens freundlich. Wir lachen viel und helfen uns gegenseitig.'),
        'frage': ('Eine Frage an deinen Chef', 'Was würdest du deinen Chef gern fragen, wenn du dürftest?',
                  'Warum dauert es so lange, bis Entscheidungen getroffen werden? Können wir nicht schneller arbeiten?'),
        'liste': ('Drei Abteilungen in deiner Firma', 'Nenn drei Abteilungen oder Bereiche, die du kennst, und je eine Aufgabe.',
                  'Die Buchhaltung kümmert sich um die Rechnungen. Das Marketing macht die Werbung. Die Personalabteilung sucht neue Kollegen.'),
        'dialog': ('Mini-Dialog: Am Empfang', 'Schreib einen kurzen Dialog: ein Besucher kommt an den Empfang deiner Firma.',
                   '— Guten Tag, ich habe einen Termin mit Frau Meyer. — Wie ist Ihr Name, bitte? — Müller, ich komme von der Firma Schulz. — Einen Moment, ich rufe Frau Meyer.'),
    }),

    '1031V': v('1031V', 'Einziehen und Ausziehen', 'umziehen', {
        'persoenlich': ('Dein letzter Umzug', 'Wann bist du das letzte Mal umgezogen? Wohin und warum? Schreib zwei oder drei Sätze.',
                        'Vor zwei Jahren bin ich von Stuttgart nach Berlin gezogen. Ich habe hier eine neue Stelle gefunden und wollte etwas Neues sehen.'),
        'beobachtung': ('Was beim Umziehen stressig ist', 'Was ist beim Umzug am stressigsten? Zwei Sätze.',
                        'Am stressigsten ist für mich das Packen der Kisten. Es dauert immer viel länger, als ich denke.'),
        'frage': ('Eine Frage an einen Freund, der umzieht', 'Stell deinem Freund zwei Fragen vor seinem Umzug.',
                  'Brauchst du Hilfe beim Packen? Hast du schon einen Transporter gemietet?'),
        'liste': ('Vier Dinge, die du beim Einziehen brauchst', 'Was brauchst du sofort, wenn du in eine neue Wohnung einziehst?',
                  'Ein Bett zum Schlafen. Einen Stuhl und einen Tisch. Geschirr und Besteck für die Küche. Eine Lampe für das Wohnzimmer.'),
        'dialog': ('Mini-Dialog: Bei der Wohnungsbesichtigung', 'Schreib einen kurzen Dialog zwischen Vermieter und Mieter.',
                   '— Guten Tag, hier ist das Wohnzimmer. — Wie hoch ist die Miete genau? — 750 Euro warm, also mit Heizung. — Und wann könnte ich einziehen?'),
    }),

    '1035V': v('1035V', 'Mein Zuhause', 'Zuhause', {
        'persoenlich': ('Deine Wohnung', 'Wo wohnst du? Wie viele Zimmer hat deine Wohnung? Zwei oder drei Sätze.',
                        'Ich wohne in einer Drei-Zimmer-Wohnung im zweiten Stock. Mein Lieblingsort ist der kleine Balkon mit Blick auf den Garten.'),
        'beobachtung': ('Dein Lieblingsraum', 'Welcher Raum in deiner Wohnung gefällt dir am besten? Warum? Zwei Sätze.',
                        'Mein Lieblingsraum ist die Küche, weil ich gern koche. Dort sind auch die Familienfotos.'),
        'frage': ('Eine Frage an einen Besucher', 'Ein Freund kommt zum ersten Mal zu dir. Was möchtest du ihm zeigen oder fragen?',
                  'Komm rein! Möchtest du erst die Wohnung sehen oder direkt etwas trinken?'),
        'liste': ('Vier Räume, vier Dinge', 'Schreib zu vier Räumen je ein wichtiges Möbelstück.',
                  'Im Schlafzimmer steht das Bett. Im Wohnzimmer das Sofa. In der Küche der Esstisch. Im Bad die Dusche.'),
        'dialog': ('Mini-Dialog: Du zeigst die Wohnung', 'Schreib einen kurzen Dialog, in dem du jemandem deine Wohnung zeigst.',
                   '— Das ist mein Wohnzimmer. — Oh, ist das hell! — Ja, im Sommer ist es manchmal zu warm. — Und woher hast du dieses schöne Bild?'),
    }),

    '1041V': v('1041V', 'Das Leben in der Stadt', 'das Stadtleben', {
        'persoenlich': ('Deine Stadt', 'In welcher Stadt wohnst du? Was magst du an ihr? Schreib zwei oder drei Sätze.',
                        'Ich wohne in München. Die Stadt ist sauber, hat viele Parks und liegt nahe an den Bergen.'),
        'beobachtung': ('Vorteile der Stadt', 'Nenne zwei Vorteile vom Leben in der Stadt.',
                        'In der Stadt kann ich ohne Auto leben. Es gibt immer etwas zu tun: Kino, Restaurants, Konzerte.'),
        'frage': ('Eine Frage an einen Stadtbesucher', 'Ein Tourist kommt zum ersten Mal in deine Stadt. Was möchtest du ihn fragen?',
                  'Hast du schon den Marienplatz gesehen? Möchtest du eine echte Brezel probieren?'),
        'liste': ('Drei Orte in deiner Stadt', 'Nenn drei Orte und sag, was man dort machen kann.',
                  'Im Englischen Garten kann man spazieren. Am Viktualienmarkt kann man Spezialitäten kaufen. In der Oper hört man Musik.'),
        'dialog': ('Mini-Dialog: Stadt oder Land?', 'Schreib einen kurzen Dialog: jemand fragt dich, ob du lieber in der Stadt oder auf dem Land lebst.',
                   '— Wohnst du gern in der Stadt? — Ja, sehr gern. — Aber es ist doch laut, oder? — Stimmt, manchmal vermisse ich die Ruhe.'),
    }),

    '1045V': v('1045V', 'Kunst und Kultur', 'Kunst und Kultur', {
        'persoenlich': ('Dein letzter Kulturbesuch', 'Wann warst du das letzte Mal im Museum, im Theater oder bei einem Konzert? Zwei Sätze.',
                        'Vor zwei Wochen war ich im Picasso-Museum in Berlin. Mir hat besonders die blaue Periode gefallen.'),
        'beobachtung': ('Welche Kunstform magst du?', 'Welche Kunst gefällt dir am besten — Malerei, Musik, Theater, Film? Warum? Zwei Sätze.',
                        'Ich mag Filme am liebsten. Sie erzählen Geschichten und ich kann darin in andere Welten reisen.'),
        'frage': ('Eine Frage an einen Künstler', 'Wenn du einen Künstler treffen könntest — was würdest du ihn fragen?',
                  'Wie lange brauchen Sie für ein Bild? Was inspiriert Sie am meisten?'),
        'liste': ('Drei Künstler oder Werke', 'Nenne drei Künstler oder Kunstwerke, die du gut findest, und sag kurz warum.',
                  'Picasso, weil seine Bilder ungewöhnlich sind. Mozart, weil seine Musik fröhlich ist. „Der kleine Prinz", weil das Buch so tief ist.'),
        'dialog': ('Mini-Dialog: Im Museum', 'Schreib einen kurzen Dialog zwischen zwei Besuchern im Museum.',
                   '— Was meinst du zu diesem Bild? — Ich verstehe es nicht so richtig. — Es soll Einsamkeit zeigen. — Ach so, jetzt sehe ich es auch.'),
    }),

    '1051V': v('1051V', 'Sport treiben', 'Sport', {
        'persoenlich': ('Dein Sport', 'Welchen Sport machst du? Wie oft? Schreib zwei oder drei Sätze.',
                        'Ich gehe zweimal pro Woche schwimmen. Außerdem mache ich am Wochenende lange Spaziergänge mit meinem Hund.'),
        'beobachtung': ('Warum du Sport machst (oder nicht)', 'Warum machst du Sport — oder warum nicht? Zwei Sätze.',
                        'Ich mache Sport, weil ich danach besser schlafe. Außerdem brauche ich die frische Luft nach der Arbeit.'),
        'frage': ('Eine Frage an einen Sportler', 'Stell einem Profisportler oder einer Sportlerin zwei Fragen.',
                  'Wie viele Stunden trainieren Sie am Tag? Was essen Sie vor einem Wettkampf?'),
        'liste': ('Vier Sportarten, vier Meinungen', 'Was hältst du von vier Sportarten? Je ein kurzer Satz.',
                  'Fußball ist mir zu laut. Yoga ist sehr entspannend. Schwimmen mag ich am liebsten. Boxen finde ich zu gefährlich.'),
        'dialog': ('Mini-Dialog: Im Fitnessstudio', 'Schreib einen kurzen Dialog zwischen zwei Personen im Fitnessstudio.',
                   '— Hi, machst du das Programm zum ersten Mal? — Ja, gestern habe ich angefangen. — Es lohnt sich, weiterzumachen. — Danke für die Motivation!'),
    }),

    '1055V': v('1055V', 'Fit bleiben', 'fit bleiben', {
        'persoenlich': ('Wie du fit bleibst', 'Was machst du, um gesund und fit zu bleiben? Schreib zwei oder drei Sätze.',
                        'Ich versuche, jeden Tag 30 Minuten zu Fuß zu gehen. Außerdem trinke ich viel Wasser und schlafe genug.'),
        'beobachtung': ('Ein gesunder Tag', 'Beschreib einen Tag, an dem du dich besonders gesund verhalten hast. Zwei Sätze.',
                        'Letzten Samstag habe ich ein gesundes Frühstück gegessen. Danach bin ich eine Stunde Rad gefahren.'),
        'frage': ('Eine Frage an einen Arzt', 'Was würdest du einen Arzt zum Thema Gesundheit fragen?',
                  'Wie viele Stunden Schlaf braucht ein Erwachsener wirklich? Ist 6 Stunden genug?'),
        'liste': ('Vier kleine Gewohnheiten', 'Nenn vier kleine Gewohnheiten, die für deine Gesundheit gut sind.',
                  'Ich nehme die Treppe statt den Aufzug. Ich trinke zwei Liter Wasser pro Tag. Ich esse Obst zum Frühstück. Ich gehe vor 23 Uhr ins Bett.'),
        'dialog': ('Mini-Dialog: Beim Arzt', 'Schreib einen kurzen Dialog beim Arzt — der Arzt fragt nach deinen Gewohnheiten.',
                   '— Wie viel Sport machen Sie pro Woche? — Etwa drei Stunden. — Sehr gut. Und wie sieht es mit dem Schlaf aus? — Ich schlafe meistens sieben Stunden.'),
    }),

    '1061V': v('1061V', 'Pläne machen', 'Pläne', {
        'persoenlich': ('Dein Plan für das Wochenende', 'Was hast du am Wochenende vor? Schreib zwei oder drei Sätze.',
                        'Am Samstag werde ich meine Eltern besuchen. Am Sonntag möchte ich lange schlafen und ein gutes Buch lesen.'),
        'beobachtung': ('Wie planst du dein Leben?', 'Bist du ein Planer oder spontan? Erklär kurz, warum. Zwei Sätze.',
                        'Ich plane gern alles im Voraus. Wenn ich keinen Plan habe, fühle ich mich unruhig.'),
        'frage': ('Eine Frage an einen Freund', 'Frag einen Freund nach seinen Plänen für nächste Woche.',
                  'Hast du nächste Woche schon etwas vor? Hättest du Zeit für ein Treffen am Mittwoch?'),
        'liste': ('Drei kleine Ziele', 'Welche drei kleinen Ziele hast du für diesen Monat?',
                  'Ich werde zwei neue deutsche Bücher lesen. Ich möchte 100 neue Vokabeln lernen. Und ich werde meine Wohnung gründlich putzen.'),
        'dialog': ('Mini-Dialog: Verabredung planen', 'Schreib einen kurzen Dialog, in dem zwei Freunde sich verabreden.',
                   '— Wann hast du diese Woche Zeit? — Donnerstag wäre gut. — Perfekt, sollen wir ins Café? — Ja, um 17 Uhr beim Mariencafé.'),
    }),

    '1065V': v('1065V', 'Zukunftspläne', 'Zukunftspläne', {
        'persoenlich': ('Dein Plan für die nächsten fünf Jahre', 'Was möchtest du in den nächsten fünf Jahren erreichen? Schreib zwei oder drei Sätze.',
                        'In den nächsten fünf Jahren möchte ich mein Deutsch auf C1-Niveau bringen. Außerdem plane ich, mit meiner Partnerin in eine eigene Wohnung zu ziehen.'),
        'beobachtung': ('Ein Traum, den du hast', 'Was ist ein großer Traum von dir? Zwei Sätze.',
                        'Mein Traum ist es, ein eigenes Café zu eröffnen. Ich möchte einen Ort schaffen, an dem sich Menschen wohlfühlen.'),
        'frage': ('Eine Frage an dein zukünftiges Ich', 'Stell deinem zukünftigen Ich (in 10 Jahren) eine Frage.',
                  'Bist du immer noch in Berlin? Hast du den Mut gehabt, dein Café zu eröffnen?'),
        'liste': ('Drei Pläne, drei Schritte', 'Nenn drei Zukunftspläne und je einen ersten Schritt dahin.',
                  'Plan: Berufswechsel. Erster Schritt: einen Sprachkurs machen. Plan: Reise nach Japan. Erster Schritt: sparen. Plan: gesünder leben. Erster Schritt: Zucker reduzieren.'),
        'dialog': ('Mini-Dialog: Über Pläne sprechen', 'Schreib einen kurzen Dialog zwischen zwei Personen, die über ihre Pläne reden.',
                   '— Was möchtest du in fünf Jahren machen? — Ich möchte in Deutschland leben. — Echt? Allein oder mit Familie? — Mit Familie, wenn es klappt.'),
    }),

    # ============================================================
    # EINHEIT 1 — G-Dateien (12)
    # ============================================================

    '1013G': g('1013G', 'Das Plusquamperfekt', 'das Plusquamperfekt', {
        'erfahrung': ('Eine Erinnerung', 'Erzähl eine kurze Erinnerung mit Plusquamperfekt: was war passiert, bevor etwas anderes geschah? Zwei Sätze.',
                      'Bevor ich nach Berlin gezogen war, hatte ich zwei Jahre in Madrid gelebt. Dort hatte ich auch meine ersten Deutsch-Stunden genommen.'),
        'beobachtung': ('Ein Tag, den du nicht vergisst', 'Beschreib einen wichtigen Tag mit Plusquamperfekt — was hatte vorher schon stattgefunden?',
                        'An dem Tag hatte es schon stundenlang geregnet. Ich war früh aufgestanden und hatte schon gefrühstückt, als der Anruf kam.'),
        'frage': ('Eine Frage im Plusquamperfekt', 'Stell jemandem eine Frage im Plusquamperfekt — z.B. „Hattest du schon … gemacht?"',
                  'Hattest du schon Deutsch gelernt, bevor du nach Deutschland gezogen bist? Wie viele Wörter hattest du etwa gekannt?'),
        'liste': ('Drei Dinge, die du vor 18 schon erlebt hattest', 'Schreib drei Dinge im Plusquamperfekt, die du vor deinem 18. Geburtstag schon erlebt hattest.',
                  'Mit 18 hatte ich schon zwei Länder besucht. Ich hatte schon einen Sommerjob gemacht. Und ich hatte schon eine erste große Liebe erlebt.'),
        'dialog': ('Mini-Dialog: Plusquamperfekt', 'Schreib einen kurzen Dialog (2 Fragen, 2 Antworten) im Plusquamperfekt.',
                   '— Warst du schon im Restaurant, als ich ankam? — Nein, ich war noch nicht angekommen. — Aber Tom war schon da? — Ja, er hatte sogar schon bestellt.'),
    }),

    '1017G': g('1017G', 'Präpositionen mit Akkusativ und Dativ', 'Präpositionen mit Akkusativ und Dativ', {
        'erfahrung': ('Dein letzter Ausflug', 'Erzähl in zwei Sätzen von einem Ausflug — nutze Präpositionen mit Dativ und Akkusativ (z.B. „in den Park", „an dem See").',
                      'Letzten Sonntag bin ich in den Wald gegangen. Am Bach habe ich zwei Stunden auf einem Stein gesessen.'),
        'beobachtung': ('Wo du heute warst', 'Beschreib in zwei Sätzen, wo du heute überall warst. Mit Präpositionen!',
                        'Heute war ich zuerst auf dem Markt, dann bin ich in die Apotheke gegangen. Am Nachmittag habe ich im Café gearbeitet.'),
        'frage': ('Eine Wegfrage', 'Stell jemandem eine Frage nach dem Weg. Nutze passende Präpositionen.',
                  'Entschuldigung, wie komme ich zum Bahnhof? Muss ich an der Kirche links oder rechts gehen?'),
        'liste': ('Vier Orte in deiner Stadt', 'Nenne vier Orte und sag, was du dort machst — mit Präpositionen.',
                  'Im Park gehe ich spazieren. Auf dem Markt kaufe ich frisches Gemüse. In der Bibliothek lese ich. An der Bushaltestelle warte ich auf den Bus.'),
        'dialog': ('Mini-Dialog: Wo bist du gerade?', 'Schreib einen kurzen Telefon-Dialog: jemand fragt, wo du bist.',
                   '— Wo bist du gerade? — Ich bin im Supermarkt, an der Kasse. — Sollen wir uns danach im Café treffen? — Ja, in 20 Minuten am alten Marktplatz.'),
    }),

    '1023G': g('1023G', 'Verben mit Dativ', 'Verben mit Dativ (helfen, gefallen, gehören, danken …)', {
        'erfahrung': ('Wem du heute geholfen hast', 'Wem hast du heute oder gestern geholfen? Schreib zwei Sätze mit Dativ-Verben.',
                      'Heute habe ich meiner Oma geholfen, die Einkäufe nach oben zu tragen. Sie hat mir später einen Kaffee angeboten.'),
        'beobachtung': ('Was dir gefällt', 'Was gefällt dir an deiner Stadt oder deiner Wohnung? Zwei Sätze mit „gefallen".',
                        'Mir gefällt besonders der kleine Park hinter dem Haus. Auch mein Nachbar gefällt mir, weil er immer freundlich grüßt.'),
        'frage': ('Eine Frage mit „gehören" oder „passen"', 'Stell zwei Fragen mit Dativ-Verben („gehören", „passen", „schmecken").',
                  'Wem gehört diese Jacke da auf dem Stuhl? Schmeckt dir der Kuchen, den ich gebacken habe?'),
        'liste': ('Drei Dinge, drei Personen', 'Verbinde drei Dinge mit drei Personen — nutze „gehören".',
                  'Der Hund gehört meiner Schwester. Das Auto gehört unserem Nachbarn. Das alte Klavier gehört meinen Eltern.'),
        'dialog': ('Mini-Dialog: Hilfe anbieten', 'Schreib einen kurzen Dialog, in dem jemand Hilfe anbietet.',
                   '— Soll ich dir helfen? — Ja, danke, das ist zu schwer für mich. — Gib es mir, ich trage es nach oben. — Du hast mir sehr geholfen, danke.'),
    }),

    '1027G': g('1027G', 'Wechselpräpositionen', 'die neun Wechselpräpositionen (an, auf, hinter, in, neben, über, unter, vor, zwischen) mit Akkusativ und Dativ', {
        'erfahrung': ('Was du heute bewegt hast', 'Beschreib in zwei Sätzen, was du heute irgendwohin gestellt oder gelegt hast — mit Wechselpräpositionen.',
                      'Ich habe mein Buch auf den Tisch gelegt. Danach habe ich die Schlüssel in die Schublade gesteckt.'),
        'beobachtung': ('Dein Schreibtisch', 'Was steht oder liegt auf deinem Schreibtisch? Zwei Sätze mit Wechselpräpositionen (Dativ — Ort).',
                        'Auf meinem Schreibtisch steht der Computer. Neben dem Computer liegt ein Notizbuch. Hinter dem Bildschirm sehe ich eine Pflanze.'),
        'frage': ('Eine Wo-Frage und eine Wohin-Frage', 'Stell eine „Wo?"-Frage (Dativ) und eine „Wohin?"-Frage (Akkusativ).',
                  'Wo ist mein Handy — auf dem Tisch oder unter dem Sofa? Wohin soll ich diese Tasche stellen — neben den Stuhl?'),
        'liste': ('Vier Möbel, vier Positionen', 'Nenne vier Möbel und sag, wo sie stehen — mit Wechselpräpositionen.',
                  'Das Bett steht an der Wand. Der Stuhl steht vor dem Fenster. Der Tisch steht zwischen dem Sofa und dem Fernseher. Die Lampe hängt über dem Esstisch.'),
        'dialog': ('Mini-Dialog: Möbel rücken', 'Schreib einen kurzen Dialog: zwei Personen rücken Möbel und sprechen darüber, wohin etwas soll.',
                   '— Wohin sollen wir das Sofa stellen? — Vor das Fenster, würde ich sagen. — Und der Tisch? — Den stellen wir zwischen das Sofa und den Sessel.'),
    }),

    '1033G': g('1033G', 'Der Komparativ', 'den Komparativ (größer, schöner, mehr …)', {
        'erfahrung': ('Du und dein Bruder/Schwester/Freund', 'Vergleiche dich mit einer Person — größer, älter, sportlicher etc. Zwei Sätze.',
                      'Ich bin älter als meine Schwester, aber sie ist sportlicher. Sie läuft viel schneller als ich.'),
        'beobachtung': ('Zwei Städte vergleichen', 'Vergleiche zwei Städte in zwei Sätzen mit Komparativ.',
                        'Berlin ist größer als München. Aber München ist sauberer und teurer.'),
        'frage': ('Eine Komparativ-Frage', 'Stell jemandem eine Vergleichsfrage.',
                  'Findest du Deutsch schwerer als Englisch? Welche Sprache lernst du lieber?'),
        'liste': ('Drei Vergleiche aus deinem Leben', 'Schreib drei Sätze mit Komparativ — Essen, Sport, Hobbys, was du willst.',
                  'Pizza ist leckerer als Pasta. Yoga ist entspannender als Joggen. Berlin ist interessanter als meine Heimatstadt.'),
        'dialog': ('Mini-Dialog: Beim Einkaufen', 'Schreib einen kurzen Dialog: zwei Personen wählen zwischen Produkten und vergleichen.',
                   '— Welcher Pullover gefällt dir besser? — Der blaue ist schöner, aber der rote ist günstiger. — Und welcher ist wärmer? — Ich glaube, der rote.'),
    }),

    '1037G': g('1037G', 'Der Superlativ', 'den Superlativ (am größten, der beste, am schönsten)', {
        'erfahrung': ('Dein bester Moment', 'Was war der schönste Moment deines Lebens bisher? Schreib zwei Sätze mit Superlativ.',
                      'Der schönste Moment meines Lebens war die Geburt meines Kindes. Es war das glücklichste Gefühl, das ich je hatte.'),
        'beobachtung': ('Drei Superlative über deine Stadt', 'Schreib drei Sätze mit Superlativ über deine Stadt.',
                        'Das älteste Gebäude ist das Rathaus. Der schönste Park heißt Hofgarten. Das beste Restaurant findet man in der Altstadt.'),
        'frage': ('Eine Superlativ-Frage', 'Stell jemandem eine Frage mit Superlativ.',
                  'Was war das schönste Geschenk, das du je bekommen hast? Wer ist der wichtigste Mensch in deinem Leben?'),
        'liste': ('Die besten und schlechtesten Dinge', 'Schreib zu drei Themen je einen Superlativ-Satz: Lieblingsessen, Lieblingsfilm, Lieblingsbuch.',
                  'Mein Lieblingsessen ist Pasta — am liebsten mit Tomatensauce. Mein Lieblingsfilm ist „Amélie" — das poetischste Werk. Mein Lieblingsbuch ist „Der kleine Prinz" — das tiefste Kinderbuch.'),
        'dialog': ('Mini-Dialog: Der beste Urlaub', 'Schreib einen kurzen Dialog: zwei Personen sprechen über ihren besten Urlaub.',
                   '— Wo war dein schönster Urlaub? — In Griechenland, auf Santorini. — Was war das Beste? — Der Sonnenuntergang am Meer war unbeschreiblich.'),
    }),

    '1043G': g('1043G', 'Nebensätze mit dass und weil', 'Nebensätze mit „dass" und „weil" — Verb am Satzende!', {
        'erfahrung': ('Was du heute denkst', 'Schreib zwei Sätze über das, was du heute denkst — mit „Ich denke, dass …" oder „Ich glaube, dass …".',
                      'Ich denke, dass mein Deutsch besser wird. Ich glaube auch, dass ich mehr Vokabeln lernen muss.'),
        'beobachtung': ('Etwas, das dich freut — und warum', 'Erzähl, was dich heute freut. Nutze „weil".',
                        'Mich freut heute, dass die Sonne scheint. Ich bin glücklich, weil ich nachher einen Spaziergang machen kann.'),
        'frage': ('Eine Frage mit „warum"', 'Stell eine Frage und gib eine mögliche Antwort mit „weil".',
                  'Warum lernst du Deutsch? Lernst du es, weil du in Deutschland arbeiten möchtest?'),
        'liste': ('Drei Gründe für drei Hobbys', 'Nenne drei deiner Hobbys und je einen Grund — alle mit „weil".',
                  'Ich lese gern, weil ich mich dabei entspanne. Ich koche gern, weil ich kreativ sein kann. Ich gehe gern wandern, weil ich Natur brauche.'),
        'dialog': ('Mini-Dialog: dass und weil', 'Schreib einen kurzen Dialog mit „dass" und „weil".',
                   '— Weißt du, dass Tom umzieht? — Ja, ich glaube, dass er nach München geht. — Warum eigentlich? — Weil er dort eine neue Stelle hat.'),
    }),

    '1047G': g('1047G', 'Reflexive Verben', 'reflexive Verben (sich freuen, sich treffen, sich ärgern …)', {
        'erfahrung': ('Worauf du dich freust', 'Worauf freust du dich diese Woche? Schreib zwei Sätze mit „sich freuen auf".',
                      'Ich freue mich auf das Wochenende mit meiner Familie. Außerdem freue ich mich auf das gute Wetter.'),
        'beobachtung': ('Worüber du dich ärgerst', 'Worüber ärgerst du dich manchmal? Zwei Sätze.',
                        'Ich ärgere mich oft über die langsamen Busse. Auch über laute Nachbarn ärgere ich mich.'),
        'frage': ('Eine Frage mit reflexivem Verb', 'Stell jemandem eine Frage mit einem reflexiven Verb.',
                  'Wann triffst du dich das nächste Mal mit deinen Freunden? Erinnerst du dich noch an unseren ersten Tag im Kurs?'),
        'liste': ('Vier reflexive Sätze über dich', 'Schreib vier kurze Sätze mit reflexiven Verben über deinen Tag.',
                  'Ich wasche mich morgens kalt. Ich beeile mich oft zum Bahnhof. Ich entspanne mich abends mit einem Buch. Ich freue mich auf das Bett.'),
        'dialog': ('Mini-Dialog: sich treffen', 'Schreib einen kurzen Dialog, in dem zwei Personen sich verabreden — mit reflexiven Verben.',
                   '— Wann treffen wir uns? — Sagen wir morgen um 18 Uhr? — Ich freue mich schon. — Ich mich auch — wir haben uns lange nicht gesehen.'),
    }),

    '1053G': g('1053G', 'Der-Wörter und ein-Wörter', 'die der-Wörter (dieser, jeder, welcher) und ein-Wörter (kein, mein, dein, sein)', {
        'erfahrung': ('Dein Lieblingsbuch oder -film', 'Beschreib dein Lieblingsbuch oder deinen Lieblingsfilm mit „dieses", „mein", „kein". Zwei Sätze.',
                      'Dieses Buch heißt „Tschick" und ist mein absolutes Lieblingsbuch. Keinen anderen Roman habe ich öfter gelesen.'),
        'beobachtung': ('Drei Sachen in deinem Zimmer', 'Beschreib drei Sachen mit der-Wörtern oder ein-Wörtern (dieser, mein, kein …).',
                        'Dieser Stuhl ist sehr alt. Mein Computer steht direkt daneben. Keinen Drucker habe ich im Moment.'),
        'frage': ('Frage mit „welcher"', 'Stell zwei Fragen mit „welcher", „welche" oder „welches".',
                  'Welches Buch liest du gerade? Welche Sprachen verstehst du sonst noch?'),
        'liste': ('Drei Personen, drei Eigenschaften', 'Nutze „mein", „dein", „sein", „ihr" — schreib drei Sätze über drei Personen.',
                  'Meine Schwester ist Lehrerin. Sein Bruder studiert Medizin. Ihre beste Freundin lebt in Wien.'),
        'dialog': ('Mini-Dialog: Welches?', 'Schreib einen kurzen Dialog mit Fragen wie „Welcher? Welche? Welches?".',
                   '— Welches T-Shirt soll ich anziehen? — Dieses blaue gefällt mir am besten. — Und welche Hose? — Deine schwarze passt gut dazu.'),
    }),

    '1057G': g('1057G', 'Adjektivendungen', 'Adjektivendungen nach bestimmtem und unbestimmtem Artikel', {
        'erfahrung': ('Dein Outfit heute', 'Beschreib dein Outfit heute mit Adjektivendungen. Zwei Sätze.',
                      'Ich trage heute eine blaue Hose und ein weißes T-Shirt. Dazu habe ich meine alten braunen Schuhe an.'),
        'beobachtung': ('Dein Lieblingsessen', 'Beschreib dein Lieblingsessen mit drei Adjektiven. Zwei Sätze.',
                        'Mein Lieblingsessen ist eine warme italienische Pasta. Mit frischen Tomaten und scharfem Knoblauch schmeckt sie am besten.'),
        'frage': ('Frage mit Adjektivendungen', 'Stell zwei Fragen mit Adjektiven (mit Endungen).',
                  'Magst du den neuen deutschen Film? Hast du schon das alte rote Auto vor unserer Tür gesehen?'),
        'liste': ('Vier Adjektive, vier Sachen', 'Schreib vier Sätze mit Adjektivendungen über vier Sachen.',
                  'Ich habe ein altes Buch. Das ist mein liebster Pulli. Hier sind zwei rote Äpfel. Das war ein schöner Tag.'),
        'dialog': ('Mini-Dialog: Beim Einkaufen', 'Schreib einen kurzen Dialog beim Einkaufen — mit Adjektiven und Endungen.',
                   '— Schau, dieser blaue Mantel ist schön. — Aber die kurze Jacke ist günstiger. — Und ein bisschen wärmer? — Nein, der lange Mantel ist wärmer.'),
    }),

    '1067G': g('1067G', 'Modalverben', 'die Modalverben (können, müssen, wollen, sollen, dürfen, mögen)', {
        'erfahrung': ('Was du heute machen musst', 'Was musst du heute alles machen? Zwei Sätze mit Modalverben.',
                      'Ich muss heute noch einkaufen gehen. Außerdem will ich meinen Bruder anrufen, weil er Geburtstag hat.'),
        'beobachtung': ('Was du gut kannst', 'Was kannst du besonders gut? Was kannst du nicht gut? Zwei Sätze.',
                        'Ich kann sehr gut kochen, besonders italienische Gerichte. Aber ich kann überhaupt nicht singen.'),
        'frage': ('Eine Frage mit Modalverb', 'Stell zwei Fragen mit verschiedenen Modalverben.',
                  'Kannst du mir bei den Hausaufgaben helfen? Soll ich dir den Text später schicken?'),
        'liste': ('Vier Sätze, vier Modalverben', 'Schreib vier Sätze, jeder mit einem anderen Modalverb (können, müssen, dürfen, wollen).',
                  'Ich kann ein bisschen Spanisch sprechen. Heute muss ich früh ins Bett gehen. Hier darf man nicht rauchen. Am Wochenende will ich wandern.'),
        'dialog': ('Mini-Dialog: Mit Modalverben', 'Schreib einen kurzen Dialog (2 Fragen, 2 Antworten) mit Modalverben.',
                   '— Kannst du am Samstag? — Nein, ich muss arbeiten. — Sollen wir uns dann Sonntag treffen? — Ja, das passt — ich will sowieso raus.'),
    }),

    # ============================================================
    # EINHEIT 1 — W-Datei (1)
    # ============================================================

    '1071W': {
        'lesson_code': '1071W',
        'lesson_title': 'Einen Brief schreiben',
        'banner_url': BANNER_URL, 'banner_alt': BANNER_ALT,
        'intro': 'Fünf kleine Schreibaufgaben zu den Bausteinen eines guten Briefes oder einer guten E-Mail.',
        'tasks': [
            {'titel': 'Eine freundliche Anrede', 'frage': 'Schreib drei verschiedene Anreden — eine formelle, eine semi-formelle und eine informelle.',
             'beispiel': 'Formell: „Sehr geehrte Frau Schulz,". Semi-formell: „Liebe Frau Schulz,". Informell: „Hallo Anna,".'},
            {'titel': 'Ein freundlicher Einstieg', 'frage': 'Wie beginnst du eine E-Mail, wenn du schon länger nichts geschrieben hast? Schreib zwei Sätze.',
             'beispiel': 'Ich hoffe, es geht dir gut. Lange habe ich nichts von mir hören lassen — heute will ich das ändern.'},
            {'titel': 'Ein konkretes Anliegen', 'frage': 'Formuliere ein höfliches Anliegen in zwei Sätzen — z.B. eine Bitte um Hilfe oder einen Terminwunsch.',
             'beispiel': 'Ich brauche deinen Rat zu einem kleinen Problem. Hättest du nächste Woche kurz Zeit für ein Telefonat?'},
            {'titel': 'Ein Dank', 'frage': 'Bedank dich in zwei Sätzen für etwas Konkretes.',
             'beispiel': 'Vielen Dank für deine Geduld letzten Montag. Ohne deine Hilfe hätte ich das Formular nicht ausgefüllt bekommen.'},
            {'titel': 'Eine Verabschiedung', 'frage': 'Schreib drei Verabschiedungen — eine formelle, eine semi-formelle, eine informelle.',
             'beispiel': 'Formell: „Mit freundlichen Grüßen, Maria Lopez". Semi-formell: „Herzliche Grüße, Maria". Informell: „Bis bald, Maria".'},
        ]
    },

    # ============================================================
    # EINHEIT 2 — V-Dateien (12)
    # ============================================================

    '2011V': v('2011V', 'Was riecht denn da so gut?', 'Sinneswahrnehmungen', {
        'persoenlich': ('Dein Lieblingsduft', 'Welcher Geruch erinnert dich an etwas Schönes? Zwei oder drei Sätze.',
                        'Der Geruch von frischem Brot erinnert mich an meine Oma. Sie hat jeden Sonntag Brötchen gebacken.'),
        'beobachtung': ('Geräusche um dich herum', 'Welche Geräusche hörst du gerade? Zwei Sätze.',
                        'Draußen höre ich Autos und Stimmen. In der Wohnung tickt nur die Uhr in der Küche.'),
        'frage': ('Eine Frage über Sinne', 'Stell jemandem zwei Fragen über seine Sinneswahrnehmungen.',
                  'Welches Essen schmeckt dir am besten? Welche Musik hörst du, wenn du traurig bist?'),
        'liste': ('Vier Sinne, vier Erinnerungen', 'Nenne zu vier Sinnen je eine schöne Erinnerung.',
                  'Sehen: das Meer in Griechenland. Hören: das Lachen meiner Mutter. Riechen: frischer Kaffee am Sonntag. Schmecken: Schokolade als Kind.'),
        'dialog': ('Mini-Dialog: Geht es dir gut?', 'Schreib einen kurzen Dialog, in dem du nach Geruch oder Geschmack fragst.',
                   '— Was riecht denn da so gut? — Ich backe einen Apfelkuchen. — Schmeckt der so gut wie er riecht? — Probier mal, gleich ist er fertig.'),
    }),

    '2015V': v('2015V', 'Deutsches Essen', 'deutsches Essen', {
        'persoenlich': ('Dein Lieblings-deutsches-Gericht', 'Welches deutsche Gericht magst du am liebsten? Warum? Zwei Sätze.',
                        'Ich liebe Schnitzel mit Bratkartoffeln. Es ist einfach, aber sehr lecker, und ich esse es gern mit Senf.'),
        'beobachtung': ('Unterschiede zu deiner Heimatküche', 'Was ist anders zwischen deutschem und deinem heimischen Essen? Zwei Sätze.',
                        'In Deutschland isst man mehr Kartoffeln und Wurst. In meiner Heimat essen wir mehr Reis und frischen Salat.'),
        'frage': ('Eine Frage an einen Deutschen', 'Frag einen Deutschen zwei Sachen über die deutsche Küche.',
                  'Was esst ihr eigentlich an Weihnachten traditionell? Und was trinkt man dazu?'),
        'liste': ('Drei deutsche Gerichte', 'Nenne drei deutsche Gerichte und sag kurz, wie sie aussehen oder schmecken.',
                  'Sauerbraten ist Rindfleisch in einer süß-sauren Sauce. Spätzle sind kleine Nudeln. Rote Grütze ist eine süße Fruchtspeise.'),
        'dialog': ('Mini-Dialog: Im Restaurant', 'Schreib einen kurzen Dialog im Restaurant zwischen Gast und Kellner.',
                   '— Was empfehlen Sie heute? — Probieren Sie das Wiener Schnitzel — frisch und groß. — Mit Pommes oder Kartoffelsalat? — Mit Kartoffelsalat, bitte.'),
    }),

    '2021V': v('2021V', 'Reisen und Sehenswürdigkeiten', 'Reisen', {
        'persoenlich': ('Dein letztes Reiseziel', 'Wohin bist du das letzte Mal gereist? Schreib zwei oder drei Sätze.',
                        'Letzten Sommer war ich zwei Wochen in Portugal. Ich habe Lissabon und die Atlantikküste besucht.'),
        'beobachtung': ('Eine schöne Sehenswürdigkeit', 'Welche Sehenswürdigkeit hat dich beeindruckt? Zwei Sätze.',
                        'Der Eiffelturm in Paris war beeindruckend, vor allem nachts beleuchtet. Ich hatte erwartet, dass er kleiner ist.'),
        'frage': ('Eine Reise-Frage', 'Stell jemandem zwei Fragen über sein Lieblings-Reiseziel.',
                  'Welches Land möchtest du unbedingt noch besuchen? Was würdest du dort als Erstes machen?'),
        'liste': ('Drei Sehenswürdigkeiten in deiner Region', 'Nenne drei Sehenswürdigkeiten in deiner Stadt oder Region.',
                  'Das Brandenburger Tor steht im Zentrum von Berlin. Der Reichstag liegt direkt an der Spree. Die Museumsinsel ist berühmt für ihre Kunst.'),
        'dialog': ('Mini-Dialog: Reisepläne', 'Schreib einen kurzen Dialog über Reisepläne.',
                   '— Wohin fliegst du im Sommer? — Nach Italien, in die Toskana. — Mit Familie? — Ja, wir mieten ein Haus für zwei Wochen.'),
    }),

    '2025V': v('2025V', 'Gespräche im Hotel', 'das Hotel', {
        'persoenlich': ('Dein letztes Hotel', 'Wann warst du das letzte Mal in einem Hotel? Wie war es? Zwei Sätze.',
                        'Letzten März war ich in einem kleinen Hotel in Amsterdam. Das Zimmer war winzig, aber das Frühstück war ausgezeichnet.'),
        'beobachtung': ('Was ein gutes Hotel ausmacht', 'Was ist dir an einem Hotel wichtig? Drei Dinge in zwei Sätzen.',
                        'Mir sind ein sauberes Bad und ein bequemes Bett wichtig. Außerdem gefällt mir, wenn das Personal freundlich ist.'),
        'frage': ('Eine Frage an der Rezeption', 'Schreib zwei höfliche Fragen, die du an der Hotel-Rezeption stellst.',
                  'Entschuldigung, gibt es im Zimmer kostenloses WLAN? Und ab wann gibt es morgen Frühstück?'),
        'liste': ('Vier Sachen im Hotelzimmer', 'Nenne vier Dinge, die in einem guten Hotelzimmer sein sollten.',
                  'Ein bequemes Bett mit guter Bettdecke. Ein sauberes Bad mit Dusche. Ein Schreibtisch mit Lampe. Ein Wasserkocher für Tee oder Kaffee.'),
        'dialog': ('Mini-Dialog: Check-in', 'Schreib einen kurzen Dialog beim Check-in im Hotel.',
                   '— Guten Abend, ich habe eine Reservierung auf den Namen Müller. — Einen Moment, ja, Zimmer 305. — Ist das Frühstück inklusive? — Ja, von 7 bis 10 Uhr im Restaurant.'),
    }),

    '2031V': v('2031V', 'Dienstleistungen erwerben', 'Dienstleistungen', {
        'persoenlich': ('Letzte Dienstleistung, die du genutzt hast', 'Welche Dienstleistung hast du in letzter Zeit gebraucht? Zwei Sätze.',
                        'Letzten Monat habe ich meinen Computer in eine Werkstatt gebracht, weil er nicht mehr startete. Es hat zwei Tage gedauert.'),
        'beobachtung': ('Gute und schlechte Erfahrungen', 'Eine gute oder schlechte Erfahrung mit einem Dienstleister. Zwei Sätze.',
                        'Mein Friseur ist immer sehr freundlich und macht eine tolle Frisur. Beim Klempner letztens war es leider weniger angenehm.'),
        'frage': ('Eine Frage an einen Dienstleister', 'Stell zwei Fragen, wenn du einen Dienstleister beauftragst.',
                  'Wie lange dauert die Reparatur ungefähr? Wie viel wird sie kosten?'),
        'liste': ('Vier Dienstleistungen, vier Orte', 'Nenne vier Dienstleistungen und sag, wohin man dafür geht.',
                  'Zum Friseur geht man wegen der Haare. In die Reinigung bringt man Kleidung. Beim Optiker kauft man Brillen. Beim Mechaniker repariert man das Auto.'),
        'dialog': ('Mini-Dialog: Beim Friseur', 'Schreib einen kurzen Dialog zwischen Kunde und Friseur.',
                   '— Wie hätten Sie es gern? — Die Spitzen schneiden, bitte. Nicht zu kurz. — Färben auch? — Nein, danke, nur waschen und schneiden.'),
    }),

    '2035V': v('2035V', 'Das Geld', 'Geld', {
        'persoenlich': ('Wie du mit Geld umgehst', 'Bist du eher sparsam oder gibst du gern Geld aus? Zwei Sätze.',
                        'Ich bin ziemlich sparsam, vor allem im Alltag. Aber für gutes Essen und Reisen gebe ich gern Geld aus.'),
        'beobachtung': ('Etwas, das du dir geleistet hast', 'Was hast du dir zuletzt gegönnt? Zwei Sätze.',
                        'Letzten Monat habe ich mir neue Laufschuhe gekauft. Sie waren teuer, aber sie sind super bequem.'),
        'frage': ('Eine Geld-Frage', 'Stell jemandem zwei Fragen über sein Verhältnis zu Geld.',
                  'Sparst du regelmäßig — und wenn ja, wofür? Hast du schon einmal etwas richtig Großes finanziert?'),
        'liste': ('Drei Ausgaben pro Monat', 'Nenne drei monatliche Ausgaben in deinem Leben.',
                  'Die Miete ist die größte Ausgabe. Lebensmittel kommen danach. Mein Handyvertrag kostet rund 30 Euro pro Monat.'),
        'dialog': ('Mini-Dialog: An der Kasse', 'Schreib einen kurzen Dialog an der Supermarktkasse.',
                   '— Das macht 47,80 Euro. — Kann ich mit Karte zahlen? — Natürlich, bitte halten Sie Ihre Karte ran. — Möchten Sie einen Bon? — Nein, danke.'),
    }),

    '2041V': v('2041V', 'Die Ausbildung', 'Ausbildung', {
        'persoenlich': ('Deine Ausbildung oder dein Studium', 'Was hast du gelernt oder studiert? Wie lange? Zwei Sätze.',
                        'Ich habe eine dreijährige Ausbildung zur Bürokauffrau gemacht. Danach habe ich zwei Jahre in einer kleinen Firma gearbeitet.'),
        'beobachtung': ('Was du in der Ausbildung gelernt hast', 'Was war die wichtigste Lektion deiner Ausbildung? Zwei Sätze.',
                        'In der Ausbildung habe ich gelernt, geduldig zu sein. Auch der Umgang mit schwierigen Kunden war eine wichtige Erfahrung.'),
        'frage': ('Eine Frage an einen Auszubildenden', 'Schreib zwei Fragen an jemanden, der gerade eine Ausbildung macht.',
                  'Wie gefällt dir die Ausbildung bisher? Was war bis jetzt das Schwierigste?'),
        'liste': ('Drei Wege nach der Schule', 'Nenne drei Wege nach dem Schulabschluss und sag kurz, was sie bedeuten.',
                  'Eine Ausbildung dauert meistens 3 Jahre. Ein Studium an der Uni dauert 3 bis 5 Jahre. Ein freiwilliges soziales Jahr (FSJ) dauert ein Jahr.'),
        'dialog': ('Mini-Dialog: Beim Bewerbungsgespräch', 'Schreib einen kurzen Dialog im Bewerbungsgespräch.',
                   '— Warum interessieren Sie sich für unsere Ausbildung? — Weil ich gern mit Menschen arbeite. — Welche Erfahrungen bringen Sie mit? — Ich habe ein Praktikum in einer Apotheke gemacht.'),
    }),

    '2045V': v('2045V', 'Meine Biografie', 'Lebenslauf', {
        'persoenlich': ('Drei wichtige Punkte deiner Biografie', 'Nenne drei wichtige Stationen deines Lebens.',
                        'Ich bin in Madrid geboren. Mit 18 bin ich nach Berlin gezogen. Vor drei Jahren habe ich meine Frau geheiratet.'),
        'beobachtung': ('Eine prägende Erfahrung', 'Was war eine wichtige Erfahrung in deinem Leben? Zwei Sätze.',
                        'Mein Auslandssemester in Polen hat mich geprägt. Ich habe gelernt, mit wenig auszukommen und offen für Neues zu sein.'),
        'frage': ('Eine biografische Frage', 'Stell jemandem zwei Fragen über seinen Lebensweg.',
                  'Wo bist du aufgewachsen? Was war dein wichtigster beruflicher Wechsel bisher?'),
        'liste': ('Vier Lebensphasen, vier Sätze', 'Schreib vier kurze Sätze über vier verschiedene Phasen deines Lebens.',
                  'Kindheit: in einem kleinen Dorf. Schulzeit: in der Stadt mit dem Bus. Studium: in der Hauptstadt, allein. Jetzt: verheiratet, mit Hund.'),
        'dialog': ('Mini-Dialog: Lebenslauf', 'Schreib einen kurzen Dialog, in dem jemand nach deinem Lebenslauf fragt.',
                   '— Erzählen Sie kurz von sich. — Ich komme aus Spanien, lebe seit fünf Jahren hier. — Und beruflich? — Ich arbeite als Übersetzerin und unterrichte Spanisch.'),
    }),

    '2051V': v('2051V', 'Technologie', 'Technologie', {
        'persoenlich': ('Dein wichtigstes Gerät', 'Welches Gerät benutzt du am häufigsten? Zwei Sätze.',
                        'Mein Handy benutze ich vom Aufstehen bis ins Bett. Es ist mein Wecker, meine Kamera und mein Kalender.'),
        'beobachtung': ('Technik im Alltag', 'Wie hat Technik deinen Alltag verändert? Zwei Sätze.',
                        'Früher musste ich auf den Bus warten — heute sehe ich auf der App, wann er kommt. Auch die Banküberweisung mache ich nur noch online.'),
        'frage': ('Eine Tech-Frage', 'Stell jemandem zwei Fragen über sein Verhältnis zu Technologie.',
                  'Welche App benutzt du am häufigsten? Hast du schon einmal ein Handy verloren — was hast du gemacht?'),
        'liste': ('Vier Technologien, vier Vorteile', 'Nenne vier Technologien und je einen Vorteil.',
                  'Smartphone: ständige Erreichbarkeit. Laptop: arbeiten von überall. Tablet: lesen im Bett. Smartwatch: schnelle Benachrichtigungen.'),
        'dialog': ('Mini-Dialog: Im Technikladen', 'Schreib einen kurzen Dialog mit einem Verkäufer in einem Technikladen.',
                   '— Suchen Sie etwas Bestimmtes? — Ja, ein neues Tablet. — Für was möchten Sie es nutzen? — Hauptsächlich zum Lesen und für Videos.'),
    }),

    '2055V': v('2055V', 'Medien', 'Medien', {
        'persoenlich': ('Wo du dich informierst', 'Wo holst du deine Nachrichten? Zwei Sätze.',
                        'Ich lese morgens kurz die ZEIT online. Abends höre ich manchmal noch einen Podcast über aktuelle Themen.'),
        'beobachtung': ('Vorteil und Nachteil sozialer Medien', 'Ein Vor- und ein Nachteil von sozialen Medien. Zwei Sätze.',
                        'Soziale Medien helfen mir, mit Freunden im Ausland Kontakt zu halten. Aber sie kosten auch zu viel Zeit am Tag.'),
        'frage': ('Eine Medien-Frage', 'Stell jemandem zwei Fragen über sein Medien-Verhalten.',
                  'Wie viele Stunden bist du täglich am Handy? Welcher Podcast ist im Moment dein Favorit?'),
        'liste': ('Drei Medien, drei Zwecke', 'Nenne drei Medien und sag, wofür du sie nutzt.',
                  'Bücher lese ich abends zur Entspannung. Podcasts höre ich beim Kochen. Soziale Medien nutze ich, um Freunde zu sehen.'),
        'dialog': ('Mini-Dialog: Über Nachrichten', 'Schreib einen kurzen Dialog zwischen zwei Personen über aktuelle Nachrichten.',
                   '— Hast du gehört, was gestern passiert ist? — Nein, ich habe heute noch nichts gelesen. — Schau mal kurz die Nachrichten an. — Mache ich gleich, danke.'),
    }),

    '2061V': v('2061V', 'Die Wanderlust', 'wandern', {
        'persoenlich': ('Deine letzte Wanderung', 'Wann warst du das letzte Mal wandern? Wo und wie lange? Zwei Sätze.',
                        'Letzten Sommer bin ich in den Alpen gewandert. Wir waren zwei Tage unterwegs und haben in einer Hütte übernachtet.'),
        'beobachtung': ('Warum Menschen wandern', 'Warum gehen Menschen wandern? Zwei Sätze.',
                        'Beim Wandern kann man den Kopf frei bekommen. Die Natur macht ruhig und glücklich.'),
        'frage': ('Eine Wander-Frage', 'Stell jemandem zwei Fragen über das Wandern.',
                  'Welcher ist dein Lieblings-Wanderweg? Warst du schon mal mehrere Tage am Stück unterwegs?'),
        'liste': ('Vier Sachen im Wanderrucksack', 'Was nimmst du immer mit, wenn du wandern gehst?',
                  'Eine Wasserflasche. Ein paar Müsliriegel. Eine Regenjacke. Mein Smartphone mit Wander-App.'),
        'dialog': ('Mini-Dialog: Wanderpläne', 'Schreib einen kurzen Dialog zwischen zwei Freunden über eine geplante Wanderung.',
                   '— Wollen wir am Sonntag wandern gehen? — Gerne, wohin denn? — Ich habe eine schöne Tour im Harz gefunden. — Wie lang ist sie? — Etwa 12 Kilometer, das schaffen wir gut.'),
    }),

    '2065V': v('2065V', 'Die Umwelt und die Tiere', 'Umwelt und Tiere', {
        'persoenlich': ('Was du für die Umwelt tust', 'Was machst du, um die Umwelt zu schützen? Zwei Sätze.',
                        'Ich fahre fast immer mit dem Fahrrad statt mit dem Auto. Außerdem kaufe ich Lebensmittel ohne Plastik, wenn es geht.'),
        'beobachtung': ('Ein Tier, das du magst', 'Welches Tier magst du besonders? Warum? Zwei Sätze.',
                        'Ich mag Elefanten, weil sie sehr klug und sozial sind. Es ist traurig, dass viele Elefanten in Gefahr sind.'),
        'frage': ('Eine Umwelt-Frage', 'Stell jemandem zwei Fragen zum Thema Umwelt.',
                  'Was war die letzte Sache, die du für die Umwelt verändert hast? Findest du Klimaschutz wichtiger als billige Preise?'),
        'liste': ('Vier Tipps für die Umwelt', 'Nenne vier kleine Tipps, mit denen jeder die Umwelt schützen kann.',
                  'Weniger Fleisch essen. Mit dem Rad statt mit dem Auto fahren. Wasser sparen beim Duschen. Kaputte Sachen reparieren statt neu kaufen.'),
        'dialog': ('Mini-Dialog: Über Umweltschutz', 'Schreib einen kurzen Dialog zwischen zwei Personen über Umweltschutz.',
                   '— Hast du gehört, dass es bald keine Plastiktüten mehr gibt? — Endlich! Ich habe sowieso immer eine Stofftasche dabei. — Ich auch. Aber gegen das Klimaproblem reicht das natürlich nicht. — Stimmt, aber jeder kleine Schritt zählt.'),
    }),

    # ============================================================
    # EINHEIT 2 — G-Dateien (12)
    # ============================================================

    '2013G': g('2013G', 'Indirekte Rede', 'die indirekte Rede (z.B. „Er sagte, dass er müde sei.")', {
        'erfahrung': ('Etwas, das jemand dir gesagt hat', 'Was hat dir heute jemand gesagt? Schreib es in der indirekten Rede.',
                      'Meine Mutter sagte, dass sie heute Abend anrufen würde. Mein Kollege meinte, er hätte schon zu Mittag gegessen.'),
        'beobachtung': ('Was im Radio oder TV kam', 'Berichte in indirekter Rede über eine Nachricht oder ein Wetter-Update.',
                        'Der Wetterbericht sagte, dass es morgen regnen werde. Außerdem hieß es, die Temperaturen würden fallen.'),
        'frage': ('Indirekte Frage', 'Stell zwei indirekte Fragen — „Ich möchte wissen, ob …" / „Kannst du mir sagen, wann …".',
                  'Kannst du mir sagen, wann der nächste Bus kommt? Ich möchte wissen, ob das Restaurant am Sonntag offen hat.'),
        'liste': ('Drei Aussagen, indirekt wiedergegeben', 'Wiederhole drei kurze Aussagen in indirekter Rede.',
                  'Maria sagte, dass sie krank sei. Tom meinte, er habe keine Zeit. Anna erklärte, sie wolle nach Hause gehen.'),
        'dialog': ('Mini-Dialog: Was hat er gesagt?', 'Schreib einen Dialog, in dem jemand erzählt, was eine dritte Person gesagt hat.',
                   '— Was hat dein Bruder gesagt? — Er sagte, dass er heute Abend kommt. — Und Maria? — Sie meinte, sie sei zu müde und bleibe zu Hause.'),
    }),

    '2017G': g('2017G', 'Das Passiv', 'das Passiv im Präsens und Präteritum', {
        'erfahrung': ('Was bei dir gemacht wurde', 'Schreib zwei Sätze über Dinge, die in deinem Leben gemacht werden oder wurden — z.B. im Haushalt. Im Passiv.',
                      'Bei uns wird montags die Wäsche gewaschen. Letzte Woche wurde die Küche neu gestrichen.'),
        'beobachtung': ('Was in deiner Stadt gebaut wird', 'Was wird in deiner Stadt gerade gebaut oder erneuert? Zwei Sätze im Passiv.',
                        'Im Zentrum wird gerade ein neues Einkaufszentrum gebaut. Letztes Jahr wurde unsere Schule renoviert.'),
        'frage': ('Eine Passiv-Frage', 'Stell zwei Fragen im Passiv.',
                  'Wann wird das neue Stadion eröffnet? Von wem wurde dieses Buch eigentlich übersetzt?'),
        'liste': ('Vier Tätigkeiten im Haushalt', 'Schreib vier Sätze im Passiv über Dinge, die im Haushalt gemacht werden.',
                  'Das Geschirr wird morgens abgewaschen. Der Müll wird mittwochs rausgebracht. Die Wäsche wird sonntags gemacht. Der Boden wird einmal pro Woche gewischt.'),
        'dialog': ('Mini-Dialog: Wer macht das?', 'Schreib einen Dialog mit Passiv-Konstruktionen.',
                   '— Wer hat die Küche so geputzt? — Sie wurde von meiner Schwester geputzt. — Und wann wird das Wohnzimmer gemacht? — Es wird morgen gemacht.'),
    }),

    '2023G': g('2023G', 'Position der Konnektoren', 'die Wortstellung mit Konnektoren („denn", „aber", „deshalb", „trotzdem")', {
        'erfahrung': ('Dein Tag mit Konnektoren', 'Erzähl zwei Sätze über deinen Tag mit Konnektoren wie „aber" oder „deshalb".',
                      'Ich wollte heute spazieren gehen, aber es hat geregnet. Deshalb habe ich zu Hause gelesen.'),
        'beobachtung': ('Pro und Contra', 'Schreib zwei Sätze zu einem Thema deiner Wahl mit „aber" oder „trotzdem".',
                        'Ich liebe Schokolade. Trotzdem versuche ich, nicht zu viel davon zu essen.'),
        'frage': ('Frage mit „warum" + Antwort mit „denn"', 'Schreib eine „Warum"-Frage und eine Antwort mit „denn".',
                  'Warum lernst du Deutsch so intensiv? — Ich lerne so viel, denn ich möchte bald in Berlin arbeiten.'),
        'liste': ('Vier Sätze, vier Konnektoren', 'Schreib vier Sätze mit „aber", „deshalb", „trotzdem", „denn".',
                  'Es ist spät, aber ich bin noch wach. Mir ist kalt, deshalb ziehe ich einen Pullover an. Der Film war lang, trotzdem hat er mir gefallen. Ich kaufe oft im Bio-Laden, denn die Qualität ist besser.'),
        'dialog': ('Mini-Dialog: Konnektoren', 'Schreib einen Dialog mit mindestens zwei Konnektoren.',
                   '— Warum kommst du heute spät? — Mein Zug hatte Verspätung, deshalb bin ich erst jetzt da. — Aber zum Glück bist du noch gekommen. — Ja, denn ich wollte dich unbedingt sehen.'),
    }),

    '2027G': g('2027G', 'Lokal- und Direktionaladverbien', 'Lokal- und Direktionaladverbien („oben", „unten", „nach oben", „nach unten")', {
        'erfahrung': ('Wo du wohnst', 'Beschreib in zwei Sätzen, wo in deinem Haus du wohnst — mit Lokaladverbien.',
                      'Ich wohne oben im dritten Stock. Unten im Erdgeschoss gibt es einen kleinen Briefkasten für mich.'),
        'beobachtung': ('Bewegung im Alltag', 'Beschreib zwei Bewegungen aus deinem Tag mit „nach oben", „nach unten", „nach rechts" usw.',
                        'Morgens gehe ich die Treppe nach unten zur Bäckerei. Dann fahre ich mit dem Bus nach rechts in die Stadtmitte.'),
        'frage': ('Eine Richtungsfrage', 'Stell zwei Fragen mit Richtungsadverbien.',
                  'Wohin geht es weiter — nach links oder nach rechts? Soll ich nach oben gehen oder hier unten warten?'),
        'liste': ('Vier Orte, vier Adverbien', 'Verbinde vier Orte mit vier Adverbien (oben/unten/innen/draußen).',
                  'Die Wäsche hänge ich draußen auf. Die Schuhe stelle ich drinnen ins Regal. Das Auto parke ich unten in der Garage. Die Wäscheleine ist oben im Garten.'),
        'dialog': ('Mini-Dialog: Wegbeschreibung', 'Schreib einen Dialog mit Richtungsadverbien — jemand fragt nach dem Weg.',
                   '— Entschuldigung, wo finde ich Herrn Müller? — Im zweiten Stock, gehen Sie nach oben. — Und dann? — Dann nach rechts, dritte Tür links.'),
    }),

    '2033G': g('2033G', 'Das Präteritum', 'das Präteritum (gestern fuhr, war, ging, sah)', {
        'erfahrung': ('Ein Tag in deiner Jugend', 'Erzähl in drei Sätzen einen Tag aus deiner Jugend — alles im Präteritum.',
                      'Mit 14 fuhr ich jeden Tag mit dem Bus zur Schule. Ich saß immer hinten und las dabei. Manchmal verschlief ich und musste rennen.'),
        'beobachtung': ('Ein wichtiger Tag aus deiner Vergangenheit', 'Schreib zwei Sätze über einen wichtigen Tag — im Präteritum.',
                        'Mein erster Arbeitstag war im September 2018. Ich kam zu früh und wartete eine halbe Stunde vor der Tür.'),
        'frage': ('Präteritum-Frage', 'Stell zwei Fragen im Präteritum.',
                  'Wo warst du an deinem 18. Geburtstag? Wie lange wohntest du in deiner ersten eigenen Wohnung?'),
        'liste': ('Drei Sätze über gestern', 'Erzähl drei Sätze über gestern im Präteritum.',
                  'Gestern stand ich um 7 Uhr auf. Ich frühstückte schnell und las dabei die Zeitung. Am Abend traf ich meine beste Freundin im Café.'),
        'dialog': ('Mini-Dialog: Erinnerungen', 'Schreib einen Dialog im Präteritum — zwei Personen sprechen über eine gemeinsame Erinnerung.',
                   '— Erinnerst du dich, als wir nach Italien fuhren? — Natürlich! Es regnete fast jeden Tag. — Aber wir lachten trotzdem viel. — Stimmt, und am Strand spielten wir Karten.'),
    }),

    '2037G': g('2037G', 'Modalpartikeln', 'Modalpartikeln wie „ja", „doch", „mal", „eigentlich", „denn"', {
        'erfahrung': ('Mit Modalpartikeln nachfragen', 'Schreib zwei Fragen mit „eigentlich" oder „denn".',
                      'Wie heißt du eigentlich? Wo wohnst du denn?'),
        'beobachtung': ('Eine kleine Aufforderung', 'Bitte jemanden um etwas mit „mal" oder „doch".',
                        'Komm doch mal her! Probier das mal — das schmeckt super.'),
        'frage': ('Höfliche Frage mit Modalpartikeln', 'Stell zwei höfliche Fragen mit „eigentlich", „denn" oder „mal".',
                  'Was machst du eigentlich beruflich? Hast du mal eine Sekunde Zeit?'),
        'liste': ('Vier Sätze, vier Partikeln', 'Schreib vier Sätze, jeder mit einer anderen Modalpartikel („ja", „doch", „mal", „eigentlich").',
                  'Das ist ja interessant! Komm doch zu uns rüber. Sag mal, wie spät ist es? Wie heißt du eigentlich?'),
        'dialog': ('Mini-Dialog: Lebendige Sprache', 'Schreib einen kurzen Alltagsdialog mit mehreren Modalpartikeln.',
                   '— Sag mal, wo ist denn meine Brille? — Die liegt doch auf dem Tisch! — Ach ja, jetzt sehe ich sie. — Du suchst sie eigentlich jeden Tag.'),
    }),

    '2043G': g('2043G', 'Konjunktiv II', 'den Konjunktiv II („ich hätte", „ich wäre", „ich würde …")', {
        'erfahrung': ('Was du anders machen würdest', 'Was würdest du in deinem Leben anders machen, wenn du könntest? Zwei Sätze im Konjunktiv II.',
                      'Wenn ich noch einmal jung wäre, würde ich mehr reisen. Ich hätte auch lieber eine andere Sprache als Schulsprache gewählt.'),
        'beobachtung': ('Ein höflicher Wunsch', 'Formuliere zwei höfliche Wünsche im Konjunktiv II.',
                        'Ich hätte gern noch einen Kaffee, bitte. Könnten Sie mir kurz helfen?'),
        'frage': ('Frage im Konjunktiv II', 'Stell zwei Fragen im Konjunktiv II.',
                  'Was würdest du machen, wenn du eine Million Euro hättest? Wärst du gern ein Tier — und wenn ja, welches?'),
        'liste': ('Drei „Wenn ich nur …"-Sätze', 'Schreib drei Sätze, die mit „Wenn ich nur …" beginnen.',
                  'Wenn ich nur mehr Zeit hätte! Wenn ich nur besser Klavier spielen könnte! Wenn ich nur mutiger wäre!'),
        'dialog': ('Mini-Dialog: Höfliche Bitte', 'Schreib einen kurzen Restaurant-Dialog im Konjunktiv II.',
                   '— Könnte ich bitte die Speisekarte haben? — Selbstverständlich. — Hätten Sie auch etwas Vegetarisches? — Wir hätten heute eine Pilzpfanne.'),
    }),

    '2047G': g('2047G', 'Kasus: Wiederholung', 'die vier Fälle (Nominativ, Akkusativ, Dativ, Genitiv) zusammen', {
        'erfahrung': ('Vier Sätze, vier Fälle', 'Schreib vier Sätze über deinen Tag — pro Satz ein anderer Fall (Nom., Akk., Dat., Gen.).',
                      'Der Hund schläft. Ich streichle den Hund. Ich gebe dem Hund Wasser. Das ist das Spielzeug des Hundes.'),
        'beobachtung': ('Ein Geschenk', 'Beschreib in zwei Sätzen ein Geschenk — wer gibt wem was?',
                        'Mein Bruder schenkt seiner Frau einen Ring. Sie freut sich sehr über das schöne Geschenk.'),
        'frage': ('Eine Frage mit allen vier Fällen', 'Stell zwei Fragen mit verschiedenen Fällen („Wem gehört …?", „Wessen Buch ist das?").',
                  'Wessen Tasche steht im Flur? Wem hast du gestern den Brief gegeben?'),
        'liste': ('Drei Verben, drei Sätze', 'Schreib drei Sätze mit drei verschiedenen Verben — jedes verlangt einen anderen Kasus.',
                  'Ich sehe meinen Freund. Ich helfe meinem Freund. Ich erinnere mich an meinen Freund.'),
        'dialog': ('Mini-Dialog: Alle Fälle', 'Schreib einen Dialog, in dem alle vier Fälle vorkommen.',
                   '— Wem gehört das Buch? — Es ist das Buch meiner Schwester. — Hast du es gelesen? — Ja, ich habe ihr gesagt, dass es mir gut gefallen hat.'),
    }),

    '2053G': g('2053G', 'Indefinitpronomen', 'Indefinitpronomen wie „etwas", „nichts", „jemand", „niemand", „alle", „einige"', {
        'erfahrung': ('Was niemand weiß', 'Schreib zwei Sätze mit „jemand", „niemand", „etwas" oder „nichts" über deinen Tag.',
                      'Heute habe ich niemanden in meiner Familie angerufen. Ich habe etwas Neues gelernt — fünf neue Vokabeln.'),
        'beobachtung': ('Alle, einige, niemand', 'Schreib zwei Sätze über deine Freunde oder Kollegen — mit „alle", „einige", „niemand".',
                        'Alle in meinem Team sprechen Englisch. Einige Kollegen sprechen auch Französisch. Niemand spricht Russisch.'),
        'frage': ('Frage mit Indefinitpronomen', 'Stell zwei Fragen mit Indefinitpronomen.',
                  'Hat jemand schon das neue Café an der Ecke ausprobiert? Habt ihr etwas Schönes am Wochenende vor?'),
        'liste': ('Vier Sätze, vier Pronomen', 'Schreib vier Sätze mit je einem anderen Indefinitpronomen.',
                  'Jemand hat die Tür offen gelassen. Niemand weiß, wer es war. Etwas in mir glaubt an dich. Nichts ist unmöglich.'),
        'dialog': ('Mini-Dialog: Wer war das?', 'Schreib einen Dialog mit mehreren Indefinitpronomen.',
                   '— Hat jemand mein Buch gesehen? — Nein, niemand. — Aber irgendjemand muss es weggenommen haben. — Hast du etwas im Auto vergessen?'),
    }),

    '2057G': g('2057G', 'Genitiv', 'den Genitiv (des Mannes, der Frau, der Kinder)', {
        'erfahrung': ('Eine Sache aus deiner Familie', 'Beschreib eine Sache mit Genitiv — z.B. „das Auto meines Bruders".',
                      'Das Haus meiner Eltern ist nicht groß, aber sehr gemütlich. Im Wohnzimmer steht das alte Klavier meiner Großmutter.'),
        'beobachtung': ('Drei Genitiv-Sätze', 'Schreib drei kurze Sätze mit Genitiv.',
                        'Der Hund des Nachbarn bellt oft. Die Mutter meiner Freundin kommt aus Polen. Das Auto unserer Firma ist alt.'),
        'frage': ('Frage mit „Wessen?"', 'Stell zwei Fragen mit „Wessen?".',
                  'Wessen Buch liegt da auf dem Stuhl? Wessen Idee war das eigentlich?'),
        'liste': ('Vier feste Wendungen mit Genitiv', 'Schreib vier Sätze mit Wendungen wie „während der Woche", „statt des Kaffees", „trotz des Regens".',
                  'Während der Woche arbeite ich. Statt des Kaffees nehme ich heute Tee. Trotz des Regens gehen wir spazieren. Wegen der Hitze blieb ich zu Hause.'),
        'dialog': ('Mini-Dialog: Mit Genitiv', 'Schreib einen Dialog mit Genitiv-Konstruktionen.',
                   '— Wessen Mantel liegt auf dem Stuhl? — Es ist der Mantel meines Bruders. — Und die Tasche? — Die gehört der Freundin meiner Mutter.'),
    }),

    '2063G': g('2063G', 'Verben mit fester Präposition', 'Verben mit fester Präposition („sich freuen auf", „warten auf", „denken an", „sprechen über")', {
        'erfahrung': ('Worauf du wartest', 'Worauf wartest du gerade? Schreib zwei Sätze mit Verben + Präposition.',
                      'Ich warte seit drei Wochen auf eine Antwort von der Bank. Außerdem freue ich mich auf das nächste lange Wochenende.'),
        'beobachtung': ('An wen du heute gedacht hast', 'An wen oder was hast du heute gedacht? Zwei Sätze mit „denken an".',
                        'Heute Morgen habe ich an meinen alten Lehrer gedacht. Er hat mich an die Liebe zu Büchern erinnert.'),
        'frage': ('Frage mit Verb + Präposition', 'Stell zwei Fragen mit Verben + fester Präposition.',
                  'Über welches Thema möchtest du gern reden? Auf was freust du dich diese Woche am meisten?'),
        'liste': ('Vier Verben, vier Sätze', 'Schreib vier Sätze mit je einem anderen Verb + Präposition.',
                  'Ich freue mich auf den Urlaub. Ich warte auf den Bus. Ich denke oft an meine Großeltern. Wir sprechen heute über deutsche Filme.'),
        'dialog': ('Mini-Dialog: Mit Verb + Präposition', 'Schreib einen kurzen Dialog mit drei verschiedenen Verb-Präposition-Verbindungen.',
                   '— Warum freust du dich so? — Ich freue mich auf das Konzert heute Abend. — Über welche Band sprichst du? — Über die neue Band aus Berlin. Hast du schon von ihr gehört?'),
    }),

    '2067G': g('2067G', 'Mehr über Adjektivendungen', 'Adjektivendungen ohne Artikel (z.B. „bei schönem Wetter", „mit frischem Brot")', {
        'erfahrung': ('Wetter und Aktivitäten', 'Schreib zwei Sätze mit „bei schönem Wetter", „bei kaltem Wetter" oder ähnlich.',
                      'Bei schönem Wetter gehe ich gern wandern. Bei starkem Regen bleibe ich lieber zu Hause mit einem Buch.'),
        'beobachtung': ('Was du isst und trinkst', 'Beschreib in zwei Sätzen, was du oft isst — mit Adjektiven ohne Artikel.',
                        'Zum Frühstück nehme ich gern frisches Brot mit kaltem Käse. Dazu trinke ich starken schwarzen Kaffee.'),
        'frage': ('Frage mit endungslosem Artikel', 'Stell zwei Fragen mit Adjektiven ohne Artikel.',
                  'Trinkst du lieber heißen Tee oder kaltes Wasser? Magst du Spaziergänge bei kaltem Wetter?'),
        'liste': ('Vier kleine Genussbeschreibungen', 'Schreib vier Sätze, in denen du etwas Schönes beschreibst — mit Adjektiven ohne Artikel.',
                  'Mit frischen Erdbeeren schmeckt der Joghurt am besten. Bei warmem Wind ist der Spaziergang schön. Mit guter Musik vergeht der Abend schnell. Auf weichem Sand laufe ich barfuß.'),
        'dialog': ('Mini-Dialog: Über Lieblingsdinge', 'Schreib einen kurzen Dialog mit Adjektiven ohne Artikel.',
                   '— Hast du Lust auf einen Spaziergang? — Bei diesem starkem Wind? Lieber nicht. — Dann machen wir uns warmen Tee. — Mit frischer Minze? Das wäre super.'),
    }),

}
