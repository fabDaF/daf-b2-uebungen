#!/usr/bin/env python3
"""check_lueckentext.py — strenges Gate für die KANONISCHE Lückentext-Form.

Kanonische Form (mit Frank 2026-06-30 abgenommen, Piloten 1057X + 3065G):
  - zusammenhängende STORY (durchlaufender Serif-Fließtext mit Inline-Lücken),
    KEINE isolierten Einzelsätze, KEINE Nummerierung;
  - Serifenschrift im Fließtext inkl. Eingabefelder;
  - §7-Wortbank (gemischt, nicht klickbar, .used-Durchstreichen);
  - case-sensitives Live-Feedback, kein Prüfen-Button;
  - GENAU 10 Lücken;
  - Variante V/R/X: Wortbank = Vollformen (data-answer);
  - Variante G: Wortbank = Grundform (data-base), Zielform nie sichtbar.

Marker der kanonischen Engine/CSS: FB-LT-STORY.

Anders als das alte, permissive check_wortbank.py (das JEDE Wort-Hilfe durchwinkte)
erzwingt dieses Gate GENAU EINE Form. Jede Abweichung ist ein Treffer.

Nutzung:
    python3 scripts/check_lueckentext.py            # ganzes Repo (ohne daf-archiv)
    python3 scripts/check_lueckentext.py datei.html # einzelne Dateien
    python3 scripts/check_lueckentext.py --inventur # nur Inventur-Übersicht, Exit 0

Exit-Code 1, wenn KANONISCHE Dateien Verstöße haben (Pre-Commit-Gate).
Nicht-kanonische Altbestände werden als Backlog GEZÄHLT, lösen aber für sich
allein keinen Fehler aus (sie werden im Rollout Spur A/B abgearbeitet) — außer
mit --strict.
"""
import os
import re
import sys

# Lückentext-Tab vorhanden? (auch HTML-entity-kodiert: L&uuml;ckentext)
TAB_RE = re.compile(
    r'nav-label[^>]*>\s*L(?:ü|&uuml;)ckentext'
    r'|<(?:h2|div)[^>]*>\s*[^<]*L(?:ü|&uuml;)ckentext', re.I)

MARKER = "FB-LT-STORY"
# konkurrierende Alt-Engines
COMPETITORS = ("FB-WORTBANK-MODULE", "FB-LT-V1")
GAP_RE = re.compile(r'<input\s+class="blank"\s+data-answer="([^"]*)"([^>]*)>')
GFILE_RE = re.compile(r'_\d{4}G[-_.]')
NUM_RE = re.compile(r'class="luecken-story"[^>]*>(.*?)</div>\s*(?:</div>|<!--)', re.S)


def gaps(s):
    return GAP_RE.findall(s)


def has_numbering(s):
    # <ol> in der Story oder führende "1. " Nummern in den Story-Absätzen
    m = re.search(r'class="luecken-story".*?</div>\s*</div>', s, re.S)
    region = m.group(0) if m else s
    if re.search(r'<ol\b', region):
        return True
    if re.search(r'<p>\s*\d+\.\s', region):
        return True
    return False


def check_canonical(path, s):
    """Liefert Liste von Verstoß-Strings für eine FB-LT-STORY-Datei."""
    problems = []
    g = gaps(s)
    n = len(g)
    if n != 10:
        problems.append(f"{n} Lücken (kanonisch sind GENAU 10)")
    if has_numbering(s):
        problems.append("Nummerierung in der Story (verboten)")
    for c in COMPETITORS:
        if c in s:
            problems.append(f"konkurrierende Alt-Engine vorhanden: {c}")
    if 'class="wortkasten"' in s:
        problems.append("statischer wortkasten vorhanden (Leak-/Doppelbank-Gefahr)")
    # G-Variante: jede Lücke braucht data-base; Zielform nie über Wortbank sichtbar
    is_g = bool(GFILE_RE.search(os.path.basename(path)))
    with_base = sum(1 for _, rest in g if "data-base=" in rest)
    if is_g or (0 < with_base < n):
        if with_base != n:
            problems.append(f"G-Variante: {with_base}/{n} Lücken mit data-base "
                            f"(alle brauchen die Grundform)")
    return problems


def scan(paths):
    canonical_ok = []
    canonical_bad = []   # (problems, path)
    backlog = []         # Lückentext-Tab, aber noch nicht kanonisch
    for p in paths:
        try:
            s = open(p, encoding="utf-8", errors="replace").read()
        except OSError:
            continue
        if not TAB_RE.search(s):
            continue
        if MARKER not in s:
            backlog.append(p)
            continue
        probs = check_canonical(p, s)
        if probs:
            canonical_bad.append((probs, p))
        else:
            canonical_ok.append(p)
    return canonical_ok, canonical_bad, backlog


def collect_repo():
    out = []
    for dp, dn, fn in os.walk("."):
        if "/daf-archiv" in dp or "/.git" in dp:
            continue
        for f in fn:
            if f.endswith(".html") and ".bak" not in f:
                out.append(os.path.join(dp, f))
    return out


def level_of(p):
    b = os.path.basename(p)
    m = re.search(r'DE_(A1|A2|B1|B2|C1|C2)_', b)
    if m:
        return m.group(1)
    for lvl in ("A1", "A2", "B1", "B2", "C1", "C2"):
        if f"/{lvl}" in p or f"{lvl}." in p:
            return lvl
    return "?"


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    flags = {a for a in sys.argv[1:] if a.startswith("--")}
    files = args if args else collect_repo()
    ok, bad, backlog = scan(files)

    total = len(ok) + len(bad) + len(backlog)
    print(f"Lückentext-Inventur: {total} Dateien mit Lückentext-Tab")
    print(f"  ✓ kanonisch (FB-LT-STORY, konform): {len(ok)}")
    print(f"  ✗ kanonisch, aber fehlerhaft:        {len(bad)}")
    print(f"  ⧗ Backlog (noch nicht kanonisch):    {len(backlog)}")

    # Backlog pro Niveau (= Rollout-Umfang)
    if backlog:
        per = {}
        for p in backlog:
            per[level_of(p)] = per.get(level_of(p), 0) + 1
        order = sorted(per.items())
        print("    Backlog pro Niveau: " + ", ".join(f"{k}={v}" for k, v in order))

    if bad:
        print("\nFehlerhafte kanonische Dateien:")
        for probs, p in bad:
            print(f"  ✗ {p}")
            for pr in probs:
                print(f"       - {pr}")

    if "--inventur" in flags:
        sys.exit(0)

    # Gate: kanonische Dateien MÜSSEN konform sein. Backlog blockt nur mit --strict.
    fail = bool(bad) or ("--strict" in flags and bool(backlog))
    sys.exit(1 if fail else 0)
