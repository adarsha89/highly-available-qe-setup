"""Comprehensive Integration & Contract Tests for QE Central Tracking Application."""

from datetime import datetime, timezone, timedelta
import os
import sys
import pytest
from fastapi.testclient import TestClient

# Ensure backend path is importable
BACKEND_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../backend"))
if BACKEND_DIR not in sys.path:
    sys.path.insert(0, BACKEND_DIR)

from app.main import app

client = TestClient(app)


def test_health_check_returns_healthy():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "HEALTHY"
    assert data["database"] == "connected"
    assert "timestamp" in data


def test_metrics_endpoint_returns_prometheus_format():
    response = client.get("/metrics")
    assert response.status_code == 200
    assert "qe_test_runs_total" in response.text
    assert "qe_ha_active_services" in response.text


def test_legacy_telemetry_compatibility():
    payload = {
        "suite": "qe-base-contract-verification",
        "environment": "ci",
        "status": "PASSED",
        "total_tests": 50,
        "passed_tests": 49,
        "failed_tests": 1,
        "duration_seconds": 15.2,
        "metadata": {"build_id": "build-legacy-1"},
    }
    create_res = client.post("/api/v1/runs", json=payload)
    assert create_res.status_code == 201
    created = create_res.json()
    assert created["id"] > 0
    assert created["suite"] == "qe-base-contract-verification"

    # Get by ID
    get_res = client.get(f"/api/v1/runs/{created['id']}")
    assert get_res.status_code == 200
    assert get_res.json()["suite"] == "qe-base-contract-verification"

    # Get stats
    stats_res = client.get("/api/v1/stats")
    assert stats_res.status_code == 200
    stats = stats_res.json()
    assert stats["total_runs"] > 0
    assert "pass_rate_percentage" in stats

    # Alertmanager webhook test
    alert_res = client.post("/api/v1/alerts", json={"status": "firing", "alerts": [{"labels": {"alertname": "Test"}}]})
    assert alert_res.status_code == 200
    assert alert_res.json()["status"] == "received"


def test_executions_endpoints():
    now = datetime.now(timezone.utc)
    started = (now - timedelta(minutes=5)).isoformat()
    finished = now.isoformat()

    payload = {
        "category": "api",
        "suite_name": "api-gateway-auth-suite",
        "environment": "staging",
        "build_id": "build-test-200",
        "status": "passed",
        "total_tests": 30,
        "passed_tests": 30,
        "failed_tests": 0,
        "skipped_tests": 0,
        "triggered_by": "pytest-ci",
        "started_at": started,
        "finished_at": finished,
    }
    res = client.post("/api/executions", json=payload)
    assert res.status_code == 200
    exec_data = res.json()
    assert exec_data["id"] > 0
    assert exec_data["category"] == "api"
    assert exec_data["suite_name"] == "api-gateway-auth-suite"

    # List executions
    list_res = client.get("/api/executions?build_id=build-test-200")
    assert list_res.status_code == 200
    assert len(list_res.json()) >= 1


def test_deployments_endpoints():
    now = datetime.now(timezone.utc)
    started = (now - timedelta(minutes=10)).isoformat()
    finished = now.isoformat()

    payload = {
        "service_name": "auth-service",
        "environment": "staging",
        "category": "api",
        "status": "success",
        "build_id": "build-test-200",
        "started_at": started,
        "finished_at": finished,
    }
    res = client.post("/api/deployments", json=payload)
    assert res.status_code == 200
    dep_data = res.json()
    assert dep_data["id"] > 0

    stats_res = client.get("/api/deployments/stats?environment=staging")
    assert stats_res.status_code == 200
    assert stats_res.json()["count"] > 0


def test_defects_endpoints():
    now = datetime.now(timezone.utc).isoformat()
    payload = {
        "title": "Token refresh returns 500 on expired refresh token",
        "category": "api",
        "priority": "critical",
        "status": "open",
        "detected_by": "automation",
        "detection_phase": "pre_release",
        "build_id": "build-test-200",
        "detected_at": now,
    }
    res = client.post("/api/defects", json=payload)
    assert res.status_code == 200
    defect = res.json()
    assert defect["id"] > 0
    defect_id = defect["id"]

    # Priority summary
    prio_res = client.get("/api/defects/priority-summary")
    assert prio_res.status_code == 200
    assert prio_res.json()["critical"] >= 1

    # Update defect
    patch_res = client.patch(f"/api/defects/{defect_id}", json={"status": "resolved"})
    assert patch_res.status_code == 200
    assert patch_res.json()["status"] == "resolved"


def test_flakiness_endpoints():
    unique_name = f"test_payment_gateway_timeout_{int(datetime.now(timezone.utc).timestamp() * 1000)}"
    tc_res = client.post(
        "/api/flakiness/test-cases",
        json={"name": unique_name, "category": "api", "automation_tool": "pytest"},
    )
    assert tc_res.status_code == 200
    tc_id = tc_res.json()["id"]

    # Record runs
    run1 = client.post("/api/flakiness/runs", json={"test_case_id": tc_id, "status": "passed", "is_flaky": False})
    run2 = client.post("/api/flakiness/runs", json={"test_case_id": tc_id, "status": "failed", "is_flaky": True})
    assert run1.status_code == 200
    assert run2.status_code == 200

    flakiness_res = client.get("/api/flakiness?category=api")
    assert flakiness_res.status_code == 200
    results = [item for item in flakiness_res.json() if item["name"] == unique_name]
    assert len(results) == 1
    assert results[0]["flaky_runs"] == 1


def test_quality_gates_endpoints():
    payload = {
        "name": "API Latency p95 < 200ms",
        "category": "api",
        "gate_type": "automated",
        "stage": "ci",
        "threshold": "200ms",
        "actual_value": "142ms",
        "status": "pass",
        "owner": "qe-platform",
        "build_id": "build-test-200",
    }
    res = client.post("/api/quality-gates", json=payload)
    assert res.status_code == 200
    gate = res.json()
    assert gate["id"] > 0

    summary_res = client.get("/api/quality-gates/summary")
    assert summary_res.status_code == 200
    assert "api" in summary_res.json()


def test_coverage_endpoints():
    payload = {
        "metric_name": "api_endpoint_coverage",
        "category": "api",
        "numerator": 95.0,
        "denominator": 100.0,
        "build_id": "build-test-200",
    }
    res = client.post("/api/coverage", json=payload)
    assert res.status_code == 200
    metric = res.json()
    assert metric["id"] > 0

    summary_res = client.get("/api/coverage/summary")
    assert summary_res.status_code == 200
    assert any(m["metric_name"] == "api_endpoint_coverage" for m in summary_res.json())


def test_metrics_derived_and_dashboard():
    # Defect detection efficiency
    dde_res = client.get("/api/metrics/dde")
    assert dde_res.status_code == 200
    assert "dde_percent" in dde_res.json()

    # Automation DDE
    auto_res = client.get("/api/metrics/automation-dde")
    assert auto_res.status_code == 200
    assert "automation_dde_percent" in auto_res.json()

    # Production leakage
    leakage_res = client.get("/api/metrics/production-leakage")
    assert leakage_res.status_code == 200
    assert "production_leakage_percent" in leakage_res.json()

    # Flaky rate
    flaky_res = client.get("/api/metrics/flaky-rate")
    assert flaky_res.status_code == 200
    assert "flaky_rate_percent" in flaky_res.json()

    # Dashboard snapshot
    dash_res = client.get("/api/metrics/dashboard")
    assert dash_res.status_code == 200
    dash_data = dash_res.json()
    assert "categories" in dash_data
    assert "api" in dash_data["categories"]


def test_ai_insights_endpoint():
    res = client.get("/api/ai/insights")
    assert res.status_code == 200
    data = res.json()
    assert "summary" in data
    assert "recommendations" in data
    assert isinstance(data["recommendations"], list)
    assert "provider" in data
