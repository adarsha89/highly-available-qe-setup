---
name: make-code-changes
description: Implement planned platform and infrastructure code changes (Terraform, Helm charts, ArgoCD manifests, Jenkins JCasC, Kubernetes configurations, LocalStack emulators, monitoring rules, and tests) described in an approved plan markdown. Validates all syntax and linters, verifies baseline compatibility, and writes a structured change manifest for review. Also handles rework from review reports.
---

# make-code-changes

## Purpose

Turn an approved implementation plan (`docs/plans/<slug>-plan.md`) into working, tested code, and produce `docs/changes/<slug>-changes.md` for `review-code-changes`.

## Inputs

| Input | Required | Notes |
|---|---|---|
| Plan path | yes | Default: `docs/plans/<slug>-plan.md` |
| Review / Quality report path | no | `docs/reviews/<slug>-review-cycle-<n>.md` (puts skill in **rework mode**) |

If the plan does not indicate `Status: Approved`, stop and request confirmation or approval from the user before proceeding.

## Ground Rules

- **Follow the Plan**: Implement exactly what is specified. Do not refactor unrelated code or add extraneous features.
- **Safety & Zero Secrets**: Never hardcode credentials, private tokens, or sensitive certificates. Use environment variables, Kubernetes Secrets, or LocalStack dummy variables (`AWS_ACCESS_KEY_ID=test`).
- **High Availability Compliance**: Adhere strictly to `.ai/skills/_shared/framework-guidelines.md` (PDBs, health probes, multi-node considerations, non-root containers, persistent volume claims).
- **Idempotency**: All Terraform code and Helm charts must be idempotent and re-runnable without breaking state.
- **Rework Mode**: In cycle >= 2, address every specific defect and suggestion identified in the review report.

## Procedure

### 1. Load Context & Baseline
```bash
git rev-parse HEAD                 # record as Base commit
git status --porcelain             # note existing uncommitted changes; do not overwrite or claim them
```
- Read `.ai/skills/_shared/framework-guidelines.md`
- Read the approved plan and review report (if rework mode)
- Read all existing files targeted for modification before applying edits.

### 2. Implementation Order
Implement changes systematically:
1. **Underlying Infrastructure / Emulators**: `cloud-emulators/`, `terraform/modules/`, `terraform/aws/`, `terraform/azure/`
2. **Kubernetes Core & Policies**: `kubernetes/kind/`, `kubernetes/namespaces/`, `kubernetes/policies/`
3. **Application Packaging & GitOps**: `kubernetes/helm/`, `kubernetes/argocd/`
4. **CI/CD Automation**: `jenkins/casc/`, `jenkins/jobs/`, `jenkins/plugins/`, `jenkins/pipelines/`
5. **Services & Tracking**: `qe-central-tracking-application/`
6. **Observability & Recovery**: `monitoring/`, `backup-recovery/`
7. **Verification Suites**: `tests/`

### 3. Verify Mechanically
Run the appropriate verification commands based on the modified layers:

```bash
# Terraform validation
if compgen -G "terraform/**/*.tf" > /dev/null; then
  terraform fmt -check -recursive terraform/
fi

# Helm chart validation
if [ -d "kubernetes/helm" ]; then
  for chart in kubernetes/helm/*; do
    [ -d "$chart" ] && helm lint "$chart"
  done
fi

# YAML validation for Kubernetes, ArgoCD, and JCasC
if command -v yamllint >/dev/null 2>&1; then
  yamllint -d relaxed jenkins/casc/ kubernetes/argocd/ monitoring/
fi

# Run relevant tests if LocalStack / Docker environment is available
if [ -d "tests" ]; then
  pytest tests/ -m "not e2e_live" || true
fi
```

### 4. Create Change Manifest
Write `docs/changes/<slug>-changes.md` following `.ai/skills/_shared/change-manifest-template.md`.

### 5. Return Result Block
Finish with the standard result block (guidelines section 6).
