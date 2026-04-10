#!/usr/bin/env python3
"""
render_manifest.py — Generiert MANIFEST.md aus MANIFEST.yaml.

MANIFEST.md ist die menschenlesbare Sicht auf das Manifest.
Wird bei jedem Lauf komplett überschrieben. Quelle bleibt MANIFEST.yaml.
"""
from __future__ import annotations

import sys
from datetime import datetime
from pathlib import Path

try:
    import yaml
except ImportError:
    sys.stderr.write("FEHLER: pyyaml fehlt. pip3 install pyyaml --break-system-packages\n")
    sys.exit(2)


ROLE_LABELS = {
    "niveau_active": "Aktives Niveau",
    "materialien": "Materialien",
    "architektur": "Architektur",
    "spezial": "Spezial",
    "archiv": "Archiv",
}


def render(manifest: dict) -> str:
    lines: list[str] = []
    lines.append("# fabDaF — Manifest (Übersicht)")
    lines.append("")
    lines.append(f"> **Automatisch generiert aus `MANIFEST.yaml`** am "
                 f"{datetime.now().strftime('%Y-%m-%d %H:%M')}. "
                 "Diese Datei nicht direkt editieren — YAML ändern und "
                 "`python3 scripts/render_manifest.py` erneut laufen lassen.")
    lines.append("")
    lines.append(manifest.get("description", ""))
    lines.append("")
    lines.append(f"**Projekt-Root:** `{manifest.get('root_path_absolute', '')}`  ")
    lines.append(f"**Manifest-Version:** {manifest.get('manifest_version', '?')}")
    lines.append("")

    # Grundregeln
    lines.append("## Grundregeln der Struktur")
    lines.append("")
    for rule in manifest.get("rules", []):
        lines.append(f"**{rule['id']}** — {rule['description']}")
        lines.append("")

    # Repos-Tabelle
    lines.append("## Repos im Überblick")
    lines.append("")
    lines.append("| Schlüssel | Rolle | Niveau | Lokaler Pfad | Dashboard-URL | Pages |")
    lines.append("|---|---|---|---|---|---|")
    for key, spec in manifest["repos"].items():
        role = ROLE_LABELS.get(spec.get("role", "?"), spec.get("role", "?"))
        level = spec.get("level", "—")
        path = f"`{spec.get('local_path', '?')}`"
        dash = spec.get("dashboard_basis") or "—"
        if dash != "—":
            dash = f"[{dash.split('//')[-1].rstrip('/')}]({dash})"
        pages = "✓" if spec.get("github_pages", {}).get("enabled") else "✗ (offen)"
        lines.append(f"| `{key}` | {role} | {level} | {path} | {dash} | {pages} |")
    lines.append("")

    # Detailansicht pro Repo
    lines.append("## Details pro Repo")
    lines.append("")
    for key, spec in manifest["repos"].items():
        lines.append(f"### `{key}`")
        lines.append("")
        lines.append(f"_{spec.get('purpose', '')}_")
        lines.append("")
        lines.append(f"- **Lokal:** `{spec.get('local_path', '?')}`")
        lines.append(f"- **Remote:** {spec.get('remote_url', '?')}")
        pages = spec.get("github_pages", {})
        if pages.get("enabled"):
            lines.append(f"- **GitHub Pages:** aktiv unter {pages.get('url', '?')}")
        else:
            lines.append(f"- **GitHub Pages:** ⚠ noch nicht aktiv")
        if spec.get("dashboard_basis"):
            lines.append(f"- **Dashboard basis:** `{spec['dashboard_basis']}`")
        exp = spec.get("expected", {})
        if exp:
            parts = []
            if "tracked_files_min" in exp:
                parts.append(f"≥{exp['tracked_files_min']} tracked files")
            if "html_files_min" in exp:
                parts.append(f"≥{exp['html_files_min']} HTML")
            lines.append(f"- **Erwartung:** {', '.join(parts)}")
        lines.append("")

    # Known issues
    issues = manifest.get("known_issues", [])
    if issues:
        lines.append("## Bekannte offene Punkte")
        lines.append("")
        lines.append("Jeder Eintrag hier ist ein dokumentierter, aber noch nicht behobener Zustand. "
                     "`verify_manifest.py` wertet sie nicht als Fehler, solange sie hier stehen. "
                     "Sobald behoben → aus `MANIFEST.yaml` entfernen und neu rendern.")
        lines.append("")
        by_sev = {"high": [], "medium": [], "low": []}
        for issue in issues:
            by_sev.setdefault(issue.get("severity", "low"), []).append(issue)
        for sev in ["high", "medium", "low"]:
            items = by_sev.get(sev, [])
            if not items:
                continue
            label = {"high": "🔴 Hoch", "medium": "🟡 Mittel", "low": "⚪ Niedrig"}[sev]
            lines.append(f"### {label}")
            lines.append("")
            for issue in items:
                lines.append(f"**{issue['id']}** (seit {issue.get('created', '?')}, "
                             f"Owner: {issue.get('owner', '?')})  ")
                lines.append(f"{issue['description']}")
                lines.append("")

    # Deprecated
    dep = manifest.get("deprecated_repos", [])
    if dep:
        lines.append("## Verworfene Repos")
        lines.append("")
        lines.append("Diese Repos existierten historisch, sind aber nicht mehr Teil der aktiven Struktur. "
                     "Der verify-Skript warnt, falls sie lokal wieder auftauchen.")
        lines.append("")
        lines.append("| Name | Ersetzt durch | Grund |")
        lines.append("|---|---|---|")
        for d in dep:
            lines.append(f"| `{d['name']}` | `{d.get('replaced_by', '—')}` | {d.get('reason', '')} |")
        lines.append("")

    lines.append("---")
    lines.append("")
    lines.append("## Verwendung")
    lines.append("")
    lines.append("**Prüfen:**")
    lines.append("")
    lines.append("```bash")
    lines.append("./scripts/verify_manifest.sh        # kurze Ausgabe")
    lines.append("./scripts/verify_manifest.sh -v     # verbose")
    lines.append("./scripts/verify_manifest.sh --json # JSON für Automatisierung")
    lines.append("```")
    lines.append("")
    lines.append("**Diese Übersicht neu generieren (nach YAML-Änderung):**")
    lines.append("")
    lines.append("```bash")
    lines.append("python3 scripts/render_manifest.py")
    lines.append("```")
    lines.append("")

    return "\n".join(lines)


def main() -> int:
    script_dir = Path(__file__).resolve().parent
    root = script_dir.parent
    yaml_path = root / "MANIFEST.yaml"
    md_path = root / "MANIFEST.md"

    if not yaml_path.exists():
        sys.stderr.write(f"FEHLER: {yaml_path} nicht gefunden\n")
        return 2

    with open(yaml_path, encoding="utf-8") as f:
        manifest = yaml.safe_load(f)

    md = render(manifest)
    md_path.write_text(md, encoding="utf-8")
    print(f"✓ MANIFEST.md geschrieben ({len(md.splitlines())} Zeilen)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
