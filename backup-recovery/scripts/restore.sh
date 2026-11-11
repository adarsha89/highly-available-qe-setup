#!/usr/bin/env bash
set -eo pipefail

ARCHIVE_PATH="$1"
if [ -z "$ARCHIVE_PATH" ]; then
  echo "Usage: $0 <path-to-backup-tar.gz>"
  exit 1
fi

echo "================================================================="
echo "   Restoring QE Platform from Backup: $ARCHIVE_PATH              "
echo "================================================================="

RESTORE_DIR="/tmp/qe-restore-$(date +%s)"
mkdir -p "$RESTORE_DIR"
tar -xzf "$ARCHIVE_PATH" -C "$RESTORE_DIR"

# 1. Restore Kubernetes Manifests
if command -v kubectl >/dev/null 2>&1; then
  echo "==> Re-applying Kubernetes resources..."
  find "$RESTORE_DIR" -name "*-manifests.yaml" -exec kubectl apply -f {} \;
fi

# 2. Restore Tracker Database
if [ -f "$RESTORE_DIR"/*/tracker.db.bak ]; then
  echo "==> Restoring Tracker database..."
  cp "$RESTORE_DIR"/*/tracker.db.bak tracker.db
fi

echo "==> Restore sequence completed."
