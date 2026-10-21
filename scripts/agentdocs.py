"""Generated blocks built from data/agents.json: agent guides, the agent matrix and the cheat sheet.

Imported by generate.py. Shell and Dockerfile blocks (install lines, run-task.sh commands) are
generated from the same data, so the docs and the runnable examples always agree.
"""

from __future__ import annotations

import json

from model import ROOT

AGENTS_DATA = json.loads((ROOT / "data" / "agents.json").read_text())
AGENTS = AGENTS_DATA["agents"]
NF = AGENTS_DATA["northflank_harness"]


def by_id(agent_id: str) -> dict:
    return next(a for a in AGENTS if a["id"] == agent_id)


def cell(text) -> str:
    if text is None or text == "":
        return "not documented"
    return str(text).replace("|", "\\|").replace("\n", " ")


def code(text) -> str:
    """Inline code that survives a Markdown table cell."""
    if not text:
        return "not documented"
    return "`" + str(text).replace("|", "\\|") + "`"


def table(headers: list[str], rows: list[list[str]]) -> str:
    out = ["| " + " | ".join(headers) + " |", "|" + "|".join(" --- " for _ in headers) + "|"]
    out += ["| " + " | ".join(r) + " |" for r in rows]
    return "\n".join(out)


def val(a: dict, key: str):
    f = a.get(key)
    return f.get("value") if isinstance(f, dict) else f


def link(a: dict, prefix: str = "") -> str:
    return f"[{a['name']}]({prefix}agents/{a['id']}.md)"


def licence(a: dict) -> str:
    lic = a["license"]
    return f"{lic['value']} (open source)" if lic.get("open_source") else lic["value"]


def nf_support(a: dict) -> str:
    n = a["northflank"]
    if n["native"]:
        return "built in"
    return "install in an empty sandbox"


def anchor(heading: str) -> str:
    """GitHub's anchor for a Markdown heading."""
    keep = "".join(c for c in heading.lower() if c.isalnum() or c in " -")
    return keep.replace(" ", "-")


def nf_heading(a: dict) -> str:
    return f"Option 1: Run {a['name']} on Northflank Cloud Harness"


def nf_link(a: dict, prefix: str = "") -> str:
    """The Northflank column, linking to that agent's Northflank section."""
    return f"[{nf_support(a)}]({prefix}agents/{a['id']}.md#{anchor(nf_heading(a))})"


def launch_auth(a: dict) -> str:
    """The launch.sh credential arguments for an agent."""
    n = a["northflank"]
    if n["native"] and "apiKey" in n["api_auth"]:
        return "AGENT_API_KEY=..."
    env = a["auth"][0]["env"] if a["auth"] and a["auth"][0].get("env") else []
    names = [e for e in env if not e.startswith("AWS_")][:1] or env[:1]
    if a["id"] == "goose":
        names = ["ANTHROPIC_API_KEY", "GOOSE_PROVIDER", "GOOSE_MODEL"]
    return f'AGENT_ENV="{" ".join(names)}"' if names else ""


def auth_env(a: dict, limit: int = 5) -> str:
    envs = []
    for m in a["auth"]:
        for e in m.get("env") or []:
            if e not in envs:
                envs.append(e)
    if not envs:
        return "not documented"
    shown = ", ".join(f"`{e}`" for e in envs[:limit])
    return shown + (f" and {len(envs) - limit} more" if len(envs) > limit else "")


def ordered() -> list[dict]:
    """Agents Northflank runs natively first (in data order), then the rest alphabetically."""
    native = [a for a in AGENTS if a["northflank"]["native"]]
    other = sorted((a for a in AGENTS if not a["northflank"]["native"]), key=lambda a: a["name"].lower())
    return native + other


# ---------------------------------------------------------------- README / index blocks

def block_agents(prefix: str = "") -> str:
    rows = []
    for a in ordered():
        rows.append([
            link(a, prefix),
            cell(a["vendor"]),
            licence(a),
            cell(val(a, "providers_short")),
            code(a["run"]["headless"]),
            a["auth_summary"],
            nf_link(a, prefix),
        ])
    return table(["Agent", "Made by", "Licence", "Models", "Headless command", "Auth on a server", "On Northflank"], rows)


def block_cheatsheet(prefix: str = "") -> str:
    out = []
    for a in ordered():
        out.append(f"# {a['name']}")
        out.append(a["run"]["unattended"])
    return "```bash\n" + "\n".join(out) + "\n```"


MATRIX = [
    ("Install", lambda a: code(a["install"][0]["command"])),
    ("Headless command", lambda a: code(a["run"]["headless"])),
    ("Skip permission prompts", lambda a: cell(val(a, "auto_approve"))),
    ("JSON output", lambda a: cell(val(a, "json_output"))),
    ("Resume a session", lambda a: cell(val(a, "resume"))),
    ("Choose a model", lambda a: cell(val(a, "model_flag"))),
    ("Server / API mode", lambda a: cell(val(a, "server_mode")) if a.get("server_mode") else "none documented"),
]
MATRIX2 = [
    ("Licence", licence),
    ("Models", lambda a: cell(val(a, "providers"))),
    ("Auth on a server", lambda a: a["auth_summary"]),
    ("Instructions file", lambda a: cell(val(a, "instructions_file"))),
    ("Config and credentials", lambda a: cell(val(a, "config_dir"))),
    ("Built-in sandbox", lambda a: cell(val(a, "sandbox"))),
    ("MCP", lambda a: cell(val(a, "mcp"))),
]

MATRIX_INSTRUCTIONS = [("Instructions file", lambda a: cell(val(a, "instructions_file")))]


def block_matrix(cols, prefix: str) -> str:
    return table(["Agent"] + [c for c, _ in cols], [[link(a, prefix)] + [f(a) for _, f in cols] for a in ordered()])


def block_faq(prefix: str = "") -> str:
    out = []
    for a in ordered():
        n = a["northflank"]
        where = (f"On Northflank Cloud Harness, choose **{n['ui_label']}** when you create a harness and it's preinstalled."
                 if n["native"] else
                 f"On Northflank Cloud Harness, create an **Empty sandbox** harness and install it with `install-agents.sh {a['id']}`.")
        out += [f"### How do I run {a['name']} in the cloud?", "",
                f"Install it with `{a['install'][0]['command']}`, authenticate with {a['auth_summary']}, "
                "then run a task headlessly with no prompts:", "",
                "```bash", a["run"]["unattended"], "```", "",
                f"{where} Full guide: [{a['name']} in the cloud]({prefix}agents/{a['id']}.md).", ""]
    return "\n".join(out).rstrip()


# ---------------------------------------------------------------- per-agent guide

def cite(f: dict | None) -> str:
    if not f:
        return ""
    out = ""
    if f.get("quote"):
        out += f" Docs: \"{f['quote']}\""
    if f.get("source"):
        out += f" ([source]({f['source']}))"
    return out


def block_agent(a: dict) -> str:
    n = a["northflank"]
    L = [f"Last verified: **{a['last_verified']}** · Docs: <{a['docs']}>"
         + (f" · Source: <{a['repo']}>" if a.get("repo") else ""), ""]

    L += ["## At a glance", ""]
    rows = [
        ["Made by", cell(a["vendor"])],
        ["Licence", licence(a)],
        ["Models", cell(val(a, "providers"))],
        ["Headless command", code(a["run"]["headless"])],
        ["Skip permission prompts", cell(val(a, "auto_approve"))],
        ["JSON output", cell(val(a, "json_output"))],
        ["Resume a session", cell(val(a, "resume"))],
        ["Choose a model", cell(val(a, "model_flag"))],
        ["Auth on a server", a["auth_summary"]],
        ["Instructions file", cell(val(a, "instructions_file"))],
        ["Config and credentials", cell(val(a, "config_dir"))],
        ["Built-in sandbox", cell(val(a, "sandbox"))],
        ["MCP", cell(val(a, "mcp"))],
    ]
    if a.get("server_mode"):
        rows.append(["Server / API mode", cell(val(a, "server_mode"))])
    rows += [["Northflank Cloud Harness", nf_support(a)], ["Billing", cell(val(a, "pricing_note"))]]
    L.append(table(["", ""], rows))

    # 1. Northflank
    L += ["", f"## {nf_heading(a)}", ""]
    if n["native"]:
        L += [
            f"{a['name']} is one of the agents Cloud Harness sets up for you: each harness is an isolated microVM "
            f"with {a['name']} preinstalled, your repository cloned, a persistent workspace, a web "
            "terminal and SSH access.",
            "",
            "1. In [Northflank](https://app.northflank.com), open a project → **Harnesses** → **Create harness**.",
            f"2. Choose **{n['ui_label']}** as the agent, then pick Northflank's cloud or your own cloud account.",
            f"3. Authentication: {n['auth']}.",
            "4. Select the repository and branch, then **Create harness**. The terminal opens with the agent ready.",
            "",
            "To start one harness per task from a script instead, use "
            f"[`launch.sh`](../examples/northflank-parallel-harnesses/README.md) with `AGENT={a['id']}`:",
            "",
            "```bash",
            " ".join(x for x in (f"AGENT={a['id']}", launch_auth(a), "NF_PROJECT=my-project") if x) + " \\",
            "REPO_URL=https://github.com/your-org/your-repo \\",
            "  ./launch.sh tasks.txt",
            "```",
        ]
    else:
        L += [
            f"Cloud Harness doesn't preinstall {a['name']}, but its **Empty sandbox** option gives you the same isolated "
            "microVM, persistent workspace, terminal and SSH access with no agent set up. "
            f"Install {a['name']} once and it stays installed across pauses:",
            "",
            "1. **Harnesses** → **Create harness** → choose **Empty sandbox**, select your repository, and create it.",
            f"2. Under **Environment**, add the agent's credentials ({a['auth_summary']}) as runtime variables, then click **Update & restart**.",
            f"3. In the harness terminal, run the install command from [step 1 below](#1-install), then run "
            f"{a['name']} as in [step 3](#3-run-a-task-headlessly).",
            "",
            "Install into the home directory (the persistent volume) rather than system directories, so the "
            "agent survives restarts. [`install-agents.sh`](../examples/cloud-agent-runner/install-agents.sh) "
            f"does this for you: `bash install-agents.sh {a['id']}`.",
            "",
            "To start one empty-sandbox harness per task from a script, with the installer and the task already in "
            f"the workspace, use [`launch.sh`](../examples/northflank-parallel-harnesses/README.md):",
            "",
            "```bash",
            " ".join(x for x in (f"AGENT={a['id']}", launch_auth(a), "NF_PROJECT=my-project") if x) + " \\",
            "REPO_URL=https://github.com/your-org/your-repo \\",
            "  ./launch.sh tasks.txt",
            "```",
        ]
    L += ["", "Pause the harness when you're done: compute stops and the workspace is kept. "
          "See the [Cloud Harness tutorial](../tutorials/northflank-cloud-harness/README.md)."]

    # 2. Any Linux machine
    L += ["", f"## Option 2: Run {a['name']} on any Linux VM or container", "", "### 1. Install", ""]
    for i in a["install"]:
        L.append(f"**{i['label']}**" + (f" (requires {i['requirements']})" if i.get("requirements") else "") + ":")
        L += ["", "```bash", i["command"], "```", ""]
    srcs = sorted({i["source"] for i in a["install"] if i.get("source")})
    L.append(f"Check it worked: `{a['run']['version']}`. Install docs: " + ", ".join(f"<{s}>" for s in srcs) + ".")

    L += ["", "### 2. Authenticate without a browser", "",
          "Cloud machines usually can't open a browser login, so use one of these:", ""]
    L.append(table(["Method", "Environment variables", "How"], [
        [cell(m["method"]), ", ".join(f"`{e}`" for e in m.get("env") or []) or "—",
         cell(m["how"]) + (f" ([source]({m['source']}))" if m.get("source") else "")]
        for m in a["auth"]
    ]))

    L += ["", "### 3. Run a task headlessly", "",
          "Work on a branch, let the agent finish without prompts, then commit and push for review:", "",
          "```bash", "git switch -c agent/my-task", a["run"]["unattended"],
          "git add -A && git commit -m \"agent: my task\" && git push -u origin HEAD", "```", ""]
    L.append(table(["Part", "What it does"], [[code(p), cell(m)] for p, m in a["run"]["explain"]]))
    for label, key in [("Headless mode", "headless_doc"), ("Permissions", "auto_approve")]:
        f = a.get(key)
        if f and (f.get("quote") or f.get("notes")):
            text = (f.get("notes") or f.get("value") or "").rstrip(".")
            L.append(f"\n- **{label}:** {text}.{cite(f)}")

    L += ["", "### 4. Or use this repo's container", "",
          f"[`examples/cloud-agent-runner`](../examples/cloud-agent-runner/README.md) builds an image with "
          f"{a['name']} (and any other agents you list) and runs one task per container:", "",
          "```bash", "cd examples/cloud-agent-runner",
          f"docker build --build-arg AGENTS=\"{a['id']}\" -t cloud-agent .",
          f"docker run --rm --env-file .env cloud-agent run-task.sh {a['id']} \"Fix the failing tests\"", "```"]

    if a.get("gotchas"):
        L += ["", "## Gotchas when running in the cloud", ""]
        L += [f"- {g['text'].rstrip('.')}." + (f" ([source]({g['source']}))" if g.get("source") else "")
              for g in a["gotchas"]]


    sources = set()
    for v in a.values():
        items = v if isinstance(v, list) else [v]
        for it in items:
            if isinstance(it, dict) and it.get("source"):
                sources.add(it["source"])
    L += ["", "## Sources", ""] + [f"- <{s}>" for s in sorted(sources)]
    return "\n".join(L)


# ---------------------------------------------------------------- shell blocks for the runnable example

def block_runner_cases() -> str:
    out = []
    for a in AGENTS:
        out.append(f"{a['id']})")
        for line in a["container"]["run"].splitlines():
            out.append(f"  {line}")
        out.append("  ;;")
    return "\n".join(out)


def block_shell_install() -> str:
    return "\n".join(f'case " $AGENTS " in *" {a["id"]} "*|*" all "*) {a["container"]["install"]} ;; esac' for a in AGENTS)


def block_harness_agents() -> str:
    out = []
    for a in AGENTS:
        n = a["northflank"]
        if n["native"]:
            out.append(f"{a['id']}) harness_type={n['harness_type']}; key_auth={'yes' if 'apiKey' in n['api_auth'] else 'no'} ;;")
        else:
            out.append(f"{a['id']}) harness_type=none; key_auth=no ;;")
    return "\n".join(out)


def block_agent_ids() -> str:
    return "AGENT_IDS=\"" + " ".join(a["id"] for a in AGENTS) + "\""


SHELL_BLOCKS = {
    "runner-cases": block_runner_cases,
    "agent-ids": block_agent_ids,
    "shell-install": block_shell_install,
    "harness-agents": block_harness_agents,
}
