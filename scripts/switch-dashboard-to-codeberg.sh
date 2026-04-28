#!/usr/bin/env bash
#
# Recovery-Skript: Wenn GitHub jemals stirbt (Account-Sperre, längerer Pages-
# Ausfall, was auch immer), schaltet dieses Skript das Dashboard von
# fabdaf.github.io auf fabbulos.codeberg.page um.
#
# Voraussetzung: Codeberg-Mirror ist aktiv (siehe MANIFEST.yaml mirror_policy
# und codeberg_mirror-Felder). Da die Mirror-Action auf github läuft, muss
# das letzte Mirror-Run noch durchgekommen sein, bevor github starb.
#
# Was es macht:
#   1. Backup von htmlS/dashboard.html anlegen.
#   2. sed über alle Vorkommen von 'fabdaf.github.io/' → 'fabbulos.codeberg.page/'.
#   3. Status-Bericht und nächste-Schritte-Hinweis ausgeben.
#
# Was es NICHT macht:
#   - Push. Push läuft manuell, weil im Ernstfall der gewohnte github-Pfad
#     tot ist und du direkt zu Codeberg pushen musst (siehe Hinweis am Ende).
#
# Aufruf:
#   bash scripts/switch-dashboard-to-codeberg.sh
#
# Inverse:
#   bash scripts/switch-dashboard-to-github.sh

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

DASHBOARD="htmlS/dashboard.html"

if [ ! -f "$DASHBOARD" ]; then
  echo "✗ FEHLER: $DASHBOARD nicht gefunden" >&2
  exit 1
fi

# Pre-Check: was ist drin?
GITHUB_HITS_BEFORE=$(grep -c 'fabdaf\.github\.io' "$DASHBOARD" || true)
CODEBERG_HITS_BEFORE=$(grep -c 'fabbulos\.codeberg\.page' "$DASHBOARD" || true)

echo "─── Switch-to-Codeberg ──────────────────────────────"
echo "Dashboard: $DASHBOARD"
echo "Vorher: $GITHUB_HITS_BEFORE × github.io, $CODEBERG_HITS_BEFORE × codeberg.page"

if [ "$GITHUB_HITS_BEFORE" -eq 0 ] && [ "$CODEBERG_HITS_BEFORE" -gt 0 ]; then
  echo "ℹ  Schon auf Codeberg. Nichts zu tun."
  exit 0
fi

# Backup
BACKUP="$DASHBOARD.before-codeberg-switch.$(date +%Y%m%d-%H%M%S)"
cp "$DASHBOARD" "$BACKUP"
echo "Backup: $BACKUP"

# Replace
sed -i.bak 's|https://fabdaf\.github\.io/|https://fabbulos.codeberg.page/|g' "$DASHBOARD"
rm -f "$DASHBOARD.bak"

# Post-Check
GITHUB_HITS_AFTER=$(grep -c 'fabdaf\.github\.io' "$DASHBOARD" || true)
CODEBERG_HITS_AFTER=$(grep -c 'fabbulos\.codeberg\.page' "$DASHBOARD" || true)

echo "Nachher: $GITHUB_HITS_AFTER × github.io, $CODEBERG_HITS_AFTER × codeberg.page"

if [ "$GITHUB_HITS_AFTER" -eq 0 ]; then
  echo "✓ Switchover erfolgreich."
else
  echo "⚠ Es gibt noch $GITHUB_HITS_AFTER github.io-Treffer. Bitte manuell prüfen."
fi

cat <<EOF

─── Nächste Schritte ──────────────────────────────────────

1. Änderungen committen (lokal):
   git add htmlS/dashboard.html
   git commit -m "switch: Dashboard auf Codeberg umgeleitet (github offline)"

2. Direkt zu Codeberg pushen (github ist tot, regulärer Push hängt):
   git push https://fabbuLos:<TOKEN>@codeberg.org/fabbuLos/daf-b2-uebungen.git main
   git push https://fabbuLos:<TOKEN>@codeberg.org/fabbuLos/daf-b2-uebungen.git main:pages

3. Schüler:innen die neue Dashboard-URL nennen:
   https://fabbulos.codeberg.page/daf-b2-uebungen/htmlS/dashboard.html

4. Bei github-Wiederkehr:
   bash scripts/switch-dashboard-to-github.sh
   und regulär committen/pushen.

EOF
