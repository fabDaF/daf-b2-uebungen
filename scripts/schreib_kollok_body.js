
function schreibKollCheck(nr) {
  var ta = document.querySelector('.schreib-mini-textarea[data-aufgabe="' + nr + '"]');
  if (!ta) return { ok: 0, n: 0, list: [] };
  var txt = ta.value;
  var chips = document.querySelectorAll('.koll-chip[id^="kr-' + nr + '-"]');
  var ok = 0, list = [];
  chips.forEach(function (chip) {
    var key = chip.dataset.koll, def = KOLL_RADAR[key], hit = false;
    if (def) {
      var nRe = new RegExp('(^|[^a-zäöüß])' + def.n, 'i');
      var vRe = new RegExp(def.v, 'i');
      hit = nRe.test(txt) && vRe.test(txt);
    }
    chip.classList.toggle('ok', hit);
    if (hit) ok++;
    list.push((hit ? '✓ ' : '✗ ') + key);
  });
  var kc = document.querySelector('.kc-' + nr);
  if (kc) kc.textContent = ok + '/' + chips.length;
  return { ok: ok, n: chips.length, list: list };
}

function initSchreibwerkstatt() {
  var nameInp = document.getElementById('sw-name');
  if (nameInp) {
    var savedName = lsGet(SCHREIB_NAME_KEY);
    if (savedName) nameInp.value = savedName;
    nameInp.addEventListener('input', function () { lsSet(SCHREIB_NAME_KEY, nameInp.value); });
  }
  document.querySelectorAll('.schreib-mini-textarea').forEach(function (ta) {
    var nr = ta.dataset.aufgabe;
    var saved = lsGet(SCHREIB_KEY_PREFIX + nr);
    if (saved) ta.value = saved;
    schreibUpdateCount(ta);
    schreibKollCheck(nr);
    var sentInfo = lsGet(SCHREIB_SENT_PREFIX + nr);
    if (sentInfo) schreibKarteAlsGesendetMarkieren(nr, sentInfo, true);
    ta.addEventListener('input', function () {
      schreibUpdateCount(ta);
      schreibKollCheck(nr);
      lsSet(SCHREIB_KEY_PREFIX + nr, ta.value);
      var btn = document.getElementById('sw-send-' + nr);
      if (btn && btn.classList.contains('gesendet')) { btn.classList.remove('gesendet'); btn.innerHTML = '📨 Erneut senden'; }
      var st = document.getElementById('sw-status-' + nr);
      if (st && st.classList.contains('error')) { st.classList.remove('error'); st.textContent = ''; }
    });
  });
}

function schreibUpdateCount(ta) {
  var nr = ta.dataset.aufgabe;
  var text = ta.value.trim();
  var words = text ? text.split(/\s+/).filter(function (w) { return w.length > 0; }).length : 0;
  var wc = document.querySelector('.wc-' + nr);
  if (wc) wc.textContent = words;
}

function schreibKarteAlsGesendetMarkieren(nr, info, beimLaden) {
  var ta = document.querySelector('.schreib-mini-textarea[data-aufgabe="' + nr + '"]');
  var karte = ta && ta.closest('.schreib-aufgabe-karte');
  if (karte) karte.classList.add('gesendet');
  var btn = document.getElementById('sw-send-' + nr);
  if (btn) { btn.classList.add('gesendet'); btn.innerHTML = beimLaden ? '✓ schon gesendet · erneut senden' : '✓ gesendet · erneut senden'; }
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
  if (schreibAktuellerName().length < 2) {
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

function schreibToFormData(obj) {
  var fd = new FormData();
  Object.keys(obj).forEach(function (k) { fd.append(k, obj[k]); });
  return fd;
}

function schreibPostFormsubmit(subject, message, onOk, onErr) {
  return fetch(FORMSUBMIT_ENDPOINT, {
    method: 'POST',
    body: schreibToFormData({
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
        if (/[Aa]ctivat|domain|access[\s_-]?key/.test(apiMsg)) code = 'NOT_ACTIVATED';
        var err = new Error(code);
        err.apiMessage = apiMsg;
        throw err;
      }
      onOk(data);
    })
    .catch(onErr);
}

function schreibFehlerErklaerung(err) {
  var code = (err && err.message) || '';
  if (code === 'NOT_ACTIVATED') return 'Der Versand-Endpunkt ist gerade nicht freigeschaltet (das passiert manchmal bei Adress-Wechsel auf Franks Seite).';
  if (code.indexOf('HTTP_') === 0) return 'Der Server hat eine technische Antwort gegeben (' + code.replace('HTTP_', 'HTTP ') + '), die nicht „erfolgreich“ bedeutet.';
  if (code === 'API_ERROR') return 'Der Versand-Dienst hat „nicht erfolgreich“ zurückgemeldet' + (err && err.apiMessage ? ' („' + err.apiMessage + '“)' : '') + '.';
  return 'Es gab ein Netz- oder Browser-Problem beim Senden – keine Server-Antwort.';
}

function schreibBlock(nr, text) {
  var ta = document.querySelector('.schreib-mini-textarea[data-aufgabe="' + nr + '"]');
  var titel = (ta && ta.dataset.titel) || ('Aufgabe ' + nr);
  var k = schreibKollCheck(nr);
  return '=== Aufgabe ' + nr + ': ' + titel + ' ===\nKollokationen (' + k.ok + '/' + k.n + '): ' + k.list.join(' · ') + '\n\n' + text;
}

function schreibKopierenEinzeln(nr) {
  var ta = document.querySelector('.schreib-mini-textarea[data-aufgabe="' + nr + '"]');
  if (!ta) return;
  var name = schreibAktuellerName() || '(kein Name eingetragen)';
  var text = 'Lektion: ' + SCHREIB_LEKTION + '\nName: ' + name + '\n\n' + schreibBlock(nr, ta.value.trim());
  var st = document.getElementById('sw-status-' + nr);
  function fertig(ok) {
    if (!st) return;
    if (ok) { st.classList.remove('error'); st.innerHTML = '✓ In die Zwischenablage kopiert. Jetzt in deine Mail oder deinen Chat einfügen und an Frank schicken.'; }
    else { st.classList.add('error'); st.innerHTML = '✗ Kopieren ging nicht – markier den Text in der Box selbst und nutz „Kopieren“ deines Browsers.'; }
  }
  if (navigator.clipboard && navigator.clipboard.writeText) {
    navigator.clipboard.writeText(text).then(function () { fertig(true); }, function () { fertig(false); });
  } else {
    try { var tmp = document.createElement('textarea'); tmp.value = text; document.body.appendChild(tmp); tmp.select(); document.execCommand('copy'); document.body.removeChild(tmp); fertig(true); }
    catch (e) { fertig(false); }
  }
}

function schreibZeigeFehler(nr, err, subject, message) {
  var st = document.getElementById('sw-status-' + nr);
  if (!st) return;
  var mailto = 'mailto:' + FORMSUBMIT_MAILTO + '?subject=' + encodeURIComponent(subject) + '&body=' + encodeURIComponent('Name: ' + schreibAktuellerName() + '\n\n' + message);
  st.classList.add('error');
  st.innerHTML =
    '<div class="schreib-fb">' +
      '<div class="schreib-fb-titel">⚠ Online-Versand hat nicht geklappt — dein Text ist sicher im Browser gespeichert.</div>' +
      '<div class="schreib-fb-text"><strong>Was passiert ist:</strong> ' + schreibFehlerErklaerung(err) + ' Du verlierst nichts – wähle einen der drei Wege, damit Frank deine Antwort trotzdem bekommt:</div>' +
      '<div class="schreib-fb-actions">' +
        '<a class="schreib-fb-btn schreib-fb-btn-prim" href="' + mailto + '">📧 In Mail-Programm öffnen</a>' +
        '<button type="button" class="schreib-fb-btn" onclick="schreibKopierenEinzeln(\'' + nr + '\')">📋 In Zwischenablage</button>' +
        '<button type="button" class="schreib-fb-btn" onclick="schreibSendenEinzeln(\'' + nr + '\')">🔄 Nochmal versuchen</button>' +
      '</div>' +
      '<div class="schreib-fb-hilfe">Wenn nichts klappt: sag Frank im Unterricht Bescheid — er muss den Versand auf seiner Seite einmal aktivieren.</div>' +
    '</div>';
}

function schreibZeigeFehlerSammel(err, subject, message) {
  var mailto = 'mailto:' + FORMSUBMIT_MAILTO + '?subject=' + encodeURIComponent(subject) + '&body=' + encodeURIComponent('Name: ' + schreibAktuellerName() + '\n\n' + message);
  schreibStatusZeigen('error',
    '<div class="schreib-fb">' +
      '<div class="schreib-fb-titel">⚠ Sammel-Versand hat nicht geklappt — alle Antworten sind sicher im Browser gespeichert.</div>' +
      '<div class="schreib-fb-text"><strong>Was passiert ist:</strong> ' + schreibFehlerErklaerung(err) + ' Wähle einen Weg:</div>' +
      '<div class="schreib-fb-actions">' +
        '<a class="schreib-fb-btn schreib-fb-btn-prim" href="' + mailto + '">📧 Alle als eine Mail öffnen</a>' +
        '<button type="button" class="schreib-fb-btn" onclick="schreibKopieren()">📋 Alles in Zwischenablage</button>' +
        '<button type="button" class="schreib-fb-btn" onclick="schreibSendenAlleNochOffenen()">🔄 Nochmal versuchen</button>' +
      '</div>' +
      '<div class="schreib-fb-hilfe">Wenn nichts klappt: sag Frank im Unterricht Bescheid — er muss den Versand auf seiner Seite einmal aktivieren.</div>' +
    '</div>');
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
    if (st) { st.classList.add('error'); st.textContent = 'noch zu kurz – schreib bitte etwas mehr'; }
    return;
  }
  var titel = ta.dataset.titel || ('Aufgabe ' + nr);
  var subject = SCHREIB_CODE + ' · Aufgabe ' + nr + ' · ' + titel + ' · ' + schreibAktuellerName();
  var message = schreibBlock(nr, text);
  btn.disabled = true;
  var origLabel = btn.innerHTML;
  btn.innerHTML = '⏳ Wird gesendet …';
  schreibPostFormsubmit(subject, message,
    function () {
      btn.disabled = false;
      var jetzt = new Date();
      var info = 'gesendet um ' + String(jetzt.getHours()).padStart(2, '0') + ':' + String(jetzt.getMinutes()).padStart(2, '0');
      lsSet(SCHREIB_SENT_PREFIX + nr, info);
      schreibKarteAlsGesendetMarkieren(nr, info, false);
    },
    function (err) { btn.disabled = false; btn.innerHTML = origLabel; schreibZeigeFehler(nr, err, subject, message); });
}

function schreibSendenAlleNochOffenen() {
  var btn = document.getElementById('sw-btn-all');
  if (!schreibNamePflicht()) { schreibStatusZeigen('error', '✗ Bitte zuerst deinen Namen oben eintragen.'); return; }
  var offene = [];
  document.querySelectorAll('.schreib-mini-textarea').forEach(function (ta) {
    var nr = ta.dataset.aufgabe, text = ta.value.trim();
    if (text.length >= SCHREIB_MIN_CHARS && !lsGet(SCHREIB_SENT_PREFIX + nr)) offene.push({ nr: nr, text: text });
  });
  if (offene.length === 0) {
    schreibStatusZeigen('info', 'ℹ Es gibt nichts Neues zu senden — alle Antworten sind entweder leer/sehr kurz oder bereits gesendet.');
    return;
  }
  var subject = SCHREIB_CODE + ' · ' + offene.length + ' Antworten · ' + schreibAktuellerName();
  var message = offene.map(function (o) { return schreibBlock(o.nr, o.text); }).join('\n\n');
  btn.disabled = true;
  btn.innerHTML = '⏳ Wird gesendet …';
  schreibStatusZeigen('info', '⏳ ' + offene.length + ' Antworten werden übermittelt …');
  schreibPostFormsubmit(subject, message,
    function () {
      btn.disabled = false;
      btn.innerHTML = '📨 Alle noch nicht gesendeten Antworten schicken';
      var jetzt = new Date();
      var info = 'gesendet um ' + String(jetzt.getHours()).padStart(2, '0') + ':' + String(jetzt.getMinutes()).padStart(2, '0');
      offene.forEach(function (o) { lsSet(SCHREIB_SENT_PREFIX + o.nr, info); schreibKarteAlsGesendetMarkieren(o.nr, info, false); });
      schreibStatusZeigen('success', '✓ <strong>' + offene.length + ' Antworten übermittelt.</strong> Frank meldet sich.');
    },
    function (err) { btn.disabled = false; btn.innerHTML = '📨 Alle noch nicht gesendeten Antworten schicken'; schreibZeigeFehlerSammel(err, subject, message); });
}

function schreibKopieren() {
  var teile = ['Lektion: ' + SCHREIB_LEKTION, 'Name: ' + (schreibAktuellerName() || '(kein Name)'), ''];
  document.querySelectorAll('.schreib-mini-textarea').forEach(function (ta) {
    var text = ta.value.trim();
    if (text.length >= SCHREIB_MIN_CHARS) { teile.push(schreibBlock(ta.dataset.aufgabe, text)); teile.push(''); }
  });
  if (teile.length <= 3) { schreibStatusZeigen('info', 'ℹ Noch nichts zum Kopieren — schreib mindestens eine Antwort.'); return; }
  var alles = teile.join('\n');
  if (navigator.clipboard && navigator.clipboard.writeText) {
    navigator.clipboard.writeText(alles).then(
      function () { schreibStatusZeigen('success', '✓ In Zwischenablage kopiert. Du kannst es jetzt in deine Mail einfügen.'); },
      function () { schreibStatusZeigen('error', '✗ Kopieren fehlgeschlagen. Bitte den Text manuell markieren.'); });
  } else schreibStatusZeigen('error', '✗ Dein Browser unterstützt das automatische Kopieren nicht.');
}

function schreibLeeren() {
  if (!confirm('Wirklich ALLE Antworten zurücksetzen? Auch die schon gesendeten Markierungen werden entfernt.')) return;
  document.querySelectorAll('.schreib-mini-textarea').forEach(function (ta) {
    var nr = ta.dataset.aufgabe;
    ta.value = '';
    lsDel(SCHREIB_KEY_PREFIX + nr); lsDel(SCHREIB_SENT_PREFIX + nr);
    schreibUpdateCount(ta); schreibKollCheck(nr);
    var karte = ta.closest('.schreib-aufgabe-karte');
    if (karte) karte.classList.remove('gesendet');
    var btn = document.getElementById('sw-send-' + nr);
    if (btn) { btn.classList.remove('gesendet'); btn.disabled = false; btn.innerHTML = '📨 An Frank senden'; }
    var st = document.getElementById('sw-status-' + nr);
    if (st) { st.classList.remove('error'); st.textContent = ''; }
  });
  schreibStatusZeigen('info', 'ℹ Alle Antworten wurden zurückgesetzt.');
}

if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', initSchreibwerkstatt);
else initSchreibwerkstatt();
</script>
