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

# AMBIGUOUS_BUILDERS sind Baufunktionsnamen, die in MANCHEN Dateien den Wortschatz-Training-Tab
# bauen, in ANDEREN Dateien aber einen völlig anderen Tab (z.B. eine Vorentlastungs-Fotokarten-
# Liste "Wörter") — Fund 2026-07-04: DE_A2_2015V u.a. haben SOWOHL `buildVocab()` (Wörter-Tab)
# ALS AUCH `initVocab()` (echter Wortschatz-Tab) im selben File. Nur die tatsächlich als Ziel
# identifizierte Funktion (Variable `builder` in process()) wird gestrippt/umbenannt — NIE
# pauschal alle Namen dieser Liste, sonst wird der falsche Tab zerstört.
AMBIGUOUS_BUILDERS = ["initWortschatz", "buildVocab", "initVocab", "renderVocab", "vocabInit",
                      "buildWortschatz", "renderWortschatz",
                      # "wortGrid"-Generation (Fund 2026-07-04: DE_B1_1036R) — Container id="wortGrid",
                      # Datenarray WORT_DATA, Buttons wortAlleZeigen()/wortReset().
                      "wortRender",
                      # "initWs"-Generation (Fund 2026-07-04: DE_B1_1063R) — Container id="wsContainer",
                      # Datenarray wiederverwendet aus der Vorentlastung (VORENTLASTUNG), Buttons
                      # showWsLoesung()/resetWs(). VORENTLASTUNG bleibt als Datenquelle für
                      # highlightVocabInText() erhalten — nur initWs() selbst wird ersetzt.
                      "initWs",
                      # "vocab-grid"-Generation (Fund 2026-07-04: DE_B2_2073R) — Container
                      # id="vocab-grid" (mit Bindestrich), Datenarray vocabItems, Buttons
                      # vocabReset() (kein separater Lösungs-Button in dieser Generation).
                      "vocabBuild"]
# SAFE_HELPERS_TO_STRIP sind Check/Reset/Lösungs-Helfer, die praxisnah IMMER exklusiv zum
# Wortschatz-Training-Tab gehören (ein einfacher Foto-Vorschau-Tab hat keine eigene Check-Logik).
FUNCS_TO_STRIP = ["wortschatzCheck", "checkWortschatzAllOk",
                  "showWortschatzLoesung", "showWsLoesung", "resetWortschatz",
                  "wsCheck", "buildWsCard",
                  "vocabLiveCheck", "vocabCheck", "vocabReset", "resetVocab", "checkVocabAllDone",
                  "showVocabLoesung", "vocabShowLoesung",
                  "vocabCheckAllOk",
                  "wortAlleZeigen", "wortReset",
                  "resetWs", "checkWsAllDone",
                  "vocabReset"]


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
    DATAVAR_CANDIDATES = ["WORTSCHATZ", "WS_DATA", "WORTSCHATZ_DATA", "VOCAB_DATA", "VOKABELN",
                          "vocabData", "WORT_DATA",
                          # VORENTLASTUNG wird in MANCHEN Dateien (Fund 2026-07-04: DE_B1_1063R)
                          # zusätzlich als Wortschatz-Trainingsdaten wiederverwendet (initWs()).
                          # Sicher, weil Datavar-Auswahl den Körper des GEWONNENEN Builders
                          # (initWs) durchsucht — nie einen anderen Vorentlastungs-Tab.
                          "VORENTLASTUNG",
                          # vocabItems (Fund 2026-07-04: DE_B2_2073R, vocabBuild()-Generation).
                          "vocabItems"]
    # 1) Baufunktion zuerst identifizieren (Generationen: initWortschatz / buildVocab / initVocab /
    #    renderVocab / vocabInit) — ihr Körper ist die verlässliche Quelle für BEIDE, Container-Id
    #    UND Datenvariable. Kommen MEHRERE Kandidatennamen im selben File vor (Fund 2026-07-04:
    #    getrennte Tabs "Wörter"/buildVocab und "Wortschatz"/initVocab), gewinnt die Funktion,
    #    deren referenzierter Container am WEITESTEN HINTEN im Dokument liegt — der Wortschatz-
    #    Training-Tab liegt konventionell spät (Tail-Reihenfolge Genus→Wortschatz→Schreiben).
    builder = None
    old = ""
    candidates = []
    for name in AMBIGUOUS_BUILDERS:
        body = func_body(s, name)
        if body:
            candidates.append((name, body))
    if len(candidates) == 1:
        builder, old = candidates[0]
    elif len(candidates) > 1:
        def _last_ref_pos(body):
            ids = re.findall(r"getElementById\(\s*['\"]([\w-]+)['\"]\s*\)", body)
            pos = -1
            for i in ids:
                p = s.rfind('id="' + i + '"')
                if p > pos: pos = p
            return pos
        builder, old = max(candidates, key=lambda bc: _last_ref_pos(bc[1]))
    # 2) Datenvariable: BEVORZUGT aus dem Bau-Funktionskörper lesen — schützt vor Verwechslung mit
    #    einem gleichnamigen Array eines ANDEREN Tabs (Fund 2026-07-04: DE_A2_2051V/2061V haben
    #    sowohl eine Vorentlastungs-Liste `WORTSCHATZ` für Tab "Wörter" als auch `WS_DATA` für den
    #    echten Wortschatz-Training-Tab — ein globaler Scan hätte die FALSCHE Liste erwischt und
    #    2 Wörter verloren, die nur in WS_DATA stehen). Fallback: globaler Scan wie bisher, falls
    #    kein Bau-Funktionskörper gefunden wurde.
    datavar = None
    if old:
        referenced = set(re.findall(r"\b([A-Za-z_][A-Za-z0-9_]*)\s*\.\s*forEach", old))
        for v in DATAVAR_CANDIDATES:
            if v in referenced and re.search(r"\b(var|const|let)\s+" + v + r"\s*=\s*\[", s):
                datavar = v; break
    if not datavar:
        for v in DATAVAR_CANDIDATES:
            if re.search(r"\b(var|const|let)\s+" + v + r"\s*=\s*\[", s):
                datavar = v; break
    if not datavar:
        return "ABBRUCH: keine Wortschatz-Datenvariable gefunden"
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
        if len(grid_like) == 1:
            # Eindeutiger Grid/Container-Kandidat — NICHT den ersten getElementById-Treffer
            # im Fließtext nehmen (der ist oft ein Timer-Reset VOR dem eigentlichen Container,
            # Fund 2026-07-04: DE_A2_2051V/2061V — erster Treffer war 'timer5', nicht 'vocabGrid').
            cont_id = grid_like[0]
        else:
            mm = re.search(r"getElementById\(\s*['\"]([\w-]+)['\"]\s*\)", old)
            if mm: cont_id = mm.group(1)
    if not cont_id:
        for cand in ["wortschatzContainer", "wsGrid", "vocabGrid", "wortschatzGrid", "wsContainer", "vocabContainer", "wortGrid"]:
            if 'id="' + cand + '"' in s: cont_id = cand; break
    if not cont_id:
        return "ABBRUCH: Render-Container nicht gefunden"
    # 3) Container-Tag(e) lokalisieren. NORMALFALL: genau ein Treffer. Bei doppelter ID (Bug in
    #    der Quelle, Fund 2026-07-04: DE_A2_2051V/2061V hatten id="vocabGrid" sowohl im
    #    Vorentlastungs-Tab "Wörter" als auch im Wortschatz-Training-Tab, wodurch getElementById
    #    immer nur die ERSTE traf) NICHT den ersten Treffer nehmen — der Wortschatz-Tab liegt
    #    konventionell spät im Dokument (Tail-Reihenfolge Genus→Wortschatz→Schreiben); die dem
    #    Dateiende nächste Instanz ist die Wortschatz-Training-Instanz.
    cont_tag_re = re.compile(r'<div[^>]*id="' + re.escape(cont_id) + r'"[^>]*>\s*</div>')
    cont_matches = list(cont_tag_re.finditer(s))
    if not cont_matches:
        return "ABBRUCH: Container-Tag nicht ersetzbar (id=" + cont_id + ")"
    target = cont_matches[-1]
    cidx = target.start()
    # Section-ID: die ID des zuletzt GEÖFFNETEN class="section"-Divs VOR dem Container. Nicht auf
    # ein Namensmuster raten (sec-1, sec-genus, secN, tabN, … — Generationen variieren beliebig,
    # Fund 2026-07-04: A2.1-Dateien mit "tab0".."tab5" statt "sec…" hätten mit einem sec-Muster
    # den FALSCHEN, vorherigen Tab getroffen, z.B. "sec-genus" statt "tab5" → toter Lösungen-
    # Button, weil der Selector die falsche Section traf). Stattdessen strukturell aus dem echten
    # `<div class="section…" id="…">`-Tag lesen, ID-Attribut in beliebiger Reihenfolge zulässig.
    def _section_ids_before(pos):
        out = []
        # G-Dateien nutzen <section class="section">, R/X/V/W/C-Dateien <div class="section">
        # (daf-kern) — beide Tag-Namen zulassen (Fund 2026-07-04: DE_A2_1062X/1065V hätten mit
        # nur <div> das <section id="tab4"> übersehen und "sec-genus" davor gewählt).
        for m in re.finditer(r'<(?:div|section)\b[^>]*>', s[:pos]):
            tag = m.group(0)
            cls = re.search(r'class="([^"]*)"', tag)
            if not cls or not re.search(r'(?<![\w-])section(?![\w-])', cls.group(1)):
                continue
            idm = re.search(r'id="([\w-]+)"', tag)
            if idm:
                out.append((m.start(), idm.group(1)))
        return out
    sec_matches = _section_ids_before(cidx)
    if not sec_matches:
        return "ABBRUCH: Section-ID nicht gefunden"
    sec_pos, secid = sec_matches[-1]
    # Timer-Index: zwischen Section-Start und Container
    env = s[sec_pos:cidx + 600]
    tm = re.search(r'timer-(\d+)', env) or re.search(r'timerResetOne\((\d+)\)', env) or re.search(r'resetTimer\((\d+)\)', env)
    if tm: tidx = int(tm.group(1))
    else:
        mnum = re.search(r'(\d+)$', secid); tidx = int(mnum.group(1)) if mnum else 6
    # 4) Container normalisieren — NUR die als Ziel identifizierte Instanz ersetzen (bei
    #    Duplikaten bleibt die andere Instanz unangetastet, z.B. der Vorentlastungs-Grid).
    # KEIN Inline-Grid-Style: Inline schlägt die Mobil-Media-Query des CSS-Blocks
    # (iPhone blieb zweispaltig, rechte Spalte abgeschnitten — Frank-Fund 2026-07-04).
    # Das Grid kommt ausschließlich aus FB-WORTSCHATZ-KANON-CSS.
    s = s[:target.start()] + '<div id="wortschatzContainer"></div>' + s[target.end():]
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
    # 6) alte Funktionen entfernen — feste sichere Helfer-Liste + NUR die als Ziel identifizierte
    #    Baufunktion (nie pauschal alle AMBIGUOUS_BUILDERS-Namen, sonst reißt es einen fremden Tab
    #    ein, der zufällig denselben Funktionsnamen benutzt, Fund 2026-07-04: DE_A2_2015V u.a.)
    #    + alle Wortschatz-Lösungs-Varianten (außer der kanonischen).
    strip_names = list(FUNCS_TO_STRIP)
    if builder:
        strip_names.append(builder)
    for fn in strip_names:
        s = strip_func(s, fn)
    for fn in set(re.findall(r'function\s+([A-Za-z_][A-Za-z0-9_]*)\s*\(', s)):
        if _is_ws_loesung(fn) and fn != "showWortschatzLoesung":
            s = strip_func(s, fn)
    # 6b) Verwaiste Aufrufe der gestrippten Baufunktion (z.B. `initVocab();` in der Init-Sequenz)
    #     auf den Kanon umbiegen — sonst ReferenceError (Fund 2026-07-04). NUR den gewählten
    #     Builder-Namen umbiegen, ein NICHT gewählter Namensvetter (anderer Tab) bleibt unberührt.
    if builder:
        s = re.sub(r'\b' + re.escape(builder) + r'\s*\(\s*\)', 'initWortschatz()', s)
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
