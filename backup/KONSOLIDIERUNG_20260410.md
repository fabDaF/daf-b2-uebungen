# Konsolidierung am 2026-04-10

Nach der B2.1-Katastrophe vom Morgen wurde die gesamte `fabDaF`-Struktur „vom Kopf auf die Füße gestellt". Ziel: weniger parallele Repos, eindeutige Zuordnung, keine Konflikte mehr.

## Ausgangslage

- **11 parallele Git-Repos** (fabDaF-Root + 10 Unterordner, einige davon mehrfach dasselbe Remote geklont)
- **275 ungetrackte HTML-Dateien** in verschiedenen Ordnern
- **31 Konflikte** zwischen Root-Clone und Sub-Clones von `daf-b2-uebungen` (B2.1 / B2.2 / Grammatik)
- **Dashboard-URLs** zeigten auf Repos, die nach der Konsolidierung gar nicht mehr existierten

## Endstand: 9 Repos mit klarer Zuordnung

| Ordner                         | Remote                 | HTML (top-level) |
|--------------------------------|------------------------|------------------|
| `(root)/` = `fabDaF`           | `daf-b2-uebungen`      | 157              |
| `htmlS/A1.1 NEW`               | `daf-a1-uebungen`      | 189              |
| `htmlS/A2.1`                   | `daf-a2-uebungen`      | 145              |
| `htmlS/B1.1`                   | `daf-b1-uebungen`      | 170              |
| `htmlS/Architektur`            | `daf-architektur`      | 7                |
| `htmlS/C1`                     | `daf-c1-uebungen`      | 7                |
| `htmlS/Lückentexte Mattmüller` | `daf-lueckentexte`     | 10               |
| `daf-materialien/` (NEU)       | `daf-materialien`      | (42 gesamt)      |
| `daf-archiv/` (NEU)            | `daf-archiv`           | (31 gesamt)      |

Alle 9 lokalen HEADs sind identisch mit `origin/main`.

## Phase für Phase

### Phase B2 (vor dem Hauptlauf)
- `htmlS/B2/B2.1`, `htmlS/B2/B2.2`, `htmlS/B2/Grammatik`: 4 parallele Clones desselben Remotes `daf-b2-uebungen`. 31 Konflikte per Skript aufgelöst (größte Datei gewinnt), 50 bisher ungetrackte B2.3-Dateien in den Root-Clone migriert. 3 Sub-Clones gelöscht.
- 5 Dateien aus `htmlS/B2 Grammatik` in den Root-Clone übernommen.

### Phase A1 → `daf-a1-uebungen`
- `A1-Einstieg` (70 HTML): 69 Dateien übernommen, 1 verworfen (A1.1 NEW hatte neuere Version von `das-perfekt-uebungen.html`)
- `A1` (2 HTML): beide übernommen
- `A1.2 NEW` (25 HTML): komplett verworfen — alle Dateien neuer & größer in A1.1 NEW vorhanden
- **Merge-Konflikt mit Remote** gelöst: Local „Zwischenstand" hatte Alt-Modifikationen an `1011V-hallo.html` und `1123G-die-modalverben.html`, Remote hatte neuere Claude-Code-Fixes. Reset auf origin/main, dann nur die neuen Files (69+2) + `.backup`-Dateien erneut angewendet.

### Phase A2 → `daf-a2-uebungen`
- `A2.2` (56 HTML): alle 56 Dateien übernommen, 0 Konflikte mit A2.1.
- A2.2-Ordner + ursprüngliches Remote `daf-a2-2-uebungen` sind obsolet. (Remote existiert noch, ist aber nicht mehr verlinkt.)

### Phase B1 → `daf-b1-uebungen`
- `B1.2` (50 HTML): komplett verworfen — 18 byte-identisch mit B1.1, 26 in B1.1 neuer, 6 zwar größer in B1.2 aber dort veraltet (B1.1 wurde seitdem in Claude Code nachgezogen)
- `B1.3` (50 HTML): komplett verworfen — alle 47 Konflikte gewonnen von B1.1
- `B1 Grammatik` (20 HTML): alle 20 Dateien übernommen (keine Konflikte).

### Phase B2 Grammatik → `daf-b2-uebungen` (Root)
- 5 Dateien aus `htmlS/B2 Grammatik` ins Root-Repo integriert.

### Neues Repo `daf-materialien`
Niveau­übergreifende Materialien in eigenes Repo ausgegliedert:
- `Grundlagen/` (Grammatik + Kollokationen)
- `Texte und Lesen/` (10 HTML)
- `Treffen vereinbaren/` (5 HTML)
- `Warum wir krank werden/` (5 HTML)
- `Wortschatz/` (2 HTML)

Neues GitHub-Repo via Chrome-MCP erstellt, initialer Push mit 125 Dateien.

### Neues Repo `daf-archiv`
Sicherheitsanker für Alt-Ballast:
- `B1 Grammatik Kopie/`
- `B2 Grammatik Kopie/`
- `Löschbar/`

Kann langfristig ohne Risiko gelöscht werden.

### Dashboard-URL-Update
Beide Dashboard-Kopien (`htmlS/A2.1/dashboard.html` + `htmlS/dashboard.html`) aktualisiert:
- `basis: daf-a2-2-uebungen` → `daf-a2-uebungen`
- `basis: daf-grundlagen` → `daf-materialien`

Die `file:`-Pfade bleiben unverändert (z.B. `Grundlagen/Grammatik/…`, `Texte und Lesen/…`), da die Ordnerstruktur innerhalb von `daf-materialien` erhalten blieb.

## Sicherungen

Drei Snapshots existieren als Sicherheitsnetz, alle in
`~/Cowork/Projekte/Archiv fabDaf/AUTOMATISCHE_BACKUPS/`:

- `fabDaF_NOTFALL_20260410_0931.tar.gz` (2.0 GB) — ursprüngliche Rettung vom Morgen
- `fabDaF_VOR_KONSOLIDIERUNG_20260410_0955.tar.gz` (2.0 GB) — direkt vor Phase-1
- `fabDaF_PHASE2_20260410_1021.tar.gz` (2.0 GB) — nach B2.1/B2.2 Merge, vor A1/A2/B1

## Was Frank noch tun sollte

1. **GitHub Pages für `daf-materialien` und `daf-archiv` aktivieren** (Settings → Pages → main branch → /), damit die Dashboard-Links funktionieren.
2. **Altes Repo `daf-a2-2-uebungen` ggf. auf GitHub archivieren** (Settings → Danger Zone → Archive). Es ist nicht mehr verlinkt, aber existiert noch.
3. **Altes Repo `daf-grundlagen` ebenfalls archivieren**, falls es auf GitHub existiert.
4. **launchd-Backup aktivieren** (siehe `INSTALL.md`), damit die täglichen Snapshots automatisch laufen.
5. **Kurzer Dashboard-Test**: öffne `htmlS/A2.1/dashboard.html` lokal und klick auf eine A2.2-Karte und eine Grundlagen-Karte — sie sollten auf die neuen URLs zeigen.
