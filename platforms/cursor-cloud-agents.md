# Cursor Cloud Agents: running coding agents in the cloud

Cursor runs its own agent in per-agent Firecracker microVMs on AWS. Cloud agents need Cursor Premium ($30/mo) or higher; model usage is billed at API pricing, and the infrastructure is included.

<!-- BEGIN GENERATED: platform:cursor-cloud-agents -->
Last verified: **2026-10-19** · Official pricing: <https://cursor.com/pricing>

## At a glance

|  |  |
| --- | --- |
| Type | Vendor-hosted agent |
| Coding agents | Cursor agent only |
| Environment / image | Ubuntu VM from agent setup, snapshot or Dockerfile; resources not published |
| Isolation | Firecracker microVM per agent |
| API / programmatic | Web, desktop, Slack, GitHub, Linear, API |
| Persistence | Environment snapshots kept 30 days of inactivity |
| When idle | Hibernated, then deleted on timers (values not published) |
| Max session | not published |
| Concurrency | No published limit |
| Access | Web/desktop UI; take control of the agent's remote desktop; no direct machine access |
| Git integration | GitHub, GitLab, Bitbucket Cloud, Azure DevOps |
| Secrets | Env vars, redacted runtime secrets, build secrets, OIDC |
| Network controls | All / default + allowlist / allowlist only; Tailscale, PrivateLink |
| Run in your own cloud | Self-hosted machines for tool execution (pools on Enterprise) |
| Billing model | included in a subscription |
| Price (2 vCPU / 4 GiB) | Cursor Premium ($30/mo) or higher + model usage at API rates |
| Storage | Included |
| Plan fee | Premium ($30/mo) or higher; Teams $30+/user/mo |
| Free tier / credits | None |

## Details

- **Coding agents:** Cursor agent only. Vendor docs: "Cloud Agents use a curated selection of models." ([source](https://cursor.com/docs/cloud-agent))
- **Isolation:** Firecracker microVM per agent. Vendor docs: "MicroVM isolation. Runtime workspaces run on Firecracker-based microVM infrastructure." ([source](https://cursor.com/docs/cloud-agent/security))
- **Persistence:** Environment snapshots kept 30 days of inactivity. Vendor docs: "Environment snapshots are stored for a maximum of 30 days of inactivity." ([source](https://cursor.com/docs/cloud-agent/security-network))
- **Concurrency:** No published limit. Vendor docs: "You can run as many agents as you want in parallel" ([source](https://cursor.com/docs/cloud-agent))
- **Access:** Web/desktop UI; take control of the agent's remote desktop; no direct machine access. Vendor docs: "Remote desktop control" ([source](https://cursor.com/docs/cloud-agent/capabilities))

## Published pricing (verbatim)

- "Cloud Agents are charged at API pricing for the selected model."
- "Cursor-managed Cloud Agents include the execution infrastructure."
- "Plans: Free $0, Plus $8, Premium $30, Super $100, Ultra $200, Teams $30+/user, Enterprise; "Cloud agents & automations" is not included on Free or Plus"

## Caveats

- Cursor's plans changed in 2026 (Free, Plus, Premium, Super, Ultra, Teams, Enterprise); cloud agents start at Premium. Check the pricing page for current names and prices.
- VM size, maximum run duration and idle timer values are not published.

## Sources

- <https://cursor.com/docs/cloud-agent>
- <https://cursor.com/docs/cloud-agent/capabilities>
- <https://cursor.com/docs/cloud-agent/security>
- <https://cursor.com/docs/cloud-agent/security-network>
- <https://cursor.com/docs/cloud-agent/security-network#network-access>
- <https://cursor.com/docs/cloud-agent/security-network#secret-protection>
- <https://cursor.com/docs/cloud-agent/self-hosted>
- <https://cursor.com/docs/cloud-agent/setup>
- <https://cursor.com/pricing>
<!-- END GENERATED: platform:cursor-cloud-agents -->

[← Back to the comparison](../README.md) · [Feature matrix](../comparisons/feature-matrix.md) · [Pricing](../comparisons/pricing.md)
