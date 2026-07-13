#!/usr/bin/env node
/* check_schreib_init.js — Gate für die Schreibwerkstatt (2026-07-13).

   Prüft VERHALTEN, nicht Markup: lädt jede Datei in JSDOM, klickt alle Tabs durch
   (viele Lektionen initialisieren die Schreibwerkstatt erst beim Öffnen des Tabs),
   tippt in das erste Schreibfeld und verlangt danach zweierlei:

     1. der Wortzähler zählt hoch     → sonst sieht der Schüler keine Wortzahl
     2. der Text steht in localStorage → sonst ist er beim Schließen des Fensters WEG

   Genau diese zwei Symptome hat Frank am 2026-07-13 gemeldet. Ursache damals: der
   Aufruf von initSchreibwerkstatt() war beim Patchen in eine fremde Funktion gerutscht
   (resetSatzbau o. ä.) und lief nie beim Laden — 51 Lektionen betroffen, Datenverlust.

   Reparateure: scripts/fix_schreib_init.py (Init läuft nie)
                scripts/inject_wc_autosave.py (alte Generation ohne Zähler/Autosave)

   Aufruf: node scripts/check_schreib_init.js datei1.html …
           node scripts/check_schreib_init.js --list liste.txt
   Exit 1, wenn mindestens eine Datei defekt ist. */
const fs = require('fs');
const { JSDOM, VirtualConsole } = require('jsdom');

function dateien(argv) {
  if (argv[0] === '--list') {
    return fs.readFileSync(argv[1], 'utf8').split('\n').map(s => s.trim()).filter(Boolean);
  }
  return argv;
}

function pruefe(file) {
  return new Promise(res => {
    const vc = new VirtualConsole();
    vc.on('jsdomError', () => {});
    let dom;
    try {
      dom = new JSDOM(fs.readFileSync(file, 'utf8'), {
        runScripts: 'dangerously',
        url: 'https://daf.frankburkert-daf.de/x.html',
        pretendToBeVisual: true,
        virtualConsole: vc
      });
    } catch (e) { return res({ file, status: 'LOADFAIL', info: e.message }); }

    const w = dom.window;
    setTimeout(() => {
      try {
        const d = w.document;
        // Lazy-Init: Tabs durchklicken, wie ein Schüler es täte
        d.querySelectorAll('.nav-btn, .tab-btn, [onclick^="showTab"], [onclick^="showSection"]')
          .forEach(b => { try { b.click(); } catch (e) {} });

        const mini = d.querySelector('.schreib-mini-textarea');
        const gross = d.getElementById('schreibfeld') || d.querySelector('.schreibfeld-area');
        const ta = mini || gross;
        if (!ta) { w.close(); return res({ file, status: 'OK', info: 'kein Schreibfeld' }); }

        const karte = ta.closest('.schreib-aufgabe-karte, .schreib-karte, .schreibfeld-block') || ta.parentNode;
        const wcEl = (mini ? d.querySelector('.wc-' + mini.dataset.aufgabe) : d.getElementById('schreib-count'))
                     || karte.querySelector('.fb-wc strong');

        ta.value = 'eins zwei drei vier fünf';
        ta.dispatchEvent(new w.Event('input', { bubbles: true }));

        const zaehlt = !!(wcEl && /5/.test(wcEl.textContent));
        const speichert = Object.keys(w.localStorage)
          .some(k => /schreib|fb-sw/i.test(k) && (w.localStorage.getItem(k) || '').includes('eins zwei'));
        w.close();
        res({ file, status: (zaehlt && speichert) ? 'OK' : 'DEFEKT', zaehlt, speichert });
      } catch (e) { res({ file, status: 'TESTFAIL', info: e.message }); }
    }, 300);
  });
}

(async () => {
  const files = dateien(process.argv.slice(2));
  const out = [];
  for (const f of files) out.push(await pruefe(f));
  const bad = out.filter(o => o.status === 'DEFEKT' || o.status === 'LOADFAIL');
  if (!bad.length) {
    console.log('✓ Schreibwerkstatt: Wortzähler und Autosave funktionieren (%d Dateien)', out.length);
    process.exit(0);
  }
  console.log('⛔ Schreibwerkstatt defekt in %d von %d Dateien:', bad.length, out.length);
  bad.forEach(o => console.log('   %s — Zähler:%s Speichern:%s',
    o.file, o.zaehlt ? 'ok' : 'TOT', o.speichert ? 'ok' : 'TOT (Text geht verloren!)'));
  console.log('   Reparatur: python3 scripts/fix_schreib_init.py <datei> …');
  console.log('              python3 scripts/inject_wc_autosave.py <datei> …  (alte Generation)');
  process.exit(1);
})();
