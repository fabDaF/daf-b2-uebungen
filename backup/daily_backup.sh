#!/bin/bash
# Tägliches Backup von ~/Cowork/Projekte/fabDaF
# Läuft via launchd jeden Tag um 03:00 Uhr
# Installation: siehe backup/com.fabdaf.backup.plist und INSTALL.md

set -e

SRC="$HOME/Cowork/Projekte/fabDaF"
DST="$HOME/Cowork/Projekte/Archiv fabDaf/AUTOMATISCHE_BACKUPS"
LOG="$DST/backup.log"
TS=$(date +"%Y%m%d_%H%M")

mkdir -p "$DST"
echo "=== Backup gestartet: $(date) ===" >> "$LOG"

# 1. Tar.gz des kompletten Ordners (inkl. aller .git-Verzeichnisse)
tar --exclude='.DS_Store' \
    -czf "$DST/fabDaF_$TS.tar.gz" \
    -C "$(dirname "$SRC")" \
    "$(basename "$SRC")" 2>> "$LOG"

SIZE=$(du -h "$DST/fabDaF_$TS.tar.gz" | cut -f1)
echo "Archiv erstellt: fabDaF_$TS.tar.gz ($SIZE)" >> "$LOG"

# 2. Push aller Branches in allen Repos zu origin (Sicherheitsnetz)
find "$SRC" -name ".git" -type d 2>/dev/null | while read g; do
  repo=$(dirname "$g")
  cd "$repo" && git push origin --all --quiet 2>> "$LOG" || true
  cd "$repo" && git push origin --tags --quiet 2>> "$LOG" || true
done
echo "Push zu origin abgeschlossen" >> "$LOG"

# 3. Alte Backups aufräumen: Tägliche letzte 7 behalten, wöchentliche letzte 4, monatliche letzte 12
cd "$DST"
# Behalte die letzten 30 ZIPs, lösche ältere
ls -1t fabDaF_*.tar.gz 2>/dev/null | tail -n +31 | xargs -r rm -f

echo "=== Backup beendet: $(date) ===" >> "$LOG"
echo "" >> "$LOG"
