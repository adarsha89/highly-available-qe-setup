#!/usr/bin/env bash
set -eo pipefail

echo "==> Setting up Multi-Node High Availability Kubernetes Cluster with Kind..."
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONFIG_FILE="$SCRIPT_DIR/kind-ha-cluster.yaml"
CLUSTER_NAME="qe-ha-cluster"

if kind get clusters 2>/dev/null | grep -q "^$CLUSTER_NAME$"; then
  echo "==> Cluster '$CLUSTER_NAME' already exists. Reconnecting..."
  kubectl cluster-info --context "kind-$CLUSTER_NAME"
  exit 0
fi

echo "==> Creating HA Kind Cluster (3 control-plane + 3 worker nodes)..."
kind create cluster --config "$CONFIG_FILE"

echo "==> Waiting for all nodes to be Ready..."
kubectl wait --for=condition=Ready nodes --all --timeout=180s

echo "==> Applying Namespaces..."
kubectl apply -f "$SCRIPT_DIR/../namespaces/namespaces.yaml"

echo "==> Applying Pod Disruption Budgets & Policies..."
kubectl apply -f "$SCRIPT_DIR/../policies/pod-disruption-budgets.yaml"
kubectl apply -f "$SCRIPT_DIR/../policies/network-policies.yaml"

echo "==> Cluster status:"
kubectl get nodes -o wide
echo "==> High Availability Kind Cluster is Ready!"
