# E2B: running coding agents in the cloud

Firecracker microVM sandboxes controlled through an SDK, API or CLI, with prebuilt templates for Claude Code, Codex, Amp and OpenCode.

<!-- BEGIN GENERATED: platform:e2b -->
Last verified: **2026-10-19** · Official pricing: <https://e2b.dev/pricing>

## At a glance

|  |  |
| --- | --- |
| Type | Sandbox platform |
| Coding agents | Templates: Claude Code, Codex, Amp, OpenCode; any agent |
| Environment / image | Custom templates; 10 GiB disk (Hobby), 20 GiB (Pro) |
| Isolation | Firecracker microVM |
| API / programmatic | JS/Python SDK, REST API, CLI |
| Persistence | Opt-in pause/resume; paused kept indefinitely |
| When idle | Killed after 5 min timeout by default (can pause instead) |
| Max session | 1 h (Hobby) / 24 h (Pro) continuous; pausing resets |
| Concurrency | 20 (Hobby); 100–1,100 (Pro with add-ons) |
| Access | SDK terminal (PTY); SSH via custom template + proxy |
| Git integration | Via commands in the sandbox |
| Secrets | Secrets store injected by egress proxy; env vars |
| Network controls | Internet on/off, CIDR/hostname allow and deny lists |
| Run in your own cloud | Enterprise only (AWS, GCP, Azure) |
| Billing model | per vCPU + GiB, while running |
| Price (2 vCPU / 4 GiB) | $0.1656/hr |
| Storage | Disk included; paused storage pricing not published |
| Plan fee | Hobby $0; Pro $150/mo (needed for >1 h sessions or >20 concurrent) |
| Free tier / credits | One-time $100 credit |

## Details

- **Coding agents:** Templates: Claude Code, Codex, Amp, OpenCode; any agent. Vendor docs: "E2B provides a pre-built `claude` template with Claude Code already installed." ([source](https://docs.e2b.dev/agents/claude-code))
- **When idle:** Killed after 5 min timeout by default (can pause instead). Vendor docs: "Every sandbox has a timeout, and it defaults to **5 minutes** if you do not set one." ([source](https://docs.e2b.dev/faq/sandbox-lifetime))

## Published pricing (verbatim)

- "vCPUs 1 Hobby / Pro $0.000014/s"
- "Memory (GiB) 1 Hobby / Pro $0.0000045/s"
- "You pay per second for compute resources while your sandbox is running."

## Cost in the standard scenarios

| Scenario | Compute | Storage | Total |
| --- | --- | --- | --- |
| [1 dev, workdays](../scenarios/solo-developer.md) | $29.15 | $0.00 | $29.15 |
| [10 agents × 1 h](../scenarios/parallel-agents.md) | $1.66 | $0.00 | $1.66 |
| [100 tasks × 30 min](../scenarios/batch-tasks.md) | $8.28 | $0.00 | $8.28 |
| [10 × 24/7 (month)](../scenarios/team-always-on.md) | $1,208.88 | $0.00 | $1,208.88 |

## Caveats and open questions

- Storage for paused sandboxes isn't priced on the billing page, so it's counted as $0 here.
- Always-on use needs Pro and pause/resume every 24 h, or Enterprise.

## Sources

- <https://docs.e2b.dev/agents/claude-code>
- <https://docs.e2b.dev/billing>
- <https://docs.e2b.dev/byoc>
- <https://docs.e2b.dev/faq/sandbox-lifetime>
- <https://docs.e2b.dev/faq/security-and-compliance>
- <https://docs.e2b.dev/sandbox/git-integration>
- <https://docs.e2b.dev/sandbox/internet-access>
- <https://docs.e2b.dev/sandbox/persistence>
- <https://docs.e2b.dev/sandbox/ssh-access>
- <https://docs.e2b.dev/secrets>
- <https://e2b.dev/pricing>
<!-- END GENERATED: platform:e2b -->

[← Back to the comparison](../README.md) · [Feature matrix](../comparisons/feature-matrix.md) · [Pricing](../comparisons/pricing.md)
