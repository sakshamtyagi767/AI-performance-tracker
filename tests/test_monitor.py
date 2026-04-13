"""
tests/test_monitor.py
---------------------
Unit tests for the monitor.py module.

Tests verify:
  - All functions return the correct data types.
  - CPU percent is a valid float in [0, 100].
  - RAM total is positive.
  - Disk usage values are consistent (used + free ≈ total).
  - Top processes list has correct length and structure.
  - JSON payload structure is valid before sending to AI.
"""

import sys
import os

# Add parent directory to path so we can import monitor from tests/
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
import monitor
from monitor import get_cpu_stats, get_ram_stats, get_disk_stats, get_top_processes, collect_snapshot


class TestCpuStats:
    """Unit tests for get_cpu_stats()"""

    def test_returns_dict(self):
        """Should return a dictionary."""
        result = get_cpu_stats()
        assert isinstance(result, dict)

    def test_has_required_keys(self):
        """Dict must have all required keys."""
        result = get_cpu_stats()
        required = {"overall_percent", "per_core_percent", "logical_cores", "physical_cores"}
        assert required.issubset(result.keys())

    def test_cpu_percent_valid_range(self):
        """CPU overall percent must be between 0 and 100."""
        result = get_cpu_stats()
        assert 0.0 <= result["overall_percent"] <= 100.0

    def test_cpu_per_core_is_list(self):
        """Per-core data should be a list of floats."""
        result = get_cpu_stats()
        assert isinstance(result["per_core_percent"], list)
        for val in result["per_core_percent"]:
            assert isinstance(val, float | int)
            assert 0.0 <= val <= 100.0

    def test_core_counts_positive(self):
        """Core counts must be positive integers."""
        result = get_cpu_stats()
        assert result["logical_cores"] > 0
        assert result["physical_cores"] > 0


class TestRamStats:
    """Unit tests for get_ram_stats()"""

    def test_returns_dict(self):
        result = get_ram_stats()
        assert isinstance(result, dict)

    def test_has_required_keys(self):
        result = get_ram_stats()
        required = {"total_gb", "used_gb", "available_gb", "percent_used"}
        assert required.issubset(result.keys())

    def test_total_ram_positive(self):
        """Total RAM must be greater than zero."""
        result = get_ram_stats()
        assert result["total_gb"] > 0

    def test_used_does_not_exceed_total(self):
        """Used RAM cannot exceed total RAM."""
        result = get_ram_stats()
        assert result["used_gb"] <= result["total_gb"]

    def test_percent_valid_range(self):
        """RAM percent must be 0–100."""
        result = get_ram_stats()
        assert 0.0 <= result["percent_used"] <= 100.0


class TestDiskStats:
    """Unit tests for get_disk_stats()"""

    def test_returns_dict(self):
        result = get_disk_stats()
        assert isinstance(result, dict)

    def test_has_required_keys(self):
        result = get_disk_stats()
        required = {"total_gb", "used_gb", "free_gb", "percent_used"}
        assert required.issubset(result.keys())

    def test_disk_total_positive(self):
        """Disk total must be positive."""
        result = get_disk_stats()
        assert result["total_gb"] > 0

    def test_used_plus_free_approx_total(self):
        """Used + Free should approximately equal Total (within 1 GB rounding)."""
        result = get_disk_stats()
        approx_total = result["used_gb"] + result["free_gb"]
        assert abs(approx_total - result["total_gb"]) < 1.0


class TestTopProcesses:
    """Unit tests for get_top_processes()"""

    def test_returns_list(self):
        result = get_top_processes()
        assert isinstance(result, list)

    def test_max_length_is_10(self):
        """Should return at most 10 processes."""
        result = get_top_processes()
        assert len(result) <= 10

    def test_each_process_has_required_keys(self):
        """Each process dict must contain the required fields."""
        result = get_top_processes()
        required = {"pid", "name", "cpu_percent", "ram_mb"}
        for proc in result:
            assert required.issubset(proc.keys()), f"Process missing keys: {proc}"

    def test_process_cpu_valid_range(self):
        """CPU percent per process must be >= 0."""
        result = get_top_processes()
        for proc in result:
            assert proc["cpu_percent"] >= 0

    def test_process_ram_positive(self):
        """RAM usage in MB must be >= 0."""
        result = get_top_processes()
        for proc in result:
            assert proc["ram_mb"] >= 0


class TestCollectSnapshot:
    """Integration-level tests for the full snapshot."""

    def test_snapshot_structure(self):
        """Full snapshot must contain cpu, ram, disk, top_processes."""
        result = collect_snapshot()
        assert "cpu" in result
        assert "ram" in result
        assert "disk" in result
        assert "top_processes" in result

    def test_snapshot_is_json_serializable(self):
        """The snapshot dict must be JSON-serializable (required for API call)."""
        import json
        result = collect_snapshot()
        serialized = json.dumps(result)
        assert len(serialized) > 0
