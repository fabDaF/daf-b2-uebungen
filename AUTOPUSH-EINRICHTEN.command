#!/bin/bash
# Doppelklick → richtet den Auto-Push-Dienst ein (einmalig).
# Danach schiebt der Mac fertige Commits von Claude alle 2 Minuten selbst zu GitHub.
cd "$(dirname "$0")" || exit 1
clear
echo "════════════════════════════════════════════════════════"
echo "  fabDaF · Auto-Push einrichten"
echo "════════════════════════════════════════════════════════"
echo ""
bash "./scripts/install-autopush.sh"
echo ""
read -p "Enter zum Schließen..."
