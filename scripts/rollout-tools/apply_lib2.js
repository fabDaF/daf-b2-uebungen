/* Apply-Logik für B2/C1-Gerüst-Rollout — parametrisiert nach Niveau.
   Satzlängen-Staffel (Frank, 2026-06-10): B2 max. 16, C1 max. 18, min. 12. */
const fs = require('fs');
const T = s => s.split(/\s+/);
const PUNCT = new Set([',', '.', '!', '?', ';', ':']);
function q(w){ return "'" + w.replace(/'/g, "\\'") + "'"; }
function arr(a){ return '[' + a.map(q).join(', ') + ']'; }
function render(sentences){
  const lines = sentences.map(s => {
    const validStr = s.v.map(arr).join(',\n      ');
    return '  { parts: ' + arr(s.v[0]) + ',\n    valid: [' + validStr + '],\n    punct: ' + q(s.p || '.') + ' }';
  });
  return '[\n' + lines.join(',\n') + '\n]';
}
function apply(DATA, opts){
  const { dir, min = 12, max } = opts;
  if (!max) { console.error('max fehlt (B2: 16, C1: 18)'); process.exit(1); }
  let fail = 0;
  for (const [f, sentences] of Object.entries(DATA)){
    sentences.forEach((s, i) => {
      const L = s.v[0].length;
      if (!s.v.every(v => v.length === L)) { console.error(f, 'Satz', i, 'valid-Längen ungleich'); fail++; }
      const sorted = a => a.slice().sort().join('|');
      s.v.forEach(v => { if (sorted(v) !== sorted(s.v[0])) { console.error(f, 'Satz', i, 'valid-Wortmengen ungleich'); fail++; } });
      const words = s.v[0].filter(w => !PUNCT.has(w)).length;
      if (words < min) { console.error(f, 'Satz', i, 'nur', words, 'Wörter (min', min + ')'); fail++; }
      if (words > max) { console.error(f, 'Satz', i, words, 'Wörter — über Maximum', max); fail++; }
      if (!s.v[0].includes(',')) { console.error(f, 'Satz', i, 'kein Komma-Chip'); fail++; }
      s.v[0].forEach(w => { if (/\s/.test(w)) { console.error(f, 'Satz', i, 'Mehr-Wort-Chip:', w); fail++; } });
    });
  }
  if (fail) { console.error('ABBRUCH:', fail, 'Fehler'); process.exit(1); }
  for (const [f, sentences] of Object.entries(DATA)){
    const path = dir + '/' + f;
    let html = fs.readFileSync(path, 'utf8');
    const i = html.indexOf('var satzbauData');
    if (i < 0) { console.error(f, 'satzbauData nicht gefunden'); process.exit(1); }
    const start = html.indexOf('[', html.indexOf('=', i));
    let d = 0, end = -1;
    for (let p = start; p < html.length; p++){ const c = html[p];
      if (c === '[') d++; else if (c === ']') { d--; if (!d){ end = p; break; } } }
    html = html.slice(0, start) + render(sentences) + html.slice(end + 1);
    fs.writeFileSync(path, html);
    console.log('OK', f, '—', sentences.length, 'Sätze ersetzt');
  }
}
module.exports = { T, apply };

/* Chirurgischer Modus: ersetzt nur gelistete Satz-Indizes, Rest bleibt wörtlich. */
const vm = require('vm');
function applyFix(FIX, opts){
  const { dir, min = 12, max } = opts;
  let fail = 0, fixed = 0;
  for (const [f, map] of Object.entries(FIX)){
    for (const [k, orders] of Object.entries(map)){
      const L = orders[0].length;
      const sorted = a => a.slice().sort().join('|');
      orders.forEach(o => {
        if (o.length !== L){ console.error(f, k, 'valid-Längen ungleich'); fail++; }
        if (sorted(o) !== sorted(orders[0])){ console.error(f, k, 'Wortmengen ungleich'); fail++; }
      });
      const words = orders[0].filter(w => !PUNCT.has(w)).length;
      if (words < min || words > max){ console.error(f, k, 'Wortzahl', words, 'außerhalb', min + '–' + max); fail++; }
      if (!orders[0].includes(',')){ console.error(f, k, 'kein Komma-Chip'); fail++; }
      orders[0].forEach(w => { if (/\s/.test(w)){ console.error(f, k, 'Mehr-Wort-Chip:', w); fail++; } });
    }
  }
  if (fail){ console.error('ABBRUCH:', fail); process.exit(1); }
  for (const [f, map] of Object.entries(FIX)){
    const path = dir + '/' + f;
    let html = fs.readFileSync(path, 'utf8');
    const i = html.indexOf('var satzbauData');
    const start = html.indexOf('[', html.indexOf('=', i));
    let d = 0, end = -1;
    for (let p = start; p < html.length; p++){ const c = html[p];
      if (c === '[') d++; else if (c === ']'){ d--; if (!d){ end = p; break; } } }
    const data = vm.runInNewContext('(' + html.slice(start, end + 1) + ')');
    for (const [k, orders] of Object.entries(map)){
      const ex = data[Number(k)];
      if (!ex){ console.error(f, 'Index', k, 'fehlt'); process.exit(1); }
      ex.parts = orders[0].slice();
      ex.valid = orders.map(o => o.slice());
      delete ex.row;
      fixed++;
    }
    const sentences = data.map(ex => ({ v: (typeof ex.valid[0] === 'string') ? [ex.valid] : ex.valid, p: ex.punct }));
    html = html.slice(0, start) + render(sentences) + html.slice(end + 1);
    fs.writeFileSync(path, html);
    console.log('OK', f, '—', Object.keys(map).length, 'Sätze ersetzt');
  }
  console.log('Gesamt:', fixed);
}
module.exports.applyFix = applyFix;
