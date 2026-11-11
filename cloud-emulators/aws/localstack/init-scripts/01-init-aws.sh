#!/usr/bin/env bash
set -eo pipefail

echo "==> [LocalStack AWS Init] Initializing AWS mock infrastructure..."

export AWS_ACCESS_KEY_ID=test
export AWS_SECRET_ACCESS_KEY=test
export AWS_DEFAULT_REGION=us-east-1
ENDPOINT_URL="http://localhost:4566"

# 1. Create S3 Buckets for Terraform State, Artifacts, and Backups
awslocal --endpoint-url="$ENDPOINT_URL" s3 mb s3://qe-terraform-state-bucket || true
awslocal --endpoint-url="$ENDPOINT_URL" s3 mb s3://qe-automation-artifacts || true
awslocal --endpoint-url="$ENDPOINT_URL" s3 mb s3://qe-velero-backups || true

# Enable bucket versioning for state resilience
awslocal --endpoint-url="$ENDPOINT_URL" s3api put-bucket-versioning \
  --bucket qe-terraform-state-bucket \
  --versioning-configuration Status=Enabled

# 2. Create DynamoDB Lock Table for Terraform State Locking
awslocal --endpoint-url="$ENDPOINT_URL" dynamodb create-table \
  --table-name qe-terraform-locks \
  --attribute-definitions AttributeName=LockID,AttributeType=S \
  --key-schema AttributeName=LockID,KeyType=HASH \
  --billing-mode PAY_PER_REQUEST || true

# 3. Create SNS Alert Topics
awslocal --endpoint-url="$ENDPOINT_URL" sns create-topic --name qe-ha-alerts-critical || true
awslocal --endpoint-url="$ENDPOINT_URL" sns create-topic --name qe-ha-alerts-warning || true

# 4. Create SQS Queues for Test Telemetry Ingestion
awslocal --endpoint-url="$ENDPOINT_URL" sqs create-queue --queue-name qe-test-telemetry-queue || true
awslocal --endpoint-url="$ENDPOINT_URL" sqs create-queue --queue-name qe-test-telemetry-dlq || true

# 5. Create Secrets in SecretsManager
awslocal --endpoint-url="$ENDPOINT_URL" secretsmanager create-secret \
  --name "qe/platform/credentials" \
  --secret-string '{"jenkins_admin":"admin123","tracker_token":"token_secret_xyz"}' || true

echo "==> [LocalStack AWS Init] Successfully provisioned initial mock resources."
