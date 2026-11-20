# Anti-patterns

Use this file when a request matches a row in the Anti-patterns table in
`SKILL.md`, or when a design review shows one of the warning signs below. For
each one: what it looks like, why it breaks, and what to do instead.

Limits quoted here are Temporal Cloud limits per Workflow Execution; self-hosted
defaults are configurable. Check `https://docs.temporal.io/evaluate/cloud/limits`
before you quote a number.

## A Workflow as a high-rate datastore or per-record state store

- **Warning signs:** other services read or write an entity's state through
  Queries, Signals or Updates many times per second; the Workflow is the only
  copy of a record that needs compare-and-swap; "we'll keep every account's
  balance in its Entity Workflow and query it on each request".
- **Why it breaks:** each Workflow Execution processes its messages one at a
  time. The docs recommend five or fewer Signals per second sustained, allow 10
  in-flight Updates, and cap history at 51,200 Events or 50 MB. Under load you see
  `BUSY_WORKFLOW` errors, rising latency and constant Continue-As-New.
- **Do instead:** keep high-rate state in a database built for it. Use Workflows
  for the bounded, durable processes that act on that state (an onboarding, a
  dispute, a migration). Entity Workflow fits when messages per entity are low.
- **Related:** `entity-workflow`, `continue-as-new`.

## One hot Workflow for global state

- **Warning signs:** a single Workflow acts as a global counter, router, queue or
  semaphore for all traffic.
- **Why it breaks:** one execution is one lock. Every request queues behind the
  others and hits the same per-execution limits as above.
- **Do instead:** shard by key (one Workflow per tenant or resource), or keep the
  counter in a database. For locks, use one Workflow ID per resource; see the
  guide at `https://docs.temporal.io/guides/lock-shared-resources`.

## A Workflow per event for one retried call

- **Warning signs:** every inbound event starts a Workflow that only calls one
  Activity with retries; volumes in the thousands per second.
- **Why it breaks:** a Workflow adds history and Workflow Tasks with no
  orchestration to justify them.
- **Do instead:** use a Standalone Activity, Temporal's job queue for one durable,
  retried unit of work (`https://docs.temporal.io/standalone-activity`). Move to a
  Workflow when steps depend on each other, wait, or need compensation.

## Fanning out thousands of Child Workflows from one parent

- **Warning signs:** a loop starts one Child Workflow per record for 10,000 or more
  records from a single parent.
- **Why it breaks:** an execution can have at most 2,000 incomplete Child
  Workflows (the docs advise 500 or fewer), and each start adds history.
- **Do instead:** Sliding Window to bound concurrency, Batch Iterator to page, or
  MapReduce Tree to split recursively.
- **Related:** `sliding-window`, `batch-iterator`, `mapreduce-tree`,
  `fanout-child-workflows`.

## I/O, randomness or clock reads in Workflow code

- **Warning signs:** HTTP calls, database queries, `random()` or the system clock
  inside a Workflow function.
- **Why it breaks:** Workflow code replays, so it must be deterministic. These
  calls cause non-determinism errors or double side effects.
- **Do instead:** put I/O in Activities and use the SDK's deterministic time and
  random APIs. The `temporal-developer` skill covers the rules per SDK.

## Large payloads as arguments or results

- **Warning signs:** files, documents, embeddings or large JSON passed between
  Workflows and Activities.
- **Why it breaks:** each request is limited to 2 MB, and history is limited to
  50 MB.
- **Do instead:** use External Storage (Public Preview,
  `https://docs.temporal.io/external-storage`) or store the data elsewhere and
  pass a reference.

## A tight polling loop in Workflow code

- **Warning signs:** a Workflow loops on "call Activity, sleep a few seconds"
  thousands of times.
- **Why it breaks:** each iteration adds Events to history.
- **Do instead:** the Polling External Services pattern (`polling`): poll inside
  an Activity with heartbeats, or use retries with a backoff for infrequent
  polling.

## When Temporal isn't the fit

Sub-millisecond hot paths, in-memory stream processing and high-rate key-value
state belong in systems built for them. Temporal orchestrates the durable
processes around them: the retries, waits, approvals and compensations. Say so
when that's the answer rather than forcing a pattern.
