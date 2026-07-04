#!/usr/bin/env node
/* lt_verify.js — dynamischer Test der Lückentext-Steuer-Buttons (JSDOM).
   Klassifiziert den LT-Tab einer kanonischen Datei:
     RESULT:OK        Lösungen füllt alle Lücken, Neustart leert sie
     RESULT:DEAD      Button(s) vorhanden, aber wirkungslos/werfend
     RESULT:MISSING   kein Lösungen-Button im LT-Abschnitt
     RESULT:SKIP …    nicht kanonisch / kein Container / Adapter-Datei
   Aufruf: NODE_PATH=<repo>/node_modules node scripts/lt_verify.js datei.html
   Exit 0 nur bei OK oder SKIP. */
const fs = require("fs");
const { JSDOM } = require("jsdom");

const file = process.argv[process.argv.length - 1];
const html = fs.readFileSync(file, "utf8");
if (!html.includes("FB-LT-STORY-CSS")) { console.log("RESULT:SKIP nicht-kanonisch"); process.exit(0); }
if (html.includes("lueckenContainer2") || html.includes("blank2")) { console.log("RESULT:SKIP adapter"); process.exit(0); }

const dom = new JSDOM(html, { runScripts: "dangerously", pretendToBeVisual: true });
const w = dom.window, d = w.document;

setTimeout(() => {
  try {
    const bank = d.getElementById("wortbank-luecken");
    if (!bank) { console.log("RESULT:SKIP kein-container"); process.exit(0); }
    const sec = bank.closest(".section") || bank.closest("section");
    if (!sec) { console.log("RESULT:SKIP keine-section"); process.exit(0); }
    const gaps = [...sec.querySelectorAll("input.blank")];
    if (!gaps.length) { console.log("RESULT:SKIP keine-luecken"); process.exit(0); }

    const btns = [...sec.querySelectorAll("button")];
    const loes = btns.find(b => /Lösung/i.test(b.textContent));
    const rst = btns.find(b => /Neustart|Neu starten|Reset/i.test(b.textContent));
    if (!loes) { console.log("RESULT:MISSING kein-loesungen-button gaps=" + gaps.length); process.exit(1); }

    let filled = 0, after = -1;
    try { loes.click(); filled = gaps.filter(i => i.value && i.value.trim()).length; } catch (e) {}
    if (filled !== gaps.length) {
      console.log("RESULT:DEAD loesungen fuellt " + filled + "/" + gaps.length); process.exit(1);
    }
    if (rst) {
      try { rst.click(); after = gaps.filter(i => i.value && i.value.trim() && !i.disabled).length; } catch (e) { after = -2; }
      if (after !== 0) { console.log("RESULT:DEAD neustart leert nicht (rest=" + after + ")"); process.exit(1); }
    } else {
      console.log("RESULT:MISSING kein-neustart-button"); process.exit(1);
    }
    console.log("RESULT:OK gaps=" + gaps.length);
    process.exit(0);
  } catch (e) {
    console.log("RESULT:DEAD runtime " + e.message); process.exit(1);
  }
}, 400);
