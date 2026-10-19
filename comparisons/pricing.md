# Cloud coding agent platforms: pricing

All tables are generated from [`data/platforms.json`](../data/platforms.json). Rates are list prices for the default/US region, checked against the official pricing pages linked in the last column.

## Metered compute

Platforms that charge for the environment by the hour, sorted by the price of one 2 vCPU / 4 GiB environment.

<!-- BEGIN GENERATED: rates -->
| Platform | Billing model | CPU / vCPU-hr | RAM / GiB-hr | 2 vCPU / 4 GiB | Storage | Plan fee | Free tier / credits | Source |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| [Northflank Cloud Harness](../platforms/northflank.md) | fixed machine sizes, while running | $0.01667 | $0.00833 | $0.0667/hr | Volumes $0.15/GB-month | None (pay-as-you-go) | Free projects: 1 harness, up to 1 vCPU / 1 GB | [pricing](https://northflank.com/pricing) |
| [Sprites (Fly.io)](../platforms/sprites.md) | CPU and RAM actually used | $0.0385 | $0.02187 | $0.1067/hr at 25% CPU busy | Hot $0.000683/GB-hr while awake; cold $0.000027/GB-hr while kept | Pay-as-you-go; optional plans (e.g. Hero $100/mo) | $30 trial credit | [pricing](https://fly.io/sprites) |
| [Daytona](../platforms/daytona.md) | per vCPU + GiB, while running | $0.0504 | $0.0162 | $0.1656/hr | First 5 GiB free, then $0.000108/GiB-hr (~$0.079/GiB-mo) | None (prepaid credits) | $200 credit | [pricing](https://www.daytona.io/pricing) |
| [E2B](../platforms/e2b.md) | per vCPU + GiB, while running | $0.0504 | $0.0162 | $0.1656/hr | Disk included; paused storage pricing not published | Hobby $0; Pro $150/mo (needed for >1 h sessions or >20 concurrent) | One-time $100 credit | [pricing](https://e2b.dev/pricing) |
| [GitHub Codespaces](../platforms/github-codespaces.md) | fixed machine sizes, while running | $0.09 | n/a | $0.1800/hr (billed as 2 vCPU / RAM not published) | $0.07/GB-month | None | Personal: 120 core-hours + 15 GB-month/mo (Pro: 180 + 20); none for orgs | [pricing](https://docs.github.com/en/billing/concepts/product-billing/github-codespaces) |
| [Modal Sandboxes](../platforms/modal.md) | per vCPU + GiB, while running | $0.07096 | $0.02401 | $0.2380/hr | Volumes $0.09/GiB-mo, 1 TiB/mo free; egress $0.04/GiB | Starter $0/mo; Team $250/mo | $30/mo credits (Starter), $100/mo (Team) | [pricing](https://modal.com/pricing) |
<!-- END GENERATED: rates -->

*Billing models:*

- **Per vCPU + GiB, while running:** you pay for reserved CPU and RAM every second the environment runs, busy or not.
- **Fixed machine sizes:** you pay the price of the smallest size the vendor sells that fits your request.
- **CPU and RAM actually used:** you pay only for measured usage, so idle waiting is cheap.

## Subscription and licence pricing

These platforms don't sell compute by the hour, so they're excluded from the scenario totals.

<!-- BEGIN GENERATED: subscription -->
| Platform | Pricing model | What you pay |
| --- | --- | --- |
| [Claude Code on the web](../platforms/claude-code-web.md) | included in a subscription | Included in Claude Pro ($20/mo), Max (from $100/mo), Team and Enterprise; counts toward plan usage limits |
| [Cursor Cloud Agents](../platforms/cursor-cloud-agents.md) | included in a subscription | Cursor Premium ($30/mo), Super ($100/mo), Ultra ($200/mo), Teams or Enterprise; Free and Plus don't include cloud agents; model usage billed at API pricing; infrastructure included |
| [GitHub Copilot cloud agent](../platforms/copilot-cloud-agent.md) | usage-based credits | Copilot plan (Pro $10/mo to Enterprise $39/seat/mo) plus GitHub Actions minutes and AI credits per session |
| [OpenAI Codex cloud](../platforms/codex-cloud.md) | included in a subscription | Included in ChatGPT Plus ($20/mo), Pro ($100–$500/mo), Business and Enterprise; shares the plan's Codex allowance; not available with API keys |
| [Coder](../platforms/coder.md) | self-hosted licence + your cloud | Community edition free (AGPL); Premium per-user licence (price not published); compute is your own cloud bill |
| [Ona (formerly Gitpod)](../platforms/ona.md) | usage-based credits | Enterprise via sales, billed in credits; legacy Core plan billed in OCUs (price per OCU not published); new signups closed |
<!-- END GENERATED: subscription -->

How to compare these with metered platforms:

- **Vendor-hosted agents** (Claude Code on the web, Codex cloud) don't charge separately for the VM, but cloud sessions **count toward your plan's usage limits**, and running many in parallel uses those limits up faster. Cursor charges model usage at API rates on top of a paid plan.
- **Copilot cloud agent** charges GitHub Actions minutes for the runner, plus AI credits per session.
- **Coder** is free software or a per-user licence. You pay your own cloud for the machines.

## What the hourly rate doesn't show

1. **Idle time.** Platforms that bill allocated resources charge while the agent waits on the model. Pause environments you aren't using: Northflank and E2B stop compute billing when paused, Codespaces and Daytona auto-stop after 30 and 15 idle minutes by default, and Sprites pauses after about 30 s.
2. **Plan fees and limits.** E2B needs the $150/mo Pro plan for sessions over an hour or more than 20 concurrent sandboxes. Northflank, Daytona and Codespaces have no plan fee.
3. **Session limits.** An always-on agent on Codespaces (12 h) or E2B Pro (24 h) needs restart or pause/resume logic.
4. **Storage.** Persistent workspaces are billed per GB-month on most platforms, including while paused.
5. **Model usage.** Tokens for Claude or GPT models are the same wherever the agent runs, and usually cost more than the environment. See [cost optimization](../guides/cost-optimization.md).

[← Back to the comparison](../README.md) · [Feature matrix](feature-matrix.md) · [Scenarios](../scenarios/README.md)
