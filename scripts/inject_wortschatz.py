#!/usr/bin/env python3
"""inject_wortschatz.py — baut den Wortschatz-Tab DETERMINISTISCH auf das kanonische
Muster (daf-uebungsformen/wortschatz-full-pattern.md) um. Vorbild: inject_genus.py.

Strategie (generationsrobust):
  - Daten werden NICHT umgeschrieben — die injizierte initWortschatz ist SCHEMA-ADAPTIV
    (liest art|artikel, de|wort|word, plural|pl, en|prompt; type aus Artikel abgeleitet).
  - Render-Container wird auf <div id="wortschatzContainer"> normalisiert.
  - Steuerleisten-Buttons → showWortschatzLoesung()/resetWortschatz().
  - Alte Wortschatz-Funktionen werden klammer-sicher entfernt und durch den kanonischen
    Block ersetzt (Marker FB-WORTSCHATZ-KANON), parametrisiert mit echter Section-ID + Timer-Index.

Guards: bricht sicher ab, wenn Section-ID/Container/Datenvariable nicht gefunden werden.
Nutzung: python3 inject_wortschatz.py datei.html [...]
"""
import re, sys, io

FUNCS_TO_STRIP = ["initWortschatz", "wortschatzCheck", "checkWortschatzAllOk",
                  "showWortschatzLoesung", "showWsLoesung", "resetWortschatz",
                  "buildWortschatz", "renderWortschatz", "wsCheck", "buildWsCard",
                  # B2-Root-"vocab"-Generation (Fund 2026-07-04)
                  "buildVocab", "initVocab", "renderVocab", "vocabLiveCheck",
                  "vocabCheck", "vocabReset", "resetVocab", "checkVocabAllDone",
                  "showVocabLoesung", "vocabShowLoesung",
                  # A1-"vocabInit"-Generation (Fund 2026-07-04, DE_A1_1113G/1123G)
                  "vocabInit", "vocabCheckAllOk"]


def strip_func(s, name):
    """Entfernt ALLE `function name(...){...}` klammer-sicher."""
    out = s
    while True:
        m = re.search(r"function\s+" + re.escape(name) + r"\s*\([^)]*\)\s*\{", out)
        if not m:
            return out
        i = m.start(); j = m.end() - 1; depth = 0
        while j < len(out):
            if out[j] == "{": depth += 1
            elif out[j] == "}":
                depth -= 1
                if depth == 0: break
            j += 1
        out = out[:i] + out[j + 1:]


def func_body(s, name):
    m = re.search(r"function\s+" + re.escape(name) + r"\s*\([^)]*\)\s*\{", s)
    if not m: return None
    i = m.end() - 1; depth = 0
    for k in range(i, len(s)):
        if s[k] == "{": depth += 1
        elif s[k] == "}":
            depth -= 1
            if depth == 0: return s[i:k + 1]
    return None


CSS_BLOCK = (
'\n/* FB-WORTSCHATZ-KANON-CSS — skill-konforme Karten-Optik, NUR im Wortschatz-Tab (überschreibt'
' abweichende Datei-CSS, Lückentext bleibt unberührt) */\n'
'#wortschatzContainer{display:grid;grid-template-columns:1fr 1fr;gap:10px;}\n'
'#wortschatzContainer .luecken-item,#wortschatzContainer .luecke-item{background:#f8f9ff;border:1px solid #dde3ff;border-left:4px solid #667eea;border-radius:10px;padding:12px 16px;margin:0;display:block;}\n'
'#wortschatzContainer .luecken-item>div:first-child,#wortschatzContainer .luecke-item>div:first-child,#wortschatzContainer .ws-en{font-weight:700;color:#667eea;margin-bottom:8px;font-size:1.05em;}\n'
'#wortschatzContainer input.blank{border:none;border-bottom:2px solid #667eea;border-radius:0;background:#fff;padding:4px 6px;outline:none;font-family:inherit;font-size:0.95em;}\n'
'#wortschatzContainer input.blank:focus{border-bottom-color:#764ba2;}\n'
'#wortschatzContainer input.blank.correct{border-bottom-color:#27ae60;background:#e8f8f0;}\n'
'#wortschatzContainer input.blank.wrong{border-bottom-color:#e74c3c;background:#fdeaea;}\n'
'@media(max-width:640px){#wortschatzContainer{grid-template-columns:1fr;}}\n')


def inject_css(s):
    if "FB-WORTSCHATZ-KANON-CSS" in s:
        return s
    i = s.find("</style>")
    if i < 0:
        return s
    return s[:i] + CSS_BLOCK + s[i:]


def canonical_block(secid, tidx, datavar, stop_fn="stopTimer", reset_fn="resetTimer"):
    return ('\n/* FB-WORTSCHATZ-KANON — deterministisch, schema-adaptiv (inject_wortschatz.py) */\n'
'function initWortschatz(){\n'
'  var c=document.getElementById("wortschatzContainer"); if(!c) return; c.innerHTML="";\n'
'  ' + datavar + '.forEach(function(item){\n'
'    var artikel=(item.artikel!==undefined)?item.artikel:(item.art||"");\n'
'    var de=(item.de!==undefined)?item.de:(item.wort||item.word||"");\n'
'    var plural=(item.plural!==undefined)?item.plural:(item.pl||"");\n'
'    var en=(item.en!==undefined)?item.en:(item.prompt||item.frage||"");\n'
'    var type=item.type||(artikel?"n":"p");\n'
'    var row=document.createElement("div"); row.className="luecken-item"; row.style.marginBottom="0";\n'
'    var p=document.createElement("div"); p.style.cssText="font-weight:600;color:#667eea;margin-bottom:6px;font-size:1.05em;"; p.textContent=en; row.appendChild(p);\n'
'    var fl=document.createElement("div"); fl.style.cssText="display:flex;gap:8px;flex-wrap:wrap;align-items:center;";\n'
'    function mk(ph,w,ans,fld){var i=document.createElement("input");i.className="blank";i.type="text";i.placeholder=ph;i.style.width=w;i.dataset.answer=ans;i.dataset.field=fld;i.oninput=function(){wortschatzCheck(this);if(typeof timerAutoStart==="function")timerAutoStart(' + str(tidx) + ');checkWortschatzAllOk();};return i;}\n'
'    if(type==="n"){\n'
'      fl.appendChild(mk("Artikel","70px",artikel,"art"));\n'
'      fl.appendChild(mk("Wort","160px",de,"word"));\n'
'      var pl=mk("Plural","140px",plural,"plural");\n'
'      if(plural==="\\u2013"||plural===""||plural==="-"){pl.value="\\u2013";pl.disabled=true;pl.dataset.answer="\\u2013";pl.classList.add("correct");pl.style.opacity="0.6";pl.title="Dieses Wort hat keinen Plural";pl.oninput=null;}\n'
'      fl.appendChild(pl);\n'
'    } else { fl.appendChild(mk("Deutsch","220px",de,"word")); }\n'
'    row.appendChild(fl); c.appendChild(row);\n'
'  });\n'
'}\n'
'function wortschatzCheck(inp){\n'
'  var u=inp.value,a=inp.dataset.answer,f=inp.dataset.field; inp.classList.remove("correct","wrong"); if(!u) return;\n'
'  var cu=(f==="art")?u.toLowerCase().trim():u.trim(); var ca=(f==="art")?(a||"").toLowerCase():a;\n'
'  if(cu===ca) inp.classList.add("correct"); else if(ca.indexOf(cu)===0){} else inp.classList.add("wrong");\n'
'}\n'
'function checkWortschatzAllOk(){\n'
'  var ins=document.querySelectorAll("#' + secid + ' input.blank");\n'
'  var ok=ins.length>0 && Array.from(ins).every(function(i){return i.disabled||i.classList.contains("correct");});\n'
'  if(ok){try{if(typeof ' + stop_fn + '==="function") ' + stop_fn + '(' + str(tidx) + ');}catch(e){}}\n'
'}\n'
'function showWortschatzLoesung(){\n'
'  try{if(typeof ' + stop_fn + '==="function") ' + stop_fn + '(' + str(tidx) + ');}catch(e){}\n'
'  document.querySelectorAll("#' + secid + ' input.blank").forEach(function(inp){inp.value=inp.dataset.answer;inp.classList.add("correct");inp.classList.remove("wrong");});\n'
'}\n'
'function resetWortschatz(){\n'
'  document.querySelectorAll("#' + secid + ' input.blank").forEach(function(inp){if(!inp.disabled){inp.value="";inp.classList.remove("correct","wrong");}});\n'
'  try{if(typeof ' + reset_fn + '==="function") ' + reset_fn + '(' + str(tidx) + ');}catch(e){}\n'
'}\n'
'try{window.initWortschatz=initWortschatz;window.wortschatzCheck=wortschatzCheck;window.checkWortschatzAllOk=checkWortschatzAllOk;window.showWortschatzLoesung=showWortschatzLoesung;window.resetWortschatz=resetWortschatz;}catch(e){}\n')


def process(path):
    s = io.open(path, encoding="utf-8").read()
    if "FB-WORTSCHATZ-KANON" in s:
        return "skip (schon kanonisch-injiziert)"
    # 1) Datenvariable
    datavar = None
    for v in ["WORTSCHATZ", "WS_DATA", "WORTSCHATZ_DATA", "VOCAB_DATA", "VOKABELN",
              "vocabData", "WORT_DATA"]:
        if re.search(r"\b(var|const|let)\s+" + v + r"\s*=\s*\[", s):
            datavar = v; break
    if not datavar:
        return "ABBRUCH: keine Wortschatz-Datenvariable gefunden"
    # 2) Container-Id aus alter Baufunktion (Generationen: initWortschatz / buildVocab / initVocab / renderVocab)
    old = ""
    for builder in ["initWortschatz", "buildVocab", "initVocab", "renderVocab", "vocabInit"]:
        old = func_body(s, builder)
        if old:
            break
    cont_id = None
    if old:
        # SICHERHEIT: Nicht-Standard-Wortschatz mit MEHREREN Render-Containern (z.B. Vergleich
        # stadtGrid/landGrid) NICHT anfassen — sonst bleiben Referenzen auf den nicht-ersetzten
        # Container hängen → Laufzeit-Crash (1051X-Lehre). Sauber abbrechen, manuell behandeln.
        grids = set(re.findall(r"getElementById\(\s*['\"]([\w-]+)['\"]\s*\)", old))
        grid_like = [g for g in grids if ("grid" in g.lower() or "container" in g.lower()
                                          or "vokab" in g.lower() or "wortschatz" in g.lower())]
        if len(grid_like) > 1:
            return "ABBRUCH: mehrere Render-Container (" + ",".join(sorted(grid_like)) + ") — Nicht-Standard, manuell"
        mm = re.search(r"getElementById\(\s*['\"]([\w-]+)['\"]\s*\)", old)
        if mm: cont_id = mm.group(1)
    if not cont_id:
        for cand in ["wortschatzContainer", "wsGrid", "vocabGrid", "wortschatzGrid", "wsContainer", "vocabContainer"]:
            if 'id="' + cand + '"' in s: cont_id = cand; break
    if not cont_id:
        return "ABBRUCH: Render-Container nicht gefunden"
    # 3) Section-Id + Timer-Index aus Container-Umfeld
    cidx = s.find('id="' + cont_id + '"')
    # Section-ID: letzte sec-... VOR dem Container (ganzer Vortext — Banner-Base64-robust)
    sec_matches = list(re.finditer(r'id="(sec-[\w-]+)"', s[:cidx]))
    if not sec_matches:
        return "ABBRUCH: Section-ID nicht gefunden"
    secid = sec_matches[-1].group(1)
    sec_pos = sec_matches[-1].start()
    # Timer-Index: zwischen Section-Start und Container
    env = s[sec_pos:cidx + 600]
    tm = re.search(r'timer-(\d+)', env) or re.search(r'timerResetOne\((\d+)\)', env) or re.search(r'resetTimer\((\d+)\)', env)
    if tm: tidx = int(tm.group(1))
    else:
        mnum = re.match(r'sec-(\d+)$', secid); tidx = int(mnum.group(1)) if mnum else 6
    # 4) Container normalisieren
    s2 = re.sub(r'<div[^>]*id="' + re.escape(cont_id) + r'"[^>]*>\s*</div>',
                '<div id="wortschatzContainer" style="display:grid; grid-template-columns:1fr 1fr; gap:10px;"></div>', s, count=1)
    if s2 == s and cont_id != "wortschatzContainer":
        return "ABBRUCH: Container-Tag nicht ersetzbar (id=" + cont_id + ")"
    s = s2
    # 5) Steuerleisten-Buttons normalisieren: JEDE Wortschatz-Lösungen-Variante (Name enthält
    #    "loesung/lösung" UND "wortschatz/ws") → showWortschatzLoesung(). Andere Tabs (showZuoLoesung,
    #    showLueckeLoesung, showGenusLoesung) enthalten kein wortschatz/ws → unberührt.
    def _ws_token(n):
        return "wortschatz" in n or "ws" in n or "vocab" in n or "vokab" in n

    def _is_ws_loesung(name):
        n = name.lower()
        return ("loesung" in n or "lösung" in n) and _ws_token(n)

    def _is_ws_reset(name):
        n = name.lower()
        return "reset" in n and _ws_token(n)

    def _norm_onclick(m):
        if _is_ws_loesung(m.group(1)):
            return 'onclick="showWortschatzLoesung()"'
        if _is_ws_reset(m.group(1)):
            return 'onclick="resetWortschatz()"'
        return m.group(0)

    s = re.sub(r'onclick="\s*([A-Za-z_][A-Za-z0-9_]*)\s*\(\s*\)\s*"', _norm_onclick, s)
    # 5b) Compound-Onclicks der vocab-Generation (z.B. "resetVocab(); timerResetOne(3);" oder
    #     "showVocabLoesung(4)") — die referenzierten Funktionen werden gleich gestrippt,
    #     der Handler wäre tot. Auf die kanonischen Handler normalisieren (Fund 2026-07-04).
    def _norm_compound(m):
        val = m.group(1)
        if re.search(r'\b(showVocab\w*|vocabShow\w*)\s*\(', val):
            return 'onclick="showWortschatzLoesung()"'
        if re.search(r'\b(resetVocab|vocabReset)\s*\(', val):
            return 'onclick="resetWortschatz()"'
        return m.group(0)

    s = re.sub(r'onclick="([^"]*[Vv]ocab[^"]*)"', _norm_compound, s)
    # 5c) Fehlende Steuerleiste ergänzen (Direct-Feedback-Altbestand ohne jeden Lösungen/Neustart-
    #     Button, Fund 2026-07-04: A1 WORT_DATA-Generation). Franks Grundsatz: JEDER Wortschatz-Tab
    #     bekommt die kanonischen Pill-Buttons — keine Ausnahme für "nur Live-Feedback"-Alt-Layouts.
    #     Nur einfügen, wenn nach der Normalisierung oben KEIN showWortschatzLoesung()-Aufruf existiert.
    if not re.search(r'onclick="\s*showWortschatzLoesung\(\)\s*"', s):
        pill_bar = ('<div style="display:flex;gap:8px;margin:0 0 14px;">'
                    '<button onclick="showWortschatzLoesung()" style="background:#f5f7ff;border:1px solid #c5cff5;'
                    'border-radius:8px;padding:6px 16px;font-size:0.85em;color:#667eea;cursor:pointer;font-weight:600;">'
                    '\U0001f4a1 Lösungen</button>'
                    '<button onclick="resetWortschatz()" style="background:#f5f7ff;border:1px solid #c5cff5;'
                    'border-radius:8px;padding:6px 16px;font-size:0.85em;color:#667eea;cursor:pointer;font-weight:600;">'
                    '↺ Neustart</button></div>\n')
        s3 = s.replace('<div id="wortschatzContainer"', pill_bar + '<div id="wortschatzContainer"', 1)
        if s3 == s:
            return "ABBRUCH: Container-Tag fuer Pill-Bar-Insertion nicht gefunden"
        s = s3
    # 6) alte Funktionen entfernen — feste Liste + alle Wortschatz-Lösungs-Varianten (außer der kanonischen)
    for fn in FUNCS_TO_STRIP:
        s = strip_func(s, fn)
    for fn in set(re.findall(r'function\s+([A-Za-z_][A-Za-z0-9_]*)\s*\(', s)):
        if _is_ws_loesung(fn) and fn != "showWortschatzLoesung":
            s = strip_func(s, fn)
    # 6b) Verwaiste Aufrufe gestrippter Baufunktionen (z.B. `initVocab();` in der
    #     Init-Sequenz) auf den Kanon umbiegen — sonst ReferenceError (Fund 2026-07-04).
    s = re.sub(r'\b(initVocab|buildVocab|renderVocab|buildWortschatz|renderWortschatz)\s*\(\s*\)', 'initWortschatz()', s)
    # 7) kanonischen Block DIREKT NACH dem Daten-Array einfügen (gleicher <script>-Block
    #    wie der initWortschatz()-Aufruf — sonst ReferenceError über Block-Grenzen hinweg).
    # Timer-Funktionsnamen der Datei übernehmen (Lehre: stopTimer vs timerStop,
    # resetTimer vs timerResetOne — hardcodierte Namen laufen sonst ins Leere).
    stop_fn = "stopTimer" if re.search(r"function\s+stopTimer\b", s) else (
        "timerStop" if re.search(r"function\s+timerStop\b", s) else "stopTimer")
    reset_fn = "resetTimer" if re.search(r"function\s+resetTimer\b", s) else (
        "timerResetOne" if re.search(r"function\s+timerResetOne\b", s) else "resetTimer")
    blk = canonical_block(secid, tidx, datavar, stop_fn, reset_fn)
    dm = re.search(r"(?:var|const|let)\s+" + datavar + r"\s*=\s*\[", s)
    if not dm: return "ABBRUCH: Daten-Array-Start nicht gefunden"
    k = dm.end() - 1; depth = 0; end = None
    while k < len(s):
        if s[k] == "[": depth += 1
        elif s[k] == "]":
            depth -= 1
            if depth == 0: end = k; break
        k += 1
    if end is None: return "ABBRUCH: Daten-Array-Ende nicht gefunden"
    # bis zum abschließenden ; vorrücken
    semi = s.find(";", end)
    ins = (semi + 1) if (semi != -1 and semi - end < 4) else (end + 1)
    call = "" if re.search(r'\binitWortschatz\(\)', s) else "\ninitWortschatz();"
    s = s[:ins] + "\n" + blk + call + "\n" + s[ins:]
    # 8) kanonische Wortschatz-Optik (scoped CSS) sicherstellen
    s = inject_css(s)
    io.open(path, "w", encoding="utf-8").write(s)
    return "OK sec=" + secid + " timer=" + str(tidx) + " data=" + datavar + " container=" + cont_id


if __name__ == "__main__":
    for p in sys.argv[1:]:
        print(process(p), "<-", p.split("/")[-1])
