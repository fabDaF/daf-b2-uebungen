#!/usr/bin/env node
/* Gerüst-Modus-Rollout-Patcher (B1+), zweigleisig: Familie A (chips-/builder-) + B (sb-bank-/sb-row-). */
const fs = require('fs'), vm = require('vm');

const AUX = new Set(('bin bist ist sind seid war warst waren wäre wären habe hast hat haben habt hatte hattest hatten hätte hätten werde wirst wird werden werdet wurde wurden würde würden kann kannst können könnt konnte konnten könnte könnten muss musst müssen müsst musste mussten müsste müssten soll sollst sollen sollt sollte sollten will willst wollen wollt wollte wollten darf darfst dürfen dürft durfte durften dürfte dürften mag magst mögen mögt mochte möchte möchten gibt gab ging kam sah las lief fuhr nahm sprach traf blieb fand stand hielt ließ tut tat rief sang lag saß hieß trug schlug schrieb fiel fing flog schloss verlor zog bot riss schnitt trat starb warf half galt hing klang sprang stieg schien schwieg wuchs lud band bat bog brach drang empfing erschien gewann goss griff hob litt mied pfiff rang roch sank schob schoss schuf schwamm schwand schwor stach stahl stank stieß strich stritt trank verdarb vergaß verlieh verschwand wandte wich wies wog zwang aß betrug ertrug vertrug sein').split(/\s+/));
const PREFIX = new Set('ab an auf aus bei ein los mit nach vor weg zu zurück zusammen weiter fest statt teil um durch über unter wieder her hin dazu hinzu hinaus hinein heraus herein hervor empor entgegen voran voraus vorbei davon daran darauf darunter'.split(/\s+/));
const NOTVERB = new Set('heute gerade bitte ende gegenteil name liste seite stelle frage farbe sprache woche stunde minute leute familie reise küche miete'.split(/\s+/));
function suspectVerb(w){
  const lw = w.toLowerCase();
  if (AUX.has(lw)) return true;
  if (NOTVERB.has(lw)) return false;
  if (w[0] === w[0].toUpperCase() && w[0] !== w[0].toLowerCase()) return false;
  if (/^ge.+(t|en)$/.test(lw)) return true;
  if (/(ieren|en)$/.test(lw) && lw.length > 4) return true;
  if (/(st|t)$/.test(lw) && lw.length > 3) return true;
  if (/(te|ten|tet|test)$/.test(lw) && lw.length > 4) return true;  // Präteritum: machte, vertonte
  if (/(ern|eln)$/.test(lw) && lw.length > 5) return true;           // Infinitive: klettern, handeln
  return false;
}
function extract(html){
  const i = html.indexOf('var satzbauData'); if (i < 0) return null;
  const start = html.indexOf('[', html.indexOf('=', i));
  let d = 0, end = -1;
  for (let p = start; p < html.length; p++){ const c = html[p];
    if (c === '[') d++; else if (c === ']') { d--; if (!d){ end = p; break; } } }
  if (end < 0) return null;
  const sb = {}; vm.createContext(sb);
  try { return vm.runInContext('(' + html.slice(start, end+1) + ')', sb); } catch(e){ return null; }
}
function clamp(n,a,b){ return Math.max(a, Math.min(b,n)); }
function spread(pos,n){ if (pos.length<=n) return pos.slice();
  const out=[]; for(let k=0;k<n;k++) out.push(pos[Math.round(k*(pos.length-1)/(n-1))]);
  return [...new Set(out)]; }
function planSentence(ex){
  if (ex.row) return {skip:'hat schon row'};
  let valid = ex.valid;
  if (!valid || !valid.length) return {flag:'kein valid'};
  if (typeof valid[0] === 'string') valid = [valid];     // Familie A: flach -> normalisieren
  const L = valid[0].length;
  if (L < 5) return {flag:'zu kurz für Gerüst ('+L+' Wörter)'};
  if (!valid.every(v=>v.length===L)) return {flag:'valid-Längen ungleich'};
  // Satzzeichen-Chips (Nebensatz-Training!): beweglich in der Bank, niemals Anker
  const ban = new Set([',','.','!','?',';',':']);
  valid.forEach(v => {                                   // V2: Verb = 2. Konstituente, nicht 2. Wort —
    ban.add(v[1]);                                       // darum Wort 2 immer bannen und Wort 3,
    const w2 = v[2];                                     // wenn es kleingeschrieben ist (mehrteiliges Vorfeld)
    if (w2 && w2[0] === w2[0].toLowerCase()) ban.add(w2);
  });
  valid[0].forEach(w => { if (suspectVerb(w) || PREFIX.has(w.toLowerCase())) ban.add(w); });
  const invariant = [];
  for (let k=1; k<L; k++) if (valid.every(v=>v[k]===valid[0][k])) invariant.push(k);
  const anchorable = invariant.filter(k => !ban.has(valid[0][k]));
  const N = clamp(Math.round(L/3),2,4);
  if (anchorable.length < 2) return {flag:'unter 2 sichere Anker'};
  const chosen = spread(anchorable, Math.min(N, anchorable.length)).sort((a,b)=>a-b);
  const row=[], parts=[];
  for (let k=0;k<L;k++){ if (chosen.includes(k)) row.push(valid[0][k]); else { row.push('_'); parts.push(valid[0][k]); } }
  return {row, parts, flatValid: ex.valid && typeof ex.valid[0]==='string'};
}
const CSS = `
/* ── Gerüst-Modus (B1+): sichtbare Lücken + feste Anker ── */
.sb-gap { display:inline-flex; align-items:center; justify-content:center; min-width:66px; min-height:38px; padding:2px 6px; border:2px dashed #b9a7f0; border-radius:20px; background:#faf8ff; }
.sb-gap.drag-over { border-color:#e67e22; background:#fff5ec; }
.sb-gap .chip { margin:0; }
.chip.sb-locked { background:#eef0ff; border-style:solid; border-color:#c3c9f5; color:#555; cursor:default; }
.chip.sb-locked.correct { background:#27ae60; border-color:#27ae60; color:#fff; }
`;
function addon(cfg, merged){
  var C = JSON.stringify(cfg), M = JSON.stringify(merged);
  return ['',
'<script>',
'/* ── Gerüst-Modus Add-on (B1+) — additiv generiert. Mischt row/parts zur Laufzeit in satzbauData,',
'   hüllt Init/Lösung/Reset. Original-Logik für Sätze ohne row bleibt unberührt. */',
'(function(){',
'  var CFG = ' + C + ';',
'  var SBGAP = ' + M + ';',
'  SBGAP.forEach(function(g){ var ex = satzbauData[g.i]; if (!ex) return;',
'    ex.row = g.row; ex.parts = g.parts;',
'    if (typeof ex.valid[0] === "string") ex.valid = [ex.valid];',
'  });',
'  if (typeof window.sbDragged === "undefined") window.sbDragged = null;',
'  function bankEl(i){ return document.getElementById(CFG.bank + i); }',
'  function rowEl(i){ return document.getElementById(CFG.row + i); }',
'  function fbEl(i){ return document.getElementById(CFG.fb + i); }',
'  function cap(w){ return w.charAt(0).toUpperCase() + w.slice(1); }',
'  function positions(row){ return Array.from(row.children).filter(function(n){ return n.classList.contains("sb-gap") || n.classList.contains("chip"); }); }',
'  function chipOf(pos){ return pos.classList.contains("sb-gap") ? pos.querySelector(".chip") : pos; }',
'  function updateCaps(row){ if (!CFG.caps) return;',
'    positions(row).forEach(function(pos,i){ var c = chipOf(pos); if (!c) return;',
'      var o = c.dataset.orig;',
'      var proper = o.charAt(0) === o.charAt(0).toUpperCase() && o.charAt(0) !== o.charAt(0).toLowerCase();',
'      c.textContent = proper ? o : (i === 0 ? cap(o) : o); });',
'  }',
'  function sequence(i){ var row = rowEl(i), seq = [], complete = true;',
'    positions(row).forEach(function(pos){ var c = chipOf(pos); if (c) seq.push(c.dataset.orig); else complete = false; });',
'    return { seq: seq, complete: complete }; }',
'  function clearMarks(i){ var row = rowEl(i);',
'    row.querySelectorAll(".chip").forEach(function(c){ c.classList.remove("correct","incorrect"); });',
'    row.classList.remove("correct","incorrect");',
'    var p = row.querySelector(".sb-punkt"); if (p) p.parentNode.removeChild(p); }',
'  function afterChange(i){',
'    var row = rowEl(i); updateCaps(row);',
'    var fb = fbEl(i), info = sequence(i);',
'    if (!info.complete){ clearMarks(i); if (fb){ fb.textContent=""; fb.className="satzbau-feedback"; } return; }',
'    setTimeout(function(){',
'      if (typeof timerAutoStart === "function") timerAutoStart(CFG.tab);',
'      var fresh = sequence(i);',
'      var ok = satzbauData[i].valid.some(function(v){ return JSON.stringify(v) === JSON.stringify(fresh.seq); });',
'      var p = row.querySelector(".sb-punkt"); if (p) p.parentNode.removeChild(p);',
'      if (ok){',
'        row.querySelectorAll(".chip").forEach(function(c){ c.classList.remove("incorrect"); c.classList.add("correct"); });',
'        var punkt = document.createElement("span"); punkt.className = "sb-punkt";',
'        punkt.textContent = satzbauData[i].punct || "."; row.appendChild(punkt);',
'        row.classList.add("correct"); row.classList.remove("incorrect");',
'        if (fb){ fb.className = "satzbau-feedback correct"; fb.textContent = "✓ Korrekt!"; }',
'        if (typeof sbCheckAllDone === "function") sbCheckAllDone();',
'      } else {',
'        row.querySelectorAll(".chip").forEach(function(c){ c.classList.remove("correct","incorrect"); });',
'        row.querySelectorAll(".sb-gap .chip").forEach(function(c){ c.classList.add("incorrect"); });',
'        row.classList.add("incorrect"); row.classList.remove("correct");',
'        if (fb){ fb.className = "satzbau-feedback incorrect"; fb.textContent = "✗ Noch nicht richtig – verschiebe die Wörter!"; }',
'      }',
'    }, 450);',
'  }',
'  /* Geführter Modus (B1, 2026-06-10): Sofort-Feedback pro Chip-Platzierung.',
'     Richtig (konsistent mit mind. einer valid-Reihenfolge) -> grün + fixiert.',
'     Falsch -> rot + Rücksprung in die Bank nach 800 ms. */',
'  function toBank(i, chip){',
'    chip.textContent = chip.dataset.orig;  // Kleinschreibung wiederherstellen — Bank darf den Satzanfang nicht verraten',
'    bankEl(i).appendChild(chip);',
'  }',
'  function consistent(i){',
'    var pos = positions(rowEl(i));',
'    var v = satzbauData[i].valid;',
'    return v.some(function(o){',
'      for (var k = 0; k < pos.length; k++){ var c = chipOf(pos[k]); if (c && c.dataset.orig !== o[k]) return false; }',
'      return true; });',
'  }',
'  function finishRow(i){',
'    var row = rowEl(i), fb = fbEl(i);',
'    var p = row.querySelector(".sb-punkt"); if (p) p.parentNode.removeChild(p);',
'    var punkt = document.createElement("span"); punkt.className = "sb-punkt";',
'    punkt.textContent = satzbauData[i].punct || "."; row.appendChild(punkt);',
'    row.classList.add("correct"); row.classList.remove("incorrect");',
'    if (fb){ fb.className = "satzbau-feedback correct"; fb.textContent = "✓ Korrekt!"; }',
'    if (typeof sbCheckAllDone === "function") sbCheckAllDone();',
'  }',
'  function placeJudge(i, chip){',
'    if (typeof timerAutoStart === "function") timerAutoStart(CFG.tab);',
'    var row = rowEl(i); updateCaps(row);',
'    var fb = fbEl(i);',
'    if (consistent(i)){',
'      chip.classList.remove("incorrect"); chip.classList.add("correct");',
'      chip.dataset.fixed = "1"; chip.draggable = false;',
'      if (sequence(i).complete){ finishRow(i); }',
'      else if (fb){ fb.className = "satzbau-feedback"; fb.textContent = ""; }',
'    } else {',
'      chip.classList.add("incorrect");',
'      if (fb){ fb.className = "satzbau-feedback incorrect"; fb.textContent = "✗ Das passt hier nicht!"; }',
'      setTimeout(function(){',
'        chip.classList.remove("incorrect");',
'        if (!chip.dataset.fixed && chip.closest(".sb-gap")) toBank(i, chip);',
'        updateCaps(rowEl(i));',
'        if (fb && /incorrect/.test(fb.className)){ fb.className = "satzbau-feedback"; fb.textContent = ""; }',
'      }, 800);',
'    }',
'  }',
'  function makeChip(word, i){',
'    var chip = document.createElement("div");',
'    var isPunct = [",",".","!","?",";",":"].indexOf(word) !== -1;',
'    chip.className = "chip" + (isPunct ? " punct-chip" : ""); chip.textContent = word; chip.draggable = true;',
'    chip.dataset.orig = word; chip.dataset.word = word; chip.dataset.sbIdx = String(i);',
'    chip.addEventListener("dragstart", function(e){ if (chip.dataset.fixed){ e.preventDefault(); return; } window.sbDragged = chip; if (typeof timerAutoStart === "function") timerAutoStart(CFG.tab); e.dataTransfer.effectAllowed = "move"; });',
'    if (CFG.click) chip.addEventListener("click", function(){',
'      if (chip.dataset.fixed) return;',
'      if (typeof timerAutoStart === "function") timerAutoStart(CFG.tab);',
'      var inSlot = chip.closest(".sb-gap");',
'      if (inSlot){ toBank(i, chip); updateCaps(rowEl(i)); return; }',
'      var free = Array.from(rowEl(i).querySelectorAll(".sb-gap")).find(function(s){ return !s.querySelector(".chip"); });',
'      if (free){ free.appendChild(chip); placeJudge(i, chip); }',
'    });',
'    return chip;',
'  }',
'  function makeLocked(word){',
'    var chip = document.createElement("div");',
'    chip.className = "chip sb-locked"; chip.textContent = word;',
'    chip.dataset.orig = word; chip.dataset.word = word; chip.dataset.locked = "1";',
'    return chip;',
'  }',
'  function makeSlot(i){',
'    var slot = document.createElement("div"); slot.className = "sb-gap";',
'    slot.addEventListener("dragover", function(e){ e.preventDefault(); if (window.sbDragged) slot.classList.add("drag-over"); });',
'    slot.addEventListener("dragleave", function(){ slot.classList.remove("drag-over"); });',
'    slot.addEventListener("drop", function(e){',
'      e.preventDefault(); slot.classList.remove("drag-over");',
'      var d = window.sbDragged; if (!d || d.dataset.sbIdx !== String(i) || d.dataset.locked || d.dataset.fixed) return;',
'      if (slot.querySelector(".chip")) return;  // Lücke schon belegt',
'      slot.appendChild(d); window.sbDragged = null; placeJudge(i, d);',
'    });',
'    return slot;',
'  }',
'  function registerBank(bank, i){',
'    bank.addEventListener("dragover", function(e){ e.preventDefault(); });',
'    bank.addEventListener("drop", function(e){',
'      e.preventDefault(); var d = window.sbDragged;',
'      if (!d || d.dataset.sbIdx !== String(i) || d.dataset.locked || d.dataset.fixed) return;',
'      toBank(i, d); window.sbDragged = null; updateCaps(rowEl(i));',
'    });',
'  }',
'  function freshEl(id){ var el = document.getElementById(id); if (!el) return null;',
'    var c = el.cloneNode(false); el.parentNode.replaceChild(c, el); return c; }',
'  function rebuild(i){',
'    var ex = satzbauData[i]; if (!ex || !ex.row) return;',
'    var bank = freshEl(CFG.bank + i), row = freshEl(CFG.row + i);',
'    if (!bank || !row) return;',
'    var fb = fbEl(i); if (fb){ fb.textContent = ""; fb.className = "satzbau-feedback"; }',
'    var mov = ex.parts.slice();',
'    for (var k = mov.length - 1; k > 0; k--){ var j = Math.floor(Math.random()*(k+1)); var t = mov[k]; mov[k] = mov[j]; mov[j] = t; }',
'    mov.forEach(function(w){ bank.appendChild(makeChip(w, i)); });',
'    ex.row.forEach(function(tok){ row.appendChild(tok === "_" ? makeSlot(i) : makeLocked(tok)); });',
'    registerBank(bank, i);',
'    ensureButtons(i);',
'  }',
'  function rebuildAll(){ satzbauData.forEach(function(ex,i){ if (ex.row) rebuild(i); }); }',
'  function showSol(i){',
'    rebuild(i);',
'    var row = rowEl(i), bank = bankEl(i), sol = satzbauData[i].valid[0];',
'    var pool = Array.from(bank.querySelectorAll(".chip"));',
'    positions(row).forEach(function(pos,k){',
'      if (!pos.classList.contains("sb-gap")) return;',
'      var ix = pool.findIndex(function(c){ return c.dataset.orig === sol[k]; });',
'      if (ix >= 0){ while (pos.firstChild) pos.removeChild(pos.firstChild); pos.appendChild(pool[ix]); pool.splice(ix,1); }',
'    });',
'    row.querySelectorAll(".sb-gap .chip").forEach(function(c){ c.classList.add("correct"); c.dataset.fixed = "1"; c.draggable = false; });',
'    updateCaps(row);',
'    finishRow(i);',
'  }',
'  function ensureButtons(i){',
'    if (document.getElementById("sb-btns-" + i)) return;',
'    var anchor = fbEl(i) || rowEl(i); if (!anchor) return;',
'    var item = (anchor.closest ? anchor.closest(".satzbau-item") : null) || anchor.parentNode;',
'    if (item && [].some.call(item.querySelectorAll("button"), function(b){',
'      return /(Lösen|Lösung|Neustart)/.test(b.textContent); })) return;  // native Buttons vorhanden',
'    var box = document.createElement("div");',
'    box.id = "sb-btns-" + i;',
'    box.style.cssText = "display:flex;gap:8px;margin:6px 0 14px 0;";',
'    var b1 = document.createElement("button"); b1.type = "button"; b1.className = "btn"; b1.textContent = "Lösen";',
'    b1.addEventListener("click", function(){ showSol(i); });',
'    var b2 = document.createElement("button"); b2.type = "button"; b2.className = "btn"; b2.textContent = "↺ Neustart";',
'    b2.addEventListener("click", function(){ rebuild(i); });',
'    box.appendChild(b1); box.appendChild(b2);',
'    anchor.parentNode.insertBefore(box, anchor.nextSibling);',
'  }',
'  ["initSatzbau","buildSatzbau"].forEach(function(fn){',
'    if (typeof window[fn] === "function"){ var o = window[fn];',
'      window[fn] = function(){ o.apply(this, arguments); rebuildAll(); }; }',
'  });',
'  if (typeof window.sbReset === "function" && window.sbReset.length === 0){',
'    var orall = window.sbReset;',
'    window.sbReset = function(){ orall.apply(this, arguments); rebuildAll(); };',
'  }',
'  if (typeof window.sbResetOne === "function"){',
'    var orst = window.sbResetOne;',
'    window.sbResetOne = function(i){ if (satzbauData[i] && satzbauData[i].row){ rebuild(i); return; } orst.apply(this, arguments); };',
'  }',
'  if (typeof window.sbShowSolution === "function"){',
'    var osol = window.sbShowSolution;',
'    window.sbShowSolution = function(i){ if (satzbauData[i] && satzbauData[i].row){ showSol(i); return; } osol.apply(this, arguments); };',
'  }',
'  var probe = rowEl(0) || bankEl(0);',
'  if (probe && probe.children.length) rebuildAll();',
'})();',
'</scr' + 'ipt>'].join('\n');
}
// ---- main ----
const file = process.argv[2];
const write = process.argv.includes('--write');
let html = fs.readFileSync(file, 'utf8');
const report = { file, fam: null, sentences: 0, converted: 0, flags: [], skip: null };
function out(){ console.log(JSON.stringify(report)); }
html = html.replace(/\n?<script>\n\/\* ── Gerüst-Modus Add-on[\s\S]*?<\/script>/, '');
if (/\brow:\s*\[/.test(html)) { report.skip = 'schon Gerüst (inline row)'; out(); process.exit(0); }
const data = extract(html);
if (!data) { report.skip = 'satzbauData nicht parsebar'; out(); process.exit(0); }
let fam = null;
if (html.includes("'sb-bank-'") || html.includes('"sb-bank-"') || html.includes('id="sb-bank-')) fam = 'B';
else if (html.includes("'builder-'") || html.includes('"builder-"') || html.includes("builder-'+")) fam = 'A';
if (!fam) { report.skip = 'unbekanntes ID-Schema'; out(); process.exit(0); }
report.fam = fam;
const initFn = ['initSatzbau','buildSatzbau'].find(f => html.includes('function ' + f));
if (!initFn) { report.skip = 'keine Init-Funktion'; out(); process.exit(0); }
if (!html.includes('function sbShowSolution')) { report.note = 'kein natives sbShowSolution — Add-on-Buttons übernehmen'; }
let m = html.match(/sbDragged\s*=\s*chip;\s*timerAutoStart\((\d+)\)/)
     || html.match(/function sbCheckAuto[\s\S]{0,800}?timerAutoStart\((\d+)\)/)
     || html.match(/sbReset(?:One)?\([^)]*\);\s*resetTimer\((\d+)\)/)
     || html.match(/onclick="show(?:Section|Tab)\((\d+)\)"[^>]{0,200}>[\s\S]{0,200}?Satzbau/);
if (!m) { report.skip = 'SBTAB nicht ermittelbar'; out(); process.exit(0); }
const cfg = fam === 'B'
  ? { bank:'sb-bank-', row:'sb-row-', fb:'sb-fb-', caps:true,  click:false, tab:+m[1] }
  : { bank:'chips-',   row:'builder-', fb:'sfb-',  caps:false, click:true,  tab:+m[1] };
const merged = [];
data.forEach((ex, i) => {
  report.sentences++;
  const p = planSentence(ex);
  if (p.skip) return;
  if (p.flag) { report.flags.push('Satz ' + (i+1) + ': ' + p.flag); return; }
  merged.push({ i, row: p.row, parts: p.parts });
});
report.converted = merged.length;
if (!merged.length) { report.skip = 'kein Satz konvertierbar'; out(); process.exit(0); }
if (!html.includes('.sb-gap {')) html = html.replace('</style>', CSS + '</style>');
html = html.replace(/<\/body>/i, addon(cfg, merged) + '\n</body>');
if (write) fs.writeFileSync(file, html);
out();
