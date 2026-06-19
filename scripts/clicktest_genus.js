// clicktest_genus.js — universeller Tab-Klicktest (JSDOM) für Genus-Dateien.
//
// Lädt die Datei mit echtem JS, KLICKT jeden .nav-btn über sein echtes onclick
// (b.click()) und prüft: genau eine .section aktiv, der geklickte Button wird
// aktiv, und die aktiven Sektionen über alle Buttons sind paarweise verschieden
// (Bijektion). Funktioniert für index-basierte UND id-basierte showSection.
//
// WICHTIG: NICHT showSection(i) per Schleifenindex aufrufen — das maskiert
// Nav-Index-Bugs (Vorfall 2026-06-19). Immer über das echte onclick klicken.
//
//   node scripts/clicktest_genus.js datei1.html [datei2.html ...]
//
// Braucht jsdom (npm i jsdom im Sandbox-Workspace).
const fs = require('fs');
const { JSDOM, VirtualConsole } = require('jsdom');
let anyBad = false;
for (const p of process.argv.slice(2)) {
  let res;
  try {
    const dom = new JSDOM(fs.readFileSync(p, 'utf8'), {
      runScripts: 'dangerously', pretendToBeVisual: true,
      url: 'http://localhost/', virtualConsole: new VirtualConsole()
    });
    const w = dom.window, d = w.document;
    // Genus-Section finden (über den Pool) und prüfen: NICHT verschachtelt + Inhalt da.
    const pool = d.getElementById('genusPool');
    const gsec = pool ? pool.closest('.section') : null;
    const pre = [];
    if (!pool || !gsec) pre.push('keine Genus-Section');
    else {
      if (gsec.parentElement && gsec.parentElement.closest('.section'))
        pre.push('VERSCHACHTELT in andere .section');
      if (pool.children.length < 20)
        pre.push('Pool leer/zu klein (' + pool.children.length + ')');
    }
    const navs = [...d.querySelectorAll('.nav-btn')]; const bad = pre.slice(); const seen = [];
    navs.forEach((b, i) => {
      try { b.click(); } catch (e) { bad.push(i + ':EXC'); return; }
      const act = [...d.querySelectorAll('.section.active')];
      if (act.length !== 1) { bad.push(i + ':aktiv=' + act.length); return; }
      if (d.querySelector('.nav-btn.active') !== b) bad.push(i + ':nav-mismatch');
      seen.push(act[0]);
    });
    if (new Set(seen).size !== navs.length) bad.push('nicht-bijektiv(' + new Set(seen).size + '/' + navs.length + ')');
    res = bad.length ? ('BROKEN ' + bad.slice(0, 5).join(',')) : ('OK (' + navs.length + ' tabs)');
    if (bad.length) anyBad = true;
  } catch (e) { res = 'LOADFAIL ' + e.message.split('\n')[0]; anyBad = true; }
  console.log(res.padEnd(34), p.split('/').pop());
}
process.exit(anyBad ? 1 : 0);
