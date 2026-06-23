#!/usr/bin/env python3
"""
schreib_pad_lib.py — gemeinsame Erkennungslogik für die Schreibwerkstatt-Padding-Regel.

Hintergrund (daf-kern §1 / daf-lesetext): Der Inhalt jedes Tabs muss vom
Container-Rand eingerückt sein. Der Schreibwerkstatt-Patcher hängte den Tab aber
lange als nackte Section ohne Innen-Padding an. Folge: Name-Box, Aufgaben-Karten
und Textareas kleben randlos am Container, das Layout wirkt „an den Rand
gequetscht". Frank am 2026-06-19 und erneut am 2026-06-23 (A2 2014R) gemeldet.

Diese Datei ist die EINE Quelle der Wahrheit für „Was ist der Schreibwerkstatt-
Tab?" und „Ist sein Inhalt eingerückt?". Prüfer (check_schreib_pad.py) und
Reparateur (inject_schreib_pad.py) importieren sie — so können sie nie
auseinanderdriften.

WICHTIG — zwei reale Tab-Architekturen:
  * R/X/V/W/C-Dateien: Tabs sind `<div class="section">`, und `.section` hat
    KEIN Padding (`.section { display:none }`). Der Inhalt wird über einen
    `.sec-inner`-Wrapper (padding 28px 30px) eingerückt — fehlt der, klebt er.
  * G-Dateien: Tabs sind `<section class="section">`, und `.section` trägt das
    Padding selbst (`.section { display:none; padding: 28px 30px }`). Hier ist
    der Schreibwerkstatt-Tab AUTOMATISCH eingerückt — kein Bug.

Ein Schreibwerkstatt-Tab ist also korrekt eingerückt, wenn EINES gilt:
  (a) sein Inhalt liegt in einem `.sec-inner`-Wrapper, ODER
  (b) eine CSS-Regel `#<sid> { … padding … }` gibt der Section Padding
      (der FB-SCHREIB-PAD-Fix), ODER
  (c) eine Klassen-Regel des Containers (z. B. `.section { padding: … }`) gibt
      ihm horizontales Padding.
Sonst -> OFFENDER.
"""
import re

_SEC_INNER = re.compile(
    r'<div\b[^>]*\bclass="[^"]*(?<![-\w])sec-inner(?![-\w])[^"]*"', re.I)

# Default-Tab-Klassen (falls eine Datei keine display:none-Regel hat).
_DEFAULT_TAB_CLASSES = ('section', 'tab-content', 'tabcontent', 'tab-pane')


def _tab_classes(t: str):
    """Klassen, die im CSS eine `display:none`-Regel tragen = Tab-Container.

    Robust über Architekturen: R/X/V/W/C nutzen `.section`, G nutzt `.section`
    (als <section>), B1 teils `.tab-content`. Statt eine Klasse zu raten, lesen
    wir sie aus dem Stylesheet."""
    css = _style_css(t)
    found = set()
    for m in re.finditer(r'(?<![-\w.])\.([\w-]+)\s*\{([^{}]*)\}', css):
        if re.search(r'display\s*:\s*none', m.group(2), re.I):
            found.add(m.group(1))
    found.update(_DEFAULT_TAB_CLASSES)
    return found


def _sec_open_re(tab_classes):
    """Open-Tag-Regex für <div>/<section> mit einem der Tab-Klassen-Tokens."""
    alt = '|'.join(re.escape(c) for c in sorted(tab_classes, key=len, reverse=True))
    return re.compile(
        r'<(?:div|section)\b[^>]*\bclass="[^"]*(?<![-\w])(?:' + alt +
        r')(?![-\w])[^"]*"[^>]*>', re.I)

# Im Section-Segment sichtbare Marker, die NUR der Schreibwerkstatt-Tab trägt.
_SIG = re.compile(
    r'class="schreib-name-box"'
    r'|class="schreib-aufgabe'
    r'|class="schreib-mini-textarea"'
    r'|📨\s*Schreibwerkstatt',
    re.I,
)


def _attr(tag: str, name: str):
    m = re.search(name + r'="([^"]*)"', tag)
    return m.group(1) if m else None


def _style_css(t: str) -> str:
    return '\n'.join(re.findall(r'<style[^>]*>(.*?)</style>', t, re.S | re.I))


def find_schreib_section(t: str):
    """Liefert (tag, sid, seg) des Schreibwerkstatt-Tabs oder (None, None, None).

    tag = vollständiges Open-Tag des Containers (für class/id)
    sid = id-Attribut des Containers (z. B. 'sec-schreib', 'sec-5', 'tab-schreib')
    seg = HTML vom Container-Open bis zur nächsten Section bzw. Dateiende
    """
    opens = list(_sec_open_re(_tab_classes(t)).finditer(t))
    if not opens:
        return None, None, None
    starts = [m.start() for m in opens] + [len(t)]
    for i, m in enumerate(opens):
        seg = t[starts[i]:starts[i + 1]]
        if _SIG.search(seg):
            return m.group(0), _attr(m.group(0), 'id'), seg
    return None, None, None


def _has_horizontal_padding(value: str) -> bool:
    """True, wenn ein padding-Wert horizontal (links/rechts) > 0 ist."""
    toks = value.strip().split()
    if not toks:
        return False
    def nz(tok):  # nonzero length token
        return bool(re.search(r'[1-9]', tok))
    if len(toks) == 1:
        return nz(toks[0])
    if len(toks) == 2:
        return nz(toks[1])            # vertical horizontal
    if len(toks) == 3:
        return nz(toks[1])            # top horizontal bottom
    return nz(toks[1]) or nz(toks[3])  # top right bottom left


def _class_pads(css: str, classes) -> bool:
    """True, wenn irgendeine Klasse des Containers horizontales Padding setzt."""
    for c in classes:
        if c in ('active', 'aktiv'):
            continue
        for body in re.findall(
                r'(?<![-\w.])\.' + re.escape(c) + r'(?![-\w])\s*\{([^{}]*)\}', css):
            for m in re.finditer(r'padding(-left|-right)?\s*:\s*([^;}]+)', body):
                side, val = m.group(1), m.group(2)
                if side in ('-left', '-right'):
                    if re.search(r'[1-9]', val):
                        return True
                elif _has_horizontal_padding(val):
                    return True
    return False


def is_padded(t: str, tag, sid, seg) -> bool:
    """True, wenn der Schreibwerkstatt-Inhalt vom Container-Rand eingerückt ist."""
    if seg is None:
        return True  # kein Schreibwerkstatt-Tab -> nichts zu prüfen
    # (a) Inhalt in .sec-inner-Wrapper
    if _SEC_INNER.search(seg):
        return True
    # (b) CSS-Regel gibt der Section per id horizontales Padding (FB-SCHREIB-PAD)
    if sid and re.search(r'(?<![-\w])#' + re.escape(sid) + r'\s*\{[^}]*padding', t):
        return True
    # (c) eine Klassen-Regel des Containers gibt ihm horizontales Padding
    classes = (_attr(tag, 'class') or '').split()
    if _class_pads(_style_css(t), classes):
        return True
    return False


def classify(t: str):
    """Liefert ('ok'|'offender'|'no-id'|'none', sid)."""
    tag, sid, seg = find_schreib_section(t)
    if seg is None:
        return 'none', None
    if is_padded(t, tag, sid, seg):
        return 'ok', sid
    if not sid:
        return 'no-id', None
    return 'offender', sid
