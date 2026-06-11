#!/usr/bin/env node
/* patch_mc_shuffle.mjs — Verteilt die richtige MC-Antwort deterministisch über alle Positionen.
 *
 * PROBLEM: In vielen DaF-Dateien stand die richtige Antwort fast immer an derselben
 *   Position (meist Index 1). Der Lerner klickt dann blind „die zweite".
 *
 * LÖSUNG (variantenagnostisch): Wir ändern NICHT den Render-Code (der existiert in vielen
 *   Strukturvarianten), sondern PERMUTIEREN die Optionen in den Daten-Arrays selbst und
 *   passen den Korrekt-Index an. Jede Render-Variante funktioniert dadurch unverändert.
 *
 * Erkennung: jedes `var NAME = [ ... ];` dessen Elemente Objekte mit
 *   - einem Array-Feld `opts` ODER `options` (>=2 Strings) UND
 *   - einem numerischen Feld `correct` ODER `answer` im gültigen Bereich
 *   sind. Name egal (MC_DATA, mcData, MC, QUIZ_DATA, MC4_DATA, …).
 *
 * Deterministisch + idempotent: Optionen werden nach md5(frage|optiontext) sortiert.
 *   Re-Lauf ⇒ identische Reihenfolge. Verteilung der richtigen Position ≈ gleichverteilt.
 *
 * Sicherheit:
 *   - Objekte mit einem ZWEITEN Array gleicher Länge wie opts (mögliche parallele
 *     Pro-Option-Daten) werden NICHT angefasst (Desync-Schutz).
 *   - Array wird per JSON re-serialisiert (Schlüsselreihenfolge bleibt, Unicode literal).
 *   - Aufrufer prüft danach node --check + Anführungszeichen und macht bei Bruch rückgängig.
 *
 * Aufruf: node patch_mc_shuffle.mjs <datei.html> [--check]
 *   --check: nur melden, ob sich etwas ändern WÜRDE (kein Schreiben). Exit 0 immer.
 * Ausgabe: Zeile "PATCHED <n_arrays> <n_items> <datei>" oder "SKIP <grund> <datei>".
 */
import fs from 'fs';
import crypto from 'crypto';
import { fileURLToPath } from 'url';

// Direkt aufgerufen (CLI) vs. importiert (Modul)?
const isMain = process.argv[1] && fileURLToPath(import.meta.url) === process.argv[1];
const file = isMain ? process.argv[2] : null;
const checkOnly = process.argv.includes('--check');
let src = file ? fs.readFileSync(file, 'utf8') : '';

function findArrays(text) {
  // Liefert {name,start,end,body} für jedes top-level `var NAME = [ ... ];`
  const out = [];
  const re = /(?:var|let|const)\s+([A-Za-z_$][A-Za-z0-9_$]*)\s*=\s*\[/g;
  let m;
  while ((m = re.exec(text)) !== null) {
    const open = text.indexOf('[', m.index);
    let i = open, depth = 0, inStr = null, esc = false;
    for (; i < text.length; i++) {
      const c = text[i];
      if (inStr) {
        if (esc) { esc = false; }
        else if (c === '\\') { esc = true; }
        else if (c === inStr) { inStr = null; }
        continue;
      }
      if (c === '"' || c === "'" || c === '`') { inStr = c; continue; }
      if (c === '[') depth++;
      else if (c === ']') { depth--; if (depth === 0) break; }
    }
    if (depth === 0) {
      out.push({ name: m[1], open, close: i, literal: text.slice(open, i + 1) });
      re.lastIndex = i + 1;
    }
  }
  return out;
}

function evalArray(literal) {
  try { return (0, eval)('(' + literal + ')'); } catch { return null; }
}

var CORR_KEYS = ['correct', 'answer', 'ans', 'loesung', 'c', 'a', 'ok'];

var TEXT_KEYS = ['text', 'label', 't', 'txt', 'antwort', 'option'];
var FLAG_KEYS = ['correct', 'richtig', 'istRichtig', 'isCorrect', 'right', 'ok'];

function mcKeys(el) {
  // Liefert {optsKey, corrKey, mode} oder null.
  // mode: 'index' (Korrektwert ist Zahl) | 'text' (Korrektwert ist der Antwortstring)
  //     | 'objs' (Optionen sind Objekte {text, correct:bool} — Flag reist mit).
  if (!el || typeof el !== 'object' || Array.isArray(el)) return null;
  var optsKey = Array.isArray(el.opts) ? 'opts' : (Array.isArray(el.options) ? 'options' : null);
  if (!optsKey) return null;
  var opts = el[optsKey];
  if (opts.length < 2) return null;
  // Modus A/B: Optionen sind Strings, Korrektheit in eigenem Feld
  if (opts.every(function (o) { return typeof o === 'string'; })) {
    for (var i = 0; i < CORR_KEYS.length; i++) {
      var k = CORR_KEYS[i];
      if (!(k in el)) continue;
      var v = el[k];
      if (typeof v === 'number' && v >= 0 && v < opts.length) return { optsKey: optsKey, corrKey: k, mode: 'index' };
      if (typeof v === 'string' && opts.indexOf(v) >= 0) return { optsKey: optsKey, corrKey: k, mode: 'text' };
    }
    return null;
  }
  // Modus C: Optionen sind Objekte {textKey, flagKey:bool}
  if (opts.every(function (o) { return o && typeof o === 'object' && !Array.isArray(o); })) {
    var tk = TEXT_KEYS.find(function (t) { return opts.every(function (o) { return typeof o[t] === 'string'; }); });
    var fk = FLAG_KEYS.find(function (fl) { return opts.some(function (o) { return o[fl] === true; }) && opts.every(function (o) { return typeof o[fl] === 'boolean' || o[fl] === undefined; }); });
    if (tk && fk && opts.filter(function (o) { return o[fk] === true; }).length === 1) {
      return { optsKey: optsKey, textKey: tk, flagKey: fk, mode: 'objs' };
    }
  }
  return null;
}

function isMcArray(arr) {
  if (!Array.isArray(arr) || arr.length === 0) return false;
  let good = 0;
  for (const el of arr) { if (mcKeys(el)) good++; }
  return good >= Math.max(2, Math.ceil(arr.length * 0.6));
}

function md5(s) { return crypto.createHash('md5').update(s, 'utf8').digest('hex'); }

function permuteItem(el) {
  const mk = mcKeys(el);
  if (!mk) return false;
  const opts = el[mk.optsKey];
  const seedBase = String(el.frage || el.question || el.q || el.satz || el.text || el.label || el.titel || JSON.stringify(mk.mode === 'objs' ? opts.map(o => o[mk.textKey]) : opts));
  if (mk.mode === 'objs') {
    // Optionen sind Objekte; Flag reist mit. Deterministisch nach Text sortieren.
    const dec = opts.map(o => ({ o, key: md5(seedBase + '|' + o[mk.textKey]) }));
    dec.sort((a, b) => a.key < b.key ? -1 : (a.key > b.key ? 1 : 0));
    const newOpts = dec.map(d => d.o);
    const changed = newOpts.some((o, i) => o !== opts[i]);
    el[mk.optsKey] = newOpts;
    return changed;
  }
  // Desync-Schutz nur im String-Modus: zweites Array gleicher Länge ⇒ Finger weg
  for (const k of Object.keys(el)) {
    if (k !== mk.optsKey && Array.isArray(el[k]) && el[k].length === opts.length) return false;
  }
  const correctText = mk.mode === 'index' ? opts[el[mk.corrKey]] : el[mk.corrKey];
  const decorated = opts.map(o => ({ o, key: md5(seedBase + '|' + o) }));
  decorated.sort((a, b) => a.key < b.key ? -1 : (a.key > b.key ? 1 : 0));
  const newOpts = decorated.map(d => d.o);
  const changed = newOpts.some((o, i) => o !== opts[i]);
  el[mk.optsKey] = newOpts;
  if (mk.mode === 'index') el[mk.corrKey] = newOpts.indexOf(correctText);
  // mode 'text': Korrektwert bleibt der Text — reihenfolge-unabhängig
  return changed;
}

// Wiederverwendbar: nimmt Quelltext, gibt {out, patchedArrays, patchedItems, mcArraysSeen}.
export function patchSource(src) {
  const arrays = findArrays(src);
  let patchedArrays = 0, patchedItems = 0, mcArraysSeen = 0;
  const edits = [];
  for (const a of arrays) {
    if (a.literal.includes('${')) continue; // Template-Interpolation: nicht re-serialisieren
    const data = evalArray(a.literal);
    if (!isMcArray(data)) continue;
    mcArraysSeen++;
    let anyChange = false, items = 0;
    for (const el of data) {
      if (permuteItem(el)) anyChange = true;
      if (el && (Array.isArray(el.opts) || Array.isArray(el.options))) items++;
    }
    if (!anyChange) continue;
    edits.push({ open: a.open, close: a.close, newLiteral: JSON.stringify(data, null, 2) });
    patchedArrays++; patchedItems += items;
  }
  let out = src;
  edits.sort((a, b) => b.open - a.open);
  for (const e of edits) out = out.slice(0, e.open) + e.newLiteral + out.slice(e.close + 1);
  return { out, patchedArrays, patchedItems, mcArraysSeen };
}

// CLI-Modus nur, wenn direkt aufgerufen (nicht beim Import).
if (file) {
  const r = patchSource(src);
  if (r.mcArraysSeen === 0) { console.log('SKIP no-mc-array ' + file); process.exit(0); }
  if (r.patchedArrays === 0) { console.log('SKIP already-distributed ' + file); process.exit(0); }
  if (checkOnly) { console.log('WOULD-PATCH ' + r.patchedArrays + ' ' + r.patchedItems + ' ' + file); process.exit(0); }
  fs.writeFileSync(file, r.out, 'utf8');
  console.log('PATCHED ' + r.patchedArrays + ' ' + r.patchedItems + ' ' + file);
}
