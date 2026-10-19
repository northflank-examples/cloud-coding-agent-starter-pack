# Cost scenario: 100 tasks × 30 min

100 short agent tasks such as dependency bumps or lint fixes (2 vCPU, 4 GiB), 30 minutes each, ephemeral.

## Assumptions and cost by platform

Compute plus persistent workspace storage, at list price. Excludes free credits, plan fees, egress and model usage.

<!-- BEGIN GENERATED: scenario:batch-tasks -->
| | |
| --- | --- |
| Environments | 100 |
| Running hours per environment | 0.5 |
| Size | 2 vCPU, 4 GiB RAM |
| Persistent storage | none (ephemeral) |
| CPU busy (usage-billed platforms only) | 25% |

| Platform | Billed size | Per env-hour | Compute | Storage | Total |
| --- | --- | --- | --- | --- | --- |
| [Northflank Cloud Harness](../platforms/northflank.md) | 2 vCPU / 4 GiB | $0.0667 | $3.33 | $0.00 | $3.33 |
| [Sprites (Fly.io)](../platforms/sprites.md) | 2 vCPU / 4 GiB | $0.1067 | $5.34 | $0.00 | $5.34 |
| [Daytona](../platforms/daytona.md) | 2 vCPU / 4 GiB | $0.1656 | $8.28 | $0.00 | $8.28 |
| [E2B](../platforms/e2b.md) | 2 vCPU / 4 GiB | $0.1656 | $8.28 | $0.00 | $8.28 |
| [GitHub Codespaces](../platforms/github-codespaces.md) | **2 vCPU / RAM not published** | $0.1800 | $9.00 | $0.00 | $9.00 |
| [Modal Sandboxes](../platforms/modal.md) | 2 vCPU / 4 GiB | $0.2380 | $11.90 | $0.00 | $11.90 |

Not priced here, because compute isn't sold by the hour: Claude Code on the web, Cursor Cloud Agents, GitHub Copilot cloud agent, OpenAI Codex cloud, Coder, Ona (formerly Gitpod). See [subscription and licence pricing](../comparisons/pricing.md#subscription-and-licence-pricing).
<!-- END GENERATED: scenario:batch-tasks -->

Reproduce or change the assumptions locally:

```bash
python3 scripts/estimate.py --environments 100 --hours 0.5 --vcpu 2 --memory 4 --cpu-busy 0.25
```

[← All scenarios](README.md) · [Methodology](../methodology.md)
