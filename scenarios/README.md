# Coding agent workload scenarios

Hourly rates don't tell you what your bill will be, so these four standard coding-agent workloads are priced on every platform that sells compute by the hour. Each page shows its assumptions, the billed size on each platform, and the totals.

| Scenario | What it models |
| --- | --- |
| [1 dev, workdays](solo-developer.md) | One developer's persistent cloud agent workspace, paused outside working hours |
| [10 agents × 1 h](parallel-agents.md) | Ten agents working on separate tasks at the same time |
| [100 tasks × 30 min](batch-tasks.md) | A batch of short, ephemeral agent tasks such as dependency bumps or lint fixes |
| [10 × 24/7 (month)](team-always-on.md) | A team's always-on agent workspaces for a full month |

<!-- BEGIN GENERATED: scenarios -->
| Platform | [1 dev, workdays](../scenarios/solo-developer.md) | [10 agents × 1 h](../scenarios/parallel-agents.md) | [100 tasks × 30 min](../scenarios/batch-tasks.md) | [10 × 24/7 (month)](../scenarios/team-always-on.md) |
| --- | --- | --- | --- | --- |
| [Northflank Cloud Harness](../platforms/northflank.md) | $14.73 | $0.67 | $3.33 | $516.62 |
| [Sprites (Fly.io)](../platforms/sprites.md) | $21.59 | $1.07 | $5.34 | $798.62 |
| [E2B](../platforms/e2b.md) | $29.15 | $1.66 | $8.28 | $1,208.88 |
| [Daytona](../platforms/daytona.md) | $30.33 | $1.66 | $8.28 | $1,220.71 |
| [GitHub Codespaces](../platforms/github-codespaces.md) | $33.08 | $1.80 | $9.00 | $1,328.00 |
| [Modal Sandboxes](../platforms/modal.md) | $41.88 | $2.38 | $11.90 | $1,737.11 |

- **1 dev, workdays**: one developer's persistent agent workspace (2 vCPU, 4 GiB, 20 GB), running 8 h × 22 working days (176 h) and paused the rest of the month.
- **10 agents × 1 h**: 10 coding agents working in parallel for one hour on separate tasks (2 vCPU, 4 GiB each), discarded afterwards.
- **100 tasks × 30 min**: 100 short agent tasks such as dependency bumps or lint fixes (2 vCPU, 4 GiB), 30 minutes each, ephemeral.
- **10 × 24/7 (month)**: 10 always-on agent workspaces for a team (2 vCPU, 4 GiB, 20 GB each), running 24/7 for a 730-hour month.
<!-- END GENERATED: scenarios -->

All totals are compute plus persistent workspace storage, at list price. They exclude free credits, plan fees, egress and model usage. Vendor-hosted agents and self-hosted platforms are covered in [subscription and licence pricing](../comparisons/pricing.md#subscription-and-licence-pricing).

To price your own workload, use the [Agent Sandbox Pricing estimator](https://p01--sandbox-pricing-estimator--wdgpv6bn4jz8.code.run/) in your browser, or run `python3 scripts/estimate.py --help`.
