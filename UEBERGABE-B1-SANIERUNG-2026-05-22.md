# Übergabe — B1-Sanierung

**Datum:** 2026-05-22
**Vorgänger-Session:** Skill-Audit, Karim-Charakterbibel, Pilot 3064X, Wortbank-Korrektur
**Stand:** Phase 0 abgeschlossen, Phase 1 startbereit

## Was du sofort wissen musst

**Frank ist DaF-Lehrer, kein Entwickler.** Er will Prosa, keine Bullet-Wüsten, keine Präambel, direkten Ton. Er pflegt die durchgehende Figur **Karim Benali** durch das ganze B1-Curriculum — junger marokkanischer Ingenieur aus Casablanca, arbeitet bei E.ON in Düsseldorf, Kollegen Stefan Meier / Elena Stojanovic / Hiroshi Tanaka. Die vollständige Charakterbibel liegt in `daf-lesetext/references/karim-universe.md`. **Lies sie vor dem ersten Karim-Text.**

Karim ist nicht überall, aber überall, wo es das Lingoda-Thema natürlich trägt. Eine Lektion wie 3064X „Das Aussehen beschreiben" hat Karim *nicht* (themenzentriert), die meisten R-Dateien *haben* Karim (erzählerisch).

## Drei nicht verhandelbare Regeln seit heute

**Erstens — Wortbank ist sichtbar, aber nicht klickbar.** Die alte `daf-kern §7` schrieb klickbare Wortbänke vor, das war falsch. Frank will, dass der Schüler **maximal schreibt**. Wortbank ist nur eine Lese-Hilfe (welche Wörter kommen in die Lücken), die Schreibleistung bleibt beim Lerner.

```javascript
// RICHTIG: span, kein click-Handler
var chip = document.createElement('span');
chip.className = 'wort-chip';
chip.textContent = w;
// KEIN addEventListener('click', ...)

// FALSCH (alte Version, in vielen Dateien noch drin):
var btn = document.createElement('button');
btn.addEventListener('click', function(){ insertWordFromBank(w); });
```

**Zweitens — Live-Feedback ist case-sensitive Präfix-Check.** Frank will, dass Groß-/Kleinschreibung geübt wird.

```javascript
function lueckeCheck(inp) {
  var val = inp.value;                  // KEIN .trim()
  var ans = inp.dataset.answer;
  inp.classList.remove('ok', 'wrong');
  if (!val) return;
  if (val === ans) inp.classList.add('ok');           // grün
  else if (!ans.startsWith(val)) inp.classList.add('wrong');  // rot
  // korrekter Präfix bleibt neutral (schwarz)
}
```

Drei Zustände: leer/korrekter Präfix = schwarz, falsches Zeichen = rot, exakt korrekt = grün.

**Drittens — Karim-Lesetexte sind konzis: 220–350 Wörter, eine bis zwei Szenen ohne römische Nummerierung, ein bis drei kurze Dialogwechsel.** Die alte Voice-Lock-Angabe „600–800 Wörter, 3–5 Szenen mit römischen Ziffern" ist überholt — `daf-lesetext` SKILL.md §8 wurde heute aktualisiert.

## Aktueller Skill-Stack (alle gepackt in `/Users/frankburkert/Cowork/Projekte/fabDaF/skills/`)

| Skill | Stand | Was geändert |
|-------|-------|--------------|
| `daf-kern.skill` | v2 | §7 Wortbank visuell statt klickbar, case-sensitive Präfix-Check |
| `daf-lesetext.skill` | v2 | Karim-Voice-Lock auf 220–350 Wörter aktualisiert, Charakterbibel als Referenz |
| `daf-textarbeit.skill` | v2 | 8-Tab-Standard (statt 6), Pflicht-Anbindung an daf-schreibwerkstatt |
| `daf-disziplin.skill` | v2 | Schlanke Verweisdatei, ergänzt arbeitsdisziplin |

Frank installiert diese vier Skills. Wenn du in einer neuen Session siehst, dass die installierten Skills älter sind als diese MD, sag Frank Bescheid — möglicherweise hat er die Installation noch nicht gemacht.

## Was als Nächstes zu tun ist

Der vollständige Sanierungsplan liegt im Kontext der letzten Session (suche „Sanierungsplan B1.1 + B1.2 + B1.3"). Die Kurzfassung:

**Phase 1 (eine Session, ~4 Stunden) — Mass-Cleanup per Skript.** Drei Skripte über alle 151 B1-Dateien:

1. **Bad-Quotes-Fix:** Regex `„([^„"""\n]{1,80})"` → schließendes `"` durch `"` ersetzen. 536 Treffer in 90 Dateien.
2. **vocab-item → initWortschatz-Migration:** Klassenumbenennung + Funktionsumbenennung + Daten-Adapter. 54 Dateien.
3. **Wortbank: klickbar → visuell.** `<button>` zu `<span>`, click-Handler raus, case-sensitive Präfix-Check in `lueckeCheck`. Etwa 70 Dateien.

Skripte gegen 3–4 Stichproben entwickeln, dann über das Repo laufen, in einem Schwung committen. Pro Schritt eigenes Skript, damit du sauber rollback kannst.

**Phase 2 (4–5 Sessions) — B1.1 inhaltlich sanieren.** Lesetexte umschreiben im Karim-Stil, X-Dateien auf 8-Tab-Struktur heben. Lingoda-PDFs liegen unter `quelltexte/B 1.1/`.

**Phase 3 (4–5 Sessions) — B1.2 inhaltlich sanieren.** Gleiche Struktur.

**Phase 4 (2–3 Sessions) — B1.3 inhaltlich sanieren.** Schon zur Hälfte modern, weniger Arbeit.

**Phase 5 (1 Session) — Abschluss-Verifikation.** daf-audit über alle 151, Dashboard-Update.

## Vier offene Frank-Entscheidungen

Frank hat sich am Ende der letzten Session noch nicht entschieden zu:

1. **Beginne ich Phase 1 sofort** oder warten wir, bis Frank weitere strategische Punkte ergänzt?
2. **Pro Session eine ganze Einheit** (8 Lektionen, didaktisch geschlossen) oder **3–4 Lektionen aus verschiedenen Einheiten** (Karim chronologisch parallel)?
3. **Bei den drei thematisch falschen Lektionen** (3062G „Komparativ und Superlativ" statt „Verschiedene Bedeutungen des Verbs werden", 3065G „Adjektivdeklination" statt dito, 3067X „Kosmetik" statt „Emotionen ausdrücken"): am Lingoda-Original ausrichten (umbenennen) oder Datei-Titel behalten?
4. **Bericht-Rhythmus:** nach jeder fertigen Einheit oder erst nach jeder Phase?

Wenn Frank dir in der ersten Nachricht „los" sagt ohne diese vier Fragen zu beantworten, frag explizit nach. Antworten aus dieser MD übernehmen ist nicht zulässig — das sind Frank-Entscheidungen.

## Bekannte Stolperfallen aus der letzten Session

**Repo-Struktur:** Das fabDaF-Repo besteht aus 9 Git-Submodulen (siehe `CLAUDE.md` und `MANIFEST.yaml`). B1-Dateien liegen in `htmlS/B1.1/` (das ist das `daf-b1-uebungen`-Repo trotz des `.1` im Pfad — siehe Manifest).

**Commit-Workflow:** Direkter `git commit` schlägt aus der Sandbox fehl wegen APFS-Lock-Problem. Immer `scripts/safe-commit.sh "msg" datei1 [datei2 …]` verwenden, das umgeht das. Nach dem Push HEAD-Vergleich mit Remote machen, weil die Warnung „Operation not permitted" über `.git/objects/*/tmp_obj_*` kosmetisch ist.

**Schreib-Tool und `.git/`:** Niemals das Write-Tool für Pfade unter `.git/` benutzen — das löst einen Cowork-Permission-Dialog aus, der im Hintergrund blockiert und stundenlang wartet.

**Sandbox-Credentials pro Session:** Beim ersten Push einer frischen Session `bash scripts/setup-sandbox-credentials.sh` aus dem Repo-Root laufen lassen.

**Skill-Update-Workflow:** Arbeitskopie in `/tmp/skill-work/<name>/` anlegen (via Python-Filecopy, nicht `cp -r` wegen Read-only-Mauer), bearbeiten, dann `python -m scripts.package_skill /tmp/skill-work/<name> /tmp/` aus dem `/sessions/elegant-gracious-mccarthy/mnt/.claude/skills/skill-verwaltung/`-Verzeichnis aufrufen. Die `.skill`-Datei dann ins `fabDaF/skills/`-Verzeichnis kopieren und Frank per `mcp__cowork__present_files` zum Installieren geben.

**Pexels-Bilder:** Sind in der Cowork-Sandbox blockiert (Egress-Proxy). Für Banner immer entweder die Lingoda-PDFs mit `pdfimages` extrahieren, das Bilder-Cache-Verzeichnis (`.bilder-cache/`) nutzen, oder Frank explizit nach passenden Bildern fragen. Memory-Eintrag „Pexels Chrome-Pflicht": jede Pexels-ID vor Commit per Chrome-MCP Batch-Fetch verifizieren.

**Browser-Cache nach Deploy:** GitHub Pages braucht 30–90 Sekunden nach Push, bis Updates live sind. Cache-Buster `?v=…` in der URL hilft, aber zusätzlich `sleep 30` vor dem Browser-Test einplanen.

## Erste konkrete Aufgabe für die nächste Session

Wenn Frank sagt „los" oder ähnliches:

1. Lies `CLAUDE.md`, `MEMORY.md` und diese Übergabe-MD.
2. Frag Frank die vier offenen Entscheidungen aus „Vier offene Frank-Entscheidungen" oben.
3. Wenn Frank Phase 1 freigibt, baue das Bad-Quotes-Fix-Skript zuerst, lass es gegen drei Stichproben laufen, lass es Frank kurz verifizieren, dann über alle 90 Dateien.
4. Danach das vocab-item-Skript, gleicher Workflow.
5. Danach das Wortbank-Klick→visuell-Skript, gleicher Workflow.
6. Commit pro Skript-Lauf eigener Commit mit klarer Message. Nicht alle drei zusammen.
7. Nach Phase 1: kurzer Status an Frank, fragen nach Phase 2-Start.

## Referenzen

- **Sanierungsplan-Volltext:** in der letzten Session-Konversation, Suchbegriff „Sanierungsplan B1.1 + B1.2 + B1.3"
- **Pilot-Datei (Goldstandard):** `https://fabdaf.github.io/daf-b1-uebungen/DE_B1_3064X-aussehen-beschreiben.html`
- **Pilot-Datei lokal:** `htmlS/B1.1/DE_B1_3064X-aussehen-beschreiben.html`
- **Karim-Charakterbibel:** im daf-lesetext.skill enthalten (`references/karim-universe.md`)
- **B1-Inventur als CSV:** `/tmp/b1_audit.csv` (151 Zeilen — vermutlich bei Session-Ende weg, dann neu generieren)
- **B1-Lesetext-Klassifikation:** `/tmp/b1_lesetexte.csv` (18 vorhandene story-texts mit Stilkategorie)

## Vorlage für den Auftakt-Satz an Frank

> Hallo Frank — ich habe die Übergabe gelesen. 3064X ist live, vier Skills sind in deinem skills/-Ordner, die Karim-Charakterbibel steht. Bevor ich mit Phase 1 (Mass-Cleanup über alle 151 Dateien) starte, brauche ich vier Entscheidungen von dir: [vier Fragen]. Sag „los", wenn du die alle beantwortet hast.
