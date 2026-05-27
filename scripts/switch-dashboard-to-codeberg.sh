#!/usr/bin/env bash
#
# Recovery-Skript: Wenn GitHub jemals stirbt (Account-Sperre, längerer Pages-
# Ausfall, was auch immer), schaltet dieses Skript das Dashboard von der
# eigenen Domain (*.daf.frankburkert-daf.de) auf fabbulos.codeberg.page um.
#
# Voraussetzung: Codeberg-Mirror ist aktiv (siehe MANIFEST.yaml mirror_policy
# und codeberg_mirror-Felder). Da die Mirror-Action auf github läuft, muss
# das letzte Mirror-Run noch durchgekommen sein, bevor github starb.
#
# Aktualisiert am 2026-05-27: Berücksichtigt die Subdomain-Migration weg von
# fabdaf.github.io auf *.daf.frankburkert-daf.de. Behält die alten github.io-
# Patterns als Fallback, falls noch Restbestände im Dashboard sind.
#
# Was es macht:
#   1. Backup von htmlS/dashboard.html anlegen.
#   2. sed über alle bekannten Subdomain-/github.io-Patterns →
#      fabbulos.codeberg.page/<repo>/.
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

# Mapping: aktuelle Live-Domain → Codeberg-Pages-Pfad
# Reihenfolge wichtig: spezifische Sub-Subdomains zuerst, damit nicht die
# kurze "daf.frankburkert-daf.de/" zuerst greift und z.B. "a1.daf.frankburkert-daf.de/"
# kaputt macht. sed ersetzt aber URL-getrennt — disjunkt durch Subdomain-Präfix.
declare -a MAPPING=(
  "https://a1.daf.frankburkert-daf.de/|https://fabbulos.codeberg.page/daf-a1-uebungen/"
  "https://a2.daf.frankburkert-daf.de/|https://fabbulos.codeberg.page/daf-a2-uebungen/"
  "https://b1.daf.frankburkert-daf.de/|https://fabbulos.codeberg.page/daf-b1-uebungen/"
  "https://c1.daf.frankburkert-daf.de/|https://fabbulos.codeberg.page/daf-c1-uebungen/"
  "https://materialien.daf.frankburkert-daf.de/|https://fabbulos.codeberg.page/daf-materialien/"
  "https://architektur.daf.frankburkert-daf.de/|https://fabbulos.codeberg.page/daf-architektur/"
  "https://lueckentexte.daf.frankburkert-daf.de/|https://fabbulos.codeberg.page/daf-lueckentexte/"
  "https://vertrag.daf.frankburkert-daf.de/|https://fabbulos.codeberg.page/daf-vertragssprache-uebungen/"
  "https://daf.frankburkert-daf.de/|https://fabbulos.codeberg.page/daf-b2-uebungen/"
  # Fallback für Restbestände aus der Zeit vor der Subdomain-Migration
  "https://fabdaf.github.io/|https://fabbulos.codeberg.page/"
)

# Pre-Check
OWNDOMAIN_BEFORE=$(grep -c 'frankburkert-daf\.de' "$DASHBOARD" || true)
GITHUB_BEFORE=$(grep -c 'fabdaf\.github\.io' "$DASHBOARD" || true)
CODEBERG_BEFORE=$(grep -c 'fabbulos\.codeberg\.page' "$DASHBOARD" || true)

echo "─── Switch-to-Codeberg ──────────────────────────────"
echo "Dashboard: $DASHBOARD"
echo "Vorher: $OWNDOMAIN_BEFORE × eigene Domain, $GITHUB_BEFORE × github.io, $CODEBERG_BEFORE × codeberg.page"

if [ "$OWNDOMAIN_BEFORE" -eq 0 ] && [ "$GITHUB_BEFORE" -eq 0 ] && [ "$CODEBERG_BEFORE" -gt 0 ]; then
  echo "ℹ  Schon auf Codeberg. Nichts zu tun."
  exit 0
fi

# Backup
BACKUP="$DASHBOARD.before-codeberg-switch.$(date +%Y%m%d-%H%M%S)"
cp "$DASHBOARD" "$BACKUP"
echo "Backup: $BACKUP"

# Replace pro Mapping-Eintrag
for entry in "${MAPPING[@]}"; do
  FROM="${entry%%|*}"
  TO="${entry##*|}"
  FROM_ESC="$(printf '%s' "$FROM" | sed 's/[\/&]/\\&/g')"
  TO_ESC="$(printf '%s' "$TO" | sed 's/[\/&]/\\&/g')"
  sed -i.bak "s|${FROM_ESC}|${TO_ESC}|g" "$DASHBOARD"
  rm -f "$DASHBOARD.bak"
done

# Post-Check
OWNDOMAIN_AFTER=$(grep -c 'frankburkert-daf\.de' "$DASHBOARD" || true)
GITHUB_AFTER=$(grep -c 'fabdaf\.github\.io' "$DASHBOARD" || true)
CODEBERG_AFTER=$(grep -c 'fabbulos\.codeberg\.page' "$DASHBOARD" || true)

echo "Nachher: $OWNDOMAIN_AFTER × eigene Domain, $GITHUB_AFTER × github.io, $CODEBERG_AFTER × codeberg.page"

if [ "$OWNDOMAIN_AFTER" -eq 0 ] && [ "$GITHUB_AFTER" -eq 0 ]; then
  echo "✓ Switchover erfolgreich."
else
  echo "⚠ Es gibt noch $OWNDOMAIN_AFTER eigene-Domain- und $GITHUB_AFTER github.io-Treffer. Bitte manuell prüfen."
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
