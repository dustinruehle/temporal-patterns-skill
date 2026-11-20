---
name: temporal-patterns
description: >-
  Catalog of Temporal's official Workflow design patterns (Saga, Continue-As-New,
  Entity Workflow, Fan-Out, Fairness, Approval and more) by
  problem domain, with problem and use-case maps, related features,
  anti-patterns and live links to each canonical page.
  Use it whenever you design, write or review Temporal Workflow or Activity code
  (a file, diff or snippet), answer a customer or teammate question about how to
  solve a problem in Temporal, or build Temporal slides or enablement. Trigger
  even when nobody says "pattern": "my Workflow history is too big", "undo
  earlier steps when a later one fails", "human approval in a Workflow", "don't
  overwhelm the downstream API", "one tenant's Workflows starve the others".
  Also trigger on use-case framings: "payments, AI agents, order
  fulfillment or ETL on Temporal". Not for other engines or queues (Airflow,
  Step Functions, GitHub Actions, BullMQ), Worker tuning, CLI or Cloud admin,
  pricing, or debugging one non-determinism error (do use it for safe Workflow
  deploys).
metadata:
  version: 0.3.0
  source: https://docs.temporal.io/design-patterns.md
---

# Temporal Design Patterns

Temporal's durable execution primitives compose into a catalog of named design
patterns. A named pattern already handles the failure cases, history growth and
edge cases that a hand-rolled Workflow shape tends to miss. Use this skill to pick
from the catalog first, then pull the canonical detail when you need it. Prefer a
catalog pattern over a hand-rolled shape, but when the right answer is a platform
feature, a single Activity or not Temporal at all, say so.

## The rule that makes this skill work

**This file is an index, not the implementation.** Pick the pattern from the
catalog here, then **fetch its page before you write implementation code or state
specifics** (guarantees, limits, SDK support, exact mechanics). Don't rebuild
pattern code from memory: the pages are the source of truth and change as the
SDKs change. This matters most in customer-facing work, where a confident but
stale detail does more harm than a fetched one.

- Full index: `https://docs.temporal.io/design-patterns.md`
- One pattern: `https://docs.temporal.io/design-patterns/{slug}.md`, for example
  `https://docs.temporal.io/design-patterns/saga-pattern.md`
- Drop `.md` for the web page you share with a person.
- Any docs page has a Markdown version: append `.md` to its URL.

If you can't fetch in this environment, name the pattern, give the canonical URL,
and mark any specifics as unverified.

> Snapshot as of 2026-11-20: 35 patterns in 10 domains. The live index is the
> source of truth. If a needed pattern seems missing, fetch the index before you
> conclude it doesn't exist. The pattern pages are maintained in the
> `temporalio/documentation` repo (`docs/design-patterns/`).

## How to work in each mode

### Mode 1: writing or reviewing code

1. Name the pattern or patterns from the catalog. Several often compose.
2. Fetch each pattern page before you write Workflow or Activity code.
3. For new code, or when a review rewrites code, load the `temporal-developer`
   skill before you write SDK code. This skill picks the shape; that one gets
   determinism, SDK idioms and testing right.
4. For a review, fetch only the pages for patterns that fix a defect you found,
   and cite them next to each finding.
5. If nothing in the catalog fits, check the features table and the anti-patterns
   below, then say so plainly. Don't invent a pattern name.

### Mode 2: customer, prospect or teammate questions

1. Lead with the customer's problem in their words and what Temporal does about
   it. Put the pattern name after that, with its link, as the term they can look
   up.
2. Name only the patterns the customer's stated facts call for. Don't add a step
   they didn't describe to justify a pattern; if one might apply later, ask about
   it instead. This limits pattern names, not standard practice: still say when
   independent calls can run in parallel. Link every pattern you name. Keep to
   the requested length; names and links count toward it.
3. If the question is framed by industry or use case, start from the use-case
   stacks in `references/use-cases.md`, then narrow.
4. Check the features table: if a Workflow waits for days, mention Worker
   Versioning; if the ask is recurring, it's Schedules; across teams, it's Nexus.
5. Give the honest tradeoff, or the close pattern it gets confused with (see
   "Choosing between close patterns").
6. Fetch the page when the answer needs specifics, and cite it. Check the release
   stage on the page before you quote it to a customer.

### Mode 3: slides and enablement

1. Fetch the live index once per deck and use its names exactly. Pattern names
   are product terms: don't rename or pluralize them.
2. The 10 domains make a ready section structure. For an industry angle, use the
   verticals in `references/use-cases.md`.
3. Fetch a pattern page when a slide needs a mechanism, a guarantee or a diagram.
   Don't invent numbers; fetch them or flag them for checking.
4. Check the features table: when a slide uses a pattern that pairs with a
   feature (Request-Response via Updates with Update-with-Start, Entity Workflow
   with Worker Versioning), name the feature and label it a feature.
5. Don't mention this skill or its lists in the deck.

### Example

> **User:** "We call a partner API to book, charge and add loyalty points. If the
> charge fails, the booking has to be released."
>
> 1. **Route:** undo earlier steps when a later one fails: **Saga Pattern**
>    (`saga-pattern`). Each step needs an idempotent compensation.
> 2. **Fetch:** `https://docs.temporal.io/design-patterns/saga-pattern.md` before
>    you describe the compensation order.
> 3. **Answer or build** from the page. For code, use `temporal-developer` for
>    the SDK's error-handling idioms.

## Pattern catalog

Match the user's symptom to the "Use it when" column, even when they never say
"pattern". Descriptions are pointers; fetch the page for detail.

### Task orchestration

| Pattern | slug | Use it when |
|---|---|---|
| Child Workflows | `child-workflows` | A big Workflow should split into smaller units, each with its own ID, history and lifecycle. |
| Parallel Execution | `parallel-execution` | Many Activities should run at once for throughput, with error handling and bounded parallelism. |
| Pick First (Race) | `pick-first` | Several Activities race; use the first result and cancel the rest (hedging). Racing Activities must heartbeat to see the cancel. |

### Workflow messaging

| Pattern | slug | Use it when |
|---|---|---|
| Signal with Start | `signal-with-start` | Start a Workflow if it isn't running, otherwise deliver the Signal to it. Atomic and fire-and-forget. |
| Request-Response via Updates | `request-response-via-updates` | A caller needs a validated request that changes Workflow state and returns a typed result synchronously. |
| Event Accumulator | `event-accumulator` | A burst of Signals from many senders should be deduplicated by key and processed as one batch after a sliding inactivity timeout. |

### Entity & lifecycle

| Pattern | slug | Use it when |
|---|---|---|
| Entity Workflow | `entity-workflow` | A long-lived business entity (account, device, order) gets one Workflow, and Signals and Updates drive each change. Low message rates only: see Anti-patterns. |
| Continue-As-New | `continue-as-new` | History grows without bound in a long loop: finish the run and restart with fresh history. Use the SDK's suggested-Continue-As-New check, let Signal and Update handlers finish first, and carry forward only the state you need. |
| Updatable Timer | `updatable-timer` | A deadline must be extended, shortened, cancelled or debounced by Signals or Updates. The page is titled "Updatable / Debounced Timer". |

### External interaction

| Pattern | slug | Use it when |
|---|---|---|
| Polling External Services | `polling` | You poll an external resource until it's ready: frequent, infrequent or periodic. |
| Long-Running Activity | `long-running-activity` | A long Activity reports progress with heartbeats, resumes after failure and supports cancellation. |
| Delayed Start | `delayed-start` | Create the Workflow now and start it after a one-time delay (grace period, schedule once). Recurring runs are Schedules, a feature. |
| Delayed Callback (Webhooks) | `delayed-callback` | Webhooks must be durable: inbound calls arrive as Signals, outbound calls fire after a durable sleep, Activities complete later with a task token. Race the wait against a timer in case the callback never arrives. |
| Approval | `approval` | The Workflow waits for a human decision, delivered as a Signal with metadata. |

### Distributed transactions

| Pattern | slug | Use it when |
|---|---|---|
| Saga Pattern | `saga-pattern` | Earlier steps must be undone when a later step fails. Register each compensation before its step runs, run them in reverse order, and make them idempotent. Business failures that should compensate are Non-Retryable Errors. |
| Early Return | `early-return` | The caller needs a result right away while the Workflow keeps working. Built on Update-with-Start. |

### Error handling & retry

| Pattern | slug | Use it when |
|---|---|---|
| Fixed Count of Retries | `fixed-count-retries` | Each attempt costs money or a limited resource, so attempts are capped. |
| Fixed Wall-Time Retries | `fixed-wall-time-retries` | Total retry time must fit an SLA, whatever the attempt count. |
| Non-Retryable Errors | `non-retryable-errors` | Some errors never succeed (validation, missing record), so fail fast. |
| Delayed Retry | `delayed-retry` | The error says how long to wait (for example Retry-After): set `nextRetryDelay` on the failure. Maximum attempts and timeouts in the Retry Policy still apply. |
| Fast/Slow Retries | `fast-slow-retries` | Retry fast first, then slowly without limit, so the Workflow outlasts a long outage. |
| Retry Alerting via Metrics | `retry-metrics` | On-call must see silent retries before an SLA breach: emit a metric past an attempt threshold. |
| Resumable Activity | `resumable-activity` | After retries run out, park the Workflow, wait for a human fix by Signal, then resume where it stopped. |

### Batch processing

| Pattern | slug | Use it when |
|---|---|---|
| Fan-Out with Child Workflows | `fanout-child-workflows` | A large record set is spread across parallel Child Workflows. Watch the pending Child Workflow limit. |
| Batch Iterator | `batch-iterator` | An unbounded dataset is paged one page per run with Continue-As-New, with the offset as a durable checkpoint. Activities run at least once, so make record processing idempotent. |
| Sliding Window | `sliding-window` | A fixed number of Child Workflows stay active, and a new one starts as each finishes. |
| MapReduce Tree | `mapreduce-tree` | A dataset is split recursively into a tree of Child Workflows, leaves run in parallel and results aggregate up. |

### QoS & throughput

| Pattern | slug | Use it when |
|---|---|---|
| Downstream Rate Limiting | `downstream-rate-limiting` | Calls per second to a downstream service must be capped: route its Activities to a dedicated Task Queue with a server-enforced rate cap, adjustable at runtime. Set it with the Worker option `maxTaskQueueActivitiesPerSecond`, or at runtime with `temporal task-queue config set --queue-rps-limit`. It limits starts per second, not how many run at once, and retries count against it. |
| Priority | `priority-task-queues` | Urgent work must dispatch ahead of other work on one Task Queue. Priority keys run from 1 (highest) to 5 (default 3). It orders dispatch only: no preemption, no reserved capacity. GA. |
| Fairness | `fairness` | One tenant's burst must not starve the others on a shared Task Queue: Task dispatch is shared across Fairness keys by weight. Best effort; not a rate cap or isolation; enabled per Namespace. GA. |

The Priority slug keeps the pattern's old name, `priority-task-queues`. The
pattern name is "Priority".

### Performance & latency

| Pattern | slug | Use it when |
|---|---|---|
| Local Activities | `local-activities` | A short, idempotent step on a latency-sensitive path runs in the Worker process, skipping server round-trips. Only for steps of a few seconds at most: it re-runs if the Worker crashes before the Workflow Task completes, and it bypasses the Task Queue, so no server rate limit. |
| Early Return + Local Activities | `early-return-local-activities` | The first response must be as fast as possible: Early Return with Phase 1 as Local Activities. |
| Eager Workflow Start | `eager-workflow-start` | Start latency matters and the Worker shares a process with the starter: the first Workflow Task skips the Matching Service. Public Preview; it doesn't respect Worker Versioning; check SDK support on the page. |

### Worker configuration

| Pattern | slug | Use it when |
|---|---|---|
| Worker-Specific Task Queues | `worker-specific-taskqueue` | Activities must run on a specific Worker or host (affinity, local files or cache, GPU). |
| Activity Dependency Injection | `activity-dependency-injection` | Activities need clients, config or secrets injected at Worker startup, keeping Workflows deterministic and Activities testable. |

## Features that answer the problem instead of a pattern

When the symptom matches a row here, name the feature and its link instead of
forcing the nearest pattern. Stages are as of 2026-11-20; check the page before
you quote one.

| If the user is trying to | Feature | Stage | Docs |
|---|---|---|---|
| Run something on a recurring schedule (cron, calendar), with an overlap policy (default Skip), pause and backfill | Schedules | GA | `https://docs.temporal.io/schedule` |
| Run one durable, retried task or a job queue, with no orchestration | Standalone Activities | GA; operator commands Public Preview | `https://docs.temporal.io/standalone-activity` |
| Call another team's service or another Namespace durably | Nexus | Varies by SDK; check the page | `https://docs.temporal.io/nexus` |
| Ship new Workflow code without breaking running Workflows (pinned or auto-upgrade; replay tests in CI) | Worker Versioning | GA | `https://docs.temporal.io/worker-versioning` |
| Find Workflows by business fields (customer ID, status) | Search Attributes | GA | `https://docs.temporal.io/search-attribute` |
| Stop duplicate starts for one business key | Workflow ID as the key. The conflict policy covers a running Workflow (Use Existing attaches to it; the default, Fail, returns an already-started error); the reuse policy covers a closed one | GA | `https://docs.temporal.io/workflow-execution/workflowid-runid` |
| Start a Workflow if needed and get a result back in one call | Update-with-Start | Check the SDK page | `https://docs.temporal.io/sending-messages#update-with-start` |
| Stream progress or tokens to a UI while a Workflow runs | Workflow Streams | Public Preview | `https://docs.temporal.io/workflow-streams` |
| Pass payloads too large for Event History | External Storage | Public Preview | `https://docs.temporal.io/external-storage` |
| Hold, resume or reset a failing Activity without a code change | Activity Pause, Unpause and Reset | Public Preview | `https://docs.temporal.io/activity-operations` |
| Serialize access to one named shared resource (lock, semaphore, mutex). To cap calls to a downstream API, use Downstream Rate Limiting instead | Docs guide, not a catalog pattern | Guide | `https://docs.temporal.io/guides/lock-shared-resources` |

Patterns and features often pair: Entity Workflow, Approval and any multi-day
wait need Worker Versioning; Request-Response via Updates and Early Return use
Update-with-Start.

## Choosing between close patterns

Call out the distinction when it's the crux of the question.

- **Signal-with-Start, Update-with-Start or Early Return:** Signal-with-Start
  makes sure the Workflow runs and delivers a fire-and-forget Signal, atomically.
  Update-with-Start does the same and returns a validated result, but it is not
  atomic: the Workflow can start even if the Update isn't delivered. Early Return
  is Update-with-Start used to answer fast while the Workflow keeps working.
- **Downstream Rate Limiting, Fairness, Priority or separate Task Queues:** a
  global cap on one downstream is a Task Queue rate limit. A per-tenant cap on a
  shared queue is a Fairness key rate limit. Priority is strict ordering by
  urgency; Fairness is weighted sharing across keys within one priority level; use
  both for tiered SLAs. A cap on how many calls run at once is a Worker setting on
  a dedicated Task Queue (see the Downstream Rate Limiting page). For hard
  isolation, use separate Task Queues with dedicated Workers.
- **Standalone Activity or Workflow:** one retryable unit of work with no waits,
  state or messages is a Standalone Activity. Dependent steps, waits, messages or
  compensation need a Workflow.
- **Resumable Activity or Activity Pause:** Resumable Activity is Workflow code
  that waits for a corrective Signal and reruns with new input. Activity Pause,
  Unpause and Reset are operator controls from the CLI or UI that hold or restart
  retries with no code change and don't change the input.
- **Delayed Start or Schedules:** one delayed start is Delayed Start; a recurring
  run is Schedules.
- **Fan-Out, Sliding Window or Batch Iterator:** above a few hundred children,
  bound concurrency with Sliding Window, or page with Batch Iterator.
- **Updatable Timer or Event Accumulator:** one adjustable deadline, or many
  events collected, deduplicated and processed as one batch after inactivity.
- **Continue-As-New or Batch Iterator:** history control for any long loop, or
  its specific use for paging a dataset.
- **Pick First or Parallel Execution:** first result wins and the rest are
  cancelled, or run all and collect all.
- **The seven retry patterns:** route by the constraint. Cost per attempt: Fixed
  Count. SLA on total time: Fixed Wall-Time. Never succeeds: Non-Retryable Errors.
  The error says when: Delayed Retry. Downstream recovering slowly: Fast/Slow.
  On-call visibility: Retry Alerting via Metrics. Needs a human fix: Resumable
  Activity.

## Patterns that compose

- **Batch Iterator** is Continue-As-New applied to paging; fetch both.
- **Fan-Out**, **Sliding Window** and **MapReduce Tree** build on **Child
  Workflows**.
- **Early Return + Local Activities** combines two catalog patterns, and **Eager
  Workflow Start** pairs with **Local Activities** for low latency end to end.
- **Fairness**, **Priority** and **Downstream Rate Limiting** are discussed
  together for multi-tenant and tiered workloads.
- **Approval** and **Delayed Callback** both rely on Signals and durable waits.
  An Approval with an expiry uses a durable timer; if approvers can extend it,
  add **Updatable Timer**. Use an Update with a validator to reject late
  decisions.
- **Event Accumulator** builds on Signals and pairs with **Continue-As-New** to
  keep a long-lived accumulator's history bounded.
- **Entity Workflow** pairs with **Continue-As-New** and with Worker Versioning.

When a solution stacks patterns, fetch each page rather than improvising the
seams.

## Limits that change which pattern you pick

Temporal Cloud limits per Workflow Execution (self-hosted defaults are
configurable). Check `https://docs.temporal.io/evaluate/cloud/limits` before you
quote a number.

- 2,000 incomplete Activities, Child Workflows, Signals sent or external
  cancellations; aim for 500 or fewer. Above that, use Sliding Window or Batch
  Iterator.
- 10,000 Signals received per execution; for sustained traffic, aim for five or
  fewer Signals per second. Above that, batch events into each Signal or spread
  them across more Workflows.
- 10 in-flight Updates and 2,000 total Updates in history.
- Event History: 51,200 Events or 50 MB. Continue-As-New well before that.
- 2 MB per request payload. Larger data goes to External Storage or a reference.

## Anti-patterns

When a request matches one of these, say so and give the alternative. Detail,
warning signs and limits for each are in `references/anti-patterns.md`.

| Don't | Do instead |
|---|---|
| Use a Workflow as a high-rate datastore or per-record state store | Keep the state in a database; use Workflows for the bounded processes that act on it |
| Route all traffic through one hot Workflow (global counter, router, semaphore) | Shard by key, or keep the counter in a database. To protect a downstream service, use a Task Queue rate limit or cap Worker slots on a dedicated Task Queue. For a lock on one named resource, use one Workflow ID per resource |
| Start a Workflow per event for one retried call at high volume | Use a Standalone Activity |
| Fan out thousands of Child Workflows from one parent | Use Sliding Window, Batch Iterator or MapReduce Tree |
| Put I/O, randomness or clock reads in Workflow code | Use Activities; see `temporal-developer` for determinism |
| Pass large payloads as arguments or results | Use External Storage or pass a reference |
| Poll in a tight loop in Workflow code | Use the Polling External Services pattern |

**When Temporal isn't the fit:** sub-millisecond hot paths, in-memory stream
processing and high-rate key-value state belong in other systems. Temporal
orchestrates the durable processes around them. Say so when that's the answer.

## Use-case stacks

When the user frames the problem by what they're building, read
`references/use-cases.md`. It maps 16 verticals to the patterns and features each
usually needs: AI agents, AI agent platforms, AI processing pipelines, AI model
training, order management and fulfillment, payment processing and settlement,
booking and reservations, data pipelines and ETL, infrastructure automation and
CI/CD, customer onboarding and identity, entity lifecycle management,
communications and marketing, financial services and lending, control plane
operations, inventory and logistics, customer service and support. A stack is a
starting menu, not a mandate: fetch only the pages you select.

## Cross-cutting techniques (not catalog patterns)

- **Idempotency.** Activities run at least once. Setting maximum attempts to 1
  gives at most once, not exactly once. Get effectively-once side effects with an
  idempotency key (a business key, or Workflow ID plus Activity ID) that the
  downstream system enforces. It underpins Saga, payments and any at-least-once
  path. There is no `idempotency` pattern page; use `temporal-developer` for SDK
  guidance.

## Docs guides

End-to-end docs guides deepen several patterns (lock and semaphore, rate limiting
with 429 handling, approvals, Entity Workflow, Worker affinity, job queues). The
list, with the pattern each one extends, is in `references/guides.md`.

## Boundaries with other tools

- **`temporal-developer` skill:** the SDK and build skill. This skill picks the
  pattern; that one covers setup, determinism, gotchas and testing. Useful
  references there: `core/patterns.md` (primitives), `core/priority-fairness.md`,
  `core/ai-patterns.md` (AI agents), `core/job-queue.md` and
  `core/standalone-activities.md` (job queues), `core/versioning.md` (Worker
  Versioning, upgrade on Continue-As-New), and the per-language
  `workflow-streams.md` and `external-storage.md`.
- **Temporal Docs search (Kapa MCP, or
  `https://docs.temporal.io/api/retrieve?q=...`):** free-text search over the
  docs. Use it after you pick a pattern, not to choose one.

## Guardrails

- Don't invent pattern names. If nothing fits, check the features table and the
  anti-patterns, then solve from first principles with `temporal-developer`.
- Don't write pattern code or state SDK support or limits from memory. Fetch the
  page.
- Treat the catalog and stage labels as a dated snapshot. Fetch the index if a
  pattern seems missing, and check a stage on its page before you quote it.
- When a pattern page and a feature page disagree (for example, on changing
  Priority for queued work), cite both and follow the feature page.
- Don't over-engineer. A single Activity or a plain sequence is often the right
  answer. Name a pattern when it earns its place.
