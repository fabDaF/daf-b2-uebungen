# fabDaF — Manifest (Übersicht)

> **Automatisch generiert aus `MANIFEST.yaml`** am 2026-07-04 13:47. Diese Datei nicht direkt editieren — YAML ändern und `python3 scripts/render_manifest.py` erneut laufen lassen.

Deutsch als Fremdsprache — Unterrichtsmaterialien und interaktive Übungen (Niveau A1–C2)

**Projekt-Root:** `~/Cowork/Projekte/fabDaF`  
**Manifest-Version:** 1

## Grundregeln der Struktur

**one_repo_per_level** — Pro Niveau (A1, A2, B1, B2, C1) existiert genau EIN Repo. Niemals parallele Versionen.

**no_parallel_working_copies** — Keine Ordner wie 'X.1 NEU', 'X.2', 'Kopie' für dasselbe Niveau. Stattdessen Git-Branches oder Archiv.

**archive_is_frozen** — daf-archiv darf nur noch erweitert, nicht mehr verändert werden. Inhalt ist historisch.

**dashboards_point_to_manifest_repos** — Jede basis-URL in einem dashboard.html MUSS auf ein Repo zeigen, das in diesem Manifest als active/materialien/archive gelistet ist.

**no_secrets_in_remote_urls** — Remote-URLs im Manifest enthalten NIE PATs oder Tokens. Die echten URLs in .git/config können PATs enthalten, aber das Manifest bleibt sauber.

## Repos im Überblick

| Schlüssel | Rolle | Niveau | Lokaler Pfad | Dashboard-URL | Pages |
|---|---|---|---|---|---|
| `daf-a1-uebungen` | Aktives Niveau | A1 | `htmlS/A1.1 NEW` | [a1.daf.frankburkert-daf.de](https://a1.daf.frankburkert-daf.de/) | ✓ |
| `daf-a2-uebungen` | Aktives Niveau | A2 | `htmlS/A2.1` | [a2.daf.frankburkert-daf.de](https://a2.daf.frankburkert-daf.de/) | ✓ |
| `daf-b1-uebungen` | Aktives Niveau | B1 | `htmlS/B1.1` | [b1.daf.frankburkert-daf.de](https://b1.daf.frankburkert-daf.de/) | ✓ |
| `daf-b2-uebungen` | Aktives Niveau | B2 | `.` | [daf.frankburkert-daf.de](https://daf.frankburkert-daf.de/) | ✓ |
| `daf-c1-uebungen` | Aktives Niveau | C1 | `htmlS/C1` | [c1.daf.frankburkert-daf.de](https://c1.daf.frankburkert-daf.de/) | ✓ |
| `daf-materialien` | Materialien | — | `daf-materialien` | [materialien.daf.frankburkert-daf.de](https://materialien.daf.frankburkert-daf.de/) | ✓ |
| `daf-architektur` | Architektur | — | `htmlS/Architektur` | [architektur.daf.frankburkert-daf.de](https://architektur.daf.frankburkert-daf.de/) | ✓ |
| `daf-lueckentexte` | Spezial | — | `htmlS/Lückentexte Mattmüller` | [lueckentexte.daf.frankburkert-daf.de](https://lueckentexte.daf.frankburkert-daf.de/) | ✓ |
| `daf-archiv` | Archiv | — | `daf-archiv` | — | ✓ |
| `A1-vokabeltrainer` | Spezial | A1 | `None` | — | ✗ (offen) |
| `daf-vertragssprache-uebungen` | Privatschüler | — | `schueler/privat-1` | [vertrag.daf.frankburkert-daf.de](https://vertrag.daf.frankburkert-daf.de/) | ✓ |

## Details pro Repo

### `daf-a1-uebungen`

_Aktive A1-Lektionen (ehem. A1-Einstieg + A1 + A1.2 NEW konsolidiert am 2026-04-10)_

- **Lokal:** `htmlS/A1.1 NEW`
- **Remote:** https://github.com/fabDaF/daf-a1-uebungen.git
- **GitHub Pages:** aktiv unter https://a1.daf.frankburkert-daf.de/
- **Dashboard basis:** `https://a1.daf.frankburkert-daf.de/`
- **Erwartung:** ≥190 tracked files, ≥180 HTML

### `daf-a2-uebungen`

_Aktive A2-Lektionen (A2.1 + A2.2 konsolidiert am 2026-04-10; 2026-04-29 Backup-Cleanup: 26 .backup.html + 2 alte Dashboards entfernt)_

- **Lokal:** `htmlS/A2.1`
- **Remote:** https://github.com/fabDaF/daf-a2-uebungen.git
- **GitHub Pages:** aktiv unter https://a2.daf.frankburkert-daf.de/
- **Dashboard basis:** `https://a2.daf.frankburkert-daf.de/`
- **Erwartung:** ≥150 tracked files, ≥100 HTML

### `daf-b1-uebungen`

_Aktive B1-Lektionen (B1.1 als Master; B1.2/B1.3 am 2026-04-10 verworfen, nur Grammatik übernommen)_

- **Lokal:** `htmlS/B1.1`
- **Remote:** https://github.com/fabDaF/daf-b1-uebungen.git
- **GitHub Pages:** aktiv unter https://b1.daf.frankburkert-daf.de/
- **Dashboard basis:** `https://b1.daf.frankburkert-daf.de/`
- **Erwartung:** ≥170 tracked files, ≥165 HTML

### `daf-b2-uebungen`

_Aktive B2-Lektionen (Root-Repo des Projekts; trägt auch MANIFEST.yaml). Zusätzlich beherbergt dieses Repo unter htmlS/C2/ den C2-Lektionsbereich (siehe sub_areas + Sektion virtual_areas)._

- **Lokal:** `.`
- **Remote:** https://github.com/fabDaF/daf-b2-uebungen.git
- **GitHub Pages:** aktiv unter https://daf.frankburkert-daf.de/
- **Dashboard basis:** `https://daf.frankburkert-daf.de/`
- **Erwartung:** ≥230 tracked files, ≥220 HTML

### `daf-c1-uebungen`

_C1-Lektionen-Repo. Im Dashboard als drei Sub-Kurse (C1.1, C1.2, C1.3) verlinkt. Lokales Sub-Repo ist seit 2026-07 vollständig (166 HTMLs)._

- **Lokal:** `htmlS/C1`
- **Remote:** https://github.com/fabDaF/daf-c1-uebungen.git
- **GitHub Pages:** aktiv unter https://c1.daf.frankburkert-daf.de/
- **Dashboard basis:** `https://c1.daf.frankburkert-daf.de/`
- **Erwartung:** ≥8 tracked files, ≥7 HTML

### `daf-materialien`

_Niveau-übergreifende Materialien: Grundlagen, Texte, Treffen, Warum wir krank werden, Wortschatz_

- **Lokal:** `daf-materialien`
- **Remote:** https://github.com/fabDaF/daf-materialien.git
- **GitHub Pages:** aktiv unter https://materialien.daf.frankburkert-daf.de/
- **Dashboard basis:** `https://materialien.daf.frankburkert-daf.de/`
- **Erwartung:** ≥40 tracked files, ≥40 HTML

### `daf-architektur`

_Architektur-Material für Privatschüler:innen (Kap13-Entwurfsplanung etc.)_

- **Lokal:** `htmlS/Architektur`
- **Remote:** https://github.com/fabDaF/daf-architektur.git
- **GitHub Pages:** aktiv unter https://architektur.daf.frankburkert-daf.de/
- **Dashboard basis:** `https://architektur.daf.frankburkert-daf.de/`
- **Erwartung:** ≥7 tracked files, ≥7 HTML

### `daf-lueckentexte`

_Lückentext-Übungen nach Mattmüller-Methode_

- **Lokal:** `htmlS/Lückentexte Mattmüller`
- **Remote:** https://github.com/fabDaF/daf-lueckentexte.git
- **GitHub Pages:** aktiv unter https://lueckentexte.daf.frankburkert-daf.de/
- **Dashboard basis:** `https://lueckentexte.daf.frankburkert-daf.de/`
- **Erwartung:** ≥10 tracked files, ≥10 HTML

### `daf-archiv`

_Historische Kopien und verworfene Versionen (B1/B2 Grammatik-Kopien, Löschbar-Ordner). FROZEN._

- **Lokal:** `daf-archiv`
- **Remote:** https://github.com/fabDaF/daf-archiv.git
- **GitHub Pages:** aktiv unter https://fabdaf.github.io/daf-archiv/
- **Erwartung:** ≥30 tracked files, ≥30 HTML

### `A1-vokabeltrainer`

_Standalone-Vokabeltrainer mit Text-to-Speech-Sprachausgabe fuer das A1-Niveau. 198 Commits seit Projektstart, letzter Commit 2025-07-14. Hosting: Netlify._

- **Lokal:** `None`
- **Remote:** https://github.com/fabDaF/A1-vokabeltrainer.git
- **GitHub Pages:** ⚠ noch nicht aktiv
- **Erwartung:** ≥1 tracked files

### `daf-vertragssprache-uebungen`

_Privatschüler-Material zu Vertragssprache, Komposita/FVG und Geschäftskommunikation auf B2/C1-Niveau (Anwendungsbereich Warenkreditversicherung). Am 2026-04-28 als Nachfolger des alten daf-wkv-uebungen-Repos angelegt — frische Git-History ohne Firmenidentifikatoren oder Schülernamen. Dashboard-Eintrag neutral, ohne Personen- oder Firmenbezug._

- **Lokal:** `schueler/privat-1`
- **Remote:** https://github.com/fabDaF/daf-vertragssprache-uebungen.git
- **GitHub Pages:** aktiv unter https://vertrag.daf.frankburkert-daf.de/
- **Dashboard basis:** `https://vertrag.daf.frankburkert-daf.de/`
- **Erwartung:** ≥3 tracked files, ≥3 HTML

## Verworfene Repos

Diese Repos existierten historisch, sind aber nicht mehr Teil der aktiven Struktur. Der verify-Skript warnt, falls sie lokal wieder auftauchen.

| Name | Ersetzt durch | Grund |
|---|---|---|
| `daf-a2-2-uebungen` | `daf-a2-uebungen` | A2.2 wurde in A2.1 konsolidiert |
| `daf-grundlagen` | `daf-materialien` | Grundlagen wurde Teil von daf-materialien |
| `daf-a1-2-uebungen` | `daf-a1-uebungen` | A1.2 NEW wurde als obsolet verworfen |
| `daf-b1-2-uebungen` | `daf-b1-uebungen` | B1.2 wurde als obsolet verworfen (B1.1 war aktueller) |
| `daf-b1-3-uebungen` | `daf-b1-uebungen` | B1.3 wurde als obsolet verworfen (B1.1 war aktueller) |

---

## Verwendung

**Prüfen:**

```bash
./scripts/verify_manifest.sh        # kurze Ausgabe
./scripts/verify_manifest.sh -v     # verbose
./scripts/verify_manifest.sh --json # JSON für Automatisierung
```

**Diese Übersicht neu generieren (nach YAML-Änderung):**

```bash
python3 scripts/render_manifest.py
```
