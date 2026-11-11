"""Shared Pytest Fixtures for LocalStack, Azure Emulator, Kubernetes, and Observability."""

import os
import pytest
import requests

LOCALSTACK_ENDPOINT = os.getenv("LOCALSTACK_ENDPOINT", "http://localhost:4566")
TRACKER_ENDPOINT = os.getenv("TRACKER_ENDPOINT", "http://localhost:8000")
PROMETHEUS_ENDPOINT = os.getenv("PROMETHEUS_ENDPOINT", "http://localhost:9090")
ALERTMANAGER_ENDPOINT = os.getenv("ALERTMANAGER_ENDPOINT", "http://localhost:9093")

@pytest.fixture(scope="session")
def localstack_endpoint():
    return LOCALSTACK_ENDPOINT

@pytest.fixture(scope="session")
def tracker_endpoint():
    return TRACKER_ENDPOINT

@pytest.fixture(scope="session")
def prometheus_endpoint():
    return PROMETHEUS_ENDPOINT

@pytest.fixture(scope="session")
def alertmanager_endpoint():
    return ALERTMANAGER_ENDPOINT

@pytest.fixture
def is_localstack_available():
    try:
        res = requests.get(f"{LOCALSTACK_ENDPOINT}/_localstack/health", timeout=2)
        return res.status_code == 200
    except requests.exceptions.RequestException:
        return False
