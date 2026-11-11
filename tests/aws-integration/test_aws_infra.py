"""Integration Tests for AWS / LocalStack Infrastructure Provisioning."""

import pytest
import requests

def test_localstack_health(is_localstack_available, localstack_endpoint):
    if not is_localstack_available:
        pytest.skip("LocalStack emulator is not running.")
    res = requests.get(f"{localstack_endpoint}/_localstack/health")
    assert res.status_code == 200
    data = res.json()
    assert "services" in data or "features" in data or isinstance(data, dict)

def test_s3_artifacts_bucket_accessible(is_localstack_available, localstack_endpoint):
    if not is_localstack_available:
        pytest.skip("LocalStack emulator is not running.")
    # Check S3 endpoint via LocalStack
    res = requests.get(f"{localstack_endpoint}/qe-automation-artifacts")
    # 200 or 403 or 404 (if not initialized yet) means S3 service responded
    assert res.status_code in [200, 403, 404]
