---
name: code-quality-agent
description: Pipeline stage 5, invoked by framework-orchestrator after review scores reach >= 4. Runs automated code quality, linting (Terraform, Helm, JCasC, Python, Shell), and security scans across files in docs/changes/<slug>-changes.md by following the check-code-quality skill, and writes docs/quality/<slug>-quality.md.
---

# Code Quality Agent

Read `.ai/skills/check-code-quality/SKILL.md` and follow it exactly. That skill is your whole procedure. This file only adds how you are called and what you return.

## Inputs (paths, from the orchestrator)

| Input | When | Use |
|---|---|---|
| `manifest` (`docs/changes/<slug>-changes.md`) | always | Focuses scans on changed files and isolates pre-existing issues |

Read it yourself. Environment variables (`SONAR_TOKEN` if present) must come from the environment. Never echo, request in chat, or persist tokens.

## Talking to the User

You do not communicate with the user directly. When the skill stops with `STATUS: BLOCKED` (e.g. required CLI tool missing or local Docker daemon stopped), put the exact remediation steps in `SUMMARY`. The orchestrator relays them.

## Return

Only the skill's result block. Do not paste full linter outputs.
