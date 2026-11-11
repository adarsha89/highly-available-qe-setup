#!/usr/bin/env bash
set -eo pipefail

echo "==> [Local Developer Runner] Executing QE suite with local telemetry..."

SUITE="${1:-local-test-run}"
START_TIME=$(date +%s)
STATUS="PASSED"

if [ -f "pom.xml" ]; then
  mvn test || STATUS="FAILED"
elif [ -d "tests" ]; then
  pytest tests/ || STATUS="FAILED"
fi

DURATION=$(( $(date +%s) - START_TIME ))

# Send telemetry if local tracker is running
if curl -s http://localhost:8000/health >/dev/null 2>&1; then
  python3 "$(dirname "$0")/../observability/qe-telemetry-exporter.py" \
    --tracker-url "http://localhost:8000" \
    --suite "$SUITE" \
    --status "$STATUS" \
    --duration "$DURATION"
fi
