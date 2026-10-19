# Claude Code on the web: running coding agents in the cloud

Anthropic runs Claude Code sessions in isolated, Anthropic-managed VMs (about 4 vCPU, 16 GB RAM, 30 GB disk). Sessions count toward your Claude plan's usage limits, with no separate charge for the VM.

<!-- BEGIN GENERATED: platform:claude-code-web -->
Last verified: **2026-10-19** · Official pricing: <https://claude.com/pricing>

## At a glance

|  |  |
| --- | --- |
| Type | Vendor-hosted agent |
| Coding agents | Claude Code only |
| Environment / image | Ubuntu 24.04 VM, ~4 vCPU / 16 GB / 30 GB; setup script; base image not replaceable |
| Isolation | Isolated VM per session |
| API / programmatic | Web, mobile, desktop, `claude --cloud` CLI |
| Persistence | Setup snapshot cached ~7 days; session files kept while paused |
| When idle | VM pauses after a few idle minutes; may be reclaimed |
| Max session | not published |
| Concurrency | No published cap; shares plan rate limits |
| Access | Web/mobile/desktop UI; `claude --teleport` pulls a session local; no shell/SSH |
| Git integration | GitHub (and GHE Server on Team/Enterprise); pushes branches |
| Secrets | Env vars; network secrets injected by proxy outside the VM |
| Network controls | None / Trusted allowlist (default) / Full / Custom |
| Run in your own cloud | Self-hosted runners, public beta (Team/Enterprise) |
| Billing model | included in a subscription |
| Price (2 vCPU / 4 GiB) | Included in Claude plans (Pro $20/mo and up) |
| Storage | Included |
| Plan fee | Pro $20/mo; Max from $100/mo; Team $25–$125/seat/mo |
| Free tier / credits | None (not on the free plan) |

## Details

- **Coding agents:** Claude Code only. Vendor docs: "A cloud session is a Claude Code session that runs on cloud infrastructure instead of on your machine." ([source](https://code.claude.com/docs/en/claude-code-on-the-web))
- **Environment / image:** Ubuntu 24.04 VM, ~4 vCPU / 16 GB / 30 GB; setup script; base image not replaceable. Vendor docs: "Cloud sessions in Anthropic-hosted environments run with approximate resource ceilings that may change over time: 4 vCPUs, 16 GB of RAM, 30 GB of disk" ([source](https://code.claude.com/docs/en/cloud-environments))
- **Isolation:** Isolated VM per session. Vendor docs: "Isolated virtual machines: each session runs in an isolated, Anthropic-managed VM." ([source](https://code.claude.com/docs/en/claude-code-on-the-web#security-and-isolation))
- **Persistence:** Setup snapshot cached ~7 days; session files kept while paused. Vendor docs: "When setup completes within roughly five minutes, Anthropic snapshots the filesystem and reuses that snapshot as the starting point for later sessions" ([source](https://code.claude.com/docs/en/cloud-environments#environment-caching))
- **When idle:** VM pauses after a few idle minutes; may be reclaimed. Vendor docs: "after a few minutes without activity, a session's VM pauses with its files saved." ([source](https://code.claude.com/docs/en/cloud-environments#time-limits))
- **Max session:** No maximum session length is published. Foreground and background commands have default timeouts (10 and 30 minutes) that can be raised. ([source](https://code.claude.com/docs/en/cloud-environments#time-limits))
- **Concurrency:** No published cap; shares plan rate limits. Vendor docs: "cloud sessions share rate limits with all other Claude and Claude Code usage within your account. Running multiple tasks in parallel consumes more rate limits proportionately." ([source](https://code.claude.com/docs/en/claude-code-on-the-web#limitations))
- **Run in your own cloud:** Self-hosted runners, public beta (Team/Enterprise). Vendor docs: "Self-hosted environments are in public beta on Team and Enterprise plans and are off by default." ([source](https://code.claude.com/docs/en/self-hosted-environments))

## Published pricing (verbatim)

- "Cloud sessions are available on Pro, Max, and Team plans, and for Enterprise users with premium seats or Chat + Claude Code seats."
- "It counts toward your plan's usage limits alongside the rest of your Claude and Claude Code usage, and there's no separate charge for the cloud VM."
- "$17 Per month with annual subscription discount ( $200 billed up front). $20 if billed monthly."

## Caveats and open questions

- No documented way to run another agent (such as Codex) in a cloud session.
- Organisations with ZDR, HIPAA or CMEK can't use cloud sessions.

## Sources

- <https://claude.com/pricing>
- <https://code.claude.com/docs/en/claude-code-on-the-web>
- <https://code.claude.com/docs/en/claude-code-on-the-web#continue-a-cloud-session-in-your-terminal>
- <https://code.claude.com/docs/en/claude-code-on-the-web#limitations>
- <https://code.claude.com/docs/en/claude-code-on-the-web#security-and-isolation>
- <https://code.claude.com/docs/en/cloud-environments>
- <https://code.claude.com/docs/en/cloud-environments#access-levels>
- <https://code.claude.com/docs/en/cloud-environments#add-network-secrets>
- <https://code.claude.com/docs/en/cloud-environments#environment-caching>
- <https://code.claude.com/docs/en/cloud-environments#time-limits>
- <https://code.claude.com/docs/en/self-hosted-environments>
<!-- END GENERATED: platform:claude-code-web -->

[← Back to the comparison](../README.md) · [Feature matrix](../comparisons/feature-matrix.md) · [Pricing](../comparisons/pricing.md)
