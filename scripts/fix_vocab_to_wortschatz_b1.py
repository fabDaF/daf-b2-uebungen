#!/usr/bin/env python3
"""fix_vocab_to_wortschatz_b1.py — Phase 1, Skript 2.

Migriert in B1-Alt-Dateien die Wortschatz-Implementierung:
  - HTML-Container-ID  vocabContainer  → wortschatzContainer
  - JS-Funktion initVocab        → initWortschatz (komplett ersetzt)
  - JS-Funktion vocabLiveCheck   → wortschatzCheck
  - JS-Funktion checkVocabAllDone → checkWortschatzAllOk
  - Calls initVocab() → initWortschatz()
  - CSS .vocab-* / #vocabContainer entfernt, neue WORTSCHATZ-CSS eingefügt
  - Datenvariable WORTSCHATZ bleibt — Format ist identisch
  - State-Variable var wortschatzInited = false; hinzugefügt

Pro Datei:
  - Tab-Index aus altem timerAutoStart(N) ermitteln (Default 4)
  - Pre-Sanity, Migration, Post-Sanity
  - Bei Sanity-Fehler: REVERT, log skip

Aufruf:
    python3 scripts/fix_vocab_to_wortschatz_b1.py --dry-run [DATEI ...]
    python3 scripts/fix_vocab_to_wortschatz_b1.py [DATEI ...]
"""
from __future__ import annotations
import argparse
import glob
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

# ════════════════════════════════════════════════════════════════════
# NEUE Komponenten (Template aus Pilot 3064X)
# ════════════════════════════════════════════════════════════════════

NEU_CSS = """\
/* ── WORTSCHATZ (Phase 1.2) ── */
#wortschatzContainer { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; }
#wortschatzContainer .luecke-item { background: #f8f9ff; padding: 12px 14px; border-radius: 10px; border-left: 4px solid #667eea; display: flex; flex-direction: column; gap: 6px; margin-bottom: 0; }
.ws-en { font-weight: 600; color: #764ba2; font-size: 0.93em; }
.ws-inputs { display: flex; gap: 6px; align-items: center; flex-wrap: wrap; width: 100%; }
.ws-inputs input.blank { min-width: auto; }
.ws-inputs input.art    { width: 70px; flex-shrink: 0; }
.ws-inputs input.wort   { flex: 1; min-width: 150px; }
.ws-inputs input.plural { width: 130px; flex-shrink: 0; }
.ws-inputs input.verb   { flex: 1; min-width: 200px; }
@media (max-width: 700px) { #wortschatzContainer { grid-template-columns: 1fr; } }
"""

NEU_JS_TEMPLATE = """\
var wortschatzInited = false;

function initWortschatz() {
    if (wortschatzInited) return;
    var cont = document.getElementById('wortschatzContainer');
    if (!cont) return;
    cont.innerHTML = '';
    WORTSCHATZ.forEach(function(w, i) {
        var row = document.createElement('div');
        row.className = 'luecke-item';
        var en = '<div class="ws-en">' + w.en + '</div>';
        var inputs;
        if (w.type === 'n') {
            inputs = '<div class="ws-inputs">' +
                '<input class="blank art"    data-id="' + i + '" data-field="artikel" placeholder="Artikel" oninput="wortschatzCheck(this)" autocomplete="off">' +
                '<input class="blank wort"   data-id="' + i + '" data-field="de"      placeholder="Wort"    oninput="wortschatzCheck(this)" autocomplete="off">' +
                '<input class="blank plural" data-id="' + i + '" data-field="plural"  placeholder="Plural"  oninput="wortschatzCheck(this)" autocomplete="off">' +
                '</div>';
        } else {
            inputs = '<div class="ws-inputs">' +
                '<input class="blank verb" data-id="' + i + '" data-field="de" placeholder="Verb (Infinitiv)" oninput="wortschatzCheck(this)" autocomplete="off">' +
                '</div>';
        }
        row.innerHTML = en + inputs;
        cont.appendChild(row);
    });
    wortschatzInited = true;
}

function wortschatzCheck(inp) {
    if (typeof timerAutoStart === 'function') timerAutoStart(__TAB_N__);
    var id = parseInt(inp.dataset.id);
    var field = inp.dataset.field;
    var target = WORTSCHATZ[id][field];
    var val = inp.value.trim();
    inp.classList.remove('ok', 'wrong');
    if (!val) return;
    if (val === target) {
        inp.classList.add('ok');
        checkWortschatzAllOk();
    } else if (!target.toLowerCase().startsWith(val.toLowerCase())) {
        inp.classList.add('wrong');
    }
}

function checkWortschatzAllOk() {
    var all = document.querySelectorAll('#wortschatzContainer input.blank');
    var allOk = Array.from(all).every(function(i) { return i.classList.contains('ok'); });
    if (allOk && typeof stopTimer === 'function') stopTimer(__TAB_N__);
}

function resetWortschatz() {
    document.querySelectorAll('#wortschatzContainer input.blank').forEach(function(inp) {
        inp.value = '';
        inp.classList.remove('ok', 'wrong');
    });
}

function showLoesungWortschatz() {
    document.querySelectorAll('#wortschatzContainer input.blank').forEach(function(inp) {
        var id = parseInt(inp.dataset.id);
        var field = inp.dataset.field;
        inp.value = WORTSCHATZ[id][field];
        inp.classList.remove('wrong');
        inp.classList.add('ok');
    });
}
"""


# ════════════════════════════════════════════════════════════════════
# Helpers
# ════════════════════════════════════════════════════════════════════

def extract_func(src: str, fname: str) -> tuple[int, int] | None:
    """Findet `function fname(...) { ... }` und gibt (start, end) zurück."""
    sig = f'function {fname}'
    idx = src.find(sig)
    if idx == -1:
        return None
    # Brace-Matching
    brace_start = src.find('{', idx)
    if brace_start == -1:
        return None
    depth = 1
    i = brace_start + 1
    while depth > 0 and i < len(src):
        ch = src[i]
        if ch == '{':
            depth += 1
        elif ch == '}':
            depth -= 1
        elif ch == '/' and i + 1 < len(src) and src[i+1] == '/':
            # Zeilenkommentar überspringen
            i = src.find('\n', i)
            if i == -1: i = len(src)
        elif ch == '/' and i + 1 < len(src) and src[i+1] == '*':
            # Blockkommentar überspringen
            i = src.find('*/', i + 2)
            if i == -1: i = len(src)
            else: i += 2
            continue
        elif ch in ('"', "'", '`'):
            # String überspringen
            quote = ch
            i += 1
            while i < len(src) and src[i] != quote:
                if src[i] == '\\':
                    i += 2
                else:
                    i += 1
        i += 1
    return (idx, i)


def detect_tab_n(src: str) -> int:
    """Tab-Index aus altem timerAutoStart(N) ermitteln."""
    # Strategie 1: in vocabLiveCheck-Body
    for fname in ('vocabLiveCheck', 'initVocab', 'checkVocabAllDone'):
        bounds = extract_func(src, fname)
        if bounds:
            body = src[bounds[0]:bounds[1]]
            m = re.search(r'timerAutoStart\((\d+)\)', body)
            if m:
                return int(m.group(1))
    return 4  # Default


def remove_old_vocab_css(src: str) -> tuple[str, int]:
    """Entferne alle Zeilen, die alte vocab-* CSS-Regeln sind.

    Eine alte CSS-Regel ist eine Zeile mit:
      .vocab-item, .vocab-en, .vocab-arrow, .vocab-inputs, .vocab-hint,
      #vocabContainer
    NICHT: .vocab-hl, .vocab-card, .vocab-grid, .vocab-term, .vocab-def
    (das sind separate, nicht zu Wortschatz-Drill gehörende Klassen)

    Auch @media-Wrapper für vocab-* werden entfernt.
    """
    # Erlaubte vocab-* Klassen (bleiben unangetastet)
    SAFE = {'vocab-hl', 'vocab-card', 'vocab-grid', 'vocab-term',
            'vocab-def', 'vocab-wort'}
    lines = src.split('\n')
    out = []
    removed = 0
    skip_next_media = False
    for line in lines:
        # Ist diese Zeile eine vocab-Item-CSS-Regel?
        # Prüfe: Selektoren, die wir entfernen wollen
        targets = re.findall(r'(\.vocab-[a-z]+|#vocabContainer)\b', line)
        if not targets:
            out.append(line)
            continue
        # Sind ALLE Targets in der Zeile zu entfernen?
        bad = [t for t in targets if not any(s in t for s in SAFE)]
        if not bad:
            # Nur erlaubte vocab-* — Zeile behalten
            out.append(line)
            continue
        # Diese Zeile hat mind. einen "bad" Selektor.
        # Nur entfernen, wenn die Zeile eine self-contained CSS-Regel ist
        stripped = line.strip()
        if (stripped.startswith(('.vocab-', '#vocab', '@media')) or
                stripped.startswith('input.vocab') or
                '.vocab-' in stripped[:60]):
            # One-line CSS-Regel oder @media-Wrapper
            if '{' in stripped and '}' in stripped:
                # Self-contained
                removed += 1
                continue
        # Sonst: konservativ behalten, log Warnung später möglich
        out.append(line)
    return '\n'.join(out), removed


def remove_old_vocab_js(src: str) -> tuple[str, int]:
    """Entferne alle alten Wortschatz-JS-Funktionen."""
    removed = 0
    for fname in ('initVocab', 'vocabLiveCheck', 'checkVocabAllDone',
                  'showVocabLoesung', 'resetVocab'):
        bounds = extract_func(src, fname)
        if bounds:
            src = src[:bounds[0]] + src[bounds[1]:]
            removed += 1
    # Auch State-Variable
    src = re.sub(r'\s*var vocabInited[^;]*;\s*', '\n', src)
    return src, removed


def insert_new_components(src: str, tab_n: int) -> str:
    """Füge NEU-CSS und NEU-JS in src ein.

    CSS: vor `</style>`
    JS: vor `</script>` (letztes)
    """
    # CSS einfügen
    css_pos = src.rfind('</style>')
    if css_pos == -1:
        return src
    src = src[:css_pos] + NEU_CSS + src[css_pos:]

    # JS einfügen
    js = NEU_JS_TEMPLATE.replace('__TAB_N__', str(tab_n))
    js_pos = src.rfind('</script>')
    if js_pos == -1:
        return src
    src = src[:js_pos] + js + src[js_pos:]
    return src


def rename_calls_and_container(src: str) -> str:
    """Container-ID umbenennen + Calls umbenennen."""
    # HTML-Container-ID
    src = re.sub(r'\bid="vocabContainer"', 'id="wortschatzContainer"', src)
    # JS-Calls (nur das Identifier-Replacement, NICHT die Funktionsdefinition)
    src = re.sub(r'\binitVocab\s*\(\s*\)', 'initWortschatz()', src)
    src = re.sub(r'\bshowVocabLoesung\s*\(\s*\)', 'showLoesungWortschatz()', src)
    src = re.sub(r'\bresetVocab\s*\(\s*\)', 'resetWortschatz()', src)
    src = re.sub(r'\bvocabLiveCheck\b', 'wortschatzCheck', src)
    src = re.sub(r'\bcheckVocabAllDone\s*\(\s*\)', 'checkWortschatzAllOk()', src)
    # JS-String-Selektoren mit #vocabContainer (in querySelectorAll/getElementById)
    src = re.sub(r"#vocabContainer\b", '#wortschatzContainer', src)
    return src


def sanity_check(orig: str, new: str) -> tuple[bool, str]:
    """Sanity-Checks: was muss in der NEUEN Datei vorhanden/abwesend sein?"""
    # MUSS vorhanden sein:
    must_have = [
        'function initWortschatz',
        'function wortschatzCheck',
        'function checkWortschatzAllOk',
        'var wortschatzInited',
        'id="wortschatzContainer"',
        '.luecke-item',
        '.ws-en',
        '.ws-inputs',
    ]
    for m in must_have:
        if m not in new:
            return False, f"fehlt: {m}"

    # MUSS abwesend sein (außer in Kommentaren):
    must_not = [
        'function initVocab(',
        'function vocabLiveCheck(',
        'function checkVocabAllDone(',
        'function showVocabLoesung(',
        'function resetVocab(',
        'id="vocabContainer"',
        '#vocabContainer',
        'vocabLiveCheck(',
        'checkVocabAllDone(',
        'showVocabLoesung(',
        'resetVocab(',
    ]
    for m in must_not:
        if m in new:
            return False, f"nicht entfernt: {m}"

    # Tag-Count: NEU darf nicht weniger Tags haben als ALT
    import re as _re
    TAG = _re.compile(r'<[a-zA-Z][a-zA-Z0-9]*')
    orig_tags = len(TAG.findall(orig))
    new_tags = len(TAG.findall(new))
    if new_tags < orig_tags - 5:  # toleranz, weil HTML-Container etwas verkleinert wird
        return False, f"Tag-Verlust: {orig_tags} → {new_tags}"

    return True, "ok"


def process(path: Path, dry_run: bool) -> tuple[str, str]:
    """Returns (status, message). Status: 'changed', 'skipped', 'noop'."""
    orig = path.read_text(encoding='utf-8')
    # 1. Pre-Check: Hat die Datei überhaupt eine alte Implementation?
    if 'function initVocab(' not in orig:
        return 'noop', 'keine initVocab-Funktion'
    if 'function initWortschatz' in orig:
        return 'noop', 'bereits migriert'

    # 2. Tab-N ermitteln
    tab_n = detect_tab_n(orig)

    # 3. Migration
    src = orig
    src, css_removed = remove_old_vocab_css(src)
    src, js_removed = remove_old_vocab_js(src)
    src = insert_new_components(src, tab_n)
    src = rename_calls_and_container(src)

    # 4. Sanity-Check
    ok, msg = sanity_check(orig, src)
    if not ok:
        return 'skipped', f"sanity-fail: {msg}"

    # 5. Schreiben
    if not dry_run:
        path.write_text(src, encoding='utf-8')
    return 'changed', f"Tab-N={tab_n}, css_removed={css_removed}, js_removed={js_removed}"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--dry-run', action='store_true')
    ap.add_argument('files', nargs='*')
    args = ap.parse_args()

    if args.files:
        files = [Path(f) for f in args.files]
    else:
        pattern = str(REPO_ROOT / 'htmlS' / 'B1.1' / 'DE_B1_*.html')
        files = sorted(Path(p) for p in glob.glob(pattern))

    if not files:
        print('Keine Dateien gefunden.', file=sys.stderr)
        return 1

    changed = skipped = noop = 0
    skipped_files = []
    for f in files:
        status, msg = process(f, dry_run=args.dry_run)
        try:
            display = f.resolve().relative_to(REPO_ROOT)
        except ValueError:
            display = f
        if status == 'changed':
            changed += 1
            print(f'  ✓  {display}  ({msg})')
        elif status == 'skipped':
            skipped += 1
            skipped_files.append((str(display), msg))
        elif status == 'noop':
            noop += 1

    verb = 'würden migriert' if args.dry_run else 'migriert'
    print(f'\n{changed} Dateien {verb}, {skipped} skipped, {noop} unverändert (no-op).')
    if skipped_files:
        print('\nSKIPPED:')
        for f, m in skipped_files:
            print(f'  ✗  {f}  →  {m}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
