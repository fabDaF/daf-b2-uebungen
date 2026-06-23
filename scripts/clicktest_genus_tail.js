// clicktest_genus_tail.js — container-agnostischer Genus-Gate für die
// heterogenen Rest-Lektionen (Tab-Container .section ODER .tab-content ODER .sec …).
//
// Findet die Genus-Section als DIREKTEN Eltern-Container von #genusPool
// (section_html bettet den Pool direkt in das Genus-Section-<div> ein),
// klickt den Genus-Nav-Button über sein echtes onclick und prüft:
//  - Pool hat >=20 Chips (initGenus lief),
//  - Genus-Section NICHT in einer gleichartigen Tab-Section verschachtelt,
//  - beim Klick gewinnt GENAU die Genus-Section die Aktiv-Klasse
//    (klassen-agnostisch: 'active'/'aktiv'/…), kein anderer Tab gleichzeitig.
//
//   node scripts/clicktest_genus_tail.js datei1.html [datei2.html ...]
const fs = require('fs');
const { JSDOM, VirtualConsole } = require('jsdom');
let anyBad = false;
for (const p of process.argv.slice(2)) {
  let res;
  try {
    let errs = [];
    const vc = new VirtualConsole().on('jsdomError', e => {
      const m = e.message.split('\n')[0];
      if (!/Not implemented/i.test(m)) errs.push(m);
    });
    const dom = new JSDOM(fs.readFileSync(p, 'utf8'), {
      runScripts: 'dangerously', pretendToBeVisual: true, url: 'http://localhost/', virtualConsole: vc
    });
    const d = dom.window.document;
    const pool = d.getElementById('genusPool');
    const gsec = pool ? pool.parentElement : null;   // Pool steckt direkt in der Genus-Section
    const bad = [];
    if (!pool || !gsec) bad.push('keine Genus-Section');
    else {
      // Container-Klasse der Genus-Section (erstes Klassen-Token, das wie ein Tab aussieht)
      const containerCls = [...gsec.classList].find(c => /section|tab|sec/i.test(c)) || gsec.classList[0];
      if (containerCls && gsec.parentElement && gsec.parentElement.closest('.' + containerCls))
        bad.push('VERSCHACHTELT');
      if (pool.children.length < 20) bad.push('Pool=' + pool.children.length);
      const gnav = [...d.querySelectorAll('.nav-btn, .nav button, .nav a, .nav div[onclick]')]
        .find(b => /Genus/.test(b.textContent || ''));
      if (!gnav) bad.push('kein Genus-Nav');
      else {
        const before = (gsec.className || '').split(/\s+/);
        try { gnav.click(); } catch (e) { bad.push('klick-EXC'); }
        const gained = (gsec.className || '').split(/\s+/).filter(c => c && !before.includes(c));
        if (gained.length === 0) bad.push('Genus-Tab nicht aktiv nach Klick');
        else if (containerCls) {
          const act = [...d.querySelectorAll('.' + containerCls + '.' + gained[0])];
          if (act.length !== 1 || act[0] !== gsec)
            bad.push('Genus nicht eindeutig aktiv (' + act.length + 'x)');
        }
      }
    }
    if (errs.length && bad.length) bad.push('js:' + errs[0].slice(0, 30));
    res = bad.length ? ('BROKEN ' + bad.slice(0, 4).join(',')) : 'GENUS-OK';
    if (bad.length) anyBad = true;
  } catch (e) { res = 'LOADFAIL ' + e.message.split('\n')[0]; anyBad = true; }
  console.log(res.padEnd(34), p.split('/').pop());
}
process.exit(anyBad ? 1 : 0);
