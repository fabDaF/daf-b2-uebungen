# fabDaF — Manifest (Übersicht)

> **Automatisch generiert aus `MANIFEST.yaml`** am 2026-04-10 11:18. Diese Datei nicht direkt editieren — YAML ändern und `python3 scripts/render_manifest.py` erneut laufen lassen.

Deutsch als Fremdsprache — Unterrichtsmaterialien und interaktive Übungen (Niveau A1–C1)

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
| `daf-a1-uebungen` | Aktives Niveau | A1 | `htmlS/A1.1 NEW` | [fabdaf.github.io/daf-a1-uebungen](https://fabdaf.github.io/daf-a1-uebungen/) | ✓ |
| `daf-a2-uebungen` | Aktives Niveau | A2 | `htmlS/A2.1` | [fabdaf.github.io/daf-a2-uebungen](https://fabdaf.github.io/daf-a2-uebungen/) | ✓ |
| `daf-b1-uebungen` | Aktives Niveau | B1 | `htmlS/B1.1` | [fabdaf.github.io/daf-b1-uebungen](https://fabdaf.github.io/daf-b1-uebungen/) | ✓ |
| `daf-b2-uebungen` | Aktives Niveau | B2 | `.` | [fabdaf.github.io/daf-b2-uebungen](https://fabdaf.github.io/daf-b2-uebungen/) | ✓ |
| `daf-c1-uebungen` | Aktives Niveau | C1 | `htmlS/C1` | [fabdaf.github.io/daf-c1-uebungen](https://fabdaf.github.io/daf-c1-uebungen/) | ✓ |
| `daf-materialien` | Materialien | — | `daf-materialien` | [fabdaf.github.io/daf-materialien](https://fabdaf.github.io/daf-materialien/) | ✗ (offen) |
| `daf-architektur` | Architektur | — | `htmlS/Architektur` | [fabdaf.github.io/daf-architektur](https://fabdaf.github.io/daf-architektur/) | ✓ |
| `daf-lueckentexte` | Spezial | — | `htmlS/Lückentexte Mattmüller` | [fabdaf.github.io/daf-lueckentexte](https://fabdaf.github.io/daf-lueckentexte/) | ✓ |
| `daf-archiv` | Archiv | — | `daf-archiv` | — | ✗ (offen) |

## Details pro Repo

### `daf-a1-uebungen`

_Aktive A1-Lektionen (ehem. A1-Einstieg + A1 + A1.2 NEW konsolidiert am 2026-04-10)_

- **Lokal:** `htmlS/A1.1 NEW`
- **Remote:** https://github.com/fabDaF/daf-a1-uebungen.git
- **GitHub Pages:** aktiv unter https://fabdaf.github.io/daf-a1-uebungen/
- **Dashboard basis:** `https://fabdaf.github.io/daf-a1-uebungen/`
- **Erwartung:** ≥190 tracked files, ≥180 HTML

### `daf-a2-uebungen`

_Aktive A2-Lektionen (A2.1 + A2.2 konsolidiert am 2026-04-10)_

- **Lokal:** `htmlS/A2.1`
- **Remote:** https://github.com/fabDaF/daf-a2-uebungen.git
- **GitHub Pages:** aktiv unter https://fabdaf.github.io/daf-a2-uebungen/
- **Dashboard basis:** `https://fabdaf.github.io/daf-a2-uebungen/`
- **Erwartung:** ≥180 tracked files, ≥140 HTML

### `daf-b1-uebungen`

_Aktive B1-Lektionen (B1.1 als Master; B1.2/B1.3 am 2026-04-10 verworfen, nur Grammatik übernommen)_

- **Lokal:** `htmlS/B1.1`
- **Remote:** https://github.com/fabDaF/daf-b1-uebungen.git
- **GitHub Pages:** aktiv unter https://fabdaf.github.io/daf-b1-uebungen/
- **Dashboard basis:** `https://fabdaf.github.io/daf-b1-uebungen/`
- **Erwartung:** ≥170 tracked files, ≥165 HTML

### `daf-b2-uebungen`

_Aktive B2-Lektionen (Root-Repo des Projekts; trägt auch MANIFEST.yaml)_

- **Lokal:** `.`
- **Remote:** https://github.com/fabDaF/daf-b2-uebungen.git
- **GitHub Pages:** aktiv unter https://fabdaf.github.io/daf-b2-uebungen/
- **Dashboard basis:** `https://fabdaf.github.io/daf-b2-uebungen/`
- **Erwartung:** ≥160 tracked files, ≥150 HTML

### `daf-c1-uebungen`

_C1-Lektionen (klein, wird schrittweise aufgebaut)_

- **Lokal:** `htmlS/C1`
- **Remote:** https://github.com/fabDaF/daf-c1-uebungen.git
- **GitHub Pages:** aktiv unter https://fabdaf.github.io/daf-c1-uebungen/
- **Dashboard basis:** `https://fabdaf.github.io/daf-c1-uebungen/`
- **Erwartung:** ≥1 tracked files, ≥1 HTML

### `daf-materialien`

_Niveau-übergreifende Materialien: Grundlagen, Texte, Treffen, Warum wir krank werden, Wortschatz_

- **Lokal:** `daf-materialien`
- **Remote:** https://github.com/fabDaF/daf-materialien.git
- **GitHub Pages:** ⚠ noch nicht aktiv
- **Dashboard basis:** `https://fabdaf.github.io/daf-materialien/`
- **Erwartung:** ≥40 tracked files, ≥40 HTML

### `daf-architektur`

_Architektur-Material für Caroline Deters (Kap13-Entwurfsplanung etc.)_

- **Lokal:** `htmlS/Architektur`
- **Remote:** https://github.com/fabDaF/daf-architektur.git
- **GitHub Pages:** aktiv unter https://fabdaf.github.io/daf-architektur/
- **Dashboard basis:** `https://fabdaf.github.io/daf-architektur/`
- **Erwartung:** ≥7 tracked files, ≥7 HTML

### `daf-lueckentexte`

_Lückentext-Übungen nach Mattmüller-Methode_

- **Lokal:** `htmlS/Lückentexte Mattmüller`
- **Remote:** https://github.com/fabDaF/daf-lueckentexte.git
- **GitHub Pages:** aktiv unter https://fabdaf.github.io/daf-lueckentexte/
- **Dashboard basis:** `https://fabdaf.github.io/daf-lueckentexte/`
- **Erwartung:** ≥10 tracked files, ≥10 HTML

### `daf-archiv`

_Historische Kopien und verworfene Versionen (B1/B2 Grammatik-Kopien, Löschbar-Ordner). FROZEN._

- **Lokal:** `daf-archiv`
- **Remote:** https://github.com/fabDaF/daf-archiv.git
- **GitHub Pages:** ⚠ noch nicht aktiv
- **Erwartung:** ≥30 tracked files, ≥30 HTML

## Bekannte offene Punkte

Jeder Eintrag hier ist ein dokumentierter, aber noch nicht behobener Zustand. `verify_manifest.py` wertet sie nicht als Fehler, solange sie hier stehen. Sobald behoben → aus `MANIFEST.yaml` entfernen und neu rendern.

### 🔴 Hoch

**dashboard_references_missing_wkv_repo** (seit 2026-04-10, Owner: frank)  
dashboard.html verweist auf basis 'https://fabdaf.github.io/daf-wkv-uebungen/' (Sektion 'WKV – Schülermaterial', Caroline Deters), aber dieses Repo existiert lokal NICHT. Die HTML-Dateien (WKV-Vertragssprache.html, WKV-Komposita-FVG.html, WKV-Geschaeftsemail.html) liegen in 'Archiv fabDaf/Schülermaterial/'. Klärungsbedarf: Ist das Repo auf GitHub live und nur lokal nie geklont, oder ist der Dashboard-Link tot? Entscheidung: entweder Repo lokal klonen + in Manifest aufnehmen, oder Dashboard-Eintrag entfernen.

### 🟡 Mittel

**pages_daf_materialien** (seit 2026-04-10, Owner: frank)  
GitHub Pages für daf-materialien noch nicht aktiviert. Dashboard-Links auf fabdaf.github.io/daf-materialien/ laufen ins Leere, bis Frank Settings → Pages → main branch → / klickt.

**orphaned_repos_on_github** (seit 2026-04-10, Owner: frank)  
Die alten Repos daf-a2-2-uebungen und daf-grundlagen existieren noch auf GitHub, werden aber von keinem Manifest-Eintrag mehr referenziert. Sollten auf GitHub archiviert werden (Settings → Danger Zone → Archive).

**c1_untracked_files** (seit 2026-04-10, Owner: frank)  
htmlS/C1 hat nur 1 getrackte HTML-Datei (DE_C1_1011G-nominalstil.html), aber 7 HTML-Dateien physisch vorhanden. 6 Dateien sind ungetrackt. Klärungsbedarf: sollen sie committed werden oder sind sie Entwürfe?

**launchd_backup_not_activated** (seit 2026-04-10, Owner: frank)  
Automatisches Backup via launchd ist vorbereitet (backup/com.fabdaf.backup.plist), aber noch nicht geladen. Siehe backup/INSTALL.md.

### ⚪ Niedrig

**pages_daf_archiv** (seit 2026-04-10, Owner: frank)  
GitHub Pages für daf-archiv noch nicht aktiviert. Nur relevant, falls Archiv-Inhalte als Read-Only-Referenz serviert werden sollen.

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
