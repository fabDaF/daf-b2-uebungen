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
    """Generischer Patcher — funktioniert für R-, X- und C-Dateien.
    Findet die Wortschatz-Position dynamisch via Regex."""
    html = path.read_text(encoding='utf-8')

    # Idempotency check
    if 'schreibwerkstatt_A1_' in html or 'id="sec-schreib"' in html:
        return f"SKIP {path.name} — bereits gepatcht"

    # 1. Nav-Button für Wortschatz finden (egal welcher Index)
    #    Erlaubt verschiedene Emoji-Varianten (z.B. 🔠 oder &#128260;)
    nav_re = re.compile(
        r'(<div class="nav-btn" onclick="showSection\((\d+)\)">'
        r'<span class="nav-emoji">[^<]+</span>'
        r'<span class="nav-label">Wortschatz</span></div>)'
    )
    m = nav_re.search(html)
    if not m:
        return f"FAIL {path.name} — Nav-Button für Wortschatz nicht gefunden"
    ws_idx = int(m.group(2))
    schreib_idx = ws_idx          # Schreiben übernimmt den alten Wortschatz-Index
    new_ws_idx = ws_idx + 1       # Wortschatz rückt um eins
    schreib_btn = (f'<div class="nav-btn" onclick="showSection({schreib_idx})">'
                   f'<span class="nav-emoji">📨</span>'
                   f'<span class="nav-label">Schreiben</span></div>')
    new_ws_btn = m.group(1).replace(f'showSection({ws_idx})', f'showSection({new_ws_idx})')
    html = html.replace(m.group(1), schreib_btn + '\n        ' + new_ws_btn, 1)

    # 2. CSS-Block — Marker etwas robuster machen
    css_re = re.compile(r'(@media \(max-width: 600px\) \{ \.tab-banner \{ max-height: 120px; \} \}\s*)\n</style>')
    css_match = css_re.search(html)
    if not css_match:
        return f"FAIL {path.name} — CSS-Marker nicht gefunden"
    html = html.replace(css_match.group(0), css_match.group(1) + '\n' + CSS_BLOCK + '\n</style>', 1)

    # 3. Section-Block — vor dem Wortschatz-Section-Kommentar einsetzen
    sec_re = re.compile(r'<!-- ===== TAB \d+: WORTSCHATZ[^>]*===== -->')
    sec_match = sec_re.search(html)
    if not sec_match:
        return f"FAIL {path.name} — Section-Marker nicht gefunden"
    # Die TAB-Nummer im Kommentar updaten
    new_ws_comment = f'<!-- ===== TAB {new_ws_idx}: WORTSCHATZ-TRAINING ===== -->'
    html = html.replace(sec_match.group(0), section_block_for(cfg, schreib_idx, new_ws_idx) + new_ws_comment, 1)

    # 4. Init-Aufruf — initSchreibwerkstatt() VOR loadBestTimes() ODER nach initWortschatz()/initVocab()
    if 'initSchreibwerkstatt()' not in html:
        if 'loadBestTimes();' in html:
            html = html.replace('loadBestTimes();', 'initSchreibwerkstatt();\nloadBestTimes();', 1)
        elif 'initWortschatz();' in html:
            html = html.replace('initWortschatz();', 'initWortschatz();\ninitSchreibwerkstatt();', 1)
        elif 'initVocab();' in html:
            html = html.replace('initVocab();', 'initVocab();\ninitSchreibwerkstatt();', 1)
        else:
            return f"FAIL {path.name} — kein bekannter Init-Marker (loadBestTimes/initWortschatz/initVocab)"

    # 5. JS-Block einfügen — vor </script>, ggf. nach Tap-to-Select-Marker
    js = JS_BLOCK_TEMPLATE.replace('{CODE}', cfg['lesson_code']).replace('{TITLE}', cfg['lesson_title'])
    tap_marker = '/* ── Ende Tap-to-Select ─────────────────────────────────────────────── */\n</script>'
    if tap_marker in html:
        html = html.replace(tap_marker, '/* ── Ende Tap-to-Select ─────────────────────────────────────────────── */\n' + js + '\n</script>', 1)
    else:
        # Fallback: einfach vor das letzte </script> setzen
        idx = html.rfind('</script>')
        if idx == -1:
            return f"FAIL {path.name} — Kein </script> gefunden"
        html = html[:idx] + js + '\n' + html[idx:]

    path.write_text(html, encoding='utf-8')
    return f"OK   {path.name} (Schreiben={schreib_idx}, Wortschatz={new_ws_idx})"


def section_block_for(cfg, schreib_idx, ws_idx):
    """Baut den Section-Block mit korrekten TAB-Nummern im Kommentar."""
    cards = "".join(task_card(i + 1, t) for i, t in enumerate(cfg['tasks']))
    return f"""    <!-- ===== TAB {schreib_idx}: SCHREIBWERKSTATT ===== -->
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

    """


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
    '1022X': {
        'lesson_code': '1022X',
        'lesson_title': 'Woher kommst du?',
        'banner_url': 'https://images.pexels.com/photos/733856/pexels-photo-733856.jpeg?auto=compress&cs=tinysrgb&w=800',
        'banner_alt': 'Notizbuch und Stift, bereit zum Schreiben',
        'intro': 'Fünf kleine Schreibaufgaben rund um Herkunft, Länder und Sprachen.',
        'tasks': [
            {'titel': 'Woher kommst du?', 'frage': 'Schreib zwei Sätze über dein Herkunftsland und deine Stadt.', 'beispiel': 'Ich komme aus Mexiko. Ich wohne in Guadalajara.'},
            {'titel': 'Welche Sprachen sprichst du?', 'frage': 'Welche Sprachen sprichst du? Schreib einen Satz mit Wörtern wie „und" oder „auch".', 'beispiel': 'Ich spreche Spanisch und Englisch. Jetzt lerne ich auch Deutsch.'},
            {'titel': 'Drei Länder, die du kennst', 'frage': 'Nenne drei Länder, die du besucht hast oder gut kennst.', 'beispiel': 'Ich kenne Spanien, Italien und Frankreich.'},
            {'titel': 'Eine Frage an einen neuen Freund', 'frage': 'Du triffst jemanden zum ersten Mal. Schreib eine Frage über die Herkunft.', 'beispiel': 'Hallo, woher kommst du? Sprichst du auch Englisch?'},
            {'titel': 'Mini-Dialog: Erstes Treffen', 'frage': 'Ihr lernt euch kennen. Schreib einen Mini-Dialog: zwei Fragen und zwei Antworten.', 'beispiel': '— Hallo! Wie heißt du? — Ich bin Carlos. Und du? — Ich bin Maria. Woher kommst du? — Aus Italien.'},
        ]
    },
    '1032X': {
        'lesson_code': '1032X',
        'lesson_title': 'Mehr über mich',
        'banner_url': 'https://images.pexels.com/photos/733856/pexels-photo-733856.jpeg?auto=compress&cs=tinysrgb&w=800',
        'banner_alt': 'Notizbuch und Stift, bereit zum Schreiben',
        'intro': 'Fünf kleine Schreibaufgaben rund um persönliche Daten und dich selbst.',
        'tasks': [
            {'titel': 'Drei Sätze über dich', 'frage': 'Schreib drei Sätze über dich: Name, Beruf, Wohnort.', 'beispiel': 'Ich heiße Pablo. Ich bin Lehrer. Ich wohne in Berlin.'},
            {'titel': 'Dein Familienstand', 'frage': 'Bist du verheiratet, ledig oder hast du eine Beziehung? Schreib einen Satz.', 'beispiel': 'Ich bin ledig und wohne allein.'},
            {'titel': 'Ein wichtiges Datum für dich', 'frage': 'Welches Datum ist wichtig für dich (Geburtstag, Hochzeitstag …)? Schreib zwei Sätze.', 'beispiel': 'Mein Geburtstag ist am 15. Mai. Ich werde dieses Jahr 30 Jahre alt.'},
            {'titel': 'Eine Frage an einen Klassenkameraden', 'frage': 'Stell jemandem aus deinem Kurs eine persönliche Frage.', 'beispiel': 'Wie alt bist du? Hast du Kinder?'},
            {'titel': 'Mini-Dialog: Persönliche Daten', 'frage': 'Du füllst ein Formular aus. Schreib einen Mini-Dialog mit dem Beamten.', 'beispiel': '— Wie ist Ihr Name? — Maria Lopez. — Wo wohnen Sie? — Hauptstraße 12, München.'},
        ]
    },
    '1042X': {
        'lesson_code': '1042X',
        'lesson_title': 'Zahlen, bitte!',
        'banner_url': 'https://images.pexels.com/photos/733856/pexels-photo-733856.jpeg?auto=compress&cs=tinysrgb&w=800',
        'banner_alt': 'Notizbuch und Stift, bereit zum Schreiben',
        'intro': 'Fünf kleine Schreibaufgaben rund um Zahlen, Preise und Bezahlen.',
        'tasks': [
            {'titel': 'Drei Lieblingszahlen', 'frage': 'Welche drei Zahlen sind für dich wichtig (Geburtstag, Glückszahl, Hausnummer …)? Schreib zwei Sätze.', 'beispiel': 'Meine Glückszahl ist 7. Mein Geburtstag ist am 22.'},
            {'titel': 'Was kostet das?', 'frage': 'Schreib zwei Beispiele: Was kostet bei dir Brot? Was kostet ein Kaffee?', 'beispiel': 'Ein Brot kostet bei mir 2,50 Euro. Ein Kaffee kostet 1,80 Euro.'},
            {'titel': 'Geld in deinem Land', 'frage': 'Welche Währung gibt es in deinem Land? Schreib einen Satz.', 'beispiel': 'In Mexiko bezahlt man mit Pesos.'},
            {'titel': 'Eine Frage zum Preis', 'frage': 'Du bist in einem Geschäft. Schreib eine Frage zum Preis.', 'beispiel': 'Entschuldigung, was kostet diese Tasche?'},
            {'titel': 'Mini-Dialog: An der Kasse', 'frage': 'Du bezahlst an der Kasse. Schreib einen Mini-Dialog: zwei Fragen und zwei Antworten.', 'beispiel': '— Das macht 12 Euro 50. — Hier sind 15 Euro. — Danke, hier ist Ihr Wechselgeld. — Auf Wiedersehen!'},
        ]
    },
    '1052X': {
        'lesson_code': '1052X',
        'lesson_title': 'Über meine Arbeit sprechen',
        'banner_url': 'https://images.pexels.com/photos/733856/pexels-photo-733856.jpeg?auto=compress&cs=tinysrgb&w=800',
        'banner_alt': 'Notizbuch und Stift, bereit zum Schreiben',
        'intro': 'Fünf kleine Schreibaufgaben rund um Beruf und Arbeit.',
        'tasks': [
            {'titel': 'Was bist du von Beruf?', 'frage': 'Schreib zwei Sätze über deine Arbeit.', 'beispiel': 'Ich bin Krankenschwester. Ich arbeite in einem Krankenhaus.'},
            {'titel': 'Wo arbeitest du?', 'frage': 'Wo arbeitest du? In einem Büro, zu Hause, draußen? Schreib zwei Sätze.', 'beispiel': 'Ich arbeite in einer Schule. Es gibt viele Kinder dort.'},
            {'titel': 'Was magst du an deiner Arbeit?', 'frage': 'Schreib einen Satz: Was gefällt dir gut? Was gefällt dir nicht?', 'beispiel': 'Ich mag meine Kollegen. Aber die Arbeit ist manchmal anstrengend.'},
            {'titel': 'Eine Frage an einen Kollegen', 'frage': 'Schreib eine Frage an einen Kollegen oder eine Kollegin.', 'beispiel': 'Wie lange arbeitest du schon hier?'},
            {'titel': 'Mini-Dialog: Über die Arbeit', 'frage': 'Jemand fragt nach deiner Arbeit. Schreib einen Mini-Dialog: zwei Fragen und zwei Antworten.', 'beispiel': '— Was sind Sie von Beruf? — Ich bin Architekt. — Und wo arbeiten Sie? — In Berlin, in einem Architekturbüro.'},
        ]
    },
    '1062X': {
        'lesson_code': '1062X',
        'lesson_title': 'Über die Zeit sprechen',
        'banner_url': 'https://images.pexels.com/photos/733856/pexels-photo-733856.jpeg?auto=compress&cs=tinysrgb&w=800',
        'banner_alt': 'Notizbuch und Stift, bereit zum Schreiben',
        'intro': 'Fünf kleine Schreibaufgaben rund um Uhrzeiten, Wochentage und Zeitangaben.',
        'tasks': [
            {'titel': 'Wie spät ist es jetzt?', 'frage': 'Schreib die Uhrzeit jetzt — in Ziffern und in Wörtern.', 'beispiel': 'Es ist 14:30 Uhr — halb drei am Nachmittag.'},
            {'titel': 'Dein Lieblingstag', 'frage': 'Welcher Tag der Woche ist dein Lieblingstag? Warum? Schreib zwei Sätze.', 'beispiel': 'Mein Lieblingstag ist Samstag. Ich treffe meine Freunde.'},
            {'titel': 'Wann stehst du auf?', 'frage': 'Wann stehst du auf? Wann gehst du ins Bett? Schreib zwei Sätze.', 'beispiel': 'Ich stehe um 7 Uhr auf. Ich gehe um 23 Uhr ins Bett.'},
            {'titel': 'Eine Frage zur Uhrzeit', 'frage': 'Du fragst auf der Straße jemanden nach der Zeit. Schreib eine Frage.', 'beispiel': 'Entschuldigung, wie spät ist es?'},
            {'titel': 'Mini-Dialog: Uhrzeit erfragen', 'frage': 'Du fragst nach Öffnungszeiten in einem Geschäft. Schreib einen Mini-Dialog.', 'beispiel': '— Wann öffnen Sie morgen? — Um 9 Uhr. — Und wann schließen Sie? — Um 18 Uhr.'},
        ]
    },
    '1072X': {
        'lesson_code': '1072X',
        'lesson_title': 'Ein Treffen ausmachen',
        'banner_url': 'https://images.pexels.com/photos/733856/pexels-photo-733856.jpeg?auto=compress&cs=tinysrgb&w=800',
        'banner_alt': 'Notizbuch und Stift, bereit zum Schreiben',
        'intro': 'Fünf kleine Schreibaufgaben rund um Verabredungen und Treffen.',
        'tasks': [
            {'titel': 'Eine Verabredung vorschlagen', 'frage': 'Schlag einer Freundin oder einem Freund ein Treffen vor — Wo? Wann?', 'beispiel': 'Hast du am Samstag Zeit? Wir können in der Stadt einen Kaffee trinken.'},
            {'titel': 'Was machst du gern mit Freunden?', 'frage': 'Was machst du gern, wenn du Freunde triffst? Schreib zwei Sätze.', 'beispiel': 'Ich gehe gern mit Freunden ins Kino. Manchmal kochen wir zusammen.'},
            {'titel': 'Du musst einen Termin absagen', 'frage': 'Du kannst nicht kommen. Schreib eine kurze Absage.', 'beispiel': 'Es tut mir leid, ich kann morgen nicht kommen. Ich bin krank.'},
            {'titel': 'Eine Frage zum Treffpunkt', 'frage': 'Du möchtest jemanden treffen. Schreib eine Frage zum Treffpunkt.', 'beispiel': 'Wo treffen wir uns? Vor dem Café oder im Park?'},
            {'titel': 'Mini-Dialog: Treffen vereinbaren', 'frage': 'Du machst ein Treffen aus. Schreib einen Mini-Dialog: zwei Fragen und zwei Antworten.', 'beispiel': '— Wann hast du Zeit? — Am Freitag um 19 Uhr. — Wo treffen wir uns? — Im Café Central.'},
        ]
    },
    '1082X': {
        'lesson_code': '1082X',
        'lesson_title': 'Mein Arbeitstag',
        'banner_url': 'https://images.pexels.com/photos/733856/pexels-photo-733856.jpeg?auto=compress&cs=tinysrgb&w=800',
        'banner_alt': 'Notizbuch und Stift, bereit zum Schreiben',
        'intro': 'Fünf kleine Schreibaufgaben rund um deinen Arbeitstag.',
        'tasks': [
            {'titel': 'Wann beginnt dein Arbeitstag?', 'frage': 'Wann fängst du mit der Arbeit an? Wann ist Feierabend? Schreib zwei Sätze.', 'beispiel': 'Ich beginne um 8 Uhr. Mein Feierabend ist um 17 Uhr.'},
            {'titel': 'Wie kommst du zur Arbeit?', 'frage': 'Wie kommst du zur Arbeit — zu Fuß, mit dem Auto, mit dem Bus? Schreib zwei Sätze.', 'beispiel': 'Ich fahre mit dem Bus zur Arbeit. Es dauert 30 Minuten.'},
            {'titel': 'Was machst du in der Mittagspause?', 'frage': 'Was machst du normalerweise in der Mittagspause? Schreib zwei Sätze.', 'beispiel': 'Ich esse mit Kollegen in der Kantine. Manchmal gehen wir spazieren.'},
            {'titel': 'Eine Frage an deinen Chef', 'frage': 'Schreib eine Frage an deinen Chef oder deine Chefin.', 'beispiel': 'Frau Müller, kann ich morgen einen Tag Urlaub nehmen?'},
            {'titel': 'Mini-Dialog: Bei der Arbeit', 'frage': 'Schreib einen Mini-Dialog mit einem Kollegen — zwei Fragen, zwei Antworten.', 'beispiel': '— Hast du heute viel zu tun? — Ja, sehr viel! — Brauchst du Hilfe? — Ja, das wäre super!'},
        ]
    },
    '1092X': {
        'lesson_code': '1092X',
        'lesson_title': 'Das mag ich',
        'banner_url': 'https://images.pexels.com/photos/733856/pexels-photo-733856.jpeg?auto=compress&cs=tinysrgb&w=800',
        'banner_alt': 'Notizbuch und Stift, bereit zum Schreiben',
        'intro': 'Fünf kleine Schreibaufgaben rund um deine Vorlieben.',
        'tasks': [
            {'titel': 'Was magst du gern?', 'frage': 'Schreib drei Sachen, die du gern magst (Essen, Hobbys, Tiere).', 'beispiel': 'Ich mag Pizza, Musik und Hunde.'},
            {'titel': 'Was magst du nicht?', 'frage': 'Schreib zwei Sachen, die du nicht magst.', 'beispiel': 'Ich mag keinen Kaffee. Ich mag auch keinen Regen.'},
            {'titel': 'Dein Lieblingsessen', 'frage': 'Was ist dein Lieblingsessen? Schreib zwei Sätze.', 'beispiel': 'Mein Lieblingsessen ist Pasta. Meine Mutter kocht sie sehr gut.'},
            {'titel': 'Eine Frage über Vorlieben', 'frage': 'Du fragst eine Freundin nach ihren Vorlieben. Schreib eine Frage.', 'beispiel': 'Was magst du lieber: Tee oder Kaffee?'},
            {'titel': 'Mini-Dialog: Über Geschmäcker', 'frage': 'Du sprichst mit einem Freund über Vorlieben. Schreib einen Mini-Dialog.', 'beispiel': '— Magst du Sushi? — Nein, ich mag keinen Fisch. — Und du, Pizza? — Pizza mag ich sehr!'},
        ]
    },
    '1102X': {
        'lesson_code': '1102X',
        'lesson_title': 'Wichtige Ausdrücke beim Einkaufen',
        'banner_url': 'https://images.pexels.com/photos/733856/pexels-photo-733856.jpeg?auto=compress&cs=tinysrgb&w=800',
        'banner_alt': 'Notizbuch und Stift, bereit zum Schreiben',
        'intro': 'Fünf kleine Schreibaufgaben rund um das Einkaufen und Kommunikation im Geschäft.',
        'tasks': [
            {'titel': 'Was kaufst du oft?', 'frage': 'Was kaufst du oft im Supermarkt? Schreib drei oder vier Sachen.', 'beispiel': 'Ich kaufe oft Brot, Milch, Käse und Obst.'},
            {'titel': 'Wo kaufst du ein?', 'frage': 'Wo kaufst du ein — Supermarkt, Markt, Bioladen? Schreib zwei Sätze.', 'beispiel': 'Ich gehe meistens in den Supermarkt. Manchmal kaufe ich auf dem Markt.'},
            {'titel': 'Höflich um etwas bitten', 'frage': 'Du suchst Brot im Supermarkt und findest es nicht. Schreib eine höfliche Frage.', 'beispiel': 'Entschuldigung, wo finde ich das Brot, bitte?'},
            {'titel': 'Eine Frage an die Verkäuferin', 'frage': 'Du möchtest etwas kaufen. Schreib eine Frage an die Verkäuferin.', 'beispiel': 'Haben Sie diese Hose auch in Größe 38?'},
            {'titel': 'Mini-Dialog: Im Geschäft', 'frage': 'Du gehst einkaufen. Schreib einen Mini-Dialog mit dem Verkäufer — zwei Fragen, zwei Antworten.', 'beispiel': '— Kann ich Ihnen helfen? — Ja, ich suche eine Jacke. — Welche Farbe? — Blau, bitte.'},
        ]
    },
    '1112X': {
        'lesson_code': '1112X',
        'lesson_title': 'Am Bahnhof',
        'banner_url': 'https://images.pexels.com/photos/733856/pexels-photo-733856.jpeg?auto=compress&cs=tinysrgb&w=800',
        'banner_alt': 'Notizbuch und Stift, bereit zum Schreiben',
        'intro': 'Fünf kleine Schreibaufgaben rund um den Bahnhof und Reisen mit dem Zug.',
        'tasks': [
            {'titel': 'Eine Reise planen', 'frage': 'Wohin möchtest du fahren? Schreib zwei Sätze: Stadt? Wann?', 'beispiel': 'Ich möchte am Wochenende nach Berlin fahren. Der Zug fährt um 9 Uhr.'},
            {'titel': 'Was nimmst du mit?', 'frage': 'Was nimmst du in den Zug mit? Schreib drei oder vier Sachen.', 'beispiel': 'Ich nehme einen Rucksack, ein Buch, Wasser und einen Apfel mit.'},
            {'titel': 'Eine Auskunft erfragen', 'frage': 'Du brauchst eine Information am Bahnhof. Schreib eine Frage.', 'beispiel': 'Entschuldigung, von welchem Gleis fährt der Zug nach Hamburg?'},
            {'titel': 'Eine Fahrkarte kaufen', 'frage': 'Du kaufst ein Ticket. Schreib eine Frage am Schalter.', 'beispiel': 'Eine Fahrkarte nach München, bitte. Wie viel kostet das?'},
            {'titel': 'Mini-Dialog: Am Schalter', 'frage': 'Du kaufst ein Ticket. Schreib einen Mini-Dialog: zwei Fragen, zwei Antworten.', 'beispiel': '— Wohin möchten Sie fahren? — Nach Köln. — Einfach oder hin und zurück? — Hin und zurück, bitte.'},
        ]
    },
    '1122X': {
        'lesson_code': '1122X',
        'lesson_title': 'Eine To-Do-Liste',
        'banner_url': 'https://images.pexels.com/photos/733856/pexels-photo-733856.jpeg?auto=compress&cs=tinysrgb&w=800',
        'banner_alt': 'Notizbuch und Stift, bereit zum Schreiben',
        'intro': 'Fünf kleine Schreibaufgaben rund um To-Do-Listen und tägliche Aufgaben.',
        'tasks': [
            {'titel': 'Deine To-Do-Liste für heute', 'frage': 'Schreib eine kurze To-Do-Liste für heute mit drei oder vier Aufgaben.', 'beispiel': 'Heute: einkaufen, Wäsche waschen, Maria anrufen, Buch lesen.'},
            {'titel': 'Was ist dringend?', 'frage': 'Was ist heute besonders wichtig? Schreib einen Satz.', 'beispiel': 'Heute muss ich unbedingt zum Arzt gehen.'},
            {'titel': 'Was schiebst du oft auf?', 'frage': 'Was schiebst du gern auf? Schreib einen Satz.', 'beispiel': 'Ich schiebe oft das Putzen auf. Ich mag es nicht.'},
            {'titel': 'Eine Erinnerung an einen Freund', 'frage': 'Du erinnerst einen Freund an etwas. Schreib eine kurze Nachricht.', 'beispiel': 'Hallo Tim, denk bitte an mein Buch. Ich brauche es morgen!'},
            {'titel': 'Mini-Dialog: Aufgabe verteilen', 'frage': 'Du verteilst Aufgaben mit jemandem. Schreib einen Mini-Dialog: zwei Fragen, zwei Antworten.', 'beispiel': '— Kannst du heute einkaufen? — Klar! Was brauchen wir? — Brot, Milch und Eier. — Okay, ich gehe gleich.'},
        ]
    },
    '2013X': {
        'lesson_code': '2013X',
        'lesson_title': 'Möbel kaufen',
        'banner_url': 'https://images.pexels.com/photos/733856/pexels-photo-733856.jpeg?auto=compress&cs=tinysrgb&w=800',
        'banner_alt': 'Notizbuch und Stift, bereit zum Schreiben',
        'intro': 'Fünf kleine Schreibaufgaben rund um Möbel und Wohnen.',
        'tasks': [
            {'titel': 'Möbel in deinem Wohnzimmer', 'frage': 'Welche Möbel hast du im Wohnzimmer? Schreib zwei oder drei Sätze.', 'beispiel': 'Ich habe ein Sofa, einen Tisch und zwei Stühle. Es gibt auch eine Lampe.'},
            {'titel': 'Was möchtest du noch kaufen?', 'frage': 'Welches Möbelstück möchtest du noch kaufen? Schreib zwei Sätze.', 'beispiel': 'Ich möchte ein neues Bett kaufen. Mein altes Bett ist nicht bequem.'},
            {'titel': 'Dein Lieblingsmöbel', 'frage': 'Welches Möbelstück magst du am liebsten? Warum? Schreib zwei Sätze.', 'beispiel': 'Ich mag mein Sofa am liebsten. Es ist sehr bequem zum Lesen.'},
            {'titel': 'Eine Frage im Möbelgeschäft', 'frage': 'Du suchst etwas im Möbelgeschäft. Schreib eine Frage.', 'beispiel': 'Entschuldigung, wo finde ich die Küchenstühle?'},
            {'titel': 'Mini-Dialog: Möbelkauf', 'frage': 'Du kaufst Möbel. Schreib einen Mini-Dialog: zwei Fragen, zwei Antworten.', 'beispiel': '— Suchen Sie etwas Bestimmtes? — Ja, einen Tisch für die Küche. — Wie groß soll er sein? — Für vier Personen.'},
        ]
    },
    '2023X': {
        'lesson_code': '2023X',
        'lesson_title': 'Öffentliche Verkehrsmittel',
        'banner_url': 'https://images.pexels.com/photos/733856/pexels-photo-733856.jpeg?auto=compress&cs=tinysrgb&w=800',
        'banner_alt': 'Notizbuch und Stift, bereit zum Schreiben',
        'intro': 'Fünf kleine Schreibaufgaben rund um Bus, Bahn und U-Bahn.',
        'tasks': [
            {'titel': 'Wie kommst du in die Stadt?', 'frage': 'Welche Verkehrsmittel benutzt du? Schreib zwei Sätze.', 'beispiel': 'Ich fahre mit der U-Bahn. Manchmal nehme ich auch den Bus.'},
            {'titel': 'Welches Verkehrsmittel magst du am liebsten?', 'frage': 'Was magst du lieber — Bus, Bahn, Auto, Fahrrad? Warum? Schreib zwei Sätze.', 'beispiel': 'Ich mag das Fahrrad am liebsten. Es ist schnell und gesund.'},
            {'titel': 'Eine kurze Wegbeschreibung', 'frage': 'Wie kommst du von zu Hause zur Arbeit oder zur Schule? Beschreib in zwei Sätzen.', 'beispiel': 'Ich gehe zu Fuß zum Bahnhof. Dann nehme ich den Zug nach Berlin.'},
            {'titel': 'Eine Frage an einen Mitreisenden', 'frage': 'Du sitzt im Bus und brauchst eine Information. Schreib eine Frage.', 'beispiel': 'Entschuldigung, wo muss ich aussteigen für den Zoo?'},
            {'titel': 'Mini-Dialog: Im Bus', 'frage': 'Du fragst nach dem Weg im Bus. Schreib einen Mini-Dialog: zwei Fragen, zwei Antworten.', 'beispiel': '— Hält dieser Bus am Hauptbahnhof? — Ja, in drei Stationen. — Danke! — Bitte schön!'},
        ]
    },
    '2033X': {
        'lesson_code': '2033X',
        'lesson_title': 'Bei der Post',
        'banner_url': 'https://images.pexels.com/photos/733856/pexels-photo-733856.jpeg?auto=compress&cs=tinysrgb&w=800',
        'banner_alt': 'Notizbuch und Stift, bereit zum Schreiben',
        'intro': 'Fünf kleine Schreibaufgaben rund um die Post.',
        'tasks': [
            {'titel': 'Hast du schon einen Brief geschickt?', 'frage': 'Wann hast du den letzten Brief geschickt? Schreib zwei Sätze.', 'beispiel': 'Ich habe letzten Monat eine Postkarte an meine Oma geschickt. Sie lebt in Italien.'},
            {'titel': 'Was schickst du gern?', 'frage': 'Was schickst du gern in einem Brief oder Paket? Schreib einen Satz.', 'beispiel': 'Ich schicke gern Postkarten aus dem Urlaub.'},
            {'titel': 'Ein Paket an einen Freund', 'frage': 'Du schickst ein Paket an einen Freund. Was ist drin? Schreib zwei Sätze.', 'beispiel': 'Im Paket ist ein Buch und eine Schokolade. Es ist ein Geschenk.'},
            {'titel': 'Eine Frage am Postschalter', 'frage': 'Du bist bei der Post. Schreib eine Frage an den Beamten.', 'beispiel': 'Wie viel kostet ein Paket nach Spanien?'},
            {'titel': 'Mini-Dialog: Bei der Post', 'frage': 'Du schickst etwas. Schreib einen Mini-Dialog: zwei Fragen, zwei Antworten.', 'beispiel': '— Ich möchte dieses Paket schicken. — Wohin? — Nach Madrid. — Das macht 12 Euro.'},
        ]
    },
    '2043X': {
        'lesson_code': '2043X',
        'lesson_title': 'Shoppen und Bezahlen',
        'banner_url': 'https://images.pexels.com/photos/733856/pexels-photo-733856.jpeg?auto=compress&cs=tinysrgb&w=800',
        'banner_alt': 'Notizbuch und Stift, bereit zum Schreiben',
        'intro': 'Fünf kleine Schreibaufgaben rund um Einkaufen und Bezahlen.',
        'tasks': [
            {'titel': 'Was kaufst du gern ein?', 'frage': 'Was kaufst du am liebsten? Schreib zwei Sätze.', 'beispiel': 'Ich kaufe gern Bücher. Manchmal kaufe ich auch neue Schuhe.'},
            {'titel': 'Bezahlst du mit Karte oder bar?', 'frage': 'Wie bezahlst du am liebsten — bar oder mit Karte? Schreib zwei Sätze.', 'beispiel': 'Ich bezahle meistens mit Karte. Bar nehme ich nur kleine Summen.'},
            {'titel': 'Ein gutes Schnäppchen', 'frage': 'Hast du etwas Gutes günstig gekauft? Schreib zwei Sätze.', 'beispiel': 'Letzte Woche habe ich eine Jacke für 30 Euro gekauft. Normal kostet sie 80 Euro!'},
            {'titel': 'Eine Frage zur Bezahlung', 'frage': 'Du möchtest mit Karte bezahlen. Schreib eine Frage.', 'beispiel': 'Kann ich mit Kreditkarte bezahlen?'},
            {'titel': 'Mini-Dialog: An der Kasse', 'frage': 'Du bezahlst an der Kasse. Schreib einen Mini-Dialog: zwei Fragen, zwei Antworten.', 'beispiel': '— Das macht 24 Euro 50. — Kann ich mit Karte bezahlen? — Ja, gerne. — Hier bitte. — Vielen Dank!'},
        ]
    },
    '2053X': {
        'lesson_code': '2053X',
        'lesson_title': 'Im Restaurant bestellen',
        'banner_url': 'https://images.pexels.com/photos/733856/pexels-photo-733856.jpeg?auto=compress&cs=tinysrgb&w=800',
        'banner_alt': 'Notizbuch und Stift, bereit zum Schreiben',
        'intro': 'Fünf kleine Schreibaufgaben rund um das Restaurant.',
        'tasks': [
            {'titel': 'Was isst du gern im Restaurant?', 'frage': 'Was bestellst du gern? Schreib zwei Sätze.', 'beispiel': 'Ich bestelle gern Pasta oder Pizza. Als Vorspeise nehme ich Salat.'},
            {'titel': 'Trinkst du Wein oder Bier?', 'frage': 'Was trinkst du im Restaurant? Schreib einen Satz.', 'beispiel': 'Ich trinke gern ein Glas Rotwein zum Essen.'},
            {'titel': 'Dein Lieblings-Restaurant', 'frage': 'Welches Restaurant magst du? Was ist gut dort? Schreib zwei Sätze.', 'beispiel': 'Ich mag „Trattoria Bella". Die Pizza ist super und das Tiramisu auch.'},
            {'titel': 'Eine Frage an den Kellner', 'frage': 'Du bist im Restaurant. Schreib eine Frage an den Kellner.', 'beispiel': 'Entschuldigung, was empfehlen Sie heute?'},
            {'titel': 'Mini-Dialog: Im Restaurant', 'frage': 'Du bestellst beim Kellner. Schreib einen Mini-Dialog: zwei Fragen, zwei Antworten.', 'beispiel': '— Was möchten Sie trinken? — Ein Wasser, bitte. — Und zum Essen? — Die Lasagne, bitte.'},
        ]
    },
    # ===== C-Dateien (Lerncheck / Ich kann …) =====
    '1014C': {
        'lesson_code': '1014C',
        'lesson_title': 'Ich kann im Deutschunterricht klarkommen',
        'banner_url': 'https://images.pexels.com/photos/733856/pexels-photo-733856.jpeg?auto=compress&cs=tinysrgb&w=800',
        'banner_alt': 'Notizbuch und Stift, bereit zum Schreiben',
        'intro': 'Fünf kleine Schreibaufgaben rund um den Deutschunterricht und das Lernen.',
        'tasks': [
            {'titel': 'Warum lernst du Deutsch?', 'frage': 'Warum lernst du Deutsch? Schreib zwei Sätze.', 'beispiel': 'Ich lerne Deutsch für meine Arbeit. Ich möchte in Deutschland arbeiten.'},
            {'titel': 'Was ist schwer an Deutsch?', 'frage': 'Was findest du schwer in Deutsch? Schreib zwei Sätze.', 'beispiel': 'Die Artikel sind schwer für mich. Auch die Aussprache von „ch" ist schwierig.'},
            {'titel': 'Was machst du gern im Unterricht?', 'frage': 'Was machst du gern in der Deutschstunde? Schreib zwei Sätze.', 'beispiel': 'Ich spreche gern mit anderen. Lesen mag ich auch.'},
            {'titel': 'Eine Frage an deine Lehrerin', 'frage': 'Was möchtest du deine Lehrerin oder deinen Lehrer fragen?', 'beispiel': 'Frau Schmidt, wann sind die Hausaufgaben fertig?'},
            {'titel': 'Mini-Dialog: Im Deutschkurs', 'frage': 'Schreib einen Mini-Dialog mit einem Klassenkameraden — zwei Fragen, zwei Antworten.', 'beispiel': '— Hallo! Wie lange lernst du schon Deutsch? — Drei Monate. Und du? — Ein Jahr. — Das ist schon gut!'},
        ]
    },
    '1024C': {
        'lesson_code': '1024C',
        'lesson_title': 'Ich kann mich vorstellen',
        'banner_url': 'https://images.pexels.com/photos/733856/pexels-photo-733856.jpeg?auto=compress&cs=tinysrgb&w=800',
        'banner_alt': 'Notizbuch und Stift, bereit zum Schreiben',
        'intro': 'Fünf kleine Schreibaufgaben rund um das Vorstellen.',
        'tasks': [
            {'titel': 'Stell dich kurz vor', 'frage': 'Schreib drei Sätze über dich: Name, Herkunft, Beruf.', 'beispiel': 'Ich heiße Anna. Ich komme aus Polen. Ich bin Pflegerin.'},
            {'titel': 'Wie geht es dir?', 'frage': 'Wie geht es dir heute? Warum? Schreib zwei Sätze.', 'beispiel': 'Heute geht es mir gut. Ich habe heute frei.'},
            {'titel': 'Stell jemanden anderen vor', 'frage': 'Beschreib eine Person aus deiner Familie oder von der Arbeit. Zwei Sätze.', 'beispiel': 'Das ist mein Bruder. Er heißt Pablo und ist 30 Jahre alt.'},
            {'titel': 'Eine erste Frage', 'frage': 'Du triffst jemanden zum ersten Mal. Was fragst du?', 'beispiel': 'Hallo, wie heißt du? Woher kommst du?'},
            {'titel': 'Mini-Dialog: Erstes Treffen', 'frage': 'Du lernst jemanden kennen. Schreib einen Mini-Dialog: zwei Fragen, zwei Antworten.', 'beispiel': '— Hi, ich bin Carlos. — Hallo, ich bin Maria. — Woher kommst du? — Aus Brasilien.'},
        ]
    },
    '1034C': {
        'lesson_code': '1034C',
        'lesson_title': 'Ich kann persönliche Daten angeben',
        'banner_url': 'https://images.pexels.com/photos/733856/pexels-photo-733856.jpeg?auto=compress&cs=tinysrgb&w=800',
        'banner_alt': 'Notizbuch und Stift, bereit zum Schreiben',
        'intro': 'Fünf kleine Schreibaufgaben rund um persönliche Daten.',
        'tasks': [
            {'titel': 'Dein Name und Alter', 'frage': 'Schreib deinen vollen Namen und dein Alter. Zwei Sätze.', 'beispiel': 'Mein Name ist Maria Lopez. Ich bin 28 Jahre alt.'},
            {'titel': 'Deine Adresse', 'frage': 'Schreib deine Adresse: Straße, Stadt, Land.', 'beispiel': 'Ich wohne in der Bahnhofstraße 5 in Hamburg, Deutschland.'},
            {'titel': 'Deine Telefonnummer', 'frage': 'Schreib deine Telefonnummer und deine E-Mail-Adresse.', 'beispiel': 'Tel: 0151 234 5678. E-Mail: maria.lopez@beispiel.de.'},
            {'titel': 'Eine Frage am Empfang', 'frage': 'Du bist am Empfang und musst Daten angeben. Schreib eine Frage an die Sekretärin.', 'beispiel': 'Entschuldigung, brauchen Sie auch meinen Pass?'},
            {'titel': 'Mini-Dialog: Beim Anmelden', 'frage': 'Du meldest dich irgendwo an. Schreib einen Mini-Dialog: zwei Fragen, zwei Antworten.', 'beispiel': '— Wie ist Ihr Name? — Maria Lopez. — Wann sind Sie geboren? — Am 15. Mai 1998.'},
        ]
    },
    '1044C': {
        'lesson_code': '1044C',
        'lesson_title': 'Ich kann einen Kaffee bestellen',
        'banner_url': 'https://images.pexels.com/photos/733856/pexels-photo-733856.jpeg?auto=compress&cs=tinysrgb&w=800',
        'banner_alt': 'Notizbuch und Stift, bereit zum Schreiben',
        'intro': 'Fünf kleine Schreibaufgaben rund um Café und Bestellung.',
        'tasks': [
            {'titel': 'Was bestellst du gern im Café?', 'frage': 'Was trinkst und isst du gern im Café? Schreib zwei Sätze.', 'beispiel': 'Ich trinke gern Cappuccino. Manchmal nehme ich auch ein Stück Kuchen.'},
            {'titel': 'Dein Lieblings-Café', 'frage': 'Welches Café magst du? Warum? Schreib zwei Sätze.', 'beispiel': 'Ich mag das „Café Lara". Es ist klein und sehr gemütlich.'},
            {'titel': 'Bestellst du lieber allein oder mit Freunden?', 'frage': 'Schreib zwei Sätze: gehst du allein ins Café oder mit Freunden?', 'beispiel': 'Ich gehe oft allein, mit einem Buch. Manchmal treffe ich Freunde.'},
            {'titel': 'Eine Frage an die Kellnerin', 'frage': 'Du bist im Café. Schreib eine Frage an die Kellnerin.', 'beispiel': 'Entschuldigung, haben Sie auch Tee?'},
            {'titel': 'Mini-Dialog: Im Café', 'frage': 'Du bestellst etwas. Schreib einen Mini-Dialog: zwei Fragen, zwei Antworten.', 'beispiel': '— Was möchten Sie? — Einen Kaffee, bitte. — Mit Milch und Zucker? — Nur mit Milch, danke.'},
        ]
    },
    '1054C': {
        'lesson_code': '1054C',
        'lesson_title': 'Ich kann über meine Arbeit sprechen',
        'banner_url': 'https://images.pexels.com/photos/733856/pexels-photo-733856.jpeg?auto=compress&cs=tinysrgb&w=800',
        'banner_alt': 'Notizbuch und Stift, bereit zum Schreiben',
        'intro': 'Fünf kleine Schreibaufgaben rund um deinen Beruf.',
        'tasks': [
            {'titel': 'Dein Beruf', 'frage': 'Was bist du von Beruf? Schreib zwei Sätze.', 'beispiel': 'Ich bin Buchhalter. Ich arbeite in einer kleinen Firma.'},
            {'titel': 'Deine Arbeitszeiten', 'frage': 'Wann arbeitest du? Schreib zwei Sätze.', 'beispiel': 'Ich arbeite von Montag bis Freitag, von 9 bis 17 Uhr.'},
            {'titel': 'Was magst du an deiner Arbeit?', 'frage': 'Was gefällt dir? Was nicht? Schreib einen Satz.', 'beispiel': 'Ich mag meine Kollegen. Aber die Stunden sind manchmal lang.'},
            {'titel': 'Eine Frage an einen Kollegen', 'frage': 'Schreib eine Frage an einen Kollegen oder eine Kollegin.', 'beispiel': 'Wie lange bist du schon hier in der Firma?'},
            {'titel': 'Mini-Dialog: Über Arbeit reden', 'frage': 'Jemand fragt nach deiner Arbeit. Schreib einen Mini-Dialog: zwei Fragen, zwei Antworten.', 'beispiel': '— Was machen Sie beruflich? — Ich bin Lehrerin. — Wo unterrichten Sie? — In einer Grundschule.'},
        ]
    },
    '1064C': {
        'lesson_code': '1064C',
        'lesson_title': 'Ich kann über die Zeit sprechen',
        'banner_url': 'https://images.pexels.com/photos/733856/pexels-photo-733856.jpeg?auto=compress&cs=tinysrgb&w=800',
        'banner_alt': 'Notizbuch und Stift, bereit zum Schreiben',
        'intro': 'Fünf kleine Schreibaufgaben rund um Uhrzeit und Datum.',
        'tasks': [
            {'titel': 'Wie spät ist es jetzt?', 'frage': 'Schreib die genaue Uhrzeit jetzt — in Ziffern und in Worten.', 'beispiel': 'Es ist 16:45 — Viertel vor fünf.'},
            {'titel': 'Wann hast du Geburtstag?', 'frage': 'Wann hast du Geburtstag? Schreib einen Satz mit Datum.', 'beispiel': 'Ich habe am 22. März Geburtstag.'},
            {'titel': 'Dein Tag — Uhrzeiten', 'frage': 'Schreib drei Uhrzeiten aus deinem Tag: Aufstehen, Mittagessen, Schlafen.', 'beispiel': 'Ich stehe um 7 Uhr auf. Ich esse um 13 Uhr. Ich schlafe um 23 Uhr.'},
            {'titel': 'Eine Frage zur Uhrzeit', 'frage': 'Du brauchst eine Information zu Öffnungszeiten. Schreib eine Frage.', 'beispiel': 'Entschuldigung, wann öffnet die Bibliothek heute?'},
            {'titel': 'Mini-Dialog: Termin', 'frage': 'Du machst einen Termin aus. Schreib einen Mini-Dialog: zwei Fragen, zwei Antworten.', 'beispiel': '— Wann passt es? — Am Montag um 14 Uhr. — Geht es auch um 16 Uhr? — Ja, kein Problem.'},
        ]
    },
    '1074C': {
        'lesson_code': '1074C',
        'lesson_title': 'Ich kann ein Treffen vereinbaren',
        'banner_url': 'https://images.pexels.com/photos/733856/pexels-photo-733856.jpeg?auto=compress&cs=tinysrgb&w=800',
        'banner_alt': 'Notizbuch und Stift, bereit zum Schreiben',
        'intro': 'Fünf kleine Schreibaufgaben rund um Verabredungen.',
        'tasks': [
            {'titel': 'Eine Verabredung vorschlagen', 'frage': 'Schreib einer Freundin oder einem Freund einen Vorschlag — Was? Wann?', 'beispiel': 'Hast du Lust ins Kino zu gehen? Vielleicht am Samstag?'},
            {'titel': 'Was machst du gern mit Freunden?', 'frage': 'Schreib zwei Aktivitäten, die du gern mit Freunden machst.', 'beispiel': 'Ich gehe gern essen oder ins Kino. Ein Kaffee am Nachmittag ist auch schön.'},
            {'titel': 'Du musst absagen', 'frage': 'Du kannst nicht kommen. Schreib eine kurze Absage.', 'beispiel': 'Tut mir leid, ich kann nicht kommen. Ich bin krank.'},
            {'titel': 'Eine Frage zum Treffpunkt', 'frage': 'Du fragst, wo du dich treffen sollt. Schreib eine Frage.', 'beispiel': 'Wo treffen wir uns am besten? Vor dem Café oder vor dem Kino?'},
            {'titel': 'Mini-Dialog: Verabredung', 'frage': 'Du machst ein Treffen aus. Schreib einen Mini-Dialog: zwei Fragen, zwei Antworten.', 'beispiel': '— Wann hast du Zeit? — Am Donnerstag. — Um wie viel Uhr? — Sagen wir 19 Uhr.'},
        ]
    },
    '1084C': {
        'lesson_code': '1084C',
        'lesson_title': 'Ich kann über meinen Zeitplan sprechen',
        'banner_url': 'https://images.pexels.com/photos/733856/pexels-photo-733856.jpeg?auto=compress&cs=tinysrgb&w=800',
        'banner_alt': 'Notizbuch und Stift, bereit zum Schreiben',
        'intro': 'Fünf kleine Schreibaufgaben rund um deinen Wochenplan.',
        'tasks': [
            {'titel': 'Dein Wochenplan', 'frage': 'Was machst du normalerweise unter der Woche? Schreib zwei Sätze.', 'beispiel': 'Von Montag bis Freitag arbeite ich. Am Wochenende treffe ich Freunde.'},
            {'titel': 'Dein Lieblingstag', 'frage': 'Welcher Tag ist dein Lieblingstag? Warum? Schreib zwei Sätze.', 'beispiel': 'Mein Lieblingstag ist Samstag. Ich kann lange schlafen.'},
            {'titel': 'Was hast du diese Woche vor?', 'frage': 'Was hast du diese Woche geplant? Schreib zwei oder drei Aktivitäten.', 'beispiel': 'Am Mittwoch gehe ich ins Fitnessstudio. Am Freitag treffe ich Anna.'},
            {'titel': 'Eine Frage zum Plan', 'frage': 'Du fragst einen Freund nach seinen Plänen. Schreib eine Frage.', 'beispiel': 'Hast du am Wochenende schon etwas vor?'},
            {'titel': 'Mini-Dialog: Pläne machen', 'frage': 'Du sprichst mit einem Freund über die Woche. Schreib einen Mini-Dialog: zwei Fragen, zwei Antworten.', 'beispiel': '— Was machst du heute Abend? — Ich gehe ins Theater. — Und morgen? — Morgen arbeite ich.'},
        ]
    },
    '1094C': {
        'lesson_code': '1094C',
        'lesson_title': 'Ich kann sagen, was ich mag',
        'banner_url': 'https://images.pexels.com/photos/733856/pexels-photo-733856.jpeg?auto=compress&cs=tinysrgb&w=800',
        'banner_alt': 'Notizbuch und Stift, bereit zum Schreiben',
        'intro': 'Fünf kleine Schreibaufgaben rund um Vorlieben und Geschmack.',
        'tasks': [
            {'titel': 'Drei Sachen, die du liebst', 'frage': 'Schreib drei Sachen, die du sehr gern magst.', 'beispiel': 'Ich liebe Schokolade, Musik und das Meer.'},
            {'titel': 'Dein Lieblingshobby', 'frage': 'Was ist dein Lieblingshobby? Schreib zwei Sätze.', 'beispiel': 'Mein Lieblingshobby ist Fotografieren. Ich mache jedes Wochenende Fotos.'},
            {'titel': 'Was magst du nicht?', 'frage': 'Was magst du nicht? Schreib zwei Sätze.', 'beispiel': 'Ich mag keine Spinnen. Auch laute Musik mag ich nicht.'},
            {'titel': 'Eine Frage über Vorlieben', 'frage': 'Du fragst eine Freundin nach ihren Vorlieben. Schreib eine Frage.', 'beispiel': 'Was magst du lieber, Sommer oder Winter?'},
            {'titel': 'Mini-Dialog: Vorlieben', 'frage': 'Du sprichst mit einem Freund über Geschmäcker. Schreib einen Mini-Dialog: zwei Fragen, zwei Antworten.', 'beispiel': '— Magst du Pizza? — Ja, sehr! — Und Sushi? — Nein, ich mag keinen Fisch.'},
        ]
    },
    '1104C': {
        'lesson_code': '1104C',
        'lesson_title': 'Ich kann Lebensmittel einkaufen',
        'banner_url': 'https://images.pexels.com/photos/733856/pexels-photo-733856.jpeg?auto=compress&cs=tinysrgb&w=800',
        'banner_alt': 'Notizbuch und Stift, bereit zum Schreiben',
        'intro': 'Fünf kleine Schreibaufgaben rund um den Lebensmitteleinkauf.',
        'tasks': [
            {'titel': 'Dein typischer Einkauf', 'frage': 'Was kaufst du normalerweise im Supermarkt? Schreib vier oder fünf Sachen.', 'beispiel': 'Ich kaufe Brot, Milch, Käse, Tomaten und Apfelsaft.'},
            {'titel': 'Wie oft kaufst du ein?', 'frage': 'Wie oft gehst du einkaufen? Schreib einen Satz.', 'beispiel': 'Ich gehe zweimal pro Woche einkaufen, meistens samstags.'},
            {'titel': 'Magst du Bio-Produkte?', 'frage': 'Kaufst du Bio-Lebensmittel? Schreib einen Satz.', 'beispiel': 'Ich kaufe oft Bio-Eier und Bio-Gemüse. Es ist gesünder.'},
            {'titel': 'Eine Frage im Supermarkt', 'frage': 'Du suchst etwas und findest es nicht. Schreib eine Frage.', 'beispiel': 'Entschuldigung, wo finde ich den Naturjoghurt?'},
            {'titel': 'Mini-Dialog: An der Käsetheke', 'frage': 'Du kaufst Käse. Schreib einen Mini-Dialog: zwei Fragen, zwei Antworten.', 'beispiel': '— Was darf es sein? — 200 Gramm Gouda, bitte. — Stück oder Scheiben? — In Scheiben, bitte.'},
        ]
    },
    '1114C': {
        'lesson_code': '1114C',
        'lesson_title': 'Ich kann Verkehrsmittel nutzen',
        'banner_url': 'https://images.pexels.com/photos/733856/pexels-photo-733856.jpeg?auto=compress&cs=tinysrgb&w=800',
        'banner_alt': 'Notizbuch und Stift, bereit zum Schreiben',
        'intro': 'Fünf kleine Schreibaufgaben rund um Verkehrsmittel.',
        'tasks': [
            {'titel': 'Wie kommst du in die Stadt?', 'frage': 'Mit welchem Verkehrsmittel fährst du? Schreib zwei Sätze.', 'beispiel': 'Ich fahre mit dem Fahrrad in die Stadt. Manchmal nehme ich auch den Bus.'},
            {'titel': 'Hast du ein Auto?', 'frage': 'Hast du ein Auto oder benutzt du den Bus? Schreib einen Satz.', 'beispiel': 'Ich habe kein Auto. Ich fahre immer mit der U-Bahn.'},
            {'titel': 'Eine Reise mit dem Zug', 'frage': 'Stell dir vor, du machst eine Zugreise. Wohin? Schreib zwei Sätze.', 'beispiel': 'Ich möchte mit dem Zug nach Berlin fahren. Es dauert vier Stunden.'},
            {'titel': 'Eine Frage am Bahnhof', 'frage': 'Du brauchst eine Information am Bahnhof. Schreib eine Frage.', 'beispiel': 'Entschuldigung, wann fährt der nächste Zug nach Köln?'},
            {'titel': 'Mini-Dialog: Im Bus', 'frage': 'Du fragst nach einer Haltestelle. Schreib einen Mini-Dialog: zwei Fragen, zwei Antworten.', 'beispiel': '— Hält dieser Bus am Hauptbahnhof? — Ja, in vier Stationen. — Danke! — Bitte sehr!'},
        ]
    },
    '1124C': {
        'lesson_code': '1124C',
        'lesson_title': 'Ich kann eine To-Do-Liste schreiben',
        'banner_url': 'https://images.pexels.com/photos/733856/pexels-photo-733856.jpeg?auto=compress&cs=tinysrgb&w=800',
        'banner_alt': 'Notizbuch und Stift, bereit zum Schreiben',
        'intro': 'Fünf kleine Schreibaufgaben rund um To-Do-Listen.',
        'tasks': [
            {'titel': 'Deine To-Do-Liste für morgen', 'frage': 'Was musst du morgen tun? Schreib drei oder vier Aufgaben.', 'beispiel': 'Morgen: einkaufen, Wäsche waschen, Mama anrufen, ein Buch lesen.'},
            {'titel': 'Deine wichtigste Aufgabe', 'frage': 'Was ist heute oder morgen besonders wichtig? Schreib einen Satz.', 'beispiel': 'Heute muss ich unbedingt zur Bank gehen.'},
            {'titel': 'Was schiebst du oft auf?', 'frage': 'Was machst du oft später? Schreib einen Satz.', 'beispiel': 'Ich schiebe das Putzen oft auf. Ich mag es nicht.'},
            {'titel': 'Eine Erinnerung an einen Freund', 'frage': 'Du erinnerst einen Freund an etwas Wichtiges. Schreib eine kurze Nachricht.', 'beispiel': 'Hallo Tim! Vergiss nicht, Mias Geschenk zu kaufen!'},
            {'titel': 'Mini-Dialog: Aufgaben verteilen', 'frage': 'Ihr verteilt Aufgaben. Schreib einen Mini-Dialog: zwei Fragen, zwei Antworten.', 'beispiel': '— Kannst du heute kochen? — Ja, klar. Was möchtest du essen? — Etwas Einfaches. — Pasta?'},
        ]
    },
    '1131C': {
        'lesson_code': '1131C',
        'lesson_title': 'Lernziele A1.1 erreicht',
        'banner_url': 'https://images.pexels.com/photos/733856/pexels-photo-733856.jpeg?auto=compress&cs=tinysrgb&w=800',
        'banner_alt': 'Notizbuch und Stift, bereit zum Schreiben',
        'intro': 'Fünf kleine Schreibaufgaben — eine Bilanz von A1.1.',
        'tasks': [
            {'titel': 'Was kannst du jetzt auf Deutsch?', 'frage': 'Schreib drei Sachen, die du jetzt auf Deutsch kannst.', 'beispiel': 'Ich kann mich vorstellen. Ich kann Zahlen sagen. Ich kann Kaffee bestellen.'},
            {'titel': 'Was war am schwersten?', 'frage': 'Was war für dich am schwersten in A1.1? Schreib zwei Sätze.', 'beispiel': 'Die Artikel waren am schwersten. Ich verwechsle oft „der" und „die".'},
            {'titel': 'Was möchtest du noch lernen?', 'frage': 'Was möchtest du als Nächstes lernen? Schreib zwei Sätze.', 'beispiel': 'Ich möchte Vergangenheit lernen. Und mehr Wörter über das Wohnen.'},
            {'titel': 'Eine Frage an deine Lehrerin', 'frage': 'Was möchtest du deine Lehrerin fragen? Schreib eine Frage.', 'beispiel': 'Frau Müller, wann beginnt der A1.2-Kurs?'},
            {'titel': 'Mini-Dialog: Kursende', 'frage': 'Du sprichst mit einem Klassenkameraden über den Kurs. Schreib einen Mini-Dialog.', 'beispiel': '— Das war schwer, oder? — Ja, aber ich habe viel gelernt. — Machst du A1.2? — Klar, ab nächsten Monat!'},
        ]
    },
    '2014C': {
        'lesson_code': '2014C',
        'lesson_title': 'Lerncheck Wohnung und Möbel',
        'banner_url': 'https://images.pexels.com/photos/733856/pexels-photo-733856.jpeg?auto=compress&cs=tinysrgb&w=800',
        'banner_alt': 'Notizbuch und Stift, bereit zum Schreiben',
        'intro': 'Fünf kleine Schreibaufgaben rund um Wohnung und Möbel.',
        'tasks': [
            {'titel': 'Beschreib deine Wohnung', 'frage': 'Wie groß ist deine Wohnung? Wie viele Zimmer? Schreib zwei Sätze.', 'beispiel': 'Meine Wohnung ist 60 Quadratmeter groß. Sie hat zwei Zimmer und eine Küche.'},
            {'titel': 'Möbel in deinem Zimmer', 'frage': 'Welche Möbel hast du in deinem Lieblingszimmer? Schreib drei oder vier Möbel.', 'beispiel': 'In meinem Wohnzimmer habe ich ein Sofa, einen Tisch, Stühle und einen Fernseher.'},
            {'titel': 'Was möchtest du ändern?', 'frage': 'Was möchtest du an deiner Wohnung ändern? Schreib zwei Sätze.', 'beispiel': 'Ich möchte eine neue Küche. Die alte ist zu klein.'},
            {'titel': 'Eine Frage an einen Vermieter', 'frage': 'Du suchst eine Wohnung. Schreib eine Frage an den Vermieter.', 'beispiel': 'Guten Tag, ist die Wohnung noch frei? Wie hoch ist die Miete?'},
            {'titel': 'Mini-Dialog: Wohnungsbesichtigung', 'frage': 'Du besichtigst eine Wohnung. Schreib einen Mini-Dialog: zwei Fragen, zwei Antworten.', 'beispiel': '— Wie groß ist die Küche? — 12 Quadratmeter. — Gibt es einen Balkon? — Ja, einen kleinen.'},
        ]
    },
    '2024C': {
        'lesson_code': '2024C',
        'lesson_title': 'Lerncheck Stadt und Wegbeschreibung',
        'banner_url': 'https://images.pexels.com/photos/733856/pexels-photo-733856.jpeg?auto=compress&cs=tinysrgb&w=800',
        'banner_alt': 'Notizbuch und Stift, bereit zum Schreiben',
        'intro': 'Fünf kleine Schreibaufgaben rund um Stadt und Wege.',
        'tasks': [
            {'titel': 'Deine Stadt', 'frage': 'Wo wohnst du? Wie ist es dort? Schreib zwei Sätze.', 'beispiel': 'Ich wohne in Hamburg. Es ist eine große, schöne Stadt am Wasser.'},
            {'titel': 'Was gibt es in deiner Nähe?', 'frage': 'Was gibt es in der Nähe deiner Wohnung? Schreib zwei Sätze.', 'beispiel': 'Bei mir gibt es einen Supermarkt und eine Bäckerei. Ein Park ist auch in der Nähe.'},
            {'titel': 'Wie kommst du zur Arbeit?', 'frage': 'Beschreib in zwei Sätzen, wie du zur Arbeit oder Schule kommst.', 'beispiel': 'Ich gehe drei Minuten zu Fuß zum Bahnhof. Dann fahre ich 20 Minuten mit dem Zug.'},
            {'titel': 'Nach dem Weg fragen', 'frage': 'Du suchst eine Apotheke. Schreib eine Frage an einen Passanten.', 'beispiel': 'Entschuldigung, wo ist die nächste Apotheke?'},
            {'titel': 'Mini-Dialog: Wegbeschreibung', 'frage': 'Du gibst eine Wegbeschreibung. Schreib einen Mini-Dialog: zwei Fragen, zwei Antworten.', 'beispiel': '— Wo ist die Post? — Gehen Sie geradeaus, dann links. — Ist es weit? — Nein, fünf Minuten zu Fuß.'},
        ]
    },
    '2034C': {
        'lesson_code': '2034C',
        'lesson_title': 'Lerncheck — in der Stadt erledigen',
        'banner_url': 'https://images.pexels.com/photos/733856/pexels-photo-733856.jpeg?auto=compress&cs=tinysrgb&w=800',
        'banner_alt': 'Notizbuch und Stift, bereit zum Schreiben',
        'intro': 'Fünf kleine Schreibaufgaben rund um Erledigungen in der Stadt.',
        'tasks': [
            {'titel': 'Was musst du heute erledigen?', 'frage': 'Was hast du heute oder morgen in der Stadt zu tun? Schreib drei Sätze.', 'beispiel': 'Ich muss zur Post gehen. Dann zur Bank. Und am Ende einkaufen.'},
            {'titel': 'Bei der Bank', 'frage': 'Was machst du oft bei der Bank? Schreib einen Satz.', 'beispiel': 'Ich hole oft Bargeld. Manchmal überweise ich Geld.'},
            {'titel': 'Bei der Post', 'frage': 'Was schickst du gern? Schreib zwei Sätze.', 'beispiel': 'Ich schicke manchmal Postkarten an meine Familie. Pakete schicke ich selten.'},
            {'titel': 'Eine Frage am Schalter', 'frage': 'Du bist am Schalter und brauchst Hilfe. Schreib eine Frage.', 'beispiel': 'Entschuldigung, wie viel kostet ein Brief nach Italien?'},
            {'titel': 'Mini-Dialog: Erledigungen', 'frage': 'Du erledigst etwas. Schreib einen Mini-Dialog: zwei Fragen, zwei Antworten.', 'beispiel': '— Kann ich Ihnen helfen? — Ja, ich möchte Geld abheben. — Wie viel? — 200 Euro, bitte.'},
        ]
    },
    '2044C': {
        'lesson_code': '2044C',
        'lesson_title': 'Lerncheck Kleidung kaufen',
        'banner_url': 'https://images.pexels.com/photos/733856/pexels-photo-733856.jpeg?auto=compress&cs=tinysrgb&w=800',
        'banner_alt': 'Notizbuch und Stift, bereit zum Schreiben',
        'intro': 'Fünf kleine Schreibaufgaben rund um Kleidung und Mode.',
        'tasks': [
            {'titel': 'Deine Lieblingsfarbe', 'frage': 'Welche Farbe trägst du am liebsten? Schreib einen Satz.', 'beispiel': 'Ich trage am liebsten Blau. Es passt zu allem.'},
            {'titel': 'Was trägst du heute?', 'frage': 'Beschreib deine Kleidung heute in zwei Sätzen.', 'beispiel': 'Heute trage ich eine schwarze Hose und einen weißen Pullover.'},
            {'titel': 'Was möchtest du kaufen?', 'frage': 'Was brauchst du gerade? Schreib zwei Sätze.', 'beispiel': 'Ich brauche neue Schuhe. Meine alten sind kaputt.'},
            {'titel': 'Eine Frage im Geschäft', 'frage': 'Du probierst etwas an. Schreib eine Frage an die Verkäuferin.', 'beispiel': 'Haben Sie diese Hose auch in Größe 38?'},
            {'titel': 'Mini-Dialog: Im Bekleidungsgeschäft', 'frage': 'Du kaufst Kleidung. Schreib einen Mini-Dialog: zwei Fragen, zwei Antworten.', 'beispiel': '— Suchen Sie etwas Bestimmtes? — Ja, eine Jacke. — Welche Größe? — Mittel, bitte.'},
        ]
    },
    '2054C': {
        'lesson_code': '2054C',
        'lesson_title': 'Lerncheck im Restaurant',
        'banner_url': 'https://images.pexels.com/photos/733856/pexels-photo-733856.jpeg?auto=compress&cs=tinysrgb&w=800',
        'banner_alt': 'Notizbuch und Stift, bereit zum Schreiben',
        'intro': 'Fünf kleine Schreibaufgaben rund um das Restaurant.',
        'tasks': [
            {'titel': 'Dein Lieblings-Restaurant', 'frage': 'Welches Restaurant magst du? Was isst du dort? Schreib zwei Sätze.', 'beispiel': 'Ich mag „La Trattoria". Dort esse ich oft Pizza und Tiramisu.'},
            {'titel': 'Was bestellst du gern?', 'frage': 'Was bestellst du im Restaurant? Schreib zwei Sätze.', 'beispiel': 'Als Vorspeise nehme ich Salat. Dann Pasta oder Fisch.'},
            {'titel': 'Trinken im Restaurant', 'frage': 'Was trinkst du gern zum Essen? Schreib einen Satz.', 'beispiel': 'Ich trinke gern ein Glas Wein zum Essen.'},
            {'titel': 'Eine Frage an den Kellner', 'frage': 'Du bist im Restaurant. Schreib eine Frage an den Kellner.', 'beispiel': 'Können Sie mir die Speisekarte bringen, bitte?'},
            {'titel': 'Mini-Dialog: Bestellen', 'frage': 'Du bestellst beim Kellner. Schreib einen Mini-Dialog: zwei Fragen, zwei Antworten.', 'beispiel': '— Was wünschen Sie? — Eine Pizza Margherita, bitte. — Möchten Sie etwas trinken? — Ein Wasser, bitte.'},
        ]
    },
    # ===== X-Dateien (Textarbeit) =====
    '1012X': {
        'lesson_code': '1012X',
        'lesson_title': 'Wie schreibt man das?',
        'banner_url': 'https://images.pexels.com/photos/733856/pexels-photo-733856.jpeg?auto=compress&cs=tinysrgb&w=800',
        'banner_alt': 'Notizbuch und Stift, bereit zum Schreiben',
        'intro': 'Fünf kleine Schreibaufgaben rund um Buchstaben, Zahlen und persönliche Daten.',
        'tasks': [
            {'titel': 'Buchstabiere deinen Namen', 'frage': 'Schreib deinen Vornamen und Nachnamen, jeden Buchstaben einzeln, getrennt durch Bindestriche.', 'beispiel': 'M-A-R-I-A   L-O-P-E-Z'},
            {'titel': 'Deine Telefonnummer in Worten', 'frage': 'Schreib deine Telefonnummer in Ziffern UND in Wörtern (mindestens 5 Ziffern).', 'beispiel': 'Meine Nummer: 040-12345 — null vier null eins zwei drei vier fünf.'},
            {'titel': 'Deine Adresse', 'frage': 'Schreib deine Adresse: Straße, Hausnummer, Stadt, Land. Zwei oder drei Sätze.', 'beispiel': 'Ich wohne in der Hauptstraße 17 in München. Das ist in Deutschland.'},
            {'titel': 'Wie alt sind sie?', 'frage': 'Schreib dein Alter und das Alter von zwei Personen aus deiner Familie.', 'beispiel': 'Ich bin 28 Jahre alt. Mein Bruder ist 32 und meine Mutter ist 60.'},
            {'titel': 'Mini-Dialog: Am Telefon buchstabieren', 'frage': 'Du buchstabierst deinen Namen am Telefon. Schreib einen Mini-Dialog: zwei Fragen und zwei Antworten.', 'beispiel': '— Wie heißen Sie? — Mein Name ist Lopez. — Können Sie das buchstabieren? — L-O-P-E-Z.'},
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
        candidates = [c for c in candidates if not c.name.endswith('.bak') and '-uebungen.html' not in c.name]
        if not candidates:
            print(f"FAIL — Datei DE_A1_{code}-*.html nicht gefunden")
            continue
        if len(candidates) > 1:
            print(f"FAIL — Mehrdeutig, gefunden:", [c.name for c in candidates])
            continue
        print(patch_file(candidates[0], cfg))
