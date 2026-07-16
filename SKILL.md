---
name: temporal-patterns
description: >-
  Catalog of Temporal's official, battle-tested Workflow design patterns (Saga,
  Continue-As-New, Signal-with-Start, Entity Workflow, Fan-Out, Fairness, Local
  Activities, Approval, and ~30 more) by problem domain, with a
  problem-to-pattern routing map and live links to each pattern's canonical page.
  Use WHENEVER working with Temporal design patterns in any mode: writing or
  reviewing Workflow/Activity code (pick the right named pattern and fetch its
  page before coding), answering customer or teammate questions on how to solve a
  problem in Temporal (map it to a pattern, explain tradeoffs), or building
  slides, decks, or enablement (exact names, domain groupings, canonical
  descriptions). Trigger even when the user never says "pattern" — e.g. "how do I
  do human approval in a workflow", "my history is getting too big", "undo
  earlier steps when a later one fails", "don't overwhelm the downstream API",
  "one tenant is starving the others". Always reach for a catalog pattern instead
  of hand-rolling a Workflow shape.
metadata:
  version: 0.1.0
  source: https://docs.temporal.io/design-patterns.md
---

# Temporal Design Patterns

Temporal's durable-execution primitives compose into a catalog of proven, named
design patterns. Reaching for a named pattern beats inventing a Workflow shape:
the pattern already encodes the failure handling, the history-growth control, and
the edge cases someone else already hit. This skill exists so that — whether
coding, answering a question, or building a deck — you select from the catalog
first and pull canonical detail on demand.

## The one rule that makes this skill work

**The catalog below is an index, not the implementation.** Each pattern has a
canonical markdown page. Select the pattern from memory using the index and
routing map here; **fetch the pattern page before writing implementation code or
asserting specifics** (guarantees, limits, SDK support, exact mechanics). Do not
reconstruct pattern code from memory — the pages are the source of truth and stay
current as SDKs change. This matters most for customer-facing work, where a
confident-but-stale detail is worse than a fetched, verified one.

### URL construction (deterministic)

- Full index: `https://docs.temporal.io/design-patterns.md`
- Any pattern: `https://docs.temporal.io/design-patterns/{slug}.md`
- Example: `https://docs.temporal.io/design-patterns/saga-pattern.md`

The `{slug}` for every pattern is in the catalog tables below. Append `.md` for
the clean, token-cheap version (drop it for the human-readable web page to share
with a customer).

If fetching isn't available in the current environment, don't guess at
implementation detail — name the pattern, give the canonical URL for the user to
open, and keep any specifics conservative and clearly flagged as unverified.

> The catalog is a snapshot as of skill authoring (34 patterns, 10 domains). The
> live index is the real source of truth. If a pattern the user needs isn't
> listed, or you suspect the catalog has grown, re-fetch the index before
> concluding a pattern doesn't exist.

---

## How to work in each mode

### Mode 1 — Coding Temporal

1. Name the pattern(s) using the routing map. If several compose (common), name
   each.
2. **Fetch each pattern's `.md` page before writing Workflow/Activity code.**
3. For real implementation, also load the language guidance from the
   `temporal-developer` skill (determinism rules, gotchas, testing) — this skill
   picks the *shape*, that skill gets the *SDK details* right.
4. If nothing in the catalog fits, say so plainly and drop to first principles
   with `temporal-developer` — do **not** invent a "pattern" that isn't in the
   catalog.

### Mode 2 — Customer / prospect / teammate questions

1. Map the described problem to a pattern (or a small set) via the routing map.
2. Lead with the pattern name, then a plain-language "what it does / when to use
   it," then the honest tradeoff or the adjacent pattern it's often confused with
   (see *Choosing between close patterns*).
3. Fetch the page when the answer needs specifics — durability guarantees, size
   limits, SDK availability — and cite the canonical page rather than asserting
   from memory. Prefer conservative, verified language over unverified specifics.
4. Offer the human-readable doc link (slug without `.md`) so they can go deeper.

### Mode 3 — Decks / enablement

1. Use the **exact** pattern names — they're product terminology; don't rename or
   pluralize creatively.
2. The 10 domains are a ready-made deck/section structure (one domain per section,
   patterns as bullets).
3. Keep descriptions crisp; fetch a pattern's page when a slide needs a specific
   mechanism, guarantee, or diagram description. Don't invent numbers or claims —
   if a slide needs a stat, fetch it or flag it as needing verification.

### The flow, in one example

> **User:** "We call a partner API that undoes a booking, a payment, and a
> loyalty credit — if the payment reversal fails I need the booking un-cancelled."
>
> 1. **Route:** "undo earlier steps when a later step fails" → **Saga Pattern**
>    (`saga-pattern`). Compensation-heavy phrasing also means each step needs an
>    idempotent compensating action.
> 2. **Fetch:** `https://docs.temporal.io/design-patterns/saga-pattern.md`
>    before writing or describing the compensation ordering.
> 3. **Build/answer** from the fetched page — and if coding, pull the language
>    reference from `temporal-developer` for the SDK's error-handling idioms.

---

## Problem → pattern routing map

Match the user's symptom (left) to the pattern (right), even when they never say
"pattern." Then fetch the page.

| If the user is trying to… | Pattern(s) | slug |
|---|---|---|
| Break a big workflow into smaller reusable units | Child Workflows | `child-workflows` |
| Run many activities at once for throughput | Parallel Execution | `parallel-execution` |
| Race several activities, take the first, cancel the rest (hedging) | Pick First | `pick-first` |
| Start a workflow only if it isn't running, else just signal it | Signal with Start | `signal-with-start` |
| Do a synchronous request/response with validation and a returned result | Request-Response via Updates | `request-response-via-updates` |
| Model a long-lived business entity (account, cart, device, user) | Entity Workflow | `entity-workflow` |
| Stop history from growing without bound in a long loop | Continue-As-New | `continue-as-new` |
| Have a timer they can extend, shorten, or cancel from events | Updatable Timer | `updatable-timer` |
| Poll an external service/resource until it's ready | Polling External Services | `polling` |
| Run a long activity that reports progress and can resume after failure | Long-Running Activity | `long-running-activity` |
| Create now but defer execution (schedule-once, grace period) | Delayed Start | `delayed-start` |
| Integrate webhooks in/out durably, complete activities via task token | Delayed Callback (Webhooks) | `delayed-callback` |
| Wait for a human decision / approval before proceeding | Approval | `approval` |
| Undo/compensate earlier steps when a later step fails (rollback) | Saga Pattern | `saga-pattern` |
| Return a result to the caller immediately but keep processing | Early Return | `early-return` |
| Cap retry attempts because each attempt costs money / a paid resource | Fixed Count of Retries | `fixed-count-retries` |
| Bound total elapsed retry time to an SLA regardless of attempt count | Fixed Wall-Time Retries | `fixed-wall-time-retries` |
| Fail fast on unrecoverable errors (validation, missing record) | Non-Retryable Errors | `non-retryable-errors` |
| Wait a specific interval the error itself dictates (e.g. Retry-After) | Delayed Retry | `delayed-retry` |
| Retry fast first, then shift to slow, staying alive until recovery | Fast/Slow Retries | `fast-slow-retries` |
| Alert on-call when retries silently persist toward an SLA breach | Retry Alerting via Metrics | `retry-metrics` |
| Park after retries exhaust, wait for a human fix, then resume | Resumable Activity | `resumable-activity` |
| Process a large record set across parallel children, auto-scaling | Fan-Out with Child Workflows | `fanout-child-workflows` |
| Page an unbounded dataset with exactly-once, no history overflow | Batch Iterator | `batch-iterator` |
| Keep a fixed number of children active, starting a new one as each finishes | Sliding Window | `sliding-window` |
| Recursively split + aggregate a dataset (map then reduce, tree) | MapReduce Tree | `mapreduce-tree` |
| Cap activity call rate against a downstream service so it isn't overwhelmed | Downstream Rate Limiting | `downstream-rate-limiting` |
| Make time-sensitive work jump ahead of lower-priority work | Priority Task Queues | `priority-task-queues` |
| Stop one tenant/user's burst from starving the others (multi-tenant) | Fairness | `fairness` |
| Shave latency for a short idempotent step, skipping server round-trips | Local Activities | `local-activities` |
| Get the lowest possible first-response latency | Early Return + Local Activities | `early-return-local-activities` |
| Cut workflow-start latency via a co-located worker | Eager Workflow Start | `eager-workflow-start` |
| Route work to a specific worker/host (affinity, host-local cache/GPU) | Worker-Specific Task Queues | `worker-specific-taskqueue` |
| Inject DB clients/config/secrets into activities, keep workflow deterministic | Activity Dependency Injection | `activity-dependency-injection` |

---

## Full catalog by domain

Descriptions are terse pointers, not the full page. Fetch the slug for detail.

### Task orchestration
- **Child Workflows** — `child-workflows` — decompose into smaller units, each with its own ID, history, lifecycle.
- **Parallel Execution** — `parallel-execution` — run activities concurrently with error handling and controlled parallelism.
- **Pick First (Race)** — `pick-first` — start several in parallel, use the first result, cancel the rest.

### Workflow messaging
- **Signal with Start** — `signal-with-start` — start-if-absent, else deliver the signal to the running workflow.
- **Request-Response via Updates** — `request-response-via-updates` — synchronous, validated request/response that mutates state and returns a result.

### Entity & lifecycle
- **Entity Workflow** — `entity-workflow` — model a long-lived business entity as one persistent workflow.
- **Continue-As-New** — `continue-as-new` — complete the current run and restart with fresh history to bound growth.
- **Updatable Timer** — `updatable-timer` — a timer that responds to signals/updates: extend, shorten, cancel.

### External interaction
- **Polling External Services** — `polling` — frequent / infrequent / periodic polling strategies.
- **Long-Running Activity** — `long-running-activity` — heartbeat progress, resume after failure, support cancellation.
- **Delayed Start** — `delayed-start` — create immediately, defer execution until a delay expires.
- **Delayed Callback (Webhooks)** — `delayed-callback` — inbound webhooks via signals, outbound via durable timers, async completion via task token.
- **Approval** — `approval` — human-in-the-loop; block until an external decision, captured via signal with metadata.

### Distributed transactions
- **Saga Pattern** — `saga-pattern` — each step has a compensation that undoes it if a later step fails.
- **Early Return** — `early-return` — return a result synchronously while processing continues in the background.

### Error handling & retry
- **Fixed Count of Retries** — `fixed-count-retries` — cap attempts to control cost per attempt.
- **Fixed Wall-Time Retries** — `fixed-wall-time-retries` — bound total elapsed retry time to an SLA.
- **Non-Retryable Errors** — `non-retryable-errors` — mark errors that will never succeed so Temporal fails fast.
- **Delayed Retry** — `delayed-retry` — override the next interval via `nextRetryDelay` when the error says how long to wait.
- **Fast/Slow Retries** — `fast-slow-retries` — short interval first, then long once fast retries exhaust, keeping the workflow alive.
- **Retry Alerting via Metrics** — `retry-metrics` — emit a custom metric past an attempt threshold to surface silent failures.
- **Resumable Activity** — `resumable-activity` — park after retries exhaust, wait for a human correction, resume where it left off.

### Batch processing
- **Fan-Out with Child Workflows** — `fanout-child-workflows` — distribute a large record set across parallel children.
- **Batch Iterator** — `batch-iterator` — page unbounded datasets via Continue-As-New with exactly-once guarantees.
- **Sliding Window** — `sliding-window` — keep a fixed count of children active, starting a new one as each completes.
- **MapReduce Tree** — `mapreduce-tree` — recursively split into a binary tree of children, process leaves, aggregate up.

### QoS & throughput
- **Downstream Rate Limiting** — `downstream-rate-limiting` — route throttled activities to a dedicated task queue with a throughput-limited worker pool.
- **Priority Task Queues** — `priority-task-queues` — priority levels so urgent work runs ahead within one task queue.
- **Fairness** — `fairness` — spread worker capacity across tenants/users so a burst from one doesn't starve others.

### Performance & latency
- **Local Activities** — `local-activities` — run the activity in-process in the Workflow Task, no scheduling round-trip. Short, idempotent, latency-sensitive only.
- **Early Return + Local Activities** — `early-return-local-activities` — Early Return with Phase 1 as local activities for the lowest first-response latency.
- **Eager Workflow Start** — `eager-workflow-start` — dispatch the first Workflow Task to a co-located worker, bypassing Matching. Requires shared process + client connection.

### Worker configuration
- **Worker-Specific Task Queues** — `worker-specific-taskqueue` — unique task queues for worker affinity / host-specific processing.
- **Activity Dependency Injection** — `activity-dependency-injection` — inject external deps at worker startup; keeps workflow code deterministic and activities testable.

---

## Patterns that compose

Real solutions usually stack patterns. Common compositions:

- **Batch Iterator** is Continue-As-New applied to paging → fetch both.
- **Fan-Out**, **Sliding Window**, and **MapReduce Tree** all build on **Child Workflows**.
- **Early Return + Local Activities** literally combines two catalog patterns.
- **Eager Workflow Start** pairs with **Local Activities** for end-to-end low latency.
- **Fairness**, **Priority Task Queues**, and **Downstream Rate Limiting** are the QoS trio — often discussed together for multi-tenant / tiered workloads.
- **Approval** and **Delayed Callback** both rely on signals + durable waits and often appear in the same human/external-driven workflow.

When a solution stacks patterns, fetch each page rather than improvising the seams.

## Choosing between close patterns

These get conflated; call out the distinction when it's the crux of a question.

- **Signal-with-Start vs Request-Response via Updates vs Early Return** — fire-and-ensure-running (signal-with-start) vs synchronous validated result (updates) vs immediate ack then keep working (early return).
- **Continue-As-New vs Batch Iterator** — history control for any long loop vs the specific paging-a-dataset application of it.
- **The seven retry patterns** — route by the *constraint*: cost per attempt → fixed count; SLA on total time → fixed wall-time; unrecoverable → non-retryable; error dictates the wait → delayed retry; downstream recovering → fast/slow; visibility to on-call → retry metrics; needs a human → resumable activity.
- **Pick First vs Parallel Execution** — first-wins-cancel-rest vs run-all-collect-all.
- **Fairness vs Priority** — even distribution across tenants vs deliberate ordering by importance.

---

## Boundaries with other tools

- **`temporal-developer` skill** — the deep SDK/build skill. Its `references/core/patterns.md` covers *conceptual primitives* (signals, queries, saga concept). **This** skill is the *composable design-pattern catalog* (34 named solution shapes). When actually coding: use this skill to choose the pattern, `temporal-developer` for language setup, determinism, gotchas, and testing. Note `temporal-developer` also has `priority-fairness.md` — use it for SDK specifics once Fairness/Priority is the chosen pattern.
- **Temporal Docs (Kapa) MCP** — semantic search over doc prose. Good for open-ended "what do the docs say about X." Poor at reliably surfacing the *structured* catalog. Prefer this skill's index for pattern selection; use Kapa for free-text doc lookup afterward.

## Guardrails

- Don't invent pattern names that aren't in the catalog. If nothing fits, say so and solve from first principles with `temporal-developer`.
- Don't write pattern implementation code, or state SDK-specific support/limits, from memory — fetch the page.
- Treat the embedded catalog as a snapshot; re-fetch the index if a needed pattern seems missing.
- Don't over-engineer. A pattern is worth its complexity only when the problem calls for it — a single activity call or a plain sequence often is the right answer. Name the pattern when it earns its place, not to show it off.
