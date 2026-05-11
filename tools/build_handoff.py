#!/usr/bin/env python3
"""
build_handoff.py — B.L.A.S.T. Handoff Bundler (Layer 3 · Tools)

Bundles the deployable site + supporting docs into a single ZIP for the
receiving developer. Also produces image_inventory.json — a list of every
external image URL the site loads, so the developer can self-host them.

Usage:
    python3 tools/build_handoff.py
    python3 tools/build_handoff.py --output mybundle.zip

Output:
    .tmp/tavci-kuhna-handoff.zip   (default)
    .tmp/image_inventory.json
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import zipfile
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
EXTERNAL_IMG_RE = re.compile(
    r"""(?:src|background-image|content)\s*[=:]\s*["']?(?:url\()?["']?(https?://[^\s"'\)]+\.(?:jpe?g|png|webp|gif|svg))""",
    re.IGNORECASE,
)


def collect_external_images() -> list[dict]:
    inventory: list[dict] = []
    seen: set[str] = set()
    for html in (PROJECT_ROOT / "public").rglob("*.html"):
        text = html.read_text(encoding="utf-8")
        for m in EXTERNAL_IMG_RE.finditer(text):
            url = m.group(1)
            if url in seen:
                continue
            seen.add(url)
            inventory.append({
                "source_url": url,
                "host": url.split("/")[2],
                "found_in": html.name,
                "suggested_local_path": f"/wp-content/uploads/website/{Path(url).name.split('?')[0]}",
            })
    return sorted(inventory, key=lambda x: (x["host"], x["found_in"]))


def write_inventory(inventory: list[dict], out: Path) -> None:
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(inventory, indent=2, ensure_ascii=False), encoding="utf-8")


def build_zip(zip_path: Path) -> None:
    zip_path.parent.mkdir(parents=True, exist_ok=True)

    # Bundle these top-level entries
    include_dirs = ["public", "architecture", "tools"]
    include_files = ["gemini.md", "README.md", ".env.example", ".gitignore"]

    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for d in include_dirs:
            src_dir = PROJECT_ROOT / d
            if not src_dir.is_dir():
                continue
            for path in src_dir.rglob("*"):
                if path.is_file():
                    arcname = path.relative_to(PROJECT_ROOT)
                    zf.write(path, arcname)
        for f in include_files:
            src = PROJECT_ROOT / f
            if src.is_file():
                zf.write(src, src.relative_to(PROJECT_ROOT))


def main() -> int:
    parser = argparse.ArgumentParser(description="B.L.A.S.T. handoff bundler.")
    parser.add_argument(
        "--output",
        default=str(PROJECT_ROOT / ".tmp" / "tavci-kuhna-handoff.zip"),
        help="Output ZIP path (default: .tmp/tavci-kuhna-handoff.zip)",
    )
    args = parser.parse_args()

    inventory_path = PROJECT_ROOT / ".tmp" / "image_inventory.json"
    inventory = collect_external_images()
    write_inventory(inventory, inventory_path)
    print(f"✓ Wrote image inventory ({len(inventory)} unique URLs) → {inventory_path.relative_to(PROJECT_ROOT)}")

    zip_path = Path(args.output)
    build_zip(zip_path)
    size_kb = zip_path.stat().st_size / 1024
    print(f"✓ Built handoff bundle → {zip_path.relative_to(PROJECT_ROOT)} ({size_kb:.1f} KB)")
    print()
    print("Contents (top level): public/  architecture/  tools/  gemini.md  README.md  .env.example  .gitignore")
    return 0


if __name__ == "__main__":
    sys.exit(main())
