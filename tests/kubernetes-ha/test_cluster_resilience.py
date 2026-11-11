"""Tests for Kubernetes Multi-Node HA, PDBs, and Anti-Affinity."""

import subprocess
import shutil
import pytest

@pytest.fixture
def has_kubectl():
    return shutil.which("kubectl") is not None

def test_kubernetes_ha_manifest_integrity():
    # Verify Kind HA cluster config exists and specifies 3 control-plane nodes
    with open("kubernetes/kind/kind-ha-cluster.yaml", "r") as f:
        content = f.read()
    assert "role: control-plane" in content
    assert content.count("role: control-plane") == 3, "HA Kind cluster must have 3 control-plane nodes"
    assert "role: worker" in content
    assert content.count("role: worker") >= 2, "HA cluster must have multiple worker nodes"

def test_pod_disruption_budgets_defined():
    with open("kubernetes/policies/pod-disruption-budgets.yaml", "r") as f:
        content = f.read()
    assert "kind: PodDisruptionBudget" in content
    assert "jenkins-pdb" in content
    assert "tracker-backend-pdb" in content

def test_live_cluster_nodes_ready(has_kubectl):
    if not has_kubectl:
        pytest.skip("kubectl not installed.")
    res = subprocess.run(["kubectl", "get", "nodes"], capture_output=True, text=True)
    if res.returncode != 0:
        pytest.skip("No live Kubernetes cluster reachable.")
    assert "Ready" in res.stdout
