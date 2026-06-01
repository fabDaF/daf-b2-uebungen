/* FB-WORTBANK-MODULE — universelle, format-agnostische Lückentext-Wortbank.
   Liest Antworten zur Laufzeit aus den gerenderten Lücken-Inputs (dataset.ans/answer/...),
   rendert eine NICHT klickbare, gemischte Wortbank und gibt .used-Feedback.
   Greift nicht in die bestehende Seiten-Logik ein; tut nichts, wenn keine Antworten
   gefunden werden oder bereits eine Wortbank existiert. */
(function () {
  "use strict";
  if (window.__fbWortbankInit) return;
  window.__fbWortbankInit = true;

  var ANSWER_KEYS = ["ans", "answer", "sol", "solution", "correct", "loesung", "b"];
  var GAP_CLASS_RE = /(^|\s)(luecken-inp|luecke-inp|luecke-input|luecken-text|luecken-person|luecke-satz|blank|gap-input|gap)(\s|$)/;

  function answerOf(inp) {
    var d = inp.dataset || {};
    for (var i = 0; i < ANSWER_KEYS.length; i++) {
      var v = d[ANSWER_KEYS[i]];
      if (v != null && v !== "") return v;
    }
    return null;
  }

  var WS_TOKEN_RE = /(^|\s)(ws-[\w-]*|wort|art|artikel|plural|de|en|englisch|deutsch)(\s|$)/i;
  function isGapInput(inp) {
    if (inp.tagName !== "INPUT") return false;
    if (!GAP_CLASS_RE.test(inp.className || "")) return false;
    // Wortschatz-Felder ausschließen (eigene Section, aber defensiv)
    var id = inp.id || "";
    if (/^ws[-_]/.test(id)) return false;
    var oi = inp.getAttribute("oninput") || "";
    if (/wortschatz/i.test(oi)) return false;
    // Klassen-Token, die ein Wortschatz-Feld kennzeichnen (z. B. "blank wort")
    if (WS_TOKEN_RE.test(inp.className || "")) return false;
    return true;
  }

  // Container-Kandidaten: alle Tab-/Section-Boxen. Eine Box bekommt eine Wortbank,
  // wenn sie >=2 Lücken-Inputs enthält. Das deckt den Normalfall (eine Lückentext-
  // Section), Mehr-Tab-Lückentextdateien (Mattmüller) und Closure-Dateien ab — ohne
  // vom Tab-Label "Lückentext" abzuhängen.
  function candidateSections() {
    var nodes = document.querySelectorAll(".section, .tab, .tab-content");
    var out = [];
    Array.prototype.forEach.call(nodes, function (n) {
      // verschachtelte Container nicht doppelt zählen
      if (n.querySelector(".section, .tab, .tab-content")) return;
      if (gapInputs(n).length >= 2) out.push(n);
    });
    if (out.length) return out;
    // Fallback (Closure-Dateien ohne DOM-Antworten): Section per Label/Überschrift finden.
    var sections = document.querySelectorAll(".section, .tab, .tab-content");
    var navs = document.querySelectorAll(".nav-btn");
    for (var i = 0; i < navs.length; i++) {
      if (/Lückentext/i.test((navs[i].textContent || "").replace(/\s+/g, " ")) && sections[i]) return [sections[i]];
    }
    var heads = document.querySelectorAll(".section h1,.section h2,.section h3,.tab h1,.tab h2,.tab h3,.tab-content h2");
    for (var k = 0; k < heads.length; k++) {
      if (/Lückentext/i.test(heads[k].textContent || "")) {
        var sec = heads[k].closest(".section, .tab, .tab-content");
        if (sec) return [sec];
      }
    }
    return [];
  }

  function gapInputs(sec) {
    return Array.prototype.filter.call(sec.querySelectorAll("input"), isGapInput);
  }

  function collectAnswers(sec) {
    var out = [];
    gapInputs(sec).forEach(function (inp) {
      var a = answerOf(inp);
      if (a != null && a !== "") out.push(a);
    });
    if (out.length) return out;
    // Fallback: Lösung steckt in einer Closure, nicht im DOM -> globales Daten-Array lesen.
    return fromGlobals();
  }

  function wordsOf(arr) {
    if (!Array.isArray(arr) || !arr.length) return [];
    var words = [];
    arr.forEach(function (item) {
      if (!item || typeof item !== "object") return;
      // 'blank'/'loesung' decken die {before, blank, after}- und {pre, blank, post}-Formate ab.
      var direct = item.ans || item.answer || item.b || item.sol || item.solution || item.blank || item.loesung;
      if (direct != null && direct !== "") { words.push(direct); return; }
      var segs = item.segs || item.segments;
      if (Array.isArray(segs)) segs.forEach(function (s) { if (s && s.b) words.push(s.b); });
    });
    return words;
  }
  function fromGlobals() {
    var cands = [];
    // var-deklarierte Arrays hängen an window:
    ["LUECKE_DATA", "LUECKEN_DATA", "LT_DATA", "LUECKENDATA", "GAP_DATA", "BLANK_DATA", "LUECKEN", "LUECKE"].forEach(function (n) {
      try { if (Array.isArray(window[n]) && window[n].length) cands.push(window[n]); } catch (e) {}
    });
    // const/let-deklarierte Arrays sind NICHT auf window, aber als bloße Globals über
    // den geteilten lexikalischen Scope klassischer Scripts sichtbar:
    try { if (typeof LUECKEN_DATA !== "undefined") cands.push(LUECKEN_DATA); } catch (e) {}
    try { if (typeof LUECKEN !== "undefined") cands.push(LUECKEN); } catch (e) {}
    try { if (typeof LUECKE_DATA !== "undefined") cands.push(LUECKE_DATA); } catch (e) {}
    try { if (typeof LT_DATA !== "undefined") cands.push(LT_DATA); } catch (e) {}
    for (var i = 0; i < cands.length; i++) {
      var w = wordsOf(cands[i]);
      if (w.length) return w;
    }
    return [];
  }

  function shuffle(arr) {
    for (var i = arr.length - 1; i > 0; i--) {
      var j = Math.floor(Math.random() * (i + 1));
      var t = arr[i]; arr[i] = arr[j]; arr[j] = t;
    }
    return arr;
  }

  function ensureBank(sec) {
    var bank = sec.querySelector(".fb-wortbank");
    if (bank) return bank;
    var wrap = document.createElement("div");
    wrap.className = "fb-wortbank-wrap";
    var label = document.createElement("div");
    label.className = "fb-wortbank-label";
    label.innerHTML = "🔤 Wortbank – die richtigen Wörter, in zufälliger Reihenfolge.<br>" +
      "Tipp sie selbst in die Lücken — achte auf Groß- und Kleinschreibung.";
    bank = document.createElement("div");
    bank.className = "fb-wortbank";
    wrap.appendChild(label);
    wrap.appendChild(bank);
    // Einfügeort: nach control-bar falls vorhanden, sonst als erstes Inhaltselement
    var host = sec.querySelector(".sec-inner") || sec.querySelector(".luecken-block") || sec;
    var cb = host.querySelector(".control-bar");
    if (cb && cb.parentNode === host) {
      host.insertBefore(wrap, cb.nextSibling);
    } else {
      host.insertBefore(wrap, host.firstChild);
    }
    return bank;
  }

  function renderChips(bank, answers) {
    var sig = answers.slice().sort().join("");
    if (bank.getAttribute("data-sig") === sig) return; // unverändert -> nicht neu mischen
    bank.setAttribute("data-sig", sig);
    bank.innerHTML = "";
    shuffle(answers.slice()).forEach(function (w) {
      var chip = document.createElement("span");
      chip.className = "fb-wortbank-chip";
      chip.textContent = w;
      bank.appendChild(chip); // KEIN click-Handler — Wortbank ist nicht klickbar
    });
  }

  function updateUsed(sec, bank) {
    // "Gelöst" = Input dessen Wert exakt (case-sensitive) seiner eigenen Antwort entspricht.
    var solved = [];
    gapInputs(sec).forEach(function (inp) {
      if (!inp.value) return;
      var a = answerOf(inp);
      var byAttr = a != null && a !== "" && inp.value === a;
      // Closure-Dateien tragen die Lösung nicht im DOM, markieren das Feld aber
      // mit einer Erfolgs-Klasse (ok/correct/right/richtig).
      var byClass = /(^|\s)(ok|correct|right|richtig)(\s|$)/.test(inp.className);
      if (byAttr || byClass) solved.push(inp.value);
    });
    var remaining = solved.slice();
    Array.prototype.forEach.call(bank.querySelectorAll(".fb-wortbank-chip"), function (chip) {
      var idx = remaining.indexOf(chip.textContent);
      if (idx >= 0) { chip.classList.add("used"); remaining.splice(idx, 1); }
      else { chip.classList.remove("used"); }
    });
  }

  var wired = false;
  function refreshSection(sec) {
    var answers = collectAnswers(sec);
    if (!answers.length) return false;
    var bank = ensureBank(sec);
    renderChips(bank, answers);
    updateUsed(sec, bank);
    return true;
  }
  function build() {
    // Nichts tun, wenn die Seite schon eine Wort-Hilfe hat (skill-konforme Wortbank
    // ODER alter "Wortkasten"). Verhindert doppelte Wortlisten.
    if (document.querySelector(".wortbank, #wortbank-luecken, .wortkasten, .wort-kasten, .wordbank, #wortkasten")) return;
    var secs = candidateSections();
    if (!secs.length) return;
    var any = false;
    secs.forEach(function (sec) { if (refreshSection(sec)) any = true; });
    if (any && !wired) {
      wired = true;
      // Ein delegierter Listener fürs gesamte Dokument hält alle Wortbänke aktuell.
      document.addEventListener("input", function () {
        Array.prototype.forEach.call(document.querySelectorAll(".fb-wortbank"), function (b) {
          var sec = b.closest(".section, .tab, .tab-content") || b.parentNode.parentNode;
          if (sec) updateUsed(sec, b);
        });
      });
    }
  }

  function schedule() { setTimeout(build, 0); setTimeout(build, 150); }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", schedule);
  } else {
    schedule();
  }
  // Lazy-Render: viele Lektionen bauen den Lückentext erst beim Tab-Wechsel.
  document.addEventListener("click", function (e) {
    var t = e.target;
    if (t && t.closest && t.closest(".nav-btn")) setTimeout(build, 150);
  });
})();
