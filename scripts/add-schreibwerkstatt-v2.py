#!/usr/bin/env python3
"""
Schreibwerkstatt-Patcher v2 — robust für A1, A2, B1, B2.

Unterschiede zu v1:
  * Niveau-Parameter: --niveau A2 setzt SCHREIB_MIN_CHARS, LocalStorage-Prefix,
    Lektions-Header und Mail-Subject-Prefix automatisch.
  * Erkennt fünf verschiedene Nav-Strukturen:
      (a) <div class="nav-btn" onclick="showSection(N)">     id="sec-N"
      (b) <div class="nav-btn" onclick="showTab(N)">         id="tab-N"
      (c) <div class="nav-btn" onclick="showTab(N)">         id="secN"
      (d) <button class="nav-btn" onclick="showTab(N,this)"> id="sec-N"
      (e) <button class="nav-btn" data-section="N">          id="secN"
  * CSS- und JS-Injektion ohne harte Marker (nutzt die letzte </style>
    bzw. </script>-Position).
  * Wenn die Datei keinen Wortschatz-Tab hat, wird die Schreibwerkstatt
    als LETZTER Tab eingefügt (statt als vorletzter).

Usage:
    python3 scripts/add-schreibwerkstatt-v2.py --niveau A2 \
            --basis "htmlS/A2.1" 1014R 1024R 1034R …

Konfigurationen liegen weiterhin in CONFIGS in dieser Datei. Pro Lektion ein
Eintrag wie in v1 — Schlüssel ist der Lektionscode (ohne Niveau-Prefix).
"""
from __future__ import annotations
import argparse, re, pathlib, sys

# --- Niveau-Skalierung -------------------------------------------------------

NIVEAU_DEFAULTS = {
    'A1': {'min_chars': 5,  'lektion_prefix': 'A1',  'mail_prefix': 'A1'},
    'A2': {'min_chars': 8,  'lektion_prefix': 'A2',  'mail_prefix': 'A2'},
    'B1': {'min_chars': 12, 'lektion_prefix': 'B1',  'mail_prefix': 'B1'},
    'B2': {'min_chars': 14, 'lektion_prefix': 'B2',  'mail_prefix': 'B2'},
}

# --- CSS-Block ---------------------------------------------------------------

CSS_BLOCK = """
/* ===== Schreibwerkstatt — Niveau-flexibel ===== */
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

# --- JS-Block-Template -------------------------------------------------------

JS_BLOCK_TEMPLATE = """
/* ===== SCHREIBWERKSTATT ({NIVEAU}) =================================== */
var SCHREIB_NAME_KEY      = 'schreibwerkstatt_{NIVEAU}_{CODE}_name';
var SCHREIB_KEY_PREFIX    = 'schreibwerkstatt_{NIVEAU}_{CODE}_';
var SCHREIB_SENT_PREFIX   = 'schreibwerkstatt_{NIVEAU}_{CODE}_sent_';
var FORMSUBMIT_ENDPOINT   = 'https://formsubmit.co/ajax/unterricht@fabdaf.onmicrosoft.com';
var SCHREIB_LEKTION       = '{NIVEAU} – Lektion {CODE} · {TITLE}';
var SCHREIB_MIN_CHARS     = {MIN_CHARS};

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
  var subject = '{MAIL_PREFIX} {CODE} · Aufgabe ' + nr + ' · ' + titel + ' · ' + schreibAktuellerName();
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
  var subject = '{MAIL_PREFIX} {CODE} · ' + offene.length + ' Antworten · ' + schreibAktuellerName();
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

# --- Building blocks ---------------------------------------------------------

def task_card_html(idx: int, t: dict) -> str:
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


def section_html(cfg: dict, wrap_tag: str) -> str:
    cards = "".join(task_card_html(i + 1, t) for i, t in enumerate(cfg['tasks']))
    return f"""<{wrap_tag} class="section" id="sec-schreib">
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
    </{wrap_tag}>"""


def nav_button_html(tag: str, idx: int, handler: str | None) -> str:
    """Build the Schreiben nav-button matching the file's existing style."""
    if handler is None or handler == 'data-section':
        return (f'<{tag} class="nav-btn" data-section="{idx}">'
                f'<span class="nav-emoji">📨</span>'
                f'<span class="nav-label">Schreiben</span></{tag}>')
    if handler == 'data-tab':
        return (f'<{tag} class="nav-btn" data-tab="{idx}">'
                f'<span class="nav-emoji">📨</span>'
                f'<span class="nav-label">Schreiben</span></{tag}>')
    if handler == 'showTabThis':
        return (f'<{tag} class="nav-btn" onclick="showTab({idx},this)">'
                f'<span class="nav-emoji">📨</span>'
                f'<span class="nav-label">Schreiben</span></{tag}>')
    if handler == 'zeigeSec':
        return (f'<{tag} class="nav-btn" onclick="zeigeSec({idx},this)">'
                f'<span class="nav-emoji">📨</span>'
                f'<span class="nav-label">Schreiben</span></{tag}>')
    # plain showSection / showTab / switchTab
    return (f'<{tag} class="nav-btn" onclick="{handler}({idx})">'
            f'<span class="nav-emoji">📨</span>'
            f'<span class="nav-label">Schreiben</span></{tag}>')


# --- Pattern detection -------------------------------------------------------

NAV_BTN_RE = re.compile(
    # Captures: tag, handler-name (or empty), index (from onclick / data-section / data-tab).
    # has-this-arg flag is detected later.
    r'<(?P<tag>div|button)\s+class="nav-btn[^"]*"\s+'
    r'(?:onclick="(?P<fn>showSection|showTab|switchTab|zeigeSec)\((?P<oidx>\d+)(?P<extra>(?:\s*,\s*this)?)\)(?:\s*;\s*[a-zA-Z_$][\w$]*\([^)]*\))*"'
    r'|data-section="(?P<didx>\d+)"'
    r'|data-tab="(?P<tidx>\d+)")[^>]*>'
    r'(?P<inner>(?:[^<]|<(?!/(?P=tag)>)[^>]*>)*)'
    r'</(?P=tag)>',
    re.DOTALL,
)


def parse_nav_buttons(html: str) -> list[dict]:
    """Return a list of all nav-btn elements found in html.
       Each entry: {start, end, tag, handler, idx, full, label, has_this}
    """
    out = []
    for m in NAV_BTN_RE.finditer(html):
        full = m.group(0)
        # Extract label from inner span
        label_m = re.search(r'<span class="nav-label">([^<]*)</span>', m.group('inner'))
        label = (label_m.group(1) if label_m else '').strip()
        if m.group('didx') is not None:
            handler = 'data-section'  # marker (None was ambiguous)
            idx = int(m.group('didx'))
            has_this = False
        elif m.group('tidx') is not None:
            handler = 'data-tab'
            idx = int(m.group('tidx'))
            has_this = False
        else:
            handler = m.group('fn')
            idx = int(m.group('oidx'))
            has_this = bool(m.group('extra') and ',' in m.group('extra'))
            if handler == 'showTab' and has_this:
                handler = 'showTabThis'
        out.append(dict(
            start=m.start(), end=m.end(), tag=m.group('tag'),
            handler=handler, idx=idx, full=full, label=label, has_this=has_this,
        ))
    return out


def detect_nav_pattern(html: str) -> dict | None:
    """Find the right nav-button to insert Schreiben before. Returns:
       tag/handler/idx/full_match/sec_id_prefix/sec_wrap_tag/no_wortschatz/append.
       'append' = True if Schreiben should be inserted AFTER full_match (not before)."""
    nav_btns = parse_nav_buttons(html)
    if not nav_btns:
        return None

    last = nav_btns[-1]
    max_idx = max(b['idx'] for b in nav_btns)
    wortschatz_btns = [b for b in nav_btns if b['label'].lower() == 'wortschatz']

    if wortschatz_btns and wortschatz_btns[-1] is last and last['idx'] == max_idx:
        # Wortschatz is the last nav-btn AND has the highest idx →
        # Schreiben goes before it, takes its idx, Wortschatz is bumped.
        target = wortschatz_btns[-1]
        sec_prefix, sec_wrap_tag = detect_section_style(html, target['idx'])
        return dict(
            tag=target['tag'], handler=target['handler'], idx=target['idx'],
            full_match=target['full'], sec_id_prefix=sec_prefix,
            sec_wrap_tag=sec_wrap_tag, no_wortschatz=False, append=False,
        )

    # Wortschatz missing, OR not last, OR last-but-with-anomalous-idx →
    # append Schreiben as a new tab with idx = max_idx+1 after last nav-btn.
    # The Schreiben SECTION is also appended at the END of all sections.
    sec_prefix, sec_wrap_tag = detect_section_style(html, max_idx)
    # Use the LAST nav-btn for the full_match (so we know where to insert HTML),
    # but synthesize the index from max_idx so we don't collide.
    return dict(
        tag=last['tag'], handler=last['handler'], idx=max_idx,
        full_match=last['full'], sec_id_prefix=sec_prefix,
        sec_wrap_tag=sec_wrap_tag, no_wortschatz=True, append=True,
    )


def detect_section_style(html: str, idx: int) -> tuple[str, str]:
    """Return (id_prefix, wrap_tag) for the section with the given index.
       Tries multiple prefixes; returns special prefix '@positional' if no ID
       matches but plain `<div class="section...">` elements are present
       (in document order)."""
    for prefix in ['sec-', 'sec', 'tab-', 'tab', 'section', 's']:
        for tag in ['div', 'section']:
            pat = rf'<{tag}[^>]*\bid="{re.escape(prefix)}{idx}"[^>]*>'
            if re.search(pat, html):
                return prefix, tag
    # Fallback: positional. Check that we DO have section elements at all.
    for tag in ['div', 'section']:
        if re.search(rf'<{tag}[^>]*class="[^"]*\bsection\b[^"]*"', html):
            return '@positional', tag
    return 'sec-', 'div'


# --- Patcher -----------------------------------------------------------------

def find_wortschatz_section(html: str, idx: int, prefix: str, tag: str) -> tuple[int, int] | None:
    """Return (start, end) char range of the Wortschatz <section>/<div> opening tag.
       For prefix '@positional' uses the idx-th section in document order."""
    if prefix == '@positional':
        sections = list(re.finditer(rf'<{tag}[^>]*class="[^"]*\bsection\b[^"]*"[^>]*>', html))
        if 0 <= idx < len(sections):
            m = sections[idx]
            return (m.start(), m.end())
        return None
    pat = rf'<{tag}[^>]*\bid="{re.escape(prefix)}{idx}"[^>]*>'
    m = re.search(pat, html)
    return (m.start(), m.end()) if m else None


def patch_file(path: pathlib.Path, cfg: dict, niveau: str, niveau_cfg: dict) -> str:
    html = path.read_text(encoding='utf-8')
    # Idempotency
    if 'id="sec-schreib"' in html or f'schreibwerkstatt_{niveau}_' in html:
        return f"SKIP {path.name} — bereits gepatcht"

    pat = detect_nav_pattern(html)
    if not pat:
        return f"FAIL {path.name} — keine Nav-Struktur erkannt"

    ws_idx = pat['idx']
    append_mode = pat.get('append', False)

    # Determine new index for the Schreiben button
    if append_mode:
        # Schreiben becomes new last tab at idx+1
        schreib_idx = ws_idx + 1
        new_ws_idx = None
    else:
        # Schreiben takes the spot before Wortschatz; Wortschatz shifts up by 1
        schreib_idx = ws_idx
        new_ws_idx = ws_idx + 1

    # 1. Insert/Replace nav-button
    schreib_btn = nav_button_html(pat['tag'], schreib_idx, pat['handler'])

    if append_mode:
        html = html.replace(pat['full_match'], pat['full_match'] + '\n        ' + schreib_btn, 1)
    else:
        new_ws_btn = bump_index_in_match(pat['full_match'], pat, new_ws_idx)
        html = html.replace(pat['full_match'], schreib_btn + '\n        ' + new_ws_btn, 1)

    # 2. Insert section
    sec_html = section_html(cfg, pat['sec_wrap_tag'])

    if append_mode:
        last_sec = find_last_section_close(html, pat['sec_wrap_tag'], pat['sec_id_prefix'])
        if last_sec is None:
            return f"FAIL {path.name} — letzte Section nicht gefunden"
        html = html[:last_sec] + '\n\n    ' + sec_html + html[last_sec:]
    else:
        ws_pos = find_wortschatz_section(html, ws_idx, pat['sec_id_prefix'], pat['sec_wrap_tag'])
        if ws_pos is None:
            return f"FAIL {path.name} — Wortschatz-Section nicht gefunden (prefix={pat['sec_id_prefix']}, idx={ws_idx})"
        html = html[:ws_pos[0]] + sec_html + '\n\n    ' + html[ws_pos[0]:]

    # 3. Bump indices in JS function bodies (lazy-init refs to ws_idx → ws_idx+1)
    if not append_mode:
        html = bump_function_body_indexes(html, ws_idx, new_ws_idx)

    # 4. CSS — inject before LAST </style>
    css_pos = html.rfind('</style>')
    if css_pos == -1:
        return f"FAIL {path.name} — </style> nicht gefunden"
    html = html[:css_pos] + CSS_BLOCK + '\n' + html[css_pos:]

    # 5. Init call
    if 'initSchreibwerkstatt()' not in html:
        injected = False
        for marker in ['initWortschatz();', 'initVocab();', 'loadBestTimes();', 'initSatzbau();', 'buildLuecken();', 'buildRF();']:
            if marker in html:
                html = html.replace(marker, marker + '\ninitSchreibwerkstatt();', 1)
                injected = True
                break
        if not injected:
            # Fallback: inject just before the LAST </script> as a deferred call
            # (works regardless of whether the file uses DOMContentLoaded or inline init)
            tail = '\nif (document.readyState === "loading") { document.addEventListener("DOMContentLoaded", initSchreibwerkstatt); } else { initSchreibwerkstatt(); }\n'
            sp = html.rfind('</script>')
            html = html[:sp] + tail + html[sp:]

    # 6. JS block — before LAST </script>
    js = (JS_BLOCK_TEMPLATE
            .replace('{NIVEAU}', niveau)
            .replace('{CODE}', cfg['lesson_code'])
            .replace('{TITLE}', cfg['lesson_title'])
            .replace('{MIN_CHARS}', str(niveau_cfg['min_chars']))
            .replace('{MAIL_PREFIX}', niveau_cfg['mail_prefix'])
         )
    js_pos = html.rfind('</script>')
    if js_pos == -1:
        return f"FAIL {path.name} — </script> nicht gefunden"
    html = html[:js_pos] + js + '\n' + html[js_pos:]

    path.write_text(html, encoding='utf-8')
    if append_mode:
        return f"OK   {path.name} (Schreiben={schreib_idx}, append-mode)"
    return f"OK   {path.name} (Schreiben={schreib_idx}, Wortschatz={new_ws_idx})"


def bump_index_in_match(full: str, pat: dict, new_idx: int) -> str:
    """Replace the Wortschatz nav button's index with new_idx."""
    if pat['handler'] is None or pat['handler'] == 'data-section':
        return re.sub(r'data-section="\d+"', f'data-section="{new_idx}"', full, count=1)
    if pat['handler'] == 'data-tab':
        return re.sub(r'data-tab="\d+"', f'data-tab="{new_idx}"', full, count=1)
    if pat['handler'] == 'showTabThis':
        return re.sub(r'showTab\(\d+\s*,\s*this\)', f'showTab({new_idx},this)', full, count=1)
    if pat['handler'] == 'zeigeSec':
        return re.sub(r'zeigeSec\(\d+\s*,\s*this\)', f'zeigeSec({new_idx},this)', full, count=1)
    # Plain showSection / showTab / switchTab — replace just the first arg
    return re.sub(rf"{pat['handler']}\(\d+", f"{pat['handler']}({new_idx}", full, count=1)


def bump_function_body_indexes(html: str, old_idx: int, new_idx: int) -> str:
    """Inside showSection/showTab/zeigeSec function bodies, bump literal idx
       comparisons (idx === N) where N == old_idx → new_idx. Also handles
       arguments[0] === N. This avoids breaking lazy-init logic when we
       shift Wortschatz from idx N to N+1."""
    for fn_name in ['showSection', 'showTab', 'zeigeSec', 'switchTab']:
        fn_re = re.compile(rf'(function {fn_name}\([^)]*\)\s*\{{)(.*?)(\n\s*\}})', re.DOTALL)
        m = fn_re.search(html)
        if not m:
            continue
        body = m.group(2)
        new_body = re.sub(
            rf'(idx ===\s*){old_idx}\b',
            rf'\g<1>{new_idx}',
            body,
        )
        new_body = re.sub(
            rf'(arguments\[0\] ===\s*){old_idx}\b',
            rf'\g<1>{new_idx}',
            new_body,
        )
        if new_body != body:
            html = html[:m.start()] + m.group(1) + new_body + m.group(3) + html[m.end():]
    return html


def find_last_section_close(html: str, wrap_tag: str, id_prefix: str) -> int | None:
    """Find the position right BEFORE the closing tag of the LAST section
       in the document (i.e., where to insert a new section to make it the
       new last)."""
    if id_prefix == '@positional':
        pat = re.compile(rf'<{wrap_tag}[^>]*class="[^"]*\bsection\b[^"]*"[^>]*>', re.DOTALL)
    else:
        pat = re.compile(rf'<{wrap_tag}[^>]*\bid="{re.escape(id_prefix)}\d+"[^>]*>', re.DOTALL)
    matches = list(pat.finditer(html))
    if not matches:
        return None
    # Find the closing tag of the last section. We balance opening tags from
    # the last opening tag forward.
    last = matches[-1]
    pos = last.end()
    depth = 1
    open_close_re = re.compile(rf'</?{wrap_tag}\b[^>]*>', re.DOTALL)
    for m in open_close_re.finditer(html, pos):
        if m.group(0).startswith('</'):
            depth -= 1
            if depth == 0:
                return m.end()
        else:
            depth += 1
    return None


# --- CONFIGS placeholder -----------------------------------------------------

CONFIGS: dict[str, dict] = {}  # filled in via lesson-specific imports


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--niveau', required=True, choices=list(NIVEAU_DEFAULTS.keys()))
    p.add_argument('--basis', required=True, help='Basis-Verzeichnis (z.B. "htmlS/A2.1")')
    p.add_argument('codes', nargs='+', help='Lektions-Codes (z.B. 1014R 1024R …)')
    args = p.parse_args()

    niveau_cfg = NIVEAU_DEFAULTS[args.niveau]
    base = pathlib.Path(args.basis)

    # Lazy-load configs
    from importlib import import_module
    mod_name = f'configs_{args.niveau.lower()}'
    try:
        mod = import_module(mod_name)
        CONFIGS.update(mod.CONFIGS)
    except ImportError:
        # Allow running with empty configs (for testing the patcher logic)
        pass

    for code in args.codes:
        cfg = CONFIGS.get(code)
        if not cfg:
            print(f"FAIL — Konfig für {code} fehlt")
            continue
        cands = list(base.glob(f"DE_{args.niveau}_{code}-*.html"))
        cands = [c for c in cands if 'backup' not in c.name and '-uebungen' not in c.name]
        if not cands:
            print(f"FAIL — Datei DE_{args.niveau}_{code}-*.html nicht gefunden")
            continue
        if len(cands) > 1:
            print(f"FAIL — Mehrdeutig: {[c.name for c in cands]}")
            continue
        print(patch_file(cands[0], cfg, args.niveau, niveau_cfg))


if __name__ == '__main__':
    sys.path.insert(0, str(pathlib.Path(__file__).parent))
    main()
