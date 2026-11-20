# Mode tasks

Three tasks, one per mode the skill claims. Run each twice with `claude -p`: run A
prepends `Use the temporal-patterns skill.`; run B, the baseline, passes
`--disallowedTools Skill`. Grade both on the key under each task.

## T1 · Code review (Mode 1)

Prompt (send verbatim, including the code block):

````
Review this Workflow and fix it.

```python
import asyncio
from datetime import timedelta
from temporalio import workflow
from temporalio.exceptions import ActivityError

with workflow.unsafe.imports_passed_through():
    from activities import reserve_inventory, charge_card, ship_order, \
        release_inventory, refund_card, send_digest


@workflow.defn
class OrderFeedWorkflow:
    def __init__(self) -> None:
        self.events: list[dict] = []

    @workflow.signal
    def new_order(self, order: dict) -> None:
        self.events.append(order)

    @workflow.run
    async def run(self, customer_id: str) -> None:
        # Runs forever: one workflow per customer, processes every order they place
        while True:
            await workflow.wait_condition(lambda: len(self.events) > 0)
            order = self.events[-1]

            # hand-rolled retry for the flaky payment provider
            attempt = 0
            while True:
                try:
                    reservation = await workflow.execute_activity(
                        reserve_inventory, order,
                        start_to_close_timeout=timedelta(seconds=30))
                    try:
                        charge = await workflow.execute_activity(
                            charge_card, order,
                            start_to_close_timeout=timedelta(seconds=30))
                        try:
                            await workflow.execute_activity(
                                ship_order, order,
                                start_to_close_timeout=timedelta(seconds=30))
                        except ActivityError:
                            await workflow.execute_activity(
                                refund_card, charge,
                                start_to_close_timeout=timedelta(seconds=30))
                            raise
                    except ActivityError:
                        await workflow.execute_activity(
                            release_inventory, reservation,
                            start_to_close_timeout=timedelta(seconds=30))
                        raise
                    break
                except ActivityError:
                    attempt += 1
                    if attempt > 5:
                        break
                    await asyncio.sleep(2 ** attempt)

            # daily digest of everything so far
            if len(self.events) % 50 == 0:
                await workflow.execute_activity(
                    send_digest, self.events,
                    start_to_close_timeout=timedelta(minutes=5))
```
````

Planted defects (grading key):
1. Infinite loop with an ever-growing `self.events` list and no Continue-As-New (history and payload growth). Pattern: Continue-As-New / Entity Workflow.
2. Processes `self.events[-1]` and never removes it, so the loop re-processes the same order forever (busy loop); bursts of signals drop orders. Should drain a queue.
3. Compensation via nested try/except: refund then release happen inside nested blocks, so a ship failure refunds and releases (OK) but the outer retry then re-reserves and re-charges; compensations themselves not protected; no compensation list. Pattern: Saga.
4. Hand-coded retry loop in the Workflow around activities that already have a default retry policy (unlimited retries), so the loop rarely triggers and, when it does, double-retries; `2 ** attempt` sleep is a durable timer but the logic belongs in a RetryPolicy. Patterns: retry family (Fixed Count of Retries, Non-Retryable Errors for card declines).
5. Card decline would retry forever (default policy) and charge retries risk double-charge without an idempotency key.
6. `send_digest` passes the whole growing list as an activity input (payload size limit, 2 MB per payload); "daily" digest is actually every 50 events.
7. Bonus: Entity Workflow per customer started by signal implies Signal-with-Start on the client; Update could return per-order status.

## T2 · Customer Q&A (Mode 2)

```
A prospect asks: we process loan applications that wait days for underwriter decisions and call 6 external services, some flaky, some rate limited. How would you structure this in Temporal? Draft my answer, 200 words.
```

Grading key: one Workflow per application; underwriter decision via Signal or Update with a durable wait (Approval pattern), optional timeout/escalation timer; 6 services as Activities with per-service RetryPolicy (flaky); rate limits via a dedicated Task Queue with `max_task_queue_activities_per_second` (Downstream Rate Limiting) or worker-side limits; Non-Retryable Errors for hard rejects; optional Saga only if steps need undoing; Parallel Execution for independent checks. About 200 words. No pricing.

## T3 · Slides (Mode 3)

```
Outline 5 slides introducing Temporal design patterns to a platform team building an internal AI agent platform. Exact pattern names, one line each, plus a link per pattern.
```

Grading key: exact names and slugs matching https://docs.temporal.io/design-patterns.md; links resolve (`https://docs.temporal.io/design-patterns/{slug}`); fit for an internal agent platform (multi-tenant: Fairness, Priority Task Queues, Downstream Rate Limiting; agent sessions: Entity Workflow, Continue-As-New, Request-Response via Updates, Signal with Start; tools: Long-Running Activity, Activity Dependency Injection, Worker-Specific Task Queues); current features where relevant (Update-with-Start, Priority and Fairness, Worker Versioning, Nexus); no invented pattern names.
