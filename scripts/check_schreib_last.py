#!/usr/bin/env python3
"""check_schreib_last.py — Sicherheitsnetz: Schreibwerkstatt MUSS letzter Tab sein.

Grundsatzregel seit 2026-06-29 (CLAUDE.md): Der Schreibwerkstatt-Tab (📨 Schreiben)
steht in JEDER Lektion ganz am Ende. Dieses Skript meldet jede Datei mit einem
Schreiben-Nav-Tab, der nicht der letzte ist (Exit 1) — geeignet als Pre-Commit-Gate.

Dateien ohne Schreiben-Tab sind in Ordnung (S-/W-Sonderfälle, reine Drills etc.).

Nutzung:
    python3 scripts/check_schreib_last.py            # ganzes Repo (ohne daf-archiv)
    python3 scripts/check_schreib_last.py datei.html # einzelne Dateien
"""
import os, re, sys

# Nav-Buttons: <div|button|a class="...nav-btn...">…</…> — Tag-agnostisch beim Schließen
NAVBTN_RE = re.compile(r'<(div|button|a)\b[^>]*\bclass="[^"]*\bnav-btn\b[^"]*"[^>]*>(.*?)</\1>', re.S)

def nav_labels(s):
    out = []
    for m in NAVBTN_RE.finditer(s):
        txt = re.sub(r'<[^>]+>', ' ', m.group(2))
        txt = re.sub(r'&[a-zA-Z#0-9]+;', ' ', txt)   # HTML-Entities neutralisieren
        out.append(re.sub(r'\s+', ' ', txt).strip().lower())
    return out

def offenders(paths):
    bad = []
    for p in paths:
        try:
            s = open(p, encoding='utf-8', errors='replace').read()
        except Exception:
            continue
        labels = nav_labels(s)
        if len(labels) < 2:
            continue
        si = [i for i, l in enumerate(labels) if 'schreib' in l]
        if not si:
            continue                       # kein Schreiben-Tab → ok
        if si[-1] != len(labels) - 1:
            bad.append((p, si[-1], len(labels) - 1))
    return bad

def collect_repo():
    out = []
    for dp, dn, fn in os.walk('.'):
        if '/daf-archiv' in dp or '/.git' in dp:
            continue
        for f in fn:
            if f.endswith('.html') and '.bak' not in f:
                out.append(os.path.join(dp, f))
    return out

if __name__ == '__main__':
    args = sys.argv[1:]
    files = args if args else collect_repo()
    bad = offenders(files)
    if bad:
        print(f"✗ {len(bad)} Datei(en) mit Schreibwerkstatt-Tab, der NICHT letzter ist "
              f"(CLAUDE.md: Schreiben ist immer der letzte Tab):")
        for p, pos, last in bad:
            print(f"    {p}  (Schreiben an Position {pos}, letzter Tab ist {last})")
        print("\nFix: Schreiben-Tab ans Ende verschieben (relative Reihenfolge der "
              "übrigen Tabs beibehalten); danach JS-Parse + Browser-Stichprobe.")
        sys.exit(1)
    print(f"✓ Alle {len(files)} geprüften Dateien haben den Schreibwerkstatt-Tab "
          f"am Ende (oder keinen Schreiben-Tab).")
    sys.exit(0)
