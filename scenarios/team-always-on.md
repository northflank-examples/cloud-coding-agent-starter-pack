# Cost scenario: 10 × 24/7 (month)

10 always-on agent workspaces for a team (2 vCPU, 4 GiB, 20 GB each), running 24/7 for a 730-hour month.

## Assumptions and cost by platform

Compute plus persistent workspace storage, at list price. Excludes free credits, plan fees, egress and model usage.

<!-- BEGIN GENERATED: scenario:team-always-on -->
| | |
| --- | --- |
| Environments | 10 |
| Running hours per environment | 730 |
| Size | 2 vCPU, 4 GiB RAM |
| Persistent storage | 20 GB per environment for 1 month(s) |
| CPU busy (usage-billed platforms only) | 10% |

| Platform | Billed size | Per env-hour | Compute | Storage | Total |
| --- | --- | --- | --- | --- | --- |
| [Northflank Cloud Harness](../platforms/northflank.md) | 2 vCPU / 4 GiB | $0.0667 | $486.62 | $30.00 | $516.62 |
| [Sprites (Fly.io)](../platforms/sprites.md) | 2 vCPU / 4 GiB | $0.0952 | $694.96 | $103.66 | $798.62 |
| [E2B](../platforms/e2b.md) | 2 vCPU / 4 GiB | $0.1656 | $1,208.88 | $0.00 | $1,208.88 |
| [Daytona](../platforms/daytona.md) | 2 vCPU / 4 GiB | $0.1656 | $1,208.88 | $11.83 | $1,220.71 |
| [GitHub Codespaces](../platforms/github-codespaces.md) | **2 vCPU / RAM not published** | $0.1800 | $1,314.00 | $14.00 | $1,328.00 |
| [Modal Sandboxes](../platforms/modal.md) | 2 vCPU / 4 GiB | $0.2380 | $1,737.11 | $0.00 | $1,737.11 |

Not priced here, because compute isn't sold by the hour: Claude Code on the web, Cursor Cloud Agents, GitHub Copilot cloud agent, OpenAI Codex cloud, Coder, Ona (formerly Gitpod). See [subscription and licence pricing](../comparisons/pricing.md#subscription-and-licence-pricing).
<!-- END GENERATED: scenario:team-always-on -->

Reproduce or change the assumptions locally:

```bash
python3 scripts/estimate.py --environments 10 --hours 730 --vcpu 2 --memory 4 --disk 20 --months 1 --cpu-busy 0.1
```

[← All scenarios](README.md) · [Methodology](../methodology.md)
