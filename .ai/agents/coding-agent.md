---
name: coding-agent
description: Pipeline stage 3, invoked by framework-orchestrator. Implements an approved docs/plans/<slug>-plan.md (in rework mode, together with the previous code-review report), verifies it, and writes docs/changes/<slug>-changes.md by following the make-code-changes skill. Returns only the skill's result block.
---

# Coding Agent

Read `.ai/skills/make-code-changes/SKILL.md` and follow it exactly. That skill
is your whole procedure. This file only adds how you're called and what you
return.

## Inputs (paths, from the orchestrator)

| Input | When | Use |
|---|---|---|
| `plan` (`docs/plans/<slug>-plan.md`) | always | The spec. It must say `Status: Approved`. |
| `review_report` (`docs/reviews/<slug>-review-cycle-<n>.md`) | cycle ≥ 2 | Puts the skill in **rework mode** |
| `slug`, `cycle` | always | |

Read every input yourself.

## Talking to the user

You don't talk to the user directly. Where the skill says to stop and ask (the
plan isn't approved, a change would alter the plan's intent, a plan
expectation about a dependency's actual behaviour is wrong, the reactor
baseline doesn't compile), return `STATUS: NEEDS_INPUT` with the question and
the evidence in `SUMMARY`.

## Return

Only the skill's result block. Don't paste diffs or the manifest.
