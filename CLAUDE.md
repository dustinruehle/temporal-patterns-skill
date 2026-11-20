# CLAUDE.md

Guidance for Claude Code when working in this repository.

## What this repository is

This isn't application code. It's the source and packaging for one Claude skill,
`temporal-patterns`. The skill maps a described problem to one of Temporal's
official Workflow design patterns, a platform feature or an anti-pattern, and
fetches the pattern's canonical docs page before it writes code or states
specifics.

## Files and their roles

- `SKILL.md`: the skill. Frontmatter (`name`, `description`, `metadata`), then
  the rules, the three modes, the pattern catalog (one table per domain), the
  features table, choosing and composition notes, limits, anti-patterns,
  cross-cutting techniques, boundaries and guardrails.
- `references/use-cases.md`, `references/anti-patterns.md`, `references/guides.md`:
  loaded on demand when `SKILL.md` points to them.
- `evals/`: routing, triggering and mode eval sets, with results per version.
- `scripts/validate_skill.py`: frontmatter, description length (1,024 max, no
  angle brackets), and that every `references/` file named in `SKILL.md` exists.
- `scripts/check_links.py`: catalog slugs resolve; the catalog matches the live
  index both ways and by name; reference slugs exist in the catalog; stated
  counts match; every other docs URL resolves.
- `Makefile`: `setup`, `build`, `verify`, `lint`, `check-links`.
- `.github/workflows/ci.yml` and `release.yml`: CI checks; release on a `v*` tag.

## The package is a build artifact

`temporal-patterns.skill` is a ZIP of `temporal-patterns/SKILL.md` and
`temporal-patterns/references/*.md`. It isn't committed (`dist/` and `*.skill` are
gitignored). CI uploads it on every PR; tagged releases attach it.

## Editing workflow

1. Edit `SKILL.md` or `references/`.
2. Run `make lint`, `make verify` and `make check-links`.
3. If routing text, the description or the catalog changed, re-run the evals and
   record the results in `evals/README.md`.
4. Add an `## [Unreleased]` entry to `CHANGELOG.md`.

## Conventions that keep the skill correct

- **The catalog is an index, not the implementation.** Don't embed pattern code.
  Each pattern is referenced by slug; its page is
  `https://docs.temporal.io/design-patterns/{slug}.md`.
- **Pattern names are product terms.** Use the name from the live index exactly.
  The Priority pattern keeps the old slug `priority-task-queues`.
- **Stages are dated.** The features table and catalog notes carry release stages
  as of a date. Quote them as the docs state them.
- **The parsers depend on the table layout.** `check_links.py` reads catalog rows
  shaped `| Name | \`slug\` | Use it when |` under `## Pattern catalog`, and slug
  lines in `references/` that start with `- **Patterns:**`, `- **Also
  consider:**` or `- **Related:**`. Keep those shapes or update the script in the
  same change.
- **The description must stay at or under 1,024 characters.** Longer ones are
  cut off on claude.ai.
- **Boundaries:** the `temporal-developer` skill owns SDK setup, determinism and
  testing; the Temporal Docs search (Kapa) is for free-text lookup after a pattern
  is chosen.
- **Prose style:** Google developer documentation style. Plain and active; no em
  or en dashes and no arrows.
- **Public repo:** no customer names, internal call details or pricing.

## Keeping the catalog current

The live index at `https://docs.temporal.io/design-patterns.md` is the source of
truth, and the pages are maintained in `temporalio/documentation` under
`docs/design-patterns/`. `make check-links` reports any pattern the index has and
the catalog lacks, and any name that differs.
