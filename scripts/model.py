"""Cost model for cloud coding agent platforms. No dependencies.

Every number comes from data/platforms.json. See methodology.md for the rules.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA_FILE = ROOT / "data" / "platforms.json"
HOURS_PER_MONTH = 730

# Pricing models that produce a per-hour compute price.
METERED = {"allocated", "usage", "fixed"}


def load() -> dict:
    with DATA_FILE.open() as f:
        return json.load(f)


@dataclass(frozen=True)
class Workload:
    environments: int          # how many agent environments
    hours: float               # billed running hours per environment
    vcpu: float = 2
    memory_gib: float = 4
    disk_gb: float = 0         # persistent workspace storage per environment
    months: float = 0          # months the persistent storage is kept (0 = ephemeral)
    cpu_busy: float = 0.25     # fraction of time CPU is busy (usage-billed platforms only)


def billed_size(p: dict, w: Workload) -> tuple[float, float | None, float | None] | None:
    """(vcpu, memory_gib or None if unpublished, fixed hourly price or None) billed for this workload."""
    pricing = p["pricing"]
    if pricing["model"] not in METERED:
        return None
    sizes = pricing.get("fixed_sizes") or []
    if pricing["model"] == "fixed" or sizes:
        # memory_gib None = the vendor sells by core and doesn't publish RAM for the size
        fits = [s for s in sizes if s["vcpu"] >= w.vcpu and (s["memory_gib"] is None or s["memory_gib"] >= w.memory_gib)]
        if not fits:
            return None
        best = min(fits, key=lambda s: (_size_hourly(pricing, s), s["vcpu"], s["memory_gib"] or 0))
        return best["vcpu"], best["memory_gib"], best.get("hourly")
    return w.vcpu, w.memory_gib, None


def _size_hourly(pricing: dict, size: dict) -> float:
    if size.get("hourly") is not None:
        return size["hourly"]
    return size["vcpu"] * pricing["cpu_per_vcpu_hour"] + size["memory_gib"] * pricing["memory_per_gib_hour"]


def hourly_cost(p: dict, w: Workload) -> float | None:
    """Compute price per environment-hour, or None if the platform isn't metered."""
    size = billed_size(p, w)
    if size is None:
        return None
    vcpu, mem, fixed = size
    if fixed is not None:
        return fixed
    pricing = p["pricing"]
    cpu = vcpu * pricing["cpu_per_vcpu_hour"]
    if pricing["model"] == "usage":
        cpu *= w.cpu_busy
    return cpu + mem * pricing["memory_per_gib_hour"]


def storage_cost(p: dict, w: Workload) -> float:
    """Persistent workspace storage for the whole workload.

    storage_per_gb_month is charged for every month the workspace is kept;
    storage_per_gb_hour_running is an extra charge while the environment runs (Sprites "hot" storage).
    """
    pricing = p["pricing"]
    if not w.disk_gb or not w.months:
        return 0.0
    billable = max(0.0, w.disk_gb - (pricing.get("storage_free_gb") or 0))
    kept = billable * (pricing.get("storage_per_gb_month") or 0) * w.months
    running = billable * (pricing.get("storage_per_gb_hour_running") or 0) * w.hours
    return w.environments * (kept + running)


def workload_cost(p: dict, w: Workload) -> dict | None:
    hourly = hourly_cost(p, w)
    if hourly is None:
        return None
    compute = w.environments * w.hours * hourly
    storage = storage_cost(p, w)
    return {"hourly": hourly, "compute": compute, "storage": storage, "total": compute + storage}


def scenario_workload(s: dict) -> Workload:
    return Workload(
        environments=s["environments"],
        hours=s["hours"],
        vcpu=s["vcpu"],
        memory_gib=s["memory_gib"],
        disk_gb=s.get("disk_gb", 0),
        months=s.get("months", 0),
        cpu_busy=s.get("cpu_busy", 0.25),
    )


def size_text(size: tuple) -> str:
    vcpu, mem = size[0], size[1]
    return f"{vcpu:g} vCPU / " + (f"{mem:g} GiB" if mem is not None else "RAM not published")
