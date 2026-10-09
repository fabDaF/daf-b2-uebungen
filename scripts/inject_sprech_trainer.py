#!/usr/bin/env python3
"""Sprech-Trainer (mündlicher Abruf unter Zeitdruck) in die Verben-mit-Präposition-Serie einbauen
ODER bestehende Sprech-Trainer auf den kanonischen Stand bringen.

Quelle der Wahrheit: daf-materialien/Grundlagen/Grammatik/verben-praep-teil1.html
(alles zwischen den Markern FB-SPRECH-TRAINER). Die Blöcke unten sind 1:1 daraus kopiert
(Stand 2026-10-09, Commit fbb6920). Skill: daf-uebungsformen → „Sprech-Trainer".

Aufruf:
  python3 inject_sprech_trainer.py DATEI.html [...]        # einbauen bzw. aktualisieren (idempotent)
  python3 inject_sprech_trainer.py --dry-run DATEI.html     # nur anzeigen, was passieren würde
  python3 inject_sprech_trainer.py --check REFERENZ.html    # Drift-Wächter: Exit 1, wenn die
                                                            # eingebetteten Blöcke von der Referenz abweichen

Modi pro Datei:
  - Marker fehlt  → EINBAUEN: Tab nach Trainer (4), vor Merk-Werkstatt; Schreibwerkstatt bleibt letzter Tab.
  - Marker da     → AKTUALISIEREN: CSS-, HTML- und JS-Block werden durch den kanonischen Stand ersetzt.
  - In beiden Fällen: fehlt vapHint() (Merk-Hinweis ohne Lösung), wird es ergänzt und alle
    Hinweis-Ausgaben (Quiz, Trainer, Sprech-Trainer) werden darauf umgestellt.
"""
import sys, re

CSS_START = '/* ===== SPRECH-TRAINER (FB-SPRECH-TRAINER) ===== */'
HTML_START = '<!-- ===== TAB 6 — SPRECH-TRAINER (FB-SPRECH-TRAINER) ===== -->'
JS_START = '// ======== SPRECH-TRAINER (mündlicher Abruf unter Zeitdruck) — FB-SPRECH-TRAINER ========'
CSS = r"""/* ===== SPRECH-TRAINER (FB-SPRECH-TRAINER) ===== */
.sp-cue { display: flex; flex-wrap: wrap; align-items: baseline; gap: 6px 14px; font-family: Georgia, 'Times New Roman', serif; font-size: 1.7em; color: var(--text); line-height: 1.5; margin: 6px 0 2px; }
.sp-plus { color: var(--faint); font-size: .7em; }
.sp-nomen { color: var(--accent-2); }
.sp-aufgabe { font-size: .92em; color: var(--muted); margin: 8px 0 14px; }
.sp-bar { height: 10px; background: var(--line); border-radius: 6px; overflow: hidden; }
.sp-bar div { height: 100%; width: 100%; background: linear-gradient(90deg, var(--accent), var(--accent-2)); transition: width .1s linear; }
.sp-count { font-size: .8em; color: var(--muted-2); margin-top: 4px; font-variant-numeric: tabular-nums; }
.sp-gehoert { font-size: .9em; color: var(--muted); margin-top: 10px; }
.sp-gehoert:empty { display: none; }
.sp-gehoert { padding: 8px 12px; border-radius: 8px; line-height: 1.5; }
.sp-gehoert.sp-info { background: var(--info-bg); color: var(--info-tx); }
.sp-gehoert.sp-gut { background: var(--ok-bg); color: var(--ok-tx); }
.sp-gehoert.sp-schlecht { background: var(--err-bg); color: var(--err-tx); }
.sp-gehoert.sp-warn { background: var(--warn-bg); color: var(--warn-tx); border: 1px solid var(--warn-bd); }
.sp-puls { color: #e53935; animation: sp-puls 1s infinite; }
@keyframes sp-puls { 0%,100% { opacity: 1; } 50% { opacity: .25; } }
.mc-opt.sp-empf { box-shadow: 0 0 0 3px rgba(102,126,234,.45); transform: scale(1.06); }
.sp-ok { color: var(--ok-tx); font-weight: 700; }
.sp-no { color: var(--err-tx); font-weight: 700; }
.sp-loesung-zeile { font-family: Georgia, 'Times New Roman', serif; font-size: 1.35em; color: var(--text); margin-top: 12px; line-height: 1.6; }
.sp-stand { display: flex; flex-wrap: wrap; gap: 14px; font-size: .88em; color: var(--muted); margin-bottom: 10px; min-height: 1.2em; }
.sp-stand .sp-ohne { color: var(--muted-2); font-style: italic; }
.sp-quittung { font-weight: 600; padding: 8px 12px; border-radius: 8px; }
.sp-quittung.gut { background: var(--ok-bg); color: var(--ok-tx); }
.sp-quittung.schlecht { background: var(--warn-bg); color: var(--warn-tx); }
.sp-wdh { margin-top: 12px; font-size: .92em; color: var(--warn-tx); }
.sp-tipp { font-size: .82em; color: var(--muted-2); margin-top: 6px; }
"""

HTML = r"""<!-- ===== TAB 6 — SPRECH-TRAINER (FB-SPRECH-TRAINER) ===== -->
<div class="section" id="sec-5"><div class="sec-inner">
  <h2>🗣️ Sprech-Trainer</h2>
  <div class="sec-desc">Wer die Präposition beim Schreiben weiß, hat sie beim Sprechen noch lange nicht parat – dort fehlt die Zeit zum Nachdenken. Hier zählt deshalb Tempo: Nur das Verb erscheint, der Satz mit der passenden Präposition wird <strong>laut</strong> gesprochen, bevor der Balken abgelaufen ist. Erst danach kommt die Lösung – mit dem Merk-Wort als Eselsbrücke.</div>
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
    <button class="mc-opt" id="sp-mic" onclick="spMicToggle()" title="Klicken zum Ein- oder Ausschalten" hidden>🎤 Mikrofon ist aus</button>
  </div>
  <div class="sp-stand" id="sp-stand"></div>
  <div class="tr-karte" id="sp-karte"></div>
  <div class="sp-tipp">Tipp: Leertaste zeigt die Lösung bzw. geht weiter. Mit Mikrofon hört die Seite mit und prüft, ob die richtige Präposition gefallen ist (Chrome, Safari).</div>
</div></div>

"""

JS = r"""// ======== SPRECH-TRAINER (mündlicher Abruf unter Zeitdruck) — FB-SPRECH-TRAINER ========
let spQueue = [], spPos = 0, spTimer = null, spRunde = {ok:0, total:0, fehler:[], mic:false, micOk:0, micTotal:0}, spMic = false, spRec = null, spGehoert = '', spOffen = false;
const SP_PRAEPS = ['an','auf','aus','bei','für','gegen','in','mit','nach','über','um','unter','von','vor','zu','durch'];
const SpRecCtor = window.SpeechRecognition || window.webkitSpeechRecognition || null;
function spWoForm(p){ return 'wo' + (/^[aeiouäöü]/.test(p) ? 'r' : '') + p; }
function spMischen(a){ for (let i = a.length - 1; i > 0; i--){ const j = Math.floor(Math.random() * (i + 1)); [a[i], a[j]] = [a[j], a[i]]; } return a; }
function spNomen(e){ return `${e.pl ? 'die' : e.m[0]} ${e.m[1]}${e.m[2]}`; }
function spStart(mitMic){
  if (mitMic === true && !spMic) spMicToggle();
  if (mitMic === false && spMic) spMicToggle();
  const t = document.getElementById('sp-teil').value;
  spQueue = spMischen(VAP.filter(e => t === 'alle' ? e.t > 0 : e.t === Number(t)));
  spPos = 0; spRunde = {ok:0, total:0, fehler:[], mic:spMic, micOk:0, micTotal:0}; spZeige();
}
function spStopp(){ if (spTimer) clearInterval(spTimer); spTimer = null; spRecStop(); }
function spZeige(){
  spStopp(); spOffen = false;
  const box = document.getElementById('sp-karte');
  if (!spQueue.length || spPos >= spQueue.length){
    const nochmal = spRunde.fehler.length ? `<div class="sp-wdh"><strong>Noch nicht automatisch:</strong> ${spRunde.fehler.map(x => esc(vapVerbLabel(x)) + ' ' + esc(x.p)).join(' · ')}</div>` : '';
    const micBtn = SpRecCtor ? `<button class="mc-opt ok" onclick="spStart(true)">🎤 Mit Mikrofon starten</button>` : '';
    box.innerHTML = `<div class="tr-leer">${spRunde.total ? `🎉 Runde fertig – <strong>${spRunde.ok} von ${spRunde.total}</strong> Sätzen sofort parat${spRunde.mic ? ` · Mikrofon: ${spRunde.micOk} von ${spRunde.micTotal} richtig erkannt` : ''}.` : 'Das Verb erscheint – dann laut einen Satz mit der Präposition sprechen, bevor der Balken abgelaufen ist.'}
      ${nochmal}
      <div class="tr-leer-btns">${micBtn}<button class="mc-opt" onclick="spStart(false)">${spRunde.total ? 'Noch eine Runde ohne Mikrofon' : 'Ohne Mikrofon starten'}</button></div>
      ${SpRecCtor ? '' : '<div class="quiz-hint">Dieser Browser hat keine Spracherkennung – mit Mikrofon geht es in Chrome oder Safari.</div>'}</div>`;
    spStandZeigen();
    return;
  }
  const e = spQueue[spPos], modus = document.getElementById('sp-modus').value, sek = Number(document.getElementById('sp-zeit').value);
  const aufgabe = modus === 'satz' ? 'Laut einen Satz mit diesem Verb sprechen – mit der richtigen Präposition.' : 'Laut fragen: „Wo…?“ – und mit der Präposition antworten.';
  box.innerHTML = `<div class="tr-meta">Karte ${spPos + 1} von ${spQueue.length} · ${esc(VAP_GRUPPEN[e.g] || '')}</div>
    <div class="sp-cue"><span class="sp-verb">${esc(vapVerbLabel(e))}</span></div>
    ${e.h ? `<div class="quiz-hint">(${esc(vapHint(e))})</div>` : ''}
    <div class="sp-aufgabe">🗣️ ${aufgabe}</div>
    <div class="sp-bar"><div id="sp-fill"></div></div><div class="sp-count" id="sp-count">${sek} s</div>
    <div class="sp-gehoert" id="sp-gehoert"></div>
    <div class="tr-loesung" id="sp-loesung"></div>
    <div class="tr-aktion" id="sp-aktion"><button class="mc-opt" onclick="spAufloesen()">Lösung zeigen</button></div>`;
  const ende = Date.now() + sek * 1000; // Uhrzeit statt Tick-Zählung: robust gegen gedrosselte Timer
  const fill = document.getElementById('sp-fill'), cnt = document.getElementById('sp-count');
  spTimer = setInterval(() => { const rest = Math.max(0, ende - Date.now()); fill.style.width = (rest / (sek * 1000) * 100) + '%'; cnt.textContent = Math.ceil(rest / 1000) + ' s'; if (rest <= 0) spAufloesen(); }, 100);
  spGehoert = ''; spBewertet = false; spStandZeigen(); if (spMic) spRecStart(e);
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
  if (!spMic) spStatus('Vergleiche mit der Lösung: Hast du <strong>' + esc(e.p) + '</strong> + ' + KASUS_TXT[e.k] + ' gesagt? Dann „Ja, sofort“.', 'info');
  setTimeout(() => { if (spOffen && spQueue[spPos] === e) spMicFazit(e); }, 900);
}
function spBewerten(ok){
  if (spBewertet) return; spBewertet = true;
  const e = spQueue[spPos];
  spRunde.total++; if (ok) spRunde.ok++; else spRunde.fehler.push(e);
  const akt = document.getElementById('sp-aktion');
  if (akt) akt.innerHTML = ok ? '<span class="sp-quittung gut">✓ Sofort gewusst – weiter so!</span>' : `<span class="sp-quittung schlecht">↺ Merk dir: <strong>${esc(vapVerbLabel(e))} ${esc(e.p)}</strong> + ${KASUS_TXT[e.k]} – kommt am Ende der Runde in die Wiederholungsliste.</span>`;
  spStandZeigen();
  setTimeout(() => { spPos++; spZeige(); }, ok ? 900 : 1800);
}
let spBewertet = false;
function spStandZeigen(){
  const el = document.getElementById('sp-stand'); if (!el) return;
  if (!spQueue.length){ el.innerHTML = ''; return; }
  const karte = Math.min(spPos + 1, spQueue.length);
  el.innerHTML = `<span>Karte <strong>${karte}</strong> von ${spQueue.length}</span><span class="sp-ok">✓ ${spRunde.ok} sofort</span><span class="sp-no">✗ ${spRunde.total - spRunde.ok} überlegt</span>` +
    (spMic ? `<span>🎤 ${spRunde.micOk} von ${spRunde.micTotal} erkannt</span>` : '<span class="sp-ohne">ohne Mikrofon – du bewertest dich selbst</span>');
}
function spMicToggle(){
  spMic = !spMic;
  const b = document.getElementById('sp-mic'); b.textContent = spMic ? '🎤 Mikrofon ist an' : '🎤 Mikrofon ist aus'; b.classList.toggle('ok', spMic);
  if (!spMic){ spRecStop(); spStatus(''); return; }
  if (spTimer && spQueue[spPos]) spRecStart(spQueue[spPos]);
  else spStatus('🎤 Mikrofon ist an – es hört ab der nächsten Karte zu.', 'info');
}
// Statuszeile unter der Karte: zeigt jederzeit, was das Mikrofon tut
function spStatus(html, typ){
  const el = document.getElementById('sp-gehoert'); if (!el) return;
  el.className = 'sp-gehoert' + (typ ? ' sp-' + typ : '');
  el.innerHTML = html;
}
const SP_FEHLER = {
  'not-allowed': '🚫 Mikrofon blockiert. Bitte oben in der Adressleiste das Mikrofon für diese Seite erlauben und neu laden.',
  'service-not-allowed': '🚫 Spracherkennung ist in diesem Browser gesperrt. Bitte Chrome oder Safari verwenden.',
  'audio-capture': '🎤 Kein Mikrofon gefunden. Bitte ein Mikrofon anschließen oder in den Systemeinstellungen freigeben.',
  'network': '📶 Die Spracherkennung braucht eine Internetverbindung (Chrome schickt die Aufnahme an Google).',
  'language-not-supported': 'Deutsch wird von der Spracherkennung dieses Browsers nicht unterstützt.'
};
function spRecStart(e){
  if (!SpRecCtor){ spStatus('Dieser Browser hat keine Spracherkennung. Bitte Chrome oder Safari verwenden.', 'warn'); return; }
  spRecStop();
  const karte = spPos;
  try {
    const rec = new SpRecCtor(); spRec = rec;
    rec.lang = 'de-DE'; rec.interimResults = true; rec.continuous = true; rec.maxAlternatives = 3;
    rec.onstart = () => { if (spRec === rec && !spGehoert) spStatus('<span class="sp-puls">●</span> Ich höre zu … jetzt sprechen.', 'info'); };
    rec.onresult = ev => {
      let t = ''; for (const r of ev.results) t += r[0].transcript + ' ';
      spGehoert = t.trim(); spGehoertZeigen(e);
      // richtige Präposition sicher erkannt → Karte sofort auflösen (Belohnung ohne Warten)
      const last = ev.results[ev.results.length - 1];
      if (last && last.isFinal && !spOffen && spPos === karte && spUrteil(e).hat) spAufloesen();
    };
    rec.onerror = ev => {
      const msg = SP_FEHLER[ev.error];
      if (msg){ spStatus(msg, 'warn'); if (ev.error === 'not-allowed' || ev.error === 'service-not-allowed' || ev.error === 'audio-capture'){ spMic = false; const b = document.getElementById('sp-mic'); if (b){ b.textContent = '🎤 Mikrofon ist aus'; b.classList.remove('ok'); } } }
      else if (ev.error === 'no-speech' && !spGehoert && !spOffen) spStatus('🤫 Noch nichts gehört – bitte lauter oder näher am Mikrofon sprechen.', 'warn');
    };
    // Chrome beendet die Erkennung nach Sprechpausen von selbst → solange die Karte läuft, neu starten
    rec.onend = () => { if (spRec === rec && spMic && !spOffen && spPos === karte && spTimer){ try { rec.start(); } catch (x){} } };
    rec.start();
  } catch (x){ spRec = null; spStatus('Die Spracherkennung konnte nicht gestartet werden.', 'warn'); }
}
function spRecStop(){ if (spRec){ const r = spRec; spRec = null; try { r.onend = null; r.onresult = null; r.stop(); } catch (x){} } }
function spUrteil(e){
  const low = ' ' + spGehoert.toLowerCase().replace(/[.,!?;:„“"]/g, ' ').replace(/\s+/g, ' ') + ' ';
  const kontr = Object.keys(VAP_KONTR).filter(k => k.indexOf(e.p + ' ') === 0).map(k => VAP_KONTR[k]);
  const formen = [e.p, schreibDaForm(e.p), spWoForm(e.p)].concat(kontr);
  const hat = formen.some(f => low.indexOf(' ' + f + ' ') !== -1);
  const falsch = SP_PRAEPS.filter(p => p !== e.p && p !== e.p2 && low.indexOf(' ' + p + ' ') !== -1);
  const nomen = low.indexOf((e.m[1] + e.m[2]).toLowerCase()) !== -1;
  return {hat, falsch, nomen};
}
function spGehoertZeigen(e){
  if (!spGehoert) return;
  const u = spUrteil(e);
  const urteil = u.hat ? `<span class="sp-ok">✓ „${esc(e.p)}“ erkannt</span>` : u.falsch.length ? `<span class="sp-no">✗ „${esc(u.falsch[0])}“ statt „${esc(e.p)}“</span>` : '';
  spStatus(`🎤 Gehört: „${esc(spGehoert)}“ ${urteil}`, u.hat ? 'gut' : (u.falsch.length ? 'schlecht' : 'info'));
}
// Bewertung nach dem Auflösen: was hat das Mikrofon gehört?
function spMicFazit(e){
  if (!spMic) return;
  const u = spUrteil(e);
  let html, typ, empf = null;
  if (!spGehoert){ html = '🎤 Das Mikrofon hat nichts verstanden. Bewerte dich bitte selbst.'; typ = 'warn'; }
  else if (u.hat){ html = `🎤 Gehört: „${esc(spGehoert)}“ <span class="sp-ok">✓ Richtig – „${esc(e.p)}“ war dabei!</span>`; typ = 'gut'; empf = true; }
  else if (u.falsch.length){ html = `🎤 Gehört: „${esc(spGehoert)}“ <span class="sp-no">✗ Du hast „${esc(u.falsch[0])}“ gesagt – richtig ist „${esc(e.p)}“.</span>`; typ = 'schlecht'; empf = false; }
  else { html = `🎤 Gehört: „${esc(spGehoert)}“ <span class="sp-no">– die Präposition „${esc(e.p)}“ war nicht dabei.</span>`; typ = 'schlecht'; empf = false; }
  spStatus(html, typ);
  if (empf !== null){ spRunde.micTotal++; if (empf) spRunde.micOk++; spStandZeigen(); }
  if (empf !== null){ const btns = document.querySelectorAll('#sp-aktion .mc-opt'); if (btns.length === 2) btns[empf ? 0 : 1].classList.add('sp-empf'); }
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
    if (!spQueue.length || spPos >= spQueue.length) spStart(spMic); else if (!spOffen) spAufloesen(); else spBewerten(true);
  });
  // Mikrofon aus, sobald der Tab verlassen wird
  document.querySelectorAll('.nav-btn').forEach(b => b.addEventListener('click', () => { if (!document.getElementById('sec-5').classList.contains('active')) spStopp(); }));
  spZeige();
}

"""

VAPHINT = r"""// Merk-Hinweis ohne Lösung: Präposition (und da(r)+Präposition) im Hinweis maskieren
function vapHint(e){
  let h = e.h || '';
  const W = 'A-Za-zÄÖÜäöüß';
  [e.p, e.p2].filter(Boolean).forEach(p => {
    const da = (/^[aeiouäöü]/i.test(p) ? 'dar' : 'da') + p;
    h = h.replace(new RegExp('(^|[^' + W + '])' + da + '(?=$|[^' + W + '])', 'gi'), '$1da___')
         .replace(new RegExp('(^|[^' + W + '])' + p + '(?=$|[^' + W + '])', 'gi'), '$1___');
  });
  return h;
}
"""


# Was der Sprech-Trainer-Code aus der Seite braucht (sonst bricht er zur Laufzeit)
BRAUCHT = ['const VAP', 'VAP_GRUPPEN', 'VAP_KONTR', 'function vapVerbLabel', 'function vapPhrase',
           'KASUS_TXT', 'function schreibDaForm', 'function esc', 'class="tr-karte"', '.tr-karte']


def block_end(s, start, ende_muster):
    """Ende eines Blocks = Beginn des nächsten Abschnitts-Markers nach start."""
    i = s.index(start)
    m = re.compile(ende_muster, re.M).search(s, i + len(start))
    assert m, f'Blockende nach {start[:30]}… nicht gefunden'
    return i, m.start()


def ersetze_block(s, start, ende_muster, neu):
    i, j = block_end(s, start, ende_muster)
    return s[:i] + neu + s[j:]


def vaphint_sicherstellen(s, name):
    if 'function vapHint(' not in s:
        assert s.count(JS_START) == 1, name
        s = s.replace(JS_START, VAPHINT + JS_START, 1)
    # alle Hinweis-Ausgaben maskieren (Quiz: q, Trainer/Sprech-Trainer: e)
    s = s.replace('${q.h?`<div class="quiz-hint">(${esc(q.h)})</div>`:\'\'}',
                  '${q.h?`<div class="quiz-hint">(${esc(vapHint(q))})</div>`:\'\'}')
    s = s.replace('${e.h ? `<div class="quiz-hint">(${esc(e.h)})</div>` : \'\'}',
                  '${e.h ? `<div class="quiz-hint">(${esc(vapHint(e))})</div>` : \'\'}')
    assert 'esc(e.h)' not in s and 'esc(q.h)' not in s, f'{name}: unmaskierter Hinweis übrig'
    return s


def einbauen(s, name):
    # Nav: Merk-Werkstatt 5→6, Schreibwerkstatt 6→7, neuer Button an Position 5
    nav_old = '  <div class="nav-btn" onclick="showSection(5)"><span class="nav-emoji">💡</span>'
    assert nav_old in s, f'{name}: Nav-Anker (Merk-Werkstatt an Position 5) fehlt'
    s = s.replace('onclick="showSection(6)"><span class="nav-emoji">📨</span>', 'onclick="showSection(7)"><span class="nav-emoji">📨</span>', 1)
    s = s.replace(nav_old, '  <div class="nav-btn" onclick="showSection(5)"><span class="nav-emoji">🗣️</span><span class="nav-label">Sprechen</span></div>\n  <div class="nav-btn" onclick="showSection(6)"><span class="nav-emoji">💡</span>', 1)
    # Sections umnummerieren (Zwei-Phasen), neue Section vor Merk-Werkstatt
    assert s.count('id="sec-6"') == 1 and s.count('id="sec-5"') == 1, name
    s = s.replace('id="sec-6"', 'id="sec-__7"', 1).replace('id="sec-5"', 'id="sec-6"', 1).replace('id="sec-__7"', 'id="sec-7"', 1)
    marker = '<!-- ===== TAB 6 — MERK-WERKSTATT ===== -->'
    assert marker in s, f'{name}: HTML-Anker Merk-Werkstatt fehlt'
    s = s.replace(marker, HTML + '<!-- ===== TAB 7 — MERK-WERKSTATT ===== -->', 1)
    css_anchor = '/* ===== EIGENES MERK-WORT IN DER KARTE ===== */'
    assert css_anchor in s, f'{name}: CSS-Anker fehlt'
    s = s.replace(css_anchor, CSS + css_anchor, 1)
    js_anchor = '// ======== MERK-WERKSTATT (eigene Merk-Wörter) ========'
    assert js_anchor in s, f'{name}: JS-Anker fehlt'
    s = s.replace(js_anchor, JS + js_anchor, 1)
    assert s.count('\ninitTrainer();\n') == 1, f'{name}: initTrainer() nicht eindeutig'
    s = s.replace('\ninitTrainer();\n', '\ninitTrainer();\ninitSprechTrainer();\n', 1)
    return s


def aktualisieren(s, name):
    s = ersetze_block(s, CSS_START, r'^/\* =====', CSS)
    s = ersetze_block(s, HTML_START, r'^<!-- ===== TAB', HTML)
    s = ersetze_block(s, JS_START, r'^// ======== ', JS)
    return s


def pruefen(s, name):
    fehlt = [b for b in BRAUCHT if b not in s]
    assert not fehlt, f'{name}: Abhängigkeiten fehlen: {fehlt}'
    assert s.count(CSS_START) == 1 and s.count(HTML_START) == 1 and s.count(JS_START) == 1, f'{name}: Marker nicht genau einmal'
    assert CSS in s and HTML in s and JS in s, f'{name}: Blöcke nicht kanonisch'
    assert s.count('initSprechTrainer();') == 1, f'{name}: initSprechTrainer() nicht genau einmal'
    assert 'function vapHint(' in s and 'esc(e.h)' not in s and 'esc(q.h)' not in s, f'{name}: Hinweis verrät Lösung'


def check(ref):
    s = open(ref, encoding='utf-8').read()
    ok = True
    for name, start, ende, mein in [('CSS', CSS_START, r'^/\* =====', CSS), ('HTML', HTML_START, r'^<!-- ===== TAB', HTML), ('JS', JS_START, r'^// ======== ', JS)]:
        i, j = block_end(s, start, ende)
        if s[i:j] != mein:
            ok = False; print(f'DRIFT {name}: Referenz weicht vom Injektor ab')
    print('OK – Injektor entspricht der Referenz' if ok else '→ Blöcke im Injektor aus der Referenz neu übernehmen')
    sys.exit(0 if ok else 1)


def main(argv):
    if argv[:1] == ['--check']:
        check(argv[1]); return
    dry = argv[:1] == ['--dry-run']
    files = argv[1:] if dry else argv
    if not files:
        print(__doc__); sys.exit(2)
    for f in files:
        s = open(f, encoding='utf-8').read(); o = s
        modus = 'aktualisiert' if JS_START in s else 'eingebaut'
        s = aktualisieren(s, f) if JS_START in s else einbauen(s, f)
        s = vaphint_sicherstellen(s, f)
        pruefen(s, f)
        if s == o:
            print('unverändert (schon kanonisch)', f); continue
        if not dry:
            open(f, 'w', encoding='utf-8').write(s)
        print(('würde ' if dry else '') + modus, f)


if __name__ == '__main__':
    main(sys.argv[1:])
