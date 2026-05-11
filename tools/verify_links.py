#!/usr/bin/env python3
"""
verify_links.py — B.L.A.S.T. Link Verifier (Layer 3 · Tools)

Crawls public/*.html for every external <a href> and HEAD-requests it.
Catches link rot before it reaches production.

Usage:
    python3 tools/verify_links.py
    python3 tools/verify_links.py --verbose
    python3 tools/verify_links.py --root /path/to/public

Exit codes:
    0  All links healthy
    1  At least one link failed
    2  Crawl error (HTML missing, etc.)
"""

from __future__ import annotations

import argparse
import os
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

# Hosts we never network-check (mailto, tel, fragment-only, etc.)
SKIP_PROTOCOLS = ("mailto:", "tel:", "javascript:", "#")

# Extracts every href value from anchor tags. Tolerant of single/double quotes.
HREF_RE = re.compile(r"""<a\s+[^>]*href\s*=\s*["']([^"']+)["']""", re.IGNORECASE)


def find_html_files(root: Path) -> list[Path]:
    return sorted(root.rglob("*.html"))


def extract_hrefs(html: str) -> set[str]:
    return set(HREF_RE.findall(html))


def is_external(href: str) -> bool:
    return href.startswith(("http://", "https://"))


def is_skipworthy(href: str) -> bool:
    return href.startswith(SKIP_PROTOCOLS)


def head_check(url: str, timeout: float = 10.0) -> tuple[bool, int | str]:
    """HEAD-request a URL. Falls back to GET if server rejects HEAD.
    Returns (ok, status_or_error)."""
    headers = {
        "User-Agent": "Mozilla/5.0 (BLASTLinkVerifier/1.0; +https://tavci-kuhna.si)",
        "Accept": "*/*",
    }
    for method in ("HEAD", "GET"):
        try:
            req = urllib.request.Request(url, method=method, headers=headers)
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                status = resp.status
                if 200 <= status < 400:
                    return True, status
                # 4xx/5xx — fall through to retry with GET if we tried HEAD
                if method == "GET":
                    return False, status
        except urllib.error.HTTPError as e:
            if e.code in (405, 501) and method == "HEAD":
                continue  # try GET
            return False, e.code
        except (urllib.error.URLError, TimeoutError, ConnectionError) as e:
            return False, str(e)
    return False, "unreachable"


def main() -> int:
    parser = argparse.ArgumentParser(description="B.L.A.S.T. link verifier.")
    parser.add_argument(
        "--root",
        default=str(Path(__file__).resolve().parent.parent / "public"),
        help="Directory containing HTML files (default: ../public)",
    )
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args()

    root = Path(args.root)
    if not root.is_dir():
        print(f"✗ Root directory not found: {root}", file=sys.stderr)
        return 2

    html_files = find_html_files(root)
    if not html_files:
        print(f"✗ No HTML files found under {root}", file=sys.stderr)
        return 2

    print(f"🔗  B.L.A.S.T. link verifier · scanning {len(html_files)} HTML file(s) under {root}\n")

    all_external_links: dict[str, list[str]] = {}  # href -> [files]
    for html_file in html_files:
        hrefs = extract_hrefs(html_file.read_text(encoding="utf-8"))
        for href in hrefs:
            if is_skipworthy(href):
                continue
            if not is_external(href):
                # relative path — verify the file exists locally
                target = (html_file.parent / href.split("#", 1)[0]).resolve() if href.split("#", 1)[0] else html_file
                if not target.exists():
                    print(f"  ✗ {html_file.name}: relative link to missing file → {href}")
                    all_external_links.setdefault(f"local:{href}", []).append(html_file.name)
                continue
            all_external_links.setdefault(href, []).append(html_file.name)

    if not all_external_links:
        print("✓ No external links to verify (only internal navigation).")
        return 0

    # Filter out the local: failures we already reported
    network_links = {k: v for k, v in all_external_links.items() if not k.startswith("local:")}

    failures: list[tuple[str, int | str, list[str]]] = []
    for i, (href, sources) in enumerate(sorted(network_links.items()), start=1):
        ok, info = head_check(href)
        symbol = "✓" if ok else "✗"
        suffix = f"  ← {', '.join(sources)}" if args.verbose else ""
        print(f"  [{i:2}/{len(network_links)}] {symbol} {info:>4}  {href[:80]}{'…' if len(href) > 80 else ''}{suffix}")
        if not ok:
            failures.append((href, info, sources))

    print()
    if failures:
        print(f"✗ {len(failures)} link(s) failed:")
        for href, info, sources in failures:
            print(f"   • {info}  ·  {href}")
            print(f"     used in: {', '.join(sources)}")
        return 1

    print(f"✓ All {len(network_links)} external link(s) healthy.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
