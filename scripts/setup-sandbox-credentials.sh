#!/usr/bin/env bash
# Stellt nach einem Cowork-Session-Start die Token-Authentifizierung wieder her.
# Liest den persistent gespeicherten Token aus dem Cowork-Folder
# und legt ihn als Git-Credentials-Datei in der Sandbox-Home ab.
#
# Hintergrund: Sandbox-Home (/sessions/<random>) ist ephemer und wird pro
# Cowork-Session neu erzeugt. Der Token muss daher pro Session reaktiviert
# werden. Die persistente Quelldatei liegt im Cowork-Folder und überlebt.

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SRC="$REPO_ROOT/.git-credentials-fabdaf"
DST="$HOME/.git-credentials"

if [ ! -f "$SRC" ]; then
  echo "FEHLER: Quelldatei $SRC fehlt. Token muss erneut hinterlegt werden." >&2
  exit 1
fi

cp "$SRC" "$DST"
chmod 600 "$DST"

git config --global credential.helper "store --file=$DST"

echo "✓ Sandbox-Credentials reaktiviert (Helper: store --file=$DST)"

# Echter Push-Auth-Test via push --dry-run.
# `ls-remote` ist KEIN Auth-Test bei public Repos — die antworten ohne Token.
# `push --dry-run` zwingt git zur Credential-Lookup, schlägt sauber fehl, wenn
# die Auth nicht funktioniert (auch bei public Repos).
GIT_TERMINAL_PROMPT=0 git -C "$REPO_ROOT" push --dry-run origin HEAD >/dev/null 2>&1 \
  && echo "✓ Push-Auth gegen origin erfolgreich" \
  || { echo "FEHLER: Push-Auth fehlgeschlagen — Token ungültig oder ohne Schreibrechte?"; exit 2; }
