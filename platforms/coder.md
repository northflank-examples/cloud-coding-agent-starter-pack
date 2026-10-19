# Coder: running coding agents in the cloud

Self-hosted, open-source (AGPL-3.0) platform for Terraform-defined workspaces on your own infrastructure. It can run Claude Code, Codex or any terminal agent, plus its own Coder Agents.

<!-- BEGIN GENERATED: platform:coder -->
Last verified: **2026-10-19** · Official pricing: <https://coder.com/pricing>

## At a glance

|  |  |
| --- | --- |
| Type | Cloud dev environment |
| Coding agents | Claude Code, Codex, any terminal agent; Coder Agents |
| Environment / image | Terraform templates (VMs, Kubernetes pods, Docker) |
| Isolation | Whatever your template provisions |
| API / programmatic | REST API, CLI, Terraform |
| Persistence | Defined by template |
| When idle | Template autostop / inactivity timeout |
| Max session | No platform limit |
| Concurrency | Unlimited workspaces; 5 active Coder Agents on Community |
| Access | Web terminal, SSH, VS Code, JetBrains, Cursor |
| Git integration | Any provider (external auth) |
| Secrets | User secrets, Vault integration |
| Network controls | Your infrastructure; Agent Firewall (Premium) |
| Run in your own cloud | Self-hosted only |
| Billing model | self-hosted licence + your cloud |
| Price (2 vCPU / 4 GiB) | Free (open source) or per-user licence, plus your cloud |
| Storage | Your cloud provider |
| Plan fee | Community free; Premium per user (not published) |
| Free tier / credits | Community edition (open source) |

## Details

- **Coding agents:** Claude Code, Codex, any terminal agent; Coder Agents. Vendor docs: "Template admins can install terminal-based coding agents, such as Claude Code or Codex, directly into a workspace template using a registry module." ([source](https://coder.com/docs/ai-coder))
- **Isolation:** Whatever your template provisions. Vendor docs: "Templates describe the infrastructure for each workspace, from EC2 VMs and Kubernetes Pods to Docker containers." ([source](https://coder.com/docs/about))

## Published pricing (verbatim)

- "Community Free For hobbyists and small teams ready to join Coder's open-source community."
- "Premium Annually per user"

## Caveats and open questions

- Coder Tasks was removed in v2.34. Older comparisons that mention it are out of date.
- You operate the control plane and the infrastructure yourself.

## Sources

- <https://coder.com/docs>
- <https://coder.com/docs/about>
- <https://coder.com/docs/admin/external-auth>
- <https://coder.com/docs/admin/templates/managing-templates/schedule>
- <https://coder.com/docs/ai-coder>
- <https://coder.com/docs/ai-coder/agent-firewall>
- <https://coder.com/docs/ai-coder/agents/licensing-usage>
- <https://coder.com/docs/install>
- <https://coder.com/docs/user-guides/user-secrets>
- <https://coder.com/docs/user-guides/workspace-access>
- <https://coder.com/docs/user-guides/workspace-scheduling>
- <https://coder.com/pricing>
<!-- END GENERATED: platform:coder -->

[← Back to the comparison](../README.md) · [Feature matrix](../comparisons/feature-matrix.md) · [Pricing](../comparisons/pricing.md)
