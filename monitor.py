"""
Collects a ONE-TIME snapshot of:
  - CPU usage (overall + per-core)
  - RAM usage
  - Disk usage
  - Top N processes by CPU and RAM consumption

No background threads — runs once and exits cleanly.
"""

import psutil
from typing import Any
from config import TOP_PROCESS_COUNT


def get_cpu_stats() -> dict[str, Any]:
    """
    Collect CPU usage statistics.

    Returns:
        dict: CPU percent (overall), per-core percentages,
              and logical/physical core counts.
    """
    # interval=1 means psutil samples over 1 second for accuracy
    overall = psutil.cpu_percent(interval=1)
    per_core = psutil.cpu_percent(interval=None, percpu=True)

    return {
        "overall_percent": overall,
        "per_core_percent": per_core,
        "logical_cores": psutil.cpu_count(logical=True),
        "physical_cores": psutil.cpu_count(logical=False),
    }


def get_ram_stats() -> dict[str, Any]:
    """
    Collect RAM (virtual memory) usage statistics.

    Returns:
        dict: Total, used, available RAM in GB and usage percent.
    """
    mem = psutil.virtual_memory()
    gb = 1024 ** 3  # bytes → gigabytes conversion

    return {
        "total_gb": round(mem.total / gb, 2),
        "used_gb": round(mem.used / gb, 2),
        "available_gb": round(mem.available / gb, 2),
        "percent_used": mem.percent,
    }


def get_disk_stats() -> dict[str, Any]:
    """
    Collect disk usage statistics for the primary drive (C: on Windows).

    Returns:
        dict: Total, used, free disk space in GB and usage percent.
    """
    disk = psutil.disk_usage("C:\\")
    gb = 1024 ** 3

    return {
        "total_gb": round(disk.total / gb, 2),
        "used_gb": round(disk.used / gb, 2),
        "free_gb": round(disk.free / gb, 2),
        "percent_used": disk.percent,
    }


def get_top_processes() -> list[dict[str, Any]]:
    """
    Retrieve the top N processes sorted by CPU usage, then RAM usage.

    Skips system processes that can't be queried (PermissionError, etc.).

    Returns:
        list[dict]: Each dict has process name, PID, CPU%, and RAM in MB.
    """
    processes: list[dict[str, Any]] = []

    for proc in psutil.process_iter(["pid", "name", "cpu_percent", "memory_info"]):
        try:
            info = proc.info
            ram_mb = round(info["memory_info"].rss / (1024 ** 2), 2)
            processes.append({
                "pid": info["pid"],
                "name": info["name"],
                "cpu_percent": info["cpu_percent"],
                "ram_mb": ram_mb,
            })
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            # These are normal — some system processes can't be read
            continue

    # Sort by CPU first, then by RAM as a tiebreaker
    processes.sort(key=lambda p: (p["cpu_percent"], p["ram_mb"]), reverse=True)

    return processes[:TOP_PROCESS_COUNT]


def collect_snapshot() -> dict[str, Any]:
    """
    Collect a full system snapshot in one call.

    This is the main function called by other modules.
    It runs ONCE — no loops, no background monitoring.

    Returns:
        dict: Combined CPU, RAM, Disk, and top processes data as JSON-ready dict.
    """
    return {
        "cpu": get_cpu_stats(),
        "ram": get_ram_stats(),
        "disk": get_disk_stats(),
        "top_processes": get_top_processes(),
    }
