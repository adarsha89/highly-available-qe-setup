---
name: analyze-task
description: Turn a raw platform change request (ticket link, user prompt, architectural note) into an explicit, testable requirements document for this Highly Available QE Platform (covering Helm, Terraform, ArgoCD, JCasC, Kubernetes HA, LocalStack, and Monitoring). Focuses on what capability must exist and why, without jumping to implementation details. First step before plan-framework-code-changes.
---

# analyze-task

## Purpose

Produce `docs/requirements/<slug>-requirements.md`: an unambiguous statement of **what** platform capability must change or be added and **why**. The next skill (`plan-framework-code-changes`) decides **how**.

Focus on high availability, zero-downtime, fault tolerance, multi-cloud compatibility (AWS, Azure, and local Docker/Kind), GitOps reconciliation, and testability.

## Inputs

| Input | Required | Notes |
|---|---|---|
| Task description | yes | Free text, ticket link, issue description, or file path (`.md`, `.txt`) |
| Supporting docs | no | Architecture notes, `requirements.txt`, downstream consumer requirements |
| Slug | no | Short kebab-case slug derived from the task and confirmed with user |

If a link or file is inaccessible, inform the user and request the relevant text. Never guess unverified requirements.

## Procedure

1. **Load Context**
   - `.ai/skills/_shared/framework-guidelines.md`
   - `requirements.txt` and root `README.md`
   - Survey the existing directory structure (`terraform/`, `kubernetes/`, `jenkins/`, `cloud-emulators/`, `monitoring/`, `backup-recovery/`, `tests/`) to understand existing coverage.
2. **Extract Requirements**
   - Identify the engineering goal, impacted platform layers (Terraform modules, Helm charts, ArgoCD apps, Jenkins JCasC, monitoring/alerting, emulator hooks, test suites).
   - Identify targets: Local (Docker/Kind/LocalStack), AWS, or Microsoft Azure.
   - Note constraints: High availability requirements, recovery time/point objectives (RTO/RPO), statefulness, zero-downtime updates, backward compatibility for downstream `qe-base` consumers.
3. **Clarify Ambiguities**
   - List any missing details (e.g., failover thresholds, target cloud emulator support, scaling parameters).
   - Batch questions to the user in a single structured message with suggested defaults.
   - If instructed to use best judgement, record the decision under *Assumptions* marked `ASSUMED`.
4. **Draft Requirements Specification**
   - Ensure every functional requirement is verifiable through automated tests or linter checks (`terraform validate`, `helm lint`, `yamllint`, LocalStack integration tests, Kubernetes HA failover tests).
   - Number items uniquely (`FR-1`, `NFR-1`, `AC-1.1`).
   - Distinguish strictly between In-Scope and Out-of-Scope.
5. **Self-Audit & Emit Result**
   - Verify every Acceptance Criteria traces to a Functional Requirement.
   - Write `docs/requirements/<slug>-requirements.md` and print the standard Result block.

## Output Template: `docs/requirements/<slug>-requirements.md`

```markdown
# Requirements: <title>

| Field | Value |
|---|---|
| Slug | `<slug>` |
| Source | <ticket link / file / prompt> |
| Author | analyze-task |
| Status | Draft / Final |

## 1. Goal
<2–4 sentences: what HA platform capability, infrastructure module, or automation pipeline is being added or improved, and for what purpose.>

## 2. Background & Architecture Context
<What currently exists in the repo, target environments affected (Local, AWS, Azure), and relevant dependencies.>

## 3. Scope
### In Scope
- …
### Out of Scope
- … (with brief justification)

## 4. Platform Layers Affected
| Layer | Target Path(s) | Environments (Local / AWS / Azure) | Notes |
|---|---|---|---|
| Terraform | `terraform/modules/...` | | |
| Kubernetes / Helm | `kubernetes/helm/...` | | |
| ArgoCD | `kubernetes/argocd/...` | | |
| Jenkins / JCasC | `jenkins/casc/...` | | |
| Monitoring / Alerting | `monitoring/...` | | |
| Cloud Emulators | `cloud-emulators/...` | | |
| Tests | `tests/...` | | |

## 5. Functional Requirements
### FR-1: <Capability Name>
<Clear behavioral requirement.>
**Acceptance Criteria**
- AC-1.1: Given <initial platform state>, when <action/event occurs>, then <observable, verifiable result>.
- AC-1.2: …

## 6. High Availability & Resilience Requirements
### FR-HA-1: <Failover / Redundancy Requirement>
- AC-HA-1.1: Given a disruption of <component>, the platform must automatically recover within <seconds/minutes> with zero persistent state loss.

## 7. Non-Functional Requirements
- NFR-1 Resilience & HA: Kubernetes workloads must declare PDBs, health probes, and replica counts >= 2 (or multi-control plane).
- NFR-2 Emulation Fidelity: Changes must be verifiable against LocalStack / LocalStack-Azure without requiring paid cloud resources.
- NFR-3 Security & Secrets: Zero secrets committed to source control; use environment variables or secret managers.
- NFR-4 Idempotency: All Terraform scripts and Helm releases must be cleanly re-entrant and idempotent.
- NFR-5 Observability: All critical failures (cluster down, Jenkins down, pod crashloops) must trigger alerts in Alertmanager.

## 8. Open Questions & Assumptions
- [ASSUMED] …
```
