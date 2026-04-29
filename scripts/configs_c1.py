#!/usr/bin/env python3
"""
Schreibwerkstatt-Aufgaben für C1-Lektionen — Lückenschluss.
Skalierung C1: 40–80 Wörter pro Aufgabe, MIN_CHARS=15.
Aufgabencharakter: Stellungnahme, Vergleich, kohärente Argumentation.
"""
from __future__ import annotations
BANNER = ('https://images.pexels.com/photos/733856/pexels-photo-733856.jpeg?auto=compress&cs=tinysrgb&w=800',
          'Notizbuch und Stift, bereit zum Schreiben')

def _t(titel, frage, beispiel):
    return {'titel': titel, 'frage': frage, 'beispiel': beispiel}

def _cfg(code, title, intro, t1, t2, t3, t4, t5):
    return {'lesson_code': code, 'lesson_title': title,
            'banner_url': BANNER[0], 'banner_alt': BANNER[1],
            'intro': intro, 'tasks': [t1, t2, t3, t4, t5]}

CONFIGS = {
    '3069X': _cfg('3069X', 'DevOps-Kultur',
        'Fünf Schreibaufgaben rund um DevOps, Organisationskultur und systemische Reflexion.',
        _t('DevOps in deiner Erfahrung',
           'Hast du DevOps-Kultur oder vergleichbare Arbeitsformen erlebt? Schildere — auch wenn du nicht in IT arbeitest. Welche Elemente waren tragfähig, welche blieben Marketing-Rhetorik? (50-70 Wörter)',
           'In meiner Schule wurde 2022 „agile Methoden" eingeführt — Stand-ups, Retrospektiven, Lernlandkarten. Manches wirkte: Lehrer tauschten Materialien systematischer aus. Anderes blieb leer: ohne strukturelle Entlastung waren Retrospektiven Zusatzbelastung statt Reflexionsraum. Die wertvollen Praktiken überlebten, die rituell aufgesetzten verschwanden nach einem Jahr. Kultur lässt sich nicht verordnen — sie muss durch passende Strukturen getragen werden.'),
        _t('Strukturelle Voraussetzungen',
           'Welche strukturellen Voraussetzungen müssten gegeben sein, damit eine angestrebte Kulturveränderung über reine Haltungsappelle hinaus tatsächlich greift? Schreib einen analytischen Absatz mit zwei konkreten Bedingungen. (50-70 Wörter)',
           'Erstens psychologische Sicherheit, die nicht verbal beschworen, sondern durch Hierarchie-Reduktion und sanktionsfreie Fehlerkultur etabliert wird. Zweitens Zeit-Ressourcen: Reflexionsroutinen brauchen geschützte Slots, die nicht der „eigentlichen Arbeit" abgerungen werden müssen. Wo Arbeitsverdichtung das Gegenteil bewirkt — mehr Aufgaben in weniger Zeit —, kollabiert jede Haltungs-Initiative. Kultur ist Folge struktureller Bedingungen, nicht ihre Vorbedingung.'),
        _t('Manageriale Reduktion',
           'Das Konzept reduziert organisationale Dysfunktionalität auf mangelnde Werte und Haltungen. Welche Konsequenzen hat diese Reduktion? Argumentiere mit Bezug auf Verantwortungszuschreibung. (50-70 Wörter)',
           'Die Engführung verlagert die Verantwortung systematisch auf das Individuum: Wer scheitert, hat die richtige Haltung nicht entwickelt. Strukturelle Probleme — überlastete Teams, undurchdachte Prozesse, mikropolitische Machtkonstellationen — werden ausgeblendet. Diese Individualisierung ist analytisch unzureichend und ethisch problematisch, denn sie bürdet Mitarbeitenden eine Verantwortung auf, die sie unter den gegebenen Bedingungen nicht tragen können. Sie funktioniert als Entlastungsdiskurs für das Management.'),
        _t('Eine kritische Empfehlung',
           'Stell dir vor, du würdest das OpenCulture-Habit-Kit für ein Team begutachten. Welche Empfehlung würdest du der Geschäftsführung geben — uneingeschränkte Übernahme, modifizierte Anwendung oder Ablehnung? Begründe in einem Absatz. (50-70 Wörter)',
           'Modifizierte Anwendung. Die Mikropraktiken — Retrospektiven, Wissenstransfer, Reflexionsrituale — sind didaktisch wertvoll und nachweislich wirksam. Ihre Übernahme empfehle ich. Gleichzeitig würde ich die Geschäftsführung darauf hinweisen, dass die Wirksamkeit dieser Praktiken an strukturelle Voraussetzungen gebunden ist: Zeit, psychologische Sicherheit, sanktionsfreie Lernkultur. Ohne deren Etablierung bleibt das Konzept eine Marketing-Hülle, die im schlimmsten Fall zusätzliche Belastung erzeugt.'),
        _t('Mini-Dialog: Im Strategie-Workshop',
           'Du diskutierst mit einer Personalleiterin über die geplante DevOps-Einführung. Sie möchte schnelle Resultate, du mahnst zur strukturellen Vorbereitung. Schreib zwei Beiträge pro Person. (50-70 Wörter)',
           '— Wir starten in drei Wochen mit den Retrospektiven, die Vorlagen sind fertig. — Verstehe den Druck. Aber ohne Klärung, wie mit kritischen Befunden umgegangen wird, werden die Retrospektiven leer. — Das regelt sich beim Tun. — Empirisch nicht. Ich schlage zwei Wochen Vorlauf für ein Sicherheits-Charter vor — sonst riskieren wir, die Methode zu verbrennen, bevor sie wirken kann.')),
    '3081X': _cfg('3081X', 'Wendepunkte der deutschen Kulturgeschichte',
        'Fünf Schreibaufgaben rund um Reformation, Aufklärung, Weimarer Klassik und 1968.',
        _t('Welcher Wendepunkt hat dich am meisten beschäftigt?',
           'Welcher der vier Wendepunkte (Reformation, Aufklärung, Weimarer Klassik, 1968) hat in deiner persönlichen Bildungsbiografie die größte Rolle gespielt? Begründe. (50-70 Wörter)',
           'Die Aufklärung — sie war in meiner gymnasialen Bildung allgegenwärtig: Lessing, Kant, Lichtenberg. Was sie für mich produktiv machte, war nicht das historische Datum, sondern die Geste der Mündigkeit. „Sapere aude" als Aufforderung, sich nicht hinter Autoritäten zu verstecken — diese Haltung trage ich seither in akademische und politische Diskussionen. Die anderen drei Wendepunkte kannte ich, doch nur die Aufklärung wurde Teil meines Selbstverständnisses.'),
        _t('Paradigmenwechsel definieren',
           'Was unterscheidet einen historischen Wendepunkt von einem bloßen Ereignis? Argumentiere mit einem Beispiel aus dem Text. (50-70 Wörter)',
           'Ein Wendepunkt rekonfiguriert die Voraussetzungen, unter denen sich eine Gesellschaft selbst denkt. Die Reformation war nicht primär ein religiöses Ereignis, sondern eine epistemologische Verschiebung: Heilige Schrift wurde individuell auslegbar, was Autoritätsstrukturen unterspülte und Bildungsexpansion erzwang. Ein bloßes Ereignis lässt diese Tiefenstruktur unangetastet. Wendepunkte erkennt man daran, dass nach ihnen die Fragen anders gestellt werden, nicht nur die Antworten anders ausfallen.'),
        _t('1968 — Bilanz nach 60 Jahren',
           '1968 wird im Text als kultureller Wendepunkt benannt. Welche Errungenschaften und welche problematischen Folgen siehst du heute, nahezu sechs Jahrzehnte später? Schreib einen ausgewogenen Absatz. (50-70 Wörter)',
           'Errungenschaften: die Demokratisierung von Universität und Familie, die schrittweise Entkriminalisierung weiblicher Sexualität, ein neuer Umgang mit der NS-Geschichte. Problematische Folgen: eine bisweilen ahistorische Identitätspolitik, die strukturelle Klassenfragen verdrängt, sowie eine kulturelle Selbstgenügsamkeit der Bewegung, die spätere Generationen entfremdete. 1968 hat Räume geöffnet — und gleichzeitig Codes etabliert, deren Veränderung heute schwerfällt. Beide Befunde gehören zu einer ehrlichen Bilanz.'),
        _t('Ein fünfter Wendepunkt',
           'Wenn du einen fünften Wendepunkt benennen müsstest — etwa 1989 oder die Migration der 2010er Jahre —, welchen würdest du wählen und mit welcher These rechtfertigen? (50-70 Wörter)',
           '1989 — die friedliche Revolution und die Wiedervereinigung. Sie zwang die Bundesrepublik, ihre stillen Identitäts-Sicherheiten zu überprüfen: Was war westdeutsches Selbstverständnis, wenn der Osten nicht mehr Anti-These war, sondern Realität? Die Verschiebung wirkte kulturell langsamer als politisch — in Literatur, Geschichtsschreibung, Sprache vollzog sich der Bruch erst über Jahrzehnte. Heute ist 1989 der jüngste echte Wendepunkt, dessen Folgen noch produktiv ausgehandelt werden.'),
        _t('Mini-Dialog: Im Seminar',
           'Du diskutierst im Universitätsseminar mit einer Kommilitonin, die behauptet, „Wendepunkte" seien bloße narrative Konstruktionen ohne reale Wirkkraft. Antworte respektvoll, aber widersprich substanziell. (50-70 Wörter)',
           '— Diese Wendepunkte sind doch retrospektive Erzählungen — wir bauen sie nachträglich. — Teilweise. Aber wenn Luthers Bibelübersetzung empirisch die Lese-Alphabetisierung Deutschlands transformiert hat, ist das mehr als Erzählung. — Du naturalisierst eine Konstruktion. — Eher umgekehrt: Konstruktionen mit messbaren Folgen sind nicht weniger real, weil sie konstruiert sind. Hier hilft Kategorienunterscheidung — Narrativ vs. Wirkung — statt Pauschal-Zurückweisung.')),
    '3083X': _cfg('3083X', 'Wahlversprechen und Regierungshandeln',
        'Fünf Schreibaufgaben rund um die Bilanz politischer Versprechen.',
        _t('Politische Versprechen — überprüfbar?',
           'Welche Wahlversprechen aus deinem Land hast du in den letzten Jahren mitverfolgt? Wie verlässlich war ihre Umsetzung? Schreib einen reflektierenden Absatz. (50-70 Wörter)',
           'Die spanische Sozialgesetzgebung der vergangenen Legislaturperioden wurde überraschend konsequent umgesetzt — Arbeitsmarktreform, Mindestlohnerhöhungen, Mietpreisregulierung. Andere Versprechen blieben kosmetisch: Bildungsreform und Wohnungsbau wurden mehrfach angekündigt, aber budgetär unzureichend hinterlegt. Mein Befund: Strukturreformen mit klaren Adressaten gelingen öfter, generelle Versprechen ohne Zielgruppen-Druck verlaufen häufig im Sand. Wer Versprechen einlösen will, braucht klare Adressaten und kontrollierbare Indikatoren.'),
        _t('Aktivrente — kritische Würdigung',
           'Bewerte das im Text genannte „Aktivrente"-Konzept aus zwei Perspektiven: arbeitsmarktpolitisch und sozialpolitisch. (50-70 Wörter)',
           'Arbeitsmarktpolitisch ist die Aktivrente sinnvoll — sie nutzt das Erfahrungswissen älterer Beschäftigter und entlastet bei Fachkräftemangel. Sozialpolitisch ist sie ambivalent: Sie privilegiert jene, die gesundheitlich und biografisch in der Lage sind weiterzuarbeiten — meist gut situierte Akademiker. Wer mit 65 körperlich erschöpft aus einem Pflegeberuf kommt, profitiert nicht. Eine sozial gerechte Variante würde die Maßnahme mit gestaffelten Anreizen für niedrige Renteneinkommen koppeln.'),
        _t('Verwässerung — was bedeutet das politisch?',
           'Was meint der Text mit „verwässerten" Versprechen? Erläutere den Mechanismus mit einem konkreten Beispiel deiner Wahl. (50-70 Wörter)',
           'Verwässerung bezeichnet das Beibehalten der politischen Etiketten bei substanzieller Aushöhlung der Inhalte — sei es durch verzögerte Umsetzung, abgespeckte Finanzierung oder eingeschränkte Geltungsbereiche. Beispiel: Ein „Mindestlohn von 15 Euro" wird beschlossen, aber erst 2030 wirksam und mit zahlreichen Branchenausnahmen versehen. Formal eingelöst, faktisch entkernt. Solche Manöver sind politisch attraktiv, weil sie Wahlversprechen erfüllen, ohne Konflikte mit mächtigen Lobby-Akteuren auszufechten — auf Kosten der Glaubwürdigkeit.'),
        _t('Demokratische Verantwortung',
           'Welche Mechanismen müsste eine Demokratie bereitstellen, damit Wähler die Einlösung von Wahlversprechen systematisch und nicht nur anekdotisch überprüfen können? (50-70 Wörter)',
           'Erstens unabhängige Bilanz-Kommissionen, die jährlich messbare Indikatoren öffentlich machen — wie der schweizerische Nationalrat einzelne Politikfelder evaluieren lässt. Zweitens präzisere Koalitionsverträge mit verbindlichen Meilensteinen statt unverbindlicher Absichtserklärungen. Drittens öffentlich-rechtliche Medien mit klarem Mandat zur Versprechen-Bilanzierung. Diese drei Mechanismen würden zwar politische Beweglichkeit reduzieren, dafür aber demokratische Rechenschaftspflicht stärken — ein Kompromiss, der dem aktuellen Glaubwürdigkeitsverlust angemessen wäre.'),
        _t('Mini-Dialog: Eine Politikerin verteidigt ihre Bilanz',
           'Du interviewst eine Bundestagsabgeordnete, die argumentiert, „aufgeschobene" Versprechen seien notwendige Realpolitik. Halte respektvoll, aber substanziell dagegen. (50-70 Wörter)',
           '— Aufschub ist verantwortungsvoll, wenn die Haushaltslage es erfordert. — Verstehe das. Aber wenn dieselbe Begründung in jeder Legislaturperiode greift, wird sie zur strukturellen Ausrede. — Sie können nicht alle Probleme gleichzeitig lösen. — Korrekt. Doch warum kommunizieren Sie das nicht im Wahlkampf, statt nachträglich? Ehrliche Priorisierung würde Vertrauen schützen — schweigende Vertagung untergräbt es nachhaltig.')),
}
