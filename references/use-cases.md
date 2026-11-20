# Use-case stacks

Use this file when the user frames the problem by what they're building (an
industry or a use case) rather than by a symptom. Each vertical names the
patterns that use case usually needs. Names and descriptions are in the catalog
in `SKILL.md`; fetch a pattern's page as usual.

A stack is a starting menu, not a mandate. Most problems need a subset. Pick what
the customer's stated facts call for, and fetch only the pages you select.

How to read each entry:

- **Patterns:** the canonical stack from Temporal's "Use Case to Pattern
  Mapping" v3 (2026-07-08), reconciled to catalog slugs.
- **Also consider:** patterns this skill adds beyond that mapping.
- **Features:** platform features from the features table in `SKILL.md` that
  often pair with the stack. They are not patterns.
- **Watch for:** the trap most often hit in that use case.

## AI workloads

### AI agents
- **Patterns:** `entity-workflow`, `continue-as-new`, `request-response-via-updates`, `child-workflows`, `long-running-activity`, `pick-first`, `fast-slow-retries`
- **Also consider:** `approval` for tool calls that need a human OK.
- **Features:** Workflow Streams (stream tokens or progress), External Storage (large context), Worker Versioning (long-lived agents).
- **Watch for:** the agent loop is a Workflow and each LLM or tool call is an Activity. Use Entity Workflow only for a long-lived agent per user with low message rates; Continue-As-New keeps long conversations bounded.

### AI agent platforms
- **Use when:** you run agents for other teams or tenants (shared model APIs, tenant isolation). For the agent loop itself (LLM and tool calls, approvals, streaming), use "AI agents" above; most platform questions need both.
- **Patterns:** `signal-with-start`, `worker-specific-taskqueue`, `activity-dependency-injection`, `downstream-rate-limiting`, `fairness`, `priority-task-queues`, `delayed-retry`
- **Features:** Nexus (platform APIs called by other teams), Worker Versioning.
- **Watch for:** a shared model API needs a rate cap (Downstream Rate Limiting) and per-tenant sharing (Fairness); they solve different problems.

### AI processing pipelines
- **Patterns:** `parallel-execution`, `child-workflows`, `continue-as-new`, `downstream-rate-limiting`, `fast-slow-retries`, `sliding-window`, `mapreduce-tree`, `fixed-count-retries`, `delayed-retry`, `priority-task-queues`, `fairness`
- **Features:** External Storage (documents and embeddings over the payload limit).

### AI model training
- **Patterns:** `child-workflows`, `parallel-execution`, `long-running-activity`, `downstream-rate-limiting`, `retry-metrics`, `fixed-count-retries`, `sliding-window`
- **Also consider:** `worker-specific-taskqueue` to route steps to GPU hosts.

## Commerce & payments

### Order management & fulfillment
- **Patterns:** `entity-workflow`, `saga-pattern`, `signal-with-start`, `updatable-timer`, `delayed-callback`, `early-return`, `event-accumulator`
- **Features:** Update-with-Start (create the order and confirm in one call), Worker Versioning.

### Payment processing & settlement
- **Patterns:** `saga-pattern`, `non-retryable-errors`, `fixed-wall-time-retries`, `retry-metrics`, `early-return`, `delayed-retry`
- **Also consider:** `approval` for manual review of flagged payments.
- **Features:** Workflow ID conflict and reuse policies (one Workflow per payment key).
- **Watch for:** Activities run at least once. Use idempotency keys that the payment provider enforces; see Cross-cutting techniques in `SKILL.md`.

### Booking & reservations
Added by this skill; not in the v3 mapping.
- **Patterns:** `saga-pattern`, `early-return`, `updatable-timer`, `entity-workflow`, `non-retryable-errors`
- **Features:** Update-with-Start (hold and confirm in one call).
- **Watch for:** a hold that expires is a durable timer; add Updatable Timer only if the deadline can move; releasing held inventory on failure is a Saga compensation.

## Data & infrastructure

### Data pipelines & ETL
- **Patterns:** `parallel-execution`, `child-workflows`, `continue-as-new`, `polling`, `fixed-wall-time-retries`, `batch-iterator`, `sliding-window`, `fanout-child-workflows`, `mapreduce-tree`, `delayed-retry`
- **Also consider:** `downstream-rate-limiting` for source or sink APIs with request limits.
- **Features:** Schedules (nightly or calendar triggers), External Storage.
- **Watch for:** the pending Child Workflow limit when one parent fans out; see Limits in `SKILL.md`.

### Infrastructure automation & CI/CD
- **Patterns:** `saga-pattern`, `approval`, `delayed-start`, `polling`, `resumable-activity`, `fixed-count-retries`, `retry-metrics`
- **Features:** Activity Pause (hold retries during an outage), Schedules.

## Identity & lifecycle

### Customer onboarding & identity
- **Patterns:** `saga-pattern`, `approval`, `polling`, `updatable-timer`, `delayed-callback`, `early-return`, `fast-slow-retries`, `non-retryable-errors`

### Entity lifecycle management
- **Patterns:** `entity-workflow`, `continue-as-new`, `updatable-timer`, `signal-with-start`, `request-response-via-updates`, `delayed-callback`
- **Features:** Worker Versioning (entities outlive deploys), Search Attributes (find entities by state).
- **Watch for:** one Workflow per entity fits low message rates. For high-rate reads or compare-and-swap on entity state, keep the state in a database and use Workflows for the processes that act on it. See `references/anti-patterns.md`.

## Comms & fintech

### Communications & marketing
- **Patterns:** `child-workflows`, `parallel-execution`, `updatable-timer`, `downstream-rate-limiting`, `non-retryable-errors`, `delayed-callback`, `delayed-retry`, `sliding-window`, `batch-iterator`
- **Features:** Schedules (recurring campaigns).

### Financial services & lending
- **Patterns:** `saga-pattern`, `approval`, `entity-workflow`, `fixed-wall-time-retries`, `retry-metrics`, `pick-first`, `priority-task-queues`, `non-retryable-errors`
- **Features:** Worker Versioning (applications that wait days for decisions).

## Platform & ops

### Control plane operations
- **Patterns:** `entity-workflow`, `signal-with-start`, `worker-specific-taskqueue`, `downstream-rate-limiting`, `fairness`, `priority-task-queues`, `resumable-activity`
- **Features:** Nexus (operations exposed to other teams), Worker Versioning.
- **Watch for:** a Workflow per managed resource fits low rates of change. Don't make it the store that other services read at high rates; see `references/anti-patterns.md`.

### Inventory & logistics
- **Patterns:** `entity-workflow`, `saga-pattern`, `polling`, `updatable-timer`, `delayed-callback`, `event-accumulator`, `fast-slow-retries`

### Customer service & support
- **Patterns:** `entity-workflow`, `approval`, `updatable-timer`, `signal-with-start`, `request-response-via-updates`, `event-accumulator`, `delayed-callback`
