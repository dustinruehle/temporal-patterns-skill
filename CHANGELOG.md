# Changelog

All notable changes to this skill are documented here. The format is based on
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project adheres
to [Semantic Versioning](https://semver.org/spec/v2.0.0.html). The version here
matches `metadata.version` in `SKILL.md`.

## [Unreleased]

## [0.3.0] - 2026-11-20

### Added
- **Features table**: problems whose answer is a platform feature rather than a
  pattern (Schedules, Standalone Activities, Nexus, Worker Versioning, Search
  Attributes, Workflow ID policies, Update-with-Start, Workflow Streams, External
  Storage, Activity Pause), with release stages as of 2026-11-20 and docs links.
- **Anti-patterns**: a table in `SKILL.md` and detail in
  `references/anti-patterns.md`, each with the limit it breaks and what to do
  instead. Includes a "when Temporal isn't the fit" note.
- **Limits that change which pattern you pick**: per-execution limits from the
  docs, linked.
- Choosing notes: Signal-with-Start, Update-with-Start or Early Return;
  rate limiting, Fairness, Priority or separate Task Queues; Standalone Activity
  or Workflow; Resumable Activity or Activity Pause; Delayed Start or Schedules;
  Fan-Out, Sliding Window or Batch Iterator; Updatable Timer or Event Accumulator.
- Composition note for Approval with an expiry.
- `references/guides.md`: docs guides mapped to the patterns they extend,
  including the distributed lock guide.
- Booking and reservations vertical, and per-vertical features and traps, in
  `references/use-cases.md`.
- `evals/`: routing (40 prompts), triggering (30) and mode (3) eval sets, with
  0.2.2 results.
- `make setup`.

### Changed
- `SKILL.md` restructure: the routing map and the catalog are merged into one
  table per domain, and the use-case stacks move to `references/use-cases.md`.
  The package now includes `references/`.
- Description rewritten to fit the 1,024-character limit (it was 1,263, and
  claude.ai cut it off). It names code review explicitly, puts Temporal terms in
  its examples, says "prefer" instead of "always", and lists what the skill is
  not for.
- Mode 2 leads with the customer's problem, names only the patterns their facts
  call for, and keeps to the requested length. Mode 1 loads `temporal-developer`
  for new code. Mode 3 fetches the live index once per deck.
- Use-case map updated to the v3 mapping (2026-07-08): Priority and Fairness added
  to AI processing pipelines.
- `check_links.py` checks the catalog against the live index both ways and by
  name, checks reference slugs and stated counts, and checks every other docs URL.
  It reads tables instead of punctuation.
- `validate_skill.py` enforces the description limit and checks that named
  references exist.
- Prose follows Google developer documentation style: no arrows or em dashes.

### Fixed
- "Priority Task Queues" renamed to **Priority** to match the docs (the slug
  `priority-task-queues` is unchanged).
- Fairness distributes Task dispatch, not Worker capacity; it is best effort and
  not a rate cap.
- Downstream Rate Limiting is a server-enforced start-rate cap on the Task Queue,
  not a throughput-limited Worker pool; it doesn't limit concurrency.
- Batch Iterator no longer promises exactly-once; Activities run at least once.
- Eager Workflow Start is marked Public Preview and doesn't respect Worker
  Versioning.
- Removed the stale note that Event Accumulator is missing from the docs index.
- Early Return is described as built on Update-with-Start.
- Updatable Timer routes "debounce" phrasing.

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
