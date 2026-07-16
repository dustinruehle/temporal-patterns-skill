# Temporal Patterns — a Claude Skill

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![CI](https://github.com/dustinruehle/temporal-patterns-skill/actions/workflows/ci.yml/badge.svg)](https://github.com/dustinruehle/temporal-patterns-skill/actions/workflows/ci.yml)
[![Latest release](https://img.shields.io/github/v/release/dustinruehle/temporal-patterns-skill)](https://github.com/dustinruehle/temporal-patterns-skill/releases/latest)

A shared [Claude skill](https://support.claude.com) that makes Claude reach for
Temporal's official, battle-tested Workflow design patterns instead of inventing a
Workflow shape from scratch.

---

## What it does

Temporal publishes a catalog of 35 proven Workflow design patterns (Saga,
Continue-As-New, Signal-with-Start, Fan-Out, Fairness, Approval, Local Activities,
and more), grouped into 10 problem domains. The catalog lives at
[docs.temporal.io/design-patterns](https://docs.temporal.io/design-patterns), and
every pattern has its own canonical page.

This skill teaches Claude to:

1. **Recognize** when a problem maps to a named pattern — from two angles: bottom-up
   by *symptom* even when you never say "pattern" ("my history is getting too big" →
   Continue-As-New / Batch Iterator; "undo earlier steps when a later one fails" →
   Saga), and top-down by the *use case or industry* you're building ("payments" →
   Saga + idempotency + fixed-wall-time retries; "AI agent platform" → Entity
   Workflow + Continue-As-New + rate limiting).
2. **Fetch the canonical page** for that pattern before writing code or stating
   specifics, so implementation detail is always current and source-backed.
3. **Behave correctly in three modes** — writing/reviewing Temporal code, answering
   customer or teammate questions, and building decks or enablement content.

The pattern menu, a problem-to-pattern routing table, and a use-case-to-pattern-stack
map are baked into the skill so Claude always has the map. The *details* are pulled
live from the docs on demand.

## Why you want it

- **No hand-rolled Workflow shapes.** Left alone, Claude will happily improvise a
  workflow that technically runs but ignores a pattern that already solves the
  problem with the failure handling and history-growth control worked out. This
  skill makes it pick from the catalog first.
- **Always current, never stale.** The skill embeds only the index. Actual
  implementation detail is fetched from the live docs every time, so it doesn't rot
  as SDKs change. Good for customer-facing work where a confident-but-outdated
  detail is worse than a verified one.
- **Consistent across the team.** Everyone gets the same pattern vocabulary, the
  same routing logic, and the same "verify against source before it reaches a
  customer" discipline — in code, in Q&A, and in slides.
- **Works everywhere Claude does.** Once installed, it fires automatically in
  Claude Code, Claude.ai (web), and the desktop app.

## What it is NOT

- Not a replacement for the `temporal-developer` skill. That one owns SDK setup,
  determinism rules, and testing. This one owns *which pattern to use*. They work
  together: this skill picks the shape, `temporal-developer` gets the SDK details
  right.
- Not a frozen copy of the docs. It's an index plus routing logic that points at
  the live pages.

---

## Install

1. **Download the skill.** Grab the latest `temporal-patterns.skill` from the
   [**Releases page**](https://github.com/dustinruehle/temporal-patterns-skill/releases/latest).
2. Open Claude (web, desktop, or the mobile app).
3. Start a chat and attach / upload the `temporal-patterns.skill` file.
4. On the file's card, click **Save skill**. This installs it into your profile.
   - If you don't see a **Save skill** button, your organization may not have skill
     creation enabled — ask an org owner/admin to enable it or to distribute the
     skill org-wide.
5. That's it. The skill loads automatically whenever a chat involves Temporal
   design patterns — you don't need to invoke it manually.

> Installing in **Claude Code** or distributing **org-wide** may follow a different
> path (admin console / skills directory). For the current authoritative steps, see
> Anthropic's skills documentation at [support.claude.com](https://support.claude.com)
> and [docs.claude.com](https://docs.claude.com).

## Use it

You don't call the skill explicitly — just work normally. It triggers on Temporal
pattern context. Some examples:

**Coding**
> "Help me build a Temporal workflow in TypeScript that processes 2M records
> without blowing up history."

Claude will identify Batch Iterator + Fan-Out, fetch their pages, and build against
the current SDK guidance.

**Customer / teammate Q&A**
> "A customer asked how Temporal handles a distributed transaction where step 3
> fails and they need to undo steps 1 and 2. How should I answer?"

Claude will name the Saga Pattern, explain compensations and the tradeoffs, and can
pull the canonical page for specifics you can cite.

**Starting from a use case**
> "We're building order fulfillment on Temporal — which patterns do we need?"

Claude will pull the use-case stack (Entity Workflow, Saga, Signal-with-Start,
Updatable Timer, Delayed Callback, Early Return, Event Accumulator), then narrow to
what your specific problem actually calls for.

**Decks / enablement**
> "Give me a slide outline of Temporal's design patterns for an exec briefing."

Claude will use the exact pattern names and the 10 domains as a ready-made section
structure.

### Tips

- You don't need to say "pattern." Describe the *problem* ("don't overwhelm the
  downstream API," "wait for human approval," "race two calls and take the first")
  and it'll route to the right one.
- Or start from your *use case* — "we're building payments / an AI agent platform /
  ETL on Temporal" routes to the whole pattern stack for that domain, then narrows.
- For customer-facing artifacts, ask Claude to fetch and cite the canonical page so
  the detail is verified rather than recalled.
- If Claude ever invents a pattern that isn't in the catalog, tell it to check the
  live index — the skill is instructed to treat the docs as source of truth.

---

## Repository layout

| Path | What it is |
|---|---|
| `SKILL.md` | The skill itself, and the single source of truth. |
| `README.md` | This file. |
| `CONTRIBUTING.md` | How to propose fixes and additions. |
| `CHANGELOG.md` | Notable changes, per version. |
| `Makefile` | `make build` packages the `.skill`; `make lint` / `make check-links` validate it. |
| `scripts/` | Validation and link-check helpers used locally and in CI. |
| `.github/workflows/` | CI (validate + build + link check) and Release (build + attach `.skill`). |

The distributable `temporal-patterns.skill` is a **build artifact** — it is not
committed. CI rebuilds it on every PR, and tagged releases attach it to the
[Releases page](https://github.com/dustinruehle/temporal-patterns-skill/releases).
To build it yourself: `make build` (output lands in `dist/`).

## Contributing

Routing rule wrong? Pattern missing? Skill misfiring? See
[CONTRIBUTING.md](CONTRIBUTING.md) — the skill is a single markdown file, so fixes
are quick. Please open an issue or PR.

## License

[MIT](LICENSE) © Dustin Ruehle
