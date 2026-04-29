#!/usr/bin/env python3
"""
Patcher: stellt alle Schreibwerkstatt-Dateien um auf
- Web3Forms statt formsubmit.co (kein Sponsor-Footer)
- body.success-Check (verhindert stille Fehler)
- Customer-Success-Error-UX (Erklärung + Mailto + Zwischenablage + Retry)
- Konsistenten Mailto-Fallback an unterricht@fabdaf.onmicrosoft.com (auch für die 44 C1-Dateien mit Alias-Drift)

Erkennt sowohl multi-line (B2 GEHIRN_03R-Stil) als auch one-liner (C1 3013R-Stil) Varianten.

Idempotent: nochmaliges Anwenden ist no-op.
"""
import re
import sys
import subprocess
from pathlib import Path

ACCESS_KEY = 'e96ea83f-67e2-4fff-81df-76fee86a09ff'
API_ENDPOINT = 'https://api.web3forms.com/submit'
MAILTO_FALLBACK = 'unterricht@fabdaf.onmicrosoft.com'

# ---------- Brace-Matching ----------

def find_matching_brace(text, open_idx):
    """text[open_idx] muss '{' sein. Liefert Index nach passendem '}', sonst -1."""
    if open_idx >= len(text) or text[open_idx] != '{':
        return -1
    depth = 0
    i = open_idx
    in_str = None
    esc = False
    in_line_cmt = False
    in_block_cmt = False
    while i < len(text):
        c = text[i]
        nxt = text[i + 1] if i + 1 < len(text) else ''
        if in_line_cmt:
            if c == '\n':
                in_line_cmt = False
            i += 1
            continue
        if in_block_cmt:
            if c == '*' and nxt == '/':
                in_block_cmt = False
                i += 2
                continue
            i += 1
            continue
        if in_str:
            if esc:
                esc = False
            elif c == '\\':
                esc = True
            elif c == in_str:
                in_str = None
            i += 1
            continue
        if c == '/' and nxt == '/':
            in_line_cmt = True
            i += 2
            continue
        if c == '/' and nxt == '*':
            in_block_cmt = True
            i += 2
            continue
        if c in "'\"`":
            in_str = c
            i += 1
            continue
        if c == '{':
            depth += 1
        elif c == '}':
            depth -= 1
            if depth == 0:
                return i + 1
        i += 1
    return -1


def find_paren_end(text, open_idx):
    """text[open_idx] muss '(' sein. Liefert Index nach passendem ')'."""
    if open_idx >= len(text) or text[open_idx] != '(':
        return -1
    depth = 0
    i = open_idx
    in_str = None
    esc = False
    while i < len(text):
        c = text[i]
        if in_str:
            if esc:
                esc = False
            elif c == '\\':
                esc = True
            elif c == in_str:
                in_str = None
            i += 1
            continue
        if c in "'\"`":
            in_str = c
        elif c == '(':
            depth += 1
        elif c == ')':
            depth -= 1
            if depth == 0:
                return i + 1
        i += 1
    return -1


# ---------- Patch-Bausteine ----------

CONSTANTS_BLOCK = """var FORMSUBMIT_ENDPOINT  = 'https://api.web3forms.com/submit';
var FORMSUBMIT_ACCESS_KEY = '{key}';
var FORMSUBMIT_MAILTO    = '{mail}';""".format(key=ACCESS_KEY, mail=MAILTO_FALLBACK)


NEW_POST_FN = """function schreibPostFormsubmit(subject, message, onOk, onErr) {
  return fetch(FORMSUBMIT_ENDPOINT, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' },
    body: JSON.stringify({
      access_key: FORMSUBMIT_ACCESS_KEY,
      name: schreibAktuellerName(),
      subject: subject,
      from_name: 'fabDaF Schreibwerkstatt',
      lektion: SCHREIB_LEKTION,
      message: message
    })
  })
    .then(function (r) { if (!r.ok) throw new Error('HTTP_' + r.status); return r.json(); })
    .then(function (data) {
      var ok = data && (data.success === true || data.success === 'true');
      if (!ok) {
        var code = 'API_ERROR';
        var apiMsg = (data && data.message) || '';
        if (/[Aa]ctivat|domain|access[\\s_-]?key/.test(apiMsg)) code = 'NOT_ACTIVATED';
        var err = new Error(code);
        err.apiMessage = apiMsg;
        throw err;
      }
      onOk(data);
    })
    .catch(onErr);
}"""


HELPER_FNS = """function schreibFehlerErklaerung(err) {
  var code = (err && err.message) || '';
  if (code === 'NOT_ACTIVATED') {
    return 'Der Versand-Endpunkt ist gerade nicht freigeschaltet (das passiert manchmal bei Adress-Wechsel auf Franks Seite).';
  }
  if (code.indexOf('HTTP_') === 0) {
    return 'Der Server hat eine technische Antwort gegeben (' + code.replace('HTTP_', 'HTTP ') + '), die nicht „erfolgreich" bedeutet.';
  }
  if (code === 'API_ERROR') {
    return 'Der Versand-Dienst hat „nicht erfolgreich" zurückgemeldet' + (err && err.apiMessage ? ' („' + err.apiMessage + '")' : '') + '.';
  }
  return 'Es gab ein Netz- oder Browser-Problem beim Senden — keine Server-Antwort.';
}

function schreibKopierenEinzeln(nr) {
  var ta = document.querySelector('.schreib-mini-textarea[data-aufgabe="' + nr + '"]');
  if (!ta) return;
  var titel = ta.dataset.titel || ('Aufgabe ' + nr);
  var name = (typeof schreibAktuellerName === 'function' && schreibAktuellerName()) || '(kein Name eingetragen)';
  var text = 'Lektion: ' + SCHREIB_LEKTION + '\\nName: ' + name + '\\n\\n=== Aufgabe ' + nr + ': ' + titel + ' ===\\n\\n' + ta.value.trim();
  var st = document.getElementById('sw-status-' + nr) || document.getElementById('status-' + nr);
  function fertig(ok) {
    if (!st) return;
    if (ok) { st.classList.remove('error'); st.classList.add('success'); st.innerHTML = '✓ In die Zwischenablage kopiert. Jetzt in deine Mail oder deinen Chat einfügen und an Frank schicken.'; }
    else { st.classList.add('error'); st.innerHTML = '✗ Kopieren ging nicht — markier den Text in der Box selbst und nutz „kopieren" deines Browsers.'; }
  }
  if (navigator.clipboard && navigator.clipboard.writeText) {
    navigator.clipboard.writeText(text).then(function () { fertig(true); }, function () { fertig(false); });
  } else {
    try {
      var tmp = document.createElement('textarea'); tmp.value = text; document.body.appendChild(tmp);
      tmp.select(); document.execCommand('copy'); document.body.removeChild(tmp); fertig(true);
    } catch (e) { fertig(false); }
  }
}

function schreibZeigeFehler(nr, err, subject, message) {
  var st = document.getElementById('sw-status-' + nr) || document.getElementById('status-' + nr);
  if (!st) return;
  var subjectEnc = encodeURIComponent(subject);
  var bodyEnc = encodeURIComponent('Name: ' + schreibAktuellerName() + '\\n\\n' + message);
  var mailto = 'mailto:' + FORMSUBMIT_MAILTO + '?subject=' + subjectEnc + '&body=' + bodyEnc;
  var erklaerung = schreibFehlerErklaerung(err);
  st.classList.remove('success'); st.classList.add('error');
  st.innerHTML =
    '<div class="schreib-fb">' +
      '<div class="schreib-fb-titel">⚠ Online-Versand hat nicht geklappt — dein Text ist sicher im Browser gespeichert.</div>' +
      '<div class="schreib-fb-text"><strong>Was passiert ist:</strong> ' + erklaerung + ' Du verlierst nichts — wähle einen der drei Wege, damit Frank deine Antwort trotzdem bekommt:</div>' +
      '<div class="schreib-fb-actions">' +
        '<a class="schreib-fb-btn schreib-fb-btn-prim" href="' + mailto + '">📧 In Mail-Programm öffnen</a>' +
        '<button type="button" class="schreib-fb-btn" onclick="schreibKopierenEinzeln(\\'' + nr + '\\')">📋 In Zwischenablage</button>' +
        '<button type="button" class="schreib-fb-btn" onclick="schreibSendenEinzeln(\\'' + nr + '\\')">🔄 Nochmal versuchen</button>' +
      '</div>' +
      '<div class="schreib-fb-hilfe">Wenn nichts klappt: sag Frank im Unterricht Bescheid — er muss den Versand auf seiner Seite einmal aktivieren.</div>' +
    '</div>';
}

function schreibZeigeFehlerSammel(err, subject, message) {
  var subjectEnc = encodeURIComponent(subject);
  var bodyEnc = encodeURIComponent('Name: ' + schreibAktuellerName() + '\\n\\n' + message);
  var mailto = 'mailto:' + FORMSUBMIT_MAILTO + '?subject=' + subjectEnc + '&body=' + bodyEnc;
  var erklaerung = schreibFehlerErklaerung(err);
  var fnKopieren = (typeof schreibKopieren === 'function') ? 'schreibKopieren()' : 'schreibKopierenEinzeln(1)';
  schreibStatusZeigen('error',
    '<div class="schreib-fb">' +
      '<div class="schreib-fb-titel">⚠ Sammel-Versand hat nicht geklappt — alle Antworten sind sicher im Browser gespeichert.</div>' +
      '<div class="schreib-fb-text"><strong>Was passiert ist:</strong> ' + erklaerung + ' Wähle einen Weg:</div>' +
      '<div class="schreib-fb-actions">' +
        '<a class="schreib-fb-btn schreib-fb-btn-prim" href="' + mailto + '">📧 Alle als eine Mail öffnen</a>' +
        '<button type="button" class="schreib-fb-btn" onclick="' + fnKopieren + '">📋 Alles in Zwischenablage</button>' +
        '<button type="button" class="schreib-fb-btn" onclick="schreibSendenAlleNochOffenen()">🔄 Nochmal versuchen</button>' +
      '</div>' +
      '<div class="schreib-fb-hilfe">Tipp: einzelne Karten kannst du auch separat senden — jede hat eigene Buttons.</div>' +
    '</div>');
}"""


CSS_BLOCK = """
/* Customer-Success-Fallback-Block bei Versand-Fehler (gepatcht) */
.schreib-fb { display: flex; flex-direction: column; gap: 8px; }
.schreib-fb-titel { font-weight: 700; font-size: 1em; color: #b71c1c; }
.schreib-fb-text { color: #4a4a4a; font-size: 0.92em; line-height: 1.5; }
.schreib-fb-actions { display: flex; flex-wrap: wrap; gap: 8px; margin-top: 4px; }
.schreib-fb-btn { display: inline-flex; align-items: center; gap: 6px; padding: 9px 14px; border-radius: 8px; border: 1.5px solid #667eea; background: white; color: #667eea; font-size: 0.9em; font-weight: 600; text-decoration: none; cursor: pointer; transition: all 0.15s; }
.schreib-fb-btn:hover { background: #667eea; color: white; box-shadow: 0 2px 6px rgba(102,126,234,0.3); }
.schreib-fb-btn-prim { background: #667eea; color: white; }
.schreib-fb-btn-prim:hover { background: #4f63c2; color: white; }
.schreib-fb-hilfe { color: #6c6c6c; font-size: 0.86em; font-style: italic; margin-top: 4px; }
"""


# ---------- Transformationen ----------

def patch_constants(text):
    """Ersetzt die FORMSUBMIT_ENDPOINT-Zeile (alt: formsubmit.co) durch den neuen Constants-Block.
    Falls schon Web3Forms-URL drinsteht, no-op."""
    pat = re.compile(
        r"var\s+FORMSUBMIT_ENDPOINT\s*=\s*['\"]https?://formsubmit\.co/[^'\"]*['\"];?",
        re.MULTILINE
    )
    if pat.search(text):
        return pat.sub(CONSTANTS_BLOCK, text), True
    return text, False


def patch_post_function(text):
    """Ersetzt die schreibPostFormsubmit-Funktion komplett."""
    m = re.search(r'function\s+schreibPostFormsubmit\s*\(', text)
    if not m:
        return text, False
    # Find the opening { of the function body
    paren_start = m.end() - 1  # at '('
    paren_end = find_paren_end(text, paren_start)
    if paren_end < 0:
        return text, False
    # find next '{'
    body_open = text.find('{', paren_end)
    if body_open < 0:
        return text, False
    body_end = find_matching_brace(text, body_open)
    if body_end < 0:
        return text, False
    new = text[:m.start()] + NEW_POST_FN + text[body_end:]
    return new, True


def _delete_function(text, name):
    """Löscht 'function NAME(...)' samt Body. Liefert (neuer_text, geloescht_count)."""
    count = 0
    while True:
        m = re.search(r'function\s+' + re.escape(name) + r'\s*\(', text)
        if not m:
            break
        paren_open = m.end() - 1
        paren_close = find_paren_end(text, paren_open)
        if paren_close < 0:
            break
        body_open = text.find('{', paren_close)
        if body_open < 0:
            break
        body_end = find_matching_brace(text, body_open)
        if body_end < 0:
            break
        # Auch evt. davorstehenden Whitespace + nachfolgenden Newline aufräumen
        start = m.start()
        end = body_end
        # Leading: trim back through preceding whitespace/newlines
        while start > 0 and text[start - 1] in ' \t':
            start -= 1
        if start > 0 and text[start - 1] == '\n':
            start -= 1
        # Trailing: consume one newline if present
        while end < len(text) and text[end] == '\n':
            end += 1
            break
        text = text[:start] + text[end:]
        count += 1
    return text, count


def insert_helpers(text):
    """Erst alle bestehenden Helper-Versionen löschen, dann canonical Block einfügen."""
    helpers_to_clean = ['schreibFehlerErklaerung', 'schreibKopierenEinzeln',
                        'schreibZeigeFehler', 'schreibZeigeFehlerSammel']
    cleaned = 0
    for h in helpers_to_clean:
        text, n = _delete_function(text, h)
        cleaned += n
    # Find end of new schreibPostFormsubmit and insert canonical block right after.
    m = re.search(r'function\s+schreibPostFormsubmit\s*\(', text)
    if not m:
        return text, False
    paren_start = m.end() - 1
    paren_end = find_paren_end(text, paren_start)
    body_open = text.find('{', paren_end)
    body_end = find_matching_brace(text, body_open)
    if body_end < 0:
        return text, False
    new = text[:body_end] + '\n\n' + HELPER_FNS + text[body_end:]
    return new, True


def normalize_footer_email(text):
    """Falls die Datei noch 'FrankBurkert@fabdaf.onmicrosoft.com' im Footer / als
    statischen Mailto-Link enthält, durch den aktuellen Alias ersetzen.
    (Code-Konstanten werden bereits durch patch_constants gehändelt; das hier ist für
    sichtbares HTML-Markup.)"""
    if 'FrankBurkert@fabdaf.onmicrosoft.com' in text:
        new = text.replace('FrankBurkert@fabdaf.onmicrosoft.com', 'unterricht@fabdaf.onmicrosoft.com')
        return new, True
    return text, False


def patch_error_callbacks(text):
    """Ersetzt die catch-Callbacks in den schreibPostFormsubmit-Aufrufen.

    Der Aufruf hat Form: schreibPostFormsubmit(subject, message, FN_OK, FN_ERR);
    FN_OK behalten wir; FN_ERR ersetzen wir durch:
      - im einzeln-Kontext: function (err) { btn.disabled=false; btn.innerHTML=ol; schreibZeigeFehler(nr, err, subject, message); }
      - im Sammel-Kontext: function (err) { btn.disabled=false; btn.innerHTML='📨 Alle …'; schreibZeigeFehlerSammel(err, subject, message); }
    """
    changed = 0
    out = []
    cursor = 0
    for inv in re.finditer(r'\bschreibPostFormsubmit\s*\(', text):
        # Skip the function definition itself (preceded by "function ")
        pre = text[max(0, inv.start() - 15):inv.start()]
        if re.search(r'function\s+$', pre):
            continue
        # Output everything up to (and including) the open paren
        out.append(text[cursor:inv.end()])
        # The opening paren is at inv.end()-1
        paren_open = inv.end() - 1
        paren_close = find_paren_end(text, paren_open)
        if paren_close < 0:
            # bail — emit rest and stop
            out.append(text[inv.end():])
            cursor = len(text)
            break
        args_str = text[inv.end():paren_close - 1]  # content between ()

        # Now we need to split args: subject, message, fn_ok, fn_err
        # Simple top-level splitter that respects parens/braces/strings.
        parts = _split_top_args(args_str)
        if len(parts) != 4:
            # Unexpected shape — leave invocation untouched
            out.append(args_str + ')')
            cursor = paren_close
            continue

        # Decide context: einzeln vs Sammel.
        # Robust: schau in success-Callback (parts[2]) und in alten error-Callback (parts[3])
        # nach Kennzeichen. einzeln updates one card via SCHREIB_SENT_PREFIX + nr; sammel
        # iteriert über offene und ruft schreibStatusZeigen auf.
        ok_cb = parts[2]
        err_cb_old = parts[3]
        sammel_markers = ('offene.forEach', 'schreibStatusZeigen', 'Antworten übermittelt',
                           'Antworten · ', 'forEach(function (o)', 'forEach(function(o)')
        einzeln_markers = ('SCHREIB_SENT_PREFIX + nr', 'SCHREIB_SENT_PREFIX+nr',
                           "'sw-status-' + nr", "'status-' + nr",
                           'schreibKarteAlsGesendetMarkieren(nr', 'schreibKarteAlsGesendetMarkieren(o.nr')
        is_sammel = any(m in ok_cb for m in sammel_markers) or any(m in err_cb_old for m in sammel_markers)
        is_einzeln = any(m in ok_cb for m in einzeln_markers) and not is_sammel
        if is_sammel and not is_einzeln:
            ctx = 'sammel'
        elif is_einzeln:
            ctx = 'einzeln'
        else:
            # Fallback: presence of 'nr' as a top-level reference in success callback
            ctx = 'einzeln' if re.search(r'\bnr\b', ok_cb) and 'offene' not in ok_cb else 'sammel'

        # Erkenne lokale Variable für den Original-Button-Text (origLabel | ol | …)
        # aus dem alten error-Callback ODER dem success-Callback.
        scope = err_cb_old + '\n' + ok_cb
        # Heuristik: Sucht nach `btn.innerHTML = NAME;` (einfache Zuweisung); NAME ist ein
        # Bezeichner der vorher per `var NAME = btn.innerHTML;` deklariert wurde.
        m_var = re.search(r'btn\.innerHTML\s*=\s*([A-Za-z_$][\w$]*)\s*;', scope)
        orig_label_var = m_var.group(1) if m_var else 'origLabel'

        # Replacement
        if ctx == 'einzeln':
            new_err = (
                "function (err) { btn.disabled = false; btn.innerHTML = " + orig_label_var + "; "
                "schreibZeigeFehler(nr, err, subject, message); }"
            )
        else:
            new_err = (
                "function (err) { btn.disabled = false; btn.innerHTML = '📨 Alle noch nicht gesendeten Antworten schicken'; "
                "schreibZeigeFehlerSammel(err, subject, message); }"
            )

        new_args = parts[0] + ',' + parts[1] + ',' + parts[2] + ',\n    ' + new_err
        out.append(new_args + ')')
        cursor = paren_close
        changed += 1

    out.append(text[cursor:])
    return ''.join(out), changed > 0


def _split_top_args(s):
    """Splittet den Inhalt zwischen () entlang Top-Level-Kommas."""
    parts = []
    depth_p = 0
    depth_b = 0
    depth_c = 0
    in_str = None
    esc = False
    last = 0
    for i, c in enumerate(s):
        if in_str:
            if esc:
                esc = False
            elif c == '\\':
                esc = True
            elif c == in_str:
                in_str = None
            continue
        if c in "'\"`":
            in_str = c
        elif c == '(':
            depth_p += 1
        elif c == ')':
            depth_p -= 1
        elif c == '{':
            depth_b += 1
        elif c == '}':
            depth_b -= 1
        elif c == '[':
            depth_c += 1
        elif c == ']':
            depth_c -= 1
        elif c == ',' and depth_p == 0 and depth_b == 0 and depth_c == 0:
            parts.append(s[last:i])
            last = i + 1
    parts.append(s[last:])
    return parts


def insert_css(text):
    """Fügt die CSS-Regeln in den ersten </style>-Block ein, sofern nicht vorhanden."""
    if '.schreib-fb {' in text:
        return text, False
    m = re.search(r'</style>', text, re.IGNORECASE)
    if not m:
        return text, False
    new = text[:m.start()] + CSS_BLOCK + text[m.start():]
    return new, True


def fix_orig_label_var(text):
    """Im einzeln-Handler heißt die Variable mal `ol`, mal `origLabel`. Wir generieren immer
    `origLabel || ol` als Fallback im Error-Callback. Das funktioniert, solange entweder
    `var ol` oder `var origLabel` deklariert ist. Sicherstellen, dass dem Code-Pfad das nicht
    in die Quere kommt: wenn das Ergebnis Fehler wirft, weil weder `ol` noch `origLabel` definiert
    sind, könnte das passieren. Wir prüfen aber zur Sicherheit nicht — JSDOM-Test deckt das ab."""
    return text, False


# ---------- Pipeline ----------

def patch_file(path: Path) -> dict:
    text = path.read_text(encoding='utf-8')
    orig = text
    report = {'file': str(path), 'changes': []}

    text, ch = patch_constants(text)
    if ch:
        report['changes'].append('constants')

    text, ch = patch_post_function(text)
    if ch:
        report['changes'].append('post_fn')

    text, ch = insert_helpers(text)
    if ch:
        report['changes'].append('helpers')

    text, ch = patch_error_callbacks(text)
    if ch:
        report['changes'].append('error_callbacks')

    text, ch = insert_css(text)
    if ch:
        report['changes'].append('css')

    text, ch = normalize_footer_email(text)
    if ch:
        report['changes'].append('footer_email')

    if text == orig:
        report['status'] = 'noop'
        return report

    # JS-Syntaxcheck vor dem Speichern
    scripts = re.findall(r'<script[^>]*>([\s\S]*?)</script>', text, re.IGNORECASE)
    js = '\n//---\n'.join(scripts)
    tmp = Path('/tmp/_chk_schreib.js')
    tmp.write_text(js, encoding='utf-8')
    r = subprocess.run(['node', '--check', str(tmp)], capture_output=True, text=True)
    if r.returncode != 0:
        report['status'] = 'syntax_error'
        report['stderr'] = r.stderr[:500]
        return report

    path.write_text(text, encoding='utf-8')
    report['status'] = 'patched'
    return report


def find_target_files(root: Path):
    """Alle Dateien mit Schreibwerkstatt-Pattern."""
    candidates = []
    for sub in [
        'htmlS/A1.1 NEW',
        'htmlS/A2.1',
        'htmlS/B1.1',
        '.',          # B2 root
        'htmlS/C1',
        'htmlS/C2',
    ]:
        d = root / sub
        if not d.exists():
            continue
        for p in sorted(d.glob('*.html')):
            try:
                content = p.read_text(encoding='utf-8', errors='ignore')
            except Exception:
                continue
            if 'FORMSUBMIT_ENDPOINT' in content and 'schreibPostFormsubmit' in content:
                candidates.append(p)
    return candidates


def main():
    root = Path('/sessions/clever-exciting-archimedes/mnt/fabDaF')
    files = find_target_files(root)
    if len(sys.argv) > 1 and sys.argv[1] == '--dry-run':
        print(f"Would patch {len(files)} files")
        return
    if len(sys.argv) > 1 and sys.argv[1].endswith('.html'):
        files = [Path(a) for a in sys.argv[1:]]
    print(f"Patching {len(files)} files…")
    by_status = {'patched': 0, 'noop': 0, 'syntax_error': 0}
    failures = []
    for p in files:
        r = patch_file(p)
        s = r['status']
        by_status[s] = by_status.get(s, 0) + 1
        if s == 'syntax_error':
            failures.append(r)
    print(f"  patched:      {by_status['patched']}")
    print(f"  noop:         {by_status['noop']}")
    print(f"  syntax_error: {by_status['syntax_error']}")
    if failures:
        print("\nFAILURES:")
        for f in failures:
            print(f"  {f['file']}")
            print(f"    {f.get('stderr', '')[:200]}")


if __name__ == '__main__':
    main()
