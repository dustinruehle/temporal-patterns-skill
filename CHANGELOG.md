# Changelog

All notable changes to this skill are documented here. The format is based on
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project adheres
to [Semantic Versioning](https://semver.org/spec/v2.0.0.html). The version here
matches `metadata.version` in `SKILL.md`.

## [Unreleased]

## [0.2.2] - 2026-07-16

### Added
- README "Use cases covered" subsection listing the 6 buckets and 15 verticals of the
  use-case→pattern-stack map, so readers can see coverage without opening `SKILL.md`.

## [0.2.1] - 2026-07-16

### Changed
- `check_links.py` now also validates the use-case→pattern-stack section: every slug
  referenced in the routing map and use-case map must exist in the catalog (offline
  check), in addition to confirming each catalog slug resolves online.
- Frontmatter `description` now triggers on use-case/industry framing, not just symptoms.
- Use-case section instructs fetching only the selected pattern pages, not the whole stack.
- Modes 2 and 3 cross-reference the use-case→pattern-stack map.

### Fixed
- Corrected stale pattern count (34 → 35) and version references in README,
  CONTRIBUTING, and CLAUDE.
- Made previously non-clickable URLs in the README proper Markdown links.

## [0.2.0] - 2026-07-16

### Added
- **Event Accumulator** pattern (`event-accumulator`) to the catalog, routing map,
  and composition notes — a canonical pattern whose page resolves but is not yet
  listed in the docs index.
- **Use-case → pattern stack** section: top-down routing across 15 industry/use-case
  verticals (in 6 groups), reconciled from Temporal's "Use Case → Pattern Mapping v2"
  to canonical catalog slugs.
- **Cross-cutting techniques** note capturing idempotency as a technique (not a
  catalog pattern).

### Changed
- Catalog count updated from 34 to 35 patterns.

## [0.1.0] - 2026-07-16

Initial pre-release. Interfaces and catalog may change before a `1.0.0` GA.

### Added
- Initial release of the `temporal-patterns` skill.
- Problem→pattern routing map and full catalog of 34 patterns across 10 domains.
- Composition notes and "choosing between close patterns" guidance.
- Deterministic canonical-URL construction for every pattern
  (`https://docs.temporal.io/design-patterns/{slug}.md`).

[Unreleased]: https://github.com/dustinruehle/temporal-patterns-skill/compare/v0.2.2...HEAD
[0.2.2]: https://github.com/dustinruehle/temporal-patterns-skill/compare/v0.2.1...v0.2.2
[0.2.1]: https://github.com/dustinruehle/temporal-patterns-skill/compare/v0.2.0...v0.2.1
[0.2.0]: https://github.com/dustinruehle/temporal-patterns-skill/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/dustinruehle/temporal-patterns-skill/releases/tag/v0.1.0
