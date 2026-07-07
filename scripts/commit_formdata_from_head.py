#!/usr/bin/env python3
"""
commit_formdata_from_head.py — committet den FormData-Send-Fix ISOLIERT.

Warum HEAD-basiert: die Arbeitskopie enthält teils fremde, noch nicht committete
WIP (Nav-Rollout, Finding-Flow etc.). Ein Commit der Arbeitskopie würde diese WIP
mit einschleppen. Deshalb: den Fix auf die HEAD-Version jeder Zieldatei anwenden
und NUR das committen. Netto-Diff pro Datei = ausschließlich der Send-Fix; die
fremde WIP bleibt unangetastet in der Arbeitskopie.

Aufruf (aus dem jeweiligen Repo-Root):
    python3 .../commit_formdata_from_head.py --repo <repo_root> [--exclude PREFIX ...] --dry-run
    python3 .../commit_formdata_from_head.py --repo <repo_root> [--exclude PREFIX ...] --commit "MSG"

Zieldateien = im HEAD getrackte *.html mit JSON-Content-Type + web3forms.
Spezialfälle:
  * GEHIRN_02G/05G (kein access_key, formsubmit-Ära-Body) -> volle Web3Forms-Migration
  * baukoordinator (var body = JSON.stringify) -> zugewiesener-Body-Fix
"""
import argparse
import re
import subprocess
import sys
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPTS))

import fix_schreib_formdata as F           # transform_fetch_options, inject_helper, HEADER_JSON_RE
import patch_schreib_web3forms as P        # patch_constants, patch_post_function, insert_helpers, ...

HELPER_MARK = 'function schreibToFormData'


def git(repo, *args, capture=True, input_bytes=None):
    return subprocess.run(['git', '-C', str(repo), *args],
                          capture_output=capture, input=input_bytes)


def git_out(repo, *args):
    r = subprocess.run(['git', '-C', str(repo), *args], capture_output=True)
    if r.returncode != 0:
        raise RuntimeError('git ' + ' '.join(args) + ':\n' + r.stderr.decode('utf-8', 'ignore'))
    return r.stdout


def head_blob(repo, relpath):
    return git_out(repo, 'show', 'HEAD:' + relpath).decode('utf-8', 'ignore')


def has_json_pattern(text):
    return ("api.web3forms.com" in text) and (
        "'Content-Type': 'application/json'" in text or
        "'Content-Type':'application/json'" in text or
        "'Content-Type':  'application/json'" in text
    )


def is_gehirn_broken(text):
    # Web3Forms-Endpoint, aber Body ohne access_key + formsubmit-Ära-Felder
    return ('FORMSUBMIT_ENDPOINT' in text and 'access_key' not in text
            and ('_subject' in text or '_template' in text or '_captcha' in text))


def transform_gehirn(text):
    text, _ = P.patch_constants(text)
    text, _ = P.patch_post_function(text)
    text, _ = P.insert_helpers(text)
    text, _ = P.patch_error_callbacks(text)
    text, _ = P.insert_css(text)
    return text


def transform_bau(text):
    text = re.sub(r'(var\s+body\s*=\s*)JSON\.stringify\(', r'\1schreibToFormData(', text, count=1)
    text = F.HEADER_JSON_RE.sub('', text, count=1)
    if HELPER_MARK not in text:
        text, _ = F.inject_helper(text)
    return text


def transform_generic(text):
    text, n = F.transform_fetch_options(text)
    if n > 0 and HELPER_MARK not in text:
        text, _ = F.inject_helper(text)
    return text


def transform_head_version(text):
    if is_gehirn_broken(text):
        return transform_gehirn(text)
    # baukoordinator-Stil: zugewiesener Body
    if re.search(r'var\s+body\s*=\s*JSON\.stringify\(', text) and 'body: body' in text:
        return transform_bau(text)
    return transform_generic(text)


def node_check(text):
    scripts = re.findall(r'<script[^>]*>([\s\S]*?)</script>', text, re.IGNORECASE)
    js = '\n//---\n'.join(scripts)
    tmp = Path('/tmp/_chk_fromhead.js')
    tmp.write_text(js, encoding='utf-8')
    r = subprocess.run(['node', '--check', str(tmp)], capture_output=True, text=True)
    return r.returncode == 0, r.stderr[:300]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--repo', required=True)
    ap.add_argument('--exclude', action='append', default=[])
    ap.add_argument('--dry-run', action='store_true')
    ap.add_argument('--commit', default=None)
    ap.add_argument('--branch', default='main')
    ap.add_argument('--remote', default='origin')
    args = ap.parse_args()
    repo = Path(args.repo).resolve()

    tracked = git_out(repo, 'ls-files', '-z', '*.html').decode('utf-8', 'ignore').split('\0')
    tracked = [t for t in tracked if t]
    targets = []
    for rel in tracked:
        if any(rel.startswith(pref) for pref in args.exclude):
            continue
        try:
            hv = head_blob(repo, rel)
        except Exception:
            continue
        if has_json_pattern(hv):
            targets.append(rel)

    print(f'[{repo.name or repo}] {len(targets)} Zieldateien (aus HEAD)')

    staged = []   # (mode, sha, rel)
    fails = []
    unchanged = 0
    for rel in targets:
        hv = head_blob(repo, rel)
        nv = transform_head_version(hv)
        if nv == hv:
            unchanged += 1
            continue
        ok, err = node_check(nv)
        if not ok:
            fails.append((rel, err))
            continue
        # Blob schreiben
        r = subprocess.run(['git', '-C', str(repo), 'hash-object', '-w', '--stdin'],
                           input=nv.encode('utf-8'), capture_output=True)
        if r.returncode != 0:
            fails.append((rel, r.stderr.decode('utf-8', 'ignore')[:200]))
            continue
        sha = r.stdout.decode().strip()
        # Modus aus HEAD übernehmen
        mode_line = git_out(repo, 'ls-files', '-s', rel).decode().strip()
        mode = mode_line.split()[0] if mode_line else '100644'
        staged.append((mode, sha, rel))

    print(f'   zu committen: {len(staged)} | unverändert: {unchanged} | Fehler: {len(fails)}')
    for rel, err in fails[:20]:
        print('   SYNTAX/FEHLER', rel, '->', err[:120])

    if fails:
        print('   !! Abbruch wegen Fehlern (nichts committet).')
        return 2
    if args.dry_run or not args.commit:
        print('   (dry-run — kein Commit)')
        return 0
    if not staged:
        print('   nichts zu committen.')
        return 0

    # Alt-Index aus HEAD, dann Ziel-Blobs überschreiben
    import os, tempfile
    alt = tempfile.mktemp(prefix='fd-index-')
    env = dict(os.environ, GIT_INDEX_FILE=alt)
    subprocess.run(['git', '-C', str(repo), 'read-tree', 'HEAD'], env=env, check=True)
    for mode, sha, rel in staged:
        subprocess.run(['git', '-C', str(repo), 'update-index', '--cacheinfo',
                        f'{mode},{sha},{rel}'], env=env, check=True)
    tree = subprocess.run(['git', '-C', str(repo), 'write-tree'], env=env,
                          capture_output=True, check=True).stdout.decode().strip()
    parent = git_out(repo, 'rev-parse', 'HEAD').decode().strip()
    commit = subprocess.run(['git', '-C', str(repo), 'commit-tree', tree, '-p', parent,
                             '-m', args.commit], capture_output=True, check=True).stdout.decode().strip()
    # Ref per Bash-Datei-Write (nicht Write-Tool!)
    (repo / '.git' / 'refs' / 'heads' / args.branch).write_text(commit + '\n')
    push = subprocess.run(['git', '-C', str(repo), 'push', args.remote,
                           f'{args.branch}:{args.branch}'], capture_output=True)
    print('   push rc=', push.returncode)
    sys.stdout.write(push.stderr.decode('utf-8', 'ignore')[-400:])
    # origin-Ref lokal nachziehen
    rem = subprocess.run(['git', '-C', str(repo), 'ls-remote', args.remote, args.branch],
                         capture_output=True).stdout.decode().split()
    remote_sha = rem[0] if rem else '?'
    print(f'   commit={commit[:10]} remote={remote_sha[:10]} {"OK" if remote_sha==commit else "!! MISMATCH"}')
    return 0 if remote_sha == commit else 3


if __name__ == '__main__':
    sys.exit(main())
