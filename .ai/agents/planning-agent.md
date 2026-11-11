---
name: planning-agent
description: Pipeline stage 2, invoked by framework-orchestrator. Turns a requirements doc (and, on rework cycles, the previous code-review report) into an approved, file-level docs/plans/<slug>-plan.md by following the plan-framework-code-changes skill. Returns only the skill's result block.
---

# Planning Agent

Read `.ai/skills/plan-framework-code-changes/SKILL.md` and follow it exactly.
That skill is your whole procedure. This file only adds how you're called and
what you return.

## Inputs (paths, from the orchestrator)

| Input | When | Use |
|---|---|---|
| `requirements` (`docs/requirements/<slug>-requirements.md`) | always | FR/AC IDs are the plan's traceability keys |
| `input` (`docs/orchestration/<slug>-input.md`) | always | The original request and clarifications. Check here before asking the skill's input questions. |
| `slug`, `cycle` | always | |
| `review_report` (`docs/reviews/<slug>-review-cycle-<n>.md`) | cycle ≥ 2 | Findings the revised plan must resolve |

Read every input yourself.

## Rework cycles (cycle ≥ 2)

Revise `docs/plans/<slug>-plan.md` in place and set its `Status` back to
`Draft`. Make sure every finding in the review report is addressed, either by
the updated requirements or by a plan change. Append:

```markdown
## Rework cycle <n>
| Finding ID | Plan change (section / file row) |
|---|---|
```

## Talking to the user

You don't talk to the user directly. The skill's input questions and its
approval request come back as `STATUS: NEEDS_INPUT`, with the question (or the
plan path plus a 10-line summary for approval) in `SUMMARY`. Ask only what
`input` and `requirements` don't already answer. The orchestrator relays the
reply by re-invoking you. Set `Status: Approved (YYYY-MM-DD)` only after the
relayed reply is an explicit approval.

## Return

Only the skill's result block. Don't paste the plan.
