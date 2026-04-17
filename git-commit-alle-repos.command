#!/bin/bash
# Doppelklick → Terminal öffnet und committet alle Repos

BASE="$HOME/Cowork/Projekte/fabDaF"
MSG="style: .btn Design auf lila Standard aktualisiert (351 Dateien)"

# Lock-Dateien entfernen
find "$BASE/.git" -name "*.lock" -delete 2>/dev/null

commit_repo() {
    local dir="$1"
    local name="$2"
    cd "$dir" || return
    find .git -name "*.lock" -delete 2>/dev/null
    local count=$(git status --short | wc -l | tr -d ' ')
    if [ "$count" -gt "0" ]; then
        git add -u
        git commit -m "$MSG

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>"
        echo "✅ $name: $count Dateien committed"
    else
        echo "— $name: nichts zu committen"
    fi
}

commit_repo "$BASE"                              "B2"
commit_repo "$BASE/htmlS/B1.1"                  "B1"
commit_repo "$BASE/htmlS/A2.1"                  "A2"
commit_repo "$BASE/htmlS/A1.1 NEW"              "A1"
commit_repo "$BASE/htmlS/C1"                    "C1"
commit_repo "$BASE/daf-materialien"             "daf-materialien"
commit_repo "$BASE/htmlS/Architektur"           "Architektur"
commit_repo "$BASE/htmlS/Lückentexte Mattmüller" "Lückentexte"

echo ""
echo "🎉 Fertig! Alle Repos committed."
read -p "Enter zum Schließen..."
