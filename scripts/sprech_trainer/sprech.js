// ======== SPRECH-TRAINER GENERISCH (mündlicher Abruf unter Zeitdruck) — FB-SPRECH-GENERIC ========
// Daten kommen aus SP_DATA (pro Lektion): { cue, luecke?, hint?, ok:[Wortanfänge], loesung, beispiel? }
// Erkannt wird ein Treffer, wenn ein gesprochenes Wort mit einem der ok-Wortanfänge beginnt
// (bei "stamm|partikel" muss zusätzlich die Partikel als eigenes Wort fallen).
// Konkurrenz = die ok-Wortanfänge aller anderen Karten (→ „✗ X statt Y“).
var spQueue = [], spPos = 0, spTimer = null, spRunde = {ok:0, total:0, fehler:[], mic:false, micOk:0, micTotal:0}, spMic = false, spRec = null, spGehoert = '', spOffen = false, spBewertet = false;
var SpRecCtor = window.SpeechRecognition || window.webkitSpeechRecognition || null;
function spEsc(s){ return String(s == null ? '' : s).replace(/[&<>"]/g, function(c){ return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]; }); }
function spMischen(a){ for (var i = a.length - 1; i > 0; i--){ var j = Math.floor(Math.random() * (i + 1)); var t = a[i]; a[i] = a[j]; a[j] = t; } return a; }
function spSek(){ return Number(document.getElementById('sp-zeit').value); }
function spModus(){ return document.getElementById('sp-modus').value; }
function spStart(mitMic){
  if (mitMic === true && !spMic) spMicToggle();
  if (mitMic === false && spMic) spMicToggle();
  spQueue = spMischen(SP_DATA.slice());
  spPos = 0; spRunde = {ok:0, total:0, fehler:[], mic:spMic, micOk:0, micTotal:0}; spZeige();
}
function spStopp(){ if (spTimer) clearInterval(spTimer); spTimer = null; spRecStop(); }
function spZeige(){
  spStopp(); spOffen = false;
  var box = document.getElementById('sp-karte');
  if (!spQueue.length || spPos >= spQueue.length){
    var nochmal = spRunde.fehler.length ? '<div class="sp-wdh"><strong>Noch nicht automatisch:</strong> ' + spRunde.fehler.map(function(x){ return spEsc(x.loesung); }).join(' · ') + '</div>' : '';
    var micBtn = SpRecCtor ? '<button class="sp-btn ok" onclick="spStart(true)">🎤 Mit Mikrofon starten</button>' : '';
    box.innerHTML = '<div class="sp-leer">' + (spRunde.total ? '🎉 Runde fertig – <strong>' + spRunde.ok + ' von ' + spRunde.total + '</strong> sofort parat' + (spRunde.mic ? ' · Mikrofon: ' + spRunde.micOk + ' von ' + spRunde.micTotal + ' richtig erkannt' : '') + '.' : 'Das Nomen erscheint – dann laut das passende Verb sagen, bevor der Balken abgelaufen ist.') +
      nochmal + '<div class="sp-leer-btns">' + micBtn + '<button class="sp-btn" onclick="spStart(false)">' + (spRunde.total ? 'Noch eine Runde ohne Mikrofon' : 'Ohne Mikrofon starten') + '</button></div>' +
      (SpRecCtor ? '' : '<div class="sp-hint">Dieser Browser hat keine Spracherkennung – mit Mikrofon geht es in Chrome oder Safari.</div>') + '</div>';
    spStandZeigen();
    return;
  }
  var e = spQueue[spPos], sek = spSek();
  var aufgabe = spModus() === 'satz' ? 'Laut einen ganzen Satz mit dem passenden Verb sprechen.' : 'Laut Nomen + passendes Verb sagen.';
  box.innerHTML = '<div class="sp-meta">Karte ' + (spPos + 1) + ' von ' + spQueue.length + '</div>' +
    '<div class="sp-cue">' + spEsc(e.cue) + ' <span class="sp-luecke">' + spEsc(e.luecke || '___') + '</span></div>' +
    (e.hint ? '<div class="sp-hint">(' + spEsc(e.hint) + ')</div>' : '') +
    '<div class="sp-aufgabe">🗣️ ' + aufgabe + '</div>' +
    '<div class="sp-bar"><div id="sp-fill"></div></div><div class="sp-count" id="sp-count">' + sek + ' s</div>' +
    '<div class="sp-gehoert" id="sp-gehoert"></div>' +
    '<div class="sp-loesung" id="sp-loesung"></div>' +
    '<div class="sp-aktion" id="sp-aktion"><button class="sp-btn" onclick="spAufloesen()">Lösung zeigen</button></div>';
  var ende = Date.now() + sek * 1000; // Uhrzeit statt Tick-Zählung: robust gegen gedrosselte Timer
  var fill = document.getElementById('sp-fill'), cnt = document.getElementById('sp-count');
  spTimer = setInterval(function(){ var rest = Math.max(0, ende - Date.now()); fill.style.width = (rest / (sek * 1000) * 100) + '%'; cnt.textContent = Math.ceil(rest / 1000) + ' s'; if (rest <= 0) spAufloesen(); }, 100);
  spGehoert = ''; spBewertet = false; spStandZeigen(); if (spMic) spRecStart(e);
}
function spAufloesen(){
  if (spOffen) return; spOffen = true;
  if (spTimer) clearInterval(spTimer); spTimer = null;
  setTimeout(spRecStop, 800); // kurz nachhören, falls das letzte Wort noch kommt
  var e = spQueue[spPos];
  var cnt = document.getElementById('sp-count'); if (cnt) cnt.textContent = 'Lösung';
  document.getElementById('sp-loesung').innerHTML = '<div class="sp-loesung-zeile"><strong>' + spEsc(e.loesung) + '</strong></div>' + (e.beispiel ? '<div class="sp-beispiel">' + spEsc(e.beispiel) + '</div>' : '');
  document.getElementById('sp-aktion').innerHTML = '<span class="sp-frage">Kam das Verb sofort?</span><span><button class="sp-btn ok" onclick="spBewerten(true)">✓ Ja, sofort</button> <button class="sp-btn" onclick="spBewerten(false)">✗ Nein, überlegt</button></span>';
  if (!spMic) spStatus('Vergleiche mit der Lösung: Hast du <strong>' + spEsc(e.loesung) + '</strong> gesagt? Dann „Ja, sofort“.', 'info');
  setTimeout(function(){ if (spOffen && spQueue[spPos] === e) spMicFazit(e); }, 900);
}
function spBewerten(ok){
  if (spBewertet) return; spBewertet = true;
  var e = spQueue[spPos];
  spRunde.total++; if (ok) spRunde.ok++; else spRunde.fehler.push(e);
  var akt = document.getElementById('sp-aktion');
  if (akt) akt.innerHTML = ok ? '<span class="sp-quittung gut">✓ Sofort gewusst – weiter so!</span>' : '<span class="sp-quittung schlecht">↺ Merk dir: <strong>' + spEsc(e.loesung) + '</strong> – kommt am Ende der Runde in die Wiederholungsliste.</span>';
  spStandZeigen();
  setTimeout(function(){ spPos++; spZeige(); }, ok ? 900 : 1800);
}
function spStandZeigen(){
  var el = document.getElementById('sp-stand'); if (!el) return;
  if (!spQueue.length){ el.innerHTML = ''; return; }
  var karte = Math.min(spPos + 1, spQueue.length);
  el.innerHTML = '<span>Karte <strong>' + karte + '</strong> von ' + spQueue.length + '</span><span class="sp-ok">✓ ' + spRunde.ok + ' sofort</span><span class="sp-no">✗ ' + (spRunde.total - spRunde.ok) + ' überlegt</span>' +
    (spMic ? '<span>🎤 ' + spRunde.micOk + ' von ' + spRunde.micTotal + ' erkannt</span>' : '<span class="sp-ohne">ohne Mikrofon – du bewertest dich selbst</span>');
}
function spMicToggle(){
  spMic = !spMic;
  var b = document.getElementById('sp-mic'); b.textContent = spMic ? '🎤 Mikrofon ist an' : '🎤 Mikrofon ist aus'; b.classList.toggle('ok', spMic);
  if (!spMic){ spRecStop(); spStatus(''); return; }
  if (spTimer && spQueue[spPos]) spRecStart(spQueue[spPos]);
  else spStatus('🎤 Mikrofon ist an – es hört ab der nächsten Karte zu.', 'info');
}
function spStatus(html, typ){
  var el = document.getElementById('sp-gehoert'); if (!el) return;
  el.className = 'sp-gehoert' + (typ ? ' sp-' + typ : '');
  el.innerHTML = html;
}
var SP_FEHLER = {
  'not-allowed': '🚫 Mikrofon blockiert. Bitte oben in der Adressleiste das Mikrofon für diese Seite erlauben und neu laden.',
  'service-not-allowed': '🚫 Spracherkennung ist in diesem Browser gesperrt. Bitte Chrome oder Safari verwenden.',
  'audio-capture': '🎤 Kein Mikrofon gefunden. Bitte ein Mikrofon anschließen oder in den Systemeinstellungen freigeben.',
  'network': '📶 Die Spracherkennung braucht eine Internetverbindung (Chrome schickt die Aufnahme an Google).',
  'language-not-supported': 'Deutsch wird von der Spracherkennung dieses Browsers nicht unterstützt.'
};
function spRecStart(e){
  if (!SpRecCtor){ spStatus('Dieser Browser hat keine Spracherkennung. Bitte Chrome oder Safari verwenden.', 'warn'); return; }
  spRecStop();
  var karte = spPos;
  try {
    var rec = new SpRecCtor(); spRec = rec;
    rec.lang = 'de-DE'; rec.interimResults = true; rec.continuous = true; rec.maxAlternatives = 3;
    rec.onstart = function(){ if (spRec === rec && !spGehoert) spStatus('<span class="sp-puls">●</span> Ich höre zu … jetzt sprechen.', 'info'); };
    rec.onresult = function(ev){
      var t = ''; for (var i = 0; i < ev.results.length; i++) t += ev.results[i][0].transcript + ' ';
      spGehoert = t.trim(); spGehoertZeigen(e);
      // richtiges Verb sicher erkannt → Karte sofort auflösen (Belohnung ohne Warten)
      var last = ev.results[ev.results.length - 1];
      if (last && last.isFinal && !spOffen && spPos === karte && spUrteil(e).hat) spAufloesen();
    };
    rec.onerror = function(ev){
      var msg = SP_FEHLER[ev.error];
      if (msg){ spStatus(msg, 'warn'); if (ev.error === 'not-allowed' || ev.error === 'service-not-allowed' || ev.error === 'audio-capture'){ spMic = false; var b = document.getElementById('sp-mic'); if (b){ b.textContent = '🎤 Mikrofon ist aus'; b.classList.remove('ok'); } } }
      else if (ev.error === 'no-speech' && !spGehoert && !spOffen) spStatus('🤫 Noch nichts gehört – bitte lauter oder näher am Mikrofon sprechen.', 'warn');
    };
    // Chrome beendet die Erkennung nach Sprechpausen von selbst → solange die Karte läuft, neu starten
    rec.onend = function(){ if (spRec === rec && spMic && !spOffen && spPos === karte && spTimer){ try { rec.start(); } catch (x){} } };
    rec.start();
  } catch (x){ spRec = null; spStatus('Die Spracherkennung konnte nicht gestartet werden.', 'warn'); }
}
function spRecStop(){ if (spRec){ var r = spRec; spRec = null; try { r.onend = null; r.onresult = null; r.stop(); } catch (x){} } }
function spWoerter(){ return spGehoert.toLowerCase().replace(/[.,!?;:„“"–-]/g, ' ').split(/\s+/).filter(Boolean); }
// ok-Eintrag: "stamm" = ein Wort beginnt so · "stamm|partikel" = trennbares Verb (legt … ab → "leg|ab");
// bei "stamm|partikel" zählt auch der zu-Infinitiv als ein Wort (abzulegen → "ab"+"zu"+"leg").
function spTreffer(w, eintrag){
  var t = eintrag.toLowerCase().split('|'), st = t[0], pt = t[1];
  var hit = null;
  w.forEach(function(x){ if (!hit && x.indexOf(st) === 0) hit = x; });
  if (hit && (!pt || w.indexOf(pt) !== -1)) return hit;
  if (pt){ var zu = pt + 'zu' + st; for (var i = 0; i < w.length; i++) if (w[i].indexOf(zu) === 0) return w[i]; }
  return null;
}
function spUrteil(e){
  // Wörter, die schon auf der Karte stehen (der Lerner spricht sie mit), zählen nie als Verb
  var cue = (e.cue + ' ' + (e.luecke || '')).toLowerCase().replace(/[.,!?;:„“"–-]/g, ' ').split(/\s+/).filter(Boolean);
  var w = spWoerter().filter(function(x){ return cue.indexOf(x) === -1; });
  var hat = e.ok.some(function(o){ return spTreffer(w, o); });
  var eigen = e.ok.map(function(s){ return s.toLowerCase(); });
  var falsch = [];
  if (!hat) SP_DATA.forEach(function(x){ if (x === e) return; x.ok.forEach(function(o){ if (eigen.indexOf(o.toLowerCase()) !== -1) return; var t = spTreffer(w, o); if (t && falsch.indexOf(t) === -1) falsch.push(t); }); });
  return {hat: hat, falsch: falsch};
}
function spGehoertZeigen(e){
  if (!spGehoert) return;
  var u = spUrteil(e);
  var urteil = u.hat ? '<span class="sp-ok">✓ richtiges Verb erkannt</span>' : u.falsch.length ? '<span class="sp-no">✗ „' + spEsc(u.falsch[0]) + '“ passt hier nicht</span>' : '';
  spStatus('🎤 Gehört: „' + spEsc(spGehoert) + '“ ' + urteil, u.hat ? 'gut' : (u.falsch.length ? 'schlecht' : 'info'));
}
function spMicFazit(e){
  if (!spMic) return;
  var u = spUrteil(e), html, typ, empf = null;
  if (!spGehoert){ html = '🎤 Das Mikrofon hat nichts verstanden. Bewerte dich bitte selbst.'; typ = 'warn'; }
  else if (u.hat){ html = '🎤 Gehört: „' + spEsc(spGehoert) + '“ <span class="sp-ok">✓ Richtig – das passende Verb war dabei!</span>'; typ = 'gut'; empf = true; }
  else if (u.falsch.length){ html = '🎤 Gehört: „' + spEsc(spGehoert) + '“ <span class="sp-no">✗ Du hast „' + spEsc(u.falsch[0]) + '“ gesagt – richtig ist: ' + spEsc(e.loesung) + '.</span>'; typ = 'schlecht'; empf = false; }
  else { html = '🎤 Gehört: „' + spEsc(spGehoert) + '“ <span class="sp-no">– das passende Verb war nicht dabei.</span>'; typ = 'schlecht'; empf = false; }
  spStatus(html, typ);
  if (empf !== null){ spRunde.micTotal++; if (empf) spRunde.micOk++; spStandZeigen(); }
  if (empf !== null){ var btns = document.querySelectorAll('#sp-aktion .sp-btn'); if (btns.length === 2) btns[empf ? 0 : 1].classList.add('sp-empf'); }
}
function initSprechTrainer(){
  ['sp-modus','sp-zeit'].forEach(function(id){ document.getElementById(id).addEventListener('change', function(){ spQueue = []; spZeige(); }); });
  if (SpRecCtor) document.getElementById('sp-mic').hidden = false;
  var sec = document.getElementById('sec-sprechen');
  document.addEventListener('keydown', function(ev){
    if (ev.code !== 'Space' || !sec.classList.contains('active')) return;
    if (/^(INPUT|TEXTAREA|SELECT|BUTTON)$/.test(ev.target.tagName)) return;
    ev.preventDefault();
    if (!spQueue.length || spPos >= spQueue.length) spStart(spMic); else if (!spOffen) spAufloesen(); else spBewerten(true);
  });
  // Mikrofon aus, sobald der Tab verlassen wird
  document.querySelectorAll('.nav-btn').forEach(function(b){ b.addEventListener('click', function(){ if (!sec.classList.contains('active')) spStopp(); }); });
  spZeige();
}
if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', initSprechTrainer); else initSprechTrainer();
