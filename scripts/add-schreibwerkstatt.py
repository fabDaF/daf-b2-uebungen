#!/usr/bin/env python3
"""
Fügt einen Schreibwerkstatt-Tab in eine A1-DaF-HTML-Datei ein.

Idempotent: wenn die Datei bereits einen Schreibwerkstatt-Tab hat
(`schreibwerkstatt_A1_` oder `id="sec-schreib"`), wird sie übersprungen.

Usage:
    python3 scripts/add-schreibwerkstatt.py PFAD KONFIG_YAML

KONFIG_YAML enthält pro Datei:
  lesson_code: "1034R"
  lesson_title: "Omas Geburtstag"
  banner_url: "https://images.pexels.com/photos/733856/..."
  banner_alt: "..."
  intro: "Fünf kleine Schreibaufgaben rund um ..."
  tasks:
    - titel: "..."
      frage: "..."
      beispiel: "..."
    (5 Einträge)

Stand 2026-04-28: Niveau A1, R-Datei. Min-Zeichen 5.
"""
import sys, re, pathlib

# === Patch-Vorlagen ===========================================================

CSS_BLOCK = """
/* ===== Schreibwerkstatt — A1-Skalierung (kurze Antworten, niedrige Hürde) ===== */
.schreib-aufgabe-karte { background: #f8f9ff; padding: 16px 18px; margin-bottom: 16px; border-radius: 10px; border-left: 4px solid #667eea; transition: all 0.25s; }
.schreib-aufgabe-karte.gesendet { background: #f1f8e9; border-left-color: #689f38; }
.schreib-aufgabe-nr { display: inline-block; background: #667eea; color: white; font-weight: 700; font-size: 0.85em; padding: 2px 10px; border-radius: 12px; margin-right: 8px; vertical-align: middle; }
.schreib-aufgabe-karte.gesendet .schreib-aufgabe-nr { background: #689f38; }
.schreib-aufgabe-titel { font-weight: 700; color: #4a148c; font-size: 1.0em; vertical-align: middle; }
.schreib-aufgabe-karte.gesendet .schreib-aufgabe-titel { color: #33691e; }
.schreib-aufgabe-frage { color: #555; font-size: 0.92em; line-height: 1.5; margin: 8px 0 8px 0; }
.schreib-beispiel { font-size: 0.85em; color: #888; font-style: italic; margin-bottom: 8px; padding-left: 12px; border-left: 2px solid #e0e4ff; }
.schreib-mini-textarea { width: 100%; min-height: 70px; border: 1.5px solid #c5cff5; border-radius: 8px; padding: 10px 12px; font-family: 'Segoe UI', system-ui, sans-serif; font-size: 0.95em; line-height: 1.6; color: #1a1a1a; resize: vertical; outline: none; transition: border-color 0.2s; background: #fefefe; }
.schreib-mini-textarea:focus { border-color: #667eea; box-shadow: 0 0 0 2px rgba(102,126,234,0.15); }
.schreib-mini-footer { display: flex; align-items: center; justify-content: space-between; margin-top: 8px; flex-wrap: wrap; gap: 10px; }
.schreib-mini-meta { font-size: 0.82em; color: #888; }
.schreib-mini-meta strong { color: #667eea; font-weight: 700; }
.schreib-mini-status { font-size: 0.82em; color: #689f38; font-weight: 600; }
.schreib-mini-status.error { color: #c62828; }
.schreib-mini-btn { padding: 7px 14px; border-radius: 6px; border: 1.5px solid #667eea; background: white; color: #667eea; font-size: 0.83em; font-weight: 600; cursor: pointer; transition: all 0.15s; display: inline-flex; align-items: center; gap: 5px; white-space: nowrap; }
.schreib-mini-btn:hover:not(:disabled) { background: #667eea; color: white; box-shadow: 0 2px 6px rgba(102,126,234,0.3); }
.schreib-mini-btn:disabled { opacity: 0.55; cursor: not-allowed; }
.schreib-mini-btn.gesendet { border-color: #689f38; color: #689f38; background: #f1f8e9; }
.schreib-mini-btn.gesendet:hover:not(:disabled) { background: #689f38; color: white; }
.schreib-actions { display: flex; gap: 10px; flex-wrap: wrap; margin-top: 20px; padding-top: 18px; border-top: 1px solid #e0e4ff; }
.schreib-btn { padding: 10px 20px; border-radius: 8px; border: none; font-size: 0.95em; font-weight: 600; cursor: pointer; transition: all 0.2s; display: inline-flex; align-items: center; gap: 8px; }
.schreib-btn-primary { background: #667eea; color: white; }
.schreib-btn-primary:hover:not(:disabled) { background: #5568d3; box-shadow: 0 4px 12px rgba(102,126,234,0.35); transform: translateY(-1px); }
.schreib-btn-primary:disabled { background: #c5cff5; cursor: not-allowed; }
.schreib-btn-ghost { background: transparent; color: #667eea; border: 1.5px solid #c5cff5; }
.schreib-btn-ghost:hover { background: #f5f7ff; border-color: #667eea; }
.schreib-status { margin-top: 14px; padding: 12px 16px; border-radius: 8px; font-size: 0.92em; line-height: 1.5; display: none; }
.schreib-status.success { display: block; background: #e8f5e9; border-left: 4px solid #27ae60; color: #1b5e20; }
.schreib-status.error { display: block; background: #ffebee; border-left: 4px solid #e74c3c; color: #b71c1c; }
.schreib-status.info { display: block; background: #e3f2fd; border-left: 4px solid #2196f3; color: #0d47a1; }
.schreib-name { width: 100%; max-width: 320px; padding: 10px 14px; border: 1.5px solid #c5cff5; border-radius: 8px; font-family: inherit; font-size: 0.95em; outline: none; transition: border-color 0.2s; margin-bottom: 12px; }
.schreib-name:focus { border-color: #667eea; }
.schreib-label { display: block; font-size: 0.88em; color: #555; margin-bottom: 6px; font-weight: 600; }
.schreib-name-box { background: #fffaf0; border: 1.5px solid #ffd699; border-radius: 10px; padding: 14px 18px; margin-bottom: 18px; }
.schreib-name-box .schreib-label { color: #b15c00; }
.schreib-name.schreib-name-error { border-color: #c62828; box-shadow: 0 0 0 2px rgba(198,40,40,0.15); animation: schreib-name-shake 0.4s; }
@keyframes schreib-name-shake { 0%,100%{transform:translateX(0)} 25%{transform:translateX(-4px)} 75%{transform:translateX(4px)} }
"""

JS_BLOCK_TEMPLATE = """
/* ===== SCHREIBWERKSTATT (A1) =================================== */
var SCHREIB_NAME_KEY      = 'schreibwerkstatt_A1_{CODE}_name';
var SCHREIB_KEY_PREFIX    = 'schreibwerkstatt_A1_{CODE}_';
var SCHREIB_SENT_PREFIX   = 'schreibwerkstatt_A1_{CODE}_sent_';
var FORMSUBMIT_ENDPOINT   = 'https://formsubmit.co/ajax/unterricht@fabdaf.onmicrosoft.com';
var SCHREIB_LEKTION       = 'A1 – Lektion {CODE} · {TITLE}';
var SCHREIB_MIN_CHARS     = 5;

function initSchreibwerkstatt() {
  var nameInp = document.getElementById('sw-name');
  if (nameInp) {
    var savedName = localStorage.getItem(SCHREIB_NAME_KEY);
    if (savedName) nameInp.value = savedName;
    nameInp.addEventListener('input', function () {
      localStorage.setItem(SCHREIB_NAME_KEY, nameInp.value);
    });
  }
  document.querySelectorAll('.schreib-mini-textarea').forEach(function (ta) {
    var nr = ta.dataset.aufgabe;
    var saved = localStorage.getItem(SCHREIB_KEY_PREFIX + nr);
    if (saved) ta.value = saved;
    schreibUpdateCount(ta);
    var sentInfo = localStorage.getItem(SCHREIB_SENT_PREFIX + nr);
    if (sentInfo) schreibKarteAlsGesendetMarkieren(nr, sentInfo, true);
    ta.addEventListener('input', function () {
      schreibUpdateCount(ta);
      localStorage.setItem(SCHREIB_KEY_PREFIX + nr, ta.value);
      var btn = document.getElementById('sw-send-' + nr);
      if (btn && btn.classList.contains('gesendet')) {
        btn.classList.remove('gesendet');
        btn.innerHTML = '📨 Erneut senden';
      }
      var st = document.getElementById('sw-status-' + nr);
      if (st && st.classList.contains('error')) {
        st.classList.remove('error');
        st.textContent = '';
      }
    });
  });
}

function schreibUpdateCount(ta) {
  var nr = ta.dataset.aufgabe;
  var text = ta.value.trim();
  var words = text ? text.split(/\\s+/).filter(function (w) { return w.length > 0; }).length : 0;
  var wc = document.querySelector('.wc-' + nr);
  if (wc) wc.textContent = words;
}

function schreibKarteAlsGesendetMarkieren(nr, info, beimLaden) {
  var ta = document.querySelector('.schreib-mini-textarea[data-aufgabe="' + nr + '"]');
  var karte = ta && ta.closest('.schreib-aufgabe-karte');
  if (karte) karte.classList.add('gesendet');
  var btn = document.getElementById('sw-send-' + nr);
  if (btn) {
    btn.classList.add('gesendet');
    btn.innerHTML = beimLaden ? '✓ schon gesendet · erneut senden' : '✓ gesendet · erneut senden';
  }
  var status = document.getElementById('sw-status-' + nr);
  if (status) { status.classList.remove('error'); status.textContent = '✓ ' + info; }
}

function schreibStatusZeigen(typ, text) {
  var box = document.getElementById('sw-status');
  if (!box) return;
  box.className = 'schreib-status ' + typ;
  box.innerHTML = text;
}

function schreibAktuellerName() {
  var nameInp = document.getElementById('sw-name');
  return (nameInp && nameInp.value || '').trim();
}

function schreibNamePflicht() {
  var name = schreibAktuellerName();
  if (!name) {
    var nameInp = document.getElementById('sw-name');
    if (nameInp) {
      nameInp.classList.add('schreib-name-error');
      try { nameInp.focus(); nameInp.scrollIntoView({ behavior: 'smooth', block: 'center' }); } catch (e) {}
      setTimeout(function () { nameInp.classList.remove('schreib-name-error'); }, 3000);
    }
    return false;
  }
  return true;
}

function schreibPostFormsubmit(subject, message, onOk, onErr) {
  return fetch(FORMSUBMIT_ENDPOINT, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' },
    body: JSON.stringify({
      name: schreibAktuellerName(),
      _subject: subject,
      _template: 'box',
      _captcha: 'false',
      lektion: SCHREIB_LEKTION,
      message: message
    })
  })
    .then(function (r) { if (!r.ok) throw new Error('HTTP ' + r.status); return r.json(); })
    .then(onOk)
    .catch(onErr);
}

function schreibSendenEinzeln(nr) {
  var ta = document.querySelector('.schreib-mini-textarea[data-aufgabe="' + nr + '"]');
  var btn = document.getElementById('sw-send-' + nr);
  if (!ta || !btn) return;
  if (!schreibNamePflicht()) {
    var stN = document.getElementById('sw-status-' + nr);
    if (stN) { stN.classList.add('error'); stN.textContent = 'Bitte zuerst deinen Namen oben eintragen.'; }
    return;
  }
  var text = ta.value.trim();
  if (text.length < SCHREIB_MIN_CHARS) {
    var st = document.getElementById('sw-status-' + nr);
    if (st) { st.classList.add('error'); st.textContent = 'noch zu kurz — schreib bitte etwas mehr'; }
    return;
  }
  var titel = ta.dataset.titel || ('Aufgabe ' + nr);
  var subject = 'A1 {CODE} · Aufgabe ' + nr + ' · ' + titel + ' · ' + schreibAktuellerName();
  var message = '=== Aufgabe ' + nr + ': ' + titel + ' ===\\n\\n' + text;
  btn.disabled = true;
  var origLabel = btn.innerHTML;
  btn.innerHTML = '⏳ Wird gesendet …';

  schreibPostFormsubmit(subject, message,
    function () {
      btn.disabled = false;
      var jetzt = new Date();
      var info = 'gesendet um ' + String(jetzt.getHours()).padStart(2, '0') + ':' + String(jetzt.getMinutes()).padStart(2, '0');
      localStorage.setItem(SCHREIB_SENT_PREFIX + nr, info);
      schreibKarteAlsGesendetMarkieren(nr, info, false);
    },
    function () {
      btn.disabled = false; btn.innerHTML = origLabel;
      var st = document.getElementById('sw-status-' + nr);
      if (st) {
        var subjectEnc = encodeURIComponent(subject);
        var bodyEnc = encodeURIComponent('Name: ' + schreibAktuellerName() + '\\n\\n' + message);
        st.classList.add('error');
        st.innerHTML = '✗ Versand fehlgeschlagen — <a href="mailto:unterricht@fabdaf.onmicrosoft.com?subject=' + subjectEnc + '&body=' + bodyEnc + '" style="color:#c62828;font-weight:700;">stattdessen per Mail-Programm</a>';
      }
    }
  );
}

function schreibSendenAlleNochOffenen() {
  var btn = document.getElementById('sw-btn-all');
  if (!schreibNamePflicht()) {
    schreibStatusZeigen('error', '✗ Bitte zuerst deinen Namen oben eintragen.');
    return;
  }
  var offene = [];
  document.querySelectorAll('.schreib-mini-textarea').forEach(function (ta) {
    var nr = ta.dataset.aufgabe;
    var text = ta.value.trim();
    var sent = localStorage.getItem(SCHREIB_SENT_PREFIX + nr);
    if (text.length >= SCHREIB_MIN_CHARS && !sent) offene.push({ nr: nr, ta: ta, text: text });
  });
  if (offene.length === 0) {
    schreibStatusZeigen('info', 'ℹ Es gibt nichts Neues zu senden — alle Antworten sind entweder leer/sehr kurz oder bereits gesendet.');
    return;
  }
  var teile = offene.map(function (o) {
    var titel = o.ta.dataset.titel || ('Aufgabe ' + o.nr);
    return '=== Aufgabe ' + o.nr + ': ' + titel + ' ===\\n\\n' + o.text;
  });
  var subject = 'A1 {CODE} · ' + offene.length + ' Antworten · ' + schreibAktuellerName();
  var message = teile.join('\\n\\n');
  btn.disabled = true;
  btn.innerHTML = '⏳ Wird gesendet …';
  schreibStatusZeigen('info', '⏳ ' + offene.length + ' Antworten werden übermittelt …');
  schreibPostFormsubmit(subject, message,
    function () {
      btn.disabled = false;
      btn.innerHTML = '📨 Alle noch nicht gesendeten Antworten schicken';
      var jetzt = new Date();
      var info = 'gesendet um ' + String(jetzt.getHours()).padStart(2, '0') + ':' + String(jetzt.getMinutes()).padStart(2, '0');
      offene.forEach(function (o) {
        localStorage.setItem(SCHREIB_SENT_PREFIX + o.nr, info);
        schreibKarteAlsGesendetMarkieren(o.nr, info, false);
      });
      schreibStatusZeigen('success', '✓ <strong>' + offene.length + ' Antworten übermittelt.</strong> Frank meldet sich.');
    },
    function () {
      btn.disabled = false;
      btn.innerHTML = '📨 Alle noch nicht gesendeten Antworten schicken';
      schreibStatusZeigen('error', '✗ Direkter Versand nicht möglich. Bitte einzeln pro Karte versuchen oder „In Zwischenablage" verwenden.');
    }
  );
}

function schreibKopieren() {
  var teile = [];
  teile.push('Lektion: ' + SCHREIB_LEKTION);
  teile.push('Name: ' + (schreibAktuellerName() || '(kein Name)'));
  teile.push('');
  document.querySelectorAll('.schreib-mini-textarea').forEach(function (ta) {
    var nr = ta.dataset.aufgabe;
    var text = ta.value.trim();
    if (text.length >= SCHREIB_MIN_CHARS) {
      var titel = ta.dataset.titel || ('Aufgabe ' + nr);
      teile.push('=== Aufgabe ' + nr + ': ' + titel + ' ===');
      teile.push(text);
      teile.push('');
    }
  });
  if (teile.length <= 3) {
    schreibStatusZeigen('info', 'ℹ Noch nichts zum Kopieren — schreib mindestens eine Antwort.');
    return;
  }
  var alles = teile.join('\\n');
  if (navigator.clipboard && navigator.clipboard.writeText) {
    navigator.clipboard.writeText(alles).then(
      function () { schreibStatusZeigen('success', '✓ In Zwischenablage kopiert. Du kannst es jetzt in deine Mail einfügen.'); },
      function () { schreibStatusZeigen('error', '✗ Kopieren fehlgeschlagen. Bitte den Text manuell markieren.'); }
    );
  } else {
    schreibStatusZeigen('error', '✗ Dein Browser unterstützt das automatische Kopieren nicht.');
  }
}

function schreibLeeren() {
  if (!confirm('Wirklich ALLE Antworten zurücksetzen? Auch die schon gesendeten Markierungen werden entfernt.')) return;
  document.querySelectorAll('.schreib-mini-textarea').forEach(function (ta) {
    var nr = ta.dataset.aufgabe;
    ta.value = '';
    localStorage.removeItem(SCHREIB_KEY_PREFIX + nr);
    localStorage.removeItem(SCHREIB_SENT_PREFIX + nr);
    schreibUpdateCount(ta);
    var karte = ta.closest('.schreib-aufgabe-karte');
    if (karte) karte.classList.remove('gesendet');
    var btn = document.getElementById('sw-send-' + nr);
    if (btn) { btn.classList.remove('gesendet'); btn.innerHTML = '📨 An Frank senden'; }
    var st = document.getElementById('sw-status-' + nr);
    if (st) { st.className = 'schreib-mini-status'; st.textContent = ''; }
  });
  schreibStatusZeigen('info', 'ℹ Alle Antworten zurückgesetzt.');
}
/* ===== Ende Schreibwerkstatt =================================== */
"""


def task_card(idx, t):
    """Build HTML for one task card."""
    return f"""
      <div class="schreib-aufgabe-karte">
        <span class="schreib-aufgabe-nr">{idx}</span><span class="schreib-aufgabe-titel">{t['titel']}</span>
        <div class="schreib-aufgabe-frage">{t['frage']}</div>
        <div class="schreib-beispiel">Beispiel: „{t['beispiel']}"</div>
        <textarea class="schreib-mini-textarea" data-aufgabe="{idx}" data-titel="{t['titel']}"></textarea>
        <div class="schreib-mini-footer">
          <span class="schreib-mini-meta">Wörter: <strong class="wc-{idx}">0</strong> <span class="schreib-mini-status" id="sw-status-{idx}"></span></span>
          <button class="schreib-mini-btn" id="sw-send-{idx}" onclick="schreibSendenEinzeln({idx})">📨 An Frank senden</button>
        </div>
      </div>"""


def section_block(cfg):
    """Build the full <section> for the Schreibwerkstatt tab."""
    cards = "".join(task_card(i + 1, t) for i, t in enumerate(cfg['tasks']))
    return f"""    <!-- ===== TAB 6: SCHREIBWERKSTATT ===== -->
    <div class="section" id="sec-schreib">
      <img class="tab-banner" src="{cfg['banner_url']}" alt="{cfg['banner_alt']}">
      <div class="section-title">📨 Schreibwerkstatt</div>
      <div class="section-sub">{cfg['intro']}</div>

      <div class="hilfe-box">
        Schreiben ist das beste Training. Nimm dir Zeit für eine, zwei oder alle fünf Aufgaben. <strong>Jede Antwort kannst du einzeln an Frank schicken</strong> — du musst nicht alle bearbeiten. Wenn du den Sammelbutton am Ende benutzt, gehen alle noch nicht gesendeten Antworten in einer Mail.
      </div>

      <div class="schreib-name-box">
        <label class="schreib-label" for="sw-name">Dein Name (Pflicht — damit Frank weiß, wer geschrieben hat):</label>
        <input type="text" id="sw-name" class="schreib-name" placeholder="z. B. Maria Lopez" required>
      </div>
{cards}

      <div class="schreib-actions">
        <button class="schreib-btn schreib-btn-primary" id="sw-btn-all" onclick="schreibSendenAlleNochOffenen()">📨 Alle noch nicht gesendeten Antworten schicken</button>
        <button class="schreib-btn schreib-btn-ghost" onclick="schreibKopieren()">📋 In Zwischenablage</button>
        <button class="schreib-btn schreib-btn-ghost" onclick="schreibLeeren()">🗑️ Alles zurücksetzen</button>
      </div>
      <div class="schreib-status" id="sw-status"></div>
    </div>

    <!-- ===== TAB 7: WORTSCHATZ-TRAINING ===== -->"""


def patch_file(path: pathlib.Path, cfg: dict):
    html = path.read_text(encoding='utf-8')

    # Idempotency check
    if 'schreibwerkstatt_A1_' in html or 'id="sec-schreib"' in html:
        return f"SKIP {path.name} — bereits gepatcht"

    # 1. Nav-Buttons
    nav_old = ('<div class="nav-btn" onclick="showSection(5)"><span class="nav-emoji">🧩</span><span class="nav-label">Satzbau</span></div>\n'
               '        <div class="nav-btn" onclick="showSection(6)"><span class="nav-emoji">🔠</span><span class="nav-label">Wortschatz</span></div>')
    nav_new = ('<div class="nav-btn" onclick="showSection(5)"><span class="nav-emoji">🧩</span><span class="nav-label">Satzbau</span></div>\n'
               '        <div class="nav-btn" onclick="showSection(6)"><span class="nav-emoji">📨</span><span class="nav-label">Schreiben</span></div>\n'
               '        <div class="nav-btn" onclick="showSection(7)"><span class="nav-emoji">🔠</span><span class="nav-label">Wortschatz</span></div>')
    if nav_old not in html:
        return f"FAIL {path.name} — Nav-Pattern nicht gefunden"
    html = html.replace(nav_old, nav_new, 1)

    # 2. CSS-Block
    css_marker = '@media (max-width: 600px) { .tab-banner { max-height: 120px; } }\n</style>'
    if css_marker not in html:
        return f"FAIL {path.name} — CSS-Marker nicht gefunden"
    html = html.replace(css_marker, '@media (max-width: 600px) { .tab-banner { max-height: 120px; } }\n' + CSS_BLOCK + '\n</style>', 1)

    # 3. Section-Block
    section_marker = '<!-- ===== TAB 6: WORTSCHATZ-TRAINING ===== -->'
    if section_marker not in html:
        return f"FAIL {path.name} — Section-Marker nicht gefunden"
    html = html.replace(section_marker, section_block(cfg), 1)

    # 4. Init-Aufruf
    init_old = 'initSatzbau();\ninitWortschatz();\nloadBestTimes();'
    init_new = 'initSatzbau();\ninitWortschatz();\ninitSchreibwerkstatt();\nloadBestTimes();'
    if init_old not in html:
        return f"FAIL {path.name} — Init-Marker nicht gefunden"
    html = html.replace(init_old, init_new, 1)

    # 5. JS-Block
    js = JS_BLOCK_TEMPLATE.replace('{CODE}', cfg['lesson_code']).replace('{TITLE}', cfg['lesson_title'])
    js_marker = '/* ── Ende Tap-to-Select ─────────────────────────────────────────────── */\n</script>'
    if js_marker not in html:
        return f"FAIL {path.name} — JS-End-Marker nicht gefunden"
    html = html.replace(js_marker, '/* ── Ende Tap-to-Select ─────────────────────────────────────────────── */\n' + js + '\n</script>', 1)

    path.write_text(html, encoding='utf-8')
    return f"OK   {path.name}"


CONFIGS = {
    '1034R': {
        'lesson_code': '1034R',
        'lesson_title': 'Omas Geburtstag',
        'banner_url': 'https://images.pexels.com/photos/733856/pexels-photo-733856.jpeg?auto=compress&cs=tinysrgb&w=800',
        'banner_alt': 'Notizbuch und Stift, bereit zum Schreiben',
        'intro': 'Fünf kleine Schreibaufgaben rund um „Omas Geburtstag" und deine Familie.',
        'tasks': [
            {'titel': 'Deine Familie', 'frage': 'Wer gehört zu deiner Familie? Schreib zwei bis drei Sätze: Eltern, Geschwister, Großeltern.', 'beispiel': 'Ich habe einen Bruder und eine Schwester. Mein Bruder heißt Pablo. Meine Eltern wohnen in Madrid.'},
            {'titel': 'Ein Familienfest in deinem Land', 'frage': 'Welches Fest feiert deine Familie? Schreib zwei Sätze: Wann ist das Fest? Was esst ihr?', 'beispiel': 'Wir feiern Weihnachten am 24. Dezember. Wir essen Truthahn und Kuchen.'},
            {'titel': 'Eine Glückwunsch-Karte an Oma Emma', 'frage': 'Schreib eine kurze Glückwunsch-Karte an Oma Emma zum 90. Geburtstag.', 'beispiel': 'Liebe Oma Emma, alles Gute zum 90. Geburtstag! Bleib gesund und glücklich!'},
            {'titel': 'Eine Frage an Oma Emma', 'frage': 'Oma Emma ist 90 Jahre alt. Was möchtest du sie fragen? Schreib eine Frage.', 'beispiel': 'Oma Emma, was war dein Lieblings-Fest in deinem Leben?'},
            {'titel': 'Mini-Dialog mit Lisa', 'frage': 'Du triffst Lisa (Alex\\\' Schwester) auf dem Fest. Schreib einen Mini-Dialog: zwei Fragen und zwei Antworten.', 'beispiel': '— Hallo Lisa! Wie geht\\\'s? — Sehr gut! Ich bin frisch verheiratet! — Glückwunsch! Wie heißt dein Mann? — Er heißt Marco.'},
        ]
    },
    '1044R': {
        'lesson_code': '1044R',
        'lesson_title': 'Neuanfang',
        'banner_url': 'https://images.pexels.com/photos/733856/pexels-photo-733856.jpeg?auto=compress&cs=tinysrgb&w=800',
        'banner_alt': 'Notizbuch und Stift, bereit zum Schreiben',
        'intro': 'Fünf kleine Schreibaufgaben rund um „Neuanfang" und deinen Tagesablauf.',
        'tasks': [
            {'titel': 'Dein Tagesablauf', 'frage': 'Wie sieht dein normaler Tag aus? Schreib drei Sätze: Vormittag, Mittag, Abend.', 'beispiel': 'Vormittags arbeite ich. Mittags esse ich zu Hause. Abends gehe ich spazieren.'},
            {'titel': 'Ein guter Vorsatz', 'frage': 'Was möchtest du in Zukunft besser machen? Schreib einen Satz: Sport? Diät? Lernen?', 'beispiel': 'Ich möchte mehr Sport machen. Ich gehe jetzt zweimal die Woche schwimmen.'},
            {'titel': 'Im Fitnessstudio: Deine Daten', 'frage': 'Wie groß bist du? Wie viel wiegst du? Was machst du für Sport? Schreib zwei oder drei Sätze.', 'beispiel': 'Ich bin 1,70 Meter groß und wiege 65 Kilo. Ich gehe oft Joggen.'},
            {'titel': 'Eine Frage an Lucy', 'frage': 'Lucy arbeitet im Fitnessstudio. Schreib eine Frage an sie.', 'beispiel': 'Lucy, wie viel kostet ein Monat bei FitForever?'},
            {'titel': 'Mini-Dialog: Anmeldung', 'frage': 'Du meldest dich in einem Fitnessstudio an. Schreib einen Mini-Dialog: zwei Fragen und zwei Antworten.', 'beispiel': '— Guten Tag! Ich möchte mich anmelden. — Wie heißen Sie? — Ich heiße Maria. — Willkommen bei uns!'},
        ]
    },
    '1054R': {
        'lesson_code': '1054R',
        'lesson_title': 'Ein Wochenende in Berlin',
        'banner_url': 'https://images.pexels.com/photos/733856/pexels-photo-733856.jpeg?auto=compress&cs=tinysrgb&w=800',
        'banner_alt': 'Notizbuch und Stift, bereit zum Schreiben',
        'intro': 'Fünf kleine Schreibaufgaben rund um „Ein Wochenende in Berlin" und deine Stadt.',
        'tasks': [
            {'titel': 'Deine Stadt am Wochenende', 'frage': 'Was machst du am Wochenende in deiner Stadt? Schreib zwei Sätze.', 'beispiel': 'Am Samstag gehe ich ins Café. Am Sonntag mache ich einen Spaziergang im Park.'},
            {'titel': 'Eine Sehenswürdigkeit', 'frage': 'Was ist eine wichtige Sehenswürdigkeit in deiner Stadt oder deinem Land? Schreib zwei Sätze.', 'beispiel': 'In Madrid gibt es das Prado-Museum. Es hat sehr alte Bilder.'},
            {'titel': 'Ein Restaurant-Tipp', 'frage': 'Welches Restaurant magst du in deiner Stadt? Was isst man dort?', 'beispiel': 'Ich mag das Restaurant „La Cucina". Dort isst man italienische Pasta.'},
            {'titel': 'Eine Frage an Hermine', 'frage': 'Hermine ist 14 Jahre alt und liebt Berlin. Schreib eine Frage an sie.', 'beispiel': 'Hermine, was ist dein Lieblings-Ort in Berlin?'},
            {'titel': 'Mini-Dialog: Touristen', 'frage': 'Touristen kommen in deine Stadt. Schreib einen Mini-Dialog: sie fragen, du antwortest.', 'beispiel': '— Wo ist das Museum? — Es ist in der Hauptstraße. — Ist es weit? — Nein, nur zehn Minuten zu Fuß.'},
        ]
    },
    '1064R': {
        'lesson_code': '1064R',
        'lesson_title': 'Glückliche Hühner',
        'banner_url': 'https://images.pexels.com/photos/733856/pexels-photo-733856.jpeg?auto=compress&cs=tinysrgb&w=800',
        'banner_alt': 'Notizbuch und Stift, bereit zum Schreiben',
        'intro': 'Fünf kleine Schreibaufgaben rund um „Glückliche Hühner" und das Einkaufen.',
        'tasks': [
            {'titel': 'Dein Einkaufszettel', 'frage': 'Was kaufst du heute oder morgen ein? Schreib einen Einkaufszettel mit fünf bis acht Wörtern.', 'beispiel': 'Brot, Milch, Eier, Butter, Tomaten, Käse, Apfelsaft.'},
            {'titel': 'Dein Lieblings-Rezept', 'frage': 'Was kochst du gern? Schreib einen Satz: Welches Gericht? Welche Zutaten?', 'beispiel': 'Ich koche gern Pizza. Ich brauche Mehl, Tomaten, Käse und Basilikum.'},
            {'titel': 'Im Café — was bestellst du?', 'frage': 'Im Café — was bestellst du gern? Schreib zwei Sätze.', 'beispiel': 'Ich bestelle einen Cappuccino. Manchmal nehme ich auch ein Stück Kuchen.'},
            {'titel': 'Dein Hobby', 'frage': 'Louise tanzt Tango. Was ist dein Hobby? Schreib zwei Sätze.', 'beispiel': 'Mein Hobby ist Lesen. Ich lese gern Krimis am Abend.'},
            {'titel': 'Mini-Dialog im Supermarkt', 'frage': 'Du triffst eine Bekannte oder einen Bekannten im Supermarkt. Schreib einen Mini-Dialog: zwei Fragen und zwei Antworten.', 'beispiel': '— Hallo Maria! Was machst du hier? — Ich kaufe für ein Abendessen. — Schön! Wer kommt? — Meine Schwester und ihr Mann.'},
        ]
    },
    '2014R': {
        'lesson_code': '2014R',
        'lesson_title': 'Alex, der Schriftsteller',
        'banner_url': 'https://images.pexels.com/photos/733856/pexels-photo-733856.jpeg?auto=compress&cs=tinysrgb&w=800',
        'banner_alt': 'Notizbuch und Stift, bereit zum Schreiben',
        'intro': 'Fünf kleine Schreibaufgaben rund um „Alex, der Schriftsteller" und Berufe.',
        'tasks': [
            {'titel': 'Dein Beruf oder dein Wunsch', 'frage': 'Was ist dein Beruf? Wenn du noch nicht arbeitest: Was möchtest du werden? Schreib zwei Sätze.', 'beispiel': 'Ich bin Ingenieurin. Ich arbeite in einer großen Firma.'},
            {'titel': 'Vor- und Nachteile deines Berufs', 'frage': 'Was magst du an deinem Beruf? Was magst du nicht? Schreib zwei Sätze.', 'beispiel': 'Ich mag meine Kollegen. Aber ich mag die langen Stunden nicht.'},
            {'titel': 'Dein Traumberuf als Kind', 'frage': 'Was wolltest du als Kind werden? (wie Noah: Astronaut, König, Pilot ...)', 'beispiel': 'Als Kind wollte ich Tierärztin werden. Ich liebe Tiere sehr.'},
            {'titel': 'Eine Frage an Hermine', 'frage': 'Hermine möchte vielleicht Krankenschwester werden. Schreib eine Frage an sie.', 'beispiel': 'Hermine, warum möchtest du Krankenschwester werden?'},
            {'titel': 'Mini-Dialog: Vorstellungsgespräch', 'frage': 'Du machst ein Vorstellungsgespräch. Schreib einen Mini-Dialog: zwei Fragen und zwei Antworten.', 'beispiel': '— Was sind Sie von Beruf? — Ich bin Lehrerin. — Wie viele Jahre Erfahrung haben Sie? — Fünf Jahre.'},
        ]
    },
    '2024R': {
        'lesson_code': '2024R',
        'lesson_title': 'Ein Besuch',
        'banner_url': 'https://images.pexels.com/photos/733856/pexels-photo-733856.jpeg?auto=compress&cs=tinysrgb&w=800',
        'banner_alt': 'Notizbuch und Stift, bereit zum Schreiben',
        'intro': 'Fünf kleine Schreibaufgaben rund um „Ein Besuch" und deine Wohnung.',
        'tasks': [
            {'titel': 'Deine Wohnung beschreiben', 'frage': 'Wie ist deine Wohnung? Schreib zwei Sätze: Wie viele Zimmer? Hell oder dunkel? Groß oder klein?', 'beispiel': 'Meine Wohnung hat drei Zimmer. Sie ist klein, aber sehr hell.'},
            {'titel': 'Vor einem Besuch', 'frage': 'Was machst du, wenn ein Gast kommt? Schreib zwei Sätze.', 'beispiel': 'Ich räume die Küche auf. Ich koche Kaffee und mache Kuchen.'},
            {'titel': 'Dein Lieblings-Zimmer', 'frage': 'Welches Zimmer in deiner Wohnung magst du am liebsten? Schreib zwei Sätze.', 'beispiel': 'Ich mag mein Wohnzimmer. Es ist gemütlich und ich lese dort viel.'},
            {'titel': 'Eine Frage an Louise', 'frage': 'Louise sieht Alex\\\' Wohnung zum ersten Mal. Schreib eine Frage an sie.', 'beispiel': 'Louise, gefällt dir Alex\\\' Wohnung wirklich?'},
            {'titel': 'Mini-Dialog: Einladung zum Kaffee', 'frage': 'Du lädst eine Freundin zum Kaffee ein. Schreib einen Mini-Dialog: zwei Fragen und zwei Antworten.', 'beispiel': '— Hast du Lust auf einen Kaffee bei mir? — Klar, gerne! Wann? — Heute Nachmittag um 16 Uhr. — Perfekt, ich komme!'},
        ]
    },
    '2034R': {
        'lesson_code': '2034R',
        'lesson_title': 'Der Arzttermin',
        'banner_url': 'https://images.pexels.com/photos/733856/pexels-photo-733856.jpeg?auto=compress&cs=tinysrgb&w=800',
        'banner_alt': 'Notizbuch und Stift, bereit zum Schreiben',
        'intro': 'Fünf kleine Schreibaufgaben rund um „Der Arzttermin" und das Thema Gesundheit.',
        'tasks': [
            {'titel': 'Beim Arzt — was tut dir weh?', 'frage': 'Stell dir vor, du bist beim Arzt. Was tut dir weh? Schreib zwei Sätze.', 'beispiel': 'Mir tut der Kopf weh. Ich habe auch Halsschmerzen.'},
            {'titel': 'Wenn du krank bist', 'frage': 'Was machst du, wenn du krank bist? Schreib zwei Sätze.', 'beispiel': 'Ich bleibe im Bett. Ich trinke viel Tee mit Honig.'},
            {'titel': 'Ein Hausmittel aus deinem Land', 'frage': 'Welches Hausmittel kennst du aus deinem Land oder deiner Familie? Schreib zwei Sätze.', 'beispiel': 'In Spanien trinken wir bei Erkältung warme Milch mit Honig. Das hilft sehr.'},
            {'titel': 'Eine Frage an den Arzt', 'frage': 'Du bist beim Arzt und möchtest etwas wissen. Schreib eine Frage.', 'beispiel': 'Herr Doktor, wie lange muss ich die Medikamente nehmen?'},
            {'titel': 'Mini-Dialog: Termin vereinbaren', 'frage': 'Du rufst beim Arzt an und möchtest einen Termin. Schreib einen Mini-Dialog: zwei Fragen und zwei Antworten.', 'beispiel': '— Praxis Müller, guten Tag! — Hallo, ich brauche einen Termin. — Wann passt es? — Morgen um 10 Uhr, bitte.'},
        ]
    },
    '2044R': {
        'lesson_code': '2044R',
        'lesson_title': 'Freundinnen beim Shoppen',
        'banner_url': 'https://images.pexels.com/photos/733856/pexels-photo-733856.jpeg?auto=compress&cs=tinysrgb&w=800',
        'banner_alt': 'Notizbuch und Stift, bereit zum Schreiben',
        'intro': 'Fünf kleine Schreibaufgaben rund um „Freundinnen beim Shoppen" und Kleidung.',
        'tasks': [
            {'titel': 'Deine Lieblingskleidung', 'frage': 'Was trägst du am liebsten? Schreib zwei Sätze.', 'beispiel': 'Ich trage am liebsten Jeans und ein T-Shirt. Im Sommer trage ich gern Kleider.'},
            {'titel': 'Im Winter brauchst du …', 'frage': 'Was kaufst du im Winter? Schreib zwei oder drei Sätze.', 'beispiel': 'Ich brauche eine warme Jacke und Stiefel. Manchmal kaufe ich auch eine Mütze.'},
            {'titel': 'Was trägst du heute?', 'frage': 'Beschreib, was du heute anhast. Schreib zwei Sätze.', 'beispiel': 'Heute trage ich eine schwarze Hose und einen blauen Pullover. Meine Schuhe sind weiß.'},
            {'titel': 'Eine Frage an Louise', 'frage': 'Louise ist Mode-Designerin. Schreib eine Frage an sie.', 'beispiel': 'Louise, welche Farbe ist dieses Jahr modern?'},
            {'titel': 'Mini-Dialog: Im Geschäft', 'frage': 'Du bist im Kleidergeschäft. Schreib einen Mini-Dialog: zwei Fragen und zwei Antworten.', 'beispiel': '— Kann ich Ihnen helfen? — Ja, ich suche eine Hose. — Welche Größe? — 38 bitte.'},
        ]
    },
    '2054R': {
        'lesson_code': '2054R',
        'lesson_title': 'Cooler Urlaub in New York',
        'banner_url': 'https://images.pexels.com/photos/733856/pexels-photo-733856.jpeg?auto=compress&cs=tinysrgb&w=800',
        'banner_alt': 'Notizbuch und Stift, bereit zum Schreiben',
        'intro': 'Fünf kleine Schreibaufgaben rund um „Cooler Urlaub in New York" und das Reisen.',
        'tasks': [
            {'titel': 'Dein bester Urlaub', 'frage': 'Wo war dein bester Urlaub? Schreib zwei Sätze.', 'beispiel': 'Mein bester Urlaub war in Italien. Ich war zwei Wochen in Rom.'},
            {'titel': 'Was packst du in den Koffer?', 'frage': 'Was nimmst du immer mit in den Urlaub? Schreib drei bis fünf Sachen.', 'beispiel': 'Ich nehme T-Shirts, Sonnencreme, ein Buch, mein Handy und einen Fotoapparat mit.'},
            {'titel': 'Eine Sehenswürdigkeit', 'frage': 'Welche Stadt oder Sehenswürdigkeit möchtest du sehen? Schreib zwei Sätze.', 'beispiel': 'Ich möchte Paris sehen. Ich möchte den Eiffelturm besuchen.'},
            {'titel': 'Eine Frage an Alex und Nils', 'frage': 'Alex und Nils waren in New York. Schreib eine Frage an sie.', 'beispiel': 'Alex, was war dein Lieblings-Ort in New York?'},
            {'titel': 'Mini-Dialog: Am Flughafen', 'frage': 'Du bist am Flughafen. Schreib einen Mini-Dialog: zwei Fragen und zwei Antworten.', 'beispiel': '— Guten Tag, kann ich Ihren Pass sehen? — Ja, hier bitte. — Wo fliegen Sie hin? — Nach Madrid.'},
        ]
    },
    '2064R': {
        'lesson_code': '2064R',
        'lesson_title': 'Feste',
        'banner_url': 'https://images.pexels.com/photos/733856/pexels-photo-733856.jpeg?auto=compress&cs=tinysrgb&w=800',
        'banner_alt': 'Notizbuch und Stift, bereit zum Schreiben',
        'intro': 'Fünf kleine Schreibaufgaben rund um „Feste" und Feiertage in deinem Leben.',
        'tasks': [
            {'titel': 'Dein Lieblingsfest', 'frage': 'Welches Fest magst du am liebsten? Warum? Schreib zwei Sätze.', 'beispiel': 'Ich mag Weihnachten am liebsten. Die ganze Familie ist zusammen.'},
            {'titel': 'Was esst ihr beim Fest?', 'frage': 'Was kocht oder isst deine Familie an einem typischen Festtag? Schreib zwei Sätze.', 'beispiel': 'Zu Weihnachten essen wir Truthahn mit Kartoffeln. Zum Nachtisch gibt es Kuchen.'},
            {'titel': 'Ein typisches Fest in deinem Land', 'frage': 'Welches Fest gibt es in deinem Land? Schreib zwei Sätze.', 'beispiel': 'In Mexiko feiern wir den Día de los Muertos im November. Die Familien gedenken den Verstorbenen.'},
            {'titel': 'Eine Geburtstagseinladung', 'frage': 'Schreib eine kurze Einladung zu deiner Geburtstagsparty.', 'beispiel': 'Hallo Maria! Ich habe am Samstag Geburtstag. Komm um 19 Uhr zu mir!'},
            {'titel': 'Mini-Dialog: Auf der Silvesterparty', 'frage': 'Du bist auf einer Silvesterparty. Schreib einen Mini-Dialog: zwei Fragen und zwei Antworten.', 'beispiel': '— Hallo, frohes neues Jahr! — Danke, dir auch! — Was ist dein guter Vorsatz? — Ich möchte mehr Sport machen.'},
        ]
    },
}


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: add-schreibwerkstatt.py BASE_DIR LESSON_CODE [LESSON_CODE ...]")
        print("       BASE_DIR ist z.B. 'htmlS/A1.1 NEW'")
        print("       LESSON_CODE eines aus:", ', '.join(CONFIGS.keys()))
        sys.exit(2)

    base = pathlib.Path(sys.argv[1])
    for code in sys.argv[2:]:
        cfg = CONFIGS.get(code)
        if not cfg:
            print(f"FAIL — Konfig für {code} fehlt")
            continue
        # Find file in base directory matching code
        candidates = list(base.glob(f"DE_A1_{code}-*.html"))
        candidates = [c for c in candidates if not c.name.endswith('.bak')]
        if not candidates:
            print(f"FAIL — Datei DE_A1_{code}-*.html nicht gefunden")
            continue
        if len(candidates) > 1:
            print(f"FAIL — Mehrdeutig, gefunden:", [c.name for c in candidates])
            continue
        print(patch_file(candidates[0], cfg))
