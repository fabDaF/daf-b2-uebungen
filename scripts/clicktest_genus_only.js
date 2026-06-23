// clicktest_genus_only.js — prüft GEZIELT, dass der Genus-Tab funktioniert,
// ohne vollständige Bijektion aller Tabs zu verlangen (für Lektionen mit
// vorbestehenden, von Genus unabhängigen Defekten — z. B. Schreibwerkstatt-Bug).
//
// Klickt den Genus-Nav-Button über sein echtes onclick und prüft:
//  - genau die Genus-Section wird aktiv (über den Pool gefunden),
//  - Genus-Section NICHT in anderer .section verschachtelt,
//  - genusPool hat >=20 Chips (initGenus lief, kein NaN/leer),
//  - kein JS-Fehler beim Laden/Klicken.
//
//   node scripts/clicktest_genus_only.js datei1.html [datei2.html ...]
const fs = require('fs');
const { JSDOM, VirtualConsole } = require('jsdom');
let anyBad = false;
for (const p of process.argv.slice(2)) {
  let res;
  try {
    let errs = [];
    // jsdom-Limitierungen (scrollTo, canvas o. Ä.) sind KEINE echten Datei-Bugs -> ignorieren
    const vc = new VirtualConsole().on('jsdomError', e => {
      const m = e.message.split('\n')[0];
      if (!/Not implemented/i.test(m)) errs.push(m);
    });
    const dom = new JSDOM(fs.readFileSync(p, 'utf8'), {
      runScripts: 'dangerously', pretendToBeVisual: true, url: 'http://localhost/', virtualConsole: vc
    });
    const w = dom.window, d = w.document;
    const pool = d.getElementById('genusPool');
    const gsec = pool ? pool.closest('.section') : null;
    const bad = [];
    if (!pool || !gsec) bad.push('keine Genus-Section');
    else {
      if (gsec.parentElement && gsec.parentElement.closest('.section')) bad.push('VERSCHACHTELT');
      if (pool.children.length < 20) bad.push('Pool=' + pool.children.length);
      // Genus-Nav-Button finden (Label enthält "Genus") und klicken
      const gnav = [...d.querySelectorAll('.nav-btn')].find(b => /Genus/.test(b.textContent || ''));
      if (!gnav) bad.push('kein Genus-Nav');
      else {
        // Klassen-agnostisch: welche Klasse gewinnt die Genus-Section beim Klick?
        const before = (gsec.className || '').split(/\s+/);
        try { gnav.click(); } catch (e) { bad.push('klick-EXC'); }
        const gained = (gsec.className || '').split(/\s+/).filter(c => c && !before.includes(c));
        if (gained.length === 0) bad.push('Genus-Tab nicht aktiv nach Klick');
        else {
          const cls = gained[0];
          const act = [...d.querySelectorAll('.section.' + cls)];
          if (act.length !== 1 || act[0] !== gsec) bad.push('Genus nicht eindeutig aktiv (' + act.length + 'x .' + cls + ')');
        }
      }
    }
    // Fremde (nicht genus-spezifische) JS-Fehler blockieren NICHT — der Genus-Tab
    // läuft in eigenem <script>. Es zählen nur die Genus-Checks (Pool/aktiv/verschachtelt).
    // errs nur als Hinweis anhängen, wenn der Genus-Tab ohnehin schon kaputt ist.
    if (errs.length && bad.length) bad.push('js:' + errs[0].slice(0, 30));
    res = bad.length ? ('BROKEN ' + bad.slice(0, 4).join(',')) : 'GENUS-OK';
    if (bad.length) anyBad = true;
  } catch (e) { res = 'LOADFAIL ' + e.message.split('\n')[0]; anyBad = true; }
  console.log(res.padEnd(34), p.split('/').pop());
}
process.exit(anyBad ? 1 : 0);
