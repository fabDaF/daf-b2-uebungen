#!/bin/bash
# ---------------------------------------------------------------------------
# autopush.sh — schiebt fertige Commits aller fabDaF-Repos nach GitHub.
#
# Warum es das gibt: Cowork-Sessions (Claude) koennen am Mac committen, aber
# NICHT pushen — die Sandbox hat keinen Weg nach draussen, und der Cloud-Proxy
# blockt Schreibzugriffe auf nicht freigegebene Repos. Dieses Skript laeuft
# nativ unter macOS (per LaunchAgent) und hat deshalb echtes Netz.
#
# Es committet NICHTS. Es pusht nur, was bereits committet ist, und nur als
# Fast-Forward. Alles andere wird uebersprungen und protokolliert.
#
# Log:  ~/Cowork/Projekte/fabDaF/_autopush.log   (von Claude lesbar)
# ---------------------------------------------------------------------------

set -uo pipefail

BASE="${FABDAF_BASE:-$HOME/Cowork/Projekte/fabDaF}"
CRED="$BASE/.git-credentials-fabdaf"
LOG="$BASE/_autopush.log"
LOCK="${TMPDIR:-/tmp}/fabdaf-autopush.lockdir"   # bewusst NICHT im Mount:
                                                 # die Cowork-Sandbox darf dort nicht loeschen

export PATH="/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin"
export GIT_TERMINAL_PROMPT=0
export GIT_ASKPASS=/usr/bin/true

REPOS=(
  "$BASE"
  "$BASE/htmlS/A1.1 NEW"
  "$BASE/htmlS/A2.1"
  "$BASE/htmlS/B1.1"
  "$BASE/htmlS/C1"
  "$BASE/htmlS/Architektur"
  "$BASE/htmlS/Lückentexte Mattmüller"
  "$BASE/daf-materialien"
  "$BASE/daf-archiv"
  "$BASE/termin-redirect"
  "$BASE/schueler/privat-1"
)

log() { printf '%s  %s\n' "$(date '+%Y-%m-%d %H:%M:%S')" "$*" >> "$LOG"; }

# Nur eine Instanz gleichzeitig; verwaiste Locks nach 15 Min brechen.
if ! mkdir "$LOCK" 2>/dev/null; then
  if [ -d "$LOCK" ] && [ -n "$(find "$LOCK" -maxdepth 0 -mmin +15 2>/dev/null)" ]; then
    rmdir "$LOCK" 2>/dev/null && mkdir "$LOCK" 2>/dev/null || exit 0
    log "WARN  verwaistes Lock entfernt"
  else
    exit 0
  fi
fi
trap 'rmdir "$LOCK" 2>/dev/null' EXIT

[ -r "$CRED" ] || { log "FEHLER  Credential-Datei fehlt: $CRED"; exit 1; }

# Log bei >2000 Zeilen kappen, damit er nicht unbegrenzt waechst.
if [ -f "$LOG" ] && [ "$(wc -l < "$LOG" | tr -d ' ')" -gt 2000 ]; then
  tail -n 500 "$LOG" > "$LOG.tmp" && mv "$LOG.tmp" "$LOG"
fi

pushed_any=0

for repo in "${REPOS[@]}"; do
  [ -d "$repo/.git" ] || continue
  name="${repo#$BASE/}"; [ "$name" = "$repo" ] && name="(root/B2)"

  # Sandbox-Altlasten: Lock-Dateien, die Claude nicht loeschen darf.
  find "$repo/.git" -maxdepth 1 -name '*.lock' -delete 2>/dev/null

  branch=$(git -C "$repo" symbolic-ref --quiet --short HEAD 2>/dev/null) || continue
  [ -n "$branch" ] || { log "SKIP  $name — detached HEAD"; continue; }

  # Erst OHNE Netz pruefen: deckt sich HEAD mit dem letzten bekannten Stand von
  # origin, gibt es nichts zu tun. Das ist der Normalfall — so kostet der
  # 2-Minuten-Takt im Leerlauf keine einzige Netzanfrage.
  local_sha=$(git -C "$repo" rev-parse "$branch" 2>/dev/null)
  cached_sha=$(git -C "$repo" rev-parse --verify --quiet "refs/remotes/origin/$branch" 2>/dev/null)
  [ -n "$local_sha" ] || continue
  [ "$local_sha" = "$cached_sha" ] && continue

  # Ab hier gibt es vermutlich etwas zu pushen — jetzt lohnt der Netzzugriff.
  git -C "$repo" \
      -c credential.helper= \
      -c "credential.helper=store --file=$CRED" \
      fetch --quiet origin "$branch" 2>/dev/null || {
        log "SKIP  $name — fetch fehlgeschlagen (offline?)"; continue; }

  remote_sha=$(git -C "$repo" rev-parse FETCH_HEAD 2>/dev/null)
  [ -n "$remote_sha" ] || continue
  [ "$local_sha" = "$remote_sha" ] && continue

  if ! git -C "$repo" merge-base --is-ancestor "$remote_sha" "$local_sha" 2>/dev/null; then
    if git -C "$repo" merge-base --is-ancestor "$local_sha" "$remote_sha" 2>/dev/null; then
      log "SKIP  $name — lokal hinter origin/$branch (nichts zu pushen)"
    else
      log "ACHTUNG  $name — divergiert von origin/$branch, kein Auto-Push"
    fi
    continue
  fi

  ahead=$(git -C "$repo" rev-list --count "$remote_sha..$local_sha" 2>/dev/null)
  out=$(git -C "$repo" \
        -c credential.helper= \
        -c "credential.helper=store --file=$CRED" \
        push origin "$branch:$branch" 2>&1)
  if [ $? -eq 0 ]; then
    log "OK    $name — $ahead Commit(s) gepusht → ${local_sha:0:7}"
    pushed_any=1
  else
    log "FEHLER $name — Push abgelehnt: $(printf '%s' "$out" | tail -n 2 | tr '\n' ' ')"
  fi
done

[ "$pushed_any" = "1" ] && log "----- Durchlauf beendet -----"
exit 0
