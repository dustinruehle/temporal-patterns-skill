# Evals

Three eval sets guard the skill's quality across edits. Run them before a
release that changes routing text, the description or the catalog. Prompts are
generic: no company or customer names.

| File | What it tests | How to score |
|---|---|---|
| `routing.json` | 40 problem statements in five categories: direct, use-case, trap, no-pattern (the answer is a feature or "not Temporal"), anti-pattern | Follow the skill as written for each prompt. Score 0 to 2 on pattern, caveat and link. A caveat available only by fetching the page earns at most 1. |
| `triggers.json` | 30 prompts, `should_trigger` true or false, including near-misses (other workflow engines, Temporal ops questions that belong to other skills) | Run with skill-creator's `run_eval.py`, 3 runs per query. Count an invocation of any `temporal-patterns` copy as a trigger. Report precision and recall. |
| `modes.md` | One task per mode: code review, customer Q&A, slide outline | Run each with and without the skill; grade both on the key under each task. |

## Results

| Version | Routing (overall) | Trap | No-pattern | Anti-pattern | Triggering (P / R) | Modes (with vs without) |
|---|---|---|---|---|---|---|
| 0.2.2 | 61% | 46% | 20% | 37% | 1.00 / 1.00 | Code 9 vs 8.5; Q&A 7 vs 7.5; Slides 8.5 vs 4 |
| 0.3.0 | 96% | 96% | 87% | 97% | 1.00 / 1.00 (31 queries) | Code 9 vs 8; Q&A 8 vs 7; Slides 9 vs 4 |

Notes for 0.3.0: routing was scored by a fresh reviewer against the same key. The
trigger set adds one should-trigger prompt (safe Workflow deploys); six
near-miss probes that reuse the description's example phrases in non-Temporal
settings fired 0 of 18 runs. In the mode runs, the baseline was re-graded with
the same key as the new run.
