/* ============================================================================
   FB-LT-STORY — kanonische Lückentext-Engine (EINE Quelle der Wahrheit)
   ----------------------------------------------------------------------------
   Mit Frank abgenommen 2026-06-30 (Piloten 1057X Heimweh, 3065G Adjektivdeklination).
   Diese Datei ist die EINZIGE Quelle der mechanischen Lückentext-Logik. Der
   Produzent scripts/inject_lt.py spielt sie (plus die CSS unten) in jede Lektion
   ein — NIE von Hand pro Datei kopieren (sonst driften die Engines, genau der
   Fehler, den wir abschaffen).

   Kanonische Form:
     · zusammenhängende STORY (Serif-Fließtext, Inline-Lücken), KEINE Nummern;
     · GENAU 10 Lücken;  · §7-Wortbank (gemischt, nicht klickbar, .used);
     · case-sensitiv, kein Prüfen-Button (nur Live-Feedback);
     · Variante erkennt sich SELBST:
         - hat eine Lücke data-base  → Grammatik (G): Wortbank zeigt die GRUNDFORM
           (data-base), die Zielform (data-answer) ist nie sichtbar;
         - sonst                     → Wortschatz (V/R/X): Wortbank zeigt die
           Vollform (= data-answer).
     · .used streicht den Chip der getroffenen Lücke durch (G: per data-base) —
       Fortschrittsanzeige, verrät die Zielform nicht (Frank bestätigt 2026-06-30).

   Markup-Vertrag (vom Produzenten erzeugt, vom Gate check_lueckentext.py geprüft):
     <div class="wortbank" id="wortbank-luecken"></div>
     <div id="lueckenContainer" class="luecken-story">
       <p>… <input class="blank" data-answer="ZIELFORM" [data-base="GRUNDFORM"]> …</p>
     </div>

   Timer-Anbindung: die Engine ruft generische Hooks window.fbLtTimerStart()/
   fbLtTimerStop(); der Produzent verdrahtet sie pro Datei auf den richtigen
   Tab-Index (timerAutoStart(N)/timerStop(N)). Fehlen die Hooks, läuft die Engine
   ohne Timer weiter.
   ============================================================================ */

/* ---- KANONISCHE CSS (vom Produzenten mit eingespielt) -----------------------
.luecken-story { font-family: Georgia, 'Times New Roman', serif; font-size: 1.05em; line-height: 2.1; color: #2c2c2c; text-align: justify; background: #f8f9ff; border-left: 4px solid #667eea; border-radius: 0 10px 10px 0; padding: 18px 22px; }
.luecken-story p { margin: 0 0 14px; }
.luecken-story p:last-child { margin-bottom: 0; }
.luecken-story input.blank { font-family: Georgia, 'Times New Roman', serif; border: none; border-bottom: 2px solid #c5cae9; background: transparent; outline: none; font-size: 1em; color: #2c2c2c; text-align: center; padding: 1px 4px; min-width: 4ch; transition: all .2s; }
.luecken-story input.blank:focus { border-bottom-color: #667eea; }
.luecken-story input.blank.correct { border-bottom-color: #27ae60; background: #e8f8f0; color: #27ae60; font-weight: 700; }
.luecken-story input.blank.wrong { border-bottom-color: #e74c3c; background: #fdeaea; color: #e74c3c; }
.wortbank { display:flex; flex-wrap:wrap; gap:8px; padding:14px; background:#f0f0f8; border-radius:10px; min-height:48px; margin-bottom:18px; border:1px dashed #bbb; }
.wortbank-chip { background:white; border:2px solid #667eea; color:#667eea; padding:5px 12px; border-radius:14px; font-weight:500; font-size:0.9em; user-select:none; }
.wortbank-chip.used { opacity:0.35; text-decoration:line-through; }
---------------------------------------------------------------------------- */

(function () {
  "use strict";
  if (window.__fbLtStory) return;
  window.__fbLtStory = true;

  function gaps() {
    return Array.prototype.slice.call(
      document.querySelectorAll('#lueckenContainer input.blank'));
  }
  // Wortbank-Wort einer Lücke: Grundform (G) falls vorhanden, sonst Vollform.
  function wordOf(i) {
    return i.getAttribute('data-base') || i.getAttribute('data-answer') || '';
  }
  function shuffle(a) {
    for (var k = a.length - 1; k > 0; k--) {
      var j = Math.floor(Math.random() * (k + 1));
      var t = a[k]; a[k] = a[j]; a[j] = t;
    }
    return a;
  }

  function update() {
    var bank = document.getElementById('wortbank-luecken');
    if (!bank) return;
    var rem = gaps().filter(function (i) { return i.classList.contains('correct'); })
                    .map(wordOf);
    Array.prototype.slice.call(bank.querySelectorAll('.wortbank-chip')).forEach(function (c) {
      var idx = rem.indexOf(c.textContent);
      if (idx >= 0) { c.classList.add('used'); rem.splice(idx, 1); }
      else { c.classList.remove('used'); }
    });
  }

  function done() {
    var gg = gaps();
    if (gg.length && gg.every(function (i) { return i.classList.contains('correct'); })
        && typeof window.fbLtTimerStop === 'function') window.fbLtTimerStop();
  }

  function live(i) {
    var ans = i.getAttribute('data-answer'), val = i.value;   // case-sensitive, kein trim
    i.classList.remove('correct', 'wrong');
    if (val) {
      if (val === ans) i.classList.add('correct');
      else if (ans.indexOf(val) !== 0) i.classList.add('wrong');
      if (typeof window.fbLtTimerStart === 'function') window.fbLtTimerStart();
    }
    update();
    done();
  }

  function build() {
    var bank = document.getElementById('wortbank-luecken');
    if (!bank) return;
    var gg = gaps();
    if (!gg.length) return;
    gg.forEach(function (i) {
      var a = i.getAttribute('data-answer') || '', b = i.getAttribute('data-base') || '';
      i.placeholder = '';
      i.style.width = (Math.max(a.length, b.length) + 3) + 'ch';
      if (!i.__fbWired) {
        i.__fbWired = true;
        i.addEventListener('input', function () { live(i); });
      }
    });
    var seen = {}, words = [];
    gg.forEach(function (i) { var w = wordOf(i); if (w && !seen[w]) { seen[w] = true; words.push(w); } });
    bank.innerHTML = '';
    shuffle(words).forEach(function (w) {
      var c = document.createElement('span');
      c.className = 'wortbank-chip';
      c.textContent = w;
      bank.appendChild(c);
    });
    update();
  }

  // Öffentliche Hooks für die Steuer-Buttons (Produzent verdrahtet onclick darauf).
  window.fbLtBuild = build;
  window.fbLtShowLoesung = function () {
    gaps().forEach(function (i) {
      i.value = i.getAttribute('data-answer');
      i.classList.add('correct'); i.classList.remove('wrong');
    });
    update();
    if (typeof window.fbLtTimerStop === 'function') window.fbLtTimerStop();
  };
  window.fbLtReset = function () {
    gaps().forEach(function (i) { i.value = ''; i.classList.remove('correct', 'wrong'); });
    build();
  };

  function run() { build(); }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', run);
  else run();
  // Beim Wechsel auf den Lückentext-Tab neu aufbauen (mischt die Wortbank).
  document.addEventListener('click', function (e) {
    if (e.target && e.target.closest && e.target.closest('.nav-btn')) setTimeout(build, 80);
  });
})();
