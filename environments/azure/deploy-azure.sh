#!/usr/bin/env bash
set -eo pipefail

echo "==> Deploying Highly Available QE Platform to Microsoft Azure..."
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TF_DIR="$SCRIPT_DIR/../../terraform/azure"

if [ ! -f "$SCRIPT_DIR/terraform.tfvars" ]; then
  echo "WARNING: terraform.tfvars not found. Copying from terraform.tfvars.example..."
  cp "$SCRIPT_DIR/terraform.tfvars.example" "$SCRIPT_DIR/terraform.tfvars"
fi

terraform -chdir="$TF_DIR" init
terraform -chdir="$TF_DIR" plan -var-file="$SCRIPT_DIR/terraform.tfvars" -out=tfplan
echo "==> Review the plan above. Run 'terraform apply tfplan' to execute."
