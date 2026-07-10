/* smoke_test.js — Laufzeit-Smoke-Test für DaF-Lektionen (node + jsdom).
 *
 * Lädt jede angegebene HTML-Datei in jsdom, führt ihre Inline-Scripts aus und
 * meldet Lade-Zeit-Fehler (ReferenceError/TypeError), die die Init-Kette
 * abbrechen lassen — genau die Klasse, die Tabs/Übungen tot macht, ohne dass
 * node --check etwas merkt.
 *
 * Browser-APIs, die jsdom fehlen (matchMedia, IntersectionObserver,
 * ResizeObserver), werden polyfüllt, damit sie KEINE Fehlalarme erzeugen.
 *
 * Aufruf:  node scripts/smoke_test.js datei1.html [datei2.html …]
 * Exit 1, wenn mindestens eine Datei einen Laufzeitfehler wirft; sonst 0.
 * Wirft selbst, wenn jsdom nicht installiert ist (der Python-Wrapper fängt das
 * ab und überspringt das Gate).
 */
const { JSDOM, VirtualConsole } = require("jsdom");
const fs = require("fs");

const files = process.argv.slice(2).filter((f) => f.endsWith(".html"));
const BAD = /is not defined|is not a function|Cannot read|Cannot set/;

function poly(w) {
  w.matchMedia = (q) => ({ matches: false, media: q, onchange: null,
    addListener() {}, removeListener() {}, addEventListener() {}, removeEventListener() {}, dispatchEvent() { return false; } });
  const Obs = class { observe() {} unobserve() {} disconnect() {} takeRecords() { return []; } };
  w.IntersectionObserver = w.IntersectionObserver || Obs;
  w.ResizeObserver = w.ResizeObserver || Obs;
  if (!w.scrollTo) w.scrollTo = () => {};
}

const bad = [];
for (const fp of files) {
  let html;
  try { html = fs.readFileSync(fp, "utf8"); } catch (e) { continue; }
  html = html.replace(/data:[^"')]*?base64,[A-Za-z0-9+/=\s]+/g, "data:x");
  const errs = [];
  const vc = new VirtualConsole();
  vc.on("jsdomError", (e) => {
    const m = e.detail ? (e.detail.message || "") : String(e.message || "");
    if (BAD.test(m)) errs.push(m.split("\n")[0]);
  });
  try {
    const dom = new JSDOM(html, { runScripts: "dangerously", pretendToBeVisual: true,
      virtualConsole: vc, url: "https://x/" + fp, beforeParse: poly });
    try { dom.window.close(); } catch (e) {}
  } catch (e) {
    bad.push([fp, "PARSE/LOAD: " + e.message]); continue;
  }
  if (errs.length) bad.push([fp, errs[0]]);
}

if (bad.length) {
  console.log(`✗ ${bad.length} Datei(en) mit Laufzeitfehler beim Laden (Init bricht ab):`);
  bad.forEach((b) => console.log(`    ${b[0]}  ->  ${b[1]}`));
  process.exit(1);
}
console.log(`✓ Kein Laufzeitfehler beim Laden (${files.length} Dateien geprüft).`);
process.exit(0);
