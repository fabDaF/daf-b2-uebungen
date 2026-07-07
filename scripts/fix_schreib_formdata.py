#!/usr/bin/env python3
"""
fix_schreib_formdata.py — Schreibwerkstatt-Versand preflight-frei machen.

Problem: Der Versand schickte den Text als JSON mit
`Content-Type: application/json`. Das erzwingt eine CORS-Preflight-Anfrage
(OPTIONS). Firmen-Proxys beantworten OPTIONS oft mit HTTP 405 -> Versand
scheitert, bevor er Web3Forms erreicht.

Fix: Body als FormData (multipart/form-data, ein "simple request" OHNE Custom-
Header) -> KEIN Preflight. Web3Forms akzeptiert FormData nativ.

Transform je Datei (chirurgisch, nur die Sende-fetch-Optionen):
  * In JEDEM fetch(<endpoint>, { ... })-Options-Objekt, das
    'Content-Type': 'application/json' UND JSON.stringify( enthaelt:
      - headers-Eintrag entfernen (die Preflight-Ursache)
      - body: JSON.stringify(OBJ) -> body: schreibToFormData(OBJ)
        (Objektliteral bleibt woertlich; keine Feld-Parsing-Risiken)
  * Einmalig pro Datei den Helper schreibToFormData() vor </script> injizieren.

Wichtig: JSON.stringify wird NUR im Sende-fetch ersetzt, nicht global
(localStorage nutzt JSON.stringify ebenfalls).

Idempotent. JS-Syntaxcheck (node --check) vor dem Speichern.
"""
import re
import sys
import subprocess
from pathlib import Path

HELPER = (
    "\n// Wandelt ein Objekt in FormData: preflight-freier Versand (kein "
    "application/json-Header, keine CORS-OPTIONS-Vorabanfrage, die Firmen-Proxys "
    "mit HTTP 405 blocken).\n"
    "function schreibToFormData(o){var fd=new FormData();Object.keys(o).forEach("
    "function(k){fd.append(k,o[k]);});return fd;}\n"
)

HEADER_JSON_RE = re.compile(
    r"headers:\s*\{[^{}]*'Content-Type':\s*'application/json'[^{}]*\},?\s*",
)


def find_paren_end(text, open_idx):
    if open_idx >= len(text) or text[open_idx] != '(':
        return -1
    depth = 0
    i = open_idx
    in_str = None
    esc = False
    while i < len(text):
        c = text[i]
        if in_str:
            if esc:
                esc = False
            elif c == '\\':
                esc = True
            elif c == in_str:
                in_str = None
            i += 1
            continue
        if c in "'\"`":
            in_str = c
        elif c == '(':
            depth += 1
        elif c == ')':
            depth -= 1
            if depth == 0:
                return i + 1
        i += 1
    return -1


def find_matching_brace(text, open_idx):
    if open_idx >= len(text) or text[open_idx] != '{':
        return -1
    depth = 0
    i = open_idx
    in_str = None
    esc = False
    in_line = False
    in_block = False
    while i < len(text):
        c = text[i]
        nxt = text[i + 1] if i + 1 < len(text) else ''
        if in_line:
            if c == '\n':
                in_line = False
            i += 1
            continue
        if in_block:
            if c == '*' and nxt == '/':
                in_block = False
                i += 2
                continue
            i += 1
            continue
        if in_str:
            if esc:
                esc = False
            elif c == '\\':
                esc = True
            elif c == in_str:
                in_str = None
            i += 1
            continue
        if c == '/' and nxt == '/':
            in_line = True
            i += 2
            continue
        if c == '/' and nxt == '*':
            in_block = True
            i += 2
            continue
        if c in "'\"`":
            in_str = c
            i += 1
            continue
        if c == '{':
            depth += 1
        elif c == '}':
            depth -= 1
            if depth == 0:
                return i + 1
        i += 1
    return -1


def transform_fetch_options(text):
    """Findet jede fetch(...)-Options-Objekt mit JSON-Header + JSON.stringify und
    baut sie auf FormData um. Liefert (neuer_text, changed_count)."""
    changed = 0
    out = []
    cursor = 0
    for m in re.finditer(r'\bfetch\s*\(', text):
        paren_open = m.end() - 1
        paren_close = find_paren_end(text, paren_open)
        if paren_close < 0:
            continue
        call = text[paren_open + 1:paren_close - 1]  # inside fetch(...)
        # Options-Objekt = erstes '{' im Call
        rel_brace = call.find('{')
        if rel_brace < 0:
            continue
        opts_open = paren_open + 1 + rel_brace
        opts_end = find_matching_brace(text, opts_open)
        if opts_end < 0:
            continue
        opts = text[opts_open:opts_end]  # inkl. { }
        if "'Content-Type': 'application/json'" not in opts and \
           "'Content-Type':'application/json'" not in opts and \
           "'Content-Type':  'application/json'" not in opts:
            continue
        if 'JSON.stringify(' not in opts:
            continue
        # 1) headers-Eintrag entfernen
        new_opts, nsub = HEADER_JSON_RE.subn('', opts)
        # 2) body: JSON.stringify( -> body: schreibToFormData(  (nur im body-Eintrag)
        new_opts, nbody = re.subn(
            r'(body:\s*)JSON\.stringify\(', r'\1schreibToFormData(', new_opts, count=1
        )
        if nbody == 0:
            continue  # JSON.stringify war nicht im body -> nicht anfassen
        out.append(text[cursor:opts_open])
        out.append(new_opts)
        cursor = opts_end
        changed += 1
    out.append(text[cursor:])
    return ''.join(out), changed


def inject_helper(text):
    if 'function schreibToFormData' in text:
        return text, False
    idx = text.rfind('</script>')
    if idx < 0:
        return text, False
    return text[:idx] + HELPER + text[idx:], True


def patch_file(path: Path) -> dict:
    text = path.read_text(encoding='utf-8')
    orig = text
    rep = {'file': str(path), 'changes': 0}

    # Schon FormData & kein JSON-Header mehr -> noop
    if 'function schreibToFormData' in text and \
       "'Content-Type': 'application/json'" not in text and \
       "'Content-Type':'application/json'" not in text and \
       "'Content-Type':  'application/json'" not in text:
        rep['status'] = 'noop'
        return rep

    text, n = transform_fetch_options(text)
    rep['changes'] = n
    if n > 0:
        text, _ = inject_helper(text)

    if text == orig:
        rep['status'] = 'noop'
        return rep

    scripts = re.findall(r'<script[^>]*>([\s\S]*?)</script>', text, re.IGNORECASE)
    js = '\n//---\n'.join(scripts)
    tmp = Path('/tmp/_chk_formdata.js')
    tmp.write_text(js, encoding='utf-8')
    r = subprocess.run(['node', '--check', str(tmp)], capture_output=True, text=True)
    if r.returncode != 0:
        rep['status'] = 'syntax_error'
        rep['stderr'] = r.stderr[:400]
        return rep

    path.write_text(text, encoding='utf-8')
    rep['status'] = 'patched'
    return rep


def main():
    args = sys.argv[1:]
    dry = '--dry-run' in args
    files = [Path(a) for a in args if a.endswith('.html')]
    if not files:
        print('usage: fix_schreib_formdata.py [--dry-run] file1.html ...')
        return
    by = {}
    fails = []
    touched = 0
    for p in files:
        if dry:
            t = p.read_text(encoding='utf-8')
            nt, n = transform_fetch_options(t)
            st = 'would_patch' if nt != t else 'noop'
            by[st] = by.get(st, 0) + 1
            continue
        r = patch_file(p)
        s = r['status']
        by[s] = by.get(s, 0) + 1
        if s == 'patched':
            touched += 1
        if s == 'syntax_error':
            fails.append(r)
    print('Ergebnis:', by, f'(getauscht: {touched})')
    for f in fails:
        print('  SYNTAX', f['file'])
        print('   ', f.get('stderr', '')[:200])


if __name__ == '__main__':
    main()
