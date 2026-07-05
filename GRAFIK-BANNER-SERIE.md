# Stil-C-Banner-Serie — Briefing für die ausführende KI

Stand: 2026-07-05 · Auftraggeber: Frank Burkert · Verfasst von der Pilot-Session
(Referenz-Lektion: `htmlS/B1.1/DE_B1_1027X-naturkatastrophen.html`, von Frank abgenommen)

Dieses Dokument ist das vollständige Briefing für die Banner-Serie über ~750
Lektionen. Es ist modellunabhängig geschrieben. Lies es KOMPLETT, bevor du die
erste Datei anfasst. Bei Widerspruch zu Skills gilt: CLAUDE.md > dieses Dokument >
Skill-Texte.

## 0. Der Anspruch (Franks Worte)

„Geniale Kreativität, kunstvoll, besonders originell. Dem Blick wirklich anziehend
und stolz darüber empfindend, diese Lektion im eigenen Leben zu haben."

Das ist die Messlatte. Ein Banner, das nur „okay" ist, ist nicht fertig. Die
Pilot-Banner brauchten je 2–3 Iterationsrunden mit Render-Blick — plane das ein.
Du bist hier nicht Fließbandarbeiter, sondern Illustrator mit Systemvorgaben.

## 1. Die verbindlichen Regeln (nicht verhandelbar)

1. **Pro Lektion bleiben mindestens ZWEI echte Fotos** als Tab-Banner erhalten:
   eines ein **Porträt** (Mensch erkennbar), eines ein **Nicht-Porträt** (Sache,
   Landschaft, Szene). Gibt es in der Lektion kein Porträt-Foto, bleiben die zwei
   besten Nicht-Porträts — und du vermerkst es im Bericht (KEINE neuen Pexels-
   Bilder erfinden oder raten, niemals!).
2. **A1-Lektionen sind tabu**: Dort bleiben ALLE Fotos. Kein einziges A1-Banner
   wird ersetzt.
3. **Der Genus-Tab behält sein Banner** (gemeinsames Genus-SVG bzw. Bestand).
4. **Fotos und Papierschichten werden NIE vermischt** — ein Tab hat entweder ein
   Foto ODER ein Stil-C-SVG, keine Collagen.
5. **Porträt-Regel**: Das behaltene Porträt muss das ganze Gesicht (mit Augen) im
   sichtbaren Crop-Band zeigen (`object-fit: cover`, max-height 180px). Wenn die
   Augen abgeschnitten wären: `style="object-position: top"` setzen (nur an diesem
   Banner, nie global). `scripts/check_banner_faces.py` ist das Gate.
6. **Duplikate raus**: Zeigen zwei Foto-Banner fast dasselbe Motiv (z. B. zweimal
   Hurrikan-Satellitenbild), überlebt nur das stärkere.
7. **daf-archiv/, backup/, schueler/, dashboard-Dateien: niemals anfassen.**

## 2. Stil C — die Form-Spezifikation

- **Format:** `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 200" role="img" aria-label="…deutscher Alt-Text…">`
  — 1200×200, breiter als die Crop-Box: der Browser beschneidet nur die SEITEN,
  vertikal bleibt alles sichtbar. Kernmotive deshalb in x ∈ [150, 1050] halten.
- **Palette (ausschließlich):** Lila-Rampe `#EEEDFE → #CECBF6 → #AFA9EC → #7F77DD
  → #534AB7 → #3C3489 → #26215C` plus **genau EIN Akzent** `#f3c46a` (Bernstein)
  pro Banner — Sonne, Mond, ein erleuchtetes Fenster, der gehobene Baustein. Nie
  mehr als ein Akzent-Element, nie andere Fremdfarben.
- **Aufbau:** Himmel hell (`#EEEDFE` als Grundrechteck), darüber 2–4 geschichtete
  Wellenbahnen, nach unten dunkler werdend (die unterste fast immer `#26215C`).
  Wellen sind asymmetrische Beziers, KEINE gleichförmige Sinuskurve.
- **Motive:** flache Silhouetten ZWISCHEN den Schichten (Tiefenwirkung), keine
  Konturen-Zeichnungen, keine Verläufe, keine Schatten, keine Texte, **niemals
  Gesichter oder Menschen**. Mikro-Details erwünscht: zwei Vögel (Doppelbogen),
  Lichtpunkte, Gischt-Punkte — sparsam.
- **Dark-Mode-fest:** Das Banner ist ein eigenständiges Bild und bleibt in beiden
  Modi identisch — die Palette funktioniert auf hell wie dunkel.
- **Einbettung:** als `data:image/svg+xml;base64,…` im `<img class="tab-banner">`,
  mit deutschem `alt`-Text. Bei Ersatz eines Fotos das alte
  `style="object-position:…"` entfernen.

## 3. Die Kompositions-Grammatik (das eigentliche Handwerk)

Jedes Banner erzählt **Lektionsthema × Tab-Funktion** in EINER Silhouetten-Idee:

- Der Vokabular-/Vorentlastungs-Tab bekommt das Panorama des Themas.
- Übungs-Tabs bekommen eine METAPHER der Tätigkeit im Gewand des Themas:
  Satzbau = Aufbauen/Stapeln/Konstruieren · Zuordnung = Schützen/Sammeln/Paare ·
  Lückentext = Fehlen/Füllen · Schreiben = die Feder, die die Szene selbst zeichnet.
- Die stärksten Pilot-Ideen waren doppelbödig: Beim Schreiben-Banner existiert die
  vorderste Welle nur LINKS der Federspitze — die Feder zeichnet die Landschaft.
  DIESES Niveau ist gemeint. Suche pro Lektion mindestens eine solche Idee.
- **Nicht klonen.** Die Referenzen sind Grammatik, nicht Schablone. Gleiche
  Bausteine (Wellen, Sonne) dürfen wiederkehren, die Motividee pro Lektion muss
  eigen sein.

**Referenz-Bibliothek** (geprüft, von Frank abgenommen): `scripts/banner-stil-c/`
- `referenz-vulkan-panorama.svg` — Panorama-Typ: Sonne+Halo, Bergstaffelung, Rauchspirale, Vögel
- `referenz-schirm-haeuser.svg` — Schutz-Metapher: Schirm mit Wellenkante, Häuser mit EINEM Akzentfenster-Trio, Regenstriche
- `referenz-kran-bausteine.svg` — Aufbau-Metapher: Kran mit Ausleger+Gegengewicht, gestapelte Rampe-Blöcke, Akzent = gehobener Stein, Mondsichel
- `referenz-feder-welle.svg` — die doppelbödige Metapher: Federkiel, dessen Spitze das Ende der gefüllten Welle IST; Tintentropfen

## 4. Qualitäts-Checkliste (Fehler, die im Piloten real passierten)

Vor jeder Abnahme das gerenderte PNG ANSEHEN und fragen:

1. **1-Sekunden-Test:** Erkennt man die Silhouette sofort? (Der Pilot-Kran las
   sich zuerst als TISCH, der Mond als Golfball, der Schirm als Brückenbögen —
   alles erst im Render sichtbar geworden.)
2. Liegt das Kernmotiv im sichtbaren Band (x 150–1050) und wird nichts Wichtiges
   vertikal knapp?
3. Genau EIN Bernstein-Akzent? Palette eingehalten?
4. Schwebt nichts unmotiviert (Pilot: Wellen-„Band" ohne Füllung wirkte lose —
   Wellen immer bis zum Boden füllen, spätere Schichten überlappen lassen)?
5. Wirkt es komponiert oder dekoriert? (Drei zufällige Elemente = dekoriert.
   Ein Motiv mit Spannung + zwei stille Details = komponiert.)
6. Kein Mensch, kein Gesicht, kein Text im SVG?

Wenn IRGENDEIN Punkt zweifelhaft ist: überarbeiten, neu rendern, neu ansehen.
Nichts ausliefern, was du nicht selbst gesehen hast.

## 5. Workflow pro Lektion

```bash
# 0) WIP-Schutz — Datei mit fremdem Arbeitsstand NIE anfassen:
git diff HEAD --quiet -- DATEI.html || überspringen+berichten
```

1. **Inventar:** Banner extrahieren und Fotos ansehen:
   ```python
   import re, base64
   h = open(f, encoding='utf-8').read()
   for i, m in enumerate(re.finditer(r'<img class="tab-banner"[^>]*src="data:image/(jpeg|svg\+xml);base64,([^"]+)"', h)):
       open(f'/tmp/banner_{i}.' + ('jpg' if m.group(1)=='jpeg' else 'svg'), 'wb').write(base64.b64decode(m.group(2)))
   ```
   Jedes JPG mit dem Read-Tool ANSEHEN. Tab-Zuordnung über die Section-Reihenfolge.
2. **Foto-Wahl:** bestes Porträt + bestes Nicht-Porträt (Regeln §1). Rest → SVG.
3. **Entwurf:** pro Ersatz-Tab ein SVG nach §2/§3. Rendern:
   ```bash
   pip install cairosvg --break-system-packages  # einmalig
   python3 -c "import cairosvg; cairosvg.svg2png(url='x.svg', write_to='x.png', output_width=900)"
   ```
   PNG mit Read ansehen → Checkliste §4 → iterieren.
4. **Einbau:** Base64-URI ins `<img class="tab-banner">` des richtigen Tabs,
   deutscher alt-Text, altes object-position raus.
5. **Verifikation:** `node`-vm.Script-Parse aller `<script>`-Blöcke; dann
   `python3 scripts/check_all.py DATEI.html` — muss grün sein (ohne SKIP_CHECKS!).
6. **Abnahme-Ablage** (Phase 1, siehe §6): PNGs aller neuen Banner der Lektion in
   den Abnahme-Ordner legen, NICHT committen.
7. **Commit** (erst nach Freigabe bzw. in Phase 2): aus dem jeweiligen Unterrepo,
   `bash <ROOT>/scripts/safe-commit.sh "Banner Stil C: LEKTIONSCODE (n SVG, 2 Fotos behalten)" DATEI.html`
   — nur benannte Dateien, nie git add -A, kein Write-Tool auf .git/.

## 6. Phasenmodell & Abnahme

- **Phase 1 — Pilotbatch B1 Einheit 1** (1011X, 1012G, 1013R, 1014X, 1015G,
  1016R, 1017X, 1018S): KEINE Commits. Alle gerenderten Banner als PNG in den
  Abnahme-Ordner (`outputs`-Verzeichnis der Session), dazu pro Lektion drei
  Zeilen Bericht: gewählte Fotos (warum), Motividee pro SVG-Tab, Zweifel.
  Frank bzw. die Hauptsession nimmt ab; erst danach wird committet.
- **Phase 2 — Serienlauf** (nach bestandener Phase 1): committen erlaubt,
  Einheit für Einheit, Repo für Repo (B1 → B2 → A2 → C1 → …, A1 nie).
  Stichproben-Abnahme: jede fünfte Lektion legt weiterhin PNGs zur Sicht vor.
- **Bericht pro Batch:** Lektionen fertig / übersprungen (Grund) / Foto-Bilanz
  (wie viele Porträts fehlten) / Gates grün / Pushes verifiziert (ls-remote).

## 7. Bekannte Fallen

- 1011X hat bereits selbstgebaute Reise-SVGs von der Gesichter-Kampagne — dort
  prüfen, ob sie durch Stil C ersetzt werden sollen (ja, wenn sie nicht dem
  §2-Kanon entsprechen), und ob überhaupt noch Fotos vorhanden sind.
- Sanduhr-Effekt bei `git checkout --`: scheitert am Mount. Wiederherstellen
  IMMER mit `git show HEAD:DATEI > DATEI`.
- Pages-Deploys springen nach Pushes gelegentlich nicht an — bei stale Live-Stand
  leerer Retrigger-Commit (bekanntes Muster, siehe Memory).
- `check_banner_faces.py` braucht opencv; fehlt es, überspringt es sich selbst —
  das entbindet nicht von Regel §1.5.
