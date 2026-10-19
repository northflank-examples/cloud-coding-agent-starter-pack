# Daytona: running coding agents in the cloud

Persistent sandboxes (containers by default, optional VMs) managed by SDK, API or CLI. The default snapshot preinstalls Claude Code, Codex and OpenCode.

<!-- BEGIN GENERATED: platform:daytona -->
Last verified: **2026-10-19** · Official pricing: <https://www.daytona.io/pricing>

## At a glance

|  |  |
| --- | --- |
| Type | Sandbox platform |
| Coding agents | Claude Code, Codex, OpenCode preinstalled; any agent |
| Environment / image | Snapshots (images); default 1 vCPU / 1 GB, max 4 vCPU / 8 GB per sandbox by default |
| Isolation | Container by default; optional VM |
| API / programmatic | Python/TS/Go/Java/Ruby SDKs, REST API, CLI |
| Persistence | Yes by default; archived after 7 days stopped |
| When idle | Containers auto-stop after 15 min idle; VMs auto-pause after 60 min (defaults) |
| Max session | No limit (auto-stop can be disabled) |
| Concurrency | Tiered vCPU/RAM pools (Tier 1: 10 vCPU) |
| Access | Web terminal, SSH, VS Code / JetBrains over SSH |
| Git integration | SDK git operations (clone, commit, push) |
| Secrets | Org secrets swapped in by outbound proxy |
| Network controls | Restricted on Tier 1–2; allowlists/block-all on Tier 3–4 |
| Run in your own cloud | Bring your own compute (custom regions) |
| Billing model | per vCPU + GiB, while running |
| Price (2 vCPU / 4 GiB) | $0.1656/hr |
| Storage | First 5 GiB free, then $0.000108/GiB-hr (~$0.079/GiB-mo) |
| Plan fee | None (prepaid credits) |
| Free tier / credits | $200 credit |

## Details

- **Coding agents:** Claude Code, Codex, OpenCode preinstalled; any agent. Vendor docs: "The default Daytona snapshot includes Claude Code, so the command above is all you need." ([source](https://www.daytona.io/docs/en/guides/claude/claude-code-run-cli-sandbox))
- **Persistence:** Yes by default; archived after 7 days stopped. Vendor docs: "Daytona sandboxes are persistent by default." ([source](https://www.daytona.io/docs/en/persistence))

## Published pricing (verbatim)

- "CPU $0.0504/vCPU-hr and memory $0.0162/GiB-hr, per second (as verified 2026-10-14 in agent-sandbox-pricing)"

## Cost in the standard scenarios

| Scenario | Compute | Storage | Total |
| --- | --- | --- | --- |
| [1 dev, workdays](../scenarios/solo-developer.md) | $29.15 | $1.18 | $30.33 |
| [10 agents × 1 h](../scenarios/parallel-agents.md) | $1.66 | $0.00 | $1.66 |
| [100 tasks × 30 min](../scenarios/batch-tasks.md) | $8.28 | $0.00 | $8.28 |
| [10 × 24/7 (month)](../scenarios/team-always-on.md) | $1,208.88 | $11.83 | $1,220.71 |

## Caveats and open questions

- Disk is billed while the sandbox exists until it's archived (after 7 days stopped by default). Here it's priced for the full month.
- Linux VM sandbox pricing isn't published (Windows VMs are listed at $0.0858/vCPU/h); container pricing is used here.

## Sources

- <https://www.daytona.io/docs/en/billing>
- <https://www.daytona.io/docs/en/bring-your-own-compute>
- <https://www.daytona.io/docs/en/git-operations>
- <https://www.daytona.io/docs/en/guides/claude/claude-code-run-cli-sandbox>
- <https://www.daytona.io/docs/en/isolation>
- <https://www.daytona.io/docs/en/limits>
- <https://www.daytona.io/docs/en/network-limits>
- <https://www.daytona.io/docs/en/persistence>
- <https://www.daytona.io/docs/en/sandboxes>
- <https://www.daytona.io/docs/en/sandboxes#auto-stop-interval>
- <https://www.daytona.io/docs/en/secrets>
- <https://www.daytona.io/docs/en/ssh-access>
- <https://www.daytona.io/pricing>
<!-- END GENERATED: platform:daytona -->

[← Back to the comparison](../README.md) · [Feature matrix](../comparisons/feature-matrix.md) · [Pricing](../comparisons/pricing.md)
