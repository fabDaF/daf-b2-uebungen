#!/bin/bash
# Sperrt Git Garbage Collection in ALLEN Repos unter fabDaF
# Verhindert, dass unreachable commits automatisch gelöscht werden
# Benutzung: bash backup/lock_gc.sh
# Muss nur einmal laufen, aber schadet nicht, es erneut auszuführen

SRC="$HOME/Cowork/Projekte/fabDaF"
COUNT=0

echo "================================================================"
echo "  GC-Sperre für alle fabDaF-Repos"
echo "================================================================"

find "$SRC" -name ".git" -type d 2>/dev/null | while read g; do
  repo=$(dirname "$g")
  rel="${repo#$SRC/}"
  [ "$rel" = "$SRC" ] && rel="(root)"
  cd "$repo" || continue

  git config gc.auto 0
  git config gc.autoDetach false
  git config gc.pruneExpire never
  git config gc.reflogExpire never
  git config gc.reflogExpireUnreachable never

  echo "  ✓ [$rel] GC gesperrt"
  COUNT=$((COUNT+1))
done

echo "================================================================"
echo "  Fertig. GC ist in allen Repos deaktiviert."
echo "================================================================"
