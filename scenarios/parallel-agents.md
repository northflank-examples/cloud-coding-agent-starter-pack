# Cost scenario: 10 agents × 1 h

10 coding agents working in parallel for one hour on separate tasks (2 vCPU, 4 GiB each), discarded afterwards.

## Assumptions and cost by platform

Compute plus persistent workspace storage, at list price. Excludes free credits, plan fees, egress and model usage.

<!-- BEGIN GENERATED: scenario:parallel-agents -->
| | |
| --- | --- |
| Environments | 10 |
| Running hours per environment | 1 |
| Size | 2 vCPU, 4 GiB RAM |
| Persistent storage | none (ephemeral) |
| CPU busy (usage-billed platforms only) | 25% |

| Platform | Billed size | Per env-hour | Compute | Storage | Total |
| --- | --- | --- | --- | --- | --- |
| [Northflank Cloud Harness](../platforms/northflank.md) | 2 vCPU / 4 GiB | $0.0667 | $0.67 | $0.00 | $0.67 |
| [Sprites (Fly.io)](../platforms/sprites.md) | 2 vCPU / 4 GiB | $0.1067 | $1.07 | $0.00 | $1.07 |
| [Daytona](../platforms/daytona.md) | 2 vCPU / 4 GiB | $0.1656 | $1.66 | $0.00 | $1.66 |
| [E2B](../platforms/e2b.md) | 2 vCPU / 4 GiB | $0.1656 | $1.66 | $0.00 | $1.66 |
| [GitHub Codespaces](../platforms/github-codespaces.md) | **2 vCPU / RAM not published** | $0.1800 | $1.80 | $0.00 | $1.80 |
| [Modal Sandboxes](../platforms/modal.md) | 2 vCPU / 4 GiB | $0.2380 | $2.38 | $0.00 | $2.38 |

Not priced here, because compute isn't sold by the hour: Claude Code on the web, Cursor Cloud Agents, GitHub Copilot cloud agent, OpenAI Codex cloud, Coder, Ona (formerly Gitpod). See [subscription and licence pricing](../comparisons/pricing.md#subscription-and-licence-pricing).
<!-- END GENERATED: scenario:parallel-agents -->

Reproduce or change the assumptions locally:

```bash
python3 scripts/estimate.py --environments 10 --hours 1 --vcpu 2 --memory 4 --cpu-busy 0.25
```

[← All scenarios](README.md) · [Methodology](../methodology.md)
