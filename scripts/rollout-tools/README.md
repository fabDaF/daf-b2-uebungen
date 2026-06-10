# Rollout-Werkzeuge Gerüst-Modus (Stand 2026-06-10)

Workflow pro Einheit (siehe scripts/GERUEST-ROLLOUT-PLAN.md):

1. `node triage.js <DIR> '^DE_C1_204' 12 18` — zeigt nur defiziente Sätze
2. Fix-Skript nach Muster `BEISPIEL_fix-batch.js` schreiben
   (applyFix aus apply_lib2.js; C1: min 12 / max 18, B-Niveaus siehe Staffel)
3. `node scripts/geruest_patch.js DATEI --write` pro Datei
4. `VDIR=<DIR> node verify_geruest.js DATEI1 DATEI2 …`
5. `python3 scripts/check_wortbank.py` + `check_serif.py`
6. `node jsdom_test_geruest.js DATEI` (braucht /tmp/node_modules/jsdom:
   `cd /tmp && npm install jsdom --silent`)
7. `scripts/safe-commit.sh "msg" DATEIEN` aus dem jeweiligen Repo-Root

Satzregeln: 12 Wörter Minimum (ohne Satzzeichen-Chips), Maximum je Niveau
(B1: 14, B2: 16, C1/C2: 18), Komma-Chip Pflicht, ein Wort pro Chip,
Nomen groß / Rest klein, punct-Feld für ?/!.
