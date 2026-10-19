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
# Dritte Aufgabe (seit 2026-10-08): jeden neuen Commit ZUSAETZLICH direkt nach
# Codeberg spiegeln — unabhaengig von GitHub (siehe Abschnitt "Codeberg-Direktspiegel").
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
# Codeberg-Direktspiegel (seit 2026-10-08).
# Die GitHub Action codeberg-mirror.yml laeuft AUF GitHub: faellt GitHub aus
# oder wird der Account gesperrt, steht der Mirror still. Deshalb schiebt der
# Mac jeden neuen Commit zusaetzlich SELBST nach Codeberg — unabhaengig davon,
# ob der GitHub-Push oben geklappt hat. Die Action bleibt als zweiter Weg.
#   * main/master nur als Fast-Forward (nie destruktiv); ist Codeberg weiter
#     als der lokale Klon, passiert nichts.
#   * pages wird danach dem Branch nachgefuehrt (wie in der Action).
#   * Nur Repos mit .github/workflows/codeberg-mirror.yml (= Mirror-Programm).
# Zugang: bevorzugt SSH-Deploy-Key .codeberg-ssh/id_ed25519 (in allen Mirror-
#        Repos als Deploy Key mit Schreibrecht eingetragen, per daf-archiv/
#        .github/workflows/codeberg-deploykey.yml). Ersatzweise Token-Datei
#        .git-credentials-codeberg (scripts/set-codeberg-token.sh). Fehlt
#        beides, ruht dieser Teil still.
# Merker: refs/fabdaf-mirror/codeberg/<branch> = zuletzt gespiegelter Commit,
#        damit der 2-Minuten-Takt im Leerlauf kein Netz braucht.
# Bei Auth-/Netzfehlern pausiert der Teil 60 Minuten (kein Log-Spam).
# ---------------------------------------------------------------------------
CB_CRED="$BASE/.git-credentials-codeberg"
CB_OWNER="fabbuLos"
CB_BASEURL="${FABDAF_CB_BASEURL:-https://codeberg.org}"
CB_PAUSE="${TMPDIR:-/tmp}/fabdaf-codeberg.pause"
CB_KEY="$BASE/.codeberg-ssh/id_ed25519"   # bevorzugt: SSH-Deploy-Key (gitignored)

CB_MODE=""
if [ -r "$CB_KEY" ]; then
  CB_MODE=ssh
  chmod 700 "$BASE/.codeberg-ssh" 2>/dev/null; chmod 600 "$CB_KEY" 2>/dev/null
  export GIT_SSH_COMMAND="ssh -i \"$CB_KEY\" -o IdentitiesOnly=yes -o BatchMode=yes -o ConnectTimeout=20 -o StrictHostKeyChecking=accept-new -o UserKnownHostsFile=\"$BASE/.codeberg-ssh/known_hosts\""
elif [ -r "$CB_CRED" ]; then
  CB_MODE=https
fi

if [ -n "$CB_MODE" ] && [ -z "$(find "$CB_PAUSE" -maxdepth 0 -mmin -60 2>/dev/null)" ]; then
  for repo in "${REPOS[@]}"; do
    [ -d "$repo/.git" ] || continue
    [ -f "$repo/.github/workflows/codeberg-mirror.yml" ] || continue
    name="${repo#$BASE/}"; [ "$name" = "$repo" ] && name="(root/B2)"

    branch=$(git -C "$repo" symbolic-ref --quiet --short HEAD 2>/dev/null) || continue
    case "$branch" in main|master) ;; *) continue ;; esac
    local_sha=$(git -C "$repo" rev-parse "$branch" 2>/dev/null) || continue
    mark="refs/fabdaf-mirror/codeberg/$branch"
    [ "$local_sha" = "$(git -C "$repo" rev-parse --verify --quiet "$mark" 2>/dev/null)" ] && continue

    slug=$(slug_of "$repo"); cb_repo="${slug##*/}"
    [ -n "$cb_repo" ] || continue
    if [ "$CB_MODE" = ssh ]; then cb_url="git@codeberg.org:$CB_OWNER/$cb_repo.git"
    else cb_url="$CB_BASEURL/$CB_OWNER/$cb_repo.git"; fi

    out=$(git -C "$repo" -c credential.helper= -c "credential.helper=store --file=$CB_CRED" \
          push "$cb_url" "$local_sha:refs/heads/$branch" 2>&1)
    if [ $? -ne 0 ]; then
      if printf '%s' "$out" | grep -q -E "non-fast-forward|fetch first|\[rejected\]"; then
        # Codeberg ist weiter als dieser Klon (oder divergiert) — nicht anfassen,
        # Merker setzen, damit erst ein neuer lokaler Commit wieder versucht.
        git -C "$repo" update-ref "$mark" "$local_sha" 2>/dev/null
        continue
      fi
      log "FEHLER Codeberg $name — Push fehlgeschlagen: $(printf '%s' "$out" | tail -n 2 | tr '\n' ' ') — Pause 60 Min"
      touch "$CB_PAUSE"
      break
    fi

    out2=$(git -C "$repo" -c credential.helper= -c "credential.helper=store --file=$CB_CRED" \
           push "$cb_url" "+$local_sha:refs/heads/pages" 2>&1)
    if [ $? -ne 0 ]; then
      # Wettlauf mit der GitHub-Action codeberg-mirror.yml: beide force-pushen `pages`
      # in derselben Sekunde, der Zweite wird abgewiesen ("reference already exists" /
      # "incorrect old value"). Steht Codeberg-`pages` bereits auf unserem Commit, ist
      # alles in Ordnung — kein Fehler, kein Retry (2026-10-19).
      remote_pages=$(git -C "$repo" -c credential.helper= -c "credential.helper=store --file=$CB_CRED" \
                     ls-remote "$cb_url" refs/heads/pages 2>/dev/null | cut -f1)
      if [ "$remote_pages" != "$local_sha" ]; then
        log "FEHLER Codeberg $name — pages nicht nachgefuehrt: $(printf '%s' "$out2" | tail -n 2 | tr '\n' ' ')"
        continue
      fi
      out2="$local_sha -> pages (bereits aktuell, Wettlauf mit GitHub-Action)"
    fi

    git -C "$repo" update-ref "$mark" "$local_sha" 2>/dev/null
    if printf '%s\n%s\n' "$out" "$out2" | grep -q -- ' -> '; then   # nur echte Updates loggen
      log "CODEBERG $name — gespiegelt → ${local_sha:0:7}"
      pushed_any=1
    fi
  done
fi

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
