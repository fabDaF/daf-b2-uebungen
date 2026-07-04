#!/usr/bin/env python3
"""fix_lt_buttons.py — stellt im kanonischen Story-Lückentext-Tab die zwei
kanonischen Steuer-Buttons sicher: „💡 Lösungen" → fbLtShowLoesung() und
„↺ Neustart" → fbLtReset() (+ Timer-Reset der Datei, adaptiv).

Hintergrund (Frank-Fund 2026-07-04 an 1013R): Die Engine (lt-story-engine.js)
stellt die Hooks bereit, aber inject_lt.py rührt Steuerleisten nicht an —
264 kanonische Dateien hatten keinen (funktionierenden) Lösungen-Button.

Semantik ist bewusst konservativ:
  - Datei ohne FB-LT-STORY-CSS oder ohne #wortbank-luecken → skip.
  - fbLtShowLoesung bereits verdrahtet → skip (idempotent).
  - Adapter-Dateien (zweiter LT-Tab, lueckenContainer2/blank2) → ABBRUCH, manuell.
  - Vorhandene Lösungen-/Neustart-Buttons im LT-Abschnitt werden auf die
    Engine-Hooks umverdrahtet und auf den kanonischen Pill-Stil normalisiert
    (Label aus Funktion, nie aus Klasse — CLAUDE.md Pill-Regel).
  - Fehlende Buttons werden ergänzt: in die bestehende .btn-row, sonst als
    neue Steuerzeile direkt vor der Wortbank.

Ob ein VORHANDENER Alt-Button funktioniert oder tot ist, entscheidet dieses
Skript NICHT — das prüft der dynamische Test scripts/lt_verify.js. Der
Rollout-Workflow ruft fix_lt_buttons.py nur für Dateien auf, die lt_verify.js
als MISSING oder DEAD gemeldet hat.

Nutzung: python3 scripts/fix_lt_buttons.py datei.html [...]
"""
import io
import re
import sys

PILL = ("background:#f5f7ff;border:1px solid #c5cff5;border-radius:8px;"
        "padding:6px 16px;font-size:0.85em;color:#667eea;cursor:pointer;font-weight:600;")

BTN_RE = re.compile(r'<button\b[^>]*onclick="([^"]*)"[^>]*>([^<]*)</button>')


def _loes_btn_html():
    return ('<button onclick="fbLtShowLoesung()" style="' + PILL + '">'
            '\U0001F4A1 Lösungen</button>')


def _reset_btn_html(timer_call):
    oc = "fbLtReset();" + ((" " + timer_call) if timer_call else "")
    return ('<button onclick="' + oc + '" style="' + PILL + '">'
            '↺ Neustart</button>')


def ensure_buttons(s):
    """Gibt (neuer_text, status) zurück. status: 'ok'|'skip: …'|'ABBRUCH: …'"""
    if "FB-LT-STORY-CSS" not in s:
        return s, "skip: nicht kanonisch"
    i_attr = s.find('id="wortbank-luecken"')
    if i_attr < 0:
        return s, "skip: kein Wortbank-Container"
    if ("lueckenContainer2" in s) or ("blank2" in s):
        return s, "ABBRUCH: Adapter-Datei (zweiter LT-Tab) — manuell"
    # Anker = START des Container-Tags, nicht das id-Attribut — sonst zerreißt
    # eine Einfügung den Tag (Fund 2026-07-04, 9 A1-Dateien restauriert).
    i = s.rfind("<", 0, i_attr)
    if i < 0:
        return s, "ABBRUCH: Container-Tag-Start nicht gefunden"

    sec_start = max(s.rfind('<div class="section"', 0, i), s.rfind('<section', 0, i))
    if sec_start < 0:
        return s, "ABBRUCH: Section-Start nicht gefunden"
    env = s[sec_start:i]
    if "fbLtShowLoesung" in env:
        return s, "skip: schon verdrahtet"

    # Timer-Aufruf der Datei ermitteln (Index aus dem Abschnitt, Funktionsname adaptiv).
    tm = re.search(r'timer-(\d+)', env)
    timer_call = ""
    if tm:
        if re.search(r'function\s+timerResetOne\b', s):
            timer_call = "timerResetOne(" + tm.group(1) + ");"
        elif re.search(r'function\s+resetTimer\b', s):
            timer_call = "resetTimer(" + tm.group(1) + ");"

    # Vorhandene Buttons im Abschnitt klassifizieren.
    def is_loes(oc, label):
        t = (oc + " " + label).lower()
        return ("loesung" in t) or ("lösung" in t)

    def is_reset(oc, label):
        t = (oc + " " + label).lower()
        return ("reset" in t) or ("neustart" in t) or ("neu starten" in t)

    new_env = env
    have_loes = have_reset = False
    for m in BTN_RE.finditer(env):
        oc, label = m.group(1), m.group(2)
        if is_loes(oc, label) and not have_loes:
            new_env = new_env.replace(m.group(0), _loes_btn_html(), 1)
            have_loes = True
        elif is_reset(oc, label) and not have_reset:
            new_env = new_env.replace(m.group(0), _reset_btn_html(timer_call), 1)
            have_reset = True

    missing = []
    if not have_loes:
        missing.append(_loes_btn_html())
    if not have_reset:
        missing.append(_reset_btn_html(timer_call))
    if missing:
        block = "".join(missing)
        br = new_env.find('class="btn-row"')
        if br >= 0:
            close = new_env.find(">", br)
            new_env = new_env[:close + 1] + block + new_env[close + 1:]
        else:
            # Neue Steuerzeile direkt vor der Wortbank (= Ende von env).
            new_env = new_env + '<div style="display:flex;gap:8px;margin:0 0 14px;">' + block + "</div>\n    "

    return s[:sec_start] + new_env + s[i:], "ok"


def process(path):
    s = io.open(path, encoding="utf-8").read()
    s2, status = ensure_buttons(s)
    if status == "ok" and s2 != s:
        io.open(path, "w", encoding="utf-8").write(s2)
    return status


if __name__ == "__main__":
    for p in sys.argv[1:]:
        print(process(p), "<-", p.split("/")[-1])
