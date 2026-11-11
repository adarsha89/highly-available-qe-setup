"""Contract and Health Tests for QE Central Tracking Application API."""

import os
import sys
import pytest
from fastapi.testclient import TestClient

# Ensure backend can be imported
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../backend")))
from app.main import app

client = TestClient(app)


def test_health_check_returns_healthy():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "HEALTHY"
    assert "timestamp" in data


def test_metrics_endpoint_returns_prometheus_format():
    response = client.get("/metrics")
    assert response.status_code == 200
    assert "qe_test_runs_total" in response.text


def test_create_and_retrieve_test_run():
    payload = {
        "suite": "qe-base-java-verification",
        "environment": "local",
        "status": "PASSED",
        "total_tests": 45,
        "passed_tests": 45,
        "failed_tests": 0,
        "duration_seconds": 12.4,
    }
    create_res = client.post("/api/v1/runs", json=payload)
    assert create_res.status_code == 201
    created_data = create_res.json()
    assert created_data["id"] > 0
    assert created_data["suite"] == "qe-base-java-verification"

    # Verify retrieval
    get_res = client.get(f"/api/v1/runs/{created_data['id']}")
    assert get_res.status_code == 200
    assert get_res.json()["suite"] == "qe-base-java-verification"


def test_stats_calculation():
    res = client.get("/api/v1/stats")
    assert res.status_code == 200
    stats = res.json()
    assert "total_runs" in stats
    assert "pass_rate_percentage" in stats
