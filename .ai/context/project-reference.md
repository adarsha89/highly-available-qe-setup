# Project Reference

`requirements.txt` and `README.md` (repo root) are the primary sources of truth for the project requirements, architecture tree, infrastructure patterns, and deployment configurations for this Highly Available QE Platform.
Point there for requirements, setup, and onboarding context instead of re-deriving them.

## Repository Purpose
Build and maintain an enterprise-grade, highly available Quality Engineering (QE) platform supporting local development (Docker / Kind / LocalStack), AWS, and Microsoft Azure using:
- **Kubernetes**: Multi-control-plane, resilient, self-healing cluster setups (Kind locally, EKS / AKS via Terraform).
- **Terraform**: Infrastructure as Code with reusable modules (`kubernetes`, `networking`, `storage`, `iam`, `monitoring`) for AWS, Azure, and LocalStack.
- **Helm Charts**: Standardized packaging for platform workloads, operators, and QE services.
- **ArgoCD**: GitOps continuous deployment and automated drift reconciliation.
- **Jenkins & JCasC**: Highly available Jenkins server, pipelines, dynamic Kubernetes agent scaling, and Jenkins Configuration as Code.
- **Central Automation Tracking Service**: Resilient tracking service (backend, frontend, DB, API tests).
- **Cloud Emulators**: LocalStack (AWS) and LocalStack-Azure for high-fidelity offline / local testing.
- **Full Observability & Alerting**: Prometheus, Grafana, Alertmanager, and Loki with automated alerts for cluster or Jenkins outages.
- **Backup & Recovery**: Automated snapshotting, Velero policies, and automated restore tests.
- **QE Base Integration**: Observability instrumentation and unified CI scripts (Jenkins, GitHub Actions, local) for all downstream `qe-base` repositories.

For detailed design principles, architectural conventions, operational runbooks, and verification commands, see
[`.ai/skills/_shared/framework-guidelines.md`](../skills/_shared/framework-guidelines.md).
