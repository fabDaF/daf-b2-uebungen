#!/usr/bin/env bash
#
# Inverses Recovery-Skript zu switch-dashboard-to-codeberg.sh.
# Stellt das Dashboard von fabbulos.codeberg.page wieder zurück auf die
# eigene Domain (*.daf.frankburkert-daf.de), sobald GitHub wieder verfügbar ist.
#
# Aktualisiert am 2026-05-27: Berücksichtigt die Subdomain-Migration weg von
# fabdaf.github.io auf *.daf.frankburkert-daf.de. Der normale Rückweg geht
# auf die eigene Domain. Wer aus historischen Gründen Restbestände direkt
# auf fabdaf.github.io zurückwill, muss das manuell tun.

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

DASHBOARD="htmlS/dashboard.html"

if [ ! -f "$DASHBOARD" ]; then
  echo "✗ FEHLER: $DASHBOARD nicht gefunden" >&2
  exit 1
fi

# Mapping: Codeberg-Pages-Pfad → eigene Domain (Umkehr zu switch-to-codeberg.sh)
declare -a MAPPING=(
  "https://fabbulos.codeberg.page/daf-a1-uebungen/|https://a1.daf.frankburkert-daf.de/"
  "https://fabbulos.codeberg.page/daf-a2-uebungen/|https://a2.daf.frankburkert-daf.de/"
  "https://fabbulos.codeberg.page/daf-b1-uebungen/|https://b1.daf.frankburkert-daf.de/"
  "https://fabbulos.codeberg.page/daf-c1-uebungen/|https://c1.daf.frankburkert-daf.de/"
  "https://fabbulos.codeberg.page/daf-materialien/|https://materialien.daf.frankburkert-daf.de/"
  "https://fabbulos.codeberg.page/daf-architektur/|https://architektur.daf.frankburkert-daf.de/"
  "https://fabbulos.codeberg.page/daf-lueckentexte/|https://lueckentexte.daf.frankburkert-daf.de/"
  "https://fabbulos.codeberg.page/daf-vertragssprache-uebungen/|https://vertrag.daf.frankburkert-daf.de/"
  "https://fabbulos.codeberg.page/daf-b2-uebungen/|https://daf.frankburkert-daf.de/"
)

CODEBERG_BEFORE=$(grep -c 'fabbulos\.codeberg\.page' "$DASHBOARD" || true)
OWNDOMAIN_BEFORE=$(grep -c 'frankburkert-daf\.de' "$DASHBOARD" || true)

echo "─── Switch-back-to-eigene-Domain ───────────────────"
echo "Vorher: $CODEBERG_BEFORE × codeberg.page, $OWNDOMAIN_BEFORE × eigene Domain"

if [ "$CODEBERG_BEFORE" -eq 0 ] && [ "$OWNDOMAIN_BEFORE" -gt 0 ]; then
  echo "ℹ  Schon auf eigener Domain. Nichts zu tun."
  exit 0
fi

BACKUP="$DASHBOARD.before-github-switchback.$(date +%Y%m%d-%H%M%S)"
cp "$DASHBOARD" "$BACKUP"
echo "Backup: $BACKUP"

for entry in "${MAPPING[@]}"; do
  FROM="${entry%%|*}"
  TO="${entry##*|}"
  FROM_ESC="$(printf '%s' "$FROM" | sed 's/[\/&]/\\&/g')"
  TO_ESC="$(printf '%s' "$TO" | sed 's/[\/&]/\\&/g')"
  sed -i.bak "s|${FROM_ESC}|${TO_ESC}|g" "$DASHBOARD"
  rm -f "$DASHBOARD.bak"
done

CODEBERG_AFTER=$(grep -c 'fabbulos\.codeberg\.page' "$DASHBOARD" || true)
OWNDOMAIN_AFTER=$(grep -c 'frankburkert-daf\.de' "$DASHBOARD" || true)

echo "Nachher: $CODEBERG_AFTER × codeberg.page, $OWNDOMAIN_AFTER × eigene Domain"

if [ "$CODEBERG_AFTER" -eq 0 ]; then
  echo "✓ Switchback erfolgreich."
else
  echo "⚠ Es gibt noch $CODEBERG_AFTER codeberg.page-Treffer. Bitte manuell prüfen."
fi

echo ""
echo "Nächster Schritt: git add/commit/push wie üblich."
