#!/usr/bin/env bash
set -eo pipefail

echo "================================================================="
echo "   [Jenkins K8s Agent] Running Downstream QE Suite               "
echo "================================================================="

SUITE_NAME="${1:-qe-verification-suite}"
TRACKER_URL="${TRACKER_URL:-http://qe-tracker-backend:8000}"
START_TIME=$(date +%s)

echo "==> Executing test runner..."
STATUS="PASSED"
TOTAL_TESTS=0
PASSED_TESTS=0
FAILED_TESTS=0

if [ -f "pom.xml" ]; then
  mvn clean test || STATUS="FAILED"
elif [ -f "pytest.ini" ] || [ -d "tests" ]; then
  pytest || STATUS="FAILED"
else
  echo "==> Generic verification execution..."
fi

END_TIME=$(date +%s)
DURATION=$((END_TIME - START_TIME))

echo "==> Emitting telemetry to Central Automation Tracker: $TRACKER_URL..."
python3 "$(dirname "$0")/../observability/qe-telemetry-exporter.py" \
  --tracker-url "$TRACKER_URL" \
  --suite "$SUITE_NAME" \
  --status "$STATUS" \
  --duration "$DURATION" || true

echo "==> Execution finished with status: $STATUS"
if [ "$STATUS" = "FAILED" ]; then
  exit 1
fi
