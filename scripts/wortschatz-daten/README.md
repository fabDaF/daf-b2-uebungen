# Wortschatz-Daten

Wortlisten für `scripts/add_wortschatz_tab.py`, eine JSON-Datei je Lektion
(Dateiname = Lektionscode, z. B. `1062G.json`).

Format — schema-adaptiv, so wie die kanonische `initWortschatz` es liest:

```json
[{"type":"n","en":"the note","artikel":"der","de":"Zettel","plural":"Zettel"},
 {"type":"v","en":"to tidy up","de":"aufräumen"}]
```

Die Wörter stammen aus dem Wortfeld der jeweiligen Lektion — in der Regel aus
ihrem Lückentext. Zwölf Einträge, gemischt Nomen und Verben.
