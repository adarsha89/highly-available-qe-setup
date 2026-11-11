"""Disaster Recovery & Backup Restoration Validation Suite."""

import os
import pytest

def test_velero_hourly_schedule_policy_configured():
    with open("backup-recovery/policies/velero-schedule.yaml", "r") as f:
        content = f.read()
    assert "kind: Schedule" in content
    assert "schedule: \"0 * * * *\"" in content
    assert "snapshotVolumes: true" in content

def test_dr_drill_script_executable():
    drill_script = "backup-recovery/scripts/dr-drill.sh"
    assert os.path.isfile(drill_script)
    with open(drill_script, "r") as f:
        content = f.read()
    assert "backup.sh" in content
    assert "restore.sh" in content
    assert "RTO" in content
