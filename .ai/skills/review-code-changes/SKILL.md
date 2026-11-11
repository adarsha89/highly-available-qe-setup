---
name: review-code-changes
description: Thoroughly review platform, infrastructure, and automation code changes against functional requirements, high availability guidelines, security standards, and idempotency. Evaluates changes listed in a change manifest, scores 10 distinct quality parameters from 1–5, and emits an evidence-based APPROVED or CHANGES_REQUESTED report.
---

# review-code-changes

## Purpose

Provide a rigorous, evidence-grounded review of all platform and infrastructure changes, producing `docs/reviews/<slug>-review-cycle-<n>.md` that `make-code-changes` can act on during rework cycles.

## Inputs

| Input | Required | Notes |
|---|---|---|
| Change manifest path | yes | Default: `docs/changes/<slug>-changes.md` |
| Review cycle number | no | Auto-calculated (1 + highest existing review cycle) |

The plan and requirements paths are parsed from the manifest header.

## Review Principles & Strict Evidence Mode

- **Zero Speculation**: Every defect or finding must cite the exact `path:line` and explain why the configuration or code will fail, breach HA principles, or compromise security.
- **High Availability Mandate**: Verify PodDisruptionBudgets, replica redundancy, liveness/readiness probes, persistent volume lifecycle, and failover behavior.
- **Security & Secret Hygiene**: Hardcoded credentials, plain-text API tokens, or unsafe permissions result in an immediate score of 1.
- **Idempotency**: Terraform resources, Helm charts, and JCasC files must apply cleanly multiple times without configuration drift.

## 10 Quality Parameters (Scored 1 to 5)

1. **Correctness**: Syntax, schema validity, parameter types, resource relationships.
2. **Requirements Coverage**: Full alignment with all FRs and ACs in the requirements document.
3. **High Availability & Fault Tolerance**: PDBs, health probes, multi-node scheduling, failover handling.
4. **Security & Secrets Hygiene**: Zero plain-text secrets, least privilege IAM/RBAC, non-root containers.
5. **Idempotency & Reconciliation**: Clean re-execution of Terraform, ArgoCD drift handling, JCasC reloading.
6. **Infrastructure & Chart Best Practices**: Modular Terraform, validated Helm templates, resource limits.
7. **Cloud Emulation Compatibility**: Flawless execution against LocalStack / LocalStack-Azure.
8. **CI/CD & JCasC Integration**: Dynamic agent scaling, clean pipeline syntax, deterministic Jenkins configuration.
9. **Observability & Alerting**: Metrics collection, dashboard coverage, and functional Alertmanager rules.
10. **Maintainability & Documentation**: Clean comments, directory compliance with `requirements.txt`, clear runbooks.

*Scoring Rule*: An overall verdict of `APPROVED` requires all 10 scores to be **>= 4**. Any score < 4 triggers `CHANGES_REQUESTED`.

## Procedure

1. **Load Context**: Manifest, plan, requirements, and `.ai/skills/_shared/framework-guidelines.md`.
2. **Verify Real Diff**:
   ```bash
   git diff --stat <base-commit>
   git diff <base-commit>
   git status --porcelain
   ```
3. **Read Every Changed File in Full**: Inspect both the changes and their downstream dependents.
4. **Execute Verification Tools**:
   ```bash
   terraform fmt -check -recursive terraform/ || true
   for chart in kubernetes/helm/*; do [ -d "$chart" ] && helm lint "$chart"; done || true
   yamllint -d relaxed jenkins/casc/ kubernetes/argocd/ || true
   ```
5. **Write Review Report**: Write `docs/reviews/<slug>-review-cycle-<n>.md` using the template below.
6. **Return Result Block**: Finish with the standard result block.

## Output Template: `docs/reviews/<slug>-review-cycle-<n>.md`

```markdown
# Code Review: <title> (Cycle <n>)

| Field | Value |
|---|---|
| Manifest | `<path>` |
| Plan | `<path>` |
| Requirements | `<path>` |
| Reviewer | review-code-changes |
| Verdict | APPROVED / CHANGES_REQUESTED |
| Date | `<YYYY-MM-DD>` |

## 1. Executive Summary
<2-4 sentences summarizing findings and verdict.>

## 2. Parameter Scores

| # | Parameter | Score (1-5) | Summary Finding |
|---|---|---|---|
| 1 | Correctness | <score> | |
| 2 | Requirements Coverage | <score> | |
| 3 | HA & Fault Tolerance | <score> | |
| 4 | Security & Secrets Hygiene | <score> | |
| 5 | Idempotency & Reconciliation | <score> | |
| 6 | Infrastructure & Helm Quality | <score> | |
| 7 | Cloud Emulation Compatibility | <score> | |
| 8 | CI/CD & JCasC Integration | <score> | |
| 9 | Observability & Alerting | <score> | |
| 10 | Maintainability & Documentation | <score> | |

**Overall Verdict**: APPROVED / CHANGES_REQUESTED (All scores >= 4 required for approval)

## 3. Findings & Required Changes
### Finding 1: `<file>:<line>`
- **Severity**: High / Medium / Low
- **Issue**: <Concrete description of the defect or missing HA standard>
- **Required Action**: <Exact fix needed>

## 4. Suggestions (Non-blocking)
- ...
```
