#!/usr/bin/env python3
"""Schreibwerkstatt-Aufgaben für die 35 fehlenden A1-Lektionen (thematische
Hauptlektionen ohne -uebungen.html-Duplikate).

A1-Skalierung: 1-15 Wörter pro Aufgabe, SCHREIB_MIN_CHARS=5.
Aufgabencharakter: stark geführt, Beispiel-orientiert.

Wird vom Patcher add-schreibwerkstatt-v2.py automatisch geladen, wenn er mit
--niveau A1 läuft.
"""
from __future__ import annotations

BANNER_URL = 'https://images.pexels.com/photos/733856/pexels-photo-733856.jpeg?auto=compress&cs=tinysrgb&w=800'
BANNER_ALT = 'Notizbuch und Stift, bereit zum Schreiben'


def v(code, title, theme, samples):
    tasks = []
    for key in ('persoenlich', 'beobachtung', 'frage', 'liste', 'dialog'):
        t, f, b = samples[key]
        tasks.append({'titel': t, 'frage': f, 'beispiel': b})
    return {
        'lesson_code': code,
        'lesson_title': title,
        'banner_url': BANNER_URL, 'banner_alt': BANNER_ALT,
        'intro': f'Fünf kleine Schreibaufgaben rund um „{theme}". Schreib so viel oder wenig du möchtest — je eine bis 15 Wörter reichen.',
        'tasks': tasks,
    }


def g(code, title, struct, samples):
    tasks = []
    for key in ('a', 'b', 'c', 'd', 'e'):
        t, f, b = samples[key]
        tasks.append({'titel': t, 'frage': f, 'beispiel': b})
    return {
        'lesson_code': code,
        'lesson_title': title,
        'banner_url': BANNER_URL, 'banner_alt': BANNER_ALT,
        'intro': f'Fünf kleine Schreibaufgaben, bei denen du {struct} übst. Eine bis 15 Wörter pro Aufgabe.',
        'tasks': tasks,
    }


CONFIGS = {

    # ============================================================
    # V-Dateien (Vokabular)
    # ============================================================

    '1011V': v('1011V', 'Hallo!', 'Begrüßung', {
        'persoenlich': ('Dein Name', 'Wie heißt du? Schreib einen Satz.',
                        'Ich heiße Maria.'),
        'beobachtung': ('Drei Begrüßungen', 'Schreib drei deutsche Begrüßungen auf.',
                        'Hallo. Guten Tag. Auf Wiedersehen.'),
        'frage': ('Eine Frage zum Kennenlernen', 'Stell jemandem eine kurze Frage.',
                  'Wie heißt du?'),
        'liste': ('Drei Wörter zur Begrüßung', 'Nenn drei Wörter aus der Lektion.',
                  'Hallo, tschüss, guten Morgen.'),
        'dialog': ('Mini-Dialog', 'Schreib einen kurzen Dialog zum Kennenlernen.',
                   '— Hallo, ich bin Maria. — Hi, ich bin Tom.'),
    }),

    '1021V': v('1021V', 'Wie geht es dir?', 'Befinden', {
        'persoenlich': ('Wie geht es dir heute?', 'Schreib einen Satz über dein Befinden.',
                        'Mir geht es gut.'),
        'beobachtung': ('Drei Adjektive zum Befinden', 'Nenne drei Wörter wie gut, müde, traurig.',
                        'Gut, müde, traurig.'),
        'frage': ('Eine Frage', 'Frag jemanden nach seinem Befinden.',
                  'Wie geht es dir?'),
        'liste': ('Drei Antworten', 'Schreib drei Antworten auf „Wie geht es dir?".',
                  'Gut. Sehr gut. Nicht so gut.'),
        'dialog': ('Mini-Dialog', 'Schreib zwei Sätze: eine Frage und eine Antwort.',
                   '— Wie geht es dir? — Danke, gut.'),
    }),

    '103V': v('103V', 'Zahlen', 'Zahlen', {
        'persoenlich': ('Dein Alter', 'Wie alt bist du? Schreib einen Satz.',
                        'Ich bin 30 Jahre alt.'),
        'beobachtung': ('Zahlen 1–5', 'Schreib die Zahlen 1 bis 5 als Wörter.',
                        'Eins, zwei, drei, vier, fünf.'),
        'frage': ('Eine Zahl-Frage', 'Frag jemanden nach einer Zahl.',
                  'Wie alt bist du?'),
        'liste': ('Zahlen 10, 20, 30, 100', 'Schreib diese Zahlen als Wörter.',
                  'Zehn, zwanzig, dreißig, hundert.'),
        'dialog': ('Mini-Dialog', 'Zwei Sätze: Frage und Antwort mit Zahlen.',
                   '— Wie alt bist du? — Ich bin 28.'),
    }),

    '1041V': v('1041V', 'Im Café', 'das Café', {
        'persoenlich': ('Dein Lieblingsgetränk', 'Was trinkst du gern? Ein Satz.',
                        'Ich trinke gern Kaffee.'),
        'beobachtung': ('Drei Getränke', 'Nenne drei Getränke auf Deutsch.',
                        'Kaffee, Tee, Wasser.'),
        'frage': ('Eine Bestellung', 'Wie bestellst du einen Kaffee? Ein Satz.',
                  'Einen Kaffee, bitte.'),
        'liste': ('Vier Dinge im Café', 'Nenne vier Dinge im Café.',
                  'Kaffee, Kuchen, Stuhl, Tisch.'),
        'dialog': ('Mini-Dialog', 'Schreib einen kurzen Dialog im Café.',
                   '— Was möchten Sie? — Einen Tee, bitte.'),
    }),

    '1051V': v('1051V', 'Mein Beruf', 'Berufe', {
        'persoenlich': ('Dein Beruf', 'Was machst du beruflich? Ein Satz.',
                        'Ich bin Lehrerin.'),
        'beobachtung': ('Drei Berufe', 'Nenne drei Berufe auf Deutsch.',
                        'Arzt, Lehrer, Verkäufer.'),
        'frage': ('Eine Berufs-Frage', 'Frag jemanden nach seinem Beruf.',
                  'Was machst du beruflich?'),
        'liste': ('Drei Berufe in deiner Familie', 'Welche Berufe haben Familienmitglieder?',
                  'Meine Mutter ist Ärztin. Mein Bruder ist Student.'),
        'dialog': ('Mini-Dialog', 'Zwei Fragen und Antworten zum Beruf.',
                   '— Was machst du? — Ich bin Lehrer. Und du? — Ich studiere.'),
    }),

    '1061V': v('1061V', 'Die Zeit', 'die Uhrzeit', {
        'persoenlich': ('Wann stehst du auf?', 'Schreib einen Satz mit Uhrzeit.',
                        'Ich stehe um sieben Uhr auf.'),
        'beobachtung': ('Drei Uhrzeiten', 'Schreib drei Uhrzeiten als Wörter.',
                        'Acht Uhr, halb neun, Viertel vor zehn.'),
        'frage': ('Eine Zeit-Frage', 'Frag nach der Uhrzeit.',
                  'Wie spät ist es?'),
        'liste': ('Dein Tag in vier Zeiten', 'Vier Aktivitäten mit Uhrzeit.',
                  '7 Uhr: aufstehen. 8 Uhr: frühstücken. 18 Uhr: kochen. 23 Uhr: schlafen.'),
        'dialog': ('Mini-Dialog', 'Zwei Sätze zur Verabredung mit Zeit.',
                   '— Wann treffen wir uns? — Um sieben Uhr abends.'),
    }),

    '1071V': v('1071V', 'Die Wochentage', 'Wochentage', {
        'persoenlich': ('Dein Lieblingstag', 'Welcher Wochentag ist dein Lieblingstag?',
                        'Mein Lieblingstag ist Samstag.'),
        'beobachtung': ('Alle sieben Wochentage', 'Nenne alle sieben Tage in Reihenfolge.',
                        'Montag, Dienstag, Mittwoch, Donnerstag, Freitag, Samstag, Sonntag.'),
        'frage': ('Eine Wochentag-Frage', 'Frag jemanden nach seinem Plan an einem Tag.',
                  'Was machst du am Samstag?'),
        'liste': ('Drei Aktivitäten pro Woche', 'Was machst du an drei Wochentagen?',
                  'Am Montag arbeite ich. Am Mittwoch koche ich. Am Sonntag schlafe ich.'),
        'dialog': ('Mini-Dialog', 'Verabredung an einem bestimmten Tag.',
                   '— Hast du Zeit am Freitag? — Ja, gern!'),
    }),

    '1081V': v('1081V', 'Trennbare Verben', 'trennbare Verben', {
        'persoenlich': ('Wann stehst du auf?', 'Schreib einen Satz mit „aufstehen".',
                        'Ich stehe um sieben Uhr auf.'),
        'beobachtung': ('Drei trennbare Verben', 'Nenne drei trennbare Verben.',
                        'aufstehen, einkaufen, anrufen.'),
        'frage': ('Eine Frage mit trennbarem Verb', 'Stell eine Frage.',
                  'Wann kaufst du ein?'),
        'liste': ('Dein Tag mit trennbaren Verben', 'Drei Sätze mit trennbaren Verben.',
                  'Ich stehe um sechs auf. Ich kaufe um neun ein. Ich rufe Mama an.'),
        'dialog': ('Mini-Dialog', 'Zwei Sätze mit trennbaren Verben.',
                   '— Wann rufst du mich an? — Heute Abend.'),
    }),

    '1091V': v('1091V', 'Hobbys', 'Hobbys', {
        'persoenlich': ('Dein Hobby', 'Was machst du gern in deiner Freizeit?',
                        'Ich lese gern.'),
        'beobachtung': ('Drei Hobbys', 'Nenne drei Hobbys auf Deutsch.',
                        'Lesen, kochen, schwimmen.'),
        'frage': ('Eine Hobby-Frage', 'Frag jemanden nach seinem Hobby.',
                  'Was ist dein Hobby?'),
        'liste': ('Drei Aktivitäten am Wochenende', 'Was machst du am Wochenende?',
                  'Ich gehe spazieren. Ich koche. Ich lese.'),
        'dialog': ('Mini-Dialog', 'Zwei Fragen und Antworten zu Hobbys.',
                   '— Was machst du gern? — Ich tanze gern. Und du? — Ich male.'),
    }),

    '1101V': v('1101V', 'Essen und Trinken', 'Essen', {
        'persoenlich': ('Dein Lieblingsessen', 'Was isst du am liebsten?',
                        'Ich esse gern Pizza.'),
        'beobachtung': ('Drei Lebensmittel', 'Nenne drei Lebensmittel.',
                        'Brot, Käse, Apfel.'),
        'frage': ('Eine Essen-Frage', 'Frag jemanden, was er gern isst.',
                  'Was isst du gern?'),
        'liste': ('Frühstück, Mittag, Abend', 'Was isst du wann?',
                  'Frühstück: Brot. Mittag: Suppe. Abend: Salat.'),
        'dialog': ('Mini-Dialog', 'Beim Essen — zwei Sätze.',
                   '— Magst du Käse? — Ja, sehr gern.'),
    }),

    '1111V': v('1111V', 'Verkehrsmittel', 'Verkehrsmittel', {
        'persoenlich': ('Wie kommst du zur Arbeit?', 'Schreib einen Satz.',
                        'Ich fahre mit dem Bus.'),
        'beobachtung': ('Drei Verkehrsmittel', 'Nenne drei Verkehrsmittel.',
                        'Auto, Bus, Fahrrad.'),
        'frage': ('Eine Frage', 'Frag jemanden, wie er fährt.',
                  'Wie kommst du zur Arbeit?'),
        'liste': ('Drei Reisen', 'Wie reist du? Drei Sätze.',
                  'Nach Berlin mit dem Zug. Nach Madrid mit dem Flugzeug. Zur Schule zu Fuß.'),
        'dialog': ('Mini-Dialog', 'Zwei Sätze zum Reisen.',
                   '— Wie fährst du? — Mit der U-Bahn.'),
    }),

    '1121V': v('1121V', 'Beim Bürgeramt', 'das Bürgeramt', {
        'persoenlich': ('Warst du beim Amt?', 'Schreib einen kurzen Satz.',
                        'Ja, ich war letzte Woche beim Amt.'),
        'beobachtung': ('Drei Wörter zum Amt', 'Nenne drei wichtige Wörter.',
                        'Formular, Termin, Anmeldung.'),
        'frage': ('Eine Frage beim Amt', 'Wie fragst du nach einem Termin?',
                  'Ich brauche einen Termin, bitte.'),
        'liste': ('Drei Dokumente', 'Welche Dokumente brauchst du?',
                  'Pass, Anmeldeformular, Foto.'),
        'dialog': ('Mini-Dialog', 'Zwei Sätze beim Amt.',
                   '— Guten Tag, ich möchte mich anmelden. — Haben Sie einen Termin?'),
    }),

    '2011V': v('2011V', 'Wohnung und Möbel', 'die Wohnung', {
        'persoenlich': ('Deine Wohnung', 'Wo wohnst du? Ein Satz.',
                        'Ich wohne in einer kleinen Wohnung.'),
        'beobachtung': ('Drei Möbel', 'Nenne drei Möbel auf Deutsch.',
                        'Tisch, Stuhl, Bett.'),
        'frage': ('Eine Frage zur Wohnung', 'Frag jemanden nach seiner Wohnung.',
                  'Wie groß ist deine Wohnung?'),
        'liste': ('Vier Räume', 'Nenne vier Räume in einer Wohnung.',
                  'Küche, Bad, Wohnzimmer, Schlafzimmer.'),
        'dialog': ('Mini-Dialog', 'Zwei Sätze zur Wohnung.',
                   '— Wo wohnst du? — In Berlin, im zweiten Stock.'),
    }),

    '2021V': v('2021V', 'Meine Stadt', 'die Stadt', {
        'persoenlich': ('Deine Stadt', 'In welcher Stadt wohnst du?',
                        'Ich wohne in München.'),
        'beobachtung': ('Drei Orte in der Stadt', 'Nenne drei wichtige Orte.',
                        'Park, Bahnhof, Café.'),
        'frage': ('Eine Stadt-Frage', 'Frag nach dem Weg.',
                  'Wo ist der Bahnhof?'),
        'liste': ('Vier Plätze', 'Welche Orte gibt es in deiner Stadt?',
                  'Eine Schule, ein Park, ein Markt, eine Kirche.'),
        'dialog': ('Mini-Dialog', 'Touristen-Frage.',
                   '— Entschuldigung, wo ist das Museum? — Geradeaus, dann links.'),
    }),

    '2031V': v('2031V', 'Geschäfte und Besorgungen', 'die Geschäfte', {
        'persoenlich': ('Wo kaufst du ein?', 'Wo gehst du normalerweise einkaufen?',
                        'Ich kaufe im Supermarkt ein.'),
        'beobachtung': ('Drei Geschäfte', 'Nenne drei Geschäfte.',
                        'Supermarkt, Bäckerei, Apotheke.'),
        'frage': ('Eine Geschäft-Frage', 'Frag, wo es ein Geschäft gibt.',
                  'Wo ist eine Apotheke?'),
        'liste': ('Vier Sachen einkaufen', 'Was kaufst du? Vier Wörter.',
                  'Brot, Milch, Obst, Käse.'),
        'dialog': ('Mini-Dialog', 'Im Laden.',
                   '— Was kostet das? — Drei Euro fünfzig, bitte.'),
    }),

    '2041V': v('2041V', 'Kleidung und Farben', 'Kleidung', {
        'persoenlich': ('Was trägst du heute?', 'Schreib einen Satz.',
                        'Ich trage eine blaue Hose.'),
        'beobachtung': ('Drei Kleidungsstücke', 'Nenne drei Kleidungsstücke.',
                        'Hose, Hemd, Schuhe.'),
        'frage': ('Eine Kleidungs-Frage', 'Frag nach einem Kleidungsstück.',
                  'Wo finde ich eine Jacke?'),
        'liste': ('Vier Farben', 'Nenne vier Farben.',
                  'Rot, blau, grün, gelb.'),
        'dialog': ('Mini-Dialog', 'Beim Einkaufen.',
                   '— Wie gefällt dir die Jacke? — Schön, aber zu teuer.'),
    }),

    '2051V': v('2051V', 'Im Restaurant', 'das Restaurant', {
        'persoenlich': ('Dein Lieblingsessen', 'Was bestellst du am liebsten?',
                        'Ich esse gern Pasta.'),
        'beobachtung': ('Drei Gerichte', 'Nenne drei deutsche Gerichte.',
                        'Schnitzel, Bratwurst, Sauerkraut.'),
        'frage': ('Eine Restaurant-Frage', 'Wie bestellst du?',
                  'Ich hätte gern eine Pizza, bitte.'),
        'liste': ('Drei Sachen auf der Speisekarte', 'Was steht auf der Karte?',
                  'Suppe, Salat, Schnitzel.'),
        'dialog': ('Mini-Dialog', 'Beim Kellner.',
                   '— Was möchten Sie trinken? — Ein Wasser, bitte.'),
    }),

    # ============================================================
    # G-Dateien (Grammatik) — Aufgaben erzwingen die Zielstruktur
    # ============================================================

    '1000G': g('1000G', 'Das deutsche Genus', 'der, die, das (Artikel)', {
        'a': ('Drei Nomen mit Artikel', 'Schreib drei Nomen mit Artikel.',
              'der Tisch, die Lampe, das Buch.'),
        'b': ('Möbel mit Artikel', 'Drei Möbel mit Artikel.',
              'der Stuhl, die Couch, das Bett.'),
        'c': ('Essen mit Artikel', 'Drei Lebensmittel mit Artikel.',
              'der Apfel, die Banane, das Brot.'),
        'd': ('Familienmitglieder mit Artikel', 'Drei Personen mit Artikel.',
              'der Vater, die Mutter, das Kind.'),
        'e': ('Mini-Satz', 'Ein Satz mit „der", „die" oder „das".',
              'Das Buch ist neu.'),
    }),

    '1017G': g('1017G', 'sein und haben', 'die Verben „sein" und „haben"', {
        'a': ('Du mit „sein"', 'Ein Satz: ich bin … (Beruf, Alter, Nationalität)',
              'Ich bin Lehrer.'),
        'b': ('Familie mit „haben"', 'Ein Satz: ich habe …',
              'Ich habe einen Bruder.'),
        'c': ('Drei „sein"-Sätze', 'Du, dein Freund und deine Familie mit „sein".',
              'Ich bin müde. Tom ist nett. Wir sind aus Spanien.'),
        'd': ('Drei „haben"-Sätze', 'Was hast du, was hat jemand anderes?',
              'Ich habe ein Auto. Anna hat einen Hund. Wir haben Zeit.'),
        'e': ('Mini-Dialog', 'Eine Frage mit „sein", Antwort mit „haben".',
              '— Bist du müde? — Ja, ich habe wenig geschlafen.'),
    }),

    '1023G': g('1023G', 'Verben und Personalpronomen', 'Verbkonjugation im Präsens', {
        'a': ('Ich-Form', 'Schreib einen Satz mit „ich" + Verb.',
              'Ich wohne in Berlin.'),
        'b': ('Du-Form', 'Stell eine Frage mit „du" + Verb.',
              'Wohnst du in Berlin?'),
        'c': ('Wir-Form', 'Ein Satz mit „wir" + Verb.',
              'Wir lernen Deutsch.'),
        'd': ('Drei Personalpronomen', 'Drei Sätze mit ich, du, sie.',
              'Ich komme aus Spanien. Du kommst aus Italien. Sie kommt aus Polen.'),
        'e': ('Mini-Dialog', 'Frage mit „du", Antwort mit „ich".',
              '— Lernst du Deutsch? — Ja, ich lerne Deutsch.'),
    }),

    '1033G': g('1033G', 'sein und haben (Wiederholung)', '„sein" und „haben"', {
        'a': ('Deine Familie mit „haben"', 'Schreib drei Sätze: ich habe …',
              'Ich habe einen Bruder, eine Schwester und einen Hund.'),
        'b': ('Sein-Sätze', 'Ein Satz mit „bin", einer mit „ist".',
              'Ich bin Lehrer. Mein Bruder ist Student.'),
        'c': ('Eine Frage mit „haben"', 'Stell eine Frage.',
              'Hast du ein Auto?'),
        'd': ('Eine Frage mit „sein"', 'Stell eine Frage.',
              'Bist du müde?'),
        'e': ('Mini-Dialog', 'Frage und Antwort mit „sein" und „haben".',
              '— Hast du Geschwister? — Ja, ich habe eine Schwester. — Sie ist 20.'),
    }),

    '1043G': g('1043G', 'Alles über Fragen', 'W-Fragen und Ja/Nein-Fragen', {
        'a': ('Drei W-Fragen', 'Schreib drei Fragen mit Wo, Was, Wie.',
              'Wo wohnst du? Was machst du? Wie heißt du?'),
        'b': ('Ja/Nein-Frage', 'Eine Frage ohne Fragewort.',
              'Lernst du Deutsch?'),
        'c': ('Fragen zum Beruf', 'Zwei Fragen zum Beruf.',
              'Was machst du beruflich? Wo arbeitest du?'),
        'd': ('Fragen zum Wohnort', 'Zwei Fragen zur Stadt.',
              'In welcher Stadt wohnst du? Gefällt dir deine Stadt?'),
        'e': ('Mini-Interview', 'Drei Fragen für ein Interview.',
              'Wie heißt du? Wie alt bist du? Woher kommst du?'),
    }),

    '1053G': g('1053G', 'Verben mit Vokalwechsel', 'Verben mit Vokalwechsel (du fährst, er liest)', {
        'a': ('Ein Satz mit „fahren"', 'Schreib einen Satz: er fährt …',
              'Tom fährt nach Berlin.'),
        'b': ('Ein Satz mit „lesen"', 'Schreib einen Satz: sie liest …',
              'Maria liest ein Buch.'),
        'c': ('Drei Vokalwechsel-Verben', 'Drei Sätze mit du-Form.',
              'Du fährst Auto. Du liest Zeitung. Du sprichst Deutsch.'),
        'd': ('Eine Frage', 'Stell eine Frage mit Vokalwechsel.',
              'Sprichst du Englisch?'),
        'e': ('Mini-Dialog', 'Frage und Antwort.',
              '— Was liest du gern? — Ich lese Romane.'),
    }),

    '1063G': g('1063G', 'Wann machst du …?', 'Fragen mit „wann"', {
        'a': ('Wann stehst du auf?', 'Antworte: ich stehe um … auf.',
              'Ich stehe um sieben Uhr auf.'),
        'b': ('Drei „wann"-Fragen', 'Schreib drei Fragen mit „wann".',
              'Wann frühstückst du? Wann arbeitest du? Wann schläfst du?'),
        'c': ('Aktivitäten mit Uhrzeit', 'Drei Sätze mit Uhrzeit.',
              'Um 8 Uhr esse ich. Um 14 Uhr arbeite ich. Um 22 Uhr schlafe ich.'),
        'd': ('Plan für morgen', 'Drei Sätze: morgen mache ich …',
              'Morgen früh stehe ich um 6 auf. Mittags treffe ich Maria. Abends lese ich.'),
        'e': ('Mini-Dialog', 'Verabredung mit „wann".',
              '— Wann treffen wir uns? — Um sechs Uhr abends.'),
    }),

    '1073G': g('1073G', 'Monate und Datum', 'Monate, Datum, Ordnungszahlen', {
        'a': ('Dein Geburtstag', 'Wann hast du Geburtstag?',
              'Am 15. Juni.'),
        'b': ('Die Monate', 'Schreib vier Monate auf.',
              'Januar, April, August, Dezember.'),
        'c': ('Drei Daten', 'Schreib drei wichtige Daten.',
              'Am 1. Januar. Am 10. Mai. Am 24. Dezember.'),
        'd': ('Feiertage', 'Nenne drei Feiertage in deinem Land.',
              'Weihnachten am 25. Dezember. Ostern im April. Neujahr am 1. Januar.'),
        'e': ('Mini-Dialog', 'Frage und Antwort zum Geburtstag.',
              '— Wann hast du Geburtstag? — Am 12. März. Und du?'),
    }),

    '1083G': g('1083G', 'Wortstellung', 'die deutsche Wortstellung (Verb an Position 2)', {
        'a': ('Drei Sätze mit V2', 'Schreib drei einfache Hauptsätze.',
              'Ich lerne Deutsch. Heute koche ich. Am Sonntag schlafe ich lange.'),
        'b': ('Sätze mit Zeit am Anfang', 'Drei Sätze: Zeit, Verb, Subjekt.',
              'Morgen gehe ich einkaufen. Abends lese ich. Heute bin ich müde.'),
        'c': ('Frage am Anfang', 'Drei Ja/Nein-Fragen (Verb an Position 1).',
              'Kommst du mit? Magst du Pizza? Spielst du Fußball?'),
        'd': ('W-Frage', 'Drei W-Fragen.',
              'Wo wohnst du? Was machst du? Wie geht es dir?'),
        'e': ('Mini-Dialog', 'Frage und Antwort.',
              '— Wann beginnst du? — Morgen früh beginne ich.'),
    }),

    '1093G': g('1093G', 'Die Verneinung', 'die Verneinung mit „nicht" und „kein"', {
        'a': ('„Nicht"-Sätze', 'Drei Sätze mit „nicht".',
              'Ich arbeite nicht. Das ist nicht schön. Wir kommen nicht.'),
        'b': ('„Kein"-Sätze', 'Drei Sätze mit „kein/keine".',
              'Ich habe kein Auto. Sie hat keine Zeit. Wir haben kein Brot.'),
        'c': ('Negative Antworten', 'Drei Nein-Antworten auf Fragen.',
              'Nein, ich lerne kein Französisch. Nein, ich gehe nicht. Nein, ich habe keinen Hund.'),
        'd': ('Was magst du nicht?', 'Drei Sätze über Dinge, die du nicht magst.',
              'Ich mag keinen Käse. Ich tanze nicht gern. Ich fahre nicht Auto.'),
        'e': ('Mini-Dialog', 'Eine Frage und Nein-Antwort.',
              '— Hast du Zeit? — Nein, ich habe keine Zeit.'),
    }),

    '1103G': g('1103G', 'Nominativ und Akkusativ', 'Nominativ und Akkusativ', {
        'a': ('Akkusativ mit „haben"', 'Drei Sätze: ich habe einen/eine/ein …',
              'Ich habe einen Hund. Ich habe eine Katze. Ich habe ein Auto.'),
        'b': ('Nominativ als Subjekt', 'Drei Sätze mit „der Hund / die Katze / das Auto …".',
              'Der Hund ist groß. Die Katze ist klein. Das Auto ist alt.'),
        'c': ('Akkusativ mit „kaufen"', 'Drei Sätze mit „kaufen".',
              'Ich kaufe einen Apfel. Ich kaufe eine Banane. Ich kaufe ein Brot.'),
        'd': ('Akkusativ-Frage', 'Eine Frage mit Akkusativ.',
              'Hast du einen Stift?'),
        'e': ('Mini-Dialog', 'Frage und Antwort mit Akkusativ.',
              '— Hast du einen Bruder? — Ja, ich habe einen Bruder.'),
    }),

    '1113G': g('1113G', 'Dativ nach Präpositionen', 'der Dativ nach mit, bei, von, zu', {
        'a': ('Mit dem Bus', 'Drei Sätze: ich fahre mit …',
              'Ich fahre mit dem Bus. Ich fahre mit dem Zug. Ich fahre mit dem Fahrrad.'),
        'b': ('Bei der Arbeit', 'Drei Sätze mit „bei".',
              'Ich bin bei meiner Mutter. Wir wohnen bei den Großeltern. Sie arbeitet bei der Bank.'),
        'c': ('Von wem?', 'Drei Sätze mit „von".',
              'Das Geschenk ist von meiner Schwester. Der Brief ist von Tom. Die Idee ist von uns.'),
        'd': ('Zu wem gehst du?', 'Drei Sätze mit „zu".',
              'Ich gehe zu meinem Arzt. Wir fahren zu unserer Tante. Du gehst zur Schule.'),
        'e': ('Mini-Dialog', 'Frage und Antwort mit Dativ.',
              '— Wohin gehst du? — Zu meinem Freund.'),
    }),

    '1123G': g('1123G', 'Modalverben', 'die Modalverben können, müssen, wollen', {
        'a': ('Ich kann', 'Drei Sätze: ich kann …',
              'Ich kann schwimmen. Ich kann kochen. Ich kann Deutsch sprechen.'),
        'b': ('Ich muss', 'Drei Sätze: ich muss …',
              'Ich muss arbeiten. Ich muss einkaufen. Ich muss früh aufstehen.'),
        'c': ('Ich will / möchte', 'Drei Sätze mit „will" oder „möchte".',
              'Ich möchte einen Kaffee. Ich will nach Berlin fahren. Ich möchte Deutsch lernen.'),
        'd': ('Drei Modalverben', 'Drei Sätze mit verschiedenen Modalverben.',
              'Ich kann gut singen. Ich muss heute lernen. Ich möchte ins Kino gehen.'),
        'e': ('Mini-Dialog', 'Frage und Antwort mit Modalverb.',
              '— Kannst du mir helfen? — Ja, gern.'),
    }),

    '1133G': g('1133G', 'Nebensätze mit weil und dass', 'Nebensätze mit „weil" und „dass"', {
        'a': ('Drei „weil"-Sätze', 'Drei Sätze mit „weil".',
              'Ich lerne Deutsch, weil ich in Berlin lebe. Ich bin müde, weil ich wenig schlafe. Ich freue mich, weil heute Sonne ist.'),
        'b': ('Drei „dass"-Sätze', 'Drei Sätze mit „dass".',
              'Ich glaube, dass es regnet. Ich weiß, dass du müde bist. Ich denke, dass das gut ist.'),
        'c': ('Eine Erklärung', 'Erklär etwas mit „weil".',
              'Ich gehe nicht aus, weil ich krank bin.'),
        'd': ('Eine Meinung', 'Eine Meinung mit „dass".',
              'Ich finde, dass Deutsch schön ist.'),
        'e': ('Mini-Dialog', 'Frage und Antwort mit „weil" oder „dass".',
              '— Warum lernst du Deutsch? — Weil ich in Deutschland leben will.'),
    }),

    '2012G': g('2012G', 'Possessivartikel', 'die Possessivartikel (mein, dein, sein …)', {
        'a': ('Deine Familie', 'Drei Sätze mit „mein/meine".',
              'Mein Vater ist nett. Meine Mutter kocht gut. Mein Bruder ist groß.'),
        'b': ('Deine Sachen', 'Drei Sätze mit „mein/meine".',
              'Mein Buch ist neu. Meine Tasche ist schwarz. Mein Handy ist alt.'),
        'c': ('Du-Form', 'Drei Fragen mit „dein/deine".',
              'Wo ist dein Buch? Wer ist deine Schwester? Wie heißt dein Hund?'),
        'd': ('Andere Personen', 'Drei Sätze mit „sein/ihr".',
              'Sein Auto ist groß. Ihre Familie wohnt in Polen. Sein Hund ist süß.'),
        'e': ('Mini-Dialog', 'Frage und Antwort.',
              '— Wo ist dein Pass? — Mein Pass ist auf dem Tisch.'),
    }),

    '2022G': g('2022G', 'Wegbeschreibung und Imperativ', 'der Imperativ für Anweisungen', {
        'a': ('Drei Imperative', 'Drei Sätze: geh!, fahr!, biege ab!',
              'Geh geradeaus! Fahr nach rechts! Biege links ab!'),
        'b': ('Wegbeschreibung', 'Drei Sätze mit Imperativ.',
              'Geh hundert Meter. Dann nimm die zweite Straße rechts. Das Café ist auf der linken Seite.'),
        'c': ('Höflich („Sie")', 'Drei Imperative mit „Sie".',
              'Gehen Sie geradeaus! Nehmen Sie die nächste Straße links! Suchen Sie das blaue Haus!'),
        'd': ('Tipps geben', 'Drei Imperative mit Tipps.',
              'Probier die Pizza! Geh in den Park! Lies dieses Buch!'),
        'e': ('Mini-Dialog', 'Touristen-Frage mit Wegbeschreibung.',
              '— Wo ist das Museum? — Gehen Sie geradeaus, dann links.'),
    }),

    '2032G': g('2032G', 'Lokale Präpositionen mit Dativ', 'lokale Präpositionen mit Dativ (in, an, auf, neben …)', {
        'a': ('Wo bist du?', 'Drei Sätze mit Dativ-Präpositionen.',
              'Ich bin im Café. Ich bin am Bahnhof. Ich bin auf der Straße.'),
        'b': ('Wo ist X?', 'Drei Sätze über Möbel.',
              'Das Buch ist auf dem Tisch. Die Tasche ist neben dem Stuhl. Der Stift ist in der Schublade.'),
        'c': ('Wo wohnst du?', 'Drei Sätze mit Dativ.',
              'Ich wohne in Berlin. Ich wohne in einem alten Haus. Ich wohne in der Stadtmitte.'),
        'd': ('Treffpunkt', 'Drei Treffpunkte mit Dativ.',
              'Wir treffen uns am Brandenburger Tor. Wir treffen uns vor dem Kino. Wir treffen uns in dem kleinen Café.'),
        'e': ('Mini-Dialog', 'Frage und Antwort mit Dativ.',
              '— Wo bist du? — Ich bin im Park, an der Bank vor dem See.'),
    }),

    '2042G': g('2042G', 'welch- und dies-', 'die Wörter „welch-" und „dies-"', {
        'a': ('Welche Frage?', 'Drei Fragen mit „welche/welcher/welches".',
              'Welche Farbe magst du? Welcher Tag ist heute? Welches Buch liest du?'),
        'b': ('Antworten mit „dies-"', 'Drei Antworten mit „dieser/diese/dieses".',
              'Diese Farbe gefällt mir. Dieser Tag ist Montag. Dieses Buch ist gut.'),
        'c': ('Im Geschäft', 'Drei Fragen mit „welch-".',
              'Welche Schuhe magst du? Welcher Pullover ist günstig? Welches Hemd ist neu?'),
        'd': ('Drei „dies-"-Sätze', 'Drei Sätze über Dinge vor dir.',
              'Diese Tasche ist meine. Dieser Stift schreibt schlecht. Dieses Café ist klein.'),
        'e': ('Mini-Dialog', 'Frage und Antwort.',
              '— Welche Jacke nimmst du? — Diese blaue Jacke.'),
    }),

    '2052G': g('2052G', 'Präteritum von sein und haben', '„war" und „hatte"', {
        'a': ('Wo warst du?', 'Drei Sätze: ich war …',
              'Ich war zu Hause. Ich war in Berlin. Ich war im Park.'),
        'b': ('Was hattest du?', 'Drei Sätze: ich hatte …',
              'Ich hatte einen Hund. Ich hatte ein Auto. Ich hatte eine Idee.'),
        'c': ('Über gestern', 'Drei Sätze über gestern.',
              'Gestern war ich müde. Ich hatte viel Arbeit. Es war ein langer Tag.'),
        'd': ('Über deine Kindheit', 'Drei Sätze mit „war/hatte".',
              'Ich war oft glücklich. Ich hatte einen Hund. Wir waren in den Bergen.'),
        'e': ('Mini-Dialog', 'Frage und Antwort.',
              '— Wo warst du gestern? — Ich war zu Hause. — Hattest du viel Arbeit? — Ja, leider.'),
    }),

}
