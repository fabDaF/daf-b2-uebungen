#!/usr/bin/env python3
"""
Mechanischer Zwei-Fix-Runner: FB-CHIP-WRAP + FB-SW-INIT.
Nur Anwendung der exakt spezifizierten Bedingungen/Aktionen. Keine sonstigen Aenderungen.

Usage:
  python3 fb_chipwrap_swinit.py scan <dir> [<dir> ...]      # nur berichten, nichts schreiben
  python3 fb_chipwrap_swinit.py apply <dir> [<dir> ...]     # anwenden + Datei-Liste ausgeben
  python3 fb_chipwrap_swinit.py scan --filelist <listfile>  # explizite Dateiliste (eine pro Zeile)
  python3 fb_chipwrap_swinit.py apply --filelist <listfile>
"""
import re
import sys
import os

CHIP_RE = re.compile(r'\.chip\s*\{[^}]*white-space:\s*nowrap', re.DOTALL)
CHIP_EXCEPT_RE = re.compile(
    r'\.(chip-bank|drop-zone)[^{]*\.chip[^{]*\{[^}]*white-space:\s*normal', re.DOTALL
)
INIT_DEF_RE = re.compile(r'function\s+initSchreibwerkstatt\s*\(')

FIX_A_MARKER = 'FB-CHIP-WRAP'
FIX_B_MARKER = 'FB-SW-INIT'

FIX_A_LINE = "/* FB-CHIP-WRAP */ .chip-bank .chip, .drop-zone .chip { white-space: normal; display: inline-block; text-align: left; max-width: 100%; overflow-wrap: break-word; }"

FIX_B_BLOCK = """<script>/* FB-SW-INIT */ (function(){ if (typeof initSchreibwerkstatt !== 'function') return; if (document.readyState === 'loading') { document.addEventListener('DOMContentLoaded', function(){ initSchreibwerkstatt(); }); } else { initSchreibwerkstatt(); } })();</script>"""


def find_html_files(dirs):
    files = []
    for d in dirs:
        for root, subdirs, fnames in os.walk(d):
            subdirs[:] = [s for s in subdirs if s != '.git']
            for f in fnames:
                if f.endswith('.html'):
                    files.append(os.path.join(root, f))
    return sorted(files)


def check_fix_a(text):
    if FIX_A_MARKER in text:
        return False
    if 'chip-bank' not in text and 'drop-zone' not in text:
        return False
    if not CHIP_RE.search(text):
        return False
    if CHIP_EXCEPT_RE.search(text):
        return False
    return True


def check_fix_b(text):
    if FIX_B_MARKER in text:
        return False
    if not INIT_DEF_RE.search(text):
        return False
    count = text.count('initSchreibwerkstatt')
    if count != 1:
        return False
    return True


def apply_fix_a(text):
    idx = text.find('</style>')
    if idx == -1:
        return text, False
    insertion = "\n" + FIX_A_LINE + "\n"
    new_text = text[:idx] + insertion + text[idx:]
    return new_text, True


def apply_fix_b(text):
    idx = text.rfind('</body>')
    if idx == -1:
        return text, False
    insertion = FIX_B_BLOCK + "\n"
    new_text = text[:idx] + insertion + text[idx:]
    return new_text, True


def node_parse_check(filepath):
    import subprocess
    with open(filepath, 'r', encoding='utf-8', errors='surrogateescape') as f:
        text = f.read()
    scripts = re.findall(r'<script(?:\s+[^>]*)?>(.*?)</script>', text, re.DOTALL | re.IGNORECASE)
    js_snippets = [s for s in scripts if s.strip()]
    if not js_snippets:
        return True, "no inline scripts"
    combined_ok = True
    errors = []
    for i, snippet in enumerate(js_snippets):
        tmp_js = f"/tmp/fb_parse_check_{os.getpid()}_{i}.js"
        with open(tmp_js, 'w', encoding='utf-8', errors='surrogateescape') as tf:
            tf.write(snippet)
        node_script = f"""
const vm = require('vm');
const fs = require('fs');
const code = fs.readFileSync('{tmp_js}', 'utf8');
try {{
  new vm.Script(code, {{filename: '{tmp_js}'}});
  console.log('OK');
}} catch(e) {{
  console.log('ERR: ' + e.message);
  process.exit(1);
}}
"""
        tmp_node = f"/tmp/fb_parse_runner_{os.getpid()}_{i}.js"
        with open(tmp_node, 'w') as nf:
            nf.write(node_script)
        result = subprocess.run(['node', tmp_node], capture_output=True, text=True)
        os.remove(tmp_js)
        os.remove(tmp_node)
        if result.returncode != 0:
            combined_ok = False
            errors.append(f"script#{i}: {result.stdout.strip()} {result.stderr.strip()}")
    return combined_ok, "; ".join(errors) if errors else "all scripts parse ok"


def main():
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(1)
    mode = sys.argv[1]
    rest = sys.argv[2:]
    if rest and rest[0] == '--filelist':
        listfile = rest[1]
        with open(listfile) as lf:
            files = [line.strip() for line in lf if line.strip()]
    else:
        files = find_html_files(rest)

    fix_a_files = []
    fix_b_files = []
    skipped_no_body = []
    restored_parse_fail = []
    fix_b_count_mismatch = []

    for fp in files:
        try:
            with open(fp, 'r', encoding='utf-8', errors='surrogateescape') as f:
                text = f.read()
        except Exception as e:
            print(f"READ-ERROR {fp}: {e}")
            continue

        needs_a = check_fix_a(text)
        needs_b = check_fix_b(text)

        if not needs_a and not needs_b:
            continue

        if mode == 'scan':
            if needs_a:
                fix_a_files.append(fp)
            if needs_b:
                fix_b_files.append(fp)
            continue

        orig_text = text
        changed = False

        if needs_a:
            text, ok = apply_fix_a(text)
            if ok:
                changed = True
                fix_a_files.append(fp)

        if needs_b:
            if '</body>' not in text:
                skipped_no_body.append(fp)
            else:
                text, ok = apply_fix_b(text)
                if ok:
                    changed = True
                    fix_b_files.append(fp)
                    newcount = text.count('initSchreibwerkstatt')
                    if newcount < 3:
                        fix_b_count_mismatch.append((fp, newcount))

        if changed:
            with open(fp, 'w', encoding='utf-8', errors='surrogateescape') as f:
                f.write(text)
            ok, msg = node_parse_check(fp)
            if not ok:
                restored_parse_fail.append((fp, msg))
                import subprocess
                d = os.path.abspath(fp)
                repo_root = None
                cur = os.path.dirname(d)
                while cur != '/':
                    if os.path.isdir(os.path.join(cur, '.git')):
                        repo_root = cur
                        break
                    cur = os.path.dirname(cur)
                if repo_root:
                    rel = os.path.relpath(fp, repo_root)
                    subprocess.run(['git', '-C', repo_root, 'checkout', '--', rel])
                if fp in fix_a_files:
                    fix_a_files.remove(fp)
                if fp in fix_b_files:
                    fix_b_files.remove(fp)

    print("=== FIX A files ({}) ===".format(len(fix_a_files)))
    for fp in fix_a_files:
        print(fp)
    print("=== FIX B files ({}) ===".format(len(fix_b_files)))
    for fp in fix_b_files:
        print(fp)
    print("=== SKIPPED (no </body>) ({}) ===".format(len(skipped_no_body)))
    for fp in skipped_no_body:
        print(fp)
    print("=== RESTORED (parse fail) ({}) ===".format(len(restored_parse_fail)))
    for fp, msg in restored_parse_fail:
        print(f"{fp} :: {msg}")
    print("=== FIX B COUNT MISMATCH (<3 after insert) ({}) ===".format(len(fix_b_count_mismatch)))
    for fp, c in fix_b_count_mismatch:
        print(f"{fp} :: count={c}")


if __name__ == '__main__':
    main()
