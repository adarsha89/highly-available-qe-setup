---
name: check-code-quality
description: Run automated code quality, linting, security, and static analysis scans across Terraform, Helm charts, Kubernetes manifests, Jenkins JCasC, Python services, and shell scripts. Emits a structured quality report summarizing issues, security vulnerabilities, and quality gate status.
---

# check-code-quality

## Purpose

Produce `docs/quality/<slug>-quality.md`: an objective quality and static-analysis signal for the platform codebase, focused on a specific change set or full repository audit.

## Inputs

| Input | Required | Notes |
|---|---|---|
| Change manifest path | no | Focuses the audit on changed files. Default: full repo scan (`full-scan-<YYYY-MM-DD>`) |
| `SONAR_TOKEN` | no | Environment variable for SonarQube if integrating with remote/local server |

## Quality Tools & Checks Run

1. **Terraform**:
   - `terraform fmt -check -recursive terraform/`
   - `tflint --recursive` (checks deprecated syntax, unused declarations, security gaps)
2. **Helm Charts**:
   - `helm lint kubernetes/helm/*`
3. **Kubernetes Manifests**:
   - `kubeconform -summary -strict` or `kubectl --dry-run=client`
4. **Configuration as Code & YAML**:
   - `yamllint jenkins/casc/ kubernetes/argocd/ monitoring/`
5. **Shell Scripts**:
   - `shellcheck backup-recovery/scripts/*.sh` (checks error handling, quoting, portability)
6. **Python Services & Tests** (`qe-central-tracking-application/`, `tests/`):
   - `ruff check .` or `flake8` / `black --check .`
7. **SonarQube (Optional)**:
   - If `SONAR_TOKEN` is present or SonarQube is running locally, execute scanner.

## Procedure

1. **Detect Installed Linters**:
   Check available CLI tools (`terraform`, `tflint`, `helm`, `yamllint`, `shellcheck`, `ruff`/`flake8`). Run all available checks.
2. **Execute Static Analysis & Security Scans**:
   Capture errors, warnings, formatting discrepancies, and potential security vulnerabilities.
3. **Write Quality Report**:
   Compile results into `docs/quality/<slug>-quality.md`.
4. **Emit Standard Result Block**.

## Output Template: `docs/quality/<slug>-quality.md`

```markdown
# Quality Signal: <title>

| Field | Value |
|---|---|
| Slug | `<slug>` |
| Tool | check-code-quality |
| Quality Gate | PASSED / FAILED |
| Date | `<YYYY-MM-DD>` |

## 1. Executive Summary
<Overview of static analysis and linter findings across all modified layers.>

## 2. Linters & Tool Results

| Layer / Tool | Files Scanned | Errors | Warnings | Status |
|---|---|---|---|---|
| Terraform (`tflint`, `fmt`) | | | | PASSED / FAILED |
| Helm (`helm lint`) | | | | PASSED / FAILED |
| Kubernetes / JCasC (`yamllint`) | | | | PASSED / FAILED |
| Shell (`shellcheck`) | | | | PASSED / FAILED |
| Python (`ruff` / `flake8`) | | | | PASSED / FAILED |

## 3. Detailed Issues & Remediations
### Issue 1: `<file>:<line>`
- **Tool**: <Linter Name>
- **Message**: <Warning or Error output>
- **Remediation**: <Suggested fix>
```
