/* FB-WORTBANK-SHUFFLE — mischt eine vorhandene statische Wortbox bei jedem Laden
   und Tabwechsel. Anwendungsfall: Grammatik-/Deklinations-Lückentexte, deren Wortbank
   bewusst die GRUNDFORM zeigt (Infinitiv / Nominativ / Grundform des Adjektivs) — der
   Lerner konjugiert bzw. dekliniert selbst in der Lücke. Die Wörter bleiben exakt
   erhalten; nur ihre Reihenfolge wird zufällig. Kein .used-Feedback (die angezeigte
   Grundform ist absichtlich NICHT die Lücken-Lösung). Idempotent. */
(function () {
  "use strict";
  if (window.__fbWbShuffle) return;
  window.__fbWbShuffle = true;

  function shuffle(a) {
    for (var i = a.length - 1; i > 0; i--) {
      var j = Math.floor(Math.random() * (i + 1));
      var t = a[i]; a[i] = a[j]; a[j] = t;
    }
    return a;
  }

  function process(box) {
    if (!box.classList.contains("fb-wb-shuffled-init")) {
      var strong = box.querySelector("strong");
      var label = strong ? strong.textContent.trim() : "Wortbank:";
      var words = [];
      var spans = box.querySelectorAll("span");
      if (spans.length) {
        words = Array.prototype.map.call(spans, function (s) { return s.textContent.trim(); })
                     .filter(function (w) { return w; });
      } else {
        var txt = box.textContent || "";
        if (strong) txt = txt.replace(strong.textContent, "");
        words = txt.split(/[·•,]|\n/).map(function (w) { return w.trim(); })
                   .filter(function (w) { return w; });
      }
      box.setAttribute("data-fb-words", JSON.stringify(words));
      box.setAttribute("data-fb-label", label);
      box.classList.add("fb-wb-shuffled-init");
    }
    var words = JSON.parse(box.getAttribute("data-fb-words") || "[]");
    var label = box.getAttribute("data-fb-label") || "Wortbank:";
    if (!words.length) return;
    box.innerHTML = "";
    var lab = document.createElement("div");
    lab.className = "fb-wb-label";
    lab.textContent = label;
    box.appendChild(lab);
    var row = document.createElement("div");
    row.className = "fb-wb-chips";
    shuffle(words.slice()).forEach(function (w) {
      var chip = document.createElement("span");
      chip.className = "fb-wb-chip";
      chip.textContent = w;            // KEIN click-Handler — nicht klickbar
      row.appendChild(chip);
    });
    box.appendChild(row);
  }

  function run() {
    var boxes = document.querySelectorAll(".wortkasten:not(.fb-wortbank), .wortbank:not(.fb-wortbank)");
    Array.prototype.forEach.call(boxes, process);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", function () { setTimeout(run, 0); });
  } else {
    setTimeout(run, 0);
  }
  document.addEventListener("click", function (e) {
    if (e.target && e.target.closest && e.target.closest(".nav-btn")) setTimeout(run, 120);
  });
})();
