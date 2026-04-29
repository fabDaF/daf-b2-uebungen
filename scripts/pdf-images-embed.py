#!/usr/bin/env python3
"""
PDF-Bilder-Embed-Pipeline (2026-04-29):

Pro DaF-HTML-Lektion:
1. Quell-PDF zur Lektion finden (basierend auf Lektionscode wie 0102R)
2. Themenspezifische Bilder aus dem PDF extrahieren (Standardbilder rausgefiltert per Hash)
3. Auf 800×300-Banner zuschneiden (JPEG @ 85, gravity=center)
4. Tab-Banner in HTML 1:1 ersetzen (Quell-Bild i → Tab i)
5. Falls Quelle nicht ausreicht → bestehende Pexels-URL als Base64 einbetten (Fallback)

Reihenfolge der Quell-Bilder folgt der PDF-Reihenfolge (Quell-Layout: erstes Bild = Hero).

Aufruf:
    python3 scripts/pdf-images-embed.py --niveau C2 --code 0102R [--dry-run]
"""
import argparse
import base64
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BILDER_CACHE = ROOT / ".bilder-cache"

# Niveau → (HTML-Pfad, PDF-Verzeichnisse[Liste], Datei-Präfix)
NIVEAU_CONFIG = {
    "C2": {
        "html_dir": ROOT / "htmlS" / "C2",
        "pdf_dirs": [ROOT / "C 2"],
        "html_prefix": "DE_C2_",
        "pdf_prefix": "GER_C2.",
        "pool_json": BILDER_CACHE / "c2_pool.json",
    },
    "B1": {
        "html_dir": ROOT / "htmlS" / "B1.1",
        "pdf_dirs": [
            ROOT / "quelltexte" / "B 1.1",
            ROOT / "quelltexte" / "B 1.2",
            ROOT / "quelltexte" / "B 1.3",
        ],
        "html_prefix": "DE_B1_",
        "pdf_prefix": "B1_",
        "pool_json": BILDER_CACHE / "b1_pool.json",
    },
    "B2": {
        "html_dir": ROOT,  # B2-Files liegen am Repo-Root
        "pdf_dirs": [
            ROOT / "quelltexte" / "B 2.1",
            ROOT / "quelltexte" / "B 2.2",
            ROOT / "quelltexte" / "B 2.3",
        ],
        "html_prefix": "DE_B2_",
        "pdf_prefix": "B2_",
        "pool_json": BILDER_CACHE / "b2_pool.json",
    },
    "C1": {
        "html_dir": ROOT / "htmlS" / "C1",
        "pdf_dirs": [
            ROOT / "quelltexte-c1" / "C 1",
            ROOT / "quelltexte-c1" / "C 1.1",
            ROOT / "quelltexte-c1" / "C 1.2",
            ROOT / "quelltexte-c1" / "C 1.3",
            ROOT / "quelltexte-c1" / "C 1.4",
        ],
        "html_prefix": "DE_C1_",
        "pdf_prefix": "C1_",
        "pool_json": BILDER_CACHE / "c1_pool.json",
    },
}


def extract_pdf_images(pdf_path: Path, out_dir: Path) -> None:
    """pdfimages → JPEG-Files in out_dir."""
    out_dir.mkdir(parents=True, exist_ok=True)
    if any(out_dir.glob("*.jpg")):
        return  # schon extrahiert
    subprocess.run(
        ["pdfimages", "-j", str(pdf_path), str(out_dir / "img")],
        check=False,
        capture_output=True,
    )


def build_pool(niveau: str) -> dict:
    """Pool aller PDFs eines Niveaus mit themenspezifischen Bildern (Standardbilder gefiltert)."""
    config = NIVEAU_CONFIG[niveau]
    pool_json = config["pool_json"]
    if pool_json.exists():
        with open(pool_json) as f:
            return json.load(f)

    pdf_dirs = config["pdf_dirs"]
    base_dir = BILDER_CACHE / f"{niveau.lower()}_all"
    base_dir.mkdir(parents=True, exist_ok=True)

    # Alle Bilder pro PDF extrahieren (alle Quellverzeichnisse)
    for pdf_dir in pdf_dirs:
        for pdf in sorted(pdf_dir.glob("*.pdf")):
            out = base_dir / pdf.stem
            extract_pdf_images(pdf, out)

    # Hashes berechnen
    from collections import defaultdict
    hash_to_files = defaultdict(list)
    for jpg in base_dir.rglob("*.jpg"):
        h = hashlib.md5(jpg.read_bytes()).hexdigest()
        hash_to_files[h].append(jpg)
    standard_hashes = {h for h, files in hash_to_files.items() if len(files) > 1}

    # Pro PDF die themenspezifischen Bilder mit Größe sammeln (PIL statt identify-subprocess)
    try:
        from PIL import Image as PILImage  # type: ignore
    except ImportError:
        subprocess.run(["pip", "install", "Pillow", "--break-system-packages", "--quiet"], check=False)
        from PIL import Image as PILImage  # type: ignore

    pool = {}
    for pdf_dir2 in sorted(base_dir.iterdir()):
        if not pdf_dir2.is_dir():
            continue
        images = []
        for jpg in sorted(pdf_dir2.glob("*.jpg")):
            h = hashlib.md5(jpg.read_bytes()).hexdigest()
            if h in standard_hashes:
                continue
            try:
                with PILImage.open(jpg) as im:
                    w, h_dim = im.size
            except Exception:
                continue
            if w >= 300 and h_dim >= 200:
                images.append({"file": str(jpg), "w": w, "h": h_dim})
        pool[pdf_dir2.name] = images

    pool_json.parent.mkdir(parents=True, exist_ok=True)
    with open(pool_json, "w") as f:
        json.dump(pool, f, indent=2)
    return pool


def crop_to_banner(src_path: str, out_path: Path) -> None:
    """800×300 Banner-Crop, JPEG @ 85, EXIF gestrippt."""
    subprocess.run(
        [
            "convert", src_path,
            "-resize", "800x300^",
            "-gravity", "center",
            "-extent", "800x300",
            "-quality", "85",
            "-strip",
            str(out_path),
        ],
        check=True,
        capture_output=True,
    )


def jpeg_to_data_url(jpeg_path: Path) -> str:
    """JPEG-Datei → data:image/jpeg;base64-URL."""
    b64 = base64.b64encode(jpeg_path.read_bytes()).decode("ascii")
    return f"data:image/jpeg;base64,{b64}"


def find_html_file(niveau: str, code: str) -> Path:
    config = NIVEAU_CONFIG[niveau]
    pattern = f"{config['html_prefix']}{code}-*.html"
    matches = list(config["html_dir"].glob(pattern))
    if not matches:
        raise FileNotFoundError(f"Keine HTML-Datei für {niveau}/{code} unter {config['html_dir']}")
    return matches[0]


def find_pdf_dir_for_code(niveau: str, code: str, pool: dict) -> str | None:
    """Mappt Code wie '0102R' auf einen PDF-Stem im Pool.
    Erst exakter Match (0102R → GER_C2.0102R-...). Falls nicht: nur Ziffern matchen,
    weil Frank R/S manchmal anders klassifiziert als das Quellmaterial (z.B. 0503R-jagd ↔ 0503S-Hunting)."""
    config = NIVEAU_CONFIG[niveau]
    prefix_exact = config["pdf_prefix"] + code
    # 1. Versuch: exakter Match
    for stem in pool:
        if stem.startswith(prefix_exact):
            return stem
    # 2. Versuch: nur Ziffern (z.B. 0503 statt 0503R)
    digits = re.match(r"\d+", code)
    if digits:
        prefix_digits = config["pdf_prefix"] + digits.group(0)
        for stem in pool:
            if stem.startswith(prefix_digits):
                return stem
    return None


def patch_html(
    html_path: Path,
    quell_images: list[dict],
    work_dir: Path,
    dry_run: bool,
) -> tuple[int, int]:
    """Tab-Banner in HTML ersetzen. Returns (quell_count, pexels_kept_count)."""
    text = html_path.read_text(encoding="utf-8")
    # Pattern: <img class="tab-banner" src="..." alt="...">
    banner_re = re.compile(
        r'<img class="tab-banner"\s+src="([^"]+)"\s+alt="([^"]+)">',
        re.MULTILINE,
    )
    banners = banner_re.findall(text)
    if not banners:
        return 0, 0

    work_dir.mkdir(parents=True, exist_ok=True)
    new_srcs = []
    quell_used = 0
    pexels_kept = 0

    for i, (src, alt) in enumerate(banners):
        if i < len(quell_images):
            # Quell-Bild verwenden
            src_jpg = quell_images[i]["file"]
            cropped = work_dir / f"banner_{i:02d}.jpg"
            crop_to_banner(src_jpg, cropped)
            data_url = jpeg_to_data_url(cropped)
            new_srcs.append(data_url)
            quell_used += 1
        else:
            # Pexels-URL bleibt (kein Embedding hier — separater Schritt)
            new_srcs.append(src)
            pexels_kept += 1

    # Ersetzen — eindeutig pro Vorkommen
    new_text = text
    matches = list(banner_re.finditer(text))
    # Von hinten nach vorne ersetzen, damit Indizes nicht verschieben
    for i in range(len(matches) - 1, -1, -1):
        m = matches[i]
        old_src = banners[i][0]
        alt = banners[i][1]
        new_src = new_srcs[i]
        # Vorher: Original-URL als Comment direkt davor erhalten (für Quellenarchiv)
        comment = f"<!-- orig-src: {old_src} -->\n  "
        replacement = f'{comment}<img class="tab-banner" src="{new_src}" alt="{alt}">'
        new_text = new_text[: m.start()] + replacement + new_text[m.end():]

    if not dry_run:
        html_path.write_text(new_text, encoding="utf-8")

    return quell_used, pexels_kept


def process_lesson(niveau: str, code: str, dry_run: bool = False) -> None:
    pool = build_pool(niveau)
    pdf_stem = find_pdf_dir_for_code(niveau, code, pool)
    if not pdf_stem:
        print(f"  ✗ {code}: kein Quell-PDF gefunden — übersprungen")
        return
    quell_images = pool[pdf_stem]
    html_path = find_html_file(niveau, code)
    work_dir = BILDER_CACHE / f"work_{niveau.lower()}_{code}"
    used, kept = patch_html(html_path, quell_images, work_dir, dry_run)
    suffix = " (dry-run)" if dry_run else ""
    print(f"  ✓ {code:6s}  {html_path.name}  →  Quelle={used}  Pexels-bleibt={kept}{suffix}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--niveau", required=True, choices=list(NIVEAU_CONFIG.keys()))
    parser.add_argument("--code", help="Spezifischer Code (z.B. 0102R) — sonst alle des Niveaus")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    config = NIVEAU_CONFIG[args.niveau]
    if args.code:
        process_lesson(args.niveau, args.code, args.dry_run)
    else:
        # Alle Codes aus dem PDF-Pool extrahieren
        pool = build_pool(args.niveau)
        codes = []
        prefix = config["pdf_prefix"]
        for stem in sorted(pool):
            if stem.startswith(prefix):
                # GER_C2.0102R-Musical-instruments → 0102R
                # B1_1011X_DE → 1011X
                # C1_1011G_DE → 1011G
                rest = stem[len(prefix):]
                m = re.match(r"\d+[A-Z]+", rest)
                code = m.group(0) if m else rest.split("-")[0].split("_")[0]
                codes.append(code)
        print(f"=== {args.niveau}: {len(codes)} Lektionen ===")
        for code in codes:
            try:
                process_lesson(args.niveau, code, args.dry_run)
            except Exception as e:
                print(f"  ✗ {code}: FEHLER {e}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
