#!/usr/bin/env node
/* JSDOM-Funktionstest für den geführten Gerüst-Modus (Drag&Drop-Pfad, Familie B):
   1. richtiger Chip -> grün + fixiert, 2. falscher Chip -> rot + Rücksprung,
   3. kompletter Satz -> Punkt + ✓-Feedback, 4. fixierter Chip nicht erneut platzierbar. */
const { JSDOM } = require('/tmp/node_modules/jsdom');
const fs = require('fs');
const file = process.argv[2];
const html = fs.readFileSync(file, 'utf8');

const dom = new JSDOM(html, { runScripts: 'dangerously', pretendToBeVisual: true, url: 'https://b1.daf.frankburkert-daf.de/test.html' });
const w = dom.window, doc = w.document;

function drag(chip, target){
  const ds = new w.Event('dragstart', { bubbles: true, cancelable: true });
  ds.dataTransfer = { effectAllowed: '', setData(){}, getData(){ return ''; } };
  chip.dispatchEvent(ds);
  const dp = new w.Event('drop', { bubbles: true, cancelable: true });
  dp.dataTransfer = ds.dataTransfer;
  target.dispatchEvent(dp);
}

setTimeout(() => {
  try {
    if (typeof w.initSatzbau === 'function') w.initSatzbau();
    const data = w.satzbauData;
    const row0 = doc.getElementById('sb-row-0');
    const bank0 = doc.getElementById('sb-bank-0');
    if (!row0 || !bank0) { console.error('FEHLER: sb-row-0/sb-bank-0 fehlen'); process.exit(1); }

    const positions = () => [...row0.children].filter(n => n.classList.contains('sb-gap') || n.classList.contains('chip'));
    const valid = (typeof data[0].valid[0] === 'string') ? [data[0].valid] : data[0].valid;
    const sol = valid[0];
    const gapIdx = positions().map((p, k) => p.classList.contains('sb-gap') ? k : -1).filter(k => k >= 0);
    const bankChips = () => [...bank0.querySelectorAll('.chip')];

    // Test 0: FALSCHEN, kleingeschriebenen Chip an Satzposition 0 ziehen —
    // er wird dort großgeschrieben angezeigt, muss aber KLEIN in die Bank zurückkehren
    const slot0 = positions()[gapIdx[0]];
    const lower = c => c.dataset.orig.charAt(0) === c.dataset.orig.charAt(0).toLowerCase();
    const decoy = bankChips().find(c => c.dataset.orig !== sol[gapIdx[0]] && lower(c) && !valid.some(o => o[gapIdx[0]] === c.dataset.orig));
    let t0 = 'SKIP (kein passender Köder-Chip)';
    if (decoy) {
      drag(decoy, slot0);
      const capShown = decoy.textContent.charAt(0) === decoy.textContent.charAt(0).toUpperCase();
      t0 = { capShown, done: false };
    }

    // Test 1: richtigen Chip in die erste Lücke ziehen (nach Rücksprung des Köders)
    setTimeout(() => {
      if (decoy && typeof t0 === 'object') {
        const backInBank = decoy.parentElement === bank0;
        const lowerAgain = decoy.textContent === decoy.dataset.orig;
        const pass = t0.capShown && backInBank && lowerAgain;
        console.log('Test 0 (Pos-0-Köder: groß gezeigt, klein zurück):', pass ? 'PASS' : 'FAIL',
          t0.capShown ? '' : '(wurde nicht großgeschrieben)',
          backInBank ? '' : '(nicht in Bank)',
          lowerAgain ? '' : '(Bank-Text: ' + decoy.textContent + ' statt ' + decoy.dataset.orig + ')');
        t0 = pass;
      } else { console.log('Test 0:', t0); t0 = true; }

    const chip = bankChips().find(c => c.dataset.orig === sol[gapIdx[0]]);
    drag(chip, slot0);
    const t1 = chip.classList.contains('correct') && chip.dataset.fixed === '1' && chip.closest('.sb-gap') === slot0;
    console.log('Test 1 (richtig -> grün+fixiert):', t1 ? 'PASS' : 'FAIL');

    // Test 2: falschen Chip in die zweite Lücke ziehen
    const slot1 = positions()[gapIdx[1]];
    const wrong = bankChips().find(c => c.dataset.orig !== sol[gapIdx[1]]);
    drag(wrong, slot1);
    const t2a = wrong.classList.contains('incorrect') && wrong.closest('.sb-gap') === slot1;
    const fb = doc.getElementById('sb-fb-0');
    const t2fb = fb && /passt hier nicht/.test(fb.textContent);
    setTimeout(() => {
      const t2b = !wrong.classList.contains('incorrect') && wrong.parentElement === bank0;
      console.log('Test 2 (falsch -> rot+Hinweis, dann Rücksprung):', (t2a && t2b && t2fb) ? 'PASS' : 'FAIL', t2a?'':'(rot fehlt)', t2b?'':'(kein Rücksprung)', t2fb?'':'(Feedbacktext fehlt)');

      // Test 3: alle Lücken richtig füllen
      for (const k of gapIdx) {
        const slot = positions()[k];
        if (slot.querySelector('.chip')) continue;
        const c = bankChips().find(x => x.dataset.orig === sol[k]);
        if (!c) { console.error('FAIL: Chip', sol[k], 'fehlt in Bank'); process.exit(1); }
        drag(c, slot);
      }
      const seq = positions().map(p => { const c = p.classList.contains('sb-gap') ? p.querySelector('.chip') : p; return c ? c.dataset.orig : '_'; });
      const komplett = JSON.stringify(seq) === JSON.stringify(sol);
      const punkt = !!row0.querySelector('.sb-punkt');
      const t3 = komplett && punkt && /Korrekt/.test(fb.textContent) && row0.classList.contains('correct');
      console.log('Test 3 (komplett -> Punkt + ✓ Korrekt):', t3 ? 'PASS' : 'FAIL', komplett?'':'(Sequenz: '+seq.join(' ')+')', punkt?'':'(Punkt fehlt)');

      // Test 4: fixierter Chip lässt sich nicht erneut verschieben (draggable=false + Drop-Guard)
      const fixedChip = row0.querySelector('.sb-gap .chip');
      const t4a = fixedChip.draggable === false;
      drag(fixedChip, bank0); // Drop-Guard: dataset.fixed
      const t4b = fixedChip.closest('.sb-gap') !== null;
      console.log('Test 4 (fixiert bleibt fixiert):', (t4a && t4b) ? 'PASS' : 'FAIL');

      // Test 5: Großschreibung Position 0 + Komma klein
      const first = positions()[0];
      const fc = first.classList.contains('sb-gap') ? first.querySelector('.chip') : first;
      const t5 = fc && fc.textContent.charAt(0) === fc.textContent.charAt(0).toUpperCase();
      console.log('Test 5 (Großschreibung Satzanfang):', t5 ? 'PASS' : 'FAIL', '['+(fc?fc.textContent:'?')+']');

      process.exit((t0 === true && t1 && t2a && t2b && t2fb && t3 && t4a && t4b && t5) ? 0 : 1);
    }, 900);
    }, 900); // Ende Test-0-Wrapper (Rücksprung des Köders abwarten)
  } catch (e) { console.error('TESTFEHLER:', e.message); process.exit(1); }
}, 300);
