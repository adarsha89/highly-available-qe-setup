# Platform Automation Pipeline

Platform and infrastructure changes in this repository (Terraform modules, Helm charts, ArgoCD application sets, Jenkins JCasC configurations, Kubernetes manifests, monitoring/alerting rules, backup policies, or cloud emulator setups) go through the agent pipeline defined in [`.ai/agents/`](../agents/README.md). Each stage agent executes exactly one skill from [`.ai/skills/`](../skills/README.md):

```
framework-orchestrator (Platform Orchestrator)
  → task-analysis-agent (analyze-task)
  → planning-agent (plan-framework-code-changes, user approves plan)
  → coding-agent (make-code-changes)
  → code-review-agent (review-code-changes)
      any of the 10 scores < 4 → back to task-analysis-agent with the review report
      (up to 5 cycles in total, then abort with docs/orchestration/<slug>-abort.md)
  → code-quality-agent (check-code-quality)
  → memory (project memory: AGENTS.md / CLAUDE.md) → final summary
```

The flow diagram and gate rules are documented in `.ai/agents/framework-orchestrator.md`. Scaffolding a brand-new platform component or environment (e.g., a new Terraform module, Helm chart, emulator environment, or Jenkins pipeline) follows `scaffold-qe-module` → `review-code-changes` → `check-code-quality`.

## Context Hygiene Rule

Every handoff between pipeline stages passes **file paths, never inlined document content**.

- Each stage loads its input documents directly from disk rather than receiving them pasted into its prompt.
- The orchestrator does not hold document full text in its context once written to disk. Only file paths and each stage's compact structured result block (`STATUS`, `OUTPUT`, `SUMMARY`, `NEXT`, plus any `SCORES`) persist between stages.
- When an agent needs information from an existing artifact, it re-reads it from disk on demand.
- Sub-agents never communicate with the user directly; they return `STATUS: NEEDS_INPUT` to the orchestrator, which collects user clarifications and appends them to the input document before resuming.

Apply this pattern across all agents in `.ai/agents/` and skills in `.ai/skills/`.
