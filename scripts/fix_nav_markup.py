#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""fix_nav_markup.py — bringt das Nav-HTML auf Variante C (Emoji/Label in Spans).

fix_nav.py normalisiert nur das Nav-CSS. Ältere Lektionen tragen das Label aber
noch als Fließtext im Button:

    <div class="nav-btn" onclick="showSection(3)">✏️ Lückentext</div>

Variante C (daf-kern §1) verlangt zwei Spans:

    <div class="nav-btn" onclick="showSection(3)"><span class="nav-emoji">✏️</span><span class="nav-label">Lückentext</span></div>

Ohne diese Spans greifen add_wortschatz_tab.py und inject_sprech_wortschatz.py
nicht (sie suchen den Schreiben-Button über <span class="nav-label">).

  python3 scripts/fix_nav_markup.py DATEI.html [DATEI2.html ...]
  python3 scripts/fix_nav_markup.py --check DATEI.html

Idempotent: Buttons, die die Spans schon haben, bleiben unberührt. Buttons mit
anderem Innenleben (verschachteltes Markup) werden übersprungen, nicht geraten.
"""
import re
import sys

# <div|button class="nav-btn …" …>INHALT</div|button> — Inhalt ohne Tags
BTN = re.compile(
    r'(<(div|button)\s+class="nav-btn[^"]*"[^>]*>)([^<]+)(</\2>)'
)


def _split(inhalt):
    """Trennt führendes Emoji vom Label. Gibt (emoji, label) oder None."""
    s = inhalt.strip()
    if not s or ' ' not in s:
        return None
    emoji, label = s.split(' ', 1)
    label = label.strip()
    # Das erste Stück muss ein Emoji sein, kein Wort — sonst nicht anfassen.
    if not emoji or emoji[0].isalnum() or not label:
        return None
    return emoji, label


# <div class="tab-nav"> — Altname des Nav-Containers. fix_nav.py spielt die
# kanonische .nav-Regel ins CSS, fasst das HTML aber nicht an; traegt der
# Container weiter tab-nav, greift die Pillen-Optik gar nicht (Fund 2026-10-26
# an 7 B2-Lektionen). Nur umbenennen, wenn eine .nav-Regel wirklich da ist.
TABNAV_HTML = re.compile(r'<(div|nav)(\s+)class="tab-nav"')
TABNAV_CSS = re.compile(r'^\.tab-nav\s*\{[^}]*\}\n?', re.M)
NAV_REGEL = re.compile(r'^\.nav\s*\{', re.M)


def nav_container(t):
    """tab-nav -> nav, samt toter .tab-nav-Regel. Gibt (text, geaendert)."""
    if not TABNAV_HTML.search(t) or not NAV_REGEL.search(t):
        return t, False
    t = TABNAV_HTML.sub(r'<\1\2class="nav"', t)
    t = TABNAV_CSS.sub('', t)
    return t, True


def transform(t):
    treffer = []

    def ersetze(m):
        auf, _tag, inhalt, zu = m.groups()
        teile = _split(inhalt)
        if not teile:
            return m.group(0)
        emoji, label = teile
        treffer.append(label)
        return (f'{auf}<span class="nav-emoji">{emoji}</span>'
                f'<span class="nav-label">{label}</span>{zu}')

    t = BTN.sub(ersetze, t)
    t, umbenannt = nav_container(t)
    if umbenannt:
        treffer.append('Container tab-nav->nav')
    return t, treffer


def main(argv):
    args = argv[1:]
    dry = False
    if args and args[0] == '--check':
        dry, args = True, args[1:]
    if not args:
        print('Usage: fix_nav_markup.py [--check] DATEI.html ...')
        return 2

    geaendert = 0
    for f in args:
        try:
            text = open(f, encoding='utf-8').read()
        except OSError as e:
            print(f'  ?? {f}: {e}')
            continue
        neu, treffer = transform(text)
        if not treffer:
            print(f'  – {f}: bereits kanonisch oder kein Alt-Nav.')
            continue
        geaendert += 1
        if dry:
            print(f'  ~ {f}: würde {len(treffer)} Button(s) umbauen ({", ".join(treffer)})')
            continue
        open(f, 'w', encoding='utf-8').write(neu)
        print(f'  ✓ {f}: {len(treffer)} Button(s) auf Variante C ({", ".join(treffer)})')

    print(f'\n{geaendert} geändert, {len(args) - geaendert} unberührt.')
    return 1 if (dry and geaendert) else 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
