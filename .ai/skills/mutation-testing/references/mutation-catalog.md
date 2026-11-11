# Platform Resilience & Mutation Catalog

Catalog of fault injection and mutation testing scenarios tailored to validating High Availability, self-healing, failover, and alerting mechanisms for this platform.

---

## 1. Kubernetes Cluster & Node Level Scenarios (`tests/kubernetes-ha/`)

- **MUT-K8S-01: Worker Node Hard Drain**: Abruptly drain an active worker node running Jenkins or Automation Tracker pods. Verify PodDisruptionBudgets (PDB) maintain quorum and surviving nodes pick up pods without service disruption.
- **MUT-K8S-02: Control Plane Split Brain Simulation**: Partition one control plane node in a 3-node HA Kind / EKS cluster. Verify etcd quorum remains intact and the API server remains responsive.
- **MUT-K8S-03: Resource Exhaustion (OOM/CPU Throttling)**: Inject CPU/memory stress to test Horizontal Pod Autoscaler (HPA) scale-out and pod eviction boundaries.

---

## 2. Jenkins Server & JCasC Resilience (`tests/failover/`)

- **MUT-JNK-01: Controller Pod Crash**: Forcefully terminate the Jenkins controller pod (`kubectl delete pod -n jenkins jenkins-0 --now`). Verify immediate rescheduling, volume reattachment, and JCasC configuration reload within 45 seconds.
- **MUT-JNK-02: Dynamic Agent Severance**: Abruptly terminate an in-flight dynamic Kubernetes agent pod. Verify Jenkins controller flags the failure, marks the stage for retry, and spawns a replacement agent.
- **MUT-JNK-03: JCasC Configuration Corruption**: Mutate an environment variable or secret to simulate JCasC startup validation error. Verify Jenkins health check reports degraded status and Alertmanager fires.

---

## 3. Observability & Alertmanager Verification (`monitoring/`)

- **MUT-MON-01: Heartbeat Interruption**: Blackhole scraping targets for Jenkins or Kubernetes control plane. Verify Prometheus fires `JenkinsDown` or `KubernetesNodeDown` within 60 seconds and Alertmanager dispatches notifications.
- **MUT-MON-02: Alert Deduplication Test**: Fire identical alerts across multi-replica Prometheus instances. Verify Alertmanager properly deduplicates into a single alert notification.

---

## 4. Cloud Emulators & LocalStack (`tests/aws-integration/`, `tests/azure-integration/`)

- **MUT-EMU-01: Transient S3 / Blob Storage Failure**: Inject 503 Service Unavailable responses in LocalStack S3 emulator. Verify Terraform and test runners execute exponential backoff retries.
- **MUT-EMU-02: IAM Permission Deprivation**: Revoke an IAM role binding to verify Terraform and services fail fast with clear, traceable permission errors.

---

## 5. Disaster Recovery & Backup Integrity (`tests/disaster-recovery/`)

- **MUT-DR-01: Namespace Annihilation**: Delete the `automation-tracker` or `jenkins` namespace completely. Execute `backup-recovery/scripts/restore.sh` and verify state restoration to the last snapshot.
