#!/usr/bin/env bash
set -eo pipefail

echo "================================================================="
echo "   Highly Available QE Platform - Stop Jenkins Controller        "
echo "================================================================="

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PID_FILE="$SCRIPT_DIR/.jenkins-port-forward.pid"
UNINSTALL=false

for arg in "$@"; do
  case "$arg" in
    --uninstall)
      UNINSTALL=true
      ;;
  esac
done

# 1. Terminate active port-forward tunnel
echo "==> Stopping Jenkins port-forward tunnel..."
if [ -f "$PID_FILE" ]; then
  PID=$(cat "$PID_FILE" 2>/dev/null || true)
  if [ -n "$PID" ] && kill -0 "$PID" 2>/dev/null; then
    kill "$PID" 2>/dev/null || true
  fi
  rm -f "$PID_FILE"
fi
pkill -f "kubectl.*port-forward.*jenkins" 2>/dev/null || true

# 2. Stop Jenkins controller
if command -v kubectl >/dev/null 2>&1 && kubectl cluster-info >/dev/null 2>&1; then
  if [ "$UNINSTALL" = true ]; then
    echo "==> Uninstalling Jenkins Helm release..."
    helm uninstall jenkins -n jenkins 2>/dev/null || true
  else
    echo "==> Scaling Jenkins StatefulSet down to 0 replicas..."
    kubectl scale statefulset jenkins-controller -n jenkins --replicas=0 2>/dev/null || true
  fi
fi

echo "==> Jenkins controller has been stopped."
