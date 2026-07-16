#!/usr/bin/env python3
"""Verify pattern slugs in SKILL.md are valid and canonical.

Two checks:

1. Online: every slug in the *catalog by domain* section resolves at
   https://docs.temporal.io/design-patterns/{slug}.md (200).
2. Offline: every slug *referenced* elsewhere (the routing-map table and the
   use-case -> pattern-stack section) is a member of the catalog slug-set. This
   catches typos / renames in those surfaces without extra HTTP, and without the
   false positives a whole-file scan would hit (e.g. `idempotency`, which is a
   technique not a pattern, or `temporal-developer`, a sibling skill).

The catalog is the source of truth for what a valid slug is; the online check
confirms the catalog itself is real; the offline check confirms references agree.

Depends on the live docs site, so CI runs it as a non-blocking job.

Usage: python3 scripts/check_links.py [SKILL.md]
"""
import re
import sys
import urllib.error
import urllib.request

URL = "https://docs.temporal.io/design-patterns/{}.md"
SLUG = r"[a-z0-9][a-z0-9-]*"
# Catalog bullet: "... — `slug` — ..." (em-dash on both sides). Source of truth.
CATALOG_RE = re.compile(r"—\s*`(" + SLUG + r")`\s*—")
# Routing table: a cell that is just a backticked slug, at end of a row.
ROUTING_RE = re.compile(r"\|\s*`(" + SLUG + r")`\s*\|")
# Any backticked slug (used to scan the use-case section).
INLINE_RE = re.compile(r"`(" + SLUG + r")`")


def section(text, heading):
    """Return the body of a '## heading' section, up to the next '## '."""
    m = re.search(r"^##\s+" + re.escape(heading) + r"\s*$(.*?)(?=^##\s)",
                  text, re.MULTILINE | re.DOTALL)
    return m.group(1) if m else ""


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

    catalog = set(CATALOG_RE.findall(section(text, "Full catalog by domain")))
    if not catalog:
        sys.exit("check_links: found no catalog slugs — did the SKILL.md format change?")

    # 1. Offline: referenced slugs must exist in the catalog.
    referenced = set(ROUTING_RE.findall(section(text, "Problem → pattern routing map")))
    referenced |= set(INLINE_RE.findall(section(text, "Use-case → pattern stack")))
    orphans = sorted(referenced - catalog)
    if orphans:
        sys.exit(
            "check_links: slug(s) referenced in routing/use-case but not in the "
            f"catalog (typo or missing catalog entry?): {', '.join(orphans)}"
        )
    print(f"OK: all {len(referenced)} referenced slugs exist in the catalog.\n")

    # 2. Online: every catalog slug resolves.
    print(f"Checking {len(catalog)} catalog slugs against {URL.format('<slug>')}\n")
    failures = []
    for slug in sorted(catalog):
        ok, info = resolves(slug)
        print(f"  {'OK ' if ok else 'BAD'}  {slug}  ({info})")
        if not ok:
            failures.append(slug)

    print()
    if failures:
        sys.exit(f"{len(failures)} slug(s) did not resolve: {', '.join(failures)}")
    print(f"All {len(catalog)} catalog slugs resolve.")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "SKILL.md")
