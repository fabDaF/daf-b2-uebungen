#!/usr/bin/env python3
"""
nav_lib.py — geteilte Wahrheit für den kanonischen Nav-Header (Variante C: Aktiv-Pille).

Quelle der Wahrheit für PRÜFER (check_nav.py) UND NORMALISIERER (fix_nav.py),
damit beide nie auseinanderdriften — analog zu schreib_pad_lib.py.

Variante C (von Frank am 2026-06-30 gewählt):
  - Emoji ÜBER dem Wort (flex-direction: column)
  - Tabs als abgerundete Pillen auf hellem Lila-Band
  - Aktiver Tab = weiße Pille mit weichem Schatten (KEIN Unterstrich)
  - nav-emoji 1.3em, nav-label 0.78em
"""
import re

CANONICAL_NAV_CSS = """/* ===== NAV (Variante C: Aktiv-Pille) ===== */
.nav {
  display: flex; flex-wrap: wrap; gap: 4px;
  background: #eef0fb; padding: 6px;
  border-bottom: 2px solid #e9ecef;
}
.nav-btn {
  flex: 1 1 auto; min-width: 64px; padding: 12px 8px;
  border: none; background: none; cursor: pointer;
  font-weight: 500; color: #666; transition: all 0.2s; border-radius: 10px;
  display: flex; flex-direction: column; align-items: center; justify-content: center;
}
.nav-btn:hover { background: #e1e5fb; color: #667eea; }
.nav-btn.active { background: #fff; color: #667eea; font-weight: 700; box-shadow: 0 1px 4px rgba(102,126,234,.25); }
.nav-emoji { font-size: 1.3em; line-height: 1.2; }
.nav-label { font-size: 0.78em; margin-top: 2px; line-height: 1.2; }"""

# Die Ziel-Selektoren, die der Nav-Block kontrolliert. .nav-btn.schreib-last
# (order:99 — funktionale Tab-Reihenfolge) wird ABSICHTLICH NICHT angefasst.
_RULE_PATTERNS = [
    (r'\.nav\s*\{[^}]*\}',            'nav'),
    (r'\.nav-btn\s*\{[^}]*\}',        'nav-btn'),
    (r'\.nav-btn:hover\s*\{[^}]*\}',  'nav-btn:hover'),
    (r'\.nav-btn\.active\s*\{[^}]*\}','nav-btn.active'),
    (r'\.nav-btn:last-child\s*\{[^}]*\}', 'nav-btn:last-child'),
    # Nachfahren-Schreibweise mit erfassen (`.nav-btn .nav-emoji { … }`), damit
    # die Regel GANZ verschwindet statt nur ab `.nav-emoji` — sonst bleibt
    # `.nav-btn` als verwaiste Zeile stehen (Fund 2026-08-24, siehe
    # _starts_a_rule).
    (r'(?:\.nav-btn(?:\.[\w-]+)?(?::[\w-]+)?\s+)?\.nav-emoji\s*\{[^}]*\}', 'nav-emoji'),
    (r'(?:\.nav-btn(?:\.[\w-]+)?(?::[\w-]+)?\s+)?\.nav-label\s*\{[^}]*\}', 'nav-label'),
]
_NAV_COMMENT = re.compile(r'/\*\s*=+\s*NAV\b[^*]*\*/', re.I)


_TRAILING_COMMENT = re.compile(r'/\*.*?\*/\s*$', re.S)


def _starts_a_rule(text, pos):
    """
    True, wenn an Position `pos` wirklich eine NEUE Regel beginnt — und der
    Selektor nicht bloß der letzte Teil eines Nachfahren-Selektors ist.

    Warum das nötig ist (Fund 2026-08-24, B1 1012G mitten im Unterricht):
    `\\.nav-label\\s*\\{[^}]*\\}` matcht auch INNERHALB von
    `.nav-btn .nav-label { … }`. Wurde dieser Treffer entfernt, blieb die
    nackte Zeile `.nav-btn` stehen. Für den Browser ist das kein Fehler,
    sondern der Anfang eines Selektors: er liest weiter bis zur nächsten `{`
    und macht daraus `.nav-btn .section` — damit war `.section{display:none}`
    verschluckt und ALLE Tabs standen gleichzeitig untereinander.
    """
    vorher = text[:pos]
    # Kommentare und Leerraum rückwärts überspringen.
    while True:
        gekuerzt = vorher.rstrip()
        neu = _TRAILING_COMMENT.sub('', gekuerzt)
        if neu == gekuerzt:
            vorher = gekuerzt
            break
        vorher = neu
    # '\x00' ist der Platzhalter, den normalize() für den kanonischen Block
    # einsetzt — er steht für eine bereits abgeschlossene Regel.
    return (not vorher) or vorher[-1] in '}{;>\x00'


def _rule_body(text, selector_regex):
    for m in re.finditer(selector_regex, text):
        if _starts_a_rule(text, m.start()):
            return m.group(0)
    return None


def _sub_rules(pattern, ersatz, text, limit=0):
    """
    Wie re.sub, ersetzt aber NUR Treffer, die eine Regel anfangen.
    Rückgabe: (neuer_text, anzahl_ersetzungen).
    """
    out = []
    pos = 0
    n = 0
    for m in re.finditer(pattern, text):
        if m.start() < pos:
            continue
        if not _starts_a_rule(text, m.start()):
            continue
        out.append(text[pos:m.start()])
        out.append(ersatz)
        pos = m.end()
        n += 1
        if limit and n >= limit:
            break
    out.append(text[pos:])
    return ''.join(out), n


def verify(text):
    """Gibt eine Liste von Problemen zurück. Leere Liste = konform zu Variante C."""
    problems = []

    base = _rule_body(text, r'\.nav-btn\s*\{[^}]*\}')
    if not base:
        problems.append('Keine .nav-btn-Basisregel gefunden (Layout unbekannt).')
    else:
        base_ns = base.replace(' ', '')
        if 'flex-direction:column' not in base_ns:
            problems.append('.nav-btn ohne flex-direction:column — Emoji steht NEBEN statt ÜBER dem Wort.')
        if 'border-radius' not in base_ns:
            problems.append('.nav-btn ohne border-radius — keine Pillen.')

    active = _rule_body(text, r'\.nav-btn\.active\s*\{[^}]*\}')
    if not active:
        problems.append('Keine .nav-btn.active-Regel gefunden.')
    else:
        if 'box-shadow' not in active:
            problems.append('.nav-btn.active ohne box-shadow — keine Aktiv-Pille.')
        if 'border-bottom' in active:
            problems.append('.nav-btn.active mit border-bottom — das ist die alte Unterstrich-Variante, nicht die Pille.')

    nav = _rule_body(text, r'\.nav\s*\{[^}]*\}')
    if not nav:
        problems.append('Keine .nav-Regel gefunden.')
    elif 'padding' not in nav:
        problems.append('.nav ohne padding — kein Pillen-Band.')

    emoji = _rule_body(text, r'\.nav-emoji\s*\{[^}]*\}')
    if not emoji:
        problems.append('Keine .nav-emoji-Regel — Emoji-Größe undefiniert.')
    elif '1.3em' not in emoji:
        problems.append('.nav-emoji nicht 1.3em.')

    label = _rule_body(text, r'\.nav-label\s*\{[^}]*\}')
    if not label:
        problems.append('Keine .nav-label-Regel — Label-Größe undefiniert.')
    elif '0.78em' not in label and '.78em' not in label:
        problems.append('.nav-label nicht 0.78em.')

    return problems


def normalize(text):
    """
    Ersetzt den gesamten Nav-Block durch CANONICAL_NAV_CSS — generationsrobust
    und idempotent. Lässt .nav-btn.schreib-last und sonstige Extras unberührt.

    Rückgabe: (neuer_text, changed_bool, grund_str)
    Bricht sicher ab (changed=False), wenn keine .nav-btn-Basisregel existiert.
    """
    if not _rule_body(text, r'\.nav-btn\s*\{[^}]*\}'):
        return text, False, 'Keine .nav-btn-Basisregel — Layout unbekannt, nichts geändert.'

    work = text

    # Anker: Position der ersten relevanten Regel (für korrekte Einfügung).
    anchor_re = r'\.nav\s*\{[^}]*\}'
    if not _rule_body(work, anchor_re):
        anchor_re = r'\.nav-btn\s*\{[^}]*\}'

    PLACEHOLDER = '\x00NAV_CANON\x00'
    work, n = _sub_rules(anchor_re, PLACEHOLDER, work, limit=1)
    if n == 0:
        return text, False, 'Anker nicht ersetzbar — nichts geändert.'

    # Alle übrigen Ziel-Regeln und alte NAV-Kommentare entfernen — jeweils
    # INKLUSIVE des nachfolgenden Zeilenumbruchs, damit keine verwaisten
    # Leerzeilen zurückbleiben. So bleibt der Diff chirurgisch: NUR der
    # Nav-Block ändert sich, der Rest der Datei (auch Leerzeilen) bleibt unberührt.
    #
    # WICHTIG: Es wird ausschließlich entfernt, was eine Regel ANFÄNGT
    # (_starts_a_rule). Ein Treffer mitten in einem Nachfahren-Selektor würde
    # sonst nur das hintere Stück wegschneiden und den vorderen Selektor als
    # verwaiste Zeile zurücklassen — die verschluckt dann die Folgeregel.
    for pat, _name in _RULE_PATTERNS:
        work, _ = _sub_rules(pat + r'[ \t]*\r?\n?', '', work)
    work = re.sub(_NAV_COMMENT.pattern + r'[ \t]*\r?\n?', '', work, flags=re.I)

    # Platzhalter durch den kanonischen Block ersetzen.
    work = work.replace(PLACEHOLDER, CANONICAL_NAV_CSS, 1)

    # KEINE globale Leerzeilen-Glättung — die würde Zeilen außerhalb des
    # Nav-Blocks anfassen und den Diff unnötig aufblähen (nicht chirurgisch).

    changed = (work != text)
    return work, changed, ('Nav auf Variante C normalisiert.' if changed else 'Bereits kanonisch.')


if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        t = open(sys.argv[1], encoding='utf-8').read()
        print('PROBLEMS:', verify(t))
