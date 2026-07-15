#!/usr/bin/env python3
"""check_gender.py — Gate: kein Gendern (Frank-Regel, generisches Maskulinum).

Blockiert Commits, die geschlechtergerechte Sprache WIEDER einführen. Fängt die
drei zuverlässig maschinell erkennbaren Klassen — hohe Präzision, damit ein
grüner Commit nie fälschlich blockiert wird:

  1. GENDER-ZEICHEN   Lehrer:innen, Lehrer*innen, Lehrer_innen, Lehrer/innen,
                      Lehrer:in, SchülerInnen (Binnen-I).
  2. DOPPELNENNUNG    „Xinnen und/oder X" bzw. „X und/oder Xinnen"
                      (Lehrerinnen und Lehrer, Kolleginnen oder Kollegen,
                      Patientinnen und Patienten).
  3. PARTIZIP-NEUSCHÖPFUNG  Studierende, Teilnehmende, Mitarbeitende, Lernende,
                      Lehrende, Forschende, Pflegende, Sprechende, Helfende,
                      Zuhörende, Kunstschaffende, Vortragende, Mitwirkende.
                      → generisches Maskulinum (Studenten, Teilnehmer, …).

BEWUSST NICHT gefangen (kein Regex kann das trennen, sonst Fehlalarm-Flut):
  · „Reisende" — Franks Entscheidung: korrektes Standarddeutsch, kein Gendern.
  · Alleinstehende weibliche Generika („die Lehrerinnen" statt „die Lehrer").
    Das ist von echten Frauen-Bezügen (Marie Curie, Näherinnen, Königinnen)
    nur inhaltlich unterscheidbar → Mensch- und Skill-Ebene (daf-kern-Skills,
    Memory feedback_kein-gendern). Beim Erstellen/Migrieren mitdenken.

ALLOWLIST — Dateien, in denen Genderformen der GEGENSTAND sind (Erwähnung,
nicht Verwendung); dort dürfen die Formen stehen:
  · DE_C1_3064S-sprache-gesellschaft.html   (Text ÜBER die Genderdebatte)
  · DE_AMDP_000-sprachhinweis.html          (Anti-Gender-Erklärseite m. Formen-Tabelle)
  · DE_B2_1021X-kurze-literarische-textsorten.html  („sprechende Tiere" = Partizip-Adjektiv)
Neue Ausnahme nötig? Bewusst hier eintragen — die Reibung ist gewollt.

Aufruf:
    python3 scripts/check_gender.py            # ganzes Repo
    python3 scripts/check_gender.py a.html b/  # einzelne Dateien/Ordner
Exit 0 = sauber. Exit 1 = Befunde (Commit blockiert).
"""
import os
import re
import sys

SKIP_DIRS = {'daf-archiv', '.git', 'node_modules', 'backup', 'quelltexte'}
ALLOWLIST = {
    'DE_C1_3064S-sprache-gesellschaft.html',
    'DE_AMDP_000-sprachhinweis.html',
    'DE_B2_1021X-kurze-literarische-textsorten.html',
}

# 1) Gender-Zeichen: Buchstabe + : * _ + in/innen (auch In/Innen); Slash-Form; Binnen-I.
# Slash-Form nur mit großgeschriebenem Nomen-Stamm, sonst Fehlalarm auf
# Richtungsadverbien („unten/innen", „außen/innen" = innen als Adverb).
RE_ZEICHEN = re.compile(r'[A-Za-zäöüß][:*_][Ii]nnen\b|[A-Za-zäöüß][:*_][Ii]n\b|\b[A-ZÄÖÜ][A-Za-zäöüß]+/-?innen\b')
RE_BINNENI = re.compile(r'\b[A-ZÄÖÜ]?[a-zäöüß]{2,}Innen\b')

# 2) Doppelnennung mit gemeinsamem/parallelem Stamm.
STOP_INNEN = {'Prinzessinnen', 'Beginnen', 'Gewinnen', 'Spinnen', 'Rinnen', 'Sinnen', 'Minen'}
RE_DOPP_FWD = re.compile(r'\b([A-ZÄÖÜ][a-zäöüß]{2,}innen)\s+(?:und|oder|bzw\.?)\s+[A-ZÄÖÜ][a-zäöüß]')
RE_DOPP_REV = re.compile(r'\b[A-ZÄÖÜ][a-zäöüß]{2,}\s+(?:und|oder|bzw\.?)\s+([A-ZÄÖÜ][a-zäöüß]{2,}innen)\b')

# 3) Partizip-Neuschöpfungen (nominal). Reisende bewusst NICHT enthalten.
RE_PARTIZIP = re.compile(
    r'\b(Studierende[nr]?|Teilnehmende[nr]?|Mitarbeitende[nr]?|Lernende[nr]?|'
    r'Lehrende[nr]?|Forschende[nr]?|Pflegende[nr]?|Sprechende[nr]?|Helfende[nr]?|'
    r'Zuhörende[nr]?|Kunstschaffende[nr]?|Vortragende[nr]?|Mitwirkende[nr]?)\b')


def html_files(paths):
    if not paths:
        paths = ['.']
    for p in paths:
        if os.path.isfile(p):
            yield p
            continue
        for root, dirs, files in os.walk(p):
            dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
            for f in files:
                if f.endswith('.html'):
                    yield os.path.join(root, f)


def scan(text):
    """Gibt Liste (klasse, treffer) für eine Datei zurück."""
    hits = []
    for m in RE_ZEICHEN.finditer(text):
        hits.append(('Zeichen', m.group(0)))
    for m in RE_BINNENI.finditer(text):
        hits.append(('Binnen-I', m.group(0)))
    for m in RE_DOPP_FWD.finditer(text):
        if m.group(1) not in STOP_INNEN:
            hits.append(('Doppelform', m.group(0)))
    for m in RE_DOPP_REV.finditer(text):
        if m.group(1) not in STOP_INNEN:
            hits.append(('Doppelform', m.group(0)))
    for m in RE_PARTIZIP.finditer(text):
        hits.append(('Partizip', m.group(0)))
    return hits


def main(argv):
    findings = []  # (path, [(klasse, treffer), …])
    for path in html_files(argv):
        if os.path.basename(path) in ALLOWLIST:
            continue
        try:
            text = open(path, encoding='utf-8').read()
        except (OSError, UnicodeDecodeError):
            continue
        hits = scan(text)
        if hits:
            findings.append((path, hits))
    if not findings:
        print('✓ Kein Gendern — Zeichen, Doppelnennung und Partizipformen sauber '
              '(generisches Maskulinum).')
        return 0
    total = sum(len(h) for _, h in findings)
    print(f'✗ {len(findings)} Datei(en) mit Genderformen ({total} Treffer) — Commit blockiert:')
    for path, hits in sorted(findings, key=lambda x: -len(x[1])):
        seen = []
        for kl, tr in hits:
            tag = f'{kl}: {tr.strip()[:40]}'
            if tag not in seen:
                seen.append(tag)
        print(f'  {path}')
        for tag in seen[:6]:
            print(f'        {tag}')
    print('\nFix: generisches Maskulinum (Studenten, Lehrer, Teilnehmer …); '
          'Doppelform/Zeichen streichen. Echte Frauen-Bezüge sind hier NICHT '
          'betroffen — die fängt das Gate bewusst nicht. Legitime Ausnahme '
          '(Genderform als Gegenstand)? In ALLOWLIST von check_gender.py eintragen.')
    return 1


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
