#!/usr/bin/env python3
"""
inject_genus_tail.py — Genus-Tab für die HETEROGENEN Rest-Lektionen, deren
Tab-Mechanik vom Standard (showSection/showTab + .section) abweicht.

Liest die Tab-Umschaltfunktion, die Container-Klasse und den Dispatch
(Index vs. id) DIREKT AUS DEM CODE der Datei und hängt Genus IMMER als
LETZTEN Tab an. Wiederverwendet BANNER/CSS/section_html/js_block aus
inject_genus.py, damit Optik und Verhalten identisch bleiben.

  python3 scripts/inject_genus_tail.py DATEI.html woerter.json

Bricht sicher ab (Exit 2), wenn keine eindeutige Tab-Funktion erkennbar ist
— dann NICHTS geschrieben. Idempotent: vorhandener Genus-Tab -> Skip (Exit 0).
Pflicht-Gate bleibt: node scripts/clicktest_genus_only.js DATEI.html
"""
import re, sys, json, os
from collections import Counter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import inject_genus as IG


def find_tab_fn(t):
    """Funktion, die von Nav-Buttons mit Integer-Argument gerufen wird UND
    im Körper die TABS umschaltet. Zur Abgrenzung von z. B. selectMC (toggelt
    auch classList) muss der Körper auch die NAV-Leiste anfassen
    (nav-btn / .nav / querySelectorAll('.nav...'))."""
    calls = re.findall(r'onclick="([A-Za-z_]\w*)\(\s*[\'"\d]', t)
    for name, _ in Counter(calls).most_common():
        m = re.search(r'function\s+' + re.escape(name) + r'\s*\([^)]*\)\s*\{', t)
        if not m:
            continue
        body = t[m.end():m.end() + 600]
        if 'classList' not in body:
            continue
        if not ('querySelectorAll' in body or 'getElementById' in body):
            continue
        if not re.search(r"nav-btn|tab-btn|\.nav\b|querySelectorAll\(\s*['\"]\.nav", body):
            continue
        return name, body
    return None, None


def detect_container(body):
    """Container-Klasse = erste querySelectorAll('.X')-Klasse, die NICHT die
    Nav-Leiste ist (nav/nav-btn). Fallback 'section'."""
    for cls in re.findall(r"querySelectorAll\(\s*['\"]\.([A-Za-z][\w-]*)", body):
        if cls in ('nav', 'nav-btn', 'tab-btn') or cls.startswith('nav'):
            continue
        return cls
    return 'section'


def main():
    if len(sys.argv) != 3:
        print("Aufruf: inject_genus_tail.py DATEI.html woerter.json"); sys.exit(1)
    path, wjson = sys.argv[1], sys.argv[2]
    words = json.load(open(wjson, encoding='utf-8'))
    if len(words) < 20 or any(w["cat"] not in ("der", "die", "das", "pl") for w in words):
        print("ABBRUCH: woerter.json braucht >=20 Einträge, cat in der/die/das/pl"); sys.exit(2)
    forms = [w["word"] for w in words]
    if len(set(forms)) != len(forms):
        print("ABBRUCH: doppelte Wortformen:", sorted({x for x in forms if forms.count(x) > 1})); sys.exit(2)

    t = open(path, encoding='utf-8').read()

    if IG.genus_cats(t) & {"der", "die", "das", "pl"}:
        print("SKIP (hat schon Genus-Tab):", path); sys.exit(0)
    if 'id="genusPool"' in t or re.search(r'function\s+initGenus\b', t) or re.search(r'\bGENUS_DATA\s*=', t):
        print("SKIP (hat schon genus-Code/genusPool/GENUS_DATA):", path); sys.exit(0)

    fn, body = find_tab_fn(t)
    if not fn:
        print("ABBRUCH (keine Tab-Funktion erkennbar):", path); sys.exit(2)

    # Dispatch + Container-Klasse aus dem Funktionskörper lesen
    idm = re.search(r"getElementById\(\s*['\"]([A-Za-z]+-?)['\"]\s*\+", body)
    id_based = bool(idm)
    id_prefix = idm.group(1) if idm else 'sec-'
    container = detect_container(body)

    # Manche Generationen rufen die Tab-Funktion mit einer STRING-id auf
    # (onclick="show('genus', this)" + getElementById('tab-'+id)) statt mit einem
    # Integer-Index. Beide Spielarten unterstützen.
    str_mode = bool(re.search(r'onclick="' + re.escape(fn) + r"\(\s*'", t))

    if str_mode:
        nav_re = re.compile(r'<(\w+)([^>]*onclick="' + re.escape(fn) + r"\('[^']*'[^\"]*\"[^>]*)>(.*?)</\1>", re.S)
    else:
        nav_re = re.compile(r'<(\w+)([^>]*onclick="' + re.escape(fn) + r'\(\d+[^"]*"[^>]*)>(.*?)</\1>', re.S)
    navs = list(nav_re.finditer(t))
    if not navs:
        print("ABBRUCH (keine Tab-Nav):", path); sys.exit(2)

    container_re = (r'<(?:div|section)\b[^>]*\bclass="(?:[^"]*\s)?'
                    + re.escape(container) + r'(?:\s[^"]*)?"[^>]*>')
    n_containers = len(re.findall(container_re, t))

    if str_mode:
        # String-id: feste id 'genus'
        sec_id = (id_prefix + 'genus') if id_based else 'sec-genus'
    else:
        nums = []
        for m in navs:
            mm = re.search(r'onclick="' + re.escape(fn) + r'\((\d+)', m.group(0))
            if mm:
                nums.append(int(mm.group(1)))
        # Index-basierte Dispatch (querySelectorAll('.container')[idx]) indexiert in die
        # DOM-Reihenfolge der Container — NICHT in die Nav-Nummern. Bei vorbestehenden
        # Defekten (Orphan-Tab ohne Nav, doppelte showTab-Nummer) divergieren beide.
        # Der angehängte Genus-Container landet an DOM-Index = Anzahl bisheriger Container.
        if id_based:
            genus_idx = (max(nums) + 1) if nums else len(navs)
        else:
            genus_idx = n_containers
        sec_id = (id_prefix + str(genus_idx)) if id_based else "sec-genus"

    # Genus-Nav aus letztem Nav-Button klonen (Emoji+Label tauschen, Nummer/id setzen)
    def make_genus_nav(src):
        g = src.group(0)
        g = re.sub(r'&#1\d{4,5};|[\U0001F300-\U0001FAFF]', '🏷️', g, count=1)
        if 'nav-label' in g:
            g = re.sub(r'(<span[^>]*class="[^"]*nav-label[^"]*"[^>]*>).*?(</span>)', r'\1Genus\2', g, count=1, flags=re.S)
        else:
            g2 = re.sub(r'(🏷️\s*)[^<]*', r'\1Genus', g, count=1)
            g = g2 if g2 != g else re.sub(r'(>)[^<]*(</)', r'\1🏷️ Genus\2', g, count=1)
        if str_mode:
            g = re.sub(r'(onclick="' + re.escape(fn) + r"\()'[^']*'", lambda m: m.group(1) + "'genus'", g, count=1)
        else:
            g = re.sub(r'(onclick="' + re.escape(fn) + r'\()\d+', lambda m: m.group(1) + str(genus_idx), g, count=1)
        return g

    gnav = make_genus_nav(navs[-1])
    t = t[:navs[-1].end()] + "\n        " + gnav + t[navs[-1].end():]

    # Container-Elemente finden (Klasse als eigenes Token)
    secs = list(re.finditer(container_re, t))
    if not secs:
        print("ABBRUCH (keine Container '%s'):" % container, path); sys.exit(2)

    # Genus-Section HINTER dem schließenden Tag des letzten Containers (Tag-Balancing)
    sm0 = secs[-1]
    tag = re.match(r'<(\w+)', sm0.group(0)).group(1)
    opens = [(m.start(), 1) for m in re.compile(r'<' + tag + r'\b', re.I).finditer(t, sm0.start())]
    closes = [(m.end(), -1) for m in re.compile(r'</' + tag + r'\s*>', re.I).finditer(t, sm0.start())]
    depth = 0; insert_at = None
    for at, delta in sorted(opens + closes):
        depth += delta
        if depth == 0:
            insert_at = at; break
    if insert_at is None:
        insert_at = len(t)

    has_help = 'help-box' in t
    has_ctrl = 'control-bar' in t
    idxs = [int(x) for x in re.findall(r'id="timer-(\d+)"', t)]
    timer_idx = (max(idxs) + 1) if idxs else 6

    sec = IG.section_html(words, has_help, has_ctrl, timer_idx, sec_id)
    # Container-Klasse der Genus-Section an die Datei anpassen (z. B. tab-content/sec)
    if container != 'section':
        sec = sec.replace('<div class="section" id="' + sec_id + '">',
                          '<div class="' + container + '" id="' + sec_id + '">', 1)
    t = t[:insert_at] + sec + t[insert_at:]

    # Hardcodierte for-Schleifen-Grenze in der Tab-Funktion ggf. anheben
    navbtn_now = len(re.findall(r'class="nav-btn', t))
    fnm = re.search(r'function\s+' + re.escape(fn) + r'\s*\([^)]*\)\s*\{', t)
    if fnm and navbtn_now > 0:
        b2 = t[fnm.end():fnm.end() + 800]
        lm = re.search(r'for\s*\(\s*var\s+\w+\s*=\s*0\s*;\s*\w+\s*<\s*(\w+)\s*;', b2)
        if lm and lm.group(1).isdigit():
            old = lm.group(0)
            t = t.replace(old, re.sub(r'<\s*' + lm.group(1) + r'\s*;', '< %d;' % navbtn_now, old), 1)

    pos = t.rfind('</style>')
    if pos == -1:
        print("ABBRUCH (kein </style>):", path); sys.exit(2)
    t = t[:pos] + IG.CSS + t[pos:]

    jpos = t.rfind('</script>')
    if jpos == -1:
        print("ABBRUCH (kein </script>):", path); sys.exit(2)
    jpos += len('</script>')
    t = t[:jpos] + IG.js_block(words, timer_idx, sec_id) + t[jpos:]

    open(path, 'w', encoding='utf-8').write(t)
    disp = "'genus'" if str_mode else str(genus_idx)
    print("OK injiziert (fn=%s, container=.%s, %s, idx=%s, sec_id=%s):" %
          (fn, container, "id" if id_based else "index", disp, sec_id), path)


if __name__ == "__main__":
    main()
