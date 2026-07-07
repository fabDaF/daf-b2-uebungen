#!/usr/bin/env python3
"""inject_banner_pool.py — Stil-C-Banner aus dem Familien-Pool einspielen.

Zwischenlösung der Banner-Serie (Frank, 2026-07-07): KEINE Neukomposition,
Wiederverwendung der abgenommenen Phase-1-SVGs — aber nach TAB-FUNKTION,
nie nach Lektionsthema (Pool: scripts/banner-stil-c/pool/ + katalog.json).

Regeln:
- Foto-Muster bleibt: Fotos auf Vorentlastung/Vokabular/Lesetext-Tabs werden
  BEHALTEN (Ziel: 2 Fotos pro Lektion, Porträt + Nicht-Porträt) — A1 wird
  grundsätzlich NICHT angefasst (A1 = komplett Fotos, Franks Regel).
- Genus-Tab wird nie angefasst (eigener geteilter Banner).
- Bestehende SVG-Banner bleiben (idempotent).
- Foto-Banner auf Tabs MIT Pool-Familie → ersetzt (stabile Rotation pro Datei,
  keine Familien-Dublette innerhalb einer Datei).
- Tabs ohne Familie behalten ihr Foto (Bericht: KEIN-POOL).

Aufruf: python3 scripts/inject_banner_pool.py DATEI.html [...]
Bericht pro Datei: ersetzt=N fotos-behalten=N kein-pool=N
"""
import base64
import hashlib
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
POOL = os.path.join(HERE, 'banner-stil-c', 'pool')
KATALOG = json.load(open(os.path.join(POOL, 'katalog.json'), encoding='utf-8'))
FAMILIEN = {}
for k in sorted(KATALOG, key=lambda x: x['file']):
    if k['familie'] != 'exklusiv':
        FAMILIEN.setdefault(k['familie'], []).append(k)

TAB_MAP = [
    (('genus',), 'GENUS'),
    (('lückentext', 'lueckentext'), 'lueckentext'),
    (('satzbau', 'sätze bauen', 'saetze bauen'), 'satzbau'),
    (('schreib',), 'schreiben'),
    (('wortschatz',), 'wortschatz'),
    (('multiple', 'quiz', 'wähle', 'formen', 'verständnis', 'fragen', 'richtig'), 'mc'),
    (('sprechen', 'diskussion', 'dialog', 'meinung', 'gespräch'), 'sprechen'),
]
FOTO_KEEP = ('vorentlastung', 'vokabular', 'lesetext', 'geschichte', 'text',
             'lesen', 'schlüsselwörter', 'wörter')

IMG_RE = re.compile(r'<img[^>]*class="tab-banner"[^>]*>')
NAVBTN_RE = re.compile(
    r'<(button|div)\s([^>]*class="nav-btn[^"]*"[^>]*)>(.*?)</\1>', re.DOTALL)
ONCLICK_RE = re.compile(r'show(?:Section|Tab)\(\s*[\'"]?([a-z0-9]+)[\'"]?\s*\)')

ID_DIREKT = {'genus': 'GENUS', 'schreib': 'schreiben'}


def klassifiziere(text):
    t = text.lower()
    for kws, fam in TAB_MAP:
        if any(k in t for k in kws):
            return fam
    if any(k in t for k in FOTO_KEEP):
        return 'FOTO'
    return 'UNBEKANNT'


def nav_funktionen(s):
    """Tab-Funktion je Section-Schlüssel aus den Nav-Buttons.
    Schlüssel = Argument von showSection/showTab (Zahl oder Name),
    passend zur Section-ID sec-<schlüssel>."""
    karte = {}
    for m in NAVBTN_RE.finditer(s):
        attrs, inhalt = m.group(2), m.group(3)
        o = ONCLICK_RE.search(attrs)
        if not o:
            continue
        label = re.sub(r'<[^>]+>', ' ', inhalt)
        karte[o.group(1)] = klassifiziere(label)
    karte.update({k: v for k, v in ID_DIREKT.items()})
    return karte


def svg_tag(eintrag):
    raw = open(os.path.join(POOL, eintrag['file']), 'rb').read()
    b64 = base64.b64encode(raw).decode()
    return ('<img class="tab-banner" src="data:image/svg+xml;base64,' + b64 +
            '" alt="' + eintrag['alt'] + '">')


def bearbeite(pfad):
    s = open(pfad, encoding='utf-8').read()
    funktionen = nav_funktionen(s)
    # Sections in DOM-Reihenfolge schneiden; Schlüssel aus der sec-ID lesen.
    # Fallback für ID-lose Generationen (positionales showSection über
    # querySelectorAll('.section')): Sections per Klasse schneiden,
    # Schlüssel = laufende Position.
    treffer = list(re.finditer(r'id="sec-([a-z0-9]+)"', s))
    if len(treffer) < 3:
        klassen = list(re.finditer(r'<(?:div|section)[^>]*class="(?:section|tab-content)[" ]', s))
        if len(klassen) >= 3:
            class _T:
                def __init__(self, m, i): self._m, self._i = m, i
                def start(self): return self._m.start()
                def group(self, n): return str(self._i)
            treffer = [_T(m, i) for i, m in enumerate(klassen)]
    if not treffer or not funktionen:
        print(f"SKIP {pfad} | keine sec-Sections oder keine Nav-Buttons")
        return
    grenzen = [m.start() for m in treffer] + [len(s)]
    indizes = [m.group(1) for m in treffer]

    # Foto-Verteilung (Frank, 2026-07-07): NICHT beide Fotos vorn — erstes
    # Foto auf dem ersten Tab, das zweite möglichst in der TAB-MITTE: ein
    # Family-Tab mit Foto, dessen Position der Mitte am nächsten liegt,
    # behält sein Foto (hash-stabile Wahl bei Gleichstand).
    hat_foto = []
    for i in range(len(grenzen) - 1):
        teil = s[grenzen[i]:grenzen[i + 1]]
        hat_foto.append(any('svg+xml' not in t for t in IMG_RE.findall(teil)))
    mitte_pos = None
    kandidaten_mitte = [i for i in range(1, len(indizes))
                        if hat_foto[i] and funktionen.get(indizes[i]) in FAMILIEN]
    if kandidaten_mitte:
        ziel = (len(indizes) - 1) / 2.0
        naechste = sorted(kandidaten_mitte, key=lambda i: abs(i - ziel))
        beste = [i for i in naechste if abs(i - ziel) == abs(naechste[0] - ziel)]
        h = int(hashlib.sha1(os.path.basename(pfad).encode()).hexdigest(), 16)
        mitte_pos = beste[h % len(beste)]

    ersetzt = fotos = kein_pool = 0
    benutzt = set()
    for i in range(len(grenzen) - 1):
        teil = s[grenzen[i]:grenzen[i + 1]]
        fam = funktionen.get(indizes[i], 'UNBEKANNT')
        if i == 0 or i == mitte_pos:
            fam = 'FOTO-SLOT'  # erster Tab + Mitte behalten ihr Foto
        for tag in IMG_RE.findall(teil):
            if 'data:image/svg+xml' in tag:
                continue  # schon Stil C / Genus
            if fam in ('GENUS',):
                continue
            if fam == 'FOTO-SLOT':
                fotos += 1
                continue
            if fam == 'FOTO' and 'lesen' in FAMILIEN:
                fam = 'lesen'  # zweiter Lese-/Vorentlastungs-Tab bekommt das Buch-SVG
            if fam in ('FOTO', 'UNBEKANNT') or fam not in FAMILIEN:
                if fam in ('FOTO',):
                    fotos += 1
                else:
                    kein_pool += 1
                continue
            mitglieder = [m for m in FAMILIEN[fam] if m['file'] not in benutzt] or FAMILIEN[fam]
            idx = int(hashlib.sha1((os.path.basename(pfad) + fam).encode()).hexdigest(), 16) % len(mitglieder)
            wahl = mitglieder[idx]
            benutzt.add(wahl['file'])
            neu = teil.replace(tag, svg_tag(wahl), 1)
            s = s[:grenzen[i]] + neu + s[grenzen[i + 1]:]
            delta = len(neu) - len(teil)
            grenzen = [g if g <= grenzen[i] else g + delta for g in grenzen]
            teil = neu
            ersetzt += 1
    open(pfad, 'w', encoding='utf-8').write(s)
    print(f"OK {pfad} | ersetzt={ersetzt} fotos-behalten={fotos} kein-pool={kein_pool}")


if __name__ == '__main__':
    for p in sys.argv[1:]:
        bearbeite(p)
