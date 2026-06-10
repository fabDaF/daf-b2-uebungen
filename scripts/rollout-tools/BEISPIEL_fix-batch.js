#!/usr/bin/env node
/* C1-Batch 9: Einheit 203 (Partizipialkonstruktionen, akademische Sprache, Geschichte, Technik). */
const { T, applyFix } = require('./apply_lib2.js');

applyFix({
  'DE_C1_2031G-partizipialkonstruktionen.html': {
    0: [T('die von Gutenberg erfundene Drucktechnik veränderte Europa , weil Wissen plötzlich billig wurde')],
    1: [T('die zu zahlende Summe beträgt 1248 Euro , wie die beigefügte Rechnung ausweist')],
    2: [T('das gestern bestellte Paket liegt beim Nachbarn , weil niemand zu Hause war')],
    3: [T('ich sah eine in der Ferne winkende Frau , die ich nicht erkannte')],
    4: [T('die von den Kürzungen betroffenen Personen werden informiert , bevor die Presse berichtet')],
    5: [T('die nicht zu unterschätzende Gefahr heißt Selbstüberschätzung , wie erfahrene Trainer immer wieder warnen')]
  },
  'DE_C1_2032X-akademische-sprache.html': {
    0: [T('der vorliegende Text gliedert sich in drei Abschnitte , die inhaltlich aufeinander aufbauen')],
    1: [T('in Bezug auf den ersten Aspekt lässt sich feststellen , dass Klärungsbedarf besteht')],
    2: [T('es ist anzunehmen , dass sich die Lage seit der Erhebung verändert hat')],
    3: [T('daran anschließend sei betont , dass die verwendeten Quellen methodisch sehr verschieden sind')],
    4: [T('abschließend ist festzuhalten , dass weitere Untersuchungen in diesem Feld dringend nötig sind')],
    5: [T('diese These ist von erheblicher Bedeutung , weil die folgende Analyse darauf aufbaut')]
  },
  'DE_C1_2033R-buchdruck-revolution.html': {
    0: [T('Gutenberg brachte den Buchdruck um 1450 nach Europa , wo er alles veränderte')],
    1: [T('bewegliche Lettern ermöglichten die Massenproduktion von Büchern , die zuvor reine Handarbeit waren')],
    2: [T('die Reformation Luthers verbreitete sich binnen Wochen , weil der Buchdruck Flugschriften ermöglichte')],
    3: [T('bereits im 9. Jahrhundert kannten die Chinesen Druckverfahren , die Europa unbekannt blieben')],
    4: [T('die Druckerpresse übernahm Gutenberg von der Weintraubenpresse , die er technisch geschickt umbaute')],
    5: [T('der Buchdruck veränderte die Wissenskultur grundlegend , weil Bildung nicht länger Privileg blieb')]
  },
  'DE_C1_2034S-probleme-beschreiben.html': {
    0: [T('dieses Argument ist ein Widerspruch in sich , den jeder sofort erkennen kann')],
    1: [T('die Reform stellt uns vor eine Herausforderung , die wir nicht unterschätzen dürfen')],
    2: [T('wir müssen das Problem heute anschneiden , bevor es sich noch weiter verschärft')],
    3: [T('die Kontroverse um die Reform dauert zwei Jahre , ohne dass eine Lösung absehbar ist')],
    4: [T('seine unstrukturierte Arbeitsweise war ein folgenschwerer Fehler , der das ganze Projekt gefährdete')],
    5: [T('die Studie weist methodische Defizite auf , die ihre zentralen Ergebnisse fragwürdig machen')]
  },
  'DE_C1_2035R-berliner-mauer.html': {
    0: [T('die Berliner Mauer wurde 1961 errichtet , um die anhaltende Massenflucht zu stoppen')],
    1: [T('am 9. November 1989 fiel die Mauer , nachdem sie 28 Jahre gestanden hatte')],
    2: [T('Schabowskis Pressekonferenz löste den Massenandrang aus , weil seine berühmte Antwort sofort galt')],
    3: [T('die Friedliche Revolution begann mit Montagsdemonstrationen , die in Leipzig immer größer wurden')],
    4: [T('mindestens 140 Menschen starben an der Mauer , weil sie die Freiheit suchten')],
    5: [T('die deutsche Wiedervereinigung erfolgte im Oktober 1990 , nachdem beide Staaten verhandelt hatten')]
  },
  'DE_C1_2036S-wettlauf-ins-all.html': {
    0: [T('der Sputnik umrundete ab Oktober 1957 die Erde , was den Westen schockierte')],
    1: [T('Juri Gagarin flog 1961 als erster Mensch ins All , bevor Amerika reagieren konnte')],
    2: [T('Apollo 11 brachte Armstrong und Aldrin auf den Mond , während die Welt zusah')],
    3: [T('der Sputnik-Schock löste die Gründung der NASA aus , weil Amerika aufholen musste')],
    4: [T('die ISS ist seit 1998 ein Symbol der Kooperation , das ehemalige Gegner verbindet')],
    5: [T('SpaceX veränderte die Raumfahrt grundlegend , weil wiederverwendbare Raketen die Kosten drastisch senkten')]
  },
  'DE_C1_2037R-nietzsche-geschichte.html': {
    0: [T('Nietzsche schrieb seine Schrift über Geschichte 1874 , als er in Basel lehrte')],
    1: [T('der Mensch beneidet das Vieh um sein Vergessen , weil ihn die Vergangenheit belastet')],
    2: [T('zu viel Geschichte kann das Leben lähmen , wie Nietzsche damals provokant behauptete')],
    3: [T('Nietzsche unterscheidet drei Arten historischer Wahrnehmung , die jeweils ganz eigene Gefahren bergen')],
    4: [T('die monumentale Geschichte gibt Kraft , weil große Vorbilder direkt zum Handeln ermutigen')],
    5: [T('der Mensch braucht das Vergessen , um überhaupt handeln und leben zu können')]
  },
  'DE_C1_2038S-elektrizitaet.html': {
    0: [T('Volta baute 1800 die erste Batterie , die erstmals dauerhaft elektrischen Strom lieferte')],
    1: [T('Faraday entdeckte 1831 die elektromagnetische Induktion , auf der alle unsere Generatoren beruhen')],
    2: [T('Edison brachte 1879 die Glühbirne zur Marktreife , obwohl andere sie vorher erfanden')],
    3: [T('das erste öffentliche Stromnetz ging 1882 ans Netz , als Edison Manhattan beleuchtete')],
    4: [T('die Energiewende beschleunigte sich nach 2011 , als Deutschland den endgültigen Atomausstieg beschloss')],
    5: [T('heute kommt der Strom überwiegend aus erneuerbaren Quellen , die stetig ausgebaut werden')]
  }
}, { dir: '/sessions/beautiful-friendly-ride/mnt/fabDaF/htmlS/C1', min: 12, max: 18 });
