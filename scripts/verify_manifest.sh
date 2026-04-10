#!/usr/bin/env bash
# Wrapper für verify_manifest.py — damit man es auch als .sh aufrufen kann.
# Nutzung:
#   ./scripts/verify_manifest.sh           # kurze Ausgabe
#   ./scripts/verify_manifest.sh -v        # verbose (auch OK-Einträge)
#   ./scripts/verify_manifest.sh --json    # JSON-Output

set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
exec python3 "$SCRIPT_DIR/verify_manifest.py" "$@"
