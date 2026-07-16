#!/usr/bin/env python3
"""Validate a SKILL.md file's YAML frontmatter.

Checks that the frontmatter parses and carries the fields Claude relies on to load
and route the skill. Exits non-zero (with a readable message) on any problem.

Usage: python3 scripts/validate_skill.py SKILL.md
"""
import sys

try:
    import yaml
except ImportError:
    sys.exit("PyYAML is required: pip install pyyaml")

EXPECTED_NAME = "temporal-patterns"


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

    if len(str(fm["description"]).strip()) < 40:
        fail("description is suspiciously short — it drives skill triggering")

    meta = fm["metadata"]
    if not isinstance(meta, dict):
        fail("metadata must be a mapping")
    for key in ("version", "source"):
        if not meta.get(key):
            fail(f"missing required metadata key: {key}")

    print(f"OK: {path} — {fm['name']} v{meta['version']}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("usage: validate_skill.py SKILL.md")
    main(sys.argv[1])
