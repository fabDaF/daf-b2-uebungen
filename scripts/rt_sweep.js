#!/usr/bin/env node
/* rt_sweep.js — Laufzeit-Crash-Sweep (JSDOM) über beliebig viele HTML-Dateien in EINEM
   Node-Prozess (vermeidet Node-Startup-Overhead pro Datei bei großen Repos).

   Lädt jede Datei mit runScripts:'dangerously', sammelt window-'error'-Events, klickt
   danach alle Nav-Buttons (Tab-Wechsel deckt Lazy-Init-Crashes auf), feuert 'input' auf
   allen <input>-Feldern und klickt alle [onclick]-Elemente — echte ReferenceError/
   TypeError-Crashes bleiben übrig, die den Rest der Interaktivität lahmlegen.

   WICHTIG: url MUSS eine echte http(s)-Origin sein (nicht file://, nicht Default) —
   sonst wirft localStorage einen SecurityError auf jeder Seite und erzeugt Kaskaden-
   Falschalarme (Lehre aus project_b1-runtime-tdz-fund-2026-06-29).

   Aufruf: node scripts/rt_sweep.js datei1.html datei2.html …
           node scripts/rt_sweep.js --list dateiliste.txt   (eine Datei pro Zeile)
   Ausgabe: eine Zeile pro Datei — "OK <pfad>" oder "CRASH <pfad> :: <fehler1> | <fehler2> …"
   Exit-Code 1, wenn mindestens ein CRASH gefunden wurde. */
const fs = require("fs");
const path = require("path");
const { JSDOM, VirtualConsole } = require("jsdom");

function collectFiles(argv) {
  if (argv[0] === "--list") {
    return fs.readFileSync(argv[1], "utf8").split("\n").map(s => s.trim()).filter(Boolean);
  }
  return argv;
}

function testFile(file) {
  return new Promise((resolve) => {
    let html;
    try {
      html = fs.readFileSync(file, "utf8");
    } catch (e) {
      resolve({ file, status: "SKIP", errors: ["Datei nicht lesbar: " + e.message] });
      return;
    }
    const errors = [];
    // Eigene VirtualConsole pro Datei: unterdrückt harmlose "Not implemented"-Meldungen
    // (scrollTo, canvas, …), fängt aber "jsdomError"-Events ab. WICHTIG (Fund 2026-07-05,
    // B1.1-Sweep, DE_B1_3033R): synchrone Top-Level-Script-Fehler (z.B. ein Crash in einer
    // sofort aufgerufenen initXyz()-Funktion, NICHT innerhalb eines Event-Handlers) laufen
    // NICHT über window.addEventListener('error', …) — jsdom meldet sie ausschließlich als
    // "jsdomError" auf der VirtualConsole. Eine stille VirtualConsole (kein Listener) macht
    // genau diese Klasse von Bugs unsichtbar: der Sweep meldet fälschlich "OK", obwohl die
    // komplette restliche Init-Kette (spätere initXyz()-Aufrufe im selben <script>-Block)
    // nie ausgeführt wurde. Nur Meldungen mit "Uncaught" sind echte Skript-Crashes; alle
    // anderen jsdomError-Typen (Ressourcen-/CSS-/"Not implemented"-Meldungen) bleiben still.
    const vc = new VirtualConsole();
    vc.on("jsdomError", (e) => {
      const msg = String((e && e.message) || e);
      if (msg.indexOf("Uncaught") !== -1) errors.push(msg.split("\n")[0]);
    });
    let dom;
    try {
      dom = new JSDOM(html, {
        runScripts: "dangerously",
        pretendToBeVisual: true,
        virtualConsole: vc,
        url: "https://rtsweep.local/" + encodeURIComponent(path.basename(file)),
      });
    } catch (e) {
      resolve({ file, status: "CRASH", errors: ["JSDOM-Ladefehler: " + e.message] });
      return;
    }
    const w = dom.window;
    w.addEventListener("error", (e) => {
      const msg = (e.error && (e.error.stack || e.error.message)) || e.message || "unbekannter Fehler";
      errors.push(String(msg).split("\n")[0]);
    });
    // Browser-APIs, die JSDOM nicht implementiert, aber die legitim benutzt werden
    // (kein Bug in der Lektion) — SYNCHRON direkt nach der Konstruktion setzen: inline
    // <script>-Ausführung ist in JSDOM intern über eine ResourceQueue auf den nächsten
    // Tick verschoben, läuft also NACH diesem synchronen Block, aber VOR dem setTimeout
    // unten. Reihenfolge ist entscheidend, sonst greifen die Stubs zu spät.
    try {
      w.confirm = () => true;
      w.alert = () => {};
      w.scrollTo = () => {};
      if (w.Element && !w.Element.prototype.scrollIntoView) {
        w.Element.prototype.scrollIntoView = () => {};
      }
      w.matchMedia = w.matchMedia || (() => ({
        matches: false, media: "", addListener() {}, removeListener() {},
        addEventListener() {}, removeEventListener() {}, dispatchEvent() { return false; },
      }));
      if (!w.navigator.clipboard) {
        Object.defineProperty(w.navigator, "clipboard", {
          value: { writeText: () => Promise.resolve(), readText: () => Promise.resolve("") },
          configurable: true,
        });
      }
      if (typeof w.fetch !== "function") {
        w.fetch = () => Promise.resolve({
          ok: true, status: 200,
          json: () => Promise.resolve({ success: true }),
          text: () => Promise.resolve("ok"),
        });
      }
    } catch (e) {}

    setTimeout(() => {
      try {
        const d = w.document;
        // 1) Alle Nav-Buttons klicken (deckt Lazy-Tab-Init-Crashes auf).
        d.querySelectorAll(".nav-btn, [class*='nav-btn']").forEach((btn) => {
          try { btn.click(); } catch (e) { errors.push("nav-click: " + e.message); }
        });
        // 2) Auf jedem Input ein 'input'-Event feuern (Live-Feedback-Handler triggern).
        d.querySelectorAll("input").forEach((inp) => {
          try {
            inp.value = inp.value || "x";
            inp.dispatchEvent(new w.Event("input", { bubbles: true }));
          } catch (e) { errors.push("input-event: " + e.message); }
        });
        // 3) Alle [onclick]-Elemente klicken (Lösungen-/Reset-/Check-Buttons etc.).
        d.querySelectorAll("[onclick]").forEach((el) => {
          try { el.click(); } catch (e) { errors.push("onclick: " + e.message); }
        });
      } catch (e) {
        errors.push("sweep-fehler: " + e.message);
      }
      // Nach den Interaktionen noch einen Tick warten, falls async Handler nachträglich werfen.
      setTimeout(() => {
        try { dom.window.close(); } catch (e) {}
        const uniq = [...new Set(errors)];
        resolve({ file, status: uniq.length ? "CRASH" : "OK", errors: uniq });
      }, 150);
    }, 350);
  });
}

async function main() {
  const files = collectFiles(process.argv.slice(2));
  let anyCrash = false;
  for (const f of files) {
    let r = await testFile(f);
    // Re-Test-Bestätigung: ein CRASH wird nur gemeldet, wenn er reproduzierbar ist —
    // vereinzelt beobachteter Timing-Fluke (jsdom-interne ResourceQueue) sonst als
    // Falsch-Positiv. Zwei weitere Versuche; nur wenn ALLE 3 crashen, ist es echt.
    if (r.status === "CRASH") {
      const r2 = await testFile(f);
      const r3 = (r2.status === "CRASH") ? await testFile(f) : null;
      if (r2.status !== "CRASH" || (r3 && r3.status !== "CRASH")) {
        r = { file: f, status: "OK", errors: [] }; // Fluke — nicht reproduzierbar
      }
    }
    if (r.status === "CRASH") anyCrash = true;
    if (r.errors.length) {
      console.log(r.status + " " + r.file + " :: " + r.errors.join(" | "));
    } else {
      console.log(r.status + " " + r.file);
    }
  }
  process.exit(anyCrash ? 1 : 0);
}

main();
