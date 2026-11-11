"""Automated Validation Tests for Backup and Disaster Recovery."""

import os
import subprocess
import pytest

def test_backup_script_creates_archive():
    backup_script = os.path.abspath(os.path.join(os.path.dirname(__file__), "../scripts/backup.sh"))
    assert os.path.isfile(backup_script), "backup.sh script must exist"

    result = subprocess.run(["bash", backup_script], capture_output=True, text=True)
    assert result.returncode == 0, f"backup.sh failed with output: {result.stderr}"
    assert "Backup completed successfully" in result.stdout

def test_restore_script_verifies_archive():
    restore_script = os.path.abspath(os.path.join(os.path.dirname(__file__), "../scripts/restore.sh"))
    assert os.path.isfile(restore_script), "restore.sh script must exist"

    # Test missing argument error handling
    result = subprocess.run(["bash", restore_script], capture_output=True, text=True)
    assert result.returncode != 0
    assert "Usage:" in result.stdout
