#!/usr/bin/env node
/* check_js_syntax.js — Syntax-Check aller inline <script>-Blöcke einer HTML-Datei.
   Nutzt new Function(body) — parst, führt aber NICHT aus. Meldet SyntaxError mit Blocknummer.
   Aufruf: node scripts/check_js_syntax.js datei.html [...]
   Exit 0 wenn alle Blöcke sauber parsen, sonst 1. */
const fs = require("fs");
let bad = 0;
for (const file of process.argv.slice(2)) {
  const html = fs.readFileSync(file, "utf8");
  const re = /<script(?![^>]*\bsrc=)[^>]*>([\s\S]*?)<\/script>/gi;
  let m, i = 0, fileBad = false;
  while ((m = re.exec(html))) {
    i++;
    const body = m[1];
    if (!body.trim()) continue;
    try {
      new Function(body);
    } catch (e) {
      console.log(file + ": SYNTAX-FEHLER in Script-Block #" + i + ": " + e.message);
      fileBad = true;
    }
  }
  if (!fileBad) console.log(file + ": OK (" + i + " Script-Block(e))");
  else bad++;
}
process.exit(bad ? 1 : 0);
