---
name: mutation-testing
description: Plan, execute, and analyze controlled failure injections, chaos scenarios, and mutation tests against this platform's High Availability components (Kubernetes multi-node failover, Jenkins controller crash recovery, JCasC state rebuilding, LocalStack outages, and Alertmanager notification paths) to prove self-healing and alert triggers.
---

# Mutation & Resilience Testing

## Purpose

Validate whether the platform's High Availability guarantees, self-healing mechanisms, and alerting rules actually work under real failure conditions. Instead of assuming redundancy works on paper, this skill injects controlled faults ("mutations") into running infrastructure and tests the platform's automated recovery and alerting responses.

## Target Components for Fault Injection

1. **Kubernetes Multi-Node Cluster (`kubernetes-ha`)**:
   - Simulated control plane node termination.
   - Worker node drain/cordon under active workload.
   - Verification: Zero downtime for replicated services, traffic routed to surviving pods.
2. **Jenkins Server (`failover`)**:
   - Abrupt kill of Jenkins controller pod.
   - Verification: Immediate rescheduling, JCasC config reload, volume reattachment, job continuity.
3. **Alerting System (`monitoring`)**:
   - Simulated metric disruption (e.g., node unreachable, Jenkins health endpoint 500).
   - Verification: Alertmanager receives firing event and triggers simulated notification within SLA (< 60s).
4. **Cloud Emulation / LocalStack (`aws-integration`, `azure-integration`)**:
   - Injected network latency or transient service errors.
   - Verification: Terraform and services retry gracefully with exponential backoff.
5. **Disaster Recovery (`disaster-recovery`)**:
   - Simulated catastrophic state loss and trigger of `backup-recovery/scripts/restore.sh`.
   - Verification: Complete recovery to last known good state within target RTO.

## Procedure

1. **Baseline Verification**:
   Ensure the target cluster or emulator is healthy:
   ```bash
   kubectl get nodes
   kubectl get pods -A
   ```
2. **Select Mutation / Fault Scenario**:
   Consult `.ai/skills/mutation-testing/references/mutation-catalog.md` to select or define a fault scenario.
3. **Execute Mutation**:
   Trigger the fault via test scripts under `tests/failover/` or `tests/kubernetes-ha/`:
   ```bash
   pytest tests/failover/ -k "test_jenkins_pod_failure_recovery"
   ```
4. **Observe Recovery & Alerting**:
   - Measure Recovery Time Objective (RTO).
   - Check Alertmanager active alerts: `curl -s http://localhost:9093/api/v2/alerts`.
5. **Compile Mutation Report**:
   Write `docs/mutation/<slug>-mutation-report.md`.

## Output Template: `docs/mutation/<slug>-mutation-report.md`

```markdown
# Resilience & Mutation Testing Report: <title>

| Field | Value |
|---|---|
| Slug | `<slug>` |
| Target System | Kubernetes / Jenkins / LocalStack / Alertmanager |
| Overall Score | PASSED / FAILED |
| Date | `<YYYY-MM-DD>` |

## 1. Scenario Summary
<Description of injected fault and expected recovery behavior.>

## 2. Injection Matrix & Outcomes

| Scenario ID | Injected Fault | Expected Recovery | Observed RTO | Alert Triggered? | Result |
|---|---|---|---|---|---|
| MUT-K8S-01 | Kill worker node | Pods migrate via PDB | 22s | NodeNotReady (Firing) | PASSED |
| MUT-JNK-01 | Kill Jenkins pod | Rescheduled + JCasC intact | 38s | JenkinsDown (Resolved) | PASSED |
| MUT-DR-01 | Data loss simulation | Restore from backup | 95s | DRAlert (Resolved) | PASSED |

## 3. Findings & Gaps
- <Any assertion failure, slow recovery, or missed alert>
```
