# AI Agents: Highly Available QE Platform

Model- and tool-agnostic agent definitions for building, maintaining, and scaling this repository's Highly Available QE Platform (Helm charts, Terraform, ArgoCD, JCasC, Kubernetes HA, LocalStack, and Monitoring).

Each agent is defined as a markdown file with YAML front matter (`name`, `description`). No proprietary model or toolset is pinned, allowing agents to run in any compliant agent runtime (Antigravity CLI / agy, Claude Code, OpenAI Codex, etc.).

## Agent Pipeline Overview

| Agent | Role | Underlying Skill |
|---|---|---|
| [`framework-orchestrator`](framework-orchestrator.md) | Entry point. Orchestrates the rework loop, approval gates, durable memory, and summary. | n/a |
| [`task-analysis-agent`](task-analysis-agent.md) | Request (+ review report) → structured requirements | `analyze-task` |
| [`planning-agent`](planning-agent.md) | Requirements → approved architecture & file-level plan | `plan-framework-code-changes` |
| [`coding-agent`](coding-agent.md) | Approved plan (+ review report) → working code + change manifest | `make-code-changes` |
| [`code-review-agent`](code-review-agent.md) | Change manifest → strict 10-parameter review with scores | `review-code-changes` |
| [`code-quality-agent`](code-quality-agent.md) | Change manifest → multi-layer linting & static analysis report | `check-code-quality` |
| [`mutation-testing-agent`](mutation-testing-agent.md) | Plans, executes, and reports controlled resilience & fault-injection scenarios | `mutation-testing` |

### Standalone Agents

| Agent | Role | Underlying Skill |
|---|---|---|
| [`linkedin-post-agent`](linkedin-post-agent.md) | Repo analysis → evidence-backed technical LinkedIn learning post | `write-repo-learning-post` |

## Execution in Different Runtimes

### 1. Antigravity CLI (`agy`)
Run directly using the orchestrator:
```bash
agy
```

### 2. Claude Code (`claude`)
```bash
claude --agent framework-orchestrator
```

### 3. OpenAI Codex (`codex`)
```bash
codex "Run framework-orchestrator on <task>"
```
