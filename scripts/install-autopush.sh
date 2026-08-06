#!/bin/bash
# Einmalige Installation des Auto-Push-Dienstes (LaunchAgent).
# Aufruf:  bash ~/Cowork/Projekte/fabDaF/scripts/install-autopush.sh
# Deinstallation:  bash ~/Cowork/Projekte/fabDaF/scripts/install-autopush.sh --uninstall
set -euo pipefail

BASE="$HOME/Cowork/Projekte/fabDaF"
LABEL="de.frankburkert.fabdaf-autopush"
AGENTS="$HOME/Library/LaunchAgents"
PLIST="$AGENTS/$LABEL.plist"
SCRIPT="$BASE/scripts/autopush.sh"

if [ "${1:-}" = "--uninstall" ]; then
    launchctl bootout "gui/$UID/$LABEL" 2>/dev/null || launchctl unload "$PLIST" 2>/dev/null || true
    rm -f "$PLIST"
    echo "🗑  Auto-Push deinstalliert."
    exit 0
fi

[ -f "$SCRIPT" ] || { echo "❌ $SCRIPT fehlt."; exit 1; }
[ -r "$BASE/.git-credentials-fabdaf" ] || { echo "❌ Token-Datei .git-credentials-fabdaf fehlt."; exit 1; }
chmod +x "$SCRIPT"
mkdir -p "$AGENTS"

sed -e "s|PLACEHOLDER_SCRIPT|$SCRIPT|" \
    -e "s|PLACEHOLDER_ERRLOG|$BASE/_autopush.err.log|" \
    "$BASE/scripts/$LABEL.plist" > "$PLIST"

launchctl bootout "gui/$UID/$LABEL" 2>/dev/null || true
launchctl bootstrap "gui/$UID" "$PLIST" 2>/dev/null || launchctl load "$PLIST"
launchctl kickstart -k "gui/$UID/$LABEL" 2>/dev/null || true

echo "✅ Auto-Push installiert — läuft alle 2 Minuten."
echo "   Log:  $BASE/_autopush.log"
sleep 6
echo ""
echo "--- Erste Zeilen des Logs ---"
tail -n 20 "$BASE/_autopush.log" 2>/dev/null || echo "(noch kein Log — beim nächsten Durchlauf)"
