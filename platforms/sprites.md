# Sprites (Fly.io): running coding agents in the cloud

Persistent, hardware-isolated Linux VMs from Fly.io that pause after about 30 s idle and are billed on actual CPU and memory use, with the Claude, Codex, Gemini and Cursor CLIs preinstalled.

<!-- BEGIN GENERATED: platform:sprites -->
Last verified: **2026-10-19** · Official pricing: <https://fly.io/sprites>

## At a glance

|  |  |
| --- | --- |
| Type | Sandbox platform |
| Coding agents | Claude Code, Codex, Gemini CLI, Cursor preinstalled; any agent |
| Environment / image | Ubuntu 25.10, 100 GB volume |
| Isolation | Hardware-isolated VM |
| API / programmatic | REST/WebSocket API, SDKs, `sprite` CLI, MCP |
| Persistence | Yes: disk persists; checkpoints |
| When idle | Pauses after ~30 s idle; no compute charge |
| Max session | No limit (persistent); task holds up to 1 h, renewable |
| Concurrency | Per-plan (Hero: 100 running) |
| Access | `sprite console` shell; no built-in SSH |
| Git integration | git preinstalled; GitHub connector |
| Secrets | Connectors via API gateway (agent never sees token) |
| Network controls | Opt-in DNS allow/deny policy |
| Run in your own cloud | No |
| Billing model | CPU and RAM actually used |
| Price (2 vCPU / 4 GiB) | $0.1067/hr at 25% CPU busy |
| Storage | Hot $0.000683/GB-hr while awake; cold $0.000027/GB-hr while kept |
| Plan fee | Pay-as-you-go; optional plans (e.g. Hero $100/mo) |
| Free tier / credits | $30 trial credit |

## Details

- **Coding agents:** Claude Code, Codex, Gemini CLI, Cursor preinstalled; any agent. Vendor docs: "AI/CLI Tools: Claude CLI, Gemini CLI, OpenAI Codex, Cursor" ([source](https://docs.fly.io/sprites/working-with-sprites))
- **Isolation:** Hardware-isolated VM. Vendor docs: "Sprites are persistent, hardware-isolated Linux environments for running arbitrary code." ([source](https://docs.fly.io/sprites))
- **Persistence:** Yes: disk persists; checkpoints. Vendor docs: "The split is simple: disk persists, memory does not." ([source](https://docs.fly.io/sprites/concepts/lifecycle))

## Published pricing (verbatim)

- "CPU Time Cumulative CPU usage measured by cpu.stat $0.0385 /CPU-hour"
- "Memory Time Actual memory usage $0.021875 /GB-hour"
- "All resources are billed hourly, based on actual usage."

## Cost in the standard scenarios

| Scenario | Compute | Storage | Total |
| --- | --- | --- | --- |
| [1 dev, workdays](../scenarios/solo-developer.md) | $18.79 | $2.80 | $21.59 |
| [10 agents × 1 h](../scenarios/parallel-agents.md) | $1.07 | $0.00 | $1.07 |
| [100 tasks × 30 min](../scenarios/batch-tasks.md) | $5.34 | $0.00 | $5.34 |
| [10 × 24/7 (month)](../scenarios/team-always-on.md) | $694.96 | $103.66 | $798.62 |

## Caveats

- Billing is on measured usage. This comparison assumes the full stated memory is used, with CPU at each scenario's utilisation, which can overstate Sprites' cost for light workloads.
- Auto-pause after ~30 s idle can make real bills much lower than the running-hours assumptions here.

## Sources

- <https://docs.fly.io/sprites>
- <https://docs.fly.io/sprites/concepts/connectors>
- <https://docs.fly.io/sprites/concepts/lifecycle>
- <https://docs.fly.io/sprites/concepts/networking>
- <https://docs.fly.io/sprites/integrations/index>
- <https://docs.fly.io/sprites/keeping-sprites-running>
- <https://docs.fly.io/sprites/working-with-sprites>
- <https://fly.io/sprites>
<!-- END GENERATED: platform:sprites -->

[← Back to the comparison](../README.md) · [Feature matrix](../comparisons/feature-matrix.md) · [Pricing](../comparisons/pricing.md)
