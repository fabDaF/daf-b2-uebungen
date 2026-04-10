#!/bin/bash
# Integritäts-Check für fabDaF
# Findet: unreachable commits, unpushed branches, Dateien die nur lokal oder nur remote existieren
# Benutzung: bash backup/check_integrity.sh
# Sollte wöchentlich laufen ODER bevor du Sorge hast, dass etwas verloren ging

SRC="$HOME/Cowork/Projekte/fabDaF"
ALERT=0

echo "================================================================"
echo "  fabDaF Integritäts-Check"
echo "  Start: $(date)"
echo "================================================================"
echo

find "$SRC" -name ".git" -type d 2>/dev/null | while read g; do
  repo=$(dirname "$g")
  rel="${repo#$SRC/}"
  [ "$rel" = "$SRC" ] && rel="(root)"
  cd "$repo" 2>/dev/null || continue

  # 1. Unreachable commits
  unreach=$(git fsck --unreachable --no-reflogs 2>&1 | grep -c "unreachable commit")

  # 2. Unpushed commits auf aktuellem Branch
  branch=$(git rev-parse --abbrev-ref HEAD 2>/dev/null)
  unpushed=0
  if [ -n "$branch" ] && [ "$branch" != "HEAD" ]; then
    git fetch origin --quiet 2>/dev/null
    unpushed=$(git log "origin/$branch..$branch" --oneline 2>/dev/null | wc -l | tr -d ' ')
  fi

  # 3. Uncommitted changes
  dirty=$(git status --porcelain 2>/dev/null | wc -l | tr -d ' ')

  # 4. GC settings check
  gc_auto=$(git config gc.auto 2>/dev/null || echo "UNSET")
  reflog_exp=$(git config gc.reflogExpire 2>/dev/null || echo "UNSET")

  status="OK"
  [ "$unreach" -gt 0 ] && status="⚠ UNREACHABLE=$unreach"
  [ "$unpushed" -gt 0 ] && status="⚠ UNPUSHED=$unpushed"
  [ "$dirty" -gt 5 ] && status="⚠ DIRTY=$dirty"
  [ "$gc_auto" != "0" ] && status="⚠ GC_AUTO_NICHT_AUS"
  [ "$reflog_exp" != "never" ] && status="⚠ REFLOG_EXPIRE_NICHT_NEVER"

  printf "%-35s %s\n" "[$rel]" "$status"
  [ "$unreach" -gt 0 ] || [ "$unpushed" -gt 0 ] || [ "$gc_auto" != "0" ] && ALERT=1
done

echo
echo "================================================================"
if [ $ALERT -eq 0 ]; then
  echo "  ✓ Alle Repos sauber. Keine Aktion nötig."
else
  echo "  ⚠ WARNUNGEN GEFUNDEN. Bitte oben prüfen."
  echo
  echo "  Schnell-Fixes:"
  echo "  • unreachable: rescue-branches anlegen mit backup/rescue_orphans.sh"
  echo "  • unpushed: in den betroffenen Ordner und 'git push' ausführen"
  echo "  • GC_AUTO nicht aus: bash backup/lock_gc.sh"
fi
echo "================================================================"
