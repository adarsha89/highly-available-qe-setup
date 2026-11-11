#!/usr/bin/env bash
set -eo pipefail

echo "================================================================="
echo "   Highly Available QE Platform - Local Environment Bootstrap   "
echo "================================================================="

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"

# 1. Environment file setup
if [ ! -f "$SCRIPT_DIR/.env" ]; then
  echo "==> Creating .env from .env.example..."
  cp "$SCRIPT_DIR/.env.example" "$SCRIPT_DIR/.env"
fi

# 2. Check Prerequisites
echo "==> Checking prerequisites..."
command -v docker >/dev/null 2>&1 || { echo "ERROR: docker is required."; exit 1; }
docker info >/dev/null 2>&1 || { echo "ERROR: Docker daemon is not running."; exit 1; }

# 3. Provision HA Kind Cluster
echo "==> Provisioning Multi-Node HA Kubernetes Cluster via Kind..."
if command -v kind >/dev/null 2>&1; then
  if kind get clusters 2>/dev/null | grep -q "^qe-ha-cluster$"; then
    echo "==> Kind cluster 'qe-ha-cluster' is already running."
    STOPPED_NODES=$(docker ps -a -q --filter "label=io.x-k8s.kind.cluster=qe-ha-cluster" --filter "status=exited" 2>/dev/null || true)
    if [ -n "$STOPPED_NODES" ]; then
      echo "==> Starting paused Kind cluster nodes..."
      docker start $STOPPED_NODES >/dev/null 2>&1 || true
      sleep 3
    fi
  else
    "$ROOT_DIR/kubernetes/kind/setup-kind.sh"
  fi
else
  echo "==> [Notice] kind CLI not found. Local Kubernetes cluster can be started via Kind when available."
fi

# 4. Start Local Docker Services (LocalStack, Azurite, Tracker, Monitoring)
echo "==> Starting local infrastructure containers via Docker Compose..."
docker compose -f "$SCRIPT_DIR/docker-compose.yml" up -d --build

echo "==> Waiting for LocalStack AWS emulator to be ready..."
RETRIES=0
MAX_RETRIES=30
until curl -s http://localhost:4566/_localstack/health | grep -E -q "\"s3\": \"(available|running)\""; do
  RETRIES=$((RETRIES+1))
  if [ "$RETRIES" -ge "$MAX_RETRIES" ]; then
    echo " [Notice] LocalStack startup is taking longer than usual, proceeding with startup..."
    break
  fi
  sleep 2
  printf "."
done
[ "$RETRIES" -lt "$MAX_RETRIES" ] && echo " Ready!"

# 5. Setup Jenkins using scripts in jenkins/
echo "==> Setting up Jenkins CI/CD controller using jenkins/ scripts..."
if [ -f "$ROOT_DIR/jenkins/setup-jenkins.sh" ]; then
  bash "$ROOT_DIR/jenkins/setup-jenkins.sh"
elif [ -f "$ROOT_DIR/jenkins/setup.sh" ]; then
  bash "$ROOT_DIR/jenkins/setup.sh"
fi

JENKINS_PORT="${JENKINS_PORT:-8088}"

echo "================================================================="
echo "   Local QE Platform is UP and RUNNING!                          "
echo "================================================================="
echo " - LocalStack Gateway:      http://localhost:4566"
echo " - Azurite Azure Emulator:  http://localhost:10000"
echo " - Automation Tracker UI:   http://localhost:3000"
echo " - Automation Tracker API:  http://localhost:8000/docs"
echo " - Prometheus Engine:       http://localhost:9090"
echo " - Grafana Dashboards:      http://localhost:3001 (admin/admin)"
echo " - Alertmanager:            http://localhost:9093"
echo " - Jenkins Web UI:          http://localhost:${JENKINS_PORT} (admin/admin123)"
echo "================================================================="
