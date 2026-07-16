#!/usr/bin/env python3
"""Verify every pattern slug in SKILL.md resolves at docs.temporal.io.

Slugs are extracted from two structured places in SKILL.md:
  - the routing-map table rows, which end in `| `slug` |`
  - the catalog-by-domain bullets, of the form `... — `slug` — ...`

Each slug is checked against https://docs.temporal.io/design-patterns/{slug}.md.
Prints a per-slug report and exits non-zero if any fail to resolve.

This depends on the live docs site, so CI runs it as a non-blocking job.

Usage: python3 scripts/check_links.py [SKILL.md]
"""
import re
import sys
import urllib.error
import urllib.request

URL = "https://docs.temporal.io/design-patterns/{}.md"
# Routing table: a cell that is just a backticked slug, at end of a table row.
ROUTING_RE = re.compile(r"\|\s*`([a-z0-9][a-z0-9-]*)`\s*\|")
# Catalog bullet: em-dash, backticked slug, em-dash.
CATALOG_RE = re.compile(r"—\s*`([a-z0-9][a-z0-9-]*)`\s*—")


def extract_slugs(text):
    slugs = set(ROUTING_RE.findall(text))
    slugs.update(CATALOG_RE.findall(text))
    return sorted(slugs)


def resolves(slug):
    url = URL.format(slug)
    req = urllib.request.Request(
        url, method="GET", headers={"User-Agent": "temporal-patterns-skill-linkcheck"}
    )
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            return resp.status == 200, resp.status
    except urllib.error.HTTPError as e:
        return False, e.code
    except Exception as e:  # noqa: BLE001 — report any network failure
        return False, str(e)


def main(path):
    text = open(path, encoding="utf-8").read()
    slugs = extract_slugs(text)
    if not slugs:
        sys.exit("check_links: found no slugs — did the SKILL.md format change?")

    print(f"Checking {len(slugs)} pattern slugs against {URL.format('<slug>')}\n")
    failures = []
    for slug in slugs:
        ok, info = resolves(slug)
        print(f"  {'OK ' if ok else 'BAD'}  {slug}  ({info})")
        if not ok:
            failures.append(slug)

    print()
    if failures:
        sys.exit(f"{len(failures)} slug(s) did not resolve: {', '.join(failures)}")
    print(f"All {len(slugs)} slugs resolve.")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "SKILL.md")
