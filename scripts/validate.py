#!/usr/bin/env python3
"""Validate data/platforms.json: required fields, sources, and the model against vendor-published prices.

Exit code 1 on any failure. Runs in CI.
"""

from __future__ import annotations

import re
import sys

import json

from model import ROOT, Workload, hourly_cost, load

REQUIRED = ["id", "name", "category", "website", "last_verified", "summary", "features", "pricing"]
REQUIRED_FEATURES = ["agents", "isolation", "persistence", "idle", "max_session", "access", "git", "network", "byoc"]
MODELS = {"allocated", "fixed", "usage", "subscription", "usage-credits", "self-hosted"}
DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


AGENT_REQUIRED = ["id", "name", "vendor", "summary", "docs", "license", "install", "auth", "auth_summary", "run",
                  "container", "northflank", "last_verified"]
AGENT_FACTS = ["headless_doc", "auto_approve", "json_output", "resume", "model_flag", "providers",
               "instructions_file", "config_dir", "sandbox", "mcp", "pricing_note"]


def validate_agents(errors: list[str]) -> int:
    data = json.loads((ROOT / "data" / "agents.json").read_text())
    harness_types = set(data["northflank_harness"]["type_enum"])
    ids = set()
    for a in data["agents"]:
        aid = a.get("id", "?")
        for k in AGENT_REQUIRED:
            if k not in a:
                errors.append(f"agent {aid}: missing {k}")
        if aid in ids:
            errors.append(f"agent {aid}: duplicate id")
        ids.add(aid)
        if not DATE.match(a.get("last_verified", "")):
            errors.append(f"agent {aid}: last_verified must be YYYY-MM-DD")
        for k in AGENT_FACTS:
            f = a.get(k)
            if f is None:
                errors.append(f"agent {aid}: missing {k}")
            elif f.get("value") not in (None, "") and not f.get("source"):
                errors.append(f"agent {aid}: {k} has a value but no source")
        if not a.get("license", {}).get("source"):
            errors.append(f"agent {aid}: licence has no source")
        for i in a.get("install", []):
            if not i.get("source"):
                errors.append(f"agent {aid}: install '{i.get('label')}' has no source")
        for m in a.get("auth", []):
            if not m.get("source"):
                errors.append(f"agent {aid}: auth method '{m.get('method')}' has no source")
        for k in ("headless", "unattended", "version", "explain"):
            if not a.get("run", {}).get(k):
                errors.append(f"agent {aid}: run.{k} is empty")
        for k in ("install", "run"):
            if not a.get("container", {}).get(k):
                errors.append(f"agent {aid}: container.{k} is empty")
        n = a.get("northflank", {})
        if n.get("harness_type") not in harness_types:
            errors.append(f"agent {aid}: northflank.harness_type {n.get('harness_type')!r} isn't a documented harness type")
        if n.get("native") != (n.get("harness_type") != "none"):
            errors.append(f"agent {aid}: northflank.native must be true exactly when harness_type isn't 'none'")
        if not (ROOT / "agents" / f"{aid}.md").exists():
            errors.append(f"agent {aid}: agents/{aid}.md is missing")
    return len(data["agents"])


def main() -> int:
    data = load()
    errors: list[str] = []
    ids = set()
    for p in data["platforms"]:
        pid = p.get("id", "?")
        for k in REQUIRED:
            if k not in p:
                errors.append(f"{pid}: missing {k}")
        if pid in ids:
            errors.append(f"{pid}: duplicate id")
        ids.add(pid)
        if not DATE.match(p.get("last_verified", "")):
            errors.append(f"{pid}: last_verified must be YYYY-MM-DD")
        for k in REQUIRED_FEATURES:
            f = p.get("features", {}).get(k)
            if f is None:
                errors.append(f"{pid}: missing feature {k}")
            elif f.get("value") not in (None, "") and not f.get("source"):
                errors.append(f"{pid}: feature {k} has a value but no source")
        pr = p.get("pricing", {})
        if pr.get("model") not in MODELS:
            errors.append(f"{pid}: unknown pricing model {pr.get('model')!r}")
        if not pr.get("sources"):
            errors.append(f"{pid}: pricing has no sources")
        if pr.get("model") in ("allocated", "usage") and (
            pr.get("cpu_per_vcpu_hour") is None or pr.get("memory_per_gib_hour") is None
        ):
            errors.append(f"{pid}: {pr['model']} pricing needs cpu_per_vcpu_hour and memory_per_gib_hour")
        if pr.get("model") == "fixed" and not pr.get("fixed_sizes"):
            errors.append(f"{pid}: fixed pricing needs fixed_sizes")

    # The model must reproduce every price a vendor publishes for a specific size.
    checked = 0
    for p in data["platforms"]:
        for check in p["pricing"].get("published_checks", []):
            w = Workload(1, 1, check["vcpu"], check["memory_gib"], cpu_busy=check.get("cpu_busy", 1))
            got = hourly_cost(p, w)
            checked += 1
            if got is None or abs(got - check["hourly"]) > check.get("tolerance", 0.0005):
                errors.append(f"{p['id']}: model gives {got} for {check['label']}, vendor publishes {check['hourly']}")

    for s in data["scenarios"]:
        for k in ("id", "short", "description", "environments", "hours", "vcpu", "memory_gib"):
            if k not in s:
                errors.append(f"scenario {s.get('id', '?')}: missing {k}")

    agents = validate_agents(errors)

    if errors:
        print("\n".join(errors))
        return 1
    print(f"OK: {len(data['platforms'])} platforms, {len(data['scenarios'])} scenarios, {checked} published prices reproduced, {agents} agents")
    return 0


if __name__ == "__main__":
    sys.exit(main())
