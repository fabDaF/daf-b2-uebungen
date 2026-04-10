# Datenverlust-Prävention für fabDaF

Dieses Dokument beschreibt das 5-Schichten-Schutzsystem, das nach dem Vorfall am 10.04.2026 eingerichtet wurde, und was du selbst aktivieren musst, damit alles dauerhaft läuft.

## Was passiert ist

Am 10.04.2026 hat sich herausgestellt, dass ca. 50 B2.1-Lektionsdateien als 404-Fehler auf dem Dashboard erschienen. Die Ursache: Die Dateien existierten als "unreachable commits" in den `.git`-Ordnern — d.h. sie waren einmal committed, aber nicht mehr von einem aktiven Branch aus erreichbar. Grund war vermutlich ein `git checkout` über uncommitted oder lose work, kombiniert mit der Tatsache, dass `git gc` solche Commits nach 90 Tagen automatisch löscht. Nur weil `gc` in diesem Fall noch nicht gelaufen war, ließen sich die Dateien retten.

## Die 5 Schutzschichten

### Schicht 1 — GC ist in allen 11 Repos deaktiviert

In allen `.git`-Ordnern unter `fabDaF` sind folgende Settings gesetzt:
- `gc.auto 0` (kein automatisches gc)
- `gc.pruneExpire never` (lose Objekte werden nie gelöscht)
- `gc.reflogExpire never` (reflog wird nie abgeschnitten)
- `gc.reflogExpireUnreachable never`

**Wirkung:** Auch wenn du versehentlich einen Branch löschst oder einen Commit überschreibst, bleibt der Commit im reflog und in den losen Objekten erhalten — auf Dauer.

**Wartung:** Wenn du neue Repos klonst, führe einmal aus:
```bash
bash ~/Cowork/Projekte/fabDaF/backup/lock_gc.sh
```

### Schicht 2 — Rescue-Branches für alle unreachable Commits

Aus jedem unreachable "Tip"-Commit (Kopf einer verwaisten Kette) wurde ein Branch `rescue/20260410/<sha>` erzeugt und zu GitHub gepusht. Damit sind alle verwaisten Arbeiten jetzt über normale Branches erreichbar.

**Wartung:** Wenn `check_integrity.sh` meldet "UNREACHABLE=X", lauf einmal:
```bash
bash ~/Cowork/Projekte/fabDaF/backup/rescue_orphans.sh
cd ~/Cowork/Projekte/fabDaF && find . -name .git -type d -execdir sh -c 'cd $(dirname .git) && git push origin --all --quiet' \;
```

### Schicht 3 — Auto-Push nach jedem Commit

In allen 11 Repos ist ein `post-commit` Hook installiert:
```
.git/hooks/post-commit
```
Dieser pusht JEDEN Commit automatisch zu GitHub, sofern das Internet verfügbar ist. Dadurch existiert nie wieder Code nur lokal.

**Wartung:** Wenn du ein neues Repo klonst oder `hooks/` überschrieben wurde, kopiere den Hook aus einem anderen Repo oder erstelle ihn neu:
```bash
cat > .git/hooks/post-commit <<'HOOK'
#!/bin/sh
branch=$(git rev-parse --abbrev-ref HEAD 2>/dev/null)
if [ -n "$branch" ] && [ "$branch" != "HEAD" ]; then
  (git push origin "$branch" --quiet 2>/dev/null &)
fi
exit 0
HOOK
chmod +x .git/hooks/post-commit
```

### Schicht 4 — Tägliches Archiv-Backup (launchd)

Das Script `backup/daily_backup.sh` erstellt jeden Tag um 03:00 Uhr:
1. Ein `.tar.gz` des kompletten `fabDaF`-Ordners (inkl. aller `.git`) in `~/Cowork/Projekte/Archiv fabDaf/AUTOMATISCHE_BACKUPS/`
2. Pusht alle Branches und Tags in allen Repos zu origin
3. Räumt alte Backups auf (behält die letzten 30 tar.gz)

**Aktivierung (du musst das einmalig machen):**
```bash
cp ~/Cowork/Projekte/fabDaF/backup/com.fabdaf.backup.plist ~/Library/LaunchAgents/
launchctl load ~/Library/LaunchAgents/com.fabdaf.backup.plist
```

**Überprüfen, ob es läuft:**
```bash
launchctl list | grep com.fabdaf.backup
# Sollte die Plist zeigen. Erster Wert = PID (- = gerade nicht aktiv), zweiter = Exit-Code
```

**Manuell einmal testen:**
```bash
bash ~/Cowork/Projekte/fabDaF/backup/daily_backup.sh
ls -lh "$HOME/Cowork/Projekte/Archiv fabDaf/AUTOMATISCHE_BACKUPS/"
```

**Deaktivieren (falls nötig):**
```bash
launchctl unload ~/Library/LaunchAgents/com.fabdaf.backup.plist
```

### Schicht 5 — Notfall-Snapshot

Als Sofortmaßnahme wurde am 10.04.2026 um 09:31 Uhr ein kompletter Snapshot erstellt:
```
~/Cowork/Projekte/Archiv fabDaf/AUTOMATISCHE_BACKUPS/fabDaF_NOTFALL_20260410_0931.tar.gz  (2.0 GB)
```

Das ist ein einmaliger Sicherheitsanker. Lasse ihn dort liegen — wenn morgen irgendwas Schlimmes passiert, kannst du daraus alles wiederherstellen.

## Wöchentlicher Integritäts-Check

Lasse wöchentlich oder vor Panik-Momenten diesen Check laufen:
```bash
bash ~/Cowork/Projekte/fabDaF/backup/check_integrity.sh
```

Das Script meldet für jedes Repo:
- Anzahl unreachable commits
- Anzahl unpushed commits
- Dirty-Status
- Ob die GC-Settings stimmen

Alles "OK" = sauber. Wenn Warnungen kommen, zeigt das Script dir gleich den Fix-Befehl.

## Was du zusätzlich außerhalb dieses Repos machen solltest

1. **Time Machine aktivieren** (oder ein anderes externes Mac-Backup). Alles hier geht in die iCloud/auf die Festplatte, aber ein Hardware-Crash würde alles außer dem GitHub-Remote löschen. Time Machine ist die einfachste Absicherung.
2. **GitHub-Repo regelmäßig anschauen**: https://github.com/fabDaF — wenn die Rescue-Branches dort angekommen sind, ist alles gesichert.
3. **Langfristig: Die 11 parallelen Repos konsolidieren.** Aktuell hat `fabDaF` 11 eigenständige Git-Repos (Root + jeder Lektionsunterordner hat sein eigenes `.git`). Das ist historisch gewachsen, macht aber Wartung riskant. Irgendwann sollten wir das zu einem einzigen Repo zusammenführen.

## Kurzfassung für Panik-Momente

**Ich habe Dateien verloren, was tun?**
1. `bash ~/Cowork/Projekte/fabDaF/backup/check_integrity.sh` — zeigt, ob es unreachable commits gibt
2. Wenn ja: die Dateien sind noch in den `.git`-Ordnern. Rescue-Branches sind schon angelegt — schau auf GitHub unter `rescue/*`.
3. Letzter Ausweg: Notfall-ZIP oder tägliches ZIP in `AUTOMATISCHE_BACKUPS/` entpacken.

**Das Backup läuft nicht, was ist los?**
```bash
launchctl list | grep com.fabdaf.backup
cat "$HOME/Cowork/Projekte/Archiv fabDaf/AUTOMATISCHE_BACKUPS/launchd.err.log"
cat "$HOME/Cowork/Projekte/Archiv fabDaf/AUTOMATISCHE_BACKUPS/backup.log"
```
