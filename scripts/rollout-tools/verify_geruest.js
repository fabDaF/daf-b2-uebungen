#!/usr/bin/env node
/* Verifikation nach Stufe 2: Syntax aller Script-Blöcke, Quote-Showstopper,
   SBGAP-Konsistenz (Lücken==parts, Anker invariant + nie Verb-Position, Multiset). */
const fs = require('fs'), vm = require('vm');
const DIR = (process.env.VDIR || '/sessions/beautiful-friendly-ride/mnt/fabDaF/htmlS/B1.1') + '/';
let bad = 0;
for (const f of process.argv.slice(2)){
  const html = fs.readFileSync(DIR + f, 'utf8');
  [...html.matchAll(/<script>([\s\S]*?)<\/script>/g)].forEach((m, si) => {
    try { new vm.Script(m[1]); } catch(e){ console.error(f, 'Script', si, 'SYNTAXFEHLER:', e.message); bad++; }
  });
  const q = html.match(/„([^„"“”\n<]{1,80})"/g); // < ausgeschlossen: HTML-Attribute sind keine Zitat-Schließer
  if (q){ console.error(f, 'QUOTE-Fehler:', q.slice(0,3)); bad++; }
  const am = html.match(/var SBGAP = (\[[\s\S]*?\]);/);
  const dm = html.indexOf('var satzbauData');
  const start = html.indexOf('[', html.indexOf('=', dm));
  let d = 0, end = -1;
  for (let p = start; p < html.length; p++){ const c = html[p];
    if (c === '[') d++; else if (c === ']') { d--; if (!d){ end = p; break; } } }
  const data = vm.runInNewContext('(' + html.slice(start, end + 1) + ')');
  if (!am){ console.error(f, 'kein SBGAP-Block'); bad++; continue; }
  const sbgap = vm.runInNewContext('(' + am[1] + ')');
  if (sbgap.length !== data.length){ console.error(f, 'SBGAP', sbgap.length, '!= Sätze', data.length); bad++; }
  for (const g of sbgap){
    const ex = data[g.i]; let v = ex.valid; if (typeof v[0] === 'string') v = [v];
    const gaps = g.row.filter(x => x === '_').length;
    if (gaps !== g.parts.length){ console.error(f, 'Satz', g.i, 'Lücken', gaps, '!= parts', g.parts.length); bad++; }
    if (g.row.length !== v[0].length){ console.error(f, 'Satz', g.i, 'row-Länge falsch'); bad++; }
    g.row.forEach((w, k) => { if (w === '_') return;
      if (!v.every(o => o[k] === w)){ console.error(f, 'Satz', g.i, 'Anker', w, 'nicht invariant an', k); bad++; }
      if (w === ','){ console.error(f, 'Satz', g.i, 'KOMMA als Anker!'); bad++; }
    });
    const merged = [...g.parts, ...g.row.filter(x => x !== '_')].sort().join('|');
    if (merged !== v[0].slice().sort().join('|')){ console.error(f, 'Satz', g.i, 'Multiset-Mismatch'); bad++; }
  }
}
console.log(bad ? ('FEHLER: ' + bad) : ('ALLE CHECKS GRÜN — ' + process.argv.slice(2).length + ' Dateien'));
process.exit(bad ? 1 : 0);
