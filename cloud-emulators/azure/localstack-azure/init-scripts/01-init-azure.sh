#!/usr/bin/env bash
set -eo pipefail

echo "==> [Azure Local Emulator Init] Provisioning Azure storage containers and queues..."

# Azurite default dev storage connection string
AZURE_STORAGE_CONNECTION_STRING="DefaultEndpointsProtocol=http;AccountName=devstoreaccount1;AccountKey=Eby8vdM02xNOcqFlqUwJPLlmEtlCDXJ1OUzFT50uSRZ6IFsuFq2UVErCz4I6tq/K1SZFPTOtr/KBHBeksoGMGw==;BlobEndpoint=http://127.0.0.1:10000/devstoreaccount1;"

# Check if az CLI is available
if command -v az >/dev/null 2>&1; then
  echo "==> Creating Azure Blob containers via az CLI..."
  az storage container create --name qe-terraform-state --connection-string "$AZURE_STORAGE_CONNECTION_STRING" || true
  az storage container create --name qe-automation-artifacts --connection-string "$AZURE_STORAGE_CONNECTION_STRING" || true
  az storage container create --name qe-velero-backups --connection-string "$AZURE_STORAGE_CONNECTION_STRING" || true
  az storage queue create --name qe-telemetry-queue --connection-string "$AZURE_STORAGE_CONNECTION_STRING" || true
else
  echo "==> [Note] az CLI not found on host; Azure containers will be created during Terraform init/apply or Python test fixtures."
fi

echo "==> [Azure Local Emulator Init] Completed."
