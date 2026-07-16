# Changelog

All notable changes to this skill are documented here. The format is based on
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project adheres
to [Semantic Versioning](https://semver.org/spec/v2.0.0.html). The version here
matches `metadata.version` in `SKILL.md`.

## [Unreleased]

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

[Unreleased]: https://github.com/dustinruehle/temporal-patterns-skill/compare/v0.2.0...HEAD
[0.2.0]: https://github.com/dustinruehle/temporal-patterns-skill/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/dustinruehle/temporal-patterns-skill/releases/tag/v0.1.0
