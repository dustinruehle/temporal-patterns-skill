# Docs guides that extend patterns

End-to-end guides at `https://docs.temporal.io/guides/{name}` (append `.md` for
Markdown). Use them when a customer wants a worked example of a pattern. The
full list is at `https://docs.temporal.io/guides/llms.txt`.

| Guide name | What it builds | Extends |
|---|---|---|
| `lock-shared-resources` | A distributed lock and semaphore with Workflow IDs | No catalog pattern; the answer for lock and mutex questions |
| `rate-limit-downstream-apis` | Rate limiting with separate Task Queues, with 429 handling | `downstream-rate-limiting` |
| `recover-without-restart` | Pause a Workflow on failure and resume it after a fix | `resumable-activity` |
| `reliable-document-approvals` | A human-in-the-loop document approval | `approval` |
| `entity-pattern-loyalty-points` | A loyalty program with Entity Workflows | `entity-workflow` |
| `route-specialized-workloads` | Route GPU and high-memory Activities to dedicated Workers | `worker-specific-taskqueue` |
| `worker-execution-affinity` | Run all of a Workflow's Activities on the same Worker | `worker-specific-taskqueue` |
| `celery-to-standalone-activity` | Move a Celery task queue to Standalone Activities | Standalone Activities (feature) |

Multi-tenant design, with Fairness:
`https://docs.temporal.io/best-practices/multi-tenant-patterns`.
