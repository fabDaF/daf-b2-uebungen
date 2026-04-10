#!/bin/bash
# Legt Rescue-Branches für alle unreachable "Tip"-Commits an
# Ein Tip-Commit ist ein unreachable commit, der selbst keinen unreachable descendant hat
# (also das "Ende" einer verwaisten Kette)
# Benutzung: bash backup/rescue_orphans.sh
# Nach dem Lauf: git push origin --all ausführen, um die rescue-Branches zu sichern

SRC="$HOME/Cowork/Projekte/fabDaF"
TS=$(date +"%Y%m%d")
TOTAL=0

echo "================================================================"
echo "  Rescue-Branches für unreachable Tip-Commits"
echo "  Timestamp: $TS"
echo "================================================================"

find "$SRC" -name ".git" -type d 2>/dev/null | while read g; do
  repo=$(dirname "$g")
  rel="${repo#$SRC/}"
  [ "$rel" = "$SRC" ] && rel="(root)"
  cd "$repo" || continue

  # Alle unreachable commits sammeln
  all=$(git fsck --unreachable --no-reflogs 2>/dev/null | awk '/unreachable commit/ {print $3}')
  [ -z "$all" ] && continue

  # Parent-Set bilden (alles was Parent von irgendwas ist, ist KEIN Tip)
  parents=$(echo "$all" | while read c; do git cat-file -p "$c" 2>/dev/null | awk '/^parent/ {print $2}'; done | sort -u)

  # Tips = all minus parents
  tips=$(comm -23 <(echo "$all" | sort -u) <(echo "$parents"))

  count=0
  for tip in $tips; do
    short=${tip:0:8}
    ref="refs/heads/rescue/$TS/$short"
    if ! git show-ref --quiet "$ref"; then
      git update-ref "$ref" "$tip" 2>/dev/null && count=$((count+1))
    fi
  done

  [ "$count" -gt 0 ] && echo "  [$rel] $count neue rescue-Branches"
  TOTAL=$((TOTAL+count))
done

echo "================================================================"
echo "  Fertig. Jetzt unbedingt pushen:"
echo "  cd \$SRC && find . -name .git -type d -exec sh -c 'cd \$(dirname {}) && git push origin --all --quiet' \;"
echo "================================================================"
