#!/usr/bin/env python3
"""
build_search_index.py  —  fabDaF Volltext-Suchindex
Scannt alle HTML-Dateien unter htmlS/ und extrahiert bereinigten Text.
Ausgabe: htmlS/search-index.json  (Schlüssel = Dateiname, Wert = Text)

Aufruf:
    python3 scripts/build_search_index.py
"""
import os
import re
import json
from pathlib import Path

ROOT  = Path(__file__).parent.parent
BASE  = ROOT / 'htmlS'
OUT   = BASE / 'search-index.json'

SKIP_FILES = {'dashboard.html', 'search-index.json'}
SKIP_DIRS  = {'node_modules', '.git', 'franks-drill'}   # Drills haben kaum Prosatext

# ──────────────────────────────────────────────
# Hilfsfunktionen
# ──────────────────────────────────────────────

def strip_tags(html: str) -> str:
    html = re.sub(r'<[^>]+>', ' ', html)
    html = re.sub(r'&amp;',  '&', html)
    html = re.sub(r'&lt;',   '<', html)
    html = re.sub(r'&gt;',   '>', html)
    html = re.sub(r'&nbsp;', ' ', html)
    html = re.sub(r'&[a-z]+;', ' ', html)
    html = re.sub(r'\s+', ' ', html)
    return html.strip()

# CSS-Klassen, deren Inhalt wir extrahieren (Lese-, Übungs-, Info-Text)
ELEMENT_PATTERNS = [
    r'class="story-text"[^>]*>([\s\S]*?)</div>',
    r'class="befund-box"[^>]*>([\s\S]*?)</div>',
    r'class="intro-box"[^>]*>([\s\S]*?)</div>',
    r'class="therapie-box"[^>]*>([\s\S]*?)</div>',
    r'class="arbeitsrecht-box"[^>]*>([\s\S]*?)</div>',
    r'class="linguistik-box"[^>]*>([\s\S]*?)</div>',
    r'class="hilfe-box"[^>]*>([\s\S]*?)</div>',
    r'class="vocab-def"[^>]*>([\s\S]*?)</div>',
    r'class="vocab-term"[^>]*>([\s\S]*?)</div>',
    r'class="schreib-karte-frage"[^>]*>([\s\S]*?)</div>',
    r'class="amdp-domain-box"[^>]*>([\s\S]*?)</div>',
    r'class="reductio-box"[^>]*>([\s\S]*?)</div>',
    r'class="standpunkt-box"[^>]*>([\s\S]*?)</div>',
    r'class="beispiel-box"[^>]*>([\s\S]*?)</div>',
    r'class="quellen-box"[^>]*>([\s\S]*?)</div>',
    r'class="fazit-box"[^>]*>([\s\S]*?)</div>',
    r'class="rf-text"[^>]*>([\s\S]*?)</div>',
]

# JS-Datenarrays, aus denen wir String-Werte extrahieren
JS_ARRAYS = [
    'VORENTLASTUNG', 'LUECKEN', 'SCHREIB_AUFGABEN',
    'WORTSCHATZ', 'RF_ITEMS', 'GENUS_DATA', 'SATZBAU',
]

def extract_js_strings(block: str) -> list[str]:
    """Extrahiert alle JS-String-Werte (einfache und doppelte Anführungszeichen)."""
    results = []
    # Einfache Anführungszeichen (ohne Escape)
    for m in re.finditer(r"'([^'\\]{4,})'", block):
        results.append(m.group(1))
    # Doppelte Anführungszeichen
    for m in re.finditer(r'"([^"\\]{4,})"', block):
        val = m.group(1)
        # Überschriften und technische Strings herausfiltern
        if not re.match(r'^[A-Z_]+$', val) and '://' not in val:
            results.append(val)
    return results

def extract_text(filepath: Path) -> str:
    try:
        raw = filepath.read_text(encoding='utf-8', errors='ignore')
    except Exception:
        return ''

    parts = []

    # 1. Seitentitel
    m = re.search(r'<title[^>]*>(.*?)</title>', raw, re.IGNORECASE)
    if m:
        parts.append(strip_tags(m.group(1)))

    # 2. Meta-Description falls vorhanden
    m = re.search(r'<meta[^>]+name="description"[^>]+content="([^"]+)"', raw, re.IGNORECASE)
    if m:
        parts.append(m.group(1))

    # 3. Strukturierte HTML-Bereiche
    for pat in ELEMENT_PATTERNS:
        for m in re.finditer(pat, raw, re.IGNORECASE):
            parts.append(strip_tags(m.group(1)))

    # 4. JS-Datenarrays
    for arr in JS_ARRAYS:
        pat = rf'var\s+{arr}\s*=\s*\[([\s\S]*?)\];'
        m = re.search(pat, raw)
        if m:
            parts.extend(extract_js_strings(m.group(1)))

    # 5. h2/h3-Überschriften (Abschnittsnamen)
    for m in re.finditer(r'<h[23][^>]*>([\s\S]*?)</h[23]>', raw, re.IGNORECASE):
        parts.append(strip_tags(m.group(1)))

    combined = ' '.join(parts)
    combined = re.sub(r'\s+', ' ', combined).strip()
    # Max. 8 000 Zeichen pro Datei (reicht für Snippets, hält Index kompakt)
    return combined[:8000]


# ──────────────────────────────────────────────
# Hauptprogramm
# ──────────────────────────────────────────────

index = {}
skipped = 0

for root, dirs, files in os.walk(BASE):
    dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
    for fname in sorted(files):
        if not fname.endswith('.html'):
            continue
        if fname in SKIP_FILES:
            continue
        fpath = Path(root) / fname
        text = extract_text(fpath)
        if text:
            index[fname] = text
        else:
            skipped += 1

with open(OUT, 'w', encoding='utf-8') as f:
    json.dump(index, f, ensure_ascii=False, separators=(',', ':'))

size_kb = OUT.stat().st_size / 1024
print(f"✓ Indexiert: {len(index)} Dateien  |  Übersprungen: {skipped}  |  Größe: {size_kb:.0f} KB")
print(f"  → {OUT}")
