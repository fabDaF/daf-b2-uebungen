#!/usr/bin/env node
/* mc_decide.mjs — Sicherer, isolierter MC-Rollout pro Repo.
 *
 * Für jede MC-Kandidatendatei:
 *   HEAD   = git show HEAD:rel
 *   TARGET = patchSource(HEAD).out   (HEAD + MC-Permutation, sonst nichts)
 *   W      = aktueller Working-Tree-Inhalt
 *   - W === HEAD   → Working ist sauber: schreibe TARGET, COMMIT.
 *   - W === TARGET → bereits sauber gepatcht: COMMIT.
 *   - sonst        → fremde Working-Tree-Änderung: NICHT anfassen, SKIP-FOREIGN.
 *   - HEAD fehlt (neue Datei) → SKIP-NEW.
 * Schreibt nie über fremde Änderungen. Gibt pro Datei eine Entscheidungszeile aus,
 * und am Ende die COMMIT-Liste null-getrennt nach <repo>/.mc_commit_list.
 *
 * Aufruf: node mc_decide.mjs <repoAbsPath> <relpath1> [<relpath2> ...]
 *   relpaths kommen null-getrennt über STDIN, wenn keine Argumente.
 */
import fs from 'fs';
import path from 'path';
import { execFileSync } from 'child_process';
import { patchSource } from './patch_mc_shuffle.mjs';

const repo = process.argv[2];
if (!repo) { console.error('Usage: mc_decide.mjs <repo> < relpaths(NUL)'); process.exit(2); }

let rels = process.argv.slice(3);
if (rels.length === 0) {
  const raw = fs.readFileSync(0, 'utf8');
  rels = raw.split('\0').filter(Boolean);
}

function headVersion(rel) {
  try { return execFileSync('git', ['-C', repo, 'show', 'HEAD:' + rel], { encoding: 'utf8', maxBuffer: 1 << 30 }); }
  catch { return null; }
}

const commitList = [];
let nCommit = 0, nForeign = 0, nNew = 0, nNochange = 0;
for (const rel of rels) {
  const abs = path.join(repo, rel);
  let W; try { W = fs.readFileSync(abs, 'utf8'); } catch { continue; }
  const HEAD = headVersion(rel);
  if (HEAD == null) { console.log('SKIP-NEW ' + rel); nNew++; continue; }
  const r = patchSource(HEAD);
  if (r.patchedArrays === 0) { console.log('SKIP-NOMC ' + rel); continue; } // HEAD hat schon gute Verteilung / kein MC
  const TARGET = r.out;
  if (W === TARGET) { commitList.push(rel); nCommit++; console.log('COMMIT(already) ' + rel); continue; }
  if (W === HEAD) { fs.writeFileSync(abs, TARGET, 'utf8'); commitList.push(rel); nCommit++; console.log('COMMIT(fresh) ' + rel); continue; }
  console.log('SKIP-FOREIGN ' + rel); nForeign++;
}
fs.writeFileSync(path.join(repo, '.mc_commit_list'), commitList.map(x => x + '\0').join(''), 'utf8');
console.log('=== repo=' + repo + ' COMMIT=' + nCommit + ' FOREIGN=' + nForeign + ' NEW=' + nNew + ' ===');
