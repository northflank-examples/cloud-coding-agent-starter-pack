# Cost scenario: 1 dev, workdays

One developer's persistent agent workspace (2 vCPU, 4 GiB, 20 GB), running 8 h × 22 working days (176 h) and paused the rest of the month.

## Assumptions and cost by platform

Compute plus persistent workspace storage, at list price. Excludes free credits, plan fees, egress and model usage.

<!-- BEGIN GENERATED: scenario:solo-developer -->
| | |
| --- | --- |
| Environments | 1 |
| Running hours per environment | 176 |
| Size | 2 vCPU, 4 GiB RAM |
| Persistent storage | 20 GB per environment for 1 month(s) |
| CPU busy (usage-billed platforms only) | 25% |

| Platform | Billed size | Per env-hour | Compute | Storage | Total |
| --- | --- | --- | --- | --- | --- |
| [Northflank Cloud Harness](../platforms/northflank.md) | 2 vCPU / 4 GiB | $0.0667 | $11.73 | $3.00 | $14.73 |
| [Sprites (Fly.io)](../platforms/sprites.md) | 2 vCPU / 4 GiB | $0.1067 | $18.79 | $2.80 | $21.59 |
| [E2B](../platforms/e2b.md) | 2 vCPU / 4 GiB | $0.1656 | $29.15 | $0.00 | $29.15 |
| [Daytona](../platforms/daytona.md) | 2 vCPU / 4 GiB | $0.1656 | $29.15 | $1.18 | $30.33 |
| [GitHub Codespaces](../platforms/github-codespaces.md) | **2 vCPU / RAM not published** | $0.1800 | $31.68 | $1.40 | $33.08 |
| [Modal Sandboxes](../platforms/modal.md) | 2 vCPU / 4 GiB | $0.2380 | $41.88 | $0.00 | $41.88 |

Not priced here, because compute isn't sold by the hour: Claude Code on the web, Cursor Cloud Agents, GitHub Copilot cloud agent, OpenAI Codex cloud, Coder, Ona (formerly Gitpod). See [subscription and licence pricing](../comparisons/pricing.md#subscription-and-licence-pricing).
<!-- END GENERATED: scenario:solo-developer -->

Reproduce or change the assumptions locally:

```bash
python3 scripts/estimate.py --environments 1 --hours 176 --vcpu 2 --memory 4 --disk 20 --months 1 --cpu-busy 0.25
```

[← All scenarios](README.md) · [Methodology](../methodology.md)
