#!/usr/bin/env bash
#
# Inverses Recovery-Skript zu switch-dashboard-to-codeberg.sh.
# Stellt das Dashboard von fabbulos.codeberg.page wieder zurück auf
# fabdaf.github.io, sobald GitHub wieder verfügbar ist.

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

DASHBOARD="htmlS/dashboard.html"

if [ ! -f "$DASHBOARD" ]; then
  echo "✗ FEHLER: $DASHBOARD nicht gefunden" >&2
  exit 1
fi

CODEBERG_HITS_BEFORE=$(grep -c 'fabbulos\.codeberg\.page' "$DASHBOARD" || true)
GITHUB_HITS_BEFORE=$(grep -c 'fabdaf\.github\.io' "$DASHBOARD" || true)

echo "─── Switch-back-to-GitHub ─────────────────────────"
echo "Vorher: $CODEBERG_HITS_BEFORE × codeberg.page, $GITHUB_HITS_BEFORE × github.io"

if [ "$CODEBERG_HITS_BEFORE" -eq 0 ] && [ "$GITHUB_HITS_BEFORE" -gt 0 ]; then
  echo "ℹ  Schon auf GitHub. Nichts zu tun."
  exit 0
fi

BACKUP="$DASHBOARD.before-github-switchback.$(date +%Y%m%d-%H%M%S)"
cp "$DASHBOARD" "$BACKUP"
echo "Backup: $BACKUP"

sed -i.bak 's|https://fabbulos\.codeberg\.page/|https://fabdaf.github.io/|g' "$DASHBOARD"
rm -f "$DASHBOARD.bak"

CODEBERG_HITS_AFTER=$(grep -c 'fabbulos\.codeberg\.page' "$DASHBOARD" || true)
GITHUB_HITS_AFTER=$(grep -c 'fabdaf\.github\.io' "$DASHBOARD" || true)

echo "Nachher: $CODEBERG_HITS_AFTER × codeberg.page, $GITHUB_HITS_AFTER × github.io"

if [ "$CODEBERG_HITS_AFTER" -eq 0 ]; then
  echo "✓ Switchback erfolgreich."
else
  echo "⚠ Es gibt noch $CODEBERG_HITS_AFTER codeberg.page-Treffer. Bitte manuell prüfen."
fi

echo ""
echo "Nächster Schritt: git add/commit/push wie üblich."
