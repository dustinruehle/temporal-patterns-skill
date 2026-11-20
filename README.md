# Temporal Patterns: a Claude skill

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![CI](https://github.com/dustinruehle/temporal-patterns-skill/actions/workflows/ci.yml/badge.svg)](https://github.com/dustinruehle/temporal-patterns-skill/actions/workflows/ci.yml)
[![Latest release](https://img.shields.io/github/v/release/dustinruehle/temporal-patterns-skill)](https://github.com/dustinruehle/temporal-patterns-skill/releases/latest)

A [Claude skill](https://support.claude.com) that makes Claude pick from
Temporal's official Workflow design patterns instead of inventing a Workflow
shape, and tells it when the answer is a platform feature or an anti-pattern
instead.

## What it does

Temporal publishes a catalog of 35 Workflow design patterns (Saga,
Continue-As-New, Signal with Start, Fan-Out, Fairness, Approval, Local Activities
and more) in 10 problem domains, at
[docs.temporal.io/design-patterns](https://docs.temporal.io/design-patterns).
Every pattern has its own page.

With the skill, Claude does the following:

1. **Routes a problem to a named pattern**, by symptom ("my history is getting
   too big" is Continue-As-New; "undo earlier steps when a later one fails" is
   Saga) or by use case ("payments", "AI agent platform", "ETL").
2. **Routes to a feature when that's the answer.** Recurring runs are Schedules,
   cross-team calls are Nexus, safe deploys are Worker Versioning, one retried job
   is a Standalone Activity. Each comes with its release stage and docs link.
3. **Flags anti-patterns**, such as a Workflow used as a high-rate datastore or a
   parent that fans out thousands of children, with the limit each one breaks
   and what to do instead.
4. **Fetches the canonical page** before it writes code or states specifics, so
   details come from the live docs.

### Where it helps most

The largest gain is exact pattern names, slugs and canonical links: decks,
enablement and answers you can cite. In a test, a slide outline scored 8.5 out of
10 with the skill and 4 without it; without it, Claude invented pattern names and
linked old blog posts. Code reviews gain mostly citations. See
[evals/README.md](evals/README.md) for the numbers.

### Use cases covered

The use-case map groups 16 verticals into 6 groups. Name yours, and Claude starts
from the patterns and features it usually needs, then narrows to your problem.

- **AI workloads:** AI agents, agent platforms, processing pipelines, model training
- **Commerce and payments:** order management and fulfillment, payment processing and settlement, booking and reservations
- **Data and infrastructure:** data pipelines and ETL, infrastructure automation and CI/CD
- **Identity and lifecycle:** customer onboarding and identity, entity lifecycle management
- **Comms and fintech:** communications and marketing, financial services and lending
- **Platform and ops:** control plane operations, inventory and logistics, customer service and support

## What it isn't

- It isn't a replacement for the `temporal-developer` skill, which covers SDK
  setup, determinism rules and testing. This skill picks the shape; that one gets
  the SDK details right.
- It isn't a copy of the docs. It's an index and routing logic that point at the
  live pages.

## Install

1. Download `temporal-patterns.skill` from the
   [Releases page](https://github.com/dustinruehle/temporal-patterns-skill/releases/latest).
2. In Claude (web, desktop or mobile), start a chat and upload the file.
3. On the file's card, click **Save skill**. If you don't see **Save skill**,
   your organization may not have skill creation turned on; ask an org owner.
4. The skill loads automatically when a chat involves Temporal design. You don't
   need to call it.

For Claude Code, unzip the package into `~/.claude/skills/` (you get
`~/.claude/skills/temporal-patterns/`), or clone this repo and link that folder to
it. For org-wide distribution, see Anthropic's skills documentation at
[support.claude.com](https://support.claude.com).

## Use it

Work as usual. Some examples:

- **Coding:** "Help me build a Temporal Workflow in TypeScript that processes 2M
  records without blowing up history." Claude names Batch Iterator or Sliding
  Window, warns about the pending Child Workflow limit, and fetches the pages.
- **Customer question:** "A customer asked how to undo steps 1 and 2 when step 3
  fails." Claude explains the Saga Pattern and its compensations and links the
  page.
- **Use case:** "We're building order fulfillment on Temporal. Which patterns do
  we need?" Claude starts from the order management stack and narrows it.
- **Decks:** "Outline Temporal's design patterns for an exec briefing." Claude
  uses the exact names from the live index and the 10 domains as sections.

Tips:

- You don't need to say "pattern". Describe the problem ("don't overwhelm the
  downstream API", "wait for a human approval").
- For customer-facing work, ask Claude to cite the canonical page.
- If Claude names a pattern that isn't in the catalog, ask it to check the live
  index.

## Repository layout

| Path | What it is |
|---|---|
| `SKILL.md` | The skill: rules, modes, pattern catalog, features table, choosing notes, limits, anti-patterns. |
| `references/` | Files the skill loads when needed: use-case stacks, anti-pattern detail, docs guides. |
| `evals/` | Routing, triggering and mode eval sets, with results per version. |
| `scripts/` | `validate_skill.py` (frontmatter, description length, references) and `check_links.py` (catalog against the live docs). |
| `Makefile` | `make build`, `make verify`, `make lint`, `make check-links`, `make setup`. |
| `.github/workflows/` | CI (lint, build, verify, link check) and Release (build and attach the `.skill`). |

The `temporal-patterns.skill` package is a build artifact and isn't committed.
CI builds it on every PR, and tagged releases attach it to the
[Releases page](https://github.com/dustinruehle/temporal-patterns-skill/releases).
To build it yourself, run `make build`; the output is in `dist/`.

## Contributing

Wrong route? Missing pattern? The skill fires when it shouldn't? See
[CONTRIBUTING.md](CONTRIBUTING.md), and open an issue or PR.

## License

[MIT](LICENSE) © Dustin Ruehle
