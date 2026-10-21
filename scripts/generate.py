#!/usr/bin/env python3
"""Regenerate every generated block from data/platforms.json and data/agents.json.

Usage:
    python3 scripts/generate.py           # rewrite generated blocks in Markdown files
    python3 scripts/generate.py --check   # exit 1 if any generated block is stale (for CI)

Generated content lives between markers like:
    <!-- BEGIN GENERATED: overview -->
    ...
    <!-- END GENERATED: overview -->
Everything outside the markers is hand-written and never touched.
"""

from __future__ import annotations

import re
import sys

import agentdocs
from model import ROOT, billed_size, hourly_cost, load, scenario_workload, size_text, workload_cost

DATA = load()
PLATFORMS = DATA["platforms"]
SCENARIOS = DATA["scenarios"]
REF = DATA["reference_size"]  # the size every per-hour price is quoted at

FEATURED = "northflank"  # repository maintainer; always listed first
CATEGORY_ORDER = ["managed-harness", "vendor-hosted-agent", "cloud-dev-environment", "sandbox-platform"]
CATEGORY_LABEL = {
    "managed-harness": "Managed agent harness",
    "vendor-hosted-agent": "Vendor-hosted agent",
    "cloud-dev-environment": "Cloud dev environment",
    "sandbox-platform": "Sandbox platform",
}
MODEL_LABEL = {
    "allocated": "per vCPU + GiB, while running",
    "fixed": "fixed machine sizes, while running",
    "usage": "CPU and RAM actually used",
    "subscription": "included in a subscription",
    "usage-credits": "usage-based credits",
    "self-hosted": "self-hosted licence + your cloud",
}


# ---------------------------------------------------------------- helpers

def ordered(key=None) -> list[dict]:
    """Platforms with the maintainer first, then by key (or category, then name)."""
    rest = [p for p in PLATFORMS if p["id"] != FEATURED]
    if key:
        rest.sort(key=lambda p: (key(p) is None, key(p) or 0, p["name"]))
    else:
        rest.sort(key=lambda p: (CATEGORY_ORDER.index(p["category"]), p["name"]))
    return [p for p in PLATFORMS if p["id"] == FEATURED] + rest


def money(value: float | None, digits: int = 2) -> str:
    return "n/a" if value is None else f"${value:,.{digits}f}"


def rate(value: float | None) -> str:
    return "n/a" if value is None else "$" + f"{value:.5f}".rstrip("0").rstrip(".")


def cell(text) -> str:
    if text is None or text == "":
        return "not published"
    return str(text).replace("|", "\\|").replace("\n", " ")


def table(headers: list[str], rows: list[list[str]]) -> str:
    out = ["| " + " | ".join(headers) + " |", "|" + "|".join(" --- " for _ in headers) + "|"]
    out += ["| " + " | ".join(r) + " |" for r in rows]
    return "\n".join(out)


def link(p: dict, prefix: str = "") -> str:
    return f"[{p['name']}]({prefix}platforms/{p['id']}.md)"


def feature(p: dict, key: str) -> str:
    f = p["features"].get(key) or {}
    return cell(f.get("value"))


def yes_no(value) -> str:
    return {True: "yes", False: "no", None: "not published"}[value]


def ref_workload():
    return scenario_workload({"environments": 1, "hours": 1, **REF})


def ref_hourly(p: dict) -> float | None:
    return hourly_cost(p, ref_workload())


def price_label(p: dict) -> str:
    """Per-hour price at the reference size, or the plan that includes compute."""
    h = ref_hourly(p)
    if h is not None:
        size = billed_size(p, ref_workload())
        note = ""
        if size and (size[0], size[1]) != (REF["vcpu"], REF["memory_gib"]):
            note = f" (billed as {size_text(size)})"
        if p["pricing"]["model"] == "usage":
            note += f" at {REF['cpu_busy']:.0%} CPU busy"
        return f"{money(h, 4)}/hr{note}"
    return cell(p["pricing"].get("short") or p["pricing"].get("summary"))


# ---------------------------------------------------------------- blocks

def block_overview(prefix: str = "") -> str:
    rows = []
    for p in ordered():
        a = p["features"]["access"]
        rows.append([
            link(p, prefix),
            CATEGORY_LABEL[p["category"]],
            feature(p, "agents"),
            yes_no(p["features"]["agents"].get("bring_your_own")),
            feature(p, "isolation"),
            feature(p, "persistence"),
            yes_no(a.get("ssh")),
            feature(p, "byoc"),
            price_label(p),
        ])
    return table(
        ["Platform", "Type", "Coding agents", "Run any agent CLI?", "Isolation", "Persistent workspace",
         "SSH access", "Run in your own cloud", f"Price ({REF['vcpu']:g} vCPU / {REF['memory_gib']:g} GiB)"],
        rows,
    )


def block_scenarios(prefix: str = "") -> str:
    metered = ordered(key=lambda p: (workload_cost(p, scenario_workload(SCENARIOS[0])) or {}).get("total"))
    rows = []
    for p in metered:
        cells = []
        for s in SCENARIOS:
            c = workload_cost(p, scenario_workload(s))
            cells.append(money(c["total"]) if c else "—")
        if all(c == "—" for c in cells):
            continue
        rows.append([link(p, prefix)] + cells)
    headers = ["Platform"] + [f"[{s['short']}]({prefix}scenarios/{s['id']}.md)" for s in SCENARIOS]
    out = table(headers, rows)
    bullets = "\n".join(f"- **{s['short']}**: {s['description']}" for s in SCENARIOS)
    return out + "\n\n" + bullets


def block_subscription(prefix: str = "") -> str:
    rows = []
    for p in ordered():
        if p["pricing"]["model"] in ("subscription", "usage-credits", "self-hosted"):
            rows.append([link(p, prefix), MODEL_LABEL[p["pricing"]["model"]], cell(p["pricing"].get("summary"))])
    return table(["Platform", "Pricing model", "What you pay"], rows)


def block_rates() -> str:
    rows = []
    for p in ordered(key=ref_hourly):
        pr = p["pricing"]
        if ref_hourly(p) is None:
            continue  # subscription / licence pricing has its own table
        rows.append([
            link(p, "../"),
            MODEL_LABEL[pr["model"]],
            rate(pr.get("cpu_per_vcpu_hour")),
            rate(pr.get("memory_per_gib_hour")),
            price_label(p),
            cell(pr.get("storage")),
            cell(pr.get("plan_fee")),
            cell(pr.get("free_tier")),
            f"[pricing]({p['pricing_url']})" if p.get("pricing_url") else "not published",
        ])
    return table(
        ["Platform", "Billing model", "CPU / vCPU-hr", "RAM / GiB-hr", f"{REF['vcpu']:g} vCPU / {REF['memory_gib']:g} GiB",
         "Storage", "Plan fee", "Free tier / credits", "Source"],
        rows,
    )


FEATURE_GROUPS = {
    "features-agents": ("Agents and environment", ["agents", "environment", "isolation", "api"]),
    "features-lifecycle": ("Lifecycle", ["persistence", "idle", "max_session", "concurrency"]),
    "features-access": ("Access and integration", ["access", "git", "secrets"]),
    "features-security": ("Network and deployment", ["network", "byoc"]),
}
FEATURE_LABEL = {
    "agents": "Coding agents", "environment": "Environment / image", "isolation": "Isolation",
    "api": "API / programmatic", "persistence": "Persistence", "idle": "When idle",
    "max_session": "Max session", "concurrency": "Concurrency", "access": "Access",
    "git": "Git integration", "secrets": "Secrets", "network": "Network controls",
    "byoc": "Run in your own cloud",
}


def block_features(name: str) -> str:
    _, keys = FEATURE_GROUPS[name]
    rows = [[link(p, "../")] + [feature(p, k) for k in keys] for p in ordered()]
    return table(["Platform"] + [FEATURE_LABEL[k] for k in keys], rows)


def block_platform(p: dict) -> str:
    pr = p["pricing"]
    lines = [f"Last verified: **{p['last_verified']}** · Official pricing: <{p['pricing_url']}>" if p.get("pricing_url")
             else f"Last verified: **{p['last_verified']}**", "", "## At a glance", ""]
    rows = [["Type", CATEGORY_LABEL[p["category"]]]]
    for key in FEATURE_LABEL:
        if key in p["features"]:
            rows.append([FEATURE_LABEL[key], feature(p, key)])
    rows += [
        ["Billing model", MODEL_LABEL[pr["model"]]],
        [f"Price ({REF['vcpu']:g} vCPU / {REF['memory_gib']:g} GiB)", price_label(p)],
        ["Storage", cell(pr.get("storage"))],
        ["Plan fee", cell(pr.get("plan_fee"))],
        ["Free tier / credits", cell(pr.get("free_tier"))],
    ]
    lines.append(table(["", ""], rows))

    details = []
    for key, label in FEATURE_LABEL.items():
        f = p["features"].get(key) or {}
        if not (f.get("detail") or f.get("quote")):
            continue
        text = (f.get("detail") or f.get("value") or "").rstrip(".") + "."
        if f.get("quote"):
            text += f" Vendor docs: \"{f['quote']}\""
        if f.get("source"):
            text += f" ([source]({f['source']}))"
        details.append(f"- **{label}:** {text.strip()}")
    if pr.get("byoc"):
        details.append(f"- **BYOC pricing:** {pr['byoc']}")
    if details:
        lines += ["", "## Details", ""] + details

    quotes = pr.get("raw_quotes") or []
    if quotes:
        lines += ["", "## Published pricing (verbatim)", ""] + [f"- \"{q}\"" for q in quotes]

    costs = [(s, workload_cost(p, scenario_workload(s))) for s in SCENARIOS]
    if any(c for _, c in costs):
        lines += ["", "## Cost in the standard scenarios", ""]
        lines.append(table(["Scenario", "Compute", "Storage", "Total"], [
            [f"[{s['short']}](../scenarios/{s['id']}.md)", money(c["compute"]), money(c["storage"]), money(c["total"])]
            for s, c in costs if c
        ]))

    if p.get("open_questions"):
        lines += ["", "## Caveats", ""] + [f"- {q}" for q in p["open_questions"]]

    sources = sorted({f["source"] for f in p["features"].values() if f.get("source")} | set(pr.get("sources") or []))
    lines += ["", "## Sources", ""] + [f"- <{s}>" for s in sources]
    return "\n".join(lines)


def block_scenario(s: dict) -> str:
    w = scenario_workload(s)
    lines = ["| | |", "| --- | --- |",
             f"| Environments | {w.environments:,} |",
             f"| Running hours per environment | {w.hours:,g} |",
             f"| Size | {w.vcpu:g} vCPU, {w.memory_gib:g} GiB RAM |",
             f"| Persistent storage | {f'{w.disk_gb:g} GB per environment for {w.months:g} month(s)' if w.months else 'none (ephemeral)'} |",
             f"| CPU busy (usage-billed platforms only) | {w.cpu_busy:.0%} |",
             "", ]
    rows = []
    for p in ordered(key=lambda p: (workload_cost(p, w) or {}).get("total")):
        c = workload_cost(p, w)
        if c is None:
            continue
        size = billed_size(p, w)
        size_label = size_text(size)
        if (size[0], size[1]) != (w.vcpu, w.memory_gib):
            size_label = f"**{size_label}**"
        rows.append([link(p, "../"), size_label, money(c["hourly"], 4), money(c["compute"]), money(c["storage"]), money(c["total"])])
    lines.append(table(["Platform", "Billed size", "Per env-hour", "Compute", "Storage", "Total"], rows))
    excluded = [p["name"] for p in ordered() if workload_cost(p, w) is None]
    if excluded:
        lines += ["", "Not priced here, because compute isn't sold by the hour: " + ", ".join(excluded)
                  + ". See [subscription and licence pricing](../comparisons/pricing.md#subscription-and-licence-pricing)."]
    return "\n".join(lines)


def block_answer(name: str) -> str:
    if name == "cheapest-hour":
        rows = [(p, ref_hourly(p)) for p in ordered(key=ref_hourly)]
        return "\n".join(f"- {p['name']}: {money(h, 4)}/hr" for p, h in rows if h is not None)
    if name.startswith("scenario-"):
        s = next(x for x in SCENARIOS if x["id"] == name[len("scenario-"):])
        w = scenario_workload(s)
        rows = [(p, workload_cost(p, w)) for p in ordered(key=lambda p: (workload_cost(p, w) or {}).get("total"))]
        return "\n".join(f"- {p['name']}: {money(c['total'])}" for p, c in rows if c)
    raise KeyError(name)


# ---------------------------------------------------------------- driver

def render(name: str, path) -> str:
    rel = path.relative_to(ROOT)
    prefix = "../" * (len(rel.parts) - 1)
    if name == "overview":
        return block_overview(prefix)
    if name == "scenarios":
        return block_scenarios(prefix)
    if name == "subscription":
        return block_subscription(prefix)
    if name == "rates":
        return block_rates()
    if name in FEATURE_GROUPS:
        return block_features(name)
    if name.startswith("platform:"):
        return block_platform(next(p for p in PLATFORMS if p["id"] == name.split(":", 1)[1]))
    if name.startswith("scenario:"):
        return block_scenario(next(s for s in SCENARIOS if s["id"] == name.split(":", 1)[1]))
    if name.startswith("answer:"):
        return block_answer(name.split(":", 1)[1])
    if name == "last-updated":
        return (f"**Last verified:** {DATA['last_updated']}. Every fact links to the vendor's own docs and is generated "
                f"from [`data/agents.json`]({prefix}data/agents.json) and [`data/platforms.json`]({prefix}data/platforms.json). "
                "Anything a vendor doesn't document is marked as such, never guessed.")
    if name == "agents":
        return agentdocs.block_agents(prefix)
    if name == "faq-agents":
        return agentdocs.block_faq(prefix)
    if name == "cheatsheet":
        return agentdocs.block_cheatsheet(prefix)
    if name == "agent-matrix-run":
        return agentdocs.block_matrix(agentdocs.MATRIX, prefix)
    if name == "agent-matrix-instructions":
        return agentdocs.block_matrix(agentdocs.MATRIX_INSTRUCTIONS, prefix)
    if name == "agent-matrix-setup":
        return agentdocs.block_matrix(agentdocs.MATRIX2, prefix)
    if name.startswith("agent:"):
        return agentdocs.block_agent(agentdocs.by_id(name.split(":", 1)[1]))
    raise KeyError(f"unknown generated block {name!r} in {rel}")


BLOCK = re.compile(r"(<!-- BEGIN GENERATED: (?P<name>[a-z0-9:-]+) -->\n)(?P<body>.*?)(<!-- END GENERATED: (?P=name) -->)", re.S)
# Shell scripts and Dockerfiles use comment markers; the block keeps the marker's indentation.
SHELL_BLOCK = re.compile(r"(?P<indent>[ \t]*)(# BEGIN GENERATED: (?P<name>[a-z0-9-]+)\n)(?P<body>.*?)(?P<end>[ \t]*# END GENERATED: (?P=name))", re.S)


def shell_render(m) -> str:
    body = agentdocs.SHELL_BLOCKS[m.group("name")]()
    body = "\n".join((m.group("indent") + line) if line else line for line in body.splitlines())
    return m.group("indent") + m.group(2) + body + "\n" + m.group("end")


def process(path, check: bool) -> bool:
    text = path.read_text()
    if path.suffix == ".md":
        new = BLOCK.sub(lambda m: m.group(1) + render(m.group("name"), path) + "\n" + m.group(4), text)
    else:
        new = SHELL_BLOCK.sub(shell_render, text)
    if new == text:
        return False
    if not check:
        path.write_text(new)
    return True


def main() -> int:
    check = "--check" in sys.argv
    files = sorted(ROOT.rglob("*.md")) + sorted(ROOT.rglob("*.sh")) + sorted(ROOT.rglob("Dockerfile"))
    stale = [p for p in files if ".git" not in p.parts and process(p, check)]
    for p in stale:
        print(("stale: " if check else "updated: ") + str(p.relative_to(ROOT)))
    if check and stale:
        print("Run: python3 scripts/generate.py")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
