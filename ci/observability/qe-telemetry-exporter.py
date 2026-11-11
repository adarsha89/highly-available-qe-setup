#!/usr/bin/env python3
"""Telemetry Exporter for Downstream QE Repositories.

Sends execution results to Central Automation Tracker and Prometheus.
"""

import argparse
import json
import sys
import urllib.request
import urllib.error

def export_telemetry(tracker_url, suite, status, duration, total=0, passed=0, failed=0):
    endpoint = f"{tracker_url.rstrip('/')}/api/v1/runs"
    payload = {
        "suite": suite,
        "environment": "ci",
        "status": status,
        "total_tests": total,
        "passed_tests": passed,
        "failed_tests": failed,
        "duration_seconds": float(duration),
        "metadata": {"source": "qe-ci-pipeline"}
    }
    
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        endpoint,
        data=data,
        headers={"Content-Type": "application/json"}
    )
    
    try:
        with urllib.request.urlopen(req, timeout=5) as response:
            if response.status in [200, 201]:
                print(f"[Telemetry] Successfully reported run to {endpoint}")
                return True
    except Exception as e:
        print(f"[Telemetry Warning] Could not reach Automation Tracker ({e}); execution continued.")
        return False

def main():
    parser = argparse.ArgumentParser(description="Export QE Test Execution Telemetry")
    parser.add_argument("--tracker-url", default="http://localhost:8000", help="Central Tracker API URL")
    parser.add_argument("--suite", required=True, help="Test suite identifier")
    parser.add_argument("--status", default="PASSED", help="Execution status (PASSED/FAILED)")
    parser.add_argument("--duration", default="0.0", help="Execution duration in seconds")
    parser.add_argument("--total", type=int, default=1, help="Total test count")
    parser.add_argument("--passed", type=int, default=1, help="Passed test count")
    parser.add_argument("--failed", type=int, default=0, help="Failed test count")

    args = parser.parse_args()
    export_telemetry(args.tracker_url, args.suite, args.status, args.duration, args.total, args.passed, args.failed)

if __name__ == "__main__":
    main()
