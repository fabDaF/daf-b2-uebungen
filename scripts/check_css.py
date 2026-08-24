#!/usr/bin/env python3
"""check_css.py — CSS-Struktur-Gate: verwaiste Selektoren und verwaiste Deklarationen.

Warum es dieses Gate gibt (Fund 2026-08-24, B1 1012G mitten im Unterricht):
Ein Injektor hatte eine Regel `.nav-btn .nav-label { … }` per Regex entfernt,
aber nur den TEIL ab `.nav-label` — zurück blieb die nackte Zeile

    .nav-btn

Für den Browser ist das kein Fehler, sondern der ANFANG eines Selektors: er
liest weiter bis zur nächsten `{` und macht daraus `.nav-btn .section`. Damit
war `.section { display: none }` verschluckt — ALLE Tabs standen gleichzeitig
untereinander. Kein einziges bestehendes Gate hat das gesehen: die Datei war
syntaktisch gültig, JS-frei von Fehlern, alle check_*-Skripte grün.

Zwei Defektklassen, beide „gültiges CSS mit falscher Bedeutung":

  A) VERWAISTER SELEKTOR — ein Selektor läuft über einen Zeilenumbruch,
     ohne dass die Vorzeile mit `,` endet. Das ist fast immer ein Rest, den
     ein Regex-Reparateur stehen gelassen hat, und verschluckt die Folgeregel.
  B) VERWAISTE DEKLARATION — Deklarationen (`foo: bar;`) stehen auf
     Verschachtelungstiefe 0, also außerhalb jeder Regel. Dann wurde ein
     Selektor samt Klammern weggeschnitten; die Formatierung ist tot.

Nutzung:
    python3 scripts/check_css.py                # ganzes Repo (ohne daf-archiv)
    python3 scripts/check_css.py datei.html …   # einzelne Dateien
Exit 1, sobald ein Treffer existiert.
"""
import os
import re
import sys

STYLE_RE = re.compile(r'<style[^>]*>(.*?)</style>', re.S | re.I)
COMMENT_RE = re.compile(r'/\*.*?\*/', re.S)
DECL_RE = re.compile(r'^\s*[-a-zA-Z][-a-zA-Z0-9]*\s*:\s*[^;{}]+;\s*$')
SKIP_DIRS = {'daf-archiv', '_to_delete', 'node_modules', '.git', 'backup'}

# Stand 2026-08-24: Klasse A (verwaister Selektor) hat Backlog 0 und blockiert.
#
# Nur für Klasse B (verwaiste Deklaration). Diese beiden Dateien sind seit
# ihrem ALLERERSTEN Commit so — der Generator hat damals die Selektoren samt
# Klammern der „Figuren-Karten" verloren, es gibt also keine heile Fassung in
# der Historie, aus der man sie zurückholen könnte. Die Deklarationen sind
# wirkungslos (tote Formatierung), aber sie zu erraten wäre Erfindung. Die
# Dateien stehen deshalb bewusst hier, damit das Gate für die gefährliche
# Klasse A (verwaister Selektor, verschluckt die Folgeregel) sofort blockierend
# laufen kann. Beide sind inhaltlich dieselbe Genus-Übung.
# Am 2026-08-24 wurde der abgeschnittene zweite <head>-Block (unschließbares
# <style>) aus beiden Dateien entfernt; die selektorlosen Deklarationsgruppen im
# verbliebenen echten Stylesheet bleiben. Welche Klasse zu welcher Gruppe gehört,
# steht nirgends — Raten wäre Erfindung.
# → Aufräumen heißt: die Figuren-Karten-CSS neu schreiben, dann hier streichen.
ALLOWLIST_DEKLARATION = {
    'htmlS/A1.1 NEW/DE_A1_1000G-der-die-das-genus.html',
    'daf-materialien/Grundlagen/Grammatik/genus-training.html',
}


def _allowlisted(path):
    norm = os.path.normpath(path).replace(os.sep, '/')
    return any(norm.endswith(a) for a in ALLOWLIST_DEKLARATION)


def _strip_comments(css):
    """Kommentare entfernen, Zeilennummern erhalten."""
    return COMMENT_RE.sub(lambda m: '\n' * m.group(0).count('\n'), css)


def scan(path):
    """Gibt eine Liste (zeile, art, text) zurück. Leer = sauber."""
    try:
        text = open(path, encoding='utf-8', errors='replace').read()
    except OSError:
        return []
    findings = []
    for block in STYLE_RE.finditer(text):
        css = _strip_comments(block.group(1))
        base = text.count('\n', 0, block.start(1)) + 1
        depth = 0
        buf = ''
        buf_at = 0
        for i, ch in enumerate(css):
            if ch == '{':
                if depth == 0:
                    sel = buf.strip()
                    lines = [l.strip() for l in sel.split('\n') if l.strip()]
                    if len(lines) > 1 and not all(l.endswith(',') for l in lines[:-1]):
                        ln = base + css.count('\n', 0, buf_at)
                        findings.append((ln, 'verwaister Selektor',
                                         ' ⏎ '.join(lines)[:110]))
                    buf = ''
                depth += 1
            elif ch == '}':
                depth = max(0, depth - 1)
                if depth == 0:
                    buf = ''
                    buf_at = i + 1
            elif depth == 0:
                if ch == ';':
                    kandidat = buf.strip()
                    if DECL_RE.match(kandidat + ';'):
                        ln = base + css.count('\n', 0, buf_at)
                        findings.append((ln, 'verwaiste Deklaration',
                                         (kandidat + ';')[:110]))
                    buf = ''
                    buf_at = i + 1
                else:
                    if not buf.strip():
                        buf_at = i
                    buf += ch
    return findings


def collect_repo():
    out = []
    for dp, dn, fn in os.walk('.'):
        dn[:] = [d for d in dn if d not in SKIP_DIRS]
        for f in fn:
            if f.endswith('.html') and '.bak' not in f:
                out.append(os.path.join(dp, f))
    return sorted(out)


def main():
    files = [f for f in sys.argv[1:] if f.endswith('.html')] or collect_repo()
    total = 0
    for f in files:
        erlaubt = _allowlisted(f)
        for ln, art, txt in scan(f):
            if art == 'verwaiste Deklaration' and erlaubt:
                continue
            total += 1
            print(f"✗ {f}:{ln}  {art}: {txt}")
    if total:
        print(f"\n✗ {total} CSS-Struktur-Fehler — "
              f"verwaiste Selektoren verschlucken die Folgeregel.")
        sys.exit(1)
    print(f"✓ CSS-Struktur sauber ({len(files)} Datei(en)).")
    sys.exit(0)


if __name__ == '__main__':
    main()
