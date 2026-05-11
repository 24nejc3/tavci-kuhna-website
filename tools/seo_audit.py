#!/usr/bin/env python3
"""
seo_audit.py — B.L.A.S.T. SEO + Schema.org Auditor (Layer 3 · Tools)

For every HTML file in public/, verifies:
  • <title> exists and is < 70 chars
  • <meta name="description"> exists and is 70–170 chars
  • Open Graph tags: og:title, og:description, og:image, og:url, og:type
  • Twitter card tags: twitter:card, twitter:title, twitter:description
  • <script type="application/ld+json"> blocks parse as valid JSON
  • Schema.org Restaurant payload contains: name, address, geo, openingHoursSpecification
  • Schema.org Menu payload contains: hasMenuSection with hasMenuItem entries

Usage:
    python3 tools/seo_audit.py
    python3 tools/seo_audit.py --root /path/to/public

Exit codes:
    0  All audits pass
    1  At least one audit failed
    2  Audit infrastructure error (missing dir, etc.)
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

TITLE_RE = re.compile(r"<title>(.*?)</title>", re.IGNORECASE | re.DOTALL)
META_NAME_RE = re.compile(
    r"""<meta\s+[^>]*name\s*=\s*["']([^"']+)["'][^>]*content\s*=\s*["']([^"']*)["']""",
    re.IGNORECASE,
)
META_PROPERTY_RE = re.compile(
    r"""<meta\s+[^>]*property\s*=\s*["']([^"']+)["'][^>]*content\s*=\s*["']([^"']*)["']""",
    re.IGNORECASE,
)
JSONLD_RE = re.compile(
    r"""<script\s+[^>]*type\s*=\s*["']application/ld\+json["'][^>]*>(.*?)</script>""",
    re.IGNORECASE | re.DOTALL,
)

REQUIRED_OG = {"og:title", "og:description", "og:image", "og:url", "og:type"}
REQUIRED_TWITTER = {"twitter:card", "twitter:title", "twitter:description"}


class AuditResult:
    def __init__(self, file_name: str):
        self.file_name = file_name
        self.passes: list[str] = []
        self.failures: list[str] = []

    def ok(self, msg: str) -> None:
        self.passes.append(msg)

    def fail(self, msg: str) -> None:
        self.failures.append(msg)

    def print(self) -> None:
        print(f"\n📄  {self.file_name}")
        for p in self.passes:
            print(f"   ✓ {p}")
        for f in self.failures:
            print(f"   ✗ {f}")


def audit_title(html: str, r: AuditResult) -> None:
    m = TITLE_RE.search(html)
    if not m:
        r.fail("missing <title>")
        return
    title = m.group(1).strip()
    if not title:
        r.fail("empty <title>")
    elif len(title) > 70:
        r.fail(f"<title> is {len(title)} chars (recommended <70): {title[:60]}…")
    else:
        r.ok(f"<title> ({len(title)} chars)")


def audit_meta(html: str, r: AuditResult) -> dict[str, str]:
    names = dict(META_NAME_RE.findall(html))
    props = dict(META_PROPERTY_RE.findall(html))

    desc = names.get("description", "")
    if not desc:
        r.fail("missing meta description")
    elif not (70 <= len(desc) <= 170):
        r.fail(f"meta description is {len(desc)} chars (recommended 70–170)")
    else:
        r.ok(f"meta description ({len(desc)} chars)")

    missing_og = REQUIRED_OG - props.keys()
    if missing_og:
        r.fail(f"missing Open Graph tags: {', '.join(sorted(missing_og))}")
    else:
        r.ok("Open Graph tags complete")

    missing_tw = REQUIRED_TWITTER - names.keys()
    if missing_tw:
        r.fail(f"missing Twitter card tags: {', '.join(sorted(missing_tw))}")
    else:
        r.ok("Twitter card tags complete")

    if "viewport" not in names:
        r.fail("missing <meta name='viewport'>")
    else:
        r.ok("viewport set")

    return {**names, **props}


def audit_jsonld(html: str, r: AuditResult) -> list[dict]:
    blocks = JSONLD_RE.findall(html)
    if not blocks:
        r.fail("no <script type='application/ld+json'> found")
        return []

    parsed: list[dict] = []
    for i, raw in enumerate(blocks, start=1):
        try:
            data = json.loads(raw.strip())
            r.ok(f"JSON-LD block {i} parses ({data.get('@type', 'unknown @type')})")
            parsed.append(data)
        except json.JSONDecodeError as e:
            r.fail(f"JSON-LD block {i} invalid: {e}")
    return parsed


def audit_restaurant(data: dict, r: AuditResult) -> None:
    required = ["name", "address", "geo", "openingHoursSpecification", "telephone", "url"]
    missing = [k for k in required if k not in data]
    if missing:
        r.fail(f"Restaurant schema missing: {', '.join(missing)}")
    else:
        r.ok("Restaurant schema has all required fields")

    if "aggregateRating" in data:
        ar = data["aggregateRating"]
        if all(k in ar for k in ("ratingValue", "ratingCount")):
            r.ok(f"aggregateRating present ({ar['ratingValue']} / {ar['ratingCount']})")
        else:
            r.fail("aggregateRating present but incomplete")


def audit_menu(data: dict, r: AuditResult) -> None:
    sections = data.get("hasMenuSection", [])
    if not sections:
        r.fail("Menu schema has no hasMenuSection")
        return
    r.ok(f"Menu has {len(sections)} section(s)")
    items_with_price = 0
    for sec in sections:
        for item in sec.get("hasMenuItem", []):
            offer = item.get("offers", {})
            if offer.get("price") and offer.get("priceCurrency"):
                items_with_price += 1
    if items_with_price:
        r.ok(f"{items_with_price} menu item(s) have structured Offer (price + currency)")


def audit_html(path: Path) -> AuditResult:
    r = AuditResult(path.name)
    html = path.read_text(encoding="utf-8")
    audit_title(html, r)
    audit_meta(html, r)
    parsed = audit_jsonld(html, r)
    for data in parsed:
        t = data.get("@type")
        if t == "Restaurant":
            audit_restaurant(data, r)
        elif t == "Menu":
            audit_menu(data, r)
    return r


def main() -> int:
    parser = argparse.ArgumentParser(description="B.L.A.S.T. SEO & schema.org auditor.")
    parser.add_argument(
        "--root",
        default=str(Path(__file__).resolve().parent.parent / "public"),
        help="Directory containing HTML files (default: ../public)",
    )
    args = parser.parse_args()

    root = Path(args.root)
    if not root.is_dir():
        print(f"✗ Root directory not found: {root}", file=sys.stderr)
        return 2

    html_files = sorted(root.rglob("*.html"))
    if not html_files:
        print(f"✗ No HTML files found under {root}", file=sys.stderr)
        return 2

    print(f"🔍  B.L.A.S.T. SEO + schema auditor · {len(html_files)} HTML file(s) under {root}")

    results = [audit_html(p) for p in html_files]
    for r in results:
        r.print()

    total_failures = sum(len(r.failures) for r in results)
    print()
    if total_failures:
        print(f"✗ {total_failures} audit issue(s) found across {len(results)} file(s).")
        return 1

    print(f"✓ All audits passed across {len(results)} file(s).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
