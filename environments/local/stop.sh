#!/usr/bin/env bash
set -eo pipefail

echo "================================================================="
echo "   Highly Available QE Platform - Stop Local Environment         "
echo "================================================================="

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"

STOP_CLUSTER=false
DELETE_CLUSTER=false
CLEAN_VOLUMES=false

for arg in "$@"; do
  case "$arg" in
    --stop-cluster|--all)
      STOP_CLUSTER=true
      ;;
    --delete-cluster)
      DELETE_CLUSTER=true
      ;;
    --clean)
      CLEAN_VOLUMES=true
      ;;
    --help|-h)
      echo "Usage: ./stop.sh [OPTIONS]"
      echo ""
      echo "Options:"
      echo "  --stop-cluster, --all   Stop Kind cluster containers as well"
      echo "  --delete-cluster        Delete Kind cluster completely"
      echo "  --clean                 Remove Docker volumes and emulator caches"
      echo "  --help, -h              Show this help message"
      exit 0
      ;;
  esac
done

# 1. Stop Jenkins controller & Port-Forwarding tunnels
echo "==> Stopping Jenkins & port-forward tunnels..."
if [ -f "$ROOT_DIR/jenkins/stop-jenkins.sh" ]; then
  bash "$ROOT_DIR/jenkins/stop-jenkins.sh"
elif [ -f "$ROOT_DIR/jenkins/stop.sh" ]; then
  bash "$ROOT_DIR/jenkins/stop.sh"
else
  pkill -f "kubectl.*port-forward.*jenkins" 2>/dev/null || true
  if command -v kubectl >/dev/null 2>&1 && kubectl cluster-info >/dev/null 2>&1; then
    kubectl scale statefulset jenkins-controller -n jenkins --replicas=0 2>/dev/null || true
  fi
fi

# 2. Stop Docker Compose Services (LocalStack, Azurite, Tracker, Monitoring)
echo "==> Stopping Docker Compose services..."
if [ "$CLEAN_VOLUMES" = true ]; then
  echo "==> Removing containers, networks, volumes, and caches..."
  docker compose -f "$SCRIPT_DIR/docker-compose.yml" down -v --remove-orphans
  rm -rf "$SCRIPT_DIR/.localstack" "$SCRIPT_DIR/.azurite"
else
  docker compose -f "$SCRIPT_DIR/docker-compose.yml" down
fi

# 3. Handle Kind Cluster if requested
if [ "$DELETE_CLUSTER" = true ]; then
  if command -v kind >/dev/null 2>&1; then
    echo "==> Deleting Kind cluster 'qe-ha-cluster'..."
    kind delete cluster --name qe-ha-cluster || true
  fi
elif [ "$STOP_CLUSTER" = true ]; then
  echo "==> Stopping Kind cluster containers..."
  CLUSTER_CONTAINERS=$(docker ps -q --filter "label=io.x-k8s.kind.cluster=qe-ha-cluster")
  if [ -n "$CLUSTER_CONTAINERS" ]; then
    docker stop $CLUSTER_CONTAINERS || true
  fi
fi

echo "================================================================="
echo "   All local QE Platform applications have been STOPPED.         "
echo "================================================================="
echo " - LocalStack AWS Emulator:   STOPPED"
echo " - Azurite Azure Emulator:    STOPPED"
echo " - Automation Tracker (UI):   STOPPED"
echo " - Automation Tracker (API):  STOPPED"
echo " - Prometheus Engine:         STOPPED"
echo " - Alertmanager:              STOPPED"
echo " - Grafana Dashboards:        STOPPED"
echo " - Loki Centralized Logging:  STOPPED"
echo " - Jenkins CI/CD Controller:  STOPPED"
echo "================================================================="
