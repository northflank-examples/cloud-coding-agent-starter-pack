# GitHub Copilot cloud agent: running coding agents in the cloud

Copilot's cloud agent (formerly 'coding agent') runs in an ephemeral GitHub Actions runner for at most 59 minutes per session, pushes to one copilot/ branch and opens a PR. Claude and Codex partner agents are in public preview.

<!-- BEGIN GENERATED: platform:copilot-cloud-agent -->
Last verified: **2026-10-19** · Official pricing: <https://docs.github.com/en/copilot/get-started/plans>

## At a glance

|  |  |
| --- | --- |
| Type | Vendor-hosted agent |
| Coding agents | Copilot; Claude and Codex agents (preview) |
| Environment / image | GitHub Actions runner; customise with copilot-setup-steps.yml |
| Isolation | Ephemeral GitHub Actions runner |
| API / programmatic | Issues, PRs, agents panel, CLI, IDEs, Slack/Jira/Linear |
| Persistence | No (ephemeral); pushed commits kept |
| When idle | not published |
| Max session | 59 minutes (hard limit) |
| Concurrency | No published limit; one branch and PR per task |
| Access | Session logs and PR on GitHub; no shell/SSH |
| Git integration | GitHub only; one copilot/ branch per task |
| Secrets | Repo/org 'Agents' secrets and variables |
| Network controls | Firewall with allowlist on by default |
| Run in your own cloud | Self-hosted Actions runners (firewall must be disabled) |
| Billing model | usage-based credits |
| Price (2 vCPU / 4 GiB) | Copilot plan + Actions minutes + AI credits |
| Storage | Actions storage |
| Plan fee | Pro $10/mo; Pro+ $39/mo; Max $100/mo; Business $19/seat; Enterprise $39/seat |
| Free tier / credits | Not included on Copilot Free |

## Details

- **Coding agents:** Copilot; Claude and Codex agents (preview). Vendor docs: "You can use third-party coding agents alongside Copilot cloud agent to work asynchronously on your development tasks." ([source](https://docs.github.com/en/copilot/concepts/agent-capabilities/about-agents/about-third-party-coding-agents))
- **Max session:** 59 minutes (hard limit). Vendor docs: "Each Copilot cloud agent session has a maximum execution time of 59 minutes. This limit cannot be extended or bypassed." ([source](https://docs.github.com/en/copilot/concepts/copilot-surfaces/copilot-on-github))

## Published pricing (verbatim)

- "Coding agents consume GitHub Actions minutes and AI credits. Each agent session consumes AI credits based on the model used and the number of tokens processed."
- "This total is converted into AI credits (1 AI credit = $0.01 USD)."

## Caveats

- Per-minute Actions rates depend on runner size. See GitHub Actions billing.
- Annual Pro/Pro+ subscribers on legacy billing are charged premium requests instead of AI credits.

## Sources

- <https://docs.github.com/en/copilot/concepts/agent-capabilities/about-agents/about-third-party-coding-agents>
- <https://docs.github.com/en/copilot/concepts/agents/about-third-party-coding-agents>
- <https://docs.github.com/en/copilot/concepts/agents/cloud-agent/risks-and-mitigations>
- <https://docs.github.com/en/copilot/concepts/billing-and-usage/individuals/billing>
- <https://docs.github.com/en/copilot/concepts/copilot-surfaces/copilot-on-github>
- <https://docs.github.com/en/copilot/get-started/plans>
- <https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/customize-cloud-agent/configure-secrets-and-variables>
- <https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/customize-cloud-agent/customize-the-agent-environment>
- <https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/customize-the-firewall>
- <https://docs.github.com/en/copilot/how-tos/copilot-on-github/use-copilot-agents/manage-and-track-agents>
<!-- END GENERATED: platform:copilot-cloud-agent -->

[← Back to the comparison](../README.md) · [Feature matrix](../comparisons/feature-matrix.md) · [Pricing](../comparisons/pricing.md)
