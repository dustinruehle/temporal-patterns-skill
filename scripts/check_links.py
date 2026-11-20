#!/usr/bin/env python3
"""Check that the skill's catalog agrees with the live Temporal docs.

Offline checks:
  1. Every slug referenced in references/ (use-case stacks, anti-patterns,
     guides) is a catalog slug.
  2. The snapshot line in SKILL.md ("N patterns in M domains") matches the
     catalog, and README.md states the same pattern count.

Online checks (need the live docs site):
  3. Every catalog slug resolves at https://docs.temporal.io/design-patterns/{slug}.md.
  4. The live index lists no pattern the catalog lacks, and the catalog has no
     slug the index lacks.
  5. Every catalog pattern name matches the name in the live index.
  6. Every other docs.temporal.io URL in SKILL.md and references/ resolves.

The catalog is the "## Pattern catalog" section of SKILL.md: one Markdown table
per domain (### heading), rows "| Name | `slug` | Use it when |".

Depends on the live docs site, so CI runs it as a non-blocking job.

Usage: python3 scripts/check_links.py [SKILL.md]
"""
import pathlib
import re
import sys
import urllib.error
import urllib.request

DOCS = "https://docs.temporal.io"
INDEX_URL = DOCS + "/design-patterns.md"
PATTERN_URL = DOCS + "/design-patterns/{}.md"
SLUG = r"[a-z0-9][a-z0-9-]*"
ROW_RE = re.compile(r"^\|\s*([^|`]+?)\s*\|\s*`(" + SLUG + r")`\s*\|", re.MULTILINE)
INLINE_RE = re.compile(r"`(" + SLUG + r")`")
INDEX_RE = re.compile(r"^- \[([^\]]+)\]\(/design-patterns/(" + SLUG + r")\)", re.MULTILINE)
URL_RE = re.compile(r"https://docs\.temporal\.io/[A-Za-z0-9_\-./#]*")
SNAPSHOT_RE = re.compile(r"(\d+) patterns in (\d+) domains")
README_COUNT_RE = re.compile(r"catalog of (\d+)")
# Lines in references/ that hold pattern slugs.
REF_LINE_RE = re.compile(r"^- \*\*(Patterns|Also consider|Related):\*\*(.*)$", re.MULTILINE)
UA = {"User-Agent": "temporal-patterns-skill-linkcheck"}


def section(text, heading):
    """Body of a '## heading' section, up to the next '## ' heading."""
    m = re.search(r"^##\s+" + re.escape(heading) + r"\s*$(.*?)(?=^##\s|\Z)",
                  text, re.MULTILINE | re.DOTALL)
    return m.group(1) if m else ""


def fetch(url):
    req = urllib.request.Request(url, headers=UA)
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            return resp.status, resp.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as e:
        return e.code, ""
    except Exception as e:  # noqa: BLE001: report any network failure
        return str(e), ""


def main(path):
    root = pathlib.Path(path).resolve().parent
    text = pathlib.Path(path).read_text(encoding="utf-8")
    problems = []

    cat_text = section(text, "Pattern catalog")
    catalog = {slug: name.strip() for name, slug in ROW_RE.findall(cat_text)}
    domains = len(re.findall(r"^### ", cat_text, re.MULTILINE))
    if not catalog:
        sys.exit("check_links: found no catalog rows. Did the table format change?")
    print(f"Catalog: {len(catalog)} patterns in {domains} domains.")

    # 1. Offline: references/ slugs must be catalog slugs.
    refs = sorted((root / "references").glob("*.md"))
    for ref in refs:
        rt = ref.read_text(encoding="utf-8")
        used = set()
        for _, rest in REF_LINE_RE.findall(rt):
            used |= set(INLINE_RE.findall(rest))
        for line in rt.splitlines():  # guides table: last column
            if line.startswith("| `"):
                used |= set(INLINE_RE.findall(line.split("|")[-2]))
        orphans = sorted(used - set(catalog))
        if orphans:
            problems.append(f"{ref.name}: slugs not in the catalog: {', '.join(orphans)}")
        else:
            print(f"OK: {ref.name}: {len(used)} referenced slugs exist in the catalog.")

    # 2. Offline: stated counts match the catalog.
    m = SNAPSHOT_RE.search(text)
    if not m:
        problems.append("SKILL.md: no 'N patterns in M domains' snapshot line found")
    elif (int(m.group(1)), int(m.group(2))) != (len(catalog), domains):
        problems.append(f"SKILL.md snapshot says {m.group(0)}; catalog has "
                        f"{len(catalog)} patterns in {domains} domains")
    readme = root / "README.md"
    if readme.exists():
        rm = README_COUNT_RE.search(readme.read_text(encoding="utf-8"))
        if rm and int(rm.group(1)) != len(catalog):
            problems.append(f"README.md says a catalog of {rm.group(1)}; catalog has {len(catalog)}")

    # 3. Online: every catalog slug resolves.
    print(f"\nChecking {len(catalog)} catalog slugs against {PATTERN_URL.format('<slug>')}")
    for slug in sorted(catalog):
        status, _ = fetch(PATTERN_URL.format(slug))
        ok = status == 200
        print(f"  {'OK ' if ok else 'BAD'}  {slug}  ({status})")
        if not ok:
            problems.append(f"catalog slug does not resolve: {slug} ({status})")

    # 4 and 5. Online: the catalog matches the live index, both ways, by name.
    status, index = fetch(INDEX_URL)
    if status != 200:
        problems.append(f"could not fetch the live index ({status})")
    else:
        live = {slug: name.strip() for name, slug in INDEX_RE.findall(index)}
        print(f"\nLive index: {len(live)} patterns.")
        for slug in sorted(set(live) - set(catalog)):
            problems.append(f"live index has a pattern the catalog lacks: {live[slug]} ({slug})")
        for slug in sorted(set(catalog) - set(live)):
            problems.append(f"catalog has a slug the live index lacks: {slug}")
        for slug in sorted(set(catalog) & set(live)):
            if catalog[slug] != live[slug]:
                problems.append(f"name differs for {slug}: catalog '{catalog[slug]}', "
                                f"live index '{live[slug]}'")

    # 6. Online: other docs URLs resolve (templates and queries skipped).
    urls = set()
    for t in [text] + [r.read_text(encoding="utf-8") for r in refs]:
        urls |= {u.rstrip(".") for u in URL_RE.findall(t)}
    urls = {u for u in urls if "/design-patterns/" not in u and not u.endswith("/")
            and "{" not in u and "/api/" not in u}
    print(f"\nChecking {len(urls)} other docs URLs")
    for url in sorted(urls):
        status, _ = fetch(url.split("#")[0])
        ok = status == 200
        print(f"  {'OK ' if ok else 'BAD'}  {url}  ({status})")
        if not ok:
            problems.append(f"docs URL does not resolve: {url} ({status})")

    print()
    if problems:
        print("Problems:")
        for p in problems:
            print(f"  - {p}")
        sys.exit(f"check_links: {len(problems)} problem(s)")
    print("All checks passed.")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "SKILL.md")
