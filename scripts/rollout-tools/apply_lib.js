/* Gemeinsame Apply-Logik für den Gerüst-Rollout B1.1 (Stufe 1). */
const fs = require('fs');
const DIR = '/sessions/beautiful-friendly-ride/mnt/fabDaF/htmlS/B1.1/';
const T = s => s.split(/\s+/);
function q(w){ return "'" + w.replace(/'/g, "\\'") + "'"; }
function arr(a){ return '[' + a.map(q).join(', ') + ']'; }
function render(sentences){
  const lines = sentences.map(s => {
    const validStr = s.v.map(arr).join(',\n      ');
    return '  { parts: ' + arr(s.v[0]) + ',\n    valid: [' + validStr + '],\n    punct: ' + q(s.p || '.') + ' }';
  });
  return '[\n' + lines.join(',\n') + '\n]';
}
function apply(DATA){
  let fail = 0;
  for (const [f, sentences] of Object.entries(DATA)){
    sentences.forEach((s, i) => {
      const L = s.v[0].length;
      if (!s.v.every(v => v.length === L)) { console.error(f, 'Satz', i, 'valid-Längen ungleich'); fail++; }
      const sorted = a => a.slice().sort().join('|');
      s.v.forEach(v => { if (sorted(v) !== sorted(s.v[0])) { console.error(f, 'Satz', i, 'valid-Wortmengen ungleich'); fail++; } });
      const words = s.v[0].filter(w => w !== ',').length;
      if (words < 12) { console.error(f, 'Satz', i, 'nur', words, 'Wörter'); fail++; }
      if (!s.v[0].includes(',')) { console.error(f, 'Satz', i, 'kein Komma-Chip'); fail++; }
      s.v[0].forEach(w => { if (/\s/.test(w)) { console.error(f, 'Satz', i, 'Mehr-Wort-Chip:', w); fail++; } });
    });
  }
  if (fail) { console.error('ABBRUCH:', fail, 'Fehler'); process.exit(1); }
  for (const [f, sentences] of Object.entries(DATA)){
    const path = DIR + f;
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
