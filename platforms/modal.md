# Modal Sandboxes

Modal Sandboxes are containers you create at runtime from Modal's SDKs, isolated with gVisor or a VM runtime (you choose, or Modal picks), and built for running untrusted or agent-generated code. There's no agent preinstalled: you install Claude Code, OpenCode or any other agent in the image, and Modal publishes [examples for Claude Code](https://modal.com/docs/examples/sandbox_agent) and [OpenCode](https://modal.com/docs/examples/opencode_server). Sandboxes have their own CPU and memory rates, about three times Modal's standard Function rates, and run for at most 24 hours.

<!-- BEGIN GENERATED: platform:modal -->
Last verified: **2026-10-19** · Official pricing: <https://modal.com/pricing>

## At a glance

|  |  |
| --- | --- |
| Type | Sandbox platform |
| Coding agents | Any agent you install; official Claude Code and OpenCode examples |
| Environment / image | Any image via `modal.Image` or a registry |
| Isolation | gVisor or VM runtime (Modal picks if unset) |
| API / programmatic | Python SDK; JavaScript and Go SDKs (beta); CLI |
| Persistence | Volumes; filesystem snapshots (30-day default TTL) |
| When idle | Optional `idle_timeout` terminates the sandbox |
| Max session | 5 min default, up to 24 h; snapshot to continue |
| Concurrency | Starter 100 / Team 5,000 containers |
| Access | `modal shell`, exec with PTY, Tunnels; no SSH |
| Git integration | None built in; clone inside the sandbox |
| Secrets | `modal.Secret` |
| Network controls | `block_network`, CIDR and domain allowlists (beta) |
| Run in your own cloud | No (not published) |
| Billing model | per vCPU + GiB, while running |
| Price (2 vCPU / 4 GiB) | $0.2380/hr |
| Storage | Volumes $0.09/GiB-mo, 1 TiB/mo free; egress $0.04/GiB |
| Plan fee | Starter $0/mo; Team $250/mo |
| Free tier / credits | $30/mo credits (Starter), $100/mo (Team) |

## Details

- **Coding agents:** Any agent you install in the image. Official examples cover Claude Code, OpenCode, Cursor Cloud Agents, the Claude Agent SDK, LangGraph and Claude Managed Agents. Vendor docs: "This example demonstrates how to run Claude Code in a Modal Sandbox to analyze a GitHub repository." ([source](https://modal.com/docs/examples/sandbox_agent))
- **Environment / image:** Custom images built with modal.Image (e.g. debian_slim().pip_install), plus existing registry images and named Images. Vendor docs: "Run containers with arbitrary dependencies and setup scripts." ([source](https://modal.com/docs/guide/sandboxes))
- **Isolation:** Sandboxes run on gVisor or in a VM with its own Linux kernel (supporting Docker-in-Sandbox, FUSE and nested cgroups). You choose with the runtime parameter, or leave it unset and Modal chooses. Vendor docs: "Sandboxes run on one of two runtimes: gVisor , a container runtime developed by Google, provides strong isolation and is suitable for most workloads. VMs run the Sandbox in a virtual machine with its own Linux kernel." ([source](https://modal.com/docs/guide/sandboxes))
- **API / programmatic:** Python SDK (sync and async), JavaScript and Go SDKs (Beta), modal CLI. Vendor docs: "JavaScript/Go SDKs Beta" ([source](https://modal.com/docs/guide/sandboxes))
- **Persistence:** Volumes can be mounted. Filesystem and Directory Snapshots are kept 30 days by default (TTL configurable, or no expiry). Memory Snapshots are Alpha and expire after 7 days. Vendor docs: "Modal currently supports three different kinds of Sandbox snapshots: Filesystem Snapshots Directory Snapshots Memory Snapshots" ([source](https://modal.com/docs/guide/sandbox-snapshots))
- **When idle:** Optional idle_timeout. A Sandbox counts as active while an exec command runs, stdin is being written, or a Tunnel has an open TCP connection. Vendor docs: "Sandboxes can also be automatically terminated after a period of inactivity - you can do this by setting the idle_timeout parameter." ([source](https://modal.com/docs/guide/sandboxes))
- **Max session:** 5 min default, up to 24 h. For longer work, snapshot and restore into a new Sandbox. Vendor docs: "Sandboxes have a default maximum lifetime of 5 minutes. You can change this by passing a timeout of up to 24 hours to the Sandbox.create(...) function." ([source](https://modal.com/docs/guide/sandboxes))
- **Concurrency:** Up to 50,000 concurrent sandboxes per customer (Modal engineering blog). The plan table lists 100 containers on Starter and 5,000 on Team. Vendor docs: "supports up to fifty thousand concurrent sandboxes per customer" ([source](https://modal.com/blog/scaling-to-1-million-concurrent-sandboxes-in-seconds))
- **Access:** sandbox.exec (with PTY), Tunnels for exposing ports, and `modal shell <sandbox-id>` for an interactive shell. No SSH or browser web terminal is documented. Vendor docs: "Connect to a running Sandbox by ID: modal shell sb-abc123xyz" ([source](https://modal.com/docs/reference/cli/shell))
- **Git integration:** No built-in git integration. Examples run git clone inside the Sandbox or at image build time, using a GitHub token for private repos. Vendor docs: "Check out a git repository and run a command against it, like a test suite, or npm lint ." ([source](https://modal.com/docs/guide/sandboxes))
- **Secrets:** modal.Secret (from_name / from_dict) is passed to Sandbox.create or exec. Secret injection into outbound request headers is in Beta. Vendor docs: "You can set environment variables using inline secrets" ([source](https://modal.com/docs/guide/sandboxes))
- **Network controls:** Outbound is open by default. Options are block_network=True, outbound_cidr_allowlist and outbound_domain_allowlist (Beta, TLS on port 443 only). DNS is not restricted unless the network is fully blocked. Inbound connections are not accepted by default. Vendor docs: "Full block block_network=True Drops all outbound traffic. IP-range allowlist outbound_cidr_allowlist Only allows traffic to the listed CIDR ranges (any protocol). Domain allowlist (Beta) outbound_domain_allowlist" ([source](https://modal.com/docs/guide/sandbox-networking))
- **Run in your own cloud:** Not published. Modal runs on its own multi-cloud capacity pool, and the AWS/GCP marketplace option is for purchasing only. Vendor docs: "Transact through the AWS and GCP marketplace to use committed spend on Modal." ([source](https://modal.com/pricing))

## Published pricing (verbatim)

- "Modal Sandbox + Notebooks pricing Only pay for what you use."
- "CPU Physical core (2 vCPU equivalent) $ 0.00003942 / core / sec *minimum of 0.125 cores per container"
- "Memory $ 0.00000667 / GiB / sec"
- "Standard (Functions): CPU $ 0.0000131 / core / sec Physical core (2 vCPU equivalent)"
- "Standard (Functions): Memory $ 0.00000222 / GiB / sec"
- "Volumes $ 0.09 / GiB / mo *includes 1 TiB / mo free"
- "Network Egress $ 0.04 / GiB"
- "Starter ... $0 + compute / month $30 / month free credits 3 workspace seats included 100 containers + 10 GPU concurrency"
- "Team ... $250 + compute / month $100 / month free credits Unlimited seats 5000 containers + 50 GPU concurrency"
- "Note that each physical core is equivalent to 2 vCPUs as offered by AWS or GCP."
- "Modal Sandboxes are billed by the second based on whichever is higher: your resource request or your actual usage. ... You pay for max(request, actual) ."

## Cost in the standard scenarios

| Scenario | Compute | Storage | Total |
| --- | --- | --- | --- |
| [1 dev, workdays](../scenarios/solo-developer.md) | $41.88 | $0.00 | $41.88 |
| [10 agents × 1 h](../scenarios/parallel-agents.md) | $2.38 | $0.00 | $2.38 |
| [100 tasks × 30 min](../scenarios/batch-tasks.md) | $11.90 | $0.00 | $11.90 |
| [10 × 24/7 (month)](../scenarios/team-always-on.md) | $1,737.11 | $0.00 | $1,737.11 |

## Caveats and open questions

- Modal prices CPU per physical core; 1 core = 2 vCPU per Modal's docs, so the per-vCPU rate here is the per-core rate halved.
- Billing is max(request, actual usage), so it is modelled like allocated pricing: the request is the floor. A sandbox using more than it requests costs more.
- Sandbox rates are about 3x Modal's standard Function rates ($0.0000131/core/s and $0.00000222/GiB/s); only Sandbox rates are used here.
- Sandboxes run for at most 24 hours. The always-on scenario assumes you snapshot and restore into a new sandbox every 24 hours, which Modal documents but which isn't free of effort.
- The 1 TiB/month free Volume allowance is applied per environment here; if it is per workspace (account), large teams may pay for storage sooner.
- No official Codex CLI example was found in Modal docs or examples.
- Unclear whether the plan container limits (Starter 100, Team 5000) cap concurrent Sandboxes; the blog cites up to 50,000 concurrent sandboxes per customer.
- No SSH or browser-based web terminal is documented for Sandboxes; only `modal shell <sandbox-id>`, exec with PTY, and Tunnels.
- Not stated whether region-selection (1.15-1.75x) or non-preemptible (3x) multipliers apply to Sandbox CPU/memory rates.
- Storage pricing for retained snapshots (filesystem/directory/memory) is not published separately from Volumes.
- Pricing for the VM runtime or nested virtualization (Team/Enterprise) is not separately itemized on the pricing page.
- BYOC (running Modal Sandboxes in a customer's own cloud account) is not mentioned in official docs or pricing.

## Sources

- <https://modal.com/blog/scaling-to-1-million-concurrent-sandboxes-in-seconds>
- <https://modal.com/docs/examples/sandbox_agent>
- <https://modal.com/docs/guide/sandbox-networking>
- <https://modal.com/docs/guide/sandbox-resources>
- <https://modal.com/docs/guide/sandbox-snapshots>
- <https://modal.com/docs/guide/sandboxes>
- <https://modal.com/docs/reference/cli/shell>
- <https://modal.com/pricing>
<!-- END GENERATED: platform:modal -->
