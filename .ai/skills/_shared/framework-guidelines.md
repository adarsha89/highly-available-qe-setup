# Highly Available QE Platform Guidelines

Single source of truth for architectural principles, repo structure, coding standards, and verification procedures that every skill in `.ai/skills/` and agent in `.ai/agents/` plans against, implements against, and reviews against.

---

## 1. Repo Blueprint & Requirements Snapshot

| Concern | Standard / Choice |
|---|---|
| **Purpose** | Highly Available QE Platform supporting AWS, Microsoft Azure, and local Docker/Kind setups. |
| **Infrastructure as Code (IaC)** | Terraform (modular structure under `terraform/modules/`, environment roots under `terraform/aws/` and `terraform/azure/`). |
| **Container & Workload Packaging** | Helm Charts (`kubernetes/helm/`) for all platform services, Jenkins, ArgoCD, and monitoring. |
| **GitOps & Reconciliation** | ArgoCD (`kubernetes/argocd/`) for continuous deployment, state synchronization, and automated drift reconciliation. |
| **Kubernetes HA** | Multi-node/HA Kind setup locally (`kubernetes/kind/`), EKS / AKS via Terraform for cloud; PDBs (PodDisruptionBudgets), HPA, topology spread constraints, node anti-affinity. |
| **CI / CD Orchestration** | Highly Available Jenkins controller with JCasC (`jenkins/casc/`), dynamic Kubernetes agent pods (`jenkins/pipelines/`), plugins list (`jenkins/plugins/`), and seed jobs (`jenkins/jobs/`). |
| **Central Automation Tracking** | Central automation tracking service (`qe-central-tracking-application/backend/`, `qe-central-tracking-application/frontend/`, `qe-central-tracking-application/tests/`) deployed with active replication and failover. |
| **Cloud Emulation** | LocalStack for AWS emulation (`cloud-emulators/aws/localstack/`) and LocalStack-Azure (`cloud-emulators/azure/localstack-azure/`) for offline/local testing. |
| **Observability & Alerting** | Prometheus (`monitoring/prometheus/`), Grafana (`monitoring/grafana/`), Alertmanager (`monitoring/alertmanager/`), and Loki (`monitoring/loki/`). Must alert when Kubernetes cluster or Jenkins becomes degraded or goes down. |
| **Backup & Disaster Recovery** | Automated backup policies and recovery scripts (`backup-recovery/scripts/`, `backup-recovery/policies/`, `backup-recovery/restore-tests/`) targeting Velero / cloud snapshots. |
| **Testing Suites** | Automated validation suites under `tests/`: `aws-integration/`, `azure-integration/`, `kubernetes-ha/`, `failover/`, `disaster-recovery/`. |
| **Downstream QE Base Integration** | Standardized observability instrumentation and reusable CI scripts (`jenkins`, `github`, `local`) for all downstream `qe-base` repositories. |

---

## 2. Directory Layout & Layering Rules

```
highly-available-qa/
├── environments/               # Environment-level orchestration & overrides
│   ├── local/                  # Local docker-compose / kind orchestration
│   ├── aws/                    # AWS deployment configs & parameter maps
│   └── azure/                  # Azure deployment configs & parameter maps
│
├── cloud-emulators/            # Offline cloud emulation runtimes
│   ├── aws/localstack/         # LocalStack docker-compose, init hooks, AWS mock services
│   └── azure/localstack-azure/ # LocalStack Azure emulation configs
│
├── terraform/                  # Infrastructure as Code
│   ├── modules/                # Reusable, cloud-abstracted or cloud-specific modules
│   │   ├── kubernetes/         # Cluster provisioning (EKS, AKS, node groups)
│   │   ├── networking/         # VPCs, subnets, route tables, security groups, VNet
│   │   ├── storage/            # S3, Blob Storage, EFS/EBS, PersistentVolumes
│   │   ├── iam/                # IAM roles, policies, service account OIDC bindings
│   │   └── monitoring/         # CloudWatch, Azure Monitor, metrics integration
│   ├── aws/                    # Root module for AWS deployment
│   └── azure/                  # Root module for Azure deployment
│
├── kubernetes/                 # Kubernetes cluster manifests and charts
│   ├── kind/                   # Multi-node HA Kind cluster configs
│   ├── namespaces/             # Standard namespace definitions with resource quotas
│   ├── policies/               # NetworkPolicies, OPA Gatekeeper / Kyverno policies
│   ├── helm/                   # Custom Helm charts for platform services
│   └── argocd/                 # ArgoCD Applications, AppProjects, ApplicationSets
│
├── jenkins/                    # Jenkins controller & agents configuration
│   ├── casc/                   # Jenkins Configuration as Code YAML files
│   ├── jobs/                   # Job DSL and XML job definitions
│   ├── plugins/                # Locked plugins.txt with versioning
│   └── pipelines/              # Shared libraries, Jenkinsfiles for dynamic K8s agents
│
├── qe-central-tracking-application/ # Central test execution tracking service
│   ├── backend/                # API service (FastAPI/Go/Node) for receiving test telemetry
│   ├── frontend/               # UI dashboard for live tracking and historical runs
│   └── tests/                  # Integration and contract tests for the tracker
│
├── monitoring/                 # Full observability stack
│   ├── prometheus/             # Prometheus operator CRDs, scrape configs, recording rules
│   ├── grafana/                # Dashboards as code and datasource definitions
│   ├── alertmanager/           # Alert routing, notification templates (Slack, PagerDuty)
│   └── loki/                   # Log aggregation and Promtail/Fluentbit configurations
│
├── backup-recovery/            # DR automation and business continuity
│   ├── scripts/                # Automated backup triggers and restore executors
│   ├── policies/               # Velero backup schedules, retention, snapshot specs
│   └── restore-tests/          # Automated end-to-end restore verification tests
│
└── tests/                      # Verification test suites
    ├── aws-integration/        # Integration tests against AWS / LocalStack
    ├── azure-integration/      # Integration tests against Azure / LocalStack-Azure
    ├── kubernetes-ha/          # Multi-master failover, node disruption verification
    ├── failover/               # Pod disruption, database failover, Jenkins failover
    └── disaster-recovery/      # Cold-start and state restoration from backups
```

### Layering Rules (Dependency Direction is Top → Down)
1. **Cloud Emulators & Environments** provide runtimes and targets.
2. **Terraform** provisions underlying networks, compute, and managed storage.
3. **Kubernetes Core & Policies** configure cluster access, security, and namespaces.
4. **ArgoCD & Helm** deploy applications onto Kubernetes.
5. **Jenkins, Automation Tracker, & Monitoring** run as managed workloads.
6. **Backup & Tests** observe, protect, and validate all layers without modifying production logic.

---

## 3. High Availability & Resilience Standards

1. **Kubernetes HA**:
   - Minimum 3 control plane nodes in production (simulated via Kind multi-control-plane configuration locally).
   - Replicated worker nodes spanning multiple availability zones.
   - `PodDisruptionBudget` (PDB) configured for every critical platform deployment (Jenkins, ArgoCD, Automation Tracker, Prometheus).
   - Anti-affinity rules (`podAntiAffinity`) to prevent colocation of replica pods on the same physical/virtual node.
2. **Jenkins HA & Fault Tolerance**:
   - Controller state externalized or backed by redundant Persistent Volumes (`ReadWriteMany` / CSI volume snapshots).
   - Dynamic ephemeral agents spawned in dedicated Kubernetes namespaces using the Kubernetes Jenkins plugin.
   - JCasC (`jenkins/casc/`) guarantees 100% deterministic reconstruction of Jenkins state upon pod restart.
   - Immediate auto-recovery with health checks (`livenessProbe`, `readinessProbe`).
3. **Central Automation Tracker HA**:
   - Stateless backend with horizontal pod autoscaling (HPA).
   - Database layer configured with primary-replica replication or managed HA database emulation in LocalStack.
4. **Observability & Alerting**:
   - Prometheus and Alertmanager configured in HA pairs with deduplication.
   - Mandatory alert rules:
     - `KubernetesControlPlaneDown` / `NodeNotReady` (Severity: Critical)
     - `JenkinsControllerDown` / `JenkinsUnhealthy` (Severity: Critical)
     - `AutomationTrackerUnavailable` (Severity: High)
     - `ArgoCDSyncFailed` (Severity: Warning)
5. **LocalStack Emulation Fidelity**:
   - All cloud automation must run cleanly against LocalStack without requiring live cloud credentials.
   - Endpoints configured via Terraform provider overrides and AWS/Azure CLI configuration.

---

## 4. Security & Configuration Hygiene

- **Zero Secrets in Code**: Never commit credentials, tokens, or private keys to Git. Use environment variables, Kubernetes Secrets, HashiCorp Vault, or AWS/Azure Secrets Manager integration.
- **LocalStack Dummy Credentials**: Use standard dummy credentials for local testing (`AWS_ACCESS_KEY_ID=test`, `AWS_SECRET_ACCESS_KEY=test`, `AWS_DEFAULT_REGION=us-east-1`).
- **Idempotency**: All Terraform code must be idempotent (`terraform plan` returns clean "No changes" after apply).
- **Helm Standards**: Use strict values schema validation (`values.schema.json`), templated labels, and semantic versioning.

---

## 5. Verification Commands

Run before submitting changes:

```bash
# 1. Terraform Formatting & Validation
terraform -chdir=terraform/modules/<module> fmt -check
terraform -chdir=terraform/modules/<module> init -backend=false
terraform -chdir=terraform/modules/<module> validate

# 2. Helm Linting
helm lint kubernetes/helm/*

# 3. Kubernetes Manifests Validation
kubectl kustomize kubernetes/kind/ | kubeconform -strict -summary || echo "Validated"

# 4. Jenkins Configuration as Code Linting / Verification
# Validate JCasC YAML syntax
yamllint jenkins/casc/*.yaml

# 5. LocalStack Verification
# Spin up localstack and test terraform apply against local endpoints
tflint --recursive
pytest tests/aws-integration/
pytest tests/kubernetes-ha/
```

---

## 6. Standard Result Block

Every skill execution must finish with this machine-readable block:

```markdown
### Result
- **STATUS**: SUCCESS | CHANGES_REQUESTED | BLOCKED | NEEDS_INPUT
- **OUTPUT**: <Primary file path or summary artifact produced>
- **SUMMARY**: <1-3 sentences describing the outcome and evidence>
- **NEXT**: <Recommended next agent or skill to execute>
```

---

## 7. Model Agnosticism

- Agents and skills defined here must operate across all compliant LLM runtimes (e.g., Antigravity CLI / agy, Claude Code, OpenAI Codex).
- Never pin proprietary models in YAML frontmatter or prompt instructions.
- Pass file paths rather than inline file bodies to preserve context hygiene across any model window.
