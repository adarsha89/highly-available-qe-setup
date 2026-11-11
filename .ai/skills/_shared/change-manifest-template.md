# Change Manifest Template

Shared format for every "list of code changes" document. It is produced by `make-code-changes` (`docs/changes/<slug>-changes.md`) or scaffolding skills, and consumed by `review-code-changes` and `check-code-quality`.

The manifest provides a structured roadmap for reviewers and automated auditors. Reviewers read the actual code files and diff. Keep per-file notes factual, precise, and traceable.

Copy everything below the horizontal rule.

---

# Change Manifest: <title>

| Field | Value |
|---|---|
| Slug | `<slug>` |
| Produced by | `<skill name>` |
| Source plan | `<path to plan md>` |
| Requirements | `<path to requirements md, or "n/a">` |
| Base commit | `<git rev-parse HEAD before changes>` |
| Branch | `<branch name>` |
| Date | `<YYYY-MM-DD>` |
| Review cycle | `<0 for first implementation; n when reworking review cycle n>` |

## Summary

<3–6 sentences: what platform capability, infrastructure module, helm chart, or HA pipeline now exists that did not before.>

## Files Changed

| # | Path | Change | Layer | Purpose | Plan Ref |
|---|---|---|---|---|---|
| 1 | `terraform/modules/kubernetes/main.tf` | Modified | terraform | Add HA control-plane configuration | §4.1 |
| 2 | `kubernetes/helm/jenkins-ha/values.yaml` | Added | helm | HA Jenkins Helm values with PDB and JCasC | §4.2 |
| 3 | `jenkins/casc/jenkins.yaml` | Modified | jenkins-casc | Configure dynamic K8s cloud agent pod templates | §5.1 |
| 4 | `monitoring/prometheus/alert-rules.yaml` | Added | monitoring | Add Jenkins and K8s node failure alerts | §6.2 |

*Change* = `Added` | `Modified` | `Deleted` | `Renamed (from …)`
*Layer* = `terraform` · `helm` · `kubernetes` · `jenkins-casc` · `jenkins-pipeline` · `argocd` · `tracker` · `monitoring` · `backup` · `emulator` · `test` · `ci` · `docs`

## Per-File Details

### 1. `<path>`
- **What**: <Resources, charts, variables, manifests, or pipeline stages added/modified>
- **Why**: <Requirement / Plan item it satisfies>
- **Notes**: <High availability considerations, failover impact, zero-downtime compliance, security considerations>

(repeat per file)

## Verification & Test Coverage

| Test Script / Command | Target Layer | Expected Result | Requirement / Plan ID |
|---|---|---|---|
| `terraform validate` | terraform | Clean configuration | FR-1 |
| `helm lint kubernetes/helm/jenkins-ha` | helm | 0 errors | FR-2 |
| `pytest tests/kubernetes-ha/` | test | HA failover passes | NFR-1 |

## Deviations from Plan

- None / <Describe any architectural or implementation deviation and reason>
