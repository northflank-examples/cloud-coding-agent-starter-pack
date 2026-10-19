#!/usr/bin/env python3
"""Estimate the infrastructure cost of running coding agents on every platform.

Example:
    python3 scripts/estimate.py --environments 10 --hours 176 --vcpu 2 --memory 4 --disk 20 --months 1
"""

from __future__ import annotations

import argparse

from model import Workload, billed_size, load, size_text, workload_cost


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--environments", type=int, default=1, help="number of agent environments (default 1)")
    ap.add_argument("--hours", type=float, required=True, help="running hours per environment")
    ap.add_argument("--vcpu", type=float, default=2)
    ap.add_argument("--memory", type=float, default=4, help="GiB of RAM")
    ap.add_argument("--disk", type=float, default=0, help="persistent workspace GB per environment")
    ap.add_argument("--months", type=float, default=0, help="months the persistent storage is kept")
    ap.add_argument("--cpu-busy", type=float, default=0.25, help="CPU utilisation, for usage-billed platforms")
    a = ap.parse_args()

    w = Workload(a.environments, a.hours, a.vcpu, a.memory, a.disk, a.months, a.cpu_busy)
    data = load()
    rows, other = [], []
    for p in data["platforms"]:
        c = workload_cost(p, w)
        if c is None:
            other.append(p)
            continue
        size = billed_size(p, w)
        rows.append((c["total"], p["name"], size_text(size), c))

    print(f"{w.environments} × {w.hours:g} h at {w.vcpu:g} vCPU / {w.memory_gib:g} GiB"
          + (f", {w.disk_gb:g} GB storage for {w.months:g} mo" if w.months else "") + "\n")
    print(f"{'Platform':<28}{'Billed size':<28}{'Per hour':>10}{'Compute':>12}{'Storage':>10}{'Total':>12}")
    for total, name, size, c in sorted(rows):
        print(f"{name:<28}{size:<28}{c['hourly']:>10.4f}{c['compute']:>12,.2f}{c['storage']:>10,.2f}{total:>12,.2f}")
    if other:
        print("\nNot metered per hour (subscription, credits or self-hosted):")
        for p in other:
            print(f"  {p['name']}: {p['pricing'].get('summary')}")
    print(f"\nList prices as of {data['last_updated']}. Excludes credits, plan fees, egress and taxes.")


if __name__ == "__main__":
    main()
