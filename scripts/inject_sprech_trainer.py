#!/usr/bin/env python3
"""Fügt den Tab „Sprech-Trainer" (mündlicher Abruf unter Zeitdruck) in die Verben-mit-Präposition-Serie ein.
Position: nach Trainer (4), vor Merk-Werkstatt; Schreibwerkstatt bleibt letzter Tab. Idempotent (Marker FB-SPRECH-TRAINER)."""
import sys, re

CSS = """
/* ===== SPRECH-TRAINER (FB-SPRECH-TRAINER) ===== */
.sp-cue { display: flex; flex-wrap: wrap; align-items: baseline; gap: 6px 14px; font-family: Georgia, 'Times New Roman', serif; font-size: 1.7em; color: var(--text); line-height: 1.5; margin: 6px 0 2px; }
.sp-plus { color: var(--faint); font-size: .7em; }
.sp-nomen { color: var(--accent-2); }
.sp-aufgabe { font-size: .92em; color: var(--muted); margin: 8px 0 14px; }
.sp-bar { height: 10px; background: var(--line); border-radius: 6px; overflow: hidden; }
.sp-bar div { height: 100%; width: 100%; background: linear-gradient(90deg, var(--accent), var(--accent-2)); transition: width .1s linear; }
.sp-count { font-size: .8em; color: var(--muted-2); margin-top: 4px; font-variant-numeric: tabular-nums; }
.sp-gehoert { font-size: .9em; color: var(--muted); margin-top: 10px; }
.sp-gehoert:empty { display: none; }
.sp-ok { color: var(--ok-tx); font-weight: 700; }
.sp-no { color: var(--err-tx); font-weight: 700; }
.sp-loesung-zeile { font-family: Georgia, 'Times New Roman', serif; font-size: 1.35em; color: var(--text); margin-top: 12px; line-height: 1.6; }
.sp-tipp { font-size: .82em; color: var(--muted-2); margin-top: 6px; }
"""

HTML = """<!-- ===== TAB 6 — SPRECH-TRAINER (FB-SPRECH-TRAINER) ===== -->
<div class="section" id="sec-5"><div class="sec-inner">
  <h2>🗣️ Sprech-Trainer</h2>
  <div class="sec-desc">Wer die Präposition beim Schreiben weiß, hat sie beim Sprechen noch lange nicht parat – dort fehlt die Zeit zum Nachdenken. Hier zählt deshalb Tempo: Verb und Merk-Wort erscheinen, der Satz wird <strong>laut</strong> gesprochen, bevor der Balken abgelaufen ist. Erst danach kommt die Lösung zum Vergleichen.</div>
  <div class="tr-steuerung">
    <label>Teil <select class="verb-select" id="sp-teil"></select></label>
    <label>Aufgabe <select class="verb-select" id="sp-modus">
      <option value="satz">Satz sprechen</option>
      <option value="frage">Frage und Antwort</option>
    </select></label>
    <label>Zeit <select class="verb-select" id="sp-zeit">
      <option value="8">8 Sekunden</option>
      <option value="5" selected>5 Sekunden</option>
      <option value="3">3 Sekunden</option>
    </select></label>
    <button class="mc-opt" id="sp-mic" onclick="spMicToggle()" hidden>🎤 Mikrofon aus</button>
  </div>
  <div class="tr-karte" id="sp-karte"></div>
  <div class="sp-tipp">Tipp: Leertaste zeigt die Lösung bzw. geht weiter. Mit Mikrofon hört die Seite mit und prüft, ob die richtige Präposition gefallen ist (Chrome, Safari).</div>
</div></div>

"""

JS = r"""
// ======== SPRECH-TRAINER (mündlicher Abruf unter Zeitdruck) — FB-SPRECH-TRAINER ========
let spQueue = [], spPos = 0, spTimer = null, spRunde = {ok:0, total:0}, spMic = false, spRec = null, spGehoert = '', spOffen = false;
const SP_PRAEPS = ['an','auf','aus','bei','für','gegen','in','mit','nach','über','um','unter','von','vor','zu','durch'];
const SpRecCtor = window.SpeechRecognition || window.webkitSpeechRecognition || null;
function spWoForm(p){ return 'wo' + (/^[aeiouäöü]/.test(p) ? 'r' : '') + p; }
function spMischen(a){ for (let i = a.length - 1; i > 0; i--){ const j = Math.floor(Math.random() * (i + 1)); [a[i], a[j]] = [a[j], a[i]]; } return a; }
function spNomen(e){ return `${e.pl ? 'die' : e.m[0]} ${e.m[1]}${e.m[2]}`; }
function spStart(){
  const t = document.getElementById('sp-teil').value;
  spQueue = spMischen(VAP.filter(e => t === 'alle' ? e.t > 0 : e.t === Number(t)));
  spPos = 0; spRunde = {ok:0, total:0}; spZeige();
}
function spStopp(){ if (spTimer) clearInterval(spTimer); spTimer = null; spRecStop(); }
function spZeige(){
  spStopp(); spOffen = false;
  const box = document.getElementById('sp-karte');
  if (!spQueue.length || spPos >= spQueue.length){
    box.innerHTML = `<div class="tr-leer">${spRunde.total ? `🎉 Runde fertig – ${spRunde.ok} von ${spRunde.total} Sätzen sofort parat.` : 'Verb und Merk-Wort erscheinen – dann laut sprechen, bevor der Balken abgelaufen ist.'}
      <div class="tr-leer-btns"><button class="mc-opt" onclick="spStart()">${spRunde.total ? 'Noch eine Runde' : 'Los geht’s'}</button></div></div>`;
    return;
  }
  const e = spQueue[spPos], modus = document.getElementById('sp-modus').value, sek = Number(document.getElementById('sp-zeit').value);
  const aufgabe = modus === 'satz' ? 'Laut einen Satz mit diesem Verb und diesem Nomen sprechen.' : 'Laut fragen: „Wo…?“ – und mit dem Nomen antworten.';
  box.innerHTML = `<div class="tr-meta">Karte ${spPos + 1} von ${spQueue.length} · ${esc(VAP_GRUPPEN[e.g] || '')}</div>
    <div class="sp-cue"><span class="sp-verb">${esc(vapVerbLabel(e))}</span><span class="sp-plus">+</span><span class="sp-nomen">${esc(spNomen(e))}</span></div>
    ${e.h ? `<div class="quiz-hint">(${esc(vapHint(e))})</div>` : ''}
    <div class="sp-aufgabe">🗣️ ${aufgabe}</div>
    <div class="sp-bar"><div id="sp-fill"></div></div><div class="sp-count" id="sp-count">${sek} s</div>
    <div class="sp-gehoert" id="sp-gehoert"></div>
    <div class="tr-loesung" id="sp-loesung"></div>
    <div class="tr-aktion" id="sp-aktion"><button class="mc-opt" onclick="spAufloesen()">Lösung zeigen</button></div>`;
  const ende = Date.now() + sek * 1000; // Uhrzeit statt Tick-Zählung: robust gegen gedrosselte Timer
  const fill = document.getElementById('sp-fill'), cnt = document.getElementById('sp-count');
  spTimer = setInterval(() => { const rest = Math.max(0, ende - Date.now()); fill.style.width = (rest / (sek * 1000) * 100) + '%'; cnt.textContent = Math.ceil(rest / 1000) + ' s'; if (rest <= 0) spAufloesen(); }, 100);
  spGehoert = ''; if (spMic) spRecStart(e);
}
function spAufloesen(){
  if (spOffen) return; spOffen = true;
  if (spTimer) clearInterval(spTimer); spTimer = null;
  setTimeout(spRecStop, 800); // kurz nachhören, falls das letzte Wort noch kommt
  const e = spQueue[spPos], modus = document.getElementById('sp-modus').value;
  const cnt = document.getElementById('sp-count'); if (cnt) cnt.textContent = 'Lösung';
  const kasus = `+ ${KASUS_TXT[e.k]}${e.p2 ? ` · ${esc(e.p2)} + ${KASUS_TXT[e.k2]} (Person)` : ''}`;
  const z = modus === 'satz'
    ? `<div class="sp-loesung-zeile">${esc(vapVerbLabel(e))} <strong>${vapPhrase(e)}</strong></div><div>${kasus}</div>`
    : `<div class="sp-loesung-zeile"><strong>${esc(spWoForm(e.p).replace(/^w/, 'W'))}</strong> …? – <strong>${vapPhrase(e)}</strong> · <em>${esc(schreibDaForm(e.p))}</em></div><div>${kasus}</div>`;
  document.getElementById('sp-loesung').innerHTML = z;
  document.getElementById('sp-aktion').innerHTML = `<span class="quiz-hint">Kam die Präposition sofort?</span><span><button class="mc-opt ok" onclick="spBewerten(true)">✓ Ja, sofort</button> <button class="mc-opt" onclick="spBewerten(false)">✗ Nein, überlegt</button></span>`;
}
function spBewerten(ok){ spRunde.total++; if (ok) spRunde.ok++; spPos++; spZeige(); }
function spMicToggle(){
  spMic = !spMic;
  const b = document.getElementById('sp-mic'); b.textContent = spMic ? '🎤 Mikrofon an' : '🎤 Mikrofon aus'; b.classList.toggle('ok', spMic);
  if (spMic && spTimer && spQueue[spPos]) spRecStart(spQueue[spPos]); else spRecStop();
}
function spRecStart(e){
  if (!SpRecCtor) return; spRecStop();
  try {
    spRec = new SpRecCtor(); spRec.lang = 'de-DE'; spRec.interimResults = true; spRec.continuous = true;
    spRec.onresult = ev => { let t = ''; for (const r of ev.results) t += r[0].transcript + ' '; spGehoert = t.trim(); spGehoertZeigen(e); };
    spRec.onerror = () => {}; spRec.start();
  } catch (x){ spRec = null; }
}
function spRecStop(){ if (spRec){ try { spRec.onresult = null; spRec.stop(); } catch (x){} spRec = null; } }
function spGehoertZeigen(e){
  const el = document.getElementById('sp-gehoert'); if (!el) return;
  const low = ' ' + spGehoert.toLowerCase().replace(/[.,!?;:]/g, ' ').replace(/\s+/g, ' ') + ' ';
  const kontr = Object.keys(VAP_KONTR).filter(k => k.indexOf(e.p + ' ') === 0).map(k => VAP_KONTR[k]);
  const hat = low.indexOf(' ' + e.p + ' ') !== -1 || kontr.some(k => low.indexOf(' ' + k + ' ') !== -1);
  const falsch = SP_PRAEPS.filter(p => p !== e.p && p !== e.p2 && low.indexOf(' ' + p + ' ') !== -1);
  el.innerHTML = `Gehört: „${esc(spGehoert)}“ ` + (hat ? `<span class="sp-ok">✓ ${esc(e.p)}</span>` : falsch.length ? `<span class="sp-no">✗ „${esc(falsch[0])}“ statt „${esc(e.p)}“</span>` : '');
}
function initSprechTrainer(){
  const sel = document.getElementById('sp-teil');
  sel.innerHTML = [1,2,3,4,5].map(t => `<option value="${t}">Teil ${t} (${VAP.filter(e => e.t === t).length} Verben)</option>`).join('') + `<option value="alle">Alle ${VAP.filter(e => e.t > 0).length} Verben</option>`;
  if (window.VAP_TEIL) sel.value = String(window.VAP_TEIL);
  ['sp-teil','sp-modus','sp-zeit'].forEach(id => document.getElementById(id).addEventListener('change', () => { spQueue = []; spZeige(); }));
  if (SpRecCtor) document.getElementById('sp-mic').hidden = false;
  document.addEventListener('keydown', ev => {
    if (ev.code !== 'Space' || !document.getElementById('sec-5').classList.contains('active')) return;
    if (/^(INPUT|TEXTAREA|SELECT|BUTTON)$/.test(ev.target.tagName)) return;
    ev.preventDefault();
    if (!spQueue.length || spPos >= spQueue.length) spStart(); else if (!spOffen) spAufloesen(); else spBewerten(true);
  });
  // Mikrofon aus, sobald der Tab verlassen wird
  document.querySelectorAll('.nav-btn').forEach(b => b.addEventListener('click', () => { if (!document.getElementById('sec-5').classList.contains('active')) spStopp(); }));
  spZeige();
}
"""

for f in sys.argv[1:]:
    s = open(f, encoding='utf-8').read()
    if 'FB-SPRECH-TRAINER' in s:
        print('skip (schon drin)', f); continue
    o = s
    # Nav: Merk-Werkstatt 5→6, Schreibwerkstatt 6→7, neuer Button an Position 5
    nav_old = '  <div class="nav-btn" onclick="showSection(5)"><span class="nav-emoji">💡</span>'
    assert nav_old in s, f
    s = s.replace('onclick="showSection(6)"><span class="nav-emoji">📨</span>', 'onclick="showSection(7)"><span class="nav-emoji">📨</span>', 1)
    s = s.replace(nav_old, '  <div class="nav-btn" onclick="showSection(5)"><span class="nav-emoji">🗣️</span><span class="nav-label">Sprechen</span></div>\n  <div class="nav-btn" onclick="showSection(6)"><span class="nav-emoji">💡</span>', 1)
    # Sections: ids umbenennen (Zwei-Phasen), neue Section vor Merk-Werkstatt
    assert s.count('id="sec-6"') == 1 and s.count('id="sec-5"') == 1, f
    s = s.replace('id="sec-6"', 'id="sec-__7"', 1).replace('id="sec-5"', 'id="sec-6"', 1).replace('id="sec-__7"', 'id="sec-7"', 1)
    marker = '<!-- ===== TAB 6 — MERK-WERKSTATT ===== -->'
    assert marker in s, f
    s = s.replace(marker, HTML + '<!-- ===== TAB 7 — MERK-WERKSTATT ===== -->', 1)
    # CSS vor dem Merk-Werkstatt-CSS-Block
    css_anchor = '/* ===== EIGENES MERK-WORT IN DER KARTE ===== */'
    assert css_anchor in s, f
    s = s.replace(css_anchor, CSS.strip('\n') + '\n' + css_anchor, 1)
    # JS vor der Merk-Werkstatt-Logik, Init nach initTrainer()
    js_anchor = '// ======== MERK-WERKSTATT (eigene Merk-Wörter) ========'
    assert js_anchor in s, f
    s = s.replace(js_anchor, JS.strip('\n') + '\n\n' + js_anchor, 1)
    assert s.count('\ninitTrainer();\n') == 1, f
    s = s.replace('\ninitTrainer();\n', '\ninitTrainer();\ninitSprechTrainer();\n', 1)
    assert s != o
    open(f, 'w', encoding='utf-8').write(s); print('patched', f)
