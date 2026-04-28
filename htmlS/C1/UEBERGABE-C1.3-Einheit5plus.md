# Übergabe: C1.3 ab Einheit 5 — Pipeline läuft

**Stand:** 2026-04-29 (Folgesession nach Einheit 1) · Adressat: nächste Cowork-Session

## Stand: 33 von 50 C1.3-Lektionen fertig

**Komplett gebaut und gepushed:**
- Einheit 1 (3011G–3018S): 8/8 ✓
- Einheit 2 (3021G–3028S): 8/8 ✓
- Einheit 3 (3031G–3038S): 8/8 ✓
- Einheit 4 (3041G–3048S): 8/8 ✓
- Einheit 5: 1/8 (3051G ✓; offen: 3052X, 3053R, 3054S, 3055R, 3056S, 3057R, 3058S)
- Einheit 6 (3061G–3068S): 0/8
- Schreibwerkstatt (3071W, 3072W): 0/2

**Offen: 17 Lektionen.**

Dashboard-Blöcke `301x`, `302x`, `303x`, `304x` sind vollständig befüllt. Block `305x` muss noch angelegt werden.

## Pipeline ist erprobt — keine Setup-Mühe mehr

Die Pipeline ist bewährt:

```
/sessions/.../mnt/outputs/
├── tmpl_html.html     # 8-Tab-Template für R/X/S/W
├── tmpl_g.html        # 5-Tab-Template für G-Lektionen
├── build_lesson.py    # Generic Builder für RXSW
├── build_g.py         # Generic Builder für G
├── test_C1.js         # JSDOM-Smoke-Test (16 Checks für RXSW, 7 für G)
└── spec_NNNN.py       # Eine pro Lektion
```

**ACHTUNG bei Session-Neustart:** Diese Sandbox-Dateien werden zwischen
Sessions verworfen. Beim Wiedereinstieg müssen sie aus den fertigen
HTMLs rekonstruiert werden — am leichtesten aus DE_C1_3051G für G
und DE_C1_3048S für RXSW.

## Pipeline pro Lektion (eingespielt, 12-15 min)

```bash
cd /sessions/.../mnt/outputs

# 1. PDF lesen
pdftotext -layout "lingoda c1/C 1.3/C1_NNNNT_DE.pdf" NNNNT.txt
sed -n '40,140p' NNNNT.txt    # Inhalt überfliegen

# 2. Bilder extrahieren
mkdir -p pdf_NNNNT
pdfimages -j -p "lingoda c1/C 1.3/C1_NNNNT_DE.pdf" pdf_NNNNT/img
# Top-5 Previews:
cd pdf_NNNNT && python3 -c "..." # (siehe vorhandene Skripte)

# 3. 4-5 Bilder visuell prüfen, beste auswählen

# 4. spec_NNNN.py schreiben — Vorlagen:
#    R/X/S/W → spec_3048S.py kopieren+anpassen
#    G → spec_3051G.py kopieren+anpassen

# 5. Build + Test
python3 spec_NNNN.py
node test_C1.js DE_C1_NNNNT-slug.html  # 16/16 (RXSW) / 7/7 (G)

# 6. Commit
cd /sessions/.../mnt/fabDaF
bash scripts/safe-commit.sh "C1.3 Lektion NNNNT: <Thema>" htmlS/C1/DE_C1_NNNNT-*.html
```

## Was am Ende noch fertig zu machen ist

1. Dashboard-Blöcke `305x` und `306x` ergänzen (G→X→R→S→R→S→R→S
   pro Einheit, plus W-Schreibwerkstatt-Block `307x`).
2. Memory-Eintrag `project_c13_komplett.md` schreiben (parallel zu
   `project_c2_komplett.md`).
3. MEMORY.md-Index ergänzen.
4. Push-Ping an Frank: `curl -s -H "Title: C1.3 KOMPLETT" -H "Priority: high"
   -H "Tags: bell" -d "C1.3 fertig - alle 50 Lektionen committed.
   Bereit zur Abnahme." https://ntfy.sh/frank-claude-c46edad954`

## Inhaltliche Erkenntnisse aus Einheiten 1-4

Pro Lektion:
- **Lesetext** 800-1500 Wörter, akademisch-essayistisch, mind. 4 vocab-hl
  Markierungen aus VORENTLASTUNG-Liste.
- **Quellenangabe** im Format: <em>Quelle: Hintergrundanalyse für den
  DaF-Unterricht · C1.3 – Lektion NNNNT · nach Lingoda C1_NNNNT, frei
  erweitert · [3-5 Bezugspersonen mit Daten] · Stand April 2026</em>
- **Schreibwerkstatt:** 5 Mikroaufgaben (40-80 Wörter), nie eine große.
- **Anführungszeichen-Regex** läuft im Build automatisch.

Für G-Lektionen:
- 5-Tab-Pattern (Entdeckung, Zuordnung, Lückentext, Satzbau, Wortschatz).
- ENTDECK_BLOCK + MC_STEPS_BLOCK + REGELKARTE.
- Vorlage: spec_3051G.py.

## Konkrete erste Schritte

1. Diese Datei lesen.
2. PDF von 3052X öffnen:
   ```bash
   pdftotext -layout "lingoda c1/C 1.3/C1_3052X_DE.pdf" /tmp/3052X.txt
   head -40 /tmp/3052X.txt
   ```
3. Templates aus 3051G und 3048S rekonstruieren (siehe oben).
4. spec_3052X.py schreiben — Vorlage spec_3042X (Kommunikation).
5. Build + Test + Commit.

## Realistischer Zeitplan

Pro Lektion: 12-15 min. 17 Lektionen = ca. 4 Stunden reine Bauzeit.
Plus 30 min Setup, 30 min Dashboard-Updates, 15 min Memory + Push.
Total: ca. 5-6 Stunden. Realistisch in einer Cowork-Session abschließbar.

— Claude (Folgesession nach 28. April 2026)
