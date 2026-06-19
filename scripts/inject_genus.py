#!/usr/bin/env python3
"""
inject_genus.py — fügt einen Genus-Tab in eine DaF-HTML-Lektion ein.

Mechanik (Nav-Button, CSS, Section, JS) wird generationsrobust eingebaut;
die lektionsspezifischen Wörter kommen aus einer JSON-Datei.

  python3 scripts/inject_genus.py DATEI.html woerter.json

woerter.json: [{"word":"Apfel","cat":"der"}, ... ]  (>=20, cat in der/die/das/pl)

SICHER: bricht ab (Exit 2), wenn das erwartete Layout nicht erkannt wird
(letzter Tab ist nicht Wortschatz, kein showSection, schon Genus-Tab da).
Dann ist Handarbeit nötig — es wird NICHTS geschrieben.

Idempotent: vorhandener echter Genus-Tab -> Skip (Exit 0).
"""
import re, sys, json, os

BANNER = "data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAxMDAwIDIyMCIgcm9sZT0iaW1nIiBhcmlhLWxhYmVsPSJHZW51cyDigJQgZGVyLCBkaWUsIGRhcyI+CiAgPGRlZnM+CiAgICA8bGluZWFyR3JhZGllbnQgaWQ9ImJnIiB4MT0iMCIgeTE9IjAiIHgyPSIxIiB5Mj0iMSI+CiAgICAgIDxzdG9wIG9mZnNldD0iMCIgc3RvcC1jb2xvcj0iIzVkNmZjMiIvPgogICAgICA8c3RvcCBvZmZzZXQ9IjEiIHN0b3AtY29sb3I9IiM2YTRhOTIiLz4KICAgIDwvbGluZWFyR3JhZGllbnQ+CiAgPC9kZWZzPgoKICA8cmVjdCB3aWR0aD0iMTAwMCIgaGVpZ2h0PSIyMjAiIGZpbGw9InVybCgjYmcpIi8+CgogIDwhLS0gZGV6ZW50ZSBIYWlybGluZS1SYWhtdW5nIC0tPgogIDxyZWN0IHg9IjI0IiB5PSIyNCIgd2lkdGg9Ijk1MiIgaGVpZ2h0PSIxNzIiIHJ4PSI2IiBmaWxsPSJub25lIiBzdHJva2U9IiNmZmZmZmYiIHN0cm9rZS1vcGFjaXR5PSIwLjE4IiBzdHJva2Utd2lkdGg9IjEiLz4KCiAgPCEtLSBLaWNrZXI6IGtsZWluZSwgZ2VzcGVycnRlIFZlcnNhbGllbiAtLT4KICA8dGV4dCB4PSI1MDAiIHk9IjcyIiB0ZXh0LWFuY2hvcj0ibWlkZGxlIiBmb250LWZhbWlseT0iJ1NlZ29lIFVJJywgc3lzdGVtLXVpLCBzYW5zLXNlcmlmIgogICAgICAgIGZvbnQtc2l6ZT0iMTUiIGZvbnQtd2VpZ2h0PSI2MDAiIGxldHRlci1zcGFjaW5nPSI3IiBmaWxsPSIjZmZmZmZmIiBmaWxsLW9wYWNpdHk9IjAuNzgiPkdFTlVTJiMxNjA7JiMxNjA7JiMxODM7JiMxNjA7JiMxNjA7QVJUSUtFTCBCRVNUSU1NRU48L3RleHQ+CgogIDwhLS0gSGF1cHR6ZWlsZTogcnVoaWdlIFNlcmlmIC0tPgogIDx0ZXh0IHg9IjMyMCIgeT0iMTQ4IiB0ZXh0LWFuY2hvcj0ibWlkZGxlIiBmb250LWZhbWlseT0iR2VvcmdpYSwgJ1RpbWVzIE5ldyBSb21hbicsIHNlcmlmIiBmb250LXNpemU9IjY2IiBmaWxsPSIjZmZmZmZmIj5kZXI8L3RleHQ+CiAgPHRleHQgeD0iNTAwIiB5PSIxNDgiIHRleHQtYW5jaG9yPSJtaWRkbGUiIGZvbnQtZmFtaWx5PSJHZW9yZ2lhLCAnVGltZXMgTmV3IFJvbWFuJywgc2VyaWYiIGZvbnQtc2l6ZT0iNjYiIGZpbGw9IiNmZmZmZmYiPmRpZTwvdGV4dD4KICA8dGV4dCB4PSI2ODAiIHk9IjE0OCIgdGV4dC1hbmNob3I9Im1pZGRsZSIgZm9udC1mYW1pbHk9Ikdlb3JnaWEsICdUaW1lcyBOZXcgUm9tYW4nLCBzZXJpZiIgZm9udC1zaXplPSI2NiIgZmlsbD0iI2ZmZmZmZiI+ZGFzPC90ZXh0PgoKICA8IS0tIGRlemVudGUgRmFyYmFremVudGUgdW50ZXIgamVkZW0gQXJ0aWtlbCAtLT4KICA8cmVjdCB4PSIyODkiIHk9IjE2NiIgd2lkdGg9IjYyIiBoZWlnaHQ9IjMiIHJ4PSIxLjUiIGZpbGw9IiM3ZWEyZTYiLz4KICA8cmVjdCB4PSI0NjkiIHk9IjE2NiIgd2lkdGg9IjYyIiBoZWlnaHQ9IjMiIHJ4PSIxLjUiIGZpbGw9IiNkOThjYWUiLz4KICA8cmVjdCB4PSI2NDkiIHk9IjE2NiIgd2lkdGg9IjYyIiBoZWlnaHQ9IjMiIHJ4PSIxLjUiIGZpbGw9IiM4NmNiYWIiLz4KPC9zdmc+Cg=="

CSS = """/* ===== GENUS-TAB ===== */
.genus-pool { display:flex; flex-wrap:wrap; gap:10px; padding:16px; background:#f0f0f8; border:1px dashed #bbb; border-radius:10px; min-height:60px; margin-bottom:18px; }
.genus-chip { background:#fff; border:2px solid #667eea; color:#333; padding:8px 14px; border-radius:14px; font-weight:600; font-size:0.95em; cursor:grab; user-select:none; }
.genus-chip.dragging { opacity:0.5; }
.genus-chip.selected { outline:3px solid #f39c12; }
.genus-chip.correct { border-color:#2e7d32; background:#e8f5e9; color:#1b5e20; }
.genus-chip.wrong { border-color:#c62828; background:#ffebee; color:#b71c1c; }
.genus-kategorien { display:grid; grid-template-columns:repeat(4,1fr); gap:12px; }
.genus-kat { background:#fafaff; border-radius:10px; padding:10px; border-top:4px solid #999; }
.genus-kat.kat-der { border-top-color:#1565c0; }
.genus-kat.kat-die { border-top-color:#ad1457; }
.genus-kat.kat-das { border-top-color:#1b5e20; }
.genus-kat.kat-pl  { border-top-color:#5e35b1; }
.kat-title { text-align:center; font-weight:700; margin-bottom:8px; font-size:1.05em; }
.kat-der .kat-title { color:#1565c0; } .kat-die .kat-title { color:#ad1457; } .kat-das .kat-title { color:#1b5e20; } .kat-pl .kat-title { color:#5e35b1; }
.genus-drop { min-height:90px; background:#fff; border:2px dashed #ccc; border-radius:8px; padding:8px; display:flex; flex-direction:column; gap:6px; }
.genus-drop.dragover { border-color:#667eea; background:#eef1ff; }
@media (max-width:600px){ .genus-kategorien { grid-template-columns:repeat(2,1fr); } }
"""

def genus_cats(text):
    m = re.search(r'GENUS_DATA\s*=\s*\[', text)
    if not m: return set()
    i = m.end()-1; d=0
    for j in range(i, len(text)):
        if text[j]=='[': d+=1
        elif text[j]==']':
            d-=1
            if d==0: break
    body=text[i+1:j]
    return {c.lower() for c in re.findall(r"cat\s*:\s*['\"]([^'\"]+)['\"]", body)}

def section_html(words, has_helpbox, has_controlbar, timer_idx):
    box_cls = "help-box" if has_helpbox else "hilfe-box"
    helpbox = ('<div class="%s"><strong>Genus üben:</strong> Ziehe jedes Wort in die richtige Kategorie — '
               '<span style="color:#1565c0;font-weight:700;">der</span>, '
               '<span style="color:#ad1457;font-weight:700;">die</span>, '
               '<span style="color:#1b5e20;font-weight:700;">das</span> oder '
               '<span style="color:#5e35b1;font-weight:700;">Plural</span>. Du bekommst sofort Feedback.</div>') % box_cls
    kats = (
      '<div class="genus-kategorien">'
      '<div class="genus-kat kat-der"><div class="kat-title">der</div><div class="genus-drop" id="drop-der" data-cat="der"></div></div>'
      '<div class="genus-kat kat-die"><div class="kat-title">die</div><div class="genus-drop" id="drop-die" data-cat="die"></div></div>'
      '<div class="genus-kat kat-das"><div class="kat-title">das</div><div class="genus-drop" id="drop-das" data-cat="das"></div></div>'
      '<div class="genus-kat kat-pl"><div class="kat-title">Plural</div><div class="genus-drop" id="drop-pl" data-cat="pl"></div></div>'
      '</div>')
    ti = str(timer_idx)
    controls = (
      '<div class="control-bar"><div class="btn-row">'
      '<button class="btn btn-show" onclick="showGenusLoesung()">Lösungen</button>'
      '<button class="btn btn-reset" onclick="resetGenus()">Neu starten</button></div>'
      '<div class="timer-display"><span class="current-time">⏱ <span id="timer-'+ti+'">00:00</span></span>'
      '<span class="best-time">🏆 <span id="best-'+ti+'">--:--</span></span></div></div>'
    ) if has_controlbar else (
      '<div class="btn-row">'
      '<button class="btn btn-show" onclick="showGenusLoesung()">Lösungen</button>'
      '<button class="btn btn-reset" onclick="resetGenus()">Neu starten</button></div>'
      '<div class="timer-display"><span class="current-time">⏱ <span id="timer-'+ti+'">00:00</span></span>'
      '<span class="best-time">🏆 Best: <span id="best-'+ti+'">--:--</span></span></div>'
    )
    return ('\n    <!-- ===== TAB: GENUS ===== -->\n'
            '    <div class="section" id="sec-genus">\n'
            '        <img class="tab-banner" src="'+BANNER+'" alt="Genus üben — der, die, das">\n'
            '        <h2>🏷️ Genus</h2>\n'
            '        '+helpbox+'\n'
            '        <div class="genus-pool" id="genusPool"></div>\n'
            '        '+kats+'\n'
            '        <div id="genusFeedback" style="margin-top:14px;font-weight:600;"></div>\n'
            '        '+controls+'\n'
            '    </div>\n')

def js_block(words, timer_idx):
    data = ",\n  ".join('{ word: %s, cat: "%s" }' % (json.dumps(w["word"], ensure_ascii=False), w["cat"]) for w in words)
    ti = str(timer_idx)
    return '''
<script>
/* ========== TAB: GENUS (injiziert) ========== */
var GENUS_DATA = [
  %s
];
var GENUS_TIMER = %s;
var draggedGenus = null, selectedGenus = null;
function genusTimerStart(){ try{ if(typeof timerAutoStart==='function') timerAutoStart(GENUS_TIMER); else if(typeof startTimer==='function') startTimer(GENUS_TIMER); }catch(e){} }
function genusTimerStop(){ try{ if(typeof stopTimer==='function') stopTimer(GENUS_TIMER); }catch(e){} }
function genusTimerReset(){ try{ if(typeof resetTimer==='function') resetTimer(GENUS_TIMER); }catch(e){} }
function shuffleGenus(a){ a=a.slice(); for(var i=a.length-1;i>0;i--){ var j=Math.floor(Math.random()*(i+1)); var t=a[i]; a[i]=a[j]; a[j]=t; } return a; }
function createGenusChip(d){
  var chip=document.createElement('div');
  chip.className='genus-chip'; chip.draggable=true; chip.dataset.cat=d.cat; chip.textContent=d.word;
  chip.addEventListener('dragstart',function(e){ genusTimerStart(); draggedGenus=chip; chip.classList.add('dragging'); e.dataTransfer.setData('text/plain',''); });
  chip.addEventListener('dragend',function(){ chip.classList.remove('dragging'); });
  chip.addEventListener('click',function(){
    if(selectedGenus===chip){ chip.classList.remove('selected'); selectedGenus=null; return; }
    if(selectedGenus) selectedGenus.classList.remove('selected');
    selectedGenus=chip; chip.classList.add('selected'); genusTimerStart();
  });
  return chip;
}
function initGenus(){
  var pool=document.getElementById('genusPool'); if(!pool) return;
  pool.innerHTML='';
  ['der','die','das','pl'].forEach(function(c){ var z=document.getElementById('drop-'+c); if(z) z.innerHTML=''; });
  var fb=document.getElementById('genusFeedback'); if(fb) fb.textContent='';
  shuffleGenus(GENUS_DATA).forEach(function(d){ pool.appendChild(createGenusChip(d)); });
  document.querySelectorAll('#sec-genus .genus-drop').forEach(function(zone){
    zone.addEventListener('dragover',function(e){ e.preventDefault(); zone.classList.add('dragover'); });
    zone.addEventListener('dragleave',function(){ zone.classList.remove('dragover'); });
    zone.addEventListener('drop',function(e){ e.preventDefault(); zone.classList.remove('dragover'); if(!draggedGenus) return; zone.appendChild(draggedGenus); checkGenusChip(draggedGenus, zone.dataset.cat); draggedGenus=null; updateGenusFeedback(); });
    zone.addEventListener('click',function(){ if(!selectedGenus) return; zone.appendChild(selectedGenus); checkGenusChip(selectedGenus, zone.dataset.cat); selectedGenus.classList.remove('selected'); selectedGenus=null; updateGenusFeedback(); });
  });
  pool.addEventListener('dragover',function(e){ e.preventDefault(); });
  pool.addEventListener('drop',function(e){ e.preventDefault(); if(draggedGenus){ pool.appendChild(draggedGenus); draggedGenus.classList.remove('correct','wrong'); draggedGenus=null; updateGenusFeedback(); } });
}
function checkGenusChip(chip,cat){
  var ok=chip.dataset.cat===cat;
  chip.classList.toggle('correct',ok); chip.classList.toggle('wrong',!ok);
  if(!ok){ setTimeout(function(){ chip.classList.remove('wrong'); document.getElementById('genusPool').appendChild(chip); updateGenusFeedback(); },900); }
}
function updateGenusFeedback(){
  var platziert=document.querySelectorAll('#sec-genus .genus-drop .genus-chip').length;
  var richtig=document.querySelectorAll('#sec-genus .genus-drop .genus-chip.correct').length;
  var fb=document.getElementById('genusFeedback'); if(!fb) return;
  if(platziert===0){ fb.textContent=''; return; }
  fb.textContent=richtig+' von '+GENUS_DATA.length+' richtig zugeordnet.';
  fb.style.color=(richtig===GENUS_DATA.length)?'#2e7d32':'#555';
  if(richtig===GENUS_DATA.length) genusTimerStop();
}
function showGenusLoesung(){
  Array.from(document.querySelectorAll('#sec-genus .genus-chip')).forEach(function(chip){
    var z=document.getElementById('drop-'+chip.dataset.cat);
    if(z){ z.appendChild(chip); chip.classList.remove('wrong'); chip.classList.add('correct'); }
  });
  updateGenusFeedback();
}
function resetGenus(){ initGenus(); genusTimerReset(); }
(function(){ try{ if(typeof initTimer==='function') initTimer(GENUS_TIMER); }catch(e){} initGenus(); })();
</script>
''' % (data, ti)

def main():
    if len(sys.argv) != 3:
        print("Aufruf: inject_genus.py DATEI.html woerter.json"); sys.exit(1)
    path, wjson = sys.argv[1], sys.argv[2]
    words = json.load(open(wjson, encoding='utf-8'))
    if len(words) < 20 or any(w["cat"] not in ("der","die","das","pl") for w in words):
        print("ABBRUCH: woerter.json braucht >=20 Einträge, cat in der/die/das/pl"); sys.exit(2)
    t = open(path, encoding='utf-8').read()

    if genus_cats(t) & {"der","die","das","pl"}:
        print("SKIP (hat schon Genus-Tab):", path); sys.exit(0)
    if 'showSection(' not in t:
        print("ABBRUCH (kein showSection):", path); sys.exit(2)

    # --- Nav: alle nav-btn finden ---
    navs = list(re.finditer(r'<div class="nav-btn"[^>]*onclick="showSection\(\d+\)"[^>]*>.*?</div>', t, re.S))
    if not navs:
        print("ABBRUCH (keine nav-btn):", path); sys.exit(2)
    wnav = None
    for m in navs:
        if 'Wortschatz' in m.group(0): wnav = m
    if wnav is None or wnav is not navs[-1]:
        print("ABBRUCH (Wortschatz ist nicht letzter Nav-Tab):", path); sys.exit(2)
    # Genus-Nav aus Wortschatz-Button klonen (Format-treu)
    gnav = wnav.group(0)
    gnav = re.sub(r'(&#128218;|📚|📖|🏷️)', '🏷️', gnav, count=1)
    gnav = gnav.replace('Wortschatz', 'Genus')
    t = t[:wnav.start()] + gnav + "\n        " + t[wnav.start():]
    # Nav neu durchnummerieren (DOM-Reihenfolge)
    counter = {'n': 0}
    def renum(m):
        r = '<div class="nav-btn"' + m.group(1) + 'onclick="showSection(%d)"' % counter['n']
        counter['n'] += 1
        return r
    t = re.sub(r'<div class="nav-btn"([^>]*?)onclick="showSection\(\d+\)"', renum, t)

    # --- Sections ---
    secs = list(re.finditer(r'<div class="section(?:\s+active)?"\s+id="[^"]*"', t))
    if not secs:
        print("ABBRUCH (keine sections):", path); sys.exit(2)
    last_sec = secs[-1]
    # letzter Tab muss Wortschatz sein (Guard) — h2-Text prüfen (Base64-Banner ignorieren)
    tail = t[last_sec.start():]
    h2m = re.search(r'<h2>(.*?)</h2>', tail, re.S)
    h2txt = h2m.group(1) if h2m else ''
    if 'Wortschatz' not in h2txt and 'wortschatzContainer' not in tail:
        print("ABBRUCH (letzte Section ist nicht Wortschatz):", path); sys.exit(2)

    has_help = 'help-box' in t
    has_ctrl = 'control-bar' in t
    # freien Timer-Index bestimmen
    idxs = [int(x) for x in re.findall(r'id="timer-(\d+)"', t)]
    timer_idx = (max(idxs)+1) if idxs else 6

    sec = section_html(words, has_help, has_ctrl, timer_idx)
    # Section-Kommentar direkt davor mitnehmen, falls vorhanden
    pre = t[:last_sec.start()]
    cmt = re.search(r'(\n\s*<!--[^\n]*-->\s*)$', pre)
    insert_at = cmt.start() if cmt else last_sec.start()
    t = t[:insert_at] + sec + t[insert_at:]

    # --- CSS vor letztem </style> ---
    pos = t.rfind('</style>')
    if pos == -1:
        print("ABBRUCH (kein </style>):", path); sys.exit(2)
    t = t[:pos] + CSS + t[pos:]

    # --- JS als eigener <script> vor letztem </script> ---
    jpos = t.rfind('</script>')
    if jpos == -1:
        print("ABBRUCH (kein </script>):", path); sys.exit(2)
    jpos += len('</script>')
    t = t[:jpos] + js_block(words, timer_idx) + t[jpos:]

    open(path, 'w', encoding='utf-8').write(t)
    print("OK injiziert (timer=%d, help=%s, ctrl=%s):" % (timer_idx, has_help, has_ctrl), path)

if __name__ == "__main__":
    main()
