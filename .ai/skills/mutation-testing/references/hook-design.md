# Resilience & Mutation Hook Design

Guide for configuring and executing chaos and mutation test hooks across Kubernetes, Jenkins, and LocalStack.

## Logical Flow

```text
Mutation Registry & Catalog
  → Chaos / Fault Controller (pytest fixture or shell harness)
    → Target System (Kind / LocalStack / Jenkins / Alertmanager)
      → Observability Verification (Prometheus metrics & Alertmanager webhooks)
        → Self-Healing Verification (RTO measurement & health checks)
          → Report Generator (docs/mutation/)
```

## Activation & Environment Switches

Resilience and fault-injection runs are gated by environment variables so that ordinary CI builds never experience destructive tests by default:

```bash
# Enable chaos/mutation test mode
export RESILIENCE_TESTS_ENABLED=true
export MUTATION_ID="MUT-JNK-01"

# Run target resilience scenario
pytest tests/failover/ -m "resilience"
```

## Clean State & Tear Down

Every fault injection must follow strict cleanup conventions:
1. Pre-flight check: Verify cluster health and pod availability before triggering the fault.
2. Injected state: Trigger failure (node cordon, pod kill, network block).
3. Post-flight verification: Assert self-healing, verify alerts fired and resolved, and restore any drained nodes or modified configs.
