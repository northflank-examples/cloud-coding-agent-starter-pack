# GitHub Codespaces: running coding agents in the cloud

GitHub-hosted dev containers, each on its own VM, built from devcontainer.json and billed per core-hour plus GB-month storage. You install CLI agents yourself.

<!-- BEGIN GENERATED: platform:github-codespaces -->
Last verified: **2026-10-19** · Official pricing: <https://docs.github.com/en/billing/concepts/product-billing/github-codespaces>

## At a glance

|  |  |
| --- | --- |
| Type | Cloud dev environment |
| Coding agents | Any CLI agent you install (devcontainer) |
| Environment / image | devcontainer.json; 2 to 32 core machines |
| Isolation | Container on a dedicated VM |
| API / programmatic | REST API, `gh codespace` CLI |
| Persistence | Yes; stopped codespaces deleted after 30 days inactive |
| When idle | Stops after 30 min idle (5–240 configurable) |
| Max session | 12 hours |
| Concurrency | Limits exist but aren't published |
| Access | Browser VS Code, VS Code, JetBrains, `gh codespace ssh` |
| Git integration | GitHub only |
| Secrets | User/repo/org Codespaces secrets |
| Network controls | Private/org/public forwarded ports; no egress allowlist documented |
| Run in your own cloud | No |
| Billing model | fixed machine sizes, while running |
| Price (2 vCPU / 4 GiB) | $0.1800/hr (billed as 2 vCPU / RAM not published) |
| Storage | $0.07/GB-month |
| Plan fee | None |
| Free tier / credits | Personal: 120 core-hours + 15 GB-month/mo (Pro: 180 + 20); none for orgs |

## Details

- **Isolation:** Container on a dedicated VM. Vendor docs: "Each codespace that you create is hosted on a separate virtual machine." ([source](https://docs.github.com/en/codespaces/setting-up-your-project-for-codespaces/configuring-dev-containers/setting-a-minimum-specification-for-codespace-machines))
- **When idle:** Stops after 30 min idle (5–240 configurable). Vendor docs: "The default inactivity timeout period is 30 minutes." ([source](https://docs.github.com/en/codespaces/about-codespaces/deep-dive))
- **Max session:** 12 hours. Vendor docs: "A codespace has a maximum lifetime of 12 hours, regardless of your idle timeout policy or settings." ([source](https://docs.github.com/en/codespaces/about-codespaces/understanding-the-codespace-lifecycle))

## Published pricing (verbatim)

- "| Codespaces compute | 2 core | 1 hour | 2 | $0.18 |"
- "| Codespaces compute | 4 core | 1 hour | 4 | $0.36 |"
- "| Codespaces storage | Storage | 1 GB-month | Not applicable | $0.07 |"
- "GitHub plans for organizations and enterprises do not include a free quota for GitHub Codespaces."

## Cost in the standard scenarios

| Scenario | Compute | Storage | Total |
| --- | --- | --- | --- |
| [1 dev, workdays](../scenarios/solo-developer.md) | $31.68 | $1.40 | $33.08 |
| [10 agents × 1 h](../scenarios/parallel-agents.md) | $1.80 | $0.00 | $1.80 |
| [100 tasks × 30 min](../scenarios/batch-tasks.md) | $9.00 | $0.00 | $9.00 |
| [10 × 24/7 (month)](../scenarios/team-always-on.md) | $1,314.00 | $14.00 | $1,328.00 |

## Caveats

- RAM per machine type isn't listed on GitHub's billing or docs pages, so the comparison assumes the 2-core machine fits a 2 vCPU / 4 GiB workload.
- The 12-hour maximum lifetime means always-on agents must be restarted at least twice a day.

## Sources

- <https://docs.github.com/en/billing/concepts/product-billing/github-codespaces>
- <https://docs.github.com/en/codespaces/about-codespaces/deep-dive>
- <https://docs.github.com/en/codespaces/about-codespaces/understanding-the-codespace-lifecycle>
- <https://docs.github.com/en/codespaces/customizing-your-codespace/changing-the-machine-type-for-your-codespace>
- <https://docs.github.com/en/codespaces/developing-in-a-codespace/creating-a-codespace-for-a-repository>
- <https://docs.github.com/en/codespaces/developing-in-a-codespace/forwarding-ports-in-your-codespace>
- <https://docs.github.com/en/codespaces/developing-in-a-codespace/using-github-codespaces-with-github-cli>
- <https://docs.github.com/en/codespaces/managing-your-codespaces/managing-your-account-specific-secrets-for-github-codespaces>
- <https://docs.github.com/en/codespaces/setting-up-your-project-for-codespaces/configuring-dev-containers/setting-a-minimum-specification-for-codespace-machines>
- <https://docs.github.com/en/codespaces/setting-your-user-preferences/configuring-automatic-deletion-of-your-codespaces>
- <https://github.com/features/codespaces>
<!-- END GENERATED: platform:github-codespaces -->

[← Back to the comparison](../README.md) · [Feature matrix](../comparisons/feature-matrix.md) · [Pricing](../comparisons/pricing.md)
