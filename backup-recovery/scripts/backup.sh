#!/usr/bin/env bash
set -eo pipefail

echo "================================================================="
echo "   Initiating High Availability Backup for QE Platform          "
echo "================================================================="

BACKUP_NAME="qe-platform-backup-$(date +%Y%m%d%H%M%S)"
BACKUP_DIR="${BACKUP_DIR:-/tmp/qe-backups}/$BACKUP_NAME"
mkdir -p "$BACKUP_DIR"

# 1. Backup Kubernetes Namespaces & Resources
if command -v kubectl >/dev/null 2>&1; then
  echo "==> Exporting Kubernetes manifests for active QE namespaces..."
  for ns in jenkins argocd automation-tracker monitoring; do
    echo "  - Backing up namespace: $ns"
    kubectl get all,configmap,secret,pvc -n "$ns" -o yaml > "$BACKUP_DIR/${ns}-manifests.yaml" 2>/dev/null || true
  done
fi

# 2. Backup Tracker Database (SQLite snapshot or DB dump)
if [ -f "tracker.db" ]; then
  echo "==> Snapshotting Central Automation Tracker database..."
  cp tracker.db "$BACKUP_DIR/tracker.db.bak"
fi

# 3. Archive & Upload to S3 / LocalStack / Azure Blob Storage
echo "==> Compressing backup archive..."
tar -czf "${BACKUP_DIR}.tar.gz" -C "$(dirname "$BACKUP_DIR")" "$BACKUP_NAME"

if command -v awslocal >/dev/null 2>&1; then
  echo "==> Uploading backup archive to S3 (LocalStack / AWS)..."
  awslocal s3 cp "${BACKUP_DIR}.tar.gz" "s3://qe-velero-backups/${BACKUP_NAME}.tar.gz" || true
elif command -v aws >/dev/null 2>&1; then
  echo "==> Uploading backup archive to AWS S3..."
  aws s3 cp "${BACKUP_DIR}.tar.gz" "s3://qe-velero-backups/${BACKUP_NAME}.tar.gz" || true
fi

echo "==> Backup completed successfully: ${BACKUP_DIR}.tar.gz"
