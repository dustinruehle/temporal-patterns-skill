#!/usr/bin/env python3
"""Validate a SKILL.md file's YAML frontmatter and its references.

Checks that the frontmatter parses and carries the fields Claude relies on to load
and route the skill, that the description fits the Agent Skills limit (1,024
characters, no angle brackets), and that every references/ file SKILL.md names
exists. Exits non-zero (with a readable message) on any problem.

Usage: python3 scripts/validate_skill.py SKILL.md
"""
import pathlib
import re
import sys

try:
    import yaml
except ImportError:
    sys.exit("PyYAML is required: pip install pyyaml (or: make setup)")

EXPECTED_NAME = "temporal-patterns"
MAX_DESCRIPTION = 1024


def fail(msg):
    sys.exit(f"validate_skill: {msg}")


def main(path):
    try:
        text = open(path, encoding="utf-8").read()
    except OSError as e:
        fail(f"cannot read {path}: {e}")

    if not text.startswith("---"):
        fail("file does not start with a '---' frontmatter block")

    parts = text.split("---", 2)
    if len(parts) < 3:
        fail("frontmatter block is not closed with a second '---'")

    try:
        fm = yaml.safe_load(parts[1])
    except yaml.YAMLError as e:
        fail(f"frontmatter is not valid YAML: {e}")

    if not isinstance(fm, dict):
        fail("frontmatter did not parse to a mapping")

    for key in ("name", "description", "metadata"):
        if not fm.get(key):
            fail(f"missing required frontmatter key: {key}")

    if fm["name"] != EXPECTED_NAME:
        fail(f"name is {fm['name']!r}, expected {EXPECTED_NAME!r}")

    desc = str(fm["description"]).strip()
    if len(desc) < 40:
        fail("description is suspiciously short; it drives skill triggering")
    if len(desc) > MAX_DESCRIPTION:
        fail(f"description is {len(desc)} characters; the limit is {MAX_DESCRIPTION}. "
             "Clients truncate or reject longer descriptions.")
    if "<" in desc or ">" in desc:
        fail("description cannot contain angle brackets")

    root = pathlib.Path(path).resolve().parent
    for ref in sorted(set(re.findall(r"`(references/[A-Za-z0-9_.-]+\.md)`", text))):
        if not (root / ref).is_file():
            fail(f"SKILL.md names {ref}, which does not exist")

    meta = fm["metadata"]
    if not isinstance(meta, dict):
        fail("metadata must be a mapping")
    for key in ("version", "source"):
        if not meta.get(key):
            fail(f"missing required metadata key: {key}")

    print(f"OK: {path}: {fm['name']} v{meta['version']}, description {len(desc)} chars")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("usage: validate_skill.py SKILL.md")
    main(sys.argv[1])
