#!/usr/bin/env node
/* Triage: zeigt nur Sätze, die Arbeit brauchen (<min, >max, ohne Komma,
   großgeschriebenes Nicht-Nomen an Position 0, Mehr-Wort-Chips). */
const fs = require('fs'), vm = require('vm');
const PUNCT = new Set([',', '.', '!', '?', ';', ':']);
const [dir, pattern, min, max] = [process.argv[2], new RegExp(process.argv[3]), +process.argv[4], +process.argv[5]];
const LOWER_OK = new Set(['Sie', 'Ihnen', 'Ihr', 'Ihre', 'Ihren', 'Ihrem', 'Ihrer']); // Höflichkeitsform zählt nicht als Fehler
for (const f of fs.readdirSync(dir).filter(f => pattern.test(f) && f.endsWith('.html')).sort()){
  const html = fs.readFileSync(dir + '/' + f, 'utf8');
  const i = html.indexOf('var satzbauData'); if (i < 0) continue;
  const start = html.indexOf('[', html.indexOf('=', i));
  let d = 0, end = -1;
  for (let p = start; p < html.length; p++){ const c = html[p];
    if (c === '[') d++; else if (c === ']'){ d--; if (!d){ end = p; break; } } }
  let data; try { data = vm.runInNewContext('(' + html.slice(start, end + 1) + ')'); } catch(e){ console.log(f, 'PARSE-FAIL'); continue; }
  let shown = false;
  data.forEach((ex, k) => {
    let v = ex.valid; if (!v) return; if (typeof v[0] === 'string') v = [v];
    const words = v[0].filter(w => !PUNCT.has(w)).length;
    const probs = [];
    if (words < min) probs.push(words + 'W');
    if (words > max) probs.push(words + 'W>max');
    if (!v[0].includes(',')) probs.push('kein-Komma');
    v[0].forEach(w => { if (/\s/.test(w)) probs.push('Mehrwort:' + w); });
    if (probs.length){
      if (!shown){ console.log('=== ' + f); shown = true; }
      console.log('#' + k + ' [' + probs.join(',') + '] ' + v[0].join(' ') + (ex.punct && ex.punct !== '.' ? '  ' + ex.punct : ''));
    }
  });
}
