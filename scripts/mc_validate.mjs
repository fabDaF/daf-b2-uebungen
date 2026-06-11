#!/usr/bin/env node
/* mc_validate.mjs — prüft die .mc_commit_list eines Repos vor dem Commit.
 * Pro Datei: (1) alle <script>-Blöcke kompilieren (vm), (2) Anführungszeichen-
 * Showstopper-Zähler Working == HEAD (kein neuer Quote-Fehler). Ein Node-Prozess.
 * Gibt PASS-Liste (NUL) nach <repo>/.mc_commit_ok und meldet FAILs.
 * Aufruf: node mc_validate.mjs <repoAbsPath>
 */
import fs from 'fs';
import path from 'path';
import vm from 'vm';
import { execFileSync } from 'child_process';

const repo = process.argv[2];
const list = fs.readFileSync(path.join(repo, '.mc_commit_list'), 'utf8').split('\0').filter(Boolean);
const BADQ = /„[^„"“”\n]{1,80}"/g;
function quotes(s) { const m = s.match(BADQ); return m ? m.length : 0; }
function scripts(s) { return [...s.matchAll(/<script[^>]*>([\s\S]*?)<\/script>/g)].map(m => m[1]); }

const ok = []; let fail = 0;
for (const rel of list) {
  const abs = path.join(repo, rel);
  const W = fs.readFileSync(abs, 'utf8');
  let HEAD = ''; try { HEAD = execFileSync('git', ['-C', repo, 'show', 'HEAD:' + rel], { encoding: 'utf8', maxBuffer: 1 << 30 }); } catch {}
  // Syntax-Gate relativ zu HEAD: nur wenn HEAD parsebar war, aber Working nicht,
  // hat MEIN Patch etwas gebrochen. Browser-äquivalent via new vm.Script.
  function parseFails(s) { let n = 0; for (const sc of scripts(s)) { try { new vm.Script(sc); } catch { n++; } } return n; }
  const headFails = parseFails(HEAD), workFails = parseFails(W);
  const synOk = workFails <= headFails;   // Patch darf die Parsebarkeit nicht verschlechtern
  const qOk = quotes(W) === quotes(HEAD);
  if (synOk && qOk) ok.push(rel);
  else { fail++; console.log('FAIL ' + rel + ' synFails ' + headFails + '->' + workFails + ' quote ' + quotes(HEAD) + '->' + quotes(W)); }
}
fs.writeFileSync(path.join(repo, '.mc_commit_ok'), ok.map(x => x + '\0').join(''), 'utf8');
console.log('VALIDATED repo=' + path.basename(repo) + ' PASS=' + ok.length + ' FAIL=' + fail);
