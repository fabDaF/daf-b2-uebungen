/* FB-LT-V1 — kanonischer Vokabel-Lückentext nach LUECKENTEXT-SKILL-SPEC v1.0.
   NUR für Wortschatz-Lücken (V/R/X): die Wortbank zeigt die Vollformen (= Antworten).
   NICHT in G-Dateien einsetzen (dort gilt der Grundform-/Infinitiv-Wortkasten).
   Selbst-installierend, idempotent. Liest die Antworten aus den vorhandenen Lücken-
   Inputs (data-ans/answer), rendert eine gemischte, nicht-klickbare Wortbank mit
   .used-Durchstreichen, setzt ch-Breite, entfernt Anweisungs-/Altboxen, verdrahtet
   case-sensitives Live-Feedback. */
(function () {
  "use strict";
  if (window.__fbLtV1) return;
  window.__fbLtV1 = true;

  var GAP = /(^|\s)(luecken-inp|gap-inp|luecke-inp|lt-input|gap-input|blank)(\s|$)/;
  function ansOf(i) { var d = i.dataset || {}; return d.ans || d.answer || d.loesung || d.sol || ""; }
  function isGap(i) { return i.tagName === "INPUT" && GAP.test(i.className || "") && ansOf(i) !== ""; }
  function shuffle(a) { for (var i = a.length - 1; i > 0; i--) { var j = Math.floor(Math.random() * (i + 1)), t = a[i]; a[i] = a[j]; a[j] = t; } return a; }

  function sections() {
    var out = [], nodes = document.querySelectorAll(".section, .tab, .tab-content, .sec, .tab-pane");
    Array.prototype.forEach.call(nodes, function (n) {
      if (n.querySelector(".section, .tab, .tab-content, .sec, .tab-pane")) return;
      var gaps = Array.prototype.filter.call(n.querySelectorAll("input"), isGap);
      if (gaps.length >= 2) out.push(n);
    });
    return out;
  }
  function removeClutter(sec) {
    Array.prototype.forEach.call(sec.querySelectorAll(".hilfe-box, .wortkasten, .wortbank-label"), function (w) {
      if (!w.classList.contains("fb-lt-bank")) w.remove();
    });
  }
  function ensureBank(sec) {
    var bank = sec.querySelector(".wortbank");
    if (bank) { bank.classList.add("fb-lt-bank"); return bank; }
    bank = document.createElement("div");
    bank.className = "wortbank fb-lt-bank";
    var host = sec.querySelector(".sec-inner") || sec;
    var gaps = Array.prototype.filter.call(host.querySelectorAll("input"), isGap), anchor = null;
    if (gaps.length) { var n = gaps[0]; while (n && n.parentNode !== host) n = n.parentNode; anchor = n; }
    if (anchor) host.insertBefore(bank, anchor); else host.insertBefore(bank, host.firstChild);
    return bank;
  }
  function updateUsed(sec, bank) {
    var solved = Array.prototype.filter.call(sec.querySelectorAll("input"), function (i) { return isGap(i) && i.value === ansOf(i); }).map(function (i) { return i.value; });
    var rem = solved.slice();
    Array.prototype.forEach.call(bank.querySelectorAll(".wortbank-chip"), function (c) {
      var k = rem.indexOf(c.textContent);
      if (k >= 0) { c.classList.add("used"); rem.splice(k, 1); } else c.classList.remove("used");
    });
  }
  function live(i, sec, bank) {
    var val = i.value, ans = ansOf(i);
    i.classList.remove("correct", "wrong", "ok", "no");
    if (val) { if (val === ans) i.classList.add("correct"); else if (!ans.startsWith(val)) i.classList.add("wrong"); }
    updateUsed(sec, bank);
  }
  function build() {
    sections().forEach(function (sec) {
      var gaps = Array.prototype.filter.call(sec.querySelectorAll("input"), isGap);
      if (gaps.length < 2) return;
      removeClutter(sec);
      var bank = ensureBank(sec);
      var answers = gaps.map(ansOf);
      var sig = answers.slice().sort().join("|");
      if (bank.getAttribute("data-sig") !== sig) {
        bank.setAttribute("data-sig", sig);
        bank.innerHTML = "";
        shuffle(answers.slice()).forEach(function (w) {
          var c = document.createElement("span"); c.className = "wortbank-chip"; c.textContent = w; bank.appendChild(c);
        });
      }
      gaps.forEach(function (i) {
        i.placeholder = "";
        i.style.width = (ansOf(i).length + 4) + "ch";
        if (!i.__fbWired) { i.__fbWired = true; i.addEventListener("input", function () { live(i, sec, bank); }); }
      });
      updateUsed(sec, bank);
    });
  }
  function run() { setTimeout(build, 0); setTimeout(build, 150); }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", run); else run();
  document.addEventListener("click", function (e) { if (e.target && e.target.closest && e.target.closest(".nav-btn")) setTimeout(build, 150); });
})();
