"""Integration Tests for Azure / Azurite Local Storage Emulator."""

import pytest
import requests

AZURITE_BLOB_ENDPOINT = "http://localhost:10000"

def test_azurite_health():
    try:
        res = requests.get(f"{AZURITE_BLOB_ENDPOINT}/", timeout=2)
        # Azurite returns 400 for root GET without account query, confirming it is online
        assert res.status_code in [200, 400]
    except requests.exceptions.RequestException:
        pytest.skip("Azurite local emulator is not running.")
