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
# Zweite Aufgabe: den GitHub-Pages-Build ueberwachen. Ein Push allein bringt
# nichts auf die Website — am 2026-08-06 sind drei Builds still gescheitert und
# die Seiten blieben eine Woche alt. Nach jedem Push merkt sich das Skript den
# Commit in _autopush.state und prueft bei den folgenden Laeufen den Build.
# Gescheiterte Builds stoesst es bis zu zweimal neu an.
#
# Log:  ~/Cowork/Projekte/fabDaF/_autopush.log   (von Claude lesbar)
# ---------------------------------------------------------------------------

set -uo pipefail

BASE="${FABDAF_BASE:-$HOME/Cowork/Projekte/fabDaF}"
CRED="$BASE/.git-credentials-fabdaf"
LOG="$BASE/_autopush.log"
STATE="$BASE/_autopush.state"        # offene Deploys: slug<TAB>sha<TAB>versuche
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

# GitHub-Slug (owner/repo) aus der origin-URL des Repos.
slug_of() {
  git -C "$1" remote get-url origin 2>/dev/null \
    | sed -E 's#^.*github\.com[:/]##; s#\.git$##'
}

# Token aus der Credential-Datei; nur fuer die API noetig, nie ins Log.
gh_token() { sed -E 's#^https://[^:]+:([^@]+)@.*$#\1#' "$CRED" 2>/dev/null | head -n1; }

gh_api() {   # gh_api METHODE PFAD
  curl -sS --max-time 25 -X "$1" \
       -H "Authorization: token $(gh_token)" \
       -H "Accept: application/vnd.github+json" \
       "https://api.github.com/repos/$2" 2>/dev/null
}

json_field() { printf '%s' "$1" | sed -n "s/.*\"$2\"[[:space:]]*:[[:space:]]*\"\([^\"]*\)\".*/\1/p" | head -n1; }

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
      : # lokal hinter origin — Dauerzustand einiger Klone, kein Ereignis, nicht loggen
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
    slug=$(slug_of "$repo")
    if [ -n "$slug" ]; then
      grep -v "^$slug	" "$STATE" 2>/dev/null > "$STATE.tmp"; mv "$STATE.tmp" "$STATE" 2>/dev/null
      printf '%s\t%s\t0\n' "$slug" "$local_sha" >> "$STATE"
    fi
  else
    log "FEHLER $name — Push abgelehnt: $(printf '%s' "$out" | tail -n 2 | tr '\n' ' ')"
  fi
done

# ---------------------------------------------------------------------------
# Pages-Deploys nachverfolgen. Bei jedem Lauf werden die offenen Eintraege aus
# _autopush.state geprueft — so wartet der 2-Minuten-Takt fuer uns, statt dass
# dieser Prozess minutenlang pollt und die Pushes blockiert.
# ---------------------------------------------------------------------------
if [ -s "$STATE" ]; then
  NEXT="$STATE.next"; : > "$NEXT"
  while IFS=$'\t' read -r slug sha tries; do
    [ -n "${slug:-}" ] || continue
    body=$(gh_api GET "$slug/pages/builds/latest")
    status=$(json_field "$body" status)

    case "$status" in
      built)
        log "DEPLOY $slug — Pages-Build erfolgreich (${sha:0:7}) — live"
        ;;
      errored|null|"")
        if [ -z "$status" ]; then
          printf '%s\t%s\t%s\n' "$slug" "$sha" "$tries" >> "$NEXT"   # API nicht erreichbar: spaeter nochmal
        elif [ "${tries:-0}" -lt 2 ]; then
          gh_api POST "$slug/pages/builds" >/dev/null
          log "DEPLOY $slug — Build gescheitert, neu angestossen (Versuch $((tries+1))/2)"
          printf '%s\t%s\t%s\n' "$slug" "$sha" "$((tries+1))" >> "$NEXT"
        else
          log "FEHLER $slug — Pages-Build bleibt rot nach 2 Versuchen; Seite ist NICHT aktuell"
        fi
        ;;
      *)   # queued / building — beim naechsten Lauf erneut sehen
        printf '%s\t%s\t%s\n' "$slug" "$sha" "$tries" >> "$NEXT"
        ;;
    esac
  done < "$STATE"
  mv "$NEXT" "$STATE"
fi

[ "$pushed_any" = "1" ] && log "----- Durchlauf beendet -----"
exit 0
