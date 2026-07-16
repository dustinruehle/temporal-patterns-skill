# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repository is

This is **not application code** — it is the source and distribution setup for a
single Claude skill named `temporal-patterns`. The skill teaches Claude to map a
described problem to one of Temporal's 35 official Workflow design patterns and to
fetch the pattern's canonical doc page before writing code or asserting specifics.

## Files and their roles

- `SKILL.md` — the skill itself, and the **single source of truth**. YAML
  frontmatter (`name`, `description`, `metadata`) followed by the skill body: the
  operating rules, the problem→pattern routing map, the use-case→pattern-stack map,
  the full catalog (35 patterns across 10 domains), composition notes, cross-cutting
  techniques, and guardrails. **All content edits happen here.**
- `README.md` — human-facing docs: what the skill does, why, and how to install it
  from GitHub Releases.
- `CONTRIBUTING.md` — how humans propose fixes/additions and how maintainers release.
- `CHANGELOG.md` — Keep a Changelog format; version tracks `metadata.version` in
  `SKILL.md`.
- `Makefile` — `make build` packages the skill; `make lint` / `make check-links`
  validate it.
- `scripts/validate_skill.py` — frontmatter validation (used by `make lint` and CI).
- `scripts/check_links.py` — checks every catalog slug resolves at docs.temporal.io.
- `.github/workflows/ci.yml` — PR/push checks: lint, build, packaged-content diff,
  and a non-blocking link-check job.
- `.github/workflows/release.yml` — on a `v*` tag: build and attach the `.skill` to
  the GitHub Release.

## The `.skill` package is a build artifact — do not commit it

`temporal-patterns.skill` is a ZIP whose single entry is `temporal-patterns/SKILL.md`
(a copy of the root `SKILL.md`). It is **generated, not committed** — `dist/` and
`*.skill` are gitignored. It is published two ways:

- CI uploads it as a workflow artifact on every PR.
- Tagged releases attach it to the GitHub Releases page (how end users download it).

This keeps `SKILL.md` the only source of truth and avoids committing a binary that
churns on every edit (ZIP embeds timestamps, so byte-diffs are meaningless).

## Editing workflow

1. Edit `SKILL.md`.
2. Validate and build locally:
   ```sh
   make lint          # frontmatter is well-formed
   make build         # produces dist/temporal-patterns.skill
   make verify        # build + confirm packaged SKILL.md matches the source
   make check-links   # every catalog slug resolves at docs.temporal.io
   ```
3. Add a `## [Unreleased]` entry in `CHANGELOG.md`.
4. Open a PR. CI re-runs lint + build and diffs the packaged `SKILL.md` against the
   source, so packaging can never drift silently.

## Releasing

Releases are cut by tag; the workflow builds and attaches the `.skill`.

1. Bump `metadata.version` in `SKILL.md`.
2. Promote `## [Unreleased]` items under a new version heading in `CHANGELOG.md`.
3. `git tag vX.Y.Z && git push origin vX.Y.Z`.

Keep the tag, `metadata.version`, and the CHANGELOG heading in agreement.

## Conventions that keep the skill correct

These come from the skill's own design and must be preserved when editing:

- **The catalog is an index, not the implementation.** The skill deliberately does
  NOT embed pattern implementation code. Each pattern is referenced by `slug`, and
  the canonical page is fetched on demand at
  `https://docs.temporal.io/design-patterns/{slug}.md` (drop `.md` for the shareable
  web page). The full index is `https://docs.temporal.io/design-patterns.md`.
- **A pattern's `slug` appears in up to three places** — the routing-map table, the
  catalog-by-domain section, and any composition / choosing-between notes. Keep them
  consistent when adding, renaming, or removing a pattern. `make check-links`
  verifies the slugs against the live docs.
- **Pattern names are product terminology** — use them exactly; don't rename or
  pluralize.
- Two boundary tools are referenced intentionally and should stay distinct: the
  `temporal-developer` skill (SDK setup, determinism, testing) and the Temporal Docs
  (Kapa) MCP (free-text doc search). This skill only picks the *pattern shape*.

## Keeping the catalog current

The embedded catalog is a snapshot (35 patterns, 10 domains). The live index at
`https://docs.temporal.io/design-patterns.md` is the real source of truth. Before
concluding a pattern is missing, or when updating the catalog, re-fetch that index
and reconcile against `SKILL.md`. Note: **Event Accumulator** (`event-accumulator`)
has a live pattern page but is not currently listed in that index — the page itself
is authoritative for it.
