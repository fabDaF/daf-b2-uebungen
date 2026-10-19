#!/usr/bin/env python3
"""add_schreib_kollok.py — Schreibwerkstatt mit Kollokations-Radar für die Kollokationen-Serie.

Muster: Pilot Teil 2 (FB-SCHREIB-KOLLOK, 2026-10-19). Baut pro Datei als LETZTEN Tab
„📨 Schreibwerkstatt" ein: 5 lektionsgebundene Mikroaufgaben, je 3 Pflicht-Kollokationen
als Chips, Live-Radar (Nomen + Verb-/Adjektivstamm irgendwo im Text → Chip grün),
Standard-Pattern (Name-Pflicht, Web3Forms, body.success-Check, Fehler-UX, LocalStorage).

Aufruf (aus daf-materialien):
  python3 ../scripts/add_schreib_kollok.py Grundlagen/Kollokationen/kollokationen-teil1-*.html …
Danach: python3 ../scripts/inject_schreib_name.py DATEI (FB-NAME-REQUIRED) + check_all.py.
Der JS-Rumpf (ab schreibKollCheck) liegt in schreib_kollok_body.js neben diesem Skript —
Quelle ist der Pilot Teil 2; nie von Hand abweichen (Drift).
"""
import os, re, sys

# ---------- Aufgaben + Radar pro Teil ----------
# Radar: n = Nomen-Stamm (klein, Regex erlaubt), v = Verb-/Adjektiv-Regex (flektionstolerant, locker)
CONF = {
 1: dict(thema='Leistung, Erfahrung, Bewertung', radar={
   'Fehler unterlaufen':      ('fehler', r'(unterlauf|unterlief|unterl[aä]uft)'),
   'Fehler erkennen':         ('fehler', r'(erkenn|erkannt)'),
   'Fehler korrigieren':      ('fehler', r'korrigier'),
   'Rat erteilen':            ('rat', r'erteil'),
   'Rat befolgen':            ('rat', r'befolg'),
   'wertvoller Rat':          ('rat', r'wertvoll'),
   'Prüfung ablegen':         ('prüfung', r'(ableg|abgelegt|abzulegen|\bleg(e|t|st|te|en|ten)\b)'),
   'Prüfung bestehen':        ('prüfung', r'(besteh|bestand)'),
   'Ergebnis erzielen':       ('ergebnis', r'erziel'),
   'Kritik üben':             ('kritik', r'(\büb(t|te|ten|en|st)\b|geübt)'),
   'Entscheidung treffen':    ('entscheidung', r'(treff|triff|traf|getroffen)'),
   'Entscheidung überdenken': ('entscheidung', r'(überdenk|überdacht)'),
   'langjährige Erfahrung':   ('erfahrung', r'langjährig'),
   'Wirkung entfalten':       ('wirkung', r'entfalt'),
   'Interesse wecken':        ('interesse', r'(weck|geweckt)'),
 }, aufgaben=[
   ("Der Fehler im Formular", "Erzähl von einem Fehler, der dir im Beruf oder im Alltag unterlaufen ist: Wie hast du ihn erkannt, wie hast du ihn korrigiert, und was hat es dich gekostet? (50–70 Wörter)", ["Fehler unterlaufen", "Fehler erkennen", "Fehler korrigieren"]),
   ("Rat vom Mentor", "Jemand hat dir einmal einen wertvollen Rat erteilt. Beschreib die Situation: Wer war es, hast du den Rat befolgt – und hat er sich ausgezahlt? (50–70 Wörter)", ["Rat erteilen", "Rat befolgen", "wertvoller Rat"]),
   ("Mini-Dialog: Nach der Prüfung", "Schreib einen Mini-Dialog mit zwei Fragen und zwei Antworten: Eine Kollegin fragt dich nach einer Prüfung, die du gerade abgelegt hast. Hast du sie bestanden, welches Ergebnis hast du erzielt? (50–70 Wörter)", ["Prüfung ablegen", "Prüfung bestehen", "Ergebnis erzielen"]),
   ("Scharfe Kritik im Meeting", "In einem Meeting hat jemand scharfe Kritik an deinem Vorschlag geübt. Antworte sachlich in einer kurzen Notiz: Welche Entscheidung hast du getroffen – und bist du bereit, sie zu überdenken? (50–70 Wörter)", ["Kritik üben", "Entscheidung treffen", "Entscheidung überdenken"]),
   ("Erfahrung zählt", "Du bist Personalchefin oder Personalchef. Begründe in einem Absatz, welche Wirkung ein Kollege mit langjähriger Erfahrung im Team entfaltet und wie er das Interesse der Jüngeren weckt. (60–80 Wörter)", ["langjährige Erfahrung", "Wirkung entfalten", "Interesse wecken"]),
 ]),
 3: dict(thema='Gesundheit, Krankheit, Behandlung', radar={
   'Diagnose stellen':        ('diagnose', r'(stell|gestellt)'),
   'Therapie einleiten':      ('therapie', r'(einleit|eingeleitet|einzuleiten|\bleit(e|et|est|ete|en|eten)\b)'),
   'eindeutige Diagnose':     ('diagnose', r'eindeutig'),
   'Verletzung erleiden':     ('verletzung', r'(erleid|erlitt)'),
   'Schmerzen lindern':       ('schmerz', r'linder'),
   'Verletzung auskurieren':  ('verletzung', r'kurier'),
   'Medikament verschreiben': ('medikament', r'(verschreib|verschrieb)'),
   'Medikament einnehmen':    ('medikament', r'(einnehm|eingenommen|einzunehmen|\bnehm|\bnimm|\bnahm)'),
   'Medikament absetzen':     ('medikament', r'(absetz|abgesetzt|abzusetzen|\bsetz(e|t|st|te|en|ten)\b)'),
   'Operation durchführen':   ('operation', r'(durchführ|durchgeführt|durchzuführen|\bführ(e|t|st|te|en|ten)\b)'),
   'riskante Operation':      ('operation', r'riskant'),
   'langwierige Behandlung':  ('behandlung', r'langwierig'),
   'Krankheit bekämpfen':     ('krankheit', r'bekämpf'),
   'Krankheit besiegen':      ('krankheit', r'besieg'),
   'gezielte Therapie':       ('therapie', r'gezielt'),
 }, aufgaben=[
   ("Die Diagnose", "Erzähl aus der Sicht eines Patienten: Die Ärztin hat nach der Untersuchung eine Diagnose gestellt und sofort eine Therapie eingeleitet. Wie hast du das Gespräch erlebt, und war die Diagnose eindeutig? (50–70 Wörter)", ["Diagnose stellen", "Therapie einleiten", "eindeutige Diagnose"]),
   ("Mail an den Trainer", "Du hast beim Sport eine Verletzung erlitten. Schreib deinem Trainer eine kurze Mail: Was ist passiert, wie werden die Schmerzen gelindert, und wie lange brauchst du, um die Verletzung auszukurieren? (40–60 Wörter)", ["Verletzung erleiden", "Schmerzen lindern", "Verletzung auskurieren"]),
   ("Mini-Dialog in der Apotheke", "Schreib einen Mini-Dialog mit zwei Fragen und zwei Antworten: Der Arzt hat ein Medikament verschrieben. Du fragst die Apothekerin, wie du es einnehmen sollst und wann du es wieder absetzen kannst. (50–70 Wörter)", ["Medikament verschreiben", "Medikament einnehmen", "Medikament absetzen"]),
   ("Operation – ja oder nein?", "Ein Freund steht vor der Wahl: eine riskante Operation durchführen lassen oder eine langwierige Behandlung beginnen. Nimm Stellung: Welchen Weg würdest du ihm raten, und warum? (60–80 Wörter)", ["Operation durchführen", "riskante Operation", "langwierige Behandlung"]),
   ("Die Krankheit besiegt", "Erzähl die Geschichte einer Person, die eine schwere Krankheit bekämpft und am Ende besiegt hat. Welche Rolle spielte dabei die gezielte Therapie – und welche die Menschen um sie herum? (50–70 Wörter)", ["Krankheit bekämpfen", "Krankheit besiegen", "gezielte Therapie"]),
 ]),
 4: dict(thema='Wirtschaft & Arbeit', radar={
   'Angebot unterbreiten':    ('angebot', r'unterbreit'),
   'überzeugendes Angebot':   ('angebot', r'überzeugend'),
   'Angebot nachbessern':     ('angebot', r'(nachbesser|nachgebessert|nachzubessern|\bbesser(e|t|st|n|te)\b)'),
   'Umsatz erzielen':         ('umsatz', r'erziel'),
   'Gewinn erwirtschaften':   ('gewinn', r'erwirtschaft'),
   'Kosten senken':           ('kosten', r'(senk|gesenkt)'),
   'Vertrag aushandeln':      ('vertrag', r'(aushandel|ausgehandelt|auszuhandeln|\bhandel(e|t|st|te|n|ten)\b)'),
   'Vertrag abschließen':     ('vertrag', r'(abschließ|abgeschlossen|abzuschließen|\bschließ(e|t|st|en)\b|\bschloss)'),
   'Auftrag erteilen':        ('auftrag', r'erteil'),
   'Konkurrenz bedrängen':    ('konkurrenz', r'bedräng'),
   'Märkte erschließen':      ('m[aä]rkt', r'(erschließ|erschloss)'),
   'Investitionen tätigen':   ('investition', r'tätig'),
   'Vertrag kündigen':        ('vertrag', r'(kündig|gekündigt)'),
   'lukrativer Vertrag':      ('vertrag', r'lukrativ'),
   'Konkurrenz einholen':     ('konkurrenz', r'(einhol|eingeholt|einzuholen|\bhol(e|t|st|te|en|ten)\b)'),
 }, aufgaben=[
   ("Das Angebot", "Schreib einem Kunden eine kurze Mail: Du unterbreitest ihm ein Angebot, erklärst, warum es überzeugend ist, und bietest an, es bei Bedarf nachzubessern. (40–60 Wörter)", ["Angebot unterbreiten", "überzeugendes Angebot", "Angebot nachbessern"]),
   ("Notiz zum Quartal", "Schreib eine kurze Notiz an die Geschäftsführung: Welchen Umsatz hat eure Abteilung im letzten Quartal erzielt, welchen Gewinn habt ihr erwirtschaftet, und wo konntet ihr Kosten senken? (50–70 Wörter)", ["Umsatz erzielen", "Gewinn erwirtschaften", "Kosten senken"]),
   ("Mini-Dialog: Vertragsverhandlung", "Schreib einen Mini-Dialog mit zwei Fragen und zwei Antworten zwischen einer Einkäuferin und einem Lieferanten: Der Vertrag wird ausgehandelt – wird er abgeschlossen, und wann wird der erste Auftrag erteilt? (50–70 Wörter)", ["Vertrag aushandeln", "Vertrag abschließen", "Auftrag erteilen"]),
   ("Wachsende Konkurrenz", "Billiganbieter bedrängen euer Unternehmen. Nimm Stellung: Sollte die Firma jetzt neue Märkte erschließen und Investitionen tätigen – oder abwarten? Begründe deine Position. (60–80 Wörter)", ["Konkurrenz bedrängen", "Märkte erschließen", "Investitionen tätigen"]),
   ("Die Kündigung", "Erzähle: Ein wichtiger Kunde hat einen lukrativen Vertrag gekündigt. Was ist passiert, wie hat das Team reagiert, und mit welchem Plan wollt ihr die Konkurrenz wieder einholen? (50–70 Wörter)", ["Vertrag kündigen", "lukrativer Vertrag", "Konkurrenz einholen"]),
 ]),
 5: dict(thema='Beziehungen & Gefühle', radar={
   'Freundschaft knüpfen':    ('freundschaft', r'(knüpf|geknüpft)'),
   'Freundschaft pflegen':    ('freundschaft', r'pfleg'),
   'innige Freundschaft':     ('freundschaft', r'innig'),
   'Respekt erwerben':        ('respekt', r'(erwerb|erwirb|erwarb|erworben)'),
   'Respekt verlieren':       ('respekt', r'(verlier|verlor)'),
   'harmonische Beziehung':   ('beziehung', r'harmonisch'),
   'Wut beherrschen':         ('wut', r'beherrsch'),
   'Wut loswerden':           ('wut', r'(loswerd|loswird|losgeworden|loszuwerden|\blos\b)'),
   'Gefühle ausdrücken':      ('gefühl', r'(ausdrück|ausgedrückt|auszudrücken|\bdrück(e|t|st|te|en|ten)\b)'),
   'Angst schüren':           ('angst', r'(schür|geschürt)'),
   'Hoffnung wecken':         ('hoffnung', r'(weck|geweckt)'),
   'Angst überwinden':        ('angst', r'(überwind|überwand|überwunden)'),
   'Liebe gestehen':          ('liebe', r'(gesteh|gestand)'),
   'Liebe erwidern':          ('liebe', r'erwider'),
   'Leidenschaft entfachen':  ('leidenschaft', r'entfach'),
 }, aufgaben=[
   ("Eine Freundschaft über Jahre", "Erzähl von einer innigen Freundschaft in deinem Leben: Wie habt ihr sie geknüpft, wie pflegt ihr sie heute – trotz Entfernung oder Zeitmangel? (50–70 Wörter)", ["Freundschaft knüpfen", "Freundschaft pflegen", "innige Freundschaft"]),
   ("Respekt im Team", "Beschreib eine Chefin oder einen Kollegen, der sich den Respekt des Teams erworben hat: Wodurch? Und wodurch könnte er ihn wieder verlieren? Was macht die Beziehung im Team harmonisch? (50–70 Wörter)", ["Respekt erwerben", "Respekt verlieren", "harmonische Beziehung"]),
   ("Mini-Dialog: Nach dem Meeting", "Schreib einen Mini-Dialog mit zwei Fragen und zwei Antworten: Jemand kommt wütend aus einem Meeting. Die andere Person hilft ihm, die Wut zu beherrschen und seine Gefühle in Worte zu fassen. (50–70 Wörter)", ["Wut beherrschen", "Wut loswerden", "Gefühle ausdrücken"]),
   ("Angst oder Hoffnung?", "Nimm Stellung: Schüren die Medien in deinem Land eher Angst, oder wecken sie Hoffnung? Was hilft dir persönlich, Angst zu überwinden? (60–80 Wörter)", ["Angst schüren", "Hoffnung wecken", "Angst überwinden"]),
   ("Der Anfang einer Geschichte", "Schreib den Anfang einer kleinen Geschichte: Eine Person gesteht einer anderen ihre Liebe. Wird sie erwidert? Welche Leidenschaft entfacht die Szene – oder was geht schief? (50–70 Wörter)", ["Liebe gestehen", "Liebe erwidern", "Leidenschaft entfachen"]),
 ]),
 6: dict(thema='Recht & Ordnung', radar={
   'Klage einreichen':        ('klage', r'(einreich|eingereicht|einzureichen|\breich(e|t|st|te|en|ten)\b)'),
   'Beweise vorlegen':        ('beweis', r'(vorleg|vorgelegt|vorzulegen|\bleg(e|t|st|te|en|ten)\b)'),
   'begründete Klage':        ('klage', r'begründet'),
   'Verstoß aufdecken':       ('verst[oö]ß', r'(aufdeck|aufgedeckt|aufzudecken|\bdeck(e|t|st|te|en|ten)\b)'),
   'Verstoß ahnden':          ('verst[oö]ß', r'(ahnd|geahndet)'),
   'geltendes Gesetz':        ('gesetz', r'geltend'),
   'Urteil fällen':           ('urteil', r'(fäll|gefällt)'),
   'Urteil anfechten':        ('urteil', r'(anfecht|angefochten|anzufechten|\bf[ei]cht)'),
   'Schuld eingestehen':      ('schuld', r'(gesteh|gestand)'),
   'Gesetz verschärfen':      ('gesetz', r'verschärf'),
   'Gesetz durchsetzen':      ('gesetz', r'(durchsetz|durchgesetzt|durchzusetzen|\bsetz(e|t|st|te|en|ten)\b)'),
   'Haft verhängen':          ('haft', r'(verhäng|verhängt)'),
   'Anklage erheben':         ('anklage', r'(erheb|erhob)'),
   'erdrückende Beweise':     ('beweis', r'erdrückend'),
   'wegweisendes Urteil':     ('urteil', r'wegweisend'),
 }, aufgaben=[
   ("Streit mit dem Vermieter", "Schreib einer Freundin, die Juristin ist, eine kurze Mail: Du überlegst, Klage gegen deinen Vermieter einzureichen. Welche Beweise kannst du vorlegen, und warum hältst du die Klage für begründet? (50–70 Wörter)", ["Klage einreichen", "Beweise vorlegen", "begründete Klage"]),
   ("Notiz an die Compliance-Abteilung", "In deiner Firma wurde ein Verstoß gegen interne Regeln aufgedeckt. Schreib eine sachliche Notiz: Was ist passiert, wie sollte der Verstoß geahndet werden, und was sagt das geltende Gesetz dazu? (50–70 Wörter)", ["Verstoß aufdecken", "Verstoß ahnden", "geltendes Gesetz"]),
   ("Mini-Dialog: Nach dem Urteil", "Schreib einen Mini-Dialog mit zwei Fragen und zwei Antworten zwischen Anwältin und Mandant: Das Gericht hat sein Urteil gefällt. Soll man es anfechten – oder die Schuld eingestehen? (50–70 Wörter)", ["Urteil fällen", "Urteil anfechten", "Schuld eingestehen"]),
   ("Härtere Gesetze?", "Nimm Stellung: Sollte der Staat die Gesetze gegen Steuerhinterziehung verschärfen und konsequenter durchsetzen – bis hin zu Haftstrafen, die verhängt werden? Begründe deine Position. (60–80 Wörter)", ["Gesetz verschärfen", "Gesetz durchsetzen", "Haft verhängen"]),
   ("Der Prozess", "Erzähl einen fiktiven Fall: Die Staatsanwaltschaft erhebt Anklage, die Beweise sind erdrückend – und am Ende steht ein wegweisendes Urteil. Was war das Besondere an diesem Fall? (50–70 Wörter)", ["Anklage erheben", "erdrückende Beweise", "wegweisendes Urteil"]),
 ]),
 7: dict(thema='Bildung & Wissenschaft', radar={
   'Studium aufnehmen':       ('studium', r'(aufnehm|aufgenommen|aufzunehmen|\bnahm|\bnimm)'),
   'Studium absolvieren':     ('studium', r'absolvier'),
   'anspruchsvolles Studium': ('studium', r'anspruchsvoll'),
   'Studie durchführen':      ('studie', r'(durchführ|durchgeführt|durchzuführen|\bführ(e|t|st|te|en|ten)\b)'),
   'Studie auswerten':        ('studie', r'(auswert|ausgewertet|auszuwerten|\bwert(e|et|est|ete|en|eten)\b)'),
   'Erkenntnis gewinnen':     ('erkenntnis', r'(gewinn|gewonn|gewann)'),
   'Theorie aufstellen':      ('theorie', r'(aufstell|aufgestellt|aufzustellen|\bstell(e|t|st|te|en|ten)\b)'),
   'Theorie überprüfen':      ('theorie', r'überprüf'),
   'Methode anwenden':        ('methode', r'(anwend|angewandt|angewendet|anzuwenden|\bwend(e|et|est|ete|en|eten)\b)'),
   'Bildung fördern':         ('bildung', r'förder'),
   'Forschung betreiben':     ('forschung', r'(betreib|betrieb)'),
   'Unterricht erteilen':     ('unterricht', r'erteil'),
   'Analyse vorlegen':        ('analyse', r'(vorleg|vorgelegt|vorzulegen|\bleg(e|t|st|te|en|ten)\b)'),
   'fundierte Analyse':       ('analyse', r'fundiert'),
   'bewährte Methode':        ('methode', r'bewährt'),
 }, aufgaben=[
   ("Mein Studium", "Erzähl von deinem Studium oder deiner Ausbildung: Wann hast du es aufgenommen, wie hast du es absolviert, und was war daran anspruchsvoll? (50–70 Wörter)", ["Studium aufnehmen", "Studium absolvieren", "anspruchsvolles Studium"]),
   ("Zusammenfassung für Kollegen", "Fasse für dein Team eine Studie zusammen, die dich beeindruckt hat: Wie wurde sie durchgeführt, wie wurde sie ausgewertet, und welche Erkenntnis hat man daraus gewonnen? (50–70 Wörter)", ["Studie durchführen", "Studie auswerten", "Erkenntnis gewinnen"]),
   ("Mini-Dialog: Theorie und Praxis", "Schreib einen Mini-Dialog mit zwei Fragen und zwei Antworten zwischen einer Professorin und einem Doktoranden: Er hat eine Theorie aufgestellt – wie will er sie überprüfen, welche Methode wendet er an? (50–70 Wörter)", ["Theorie aufstellen", "Theorie überprüfen", "Methode anwenden"]),
   ("Geld für Bildung oder Forschung?", "Nimm Stellung: Sollte der Staat eher die Bildung in Schulen fördern oder mehr Forschung betreiben lassen? Wer soll den Unterricht erteilen, wenn die besten Köpfe in die Forschung gehen? (60–80 Wörter)", ["Bildung fördern", "Forschung betreiben", "Unterricht erteilen"]),
   ("Die Analyse", "Schreib der Geschäftsführung eine kurze Mail: Du legst eine fundierte Analyse vor und erklärst, auf welcher bewährten Methode sie beruht. (40–60 Wörter)", ["Analyse vorlegen", "fundierte Analyse", "bewährte Methode"]),
 ]),
 8: dict(thema='Politik & Gesellschaft', radar={
   'Mehrheit erringen':       ('mehrheit', r'(erring|errang|errungen)'),
   'Koalition schmieden':     ('koalition', r'(schmied|geschmiedet)'),
   'Regierung bilden':        ('regierung', r'(\bbild|gebildet)'),
   'überfällige Reform':      ('reform', r'überfällig'),
   'Reform durchsetzen':      ('reform', r'(durchsetz|durchgesetzt|durchzusetzen|\bsetz(e|t|st|te|en|ten)\b)'),
   'Reform blockieren':       ('reform', r'blockier'),
   'Kompromiss suchen':       ('kompromiss', r'(such|gesucht)'),
   'Kompromiss aushandeln':   ('kompromiss', r'(aushandel|ausgehandelt|auszuhandeln|\bhandel(e|t|st|te|n|ten)\b)'),
   'tragfähiger Kompromiss':  ('kompromiss', r'tragfähig'),
   'Debatte anstoßen':        ('debatte', r'(anstoß|angestoßen|anzustoßen|\bst[oö]ß(e|t|st|en)\b|stieß)'),
   'sachliche Debatte':       ('debatte', r'sachlich'),
   'Abstimmung durchführen':  ('abstimmung', r'(durchführ|durchgeführt|durchzuführen|\bführ(e|t|st|te|en|ten)\b)'),
   'Macht erlangen':          ('macht', r'erlang'),
   'Macht ausbauen':          ('macht', r'(ausbau|ausgebaut|auszubauen|\bbau(e|t|st|te|en|ten)\b)'),
   'friedlicher Protest':     ('protest', r'friedlich'),
 }, aufgaben=[
   ("Wahlabend", "Schreib eine kurze Nachrichtenmeldung: Eine Partei hat eine hauchdünne Mehrheit errungen. Welche Koalition wird jetzt geschmiedet, und wann wird die neue Regierung gebildet? (50–70 Wörter)", ["Mehrheit erringen", "Koalition schmieden", "Regierung bilden"]),
   ("Die überfällige Reform", "Welche Reform ist in deinem Land längst überfällig? Erkläre, warum sie bisher nicht durchgesetzt wurde und wer sie blockiert. (50–70 Wörter)", ["überfällige Reform", "Reform durchsetzen", "Reform blockieren"]),
   ("Mini-Dialog: Der Kompromiss", "Schreib einen Mini-Dialog mit zwei Fragen und zwei Antworten zwischen zwei Verhandlungspartnern, die einen Kompromiss suchen: Was handeln sie aus, und ist das Ergebnis tragfähig? (50–70 Wörter)", ["Kompromiss suchen", "Kompromiss aushandeln", "tragfähiger Kompromiss"]),
   ("Mail ans Team", "Schreib deinem Team eine Mail: Du stößt eine sachliche Debatte über ein strittiges Thema an (zum Beispiel Homeoffice-Regeln) und schlägst vor, am Ende eine Abstimmung durchzuführen. (40–60 Wörter)", ["Debatte anstoßen", "sachliche Debatte", "Abstimmung durchführen"]),
   ("Macht und Protest", "Erzähl von einem historischen oder fiktiven Fall: Jemand erlangt die Macht und baut sie Schritt für Schritt aus – bis ein friedlicher Protest alles verändert. (50–70 Wörter)", ["Macht erlangen", "Macht ausbauen", "friedlicher Protest"]),
 ]),
 9: dict(thema='Medien & Kommunikation', radar={
   'Rede vorbereiten':        ('rede', r'(vorbereit|vorzubereiten|\bbereit(e|et|est|ete|en|eten)\b)'),
   'Rede halten':             ('rede', r'(\bhalt|\bhält|\bhielt|gehalten)'),
   'zündende Rede':           ('rede', r'zündend'),
   'Kritik äußern':           ('kritik', r'äußer'),
   'konstruktive Kritik':     ('kritik', r'konstruktiv'),
   'Bericht überprüfen':      ('bericht', r'überprüf'),
   'Beitrag einreichen':      ('beitrag', r'(einreich|eingereicht|einzureichen|\breich(e|t|st|te|en|ten)\b)'),
   'Beitrag veröffentlichen': ('beitrag', r'veröffentlich'),
   'Kritik ernten':           ('kritik', r'(ernt|geerntet)'),
   'Berichterstattung gewährleisten': ('berichterstattung', r'gewährleist'),
   'ausgewogene Berichterstattung':   ('berichterstattung', r'ausgewogen'),
   'Nachricht verbreiten':    ('nachricht', r'verbreit'),
   'Meinung vertreten':       ('meinung', r'vertr(et|itt|at)'),
   'Meinung revidieren':      ('meinung', r'revidier'),
   'kontroverse Diskussion':  ('diskussion', r'kontrovers'),
 }, aufgaben=[
   ("Die Rede", "Du sollst bei einer Firmenfeier eine Rede halten. Beschreib, wie du sie vorbereitest und was sie zu einer zündenden Rede macht – trotz Lampenfieber. (50–70 Wörter)", ["Rede vorbereiten", "Rede halten", "zündende Rede"]),
   ("Konstruktive Kritik", "Schreib einem Kollegen eine kurze Mail: Du äußerst konstruktive Kritik an seinem Bericht und bittest ihn, zwei Punkte noch einmal zu überprüfen. (40–60 Wörter)", ["Kritik äußern", "konstruktive Kritik", "Bericht überprüfen"]),
   ("Mini-Dialog in der Redaktion", "Schreib einen Mini-Dialog mit zwei Fragen und zwei Antworten: Eine Autorin hat einen Beitrag eingereicht. Der Redakteur will ihn veröffentlichen, fürchtet aber, dass er Kritik ernten wird. (50–70 Wörter)", ["Beitrag einreichen", "Beitrag veröffentlichen", "Kritik ernten"]),
   ("Ausgewogene Berichterstattung?", "Nimm Stellung: Können soziale Medien eine ausgewogene Berichterstattung gewährleisten – oder verbreiten sie vor allem Nachrichten, die Aufmerksamkeit bringen? (60–80 Wörter)", ["Berichterstattung gewährleisten", "ausgewogene Berichterstattung", "Nachricht verbreiten"]),
   ("Meinung revidiert", "Erzähl von einer kontroversen Diskussion, in der du eine klare Meinung vertreten hast – und sie später revidiert hast. Was hat dich umgestimmt? (50–70 Wörter)", ["Meinung vertreten", "Meinung revidieren", "kontroverse Diskussion"]),
 ]),
}

CSS_TPL = r'''
        /* ===== SCHREIBWERKSTATT (FB-SCHREIB-KOLLOK) ===== */
        #sec-schreiben { padding: 30px;
          --sw-acc: var(--tx-ACC); --sw-acc-bg: var(--bg-ACC); --sw-acc-bd: var(--bd-ACC); --sw-acc-dark: var(--tx-ACC);
          --sw-card: var(--bg-f8f8f8, var(--bg-fafafa, #f8f8f8)); --sw-input: var(--sf-input, var(--bg-white, #fff));
          --sw-text: var(--tx-333, #333); --sw-text2: var(--tx-555, #555); --sw-muted: var(--tx-777, var(--tx-888, #777)); --sw-muted2: var(--tx-888, #888);
          --sw-line: var(--bd-f0f0f0, var(--bd-e0e0e0, #eee)); --sw-line2: var(--bd-e0e0e0, #e0e0e0); --sw-chip-bg: var(--bg-f0f0f0, var(--bg-ecf0f1, #f0f0f0)); --sw-chip-tx: var(--tx-666, #666);
          --sw-ok: var(--tx-27ae60, #27ae60); --sw-ok-bd: var(--bd-27ae60, #27ae60); --sw-ok-bg: var(--bg-e8f8f0, #e8f8f0);
          --sw-err: var(--tx-e74c3c, #c0392b); --sw-err-bd: var(--bd-e74c3c, #e74c3c); --sw-err-bg: var(--bg-fdeaea, #fdeaea);
          --sw-warn-bg: var(--bg-fef8f0, var(--bg-fff8e1, #fff8e1)); --sw-warn-bd: var(--bd-f0e0d0, #f0d48a); --sw-warn-tx: var(--tx-c0a070, #8a5a00);
          --sw-white: var(--tx-white, #fff); }
        .schreib-name-box { background: var(--sw-warn-bg); border: 1.5px solid var(--sw-warn-bd); border-radius: 10px; padding: 14px 18px; margin-bottom: 18px; }
        .schreib-label { display: block; font-size: 0.88em; color: var(--sw-warn-tx); margin-bottom: 6px; font-weight: 600; }
        .schreib-name { width: 100%; max-width: 320px; padding: 10px 14px; border: 1.5px solid var(--sw-acc-bd); border-radius: 8px; font-family: inherit; font-size: 0.95em; outline: none; background: var(--sw-input); color: var(--sw-text); }
        .schreib-name:focus { border-color: var(--sw-acc); }
        .schreib-name.schreib-name-error { border-color: var(--sw-err-bd); box-shadow: 0 0 0 2px rgba(231,76,60,0.15); animation: schreib-name-shake 0.4s; }
        .shake { animation: schreib-name-shake 0.4s; }
        @keyframes schreib-name-shake { 0%,100%{transform:translateX(0)} 25%{transform:translateX(-4px)} 75%{transform:translateX(4px)} }
        .schreib-aufgabe-karte { background: var(--sw-card); padding: 18px 22px 18px 24px; margin-bottom: 18px; border-radius: 10px; border-left: 4px solid var(--sw-acc); transition: all 0.25s; }
        .schreib-aufgabe-karte.gesendet { background: var(--sw-ok-bg); border-left-color: var(--sw-ok-bd); }
        .schreib-aufgabe-nr { display: inline-block; background: var(--sw-acc-bg); color: var(--sw-white); font-weight: 700; font-size: 0.85em; padding: 2px 10px; border-radius: 12px; margin-right: 8px; vertical-align: middle; }
        .schreib-aufgabe-karte.gesendet .schreib-aufgabe-nr { background: var(--sw-ok-bd); }
        .schreib-aufgabe-titel { font-weight: 700; color: var(--sw-acc-dark); font-size: 1.0em; vertical-align: middle; }
        .schreib-aufgabe-frage { color: var(--sw-text2); font-size: 0.95em; line-height: 1.55; margin: 8px 0 10px; }
        .koll-zeile { display: flex; align-items: center; gap: 8px; flex-wrap: wrap; margin-bottom: 10px; font-size: 0.86em; color: var(--sw-muted); }
        .koll-chip { display: inline-block; padding: 4px 12px; border-radius: 14px; font-weight: 600; font-size: 0.95em; background: var(--sw-chip-bg); color: var(--sw-chip-tx); border: 1.5px solid var(--sw-line2); transition: all .2s; }
        .koll-chip::before { content: '○ '; }
        .koll-chip.ok { background: var(--sw-ok-bg); color: var(--sw-ok); border-color: var(--sw-ok-bd); }
        .koll-chip.ok::before { content: '✓ '; }
        .schreib-mini-textarea {
          width: 100%; min-height: 240px; padding: 14px 16px;
          border: 1.5px solid var(--sw-acc-bd); border-radius: 8px;
          font-family: inherit; font-size: 1.02em; line-height: 1.6;
          outline: none; resize: vertical; background: var(--sw-input); color: var(--sw-text);
        }
        .schreib-mini-textarea:focus { border-color: var(--sw-acc); box-shadow: 0 0 0 2px rgba(0,0,0,0.08); }
        .schreib-mini-footer { display: flex; align-items: center; justify-content: space-between; margin-top: 10px; flex-wrap: wrap; gap: 10px; }
        .schreib-mini-meta { font-size: 0.82em; color: var(--sw-muted2); }
        .schreib-mini-meta strong { color: var(--sw-acc); font-weight: 700; }
        .schreib-mini-status { font-size: 0.82em; color: var(--sw-ok); font-weight: 600; margin-left: 8px; }
        .schreib-mini-status.error { color: var(--sw-err); }
        .schreib-mini-btn { padding: 7px 14px; border-radius: 6px; border: 1.5px solid var(--sw-acc); background: var(--sw-input); color: var(--sw-acc); font-size: 0.85em; font-weight: 600; cursor: pointer; transition: all 0.15s; display: inline-flex; align-items: center; gap: 5px; white-space: nowrap; font-family: inherit; }
        .schreib-mini-btn:hover:not(:disabled) { background: var(--sw-acc-bg); color: var(--sw-white); }
        .schreib-mini-btn:disabled { opacity: 0.55; cursor: not-allowed; }
        .schreib-mini-btn.gesendet { border-color: var(--sw-ok-bd); color: var(--sw-ok); background: var(--sw-ok-bg); }
        .schreib-actions { display: flex; gap: 10px; flex-wrap: wrap; margin-top: 20px; padding-top: 18px; border-top: 1px solid var(--sw-line); }
        .schreib-btn { padding: 10px 20px; border-radius: 8px; border: none; font-size: 0.95em; font-weight: 600; cursor: pointer; transition: all 0.2s; display: inline-flex; align-items: center; gap: 8px; font-family: inherit; }
        .schreib-btn-primary { background: var(--sw-acc-bg); color: var(--sw-white); }
        .schreib-btn-primary:hover:not(:disabled) { filter: brightness(0.92); }
        .schreib-btn-primary:disabled { opacity: .55; cursor: not-allowed; }
        .schreib-btn-ghost { background: transparent; color: var(--sw-acc); border: 1.5px solid var(--sw-acc-bd); }
        .schreib-btn-ghost:hover { background: var(--sw-card); }
        .schreib-status { margin-top: 14px; padding: 12px 16px; border-radius: 8px; font-size: 0.92em; line-height: 1.5; display: none; }
        .schreib-status.success { display: block; background: var(--sw-ok-bg); border-left: 4px solid var(--sw-ok-bd); color: var(--sw-ok); }
        .schreib-status.error { display: block; background: var(--sw-err-bg); border-left: 4px solid var(--sw-err-bd); color: var(--sw-err); }
        .schreib-status.info { display: block; background: var(--sw-card); border-left: 4px solid var(--sw-acc); color: var(--sw-acc-dark); }
        .schreib-fb { display: flex; flex-direction: column; gap: 8px; }
        .schreib-fb-titel { font-weight: 700; font-size: 1em; }
        .schreib-fb-text { color: var(--sw-text2); font-size: 0.92em; line-height: 1.5; }
        .schreib-fb-actions { display: flex; flex-wrap: wrap; gap: 8px; margin-top: 4px; }
        .schreib-fb-btn { display: inline-flex; align-items: center; gap: 6px; padding: 9px 14px; border-radius: 8px; border: 1.5px solid var(--sw-acc); background: var(--sw-input); color: var(--sw-acc); font-size: 0.9em; font-weight: 600; text-decoration: none; cursor: pointer; font-family: inherit; }
        .schreib-fb-btn:hover { background: var(--sw-acc-bg); color: var(--sw-white); }
        .schreib-fb-btn-prim { background: var(--sw-acc-bg); color: var(--sw-white); }
        .schreib-fb-hilfe { color: var(--sw-muted); font-size: 0.86em; font-style: italic; margin-top: 4px; }
        @media (max-width: 600px) { #sec-schreiben { padding: 20px; } .schreib-aufgabe-karte { padding: 14px 14px 14px 16px; } .schreib-name-box { padding: 12px 14px; } }
'''


def karte(nr, titel, frage, kolls):
    chips = ''.join('<span class="koll-chip" id="kr-%d-%d" data-koll="%s">%s</span>' % (nr, i, k, k) for i, k in enumerate(kolls))
    return '''  <div class="schreib-aufgabe-karte">
    <span class="schreib-aufgabe-nr">%d</span><span class="schreib-aufgabe-titel">%s</span>
    <div class="schreib-aufgabe-frage">%s</div>
    <div class="koll-zeile">Verwende: %s</div>
    <textarea class="schreib-mini-textarea" data-aufgabe="%d" data-titel="%s"></textarea>
    <div class="schreib-mini-footer">
      <span class="schreib-mini-meta">Wörter: <strong class="wc-%d">0</strong> &middot; Kollokationen: <strong class="kc-%d">0/%d</strong><span class="schreib-mini-status" id="sw-status-%d"></span></span>
      <button class="schreib-mini-btn" id="sw-send-%d" onclick="schreibSendenEinzeln(%d)">📨 An Frank senden</button>
    </div>
  </div>
''' % (nr, titel, frage, chips, nr, titel, nr, nr, len(kolls), nr, nr, nr)


def html_block(aufgaben):
    return '''
        <!-- ==================== TAB 5: Schreibwerkstatt (FB-SCHREIB-KOLLOK) ==================== -->
        <div class="section" id="sec-schreiben">

            <div class="section-title">📨 Schreibwerkstatt &ndash; Kollokationen in eigenen Texten</div>

  <div class="schreib-name-box">
    <label class="schreib-label" for="sw-name">Bitte, hier deinen Namen eintragen.</label>
    <input type="text" id="sw-name" class="schreib-name" autocomplete="name" required>
  </div>
''' + ''.join(karte(i + 1, *a) for i, a in enumerate(aufgaben)) + '''  <div class="schreib-actions">
    <button class="schreib-btn schreib-btn-primary" id="sw-btn-all" onclick="schreibSendenAlleNochOffenen()">📨 Alle noch nicht gesendeten Antworten schicken</button>
    <button class="schreib-btn schreib-btn-ghost" onclick="schreibKopieren()">📋 Alles kopieren</button>
    <button class="schreib-btn schreib-btn-ghost" onclick="schreibLeeren()">🗑 Zurücksetzen</button>
  </div>
  <div class="schreib-status" id="sw-status"></div>
        </div>

'''


JS_HEAD = r'''
<script>/* FB-SCHREIB-KOLLOK-JS — Schreibwerkstatt mit Kollokations-Radar */
window.lsGet = window.lsGet || function(k){try{return localStorage.getItem(k)}catch(e){return null}};
window.lsSet = window.lsSet || function(k,v){try{localStorage.setItem(k,v)}catch(e){}};
window.lsDel = window.lsDel || function(k){try{localStorage.removeItem(k)}catch(e){}};

var SCHREIB_NAME_KEY      = 'schreibwerkstatt_B2_KOLLOK_T%(T)d_name';
var SCHREIB_KEY_PREFIX    = 'schreibwerkstatt_B2_KOLLOK_T%(T)d_';
var SCHREIB_SENT_PREFIX   = 'schreibwerkstatt_B2_KOLLOK_T%(T)d_sent_';
var FORMSUBMIT_ENDPOINT   = 'https://api.web3forms.com/submit';
var FORMSUBMIT_ACCESS_KEY = 'e96ea83f-67e2-4fff-81df-76fee86a09ff';
var FORMSUBMIT_MAILTO     = 'unterricht@frankburkert-daf.de';
var SCHREIB_LEKTION       = 'B2 – Kollokationen Teil %(T)d · %(THEMA)s';
var SCHREIB_CODE          = 'B2 Kollokationen T%(T)d';
var SCHREIB_MIN_CHARS     = 14;

// Kollokations-Radar (locker): Nomen-Stamm UND Verb-/Adjektiv-Stamm irgendwo im Text — flektionstolerant.
// Nur Hilfe für den Lerner, blockiert den Versand nie. Korrektur macht Frank.
var KOLL_RADAR = {
%(RADAR)s
};
'''

HERE = os.path.dirname(os.path.abspath(__file__))
JS_BODY = open(os.path.join(HERE, 'schreib_kollok_body.js'), encoding='utf-8').read()


def js_str(s):
    return s.replace('\\', '\\\\').replace("'", "\\'")


def inject(path, T):
    c = CONF[T]
    s = open(path, encoding='utf-8').read()
    assert 'id="sec-schreiben"' not in s, path + ': schon eingebaut'
    acc = re.search(r'\.section-title \{[^}]*color: var\(--tx-([0-9a-f]+)\)', s, re.S).group(1)
    for k in ('tx', 'bg', 'bd'):
        assert ('--%s-%s:' % (k, acc)) in s, path + ': Variable fehlt --' + k + '-' + acc
    for _, _, ks in c['aufgaben']:
        for k in ks:
            assert k in c['radar'], 'Radar fehlt: ' + k
    css = CSS_TPL.replace('ACC', acc)
    # 1) CSS vor der .author-footer-Regel
    m = re.search(r'\n(\s*)\.author-footer \{', s); assert m, path + ': footer-CSS'
    s = s[:m.start()] + css + s[m.start():]
    # 2) Nav-Button nach „Sprechen"
    m = re.search(r'<div class="nav-btn" onclick="showSection\(4\)">.*?</div>', s); assert m, path + ': nav'
    s = s[:m.end()] + '\n            <div class="nav-btn" onclick="showSection(5)">📨 Schreibwerkstatt</div>' + s[m.end():]
    # 3) Section vor dem Footer
    foot = '<div class="author-footer">'; assert s.count(foot) == 1, path + ': footer'
    i = s.index(foot); j = s.rfind('\n', 0, i) + 1
    s = s[:j] + html_block(c['aufgaben']) + s[j:]
    # 4) JS vor </body>
    assert s.count('</body>') == 1, path + ': body'
    radar = ',\n'.join("  '%s': { n: '%s', v: '%s' }" % (js_str(k), js_str(n), js_str(v)) for k, (n, v) in c['radar'].items())
    js = JS_HEAD % dict(T=T, THEMA=c['thema'], RADAR=radar) + JS_BODY
    s = s.replace('</body>', js + '</body>')
    open(path, 'w', encoding='utf-8').write(s)
    print('ok', path, 'acc=' + acc)


if __name__ == '__main__':
    for arg in sys.argv[1:]:
        T = int(re.search(r'teil(\d)', arg).group(1))
        inject(arg, T)
