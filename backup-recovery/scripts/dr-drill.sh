#!/usr/bin/env bash
set -eo pipefail

echo "================================================================="
echo "   Disaster Recovery Drill: Outage & Restoration Simulation      "
echo "================================================================="

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Step 1: Take baseline backup
echo "==> Step 1: Generating fresh backup snapshot..."
bash "$SCRIPT_DIR/backup.sh"

LATEST_BACKUP=$(ls -t /tmp/qe-backups/*.tar.gz 2>/dev/null | head -n 1 || echo "")
if [ -z "$LATEST_BACKUP" ]; then
  echo "ERROR: Backup archive not found."
  exit 1
fi
echo "==> Using backup snapshot: $LATEST_BACKUP"

# Step 2: Simulate failure (e.g. simulate pod deletion or namespace degradation)
echo "==> Step 2: Simulating platform disruption..."
if command -v kubectl >/dev/null 2>&1; then
  kubectl delete pod -n jenkins -l app.kubernetes.io/name=jenkins --now || true
fi

# Step 3: Trigger Restore
START_TIME=$(date +%s)
echo "==> Step 3: Executing restore sequence..."
bash "$SCRIPT_DIR/restore.sh" "$LATEST_BACKUP"

END_TIME=$(date +%s)
ELAPSED=$((END_TIME - START_TIME))
echo "==> Disaster Recovery Drill Completed. Total RTO: ${ELAPSED} seconds."
