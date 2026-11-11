#!/usr/bin/env bash
set -eo pipefail

echo "==> [GitHub Actions] Setting up LocalStack emulator & running QE suite..."

export AWS_ACCESS_KEY_ID=test
export AWS_SECRET_ACCESS_KEY=test
export AWS_DEFAULT_REGION=us-east-1
export LOCALSTACK_ENDPOINT="${LOCALSTACK_ENDPOINT:-http://localhost:4566}"

# Run suite
STATUS="PASSED"
START_TIME=$(date +%s)

if [ -f "pom.xml" ]; then
  mvn clean test || STATUS="FAILED"
elif [ -d "tests" ]; then
  pytest tests/ || STATUS="FAILED"
fi

DURATION=$(( $(date +%s) - START_TIME ))

if [ -n "$TRACKER_URL" ]; then
  python3 "$(dirname "$0")/../observability/qe-telemetry-exporter.py" \
    --tracker-url "$TRACKER_URL" \
    --suite "${GITHUB_REPOSITORY:-qe-repo}" \
    --status "$STATUS" \
    --duration "$DURATION" || true
fi

[ "$STATUS" = "PASSED" ]
