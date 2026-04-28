# fabDaF — Projekt-Instruktionen für Claude

Diese Datei wird automatisch geladen, wenn eine Claude-Session im
fabDaF-Ordner arbeitet. Sie enthält die verbindlichen Spielregeln für
dieses Projekt. Bei Widersprüchen zwischen dieser Datei und allgemeinen
Gewohnheiten gilt diese Datei.

## Was ist fabDaF?

Deutsch-als-Fremdsprache-Projekt von Frank Burkert. Unterrichtsmaterialien
und interaktive HTML-Übungen für die Niveaus A1 bis C1. Das Projekt ist
auf neun Git-Repos verteilt, die im `MANIFEST.yaml` am Root vollständig
dokumentiert sind.

## Erste Maßnahme bei jeder strukturellen Arbeit

**Bevor** du an der Repo-Struktur, am Dashboard, an Ordner-Layouts oder
an mehreren Niveaus gleichzeitig arbeitest:

```bash
./scripts/verify_manifest.sh
```

Wenn das Skript nicht grün ist, zuerst klären, warum — nicht
drüberbauen. Jeder Fehler dort ist ein Signal, dass die IST-Welt nicht
mehr zur SOLL-Welt passt.

Bei rein inhaltlichen Arbeiten an einer einzelnen HTML-Datei (typischer
DaF-Lektion) ist das nicht nötig.

## Die Grundregeln dieses Projekts

Diese Regeln sind maschinenlesbar in `MANIFEST.yaml` unter `rules:`
definiert. Hier ist die menschliche Fassung:

**Ein Niveau, ein Repo.** Für A1, A2, B1, B2, C1 existiert je genau ein
aktives Repo. Niemals parallele Versionen wie "A2.1" und "A2.2" oder
"B1.2 NEU". Wer so etwas braucht, nutzt Git-Branches oder legt den
Ordner im `daf-archiv` ab.

**Keine parallelen Arbeitskopien.** Kein "Kopie", kein "Entwurf", kein
"OLD" auf derselben Ebene. Genau diese Parallelität hat am 2026-04-10
eine mehrstündige Konsolidierung nötig gemacht.

**Das Archiv ist eingefroren.** `daf-archiv` darf erweitert, aber nicht
verändert werden. Inhalte dort sind historisch.

**Dashboards zeigen nur auf Manifest-Repos.** Jede `basis:`-URL in
einem `dashboard.html` muss auf ein Repo zeigen, das im Manifest
gelistet ist. Tote Links sind Fehler, keine Platzhalter.

**Keine Secrets in committeten Dateien.** Remote-URLs im Manifest und
in Dokumentation enthalten nie PATs. Seit 2026-04-27 sind auch die
`.git/config`-URLs der zehn Repos tokenfrei (`https://github.com/fabDaF/<repo>.git`).
Der Token lebt nur noch an zwei Orten: macOS-Keychain für den Mac-Workflow,
und `.git-credentials-fabdaf` (chmod 600, in `.gitignore`) für die
Cowork-Sandbox. Details siehe Memory-Eintrag `reference_token-haltung.md`.

## Die neun Repos in Kurzform

| Schlüssel | Lokaler Pfad | Rolle |
|---|---|---|
| `daf-a1-uebungen` | `htmlS/A1.1 NEW` | A1 aktiv |
| `daf-a2-uebungen` | `htmlS/A2.1` | A2 aktiv |
| `daf-b1-uebungen` | `htmlS/B1.1` | B1 aktiv |
| `daf-b2-uebungen` | `.` (Root) | B2 aktiv — trägt dieses CLAUDE.md und das Manifest |
| `daf-c1-uebungen` | `htmlS/C1` | C1 aktiv |
| `daf-materialien` | `daf-materialien` | Niveau-übergreifendes Material |
| `daf-architektur` | `htmlS/Architektur` | Architektur-Kurs für Privatschüler:innen |
| `daf-lueckentexte` | `htmlS/Lückentexte Mattmüller` | Lückentexte nach Mattmüller |
| `daf-archiv` | `daf-archiv` | Historische Kopien, FROZEN |

Vollständige Details inklusive Remote-URLs, Dashboard-Zuordnungen und
Erwartungen: siehe `MANIFEST.md` (generiert aus `MANIFEST.yaml`).

## Betriebs-Warnungen — was in der Vergangenheit Zeit gekostet hat

**Post-commit-Hook pusht automatisch.** Mehrere Repos haben einen Hook,
der nach jedem Commit sofort `git push` ausführt. Wenn du manuell
`git push` hinterherschickst, bekommst du Race Conditions und
"cannot lock ref"-Fehler. Stattdessen: kurz warten, dann prüfen mit
`git rev-parse HEAD origin/main` — wenn beide gleich sind, ist alles
gut.

**api.github.com ist in Cowork-Sessions blockiert.** Repos auf GitHub
anzulegen geht nicht über `gh` oder `curl`. Workaround: Chrome MCP auf
github.com/new navigieren. Dokumentiert im Konsolidierungs-Bericht
`backup/KONSOLIDIERUNG_20260410.md`.

**Cowork-Sandbox: einmaliger Auth-Setup pro Session.**

Beim ersten Push aus einer frischen Cowork-Session ist die Sandbox-Home
leer und enthält keine Git-Credentials. Auth-Failure ist die Folge.
Reaktivierung in einem Befehl aus dem Repo-Root:

```bash
bash scripts/setup-sandbox-credentials.sh
```

Das Skript kopiert den Token aus der persistenten Datei
`.git-credentials-fabdaf` in die Sandbox-Home und konfiguriert den
globalen `credential.helper`. Ende: ein echter `push --dry-run`-Test
bestätigt, dass die Auth wirklich funktioniert.

**Stale git locks — der Cowork-Commit-Workflow (2026-04-17).**

Zwei Sandbox-Einschränkungen müssen gleichzeitig umgangen werden:

1. `.git/index.lock` und `.git/HEAD.lock` können aus der Cowork-Sandbox
   **nicht gelöscht** werden (APFS-Mount-Einschränkung,
   `Operation not permitted`). `rm -f` und `os.unlink` scheitern.
2. Das Cowork-**Write-Tool** löst Permission-Dialoge aus, wenn nach
   `.git/…` geschrieben wird. Diese Dialoge blockieren unbemerkt, wenn
   Cowork im Hintergrund liegt — und Claude wartet dann stundenlang.

Deshalb gilt: **Niemals das Write-Tool für Pfade unter `.git/` benutzen.
Niemals.** Bash-Befehle lösen diese Dialoge nicht aus und sind der
einzige dialog-freie Weg, Refs zu aktualisieren.

Der komplette Commit+Push-Workflow ist in `scripts/safe-commit.sh`
gekapselt:

```bash
scripts/safe-commit.sh "Commit-Nachricht" datei1 [datei2 …]
```

Das Skript erledigt intern:

```bash
export GIT_INDEX_FILE=/tmp/alt-index-$$        # alt-Index statt .git/index.lock
git read-tree HEAD
git update-index --add DATEI1 DATEI2 …
TREE=$(git write-tree)
PARENT=$(git rev-parse HEAD)
COMMIT=$(git commit-tree $TREE -p $PARENT -m "msg")
echo "$COMMIT" > .git/refs/heads/main          # per Bash, NICHT Write-Tool
git push origin main
echo "$COMMIT" > .git/refs/remotes/origin/main # per Bash, NICHT Write-Tool
```

Für Unter-Repos wie `htmlS/A2.1` genauso aus dem jeweiligen Repo-Root
aufrufen. `COMMIT_BRANCH` und `COMMIT_REMOTE` lassen sich per env
überschreiben.

Die `warning: unable to unlink '.git/objects/*/tmp_obj_*'`-Meldungen
sind kosmetisch — die Objekte liegen korrekt im Store.

## Wenn du etwas Neues hinzufügst

Ein neues Repo, eine neue Niveau-Kategorie, ein neuer Ordner mit
eigenem Git-Status → **erst ins `MANIFEST.yaml` eintragen, dann
physisch anlegen.** In dieser Reihenfolge. Anschließend
`python3 scripts/render_manifest.py` laufen lassen, damit `MANIFEST.md`
nachzieht. Sonst ist der neue Zustand Drift und das verify-Skript
schlägt Alarm.

## Wenn du ein known_issue behebst

In `MANIFEST.yaml` unter `known_issues:` den Eintrag löschen, dann
`render_manifest.py` laufen lassen, dann committen. Nicht umgekehrt.

## E-Mail-Adresse in Lektionen — Alias-Rotation

Die formsubmit-Endpunkte und mailto-Footer in den Lektions-HTMLs
verwenden absichtlich NICHT Franks Microsoft-Primäradresse, sondern
einen rotierbaren Alias auf derselben Domain
(`fabdaf.onmicrosoft.com`). Aktueller Alias: **`unterricht@fabdaf.onmicrosoft.com`**.

Wenn der aktive Alias zu sehr verspammt ist (Trigger: Frank merkt es),
ist der Rotations-Workflow:

1. Frank legt im Microsoft 365 Admin Center einen neuen Alias an
   (z.B. `unterricht-2027@fabdaf.onmicrosoft.com` oder kryptisch).
2. Claude tauscht in einem `sed`-Lauf alle Vorkommen von altem
   Alias gegen neuen Alias (typischerweise 250+ Dateien — formsubmit-
   Variablen UND mailto-Footer).
3. Frank deaktiviert den alten Alias in Microsoft 365 — die Spam-Quote
   im Postfach geht damit sofort zurück.

Wichtig: NIEMALS Franks Primäradresse `FrankBurkert@…` in Lektionen
hardcoden. Die Primärin ist seine Login-Identität und kann nicht
rotiert werden. Sie soll nicht öffentlich exponiert sein.

## Ergänzende Dokumente in diesem Repo

- `MANIFEST.yaml` — die SOLL-Welt, maschinenlesbar
- `MANIFEST.md` — dieselbe Info, menschenlesbar (generiert)
- `scripts/verify_manifest.sh` — IST-gegen-SOLL-Prüfung
- `scripts/render_manifest.py` — MD aus YAML erzeugen
- `backup/KONSOLIDIERUNG_20260410.md` — Geschichte der
  11-zu-9-Konsolidierung, warum die heutige Struktur so ist
- `backup/INSTALL.md` — launchd-Backup-Aktivierung

## Franks Arbeitsweise — was ich aus früheren Sessions weiß

Frank ist DaF-Lehrer, nicht Software-Entwickler. Er bevorzugt Prosa
statt Bullet-Listen, will direkte Antworten ohne Präambel, und schätzt
Selbstreflexion und dialektisches Denken (These/Antithese/Synthese).
Er hat einen post-commit-Hook installiert, damit nichts verloren geht —
Datensicherheit ist ihm wichtiger als Git-Eleganz.

Weitere projekt-übergreifende Präferenzen liegen im Auto-Memory-System
unter `~/.auto-memory/MEMORY.md`.
