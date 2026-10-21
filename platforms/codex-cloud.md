# OpenAI Codex cloud: running coding agents in the cloud

Codex runs cloud tasks in per-task isolated VMs from an environment it prepares itself. VM size depends on your ChatGPT plan, and usage comes out of the plan's Codex allowance.

<!-- BEGIN GENERATED: platform:codex-cloud -->
Last verified: **2026-10-19** · Official pricing: <https://learn.chatgpt.com/docs/pricing>

## At a glance

|  |  |
| --- | --- |
| Type | Vendor-hosted agent |
| Coding agents | Codex only |
| Environment / image | Plus: 2 vCPU / 8 GiB / 8 GiB disk; Pro/Business/Enterprise: 4 vCPU / 16 GiB / 32 GiB |
| Isolation | Isolated VM workspace per task |
| API / programmatic | Web, mobile, desktop, `codex cloud` CLI |
| Persistence | Task state recoverable up to 7 days |
| When idle | not published |
| Max session | not published |
| Concurrency | not published |
| Access | Web/mobile/desktop UI; `codex apply` pulls the diff local; no shell/SSH |
| Git integration | GitHub only |
| Secrets | Env vars; network secrets via proxy placeholder |
| Network controls | Package managers / custom domains / unrestricted; Tailscale |
| Run in your own cloud | not published |
| Billing model | included in a subscription |
| Price (2 vCPU / 4 GiB) | Included in ChatGPT plans (Plus $20/mo and up) |
| Storage | Included |
| Plan fee | Plus $20/mo; Pro $100/$200/$500/mo; Business $20/user/mo (2+ users, annual) |
| Free tier / credits | None (not on Free or Go) |

## Details

- **Environment / image:** Plus: 2 vCPU / 8 GiB / 8 GiB disk; Pro/Business/Enterprise: 4 vCPU / 16 GiB / 32 GiB. Vendor docs: "Each cloud task runs in a VM with these default resources: | Plus, Edu Plus | 2 | 8 GiB | 8 GiB | | Pro, Business, Enterprise | 4 | 16 GiB | 32 GiB |" ([source](https://learn.chatgpt.com/docs/environments/cloud-environments#vm-specifications))
- **Isolation:** Isolated VM workspace per task. Vendor docs: "Each new task gets its own isolated workspace from the published environment." ([source](https://learn.chatgpt.com/docs/environments/cloud-environments))
- **Persistence:** Task state recoverable up to 7 days. Vendor docs: "By default, a task's saved VM state is recoverable for up to seven days after you last start a turn or resume the task." ([source](https://learn.chatgpt.com/docs/environments/cloud-environments))

## Published pricing (verbatim)

- "Local messages and cloud chats share your plan's usage allowance. Weekly limits may also apply."
- "Cloud tasks may use more of your allowance than local messages."
- "[API Key] No cloud-based features (GitHub code review, Slack, etc.)"

## Caveats

- Max task duration, idle behaviour, concurrency limits and isolation technology are not published.
- Larger or custom VMs on Enterprise are priced separately through OpenAI sales.

## Sources

- <https://learn.chatgpt.com/docs/cloud>
- <https://learn.chatgpt.com/docs/developer-commands?surface=cli>
- <https://learn.chatgpt.com/docs/environments/cloud-environments>
- <https://learn.chatgpt.com/docs/environments/cloud-environments#configure-environment-variables-and-network-secrets>
- <https://learn.chatgpt.com/docs/environments/cloud-environments#connect-to-services>
- <https://learn.chatgpt.com/docs/environments/cloud-environments#current-limitations>
- <https://learn.chatgpt.com/docs/environments/cloud-environments#vm-specifications>
- <https://learn.chatgpt.com/docs/pricing>
<!-- END GENERATED: platform:codex-cloud -->

[← Back to the comparison](../README.md) · [Feature matrix](../comparisons/feature-matrix.md) · [Pricing](../comparisons/pricing.md)
