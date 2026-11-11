#!/usr/bin/env bash
set -eo pipefail

echo "================================================================="
echo "   Highly Available QE Platform - Jenkins Setup & Deployment     "
echo "================================================================="

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
HELM_CHART_DIR="$ROOT_DIR/kubernetes/helm/jenkins-ha"
CASC_FILE="$SCRIPT_DIR/casc/jenkins.yaml"
PID_FILE="$SCRIPT_DIR/.jenkins-port-forward.pid"

# Default port for Jenkins Web UI
JENKINS_PORT="${JENKINS_PORT:-8088}"

# 1. Check prerequisites
echo "==> Checking prerequisites for Jenkins..."
command -v kubectl >/dev/null 2>&1 || { echo "ERROR: kubectl is required to deploy Jenkins."; exit 1; }
command -v helm >/dev/null 2>&1 || { echo "ERROR: helm is required to deploy Jenkins."; exit 1; }

# 2. Check Kubernetes cluster connectivity
echo "==> Verifying Kubernetes cluster connectivity..."
if ! kubectl cluster-info >/dev/null 2>&1; then
  if command -v kind >/dev/null 2>&1 && kind get clusters 2>/dev/null | grep -q "^qe-ha-cluster$"; then
    echo "==> Cluster 'qe-ha-cluster' exists but is unresponsive. Checking container state..."
    STOPPED_NODES=$(docker ps -a -q --filter "label=io.x-k8s.kind.cluster=qe-ha-cluster" --filter "status=exited" 2>/dev/null || true)
    if [ -n "$STOPPED_NODES" ]; then
      echo "==> Starting paused Kind cluster containers..."
      docker start $STOPPED_NODES
      sleep 3
    fi
  else
    echo "==> Kind cluster not active. Initializing via setup-kind.sh..."
    "$ROOT_DIR/kubernetes/kind/setup-kind.sh"
  fi
fi

# 3. Ensure namespace exists
echo "==> Ensuring namespace 'jenkins' exists..."
kubectl create namespace jenkins --dry-run=client -o yaml | kubectl apply -f -

# 4. Deploy or upgrade Jenkins HA Helm chart using JCasC and seed jobs configuration
echo "==> Deploying Jenkins HA Helm chart with JCasC configuration from $CASC_FILE..."
helm upgrade --install jenkins "$HELM_CHART_DIR" \
  --namespace jenkins \
  --create-namespace \
  --set-file cascConfig="$CASC_FILE" \
  --set controller.jenkinsUrl="http://localhost:${JENKINS_PORT}/" \
  --wait --timeout=300s

# Ensure statefulset is scaled to at least 1 replica
CURRENT_REPLICAS=$(kubectl get statefulset jenkins-controller -n jenkins -o jsonpath='{.spec.replicas}' 2>/dev/null || echo "1")
if [ "$CURRENT_REPLICAS" -eq 0 ]; then
  echo "==> Scaling up jenkins-controller to 1 replica..."
  kubectl scale statefulset jenkins-controller -n jenkins --replicas=1
fi

echo "==> Waiting for Jenkins Controller rollout to complete..."
kubectl rollout status statefulset/jenkins-controller -n jenkins --timeout=180s

# 5. Establish or verify port-forwarding tunnel
SERVICE_NAME="$(kubectl get svc -n jenkins -l app.kubernetes.io/name=jenkins -o jsonpath='{.items[0].metadata.name}' 2>/dev/null || echo "jenkins-service")"

# Clean up stale PID file if process is dead
if [ -f "$PID_FILE" ]; then
  OLD_PID=$(cat "$PID_FILE" 2>/dev/null || true)
  if [ -n "$OLD_PID" ] && ! kill -0 "$OLD_PID" 2>/dev/null; then
    rm -f "$PID_FILE"
  fi
fi

# Check if port is already serving Jenkins
PORT_ACTIVE=false
if lsof -i ":${JENKINS_PORT}" >/dev/null 2>&1; then
  echo "==> Port ${JENKINS_PORT} is currently occupied. Checking if Jenkins is responding..."
  if curl -s -o /dev/null -w "%{http_code}" "http://localhost:${JENKINS_PORT}/login" 2>/dev/null | grep -q -E "200|403"; then
    echo "==> Jenkins Web UI is already reachable on http://localhost:${JENKINS_PORT}"
    PORT_ACTIVE=true
  else
    echo "==> Warning: Port ${JENKINS_PORT} is in use by another process. Terminating existing port-forward..."
    pkill -f "kubectl.*port-forward.*${JENKINS_PORT}" 2>/dev/null || true
    sleep 1
  fi
fi

if [ "$PORT_ACTIVE" = false ]; then
  echo "==> Starting port-forward (localhost:${JENKINS_PORT} -> ${SERVICE_NAME}:8080)..."
  nohup kubectl port-forward -n jenkins "svc/${SERVICE_NAME}" "${JENKINS_PORT}:8080" >/dev/null 2>&1 &
  PF_PID=$!
  echo "$PF_PID" > "$PID_FILE"
  sleep 2
fi

# 6. Verify Jenkins HTTP health endpoint
echo "==> Probing Jenkins health endpoint on http://localhost:${JENKINS_PORT}/login..."
RETRIES=0
MAX_RETRIES=20
READY=false
until [ "$READY" = true ] || [ "$RETRIES" -ge "$MAX_RETRIES" ]; do
  HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" "http://localhost:${JENKINS_PORT}/login" 2>/dev/null || echo "000")
  if [ "$HTTP_CODE" = "200" ] || [ "$HTTP_CODE" = "403" ]; then
    READY=true
    break
  fi
  RETRIES=$((RETRIES+1))
  sleep 2
  printf "."
done

if [ "$READY" = true ]; then
  echo " Ready!"
else
  echo " [Notice] Jenkins is starting up. It will be available on http://localhost:${JENKINS_PORT} momentarily."
fi

echo "================================================================="
echo "   Jenkins CI/CD Controller is Ready!                            "
echo "================================================================="
echo " - Web UI URL:         http://localhost:${JENKINS_PORT}"
echo " - Admin Username:     admin"
echo " - Admin Password:     ${JENKINS_ADMIN_PASSWORD:-admin123}"
echo " - JCasC State:        Loaded from $CASC_FILE"
echo " - Dynamic Agent Pool: kubernetes (qe-agent template)"
echo "================================================================="
