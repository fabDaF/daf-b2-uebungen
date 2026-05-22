#!/usr/bin/env python3
"""fix_wordbank_visual_b1.py — Phase 1, Skript 3.

Wortbank klickbar → visuell:
  - `function buildWordBank` komplett ersetzt (Pilot-Version)
    <button> mit click-Handler → <span> ohne click
  - `function insertWordFromBank` entfernt (verwaist)
  - `function syncWordBankChips` hinzugefügt (Pilot)
  - `function lueckeCheck` (sofern alte Logik) durch Pilot-Variante ersetzt
    (case-sensitive Präfix-Check)

Live-Check-Funktionen mit anderen Namen (liveCheck, liveCheckLuecke,
liveCheckLuecken) bleiben UNANGETASTET — die haben separate CSS-Conventions
(.correct statt .ok), das Refactoring wandert in Phase 2.

Pro Datei: Pre-Check, Migration, Post-Sanity. Skip bei Fehlbedarf.
"""
from __future__ import annotations
import argparse
import glob
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

# ════════════════════════════════════════════════════════════════════
# Pilot-Komponenten
# ════════════════════════════════════════════════════════════════════

NEU_BUILD = """\
function buildWordBank(containerEl) {
    if (!containerEl) return;
    lkContainer = containerEl;
    var inputs = Array.from(containerEl.querySelectorAll(
        'input[data-answer], input[data-ans], input.blank, input.l-inp'));
    var seen = {}, words = [];
    inputs.forEach(function(inp) {
        var w = inp.dataset.answer || inp.dataset.ans || '';
        if (w && !seen[w]) { seen[w] = true; words.push(w); }
    });
    if (!words.length) return;
    // Fisher-Yates-Shuffle
    for (var i = words.length - 1; i > 0; i--) {
        var j = Math.floor(Math.random() * (i + 1));
        var t = words[i]; words[i] = words[j]; words[j] = t;
    }
    var bank = document.createElement('div');
    bank.className = 'wort-bank';
    var lbl = document.createElement('div');
    lbl.className = 'wort-bank-label';
    lbl.innerHTML = '🔤 Wortbank – die richtigen Wörter, in zufälliger Reihenfolge.<br>Tipp sie selbst in die Lücken — achte auf Groß- und Kleinschreibung.';
    bank.appendChild(lbl);
    words.forEach(function(w) {
        // KEIN <button> mehr — <span> ist nicht klickbar
        var chip = document.createElement('span');
        chip.className = 'wort-chip';
        chip.textContent = w;
        chip.dataset.word = w;
        bank.appendChild(chip);
    });
    containerEl.insertBefore(bank, containerEl.firstChild);
    // KEIN focusin-/click-Listener mehr — Wortbank ist rein visuell
}"""

NEU_SYNC = """
function syncWordBankChips() {
    // Markiert ein Wort in der Wortbank als "benutzt", sobald es korrekt eingetippt wurde
    if (!lkContainer) return;
    var bank = lkContainer.querySelector('.wort-bank');
    if (!bank) return;
    var solved = {};
    lkContainer.querySelectorAll('input.blank.ok, input.blank.correct, input.l-inp.ok, input[data-ans].ok, input[data-answer].ok').forEach(function(inp) {
        var w = inp.value;
        if (w) solved[w] = true;
    });
    bank.querySelectorAll('.wort-chip').forEach(function(c) {
        c.classList.toggle('used', !!solved[c.dataset.word]);
    });
}
"""

# Ersetz-Variante von lueckeCheck — nur wenn vorhanden UND alte Logik
NEU_LUECKE = """\
function lueckeCheck(inp) {
    if (typeof timerAutoStart === 'function') timerAutoStart(3);
    var val = inp.value;        // KEIN .trim() — Leerzeichen sind Fehler
    var ans = inp.dataset.answer;
    inp.classList.remove('ok', 'wrong');
    if (!val) { syncWordBankChips(); return; }
    if (val === ans) {                   // exakt korrekt → grün
        inp.classList.add('ok');
        if (typeof checkLueckenDone === 'function') checkLueckenDone();
    } else if (!ans.startsWith(val)) {  // case-sensitive Präfix-Check → rot
        inp.classList.add('wrong');
    }
    // Bei korrektem Präfix bleibt das Feld neutral (schwarz).
    syncWordBankChips();
}"""


# ════════════════════════════════════════════════════════════════════
# Helpers
# ════════════════════════════════════════════════════════════════════

def extract_func(src: str, fname: str) -> tuple[int, int] | None:
    sig = f'function {fname}'
    idx = src.find(sig)
    if idx == -1:
        return None
    bs = src.find('{', idx)
    if bs == -1:
        return None
    depth = 1
    i = bs + 1
    while depth > 0 and i < len(src):
        ch = src[i]
        if ch == '{':
            depth += 1
        elif ch == '}':
            depth -= 1
        elif ch == '/' and i + 1 < len(src) and src[i+1] == '/':
            i = src.find('\n', i)
            if i == -1: i = len(src)
        elif ch == '/' and i + 1 < len(src) and src[i+1] == '*':
            i = src.find('*/', i + 2)
            i = (len(src) if i == -1 else i + 2)
            continue
        elif ch in ('"', "'", '`'):
            quote = ch
            i += 1
            while i < len(src) and src[i] != quote:
                if src[i] == '\\':
                    i += 2
                else:
                    i += 1
        i += 1
    return (idx, i)


def replace_func(src: str, fname: str, new_body: str) -> tuple[str, bool]:
    bounds = extract_func(src, fname)
    if bounds is None:
        return src, False
    return src[:bounds[0]] + new_body + src[bounds[1]:], True


def remove_func(src: str, fname: str) -> tuple[str, bool]:
    bounds = extract_func(src, fname)
    if bounds is None:
        return src, False
    # Mit nachfolgenden Leerzeichen/Newlines weg
    end = bounds[1]
    while end < len(src) and src[end] in '\n\t ':
        end += 1
    return src[:bounds[0]] + src[end:], True


def insert_after_func(src: str, after_fname: str, new_code: str) -> str:
    bounds = extract_func(src, after_fname)
    if bounds is None:
        return src
    end = bounds[1]
    return src[:end] + '\n' + new_code + src[end:]


def has_clickable_wordbank(src: str) -> bool:
    """True, wenn die Datei eine klickbare Wortbank hat."""
    if 'function buildWordBank' not in src:
        return False
    bounds = extract_func(src, 'buildWordBank')
    if bounds is None:
        return False
    body = src[bounds[0]:bounds[1]]
    return ('createElement(\'button\')' in body and 'addEventListener' in body) or \
           ('insertWordFromBank' in body)


def luecke_check_is_old(src: str) -> bool:
    """True, wenn lueckeCheck (sofern vorhanden) noch alte Logik nutzt."""
    bounds = extract_func(src, 'lueckeCheck')
    if bounds is None:
        return False
    body = src[bounds[0]:bounds[1]]
    return '.trim()' in body or '.toLowerCase()' in body


def sanity_check(orig: str, new: str) -> tuple[bool, str]:
    # Wenn buildWordBank ersetzt wurde, dürfen keine click-Reste in buildWordBank stehen
    bounds = extract_func(new, 'buildWordBank')
    if bounds:
        body = new[bounds[0]:bounds[1]]
        if 'createElement(\'button\')' in body or 'insertWordFromBank' in body:
            return False, 'buildWordBank hat noch Button/Click-Reste'
        if "addEventListener('click'" in body:
            return False, 'buildWordBank hat noch click-Listener'
    # syncWordBankChips muss vorhanden sein
    if 'function syncWordBankChips' not in new:
        return False, 'syncWordBankChips fehlt'
    # insertWordFromBank muss komplett raus (auch als Call)
    if 'function insertWordFromBank' in new:
        return False, 'insertWordFromBank-Funktion noch da'
    return True, 'ok'


def process(path: Path, dry_run: bool) -> tuple[str, str]:
    orig = path.read_text(encoding='utf-8')

    needs_wb = has_clickable_wordbank(orig)
    needs_lk = luecke_check_is_old(orig)

    if not needs_wb and not needs_lk:
        return 'noop', 'keine Migration nötig'

    src = orig
    parts = []

    if needs_wb:
        src, ok1 = replace_func(src, 'buildWordBank', NEU_BUILD)
        if ok1:
            parts.append('buildWordBank')
        src, ok2 = remove_func(src, 'insertWordFromBank')
        if ok2:
            parts.append('insertWordFromBank entfernt')
        # syncWordBankChips hinzufügen, falls fehlt
        if 'function syncWordBankChips' not in src:
            src = insert_after_func(src, 'buildWordBank', NEU_SYNC)
            parts.append('syncWordBankChips hinzugefügt')

    if needs_lk:
        src, ok3 = replace_func(src, 'lueckeCheck', NEU_LUECKE)
        if ok3:
            parts.append('lueckeCheck')
        # syncWordBankChips für lueckeCheck-Calls
        if 'function syncWordBankChips' not in src:
            src = insert_after_func(src, 'lueckeCheck', NEU_SYNC)
            parts.append('syncWordBankChips')

    # Sanity
    ok, msg = sanity_check(orig, src)
    if not ok:
        return 'skipped', f'sanity-fail: {msg}'

    if not dry_run:
        path.write_text(src, encoding='utf-8')
    return 'changed', ', '.join(parts)


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

    changed = skipped = noop = 0
    skipped_files = []
    for f in files:
        status, msg = process(f, args.dry_run)
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
