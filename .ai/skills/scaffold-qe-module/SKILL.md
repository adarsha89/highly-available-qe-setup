---
name: scaffold-qe-module
description: Scaffold a new platform module or component (Terraform module under terraform/modules/, Helm chart under kubernetes/helm/, ArgoCD application set, Jenkins JCasC pipeline, cloud emulator setup, or test suite) following the repository architecture in requirements.txt. Produces a reviewable plan, waits for human approval, scaffolds standard boilerplate, and registers the component cleanly.
---

# scaffold-qe-module

## Purpose

Add a new platform component or subsystem to this Highly Available QE Platform repository following the architectural guidelines in `.ai/skills/_shared/framework-guidelines.md` and `requirements.txt`.

Component types supported:
1. **Terraform Module** (`terraform/modules/<name>/`): `main.tf`, `variables.tf`, `outputs.tf`, `versions.tf`, `README.md`.
2. **Helm Chart** (`kubernetes/helm/<name>/`): `Chart.yaml`, `values.yaml`, `values.schema.json`, `templates/` (deployment with PDB, service, ingress, hpa, serviceaccount).
3. **ArgoCD Application / AppSet** (`kubernetes/argocd/<name>.yaml`): GitOps sync policies, automated self-heal, destination cluster/namespace.
4. **Jenkins JCasC & Pipeline** (`jenkins/casc/<name>.yaml`, `jenkins/pipelines/<name>.groovy`): Pod templates, credentials integration, pipeline definitions.
5. **Cloud Emulator Config** (`cloud-emulators/<cloud>/<tool>/`): Docker-compose service definition, initialization scripts.
6. **Integration / Failover Test Suite** (`tests/<type>/`): Pytest suite with fixtures, fault-injection hooks, and assertion reporting.

## Phases

1. **Collect Inputs**: Target component type, name, environment scope (Local, AWS, Azure), and dependencies.
2. **Detect Current State**: Check existing modules, charts, and directories to prevent duplicates and maintain naming conventions.
3. **Plan Scaffolding**: Produce `docs/plans/scaffold-<name>-plan.md` detailing the file tree, template values, and integration points.
4. **Approval Gate**: Request user review and approval of the plan.
5. **Scaffold Files**: Write standard boilerplate files, formatting, and linting configs.
6. **Verification & Manifest**: Run `terraform fmt`, `helm lint`, or `yamllint` to verify, and produce `docs/changes/scaffold-<name>-changes.md`.

## Procedure

### 1. Collect Inputs
- **Q1**: What component type are you scaffolding? (Terraform module, Helm chart, ArgoCD app, JCasC config, Emulator config, Test suite)
- **Q2**: What is the component name and purpose? (e.g., `terraform/modules/networking`, `kubernetes/helm/qe-central-tracking-application`)
- **Q3**: Which target environments does it apply to? (Local, AWS, Azure, All)

### 2. Scaffold Conventions
- **Terraform**: Strict typing in `variables.tf`, explicit descriptions on outputs, pinned minimum provider versions.
- **Helm**: Always include `PodDisruptionBudget` template, health probes (`livenessProbe`, `readinessProbe`), and non-root security context.
- **JCasC**: Validate against Jenkins JCasC schema; never embed plaintext credentials.

### 3. Verify Scaffolding
```bash
# Validate based on component type
[ -d "terraform/modules/<name>" ] && terraform -chdir="terraform/modules/<name>" fmt -check
[ -d "kubernetes/helm/<name>" ] && helm lint "kubernetes/helm/<name>"
```

### 4. Emit Result Block
Finish with the standard result block (guidelines section 6).
