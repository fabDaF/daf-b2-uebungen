# Lückentext — Plan zur verlässlichen Kanonisierung

Stand: 2026-06-30 · Status: **Beide B1-Piloten abgenommen (1057X Wortschatz, 3065G Grammatik) — kanonische Form bestätigt; G-Durchstreichen bestätigt** · Autor: Claude, mit Frank

Ziel: Die kanonische Lückentext-Form so verankern, dass (a) sie bei **neuen**
Lektionen 100 % zuverlässig automatisch entsteht und (b) bei **bestehenden**
Lektionen kein wiederkehrendes Nachkorrigieren mehr nötig ist. Vorbild ist die
funktionierende **Genus-Disziplin**: eine Regel, *ein* Produzent, *ein* strenges Gate
— alle drei zeigen auf genau dieselbe Form.

---

## 0. Die kanonische Form (Quelle der Wahrheit)

Ein Lückentext ist ein **zusammenhängender Story-Text** mit Lücken:

- **Inhalt:** durchlaufender, kohärenter Text (Story) — **keine** isolierten Einzelsätze.
- **Keine Nummerierung** (Regel vom 2026-06-19 bleibt voll erhalten — Nummern passen nur
  zu Einzelsätzen, die wir gerade nicht wollen).
- **Serifenschrift** im gesamten Lückentext-Fließtext, **inklusive Eingabefelder**
  (Georgia, "Times New Roman", serif).
- **Genau 10 Lücken** pro Lückentext (verbindlich, Frank 2026-06-30) — mechanisch vom
  Gate erzwingbar, analog zur Genus-Mindestzahl.
- **Darstellung wie Form 3 / `7001V`:** native Wortbank, `.used`-Durchstreichen bei
  richtiger Eingabe, **case-sensitives Live-Feedback** bei jedem Tastendruck, **kein**
  Prüfen-Button, mitwachsende `ch`-Feldbreite, leerer Placeholder, drei Zustände
  (neutral / grün / rot nach Präfix-Regel).
- **Zwei Varianten:**
  - **Wortschatz (V/R/X):** Wortbank zeigt die **Vollformen** = die Antworten
    (`data-ans`). Lerner erinnert das Wort.
  - **Grammatik (G):** Wortbank zeigt die **Grundform/Infinitiv** (separates Attribut,
    z. B. `data-base`); die konjugierte/deklinierte **Zielform wird nie sichtbar**.
    Kein Durchstreichen.

Zwei Begriffe von „richtig", strikt getrennt:

- **Mechanisch** (Engine, Serif, keine Nummern, Wortbank-Verhalten, Varianten-Logik)
  → per Produzent + Gate **erzwingbar**, also gegen Drift abgesichert.
- **Redaktionell** (der Inhalt ist eine echte Story) → **Autorenarbeit**, nicht
  skriptbar. Garantie für **neue** Lektionen über das Skill; bei **Altbeständen** gilt:
  **jeder Lückentext ohne Story wird mit Story NEU gebaut** — nicht bloß mechanisch
  geflickt.

**Grundsatz (Frank, 2026-06-30):** Die Story ist das **pädagogisch wertvollste
Element** des Lückentexts. Darauf wird nicht verzichtet; es werden **keine
zusammenhanglosen Einzelsätze** komponiert. Wo ein bestehender Lückentext keine Story
hat, ist ein **redaktioneller Neubau mit Story** Pflicht, kein optionaler Feinschliff.

---

## 1. Vorhandene Bausteine (wir bauen darauf auf, kein Greenfield)

- `LUECKENTEXT-SKILL-SPEC.md` (v1.0) — Spec, wird auf die neue Form aktualisiert.
- `LUECKENTEXT-BEISPIEL.html` — Referenz, wird **storybasiert neu gebaut**
  (bisher Einzelsatz-Karten → das ist genau das, was wir ablösen).
- `scripts/lt-v1-module.js` + `scripts/inject_lt_v1.py` — Engine + Produzent
  (FB-LT-V1), werden zur kanonischen Engine weiterentwickelt.
- `scripts/check_wortbank.py` — heutiges Gate, **permissiv** (akzeptiert jede
  Worthilfe; daher die sechs Sonderfall-Hacks A–F). Wird zum **strengen Form-Gate**.

Drei konkurrierende Engines koexistieren heute (Drift-Ursache): graues
`FB-WORTBANK-MODULE` (124 Dateien in htmlS), `FB-LT-V1` (75), handgeschrieben
`initWortbank`/`buildWordBank` (134); 26 Dateien tragen sogar zwei gleichzeitig.

---

## 2. Phasen

### Phase 0 — Spec + Golden Reference
- `LUECKENTEXT-SKILL-SPEC.md` auf die kanonische Form (Abschnitt 0) aktualisieren:
  exakter Markup-Vertrag (Klassen, `data-ans`/`data-base`, Marker, Container-Struktur),
  storybasiert, serif, keine Nummern, beide Varianten.
- `LUECKENTEXT-BEISPIEL.html` **storybasiert neu bauen**: eine kurze Wortschatz-Story
  (V/R/X) und eine kurze Grammatik-Story (G), beide serif, ohne Nummern.
- **Inventur:** Lückentext-Tabs projektweit zählen und grob klassifizieren —
  **Story** (nur mechanischer Feinschliff nötig) vs. **Nicht-Story** (Einzelsätze/
  Liste/nummeriert → redaktioneller Neubau nötig). So kennen wir den Umfang der
  Neubau-Kampagne in Phase 5, bevor wir sie beginnen. Heuristik, mensch-bestätigbar.
- **Erfolgskriterium:** Referenz öffnet im Browser; beide Varianten funktionieren;
  Serif sichtbar; keine Nummern; Wortbank befüllt; Live-Feedback korrekt; G zeigt nie
  die Zielform. Inventur-Zahl (Story vs. Nicht-Story) liegt vor.

### Phase 1 — Eine Engine, ein Produzent
**Beleg, warum nötig (2026-06-30):** Schon die zwei Pilote zeigten beginnenden Drift —
1057X nutzte `initLueckentext`/`liveCheckLuecke`, 3065G `buildWortbankG`/`liveCheckG`.
Per-Datei-Handeinbau driftet sofort; deshalb EINE Engine-Quelle + Produzent vor jedem
Rollout (sonst 746 leicht verschiedene Engines).

- **Engine als einzige Quelle: `scripts/lt-story-engine.js` (ERLEDIGT 2026-06-30).**
  Erkennt die Variante SELBST: hat eine Lücke `data-base` → Grammatik (Wortbank =
  Grundform, Zielform nie sichtbar), sonst Wortschatz (Wortbank = `data-answer`).
  Serif, `ch`-Breite, `.used` (G per data-base), case-sensitives Live-Feedback,
  idempotent, selbst-installierend; Timer über generische Hooks. Enthält die kanonische
  CSS als Kommentar-Block (Produzent spielt sie mit ein). JS-Parse ✓.
- **Produzent `inject_lt.py` (NÄCHSTER SCHRITT):** spielt Engine + CSS + Wortbank-
  Container + Story-Gerüst idempotent ein (wie `inject_genus.py`), verdrahtet die
  Timer-Hooks auf den richtigen Tab-Index, **bricht ab** bei unbekanntem Layout,
  **bewahrt** vorhandene Story-Inhalte, **entfernt** konkurrierende Alt-Engines/leaky
  wortkasten. Re-Lauf vereinheitlicht auch die zwei Pilot-Engines (Drift beheben).
- **Erfolgskriterium:** Produzent auf einer /tmp-Kopie einer Backlog-B1-Datei spielt die
  kanonische Engine + Gerüst ein (gate-strukturkonform); die zwei Pilote nach Re-Lauf
  weiterhin Gate-✓ mit unveränderter Story; JS parst; Browser-Stichprobe grün.

### Phase 2 — Ein strenges Gate
- `check_lueckentext.py` (bzw. Umbau von `check_wortbank.py`): **schlägt fehl**, wenn ein
  Lückentext-Tab nicht der kanonischen Form entspricht — kanonischer Engine-Marker
  vorhanden, **keine** konkurrierende Engine, keine Nummerierung, Serif auf
  Story-Container + Inputs, Wortbank zur Laufzeit befüllt, G-Variante baut aus
  `data-base` (kein Zielform-Leak). Heuristik „storybasiert, nicht Einzelsätze/
  nummeriert" als ehrlicher Warn-Check (mensch-bestätigbar, wie `check_banner_faces.py`).
- In die Pre-Commit-Kette aufnehmen (neben `check_serif.py`, `check_genus.py` …).
- **Nebeneffekt:** Weil nur noch *eine* Form erlaubt ist, werden die sechs
  Sonderfall-Hacks (A–F) mit der Zeit überflüssig.
- **Erfolgskriterium:** Gate grün auf Golden Reference, rot auf einer bekannten
  grauen/nativen/nummerierten Datei; in der Commit-Routine verankert.

### Phase 3 — Praxis-Pilot zuerst (erst produzieren, dann codifizieren)
**Bewusst VOR dem Skill.** Ein Skill soll ein *bewährtes* Muster destillieren, kein
theoretisches. Schreiben wir es zu früh, gießen wir meine Vermutungen (und Fehler) in
Stein — und produzieren danach hundert Lektionen mit demselben Denkfehler. Die
Pilot-Lektionen sind der **Test**, den das Skill braucht, bevor es existiert.
- Je eine V/R/X- und eine G-Lektion auf die kanonische Story-Form bringen
  (Produzent + redaktioneller Story-Aufbau), Gate laufen lassen, im Browser
  verifizieren, dir zur Abnahme zeigen.
- Das **Skill wird hier noch nicht gebaut** — erst Erfahrung sammeln.
- Erfahrungen gegen diesen Plan abgleichen; Spec/Engine/Gate/Plan anpassen, wo nötig.
- **Erfolgskriterium:** beide Piloten live und von dir abgenommen; Lehren eingearbeitet.

### Phase 4 — Ein eigenes Skill `daf-lueckentext` (aus dem bewährten Piloten destilliert)
Jetzt — und erst jetzt — codifizieren wir, was sich im Piloten bewährt hat. Heute ist das
Lückentext-Wissen über mehrere Skills **verstreut** (`daf-kern §7`, Teile in
`daf-uebungsformen`, `daf-grammatik`) — dieselbe „kein Zuhause"-Krankheit wie bei den drei
Engines. Lösung wie bei `daf-satzbau` / `daf-schreibwerkstatt`: **ein eigenes Skill.**

- **Neues Skill `daf-lueckentext`** als das *einzige* Zuhause der kanonischen Form:
  Markup-Vertrag, beide Varianten, Engine/Produzent/Gate-Verweise, Story-Direktive,
  keine Nummern, Serif. Es verweist auf `LUECKENTEXT-SKILL-SPEC.md` als Detail-Contract.
- **Bruchstücke herauslösen:** Lückentext-Teile aus `daf-kern §7`, `daf-uebungsformen`
  und `daf-grammatik` entfernen und durch einen **Einzeiler-Verweis** auf
  `daf-lueckentext` ersetzen. Die drei Skills werden dadurch **kleiner und
  übersichtlicher** (Frank-Ziel: weniger Umfang = leichtere Arbeit; deckt sich mit der
  skill-verwaltung-Regel „SKILL.md < 500 Zeilen").
- **Koordiniert** ausführen, damit das Wissen nie „heimatlos" ist: das neue Skill steht,
  bevor die Bruchstücke aus den alten entfernt werden.
- **Mechanik (skill-verwaltung):** je Skill eine Arbeitskopie bearbeiten →
  `python -m scripts.package_skill <skill> /tmp` → `.skill` in den Output-Ordner →
  dir je einen **Installations-Link** geben (ein Klick installiert). Skills sind aus der
  Session read-only; das Verpacken/Übergeben bereite ich vor, die Installation machst du.
- `CLAUDE.md`: kanonischen Lückentext-Abschnitt ergänzen (analog zu Genus/Nav) —
  Regel + Produzent + Gate. Sofort editierbarer, dauerhafter Anker; bei Widerspruch gilt
  CLAUDE.md, das Skill wird nachgezogen (etablierte Projekt-Konvention).
- **Erfolgskriterium:** `daf-lueckentext` installiert; die drei alten Skills enthalten nur
  noch den Verweis und sind kürzer; eine *neu* nach Skill gebaute Lektion bekommt den
  kanonischen Story-Lückentext automatisch und besteht das Gate **ohne Nachkorrektur**.

### Phase 5 — Rollout (erst nachdem der Pilot sitzt)
Zwei Spuren, je nach Inventur-Klasse:

- **Spur A — Story vorhanden, Mechanik alt:** mechanischer Sweep (skriptbar, sicher,
  HEAD-basierte Commits): Engine vereinheitlichen, Serif setzen, Nummern raus, Wortbank
  korrekt. Schnell und risikoarm.
- **Spur B — keine Story (Einzelsätze/Liste/nummeriert):** **redaktioneller Neubau mit
  Story.** Das ist Autorenarbeit pro Lektion, kein Skript — eine **anhaltende Kampagne**.
  Ehrliche Größenordnung: potenziell dreistellig (genaue Zahl aus der Inventur in
  Phase 0). Priorisiert (z. B. nach Niveau/Nutzung); das Gate flaggt Nicht-Story-Fälle
  und führt die Warteschlange. **Keine zusammenhanglosen Sätze** — lieber langsamer und
  mit echter Story.
- **Erfolgskriterium:** Gate projektweit grün für die mechanischen Dimensionen
  (Spur A erledigt); Story-Backlog (Spur B) sichtbar, priorisiert und schrumpfend.

---

## 3. Annahmen (bitte gegenprüfen)

1. Wir **entwickeln die vorhandenen Bausteine weiter** statt neu anzufangen (Spec,
   Beispiel, lt-v1-module, inject_lt_v1, check_wortbank).
2. G-Lücken tragen ein eigenes **`data-base`** (Grundform) für die Wortbank; die
   Zielform bleibt nur in `data-ans` zum Prüfen.
3. **Storybasiert** ist bei Altbeständen **redaktionell** (Neubau mit Story), nicht per
   Skript erzwingbar; das Gate kann es nur *flaggen*, nicht *reparieren*. Nicht-Story-
   Altbestände werden **neu gebaut**, nicht übersprungen — als priorisierte Kampagne.
4. Lückentext bekommt ein **eigenes Skill `daf-lueckentext`**; die Bruchstücke werden aus
   `daf-kern §7` / `daf-uebungsformen` / `daf-grammatik` herausgelöst (Skills werden
   kleiner). Skill-Edits laufen über `skill-verwaltung` (Arbeitskopie → `.skill` →
   Installations-Link); `CLAUDE.md` ist der sofortige, autoritative Anker.
5. Reihenfolge ist **Pilot vor Rollout** — kein Massenlauf, bevor eine echte Lektion
   im Unterricht überzeugt hat.

---

## 4. Was diesen Plan vom alten Zustand unterscheidet

Heute: drei Engines, ein permissives Gate, ein Spec ohne Durchsetzung → Drift.
Nach dem Plan: eine Engine, ein Produzent, ein strenges Gate, eine in CLAUDE.md/Skill
verankerte Direktive → die Form **kann gar nicht mehr abweichen**, ohne dass das Gate
rot wird. Genau die Mechanik, die Genus heute zuverlässig macht.
