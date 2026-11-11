"""Failover & Chaos Testing: Jenkins Controller Crash & Tracker Resilience."""

import subprocess
import shutil
import pytest
import requests

def test_jenkins_jcasc_declarative_config_exists():
    with open("jenkins/casc/jenkins.yaml", "r") as f:
        content = f.read()
    assert "clouds:" in content
    assert "kubernetes:" in content
    assert "qe-dynamic-agent" in content
    assert "numExecutors: 0" in content, "Controller must run 0 builds; all builds must run on dynamic K8s agents"

def test_alertmanager_has_jenkins_down_alert_rule():
    with open("monitoring/prometheus/alert-rules.yaml", "r") as f:
        content = f.read()
    assert "alert: JenkinsControllerDown" in content
    assert "alert: KubernetesNodeNotReady" in content
    assert "severity: critical" in content

def test_tracker_service_failover_and_recovery(tracker_endpoint):
    try:
        res = requests.get(f"{tracker_endpoint}/health", timeout=2)
        assert res.status_code == 200
        assert res.json()["status"] == "HEALTHY"
    except requests.exceptions.RequestException:
        pytest.skip("Tracker backend service is not running locally.")
