#!/usr/bin/env python3
"""
verify_manifest.py — Prüft die IST-Welt gegen die SOLL-Welt aus MANIFEST.yaml.

Dieses Skript ist das Herz der fabDaF-Integritätssicherung. Es liest
MANIFEST.yaml und verifiziert für jedes dort gelistete Repo, ob die
Realität damit übereinstimmt.

Exit-Codes:
    0  — alles grün (alle Repos passen, alle known_issues entweder ignoriert
         oder noch offen aber dokumentiert)
    1  — mindestens ein unerwarteter Drift gefunden
    2  — MANIFEST.yaml fehlt oder ist kaputt

Aufruf:
    python3 scripts/verify_manifest.py           # kurze Ausgabe
    python3 scripts/verify_manifest.py --verbose # detailliert
    python3 scripts/verify_manifest.py --json    # maschinenlesbar
"""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    sys.stderr.write(
        "FEHLER: Python-Paket 'pyyaml' fehlt. Installation:\n"
        "    pip3 install pyyaml --break-system-packages\n"
    )
    sys.exit(2)


# ─── Hilfsfunktionen ──────────────────────────────────────────────────────

def run(cmd: list[str], cwd: Path) -> tuple[int, str, str]:
    """Führt einen Shell-Befehl aus und gibt (rc, stdout, stderr) zurück."""
    try:
        proc = subprocess.run(
            cmd, cwd=cwd, capture_output=True, text=True, timeout=30
        )
        return proc.returncode, proc.stdout.strip(), proc.stderr.strip()
    except Exception as e:
        return 1, "", str(e)


def strip_pat(url: str) -> str:
    """Entfernt Personal Access Token aus einer GitHub-Remote-URL."""
    # https://ghp_xxx@github.com/... → https://github.com/...
    return re.sub(r"https://[^@]+@github\.com/", "https://github.com/", url)


def normalize_remote(url: str) -> str:
    """Normalisiert eine Remote-URL für den Vergleich (strippt .git am Ende)."""
    url = strip_pat(url).rstrip("/")
    if url.endswith(".git"):
        url = url[:-4]
    return url.lower()


# ─── Prüfungen ────────────────────────────────────────────────────────────

class Finding:
    """Ein einzelner Befund: Info, Warnung, Fehler."""

    LEVELS = {"ok": 0, "info": 1, "warn": 2, "error": 3}

    def __init__(self, repo: str, level: str, message: str):
        self.repo = repo
        self.level = level
        self.message = message

    def __repr__(self):
        return f"[{self.level.upper():5s}] {self.repo}: {self.message}"


def check_repo(key: str, spec: dict, root: Path) -> list[Finding]:
    """Prüft ein einzelnes Repo aus dem Manifest gegen die Realität."""
    findings: list[Finding] = []
    local_path = root / spec["local_path"]

    # 1. Existiert der Pfad?
    if not local_path.exists():
        findings.append(Finding(key, "error", f"lokaler Pfad fehlt: {local_path}"))
        return findings

    # 2. Ist es ein Git-Repo?
    git_dir = local_path / ".git"
    if not git_dir.exists():
        findings.append(Finding(key, "error", f"kein .git-Ordner in {local_path}"))
        return findings

    # 3. Remote-URL matches?
    rc, actual_remote, err = run(["git", "remote", "get-url", "origin"], local_path)
    if rc != 0:
        findings.append(Finding(key, "error", f"git remote get-url fehlgeschlagen: {err}"))
    else:
        expected = normalize_remote(spec["remote_url"])
        actual = normalize_remote(actual_remote)
        if expected != actual:
            findings.append(Finding(
                key, "error",
                f"Remote-URL weicht ab: erwartet {expected}, ist {actual}"
            ))

    # 4. HEAD synchron mit origin/main?
    rc, local_head, _ = run(["git", "rev-parse", "HEAD"], local_path)
    rc2, remote_head, _ = run(["git", "rev-parse", "origin/main"], local_path)
    if rc == 0 and rc2 == 0:
        if local_head != remote_head:
            findings.append(Finding(
                key, "warn",
                f"HEAD nicht synchron mit origin/main (lokal {local_head[:8]}, remote {remote_head[:8]})"
            ))
    else:
        findings.append(Finding(key, "warn", "konnte HEAD oder origin/main nicht lesen"))

    # 5. Tracked files Mindestanzahl
    expected = spec.get("expected", {})
    if "tracked_files_min" in expected:
        rc, out, _ = run(["git", "ls-files"], local_path)
        if rc == 0:
            count = len([l for l in out.split("\n") if l.strip()])
            if count < expected["tracked_files_min"]:
                findings.append(Finding(
                    key, "warn",
                    f"nur {count} tracked files, erwartet min. {expected['tracked_files_min']}"
                ))

    if "html_files_min" in expected:
        rc, out, _ = run(["git", "ls-files", "*.html"], local_path)
        if rc == 0:
            count = len([l for l in out.split("\n") if l.strip()])
            if count < expected["html_files_min"]:
                findings.append(Finding(
                    key, "warn",
                    f"nur {count} getrackte HTML-Dateien, erwartet min. {expected['html_files_min']}"
                ))

    if not findings:
        findings.append(Finding(key, "ok", "alles passt"))
    return findings


def check_dashboards(manifest: dict, root: Path) -> list[Finding]:
    """
    Prüft alle dashboard.html-Dateien im Projekt: Jede basis-URL muss
    entweder auf ein Manifest-Repo zeigen oder ein known_issue sein.
    """
    findings: list[Finding] = []
    expected_urls = set()
    for key, spec in manifest["repos"].items():
        if spec.get("dashboard_basis"):
            expected_urls.add(spec["dashboard_basis"].rstrip("/"))

    # known_issues: orphan wkv darf im dashboard stehen, solange als known_issue dokumentiert
    known_orphans = set()
    for issue in manifest.get("known_issues", []):
        if "daf-wkv" in issue.get("description", "").lower():
            known_orphans.add("https://fabdaf.github.io/daf-wkv-uebungen")

    dashboards = list(root.glob("**/dashboard.html"))
    pattern = re.compile(r"basis:\s*'([^']+)'")

    for dash in dashboards:
        if ".git" in dash.parts:
            continue
        try:
            content = dash.read_text(encoding="utf-8", errors="replace")
        except Exception as e:
            findings.append(Finding("dashboard", "warn", f"{dash.name}: konnte nicht lesen: {e}"))
            continue
        for match in pattern.finditer(content):
            url = match.group(1).rstrip("/")
            if url in expected_urls or url in known_orphans:
                continue
            findings.append(Finding(
                "dashboard", "error",
                f"{dash.relative_to(root)}: basis-URL '{url}' gehört zu keinem Manifest-Repo"
            ))

    if not any(f.level == "error" for f in findings):
        findings.append(Finding("dashboard", "ok", f"{len(dashboards)} Dashboards geprüft, alle basis-URLs aufgelöst"))

    return findings


def check_deprecated_not_in_use(manifest: dict, root: Path) -> list[Finding]:
    """Prüft, ob deprecated Repos noch irgendwo lokal oder im Dashboard auftauchen."""
    findings: list[Finding] = []
    deprecated = manifest.get("deprecated_repos", [])
    for dep in deprecated:
        name = dep["name"]
        # Noch als lokaler Ordner vorhanden?
        hits = list(root.glob(f"**/{name}/.git"))
        hits = [h for h in hits if ".git" not in h.parent.parent.parts[-2:]]
        if hits:
            findings.append(Finding(
                "deprecated", "warn",
                f"deprecated Repo '{name}' existiert noch lokal: {hits[0].parent}"
            ))
    if not findings:
        findings.append(Finding("deprecated", "ok", f"{len(deprecated)} deprecated Repos geprüft, keine lokalen Rückstände"))
    return findings


# ─── Haupt-Logik ──────────────────────────────────────────────────────────

def main() -> int:
    parser = argparse.ArgumentParser(description="Verifiziert fabDaF gegen MANIFEST.yaml")
    parser.add_argument("--verbose", "-v", action="store_true", help="Zeige auch 'ok'-Befunde")
    parser.add_argument("--json", action="store_true", help="Gib Ergebnis als JSON aus")
    parser.add_argument("--manifest", default=None, help="Pfad zu MANIFEST.yaml (default: autodetect)")
    args = parser.parse_args()

    # Manifest-Pfad finden
    script_dir = Path(__file__).resolve().parent
    root = script_dir.parent  # scripts/ liegt unter dem Root
    manifest_path = Path(args.manifest) if args.manifest else root / "MANIFEST.yaml"

    if not manifest_path.exists():
        sys.stderr.write(f"FEHLER: MANIFEST.yaml nicht gefunden unter {manifest_path}\n")
        return 2

    try:
        with open(manifest_path, encoding="utf-8") as f:
            manifest = yaml.safe_load(f)
    except Exception as e:
        sys.stderr.write(f"FEHLER: MANIFEST.yaml nicht parsebar: {e}\n")
        return 2

    all_findings: list[Finding] = []

    # Repo-Checks
    for key, spec in manifest["repos"].items():
        all_findings.extend(check_repo(key, spec, root))

    # Dashboard-Checks
    all_findings.extend(check_dashboards(manifest, root))

    # Deprecated-Checks
    all_findings.extend(check_deprecated_not_in_use(manifest, root))

    # Zusammenfassung
    counts = {"ok": 0, "info": 0, "warn": 0, "error": 0}
    for f in all_findings:
        counts[f.level] = counts.get(f.level, 0) + 1

    if args.json:
        output = {
            "manifest": str(manifest_path),
            "counts": counts,
            "findings": [
                {"repo": f.repo, "level": f.level, "message": f.message}
                for f in all_findings
            ],
            "known_issues": manifest.get("known_issues", []),
        }
        print(json.dumps(output, indent=2, ensure_ascii=False))
    else:
        print(f"\n─── fabDaF Manifest-Verifikation ───────────────────────────")
        print(f"Manifest: {manifest_path}")
        print(f"Root:     {root}")
        print()
        for f in all_findings:
            if f.level == "ok" and not args.verbose:
                continue
            symbol = {"ok": "✓", "info": "i", "warn": "⚠", "error": "✗"}[f.level]
            print(f"  {symbol} {f.repo:25s} {f.message}")

        print()
        print(f"Zusammenfassung: "
              f"{counts['ok']} OK, {counts['warn']} Warnungen, {counts['error']} Fehler")

        issues = manifest.get("known_issues", [])
        if issues:
            print(f"\n{len(issues)} dokumentierte known_issues (werden nicht als Fehler gewertet):")
            for issue in issues:
                print(f"  • [{issue['severity']:6s}] {issue['id']}")

        print()

    return 1 if counts["error"] > 0 else 0


if __name__ == "__main__":
    sys.exit(main())
