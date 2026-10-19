# Cloud coding agent platforms: feature matrix

Every value is generated from [`data/platforms.json`](../data/platforms.json) and links back to the vendor's docs on each [platform page](../platforms/). "not published" means the vendor doesn't document it. It never means "no" or "unlimited".

## Agents and environment

Which coding agents run there, what the environment is built from, how it's isolated, and whether you can drive it programmatically.

<!-- BEGIN GENERATED: features-agents -->
| Platform | Coding agents | Environment / image | Isolation | API / programmatic |
| --- | --- | --- | --- | --- |
| [Northflank Cloud Harness](../platforms/northflank.md) | Claude Code, Codex, Cursor, OpenCode, Pi, Devin CLI, OMP; any other agent in an empty sandbox | Northflank harness image, your own build, or any registry image; CPU/RAM from 0.1 to 32 vCPU plans | Kata microVM per harness | REST API, JavaScript SDK, Python SDK, CLI, dashboard |
| [Claude Code on the web](../platforms/claude-code-web.md) | Claude Code only | Ubuntu 24.04 VM, ~4 vCPU / 16 GB / 30 GB; setup script; base image not replaceable | Isolated VM per session | Web, mobile, desktop, `claude --cloud` CLI |
| [Cursor Cloud Agents](../platforms/cursor-cloud-agents.md) | Cursor agent only | Ubuntu VM from agent setup, snapshot or Dockerfile; resources not published | Firecracker microVM per agent | Web, desktop, Slack, GitHub, Linear, API |
| [GitHub Copilot cloud agent](../platforms/copilot-cloud-agent.md) | Copilot; Claude and Codex agents (preview) | GitHub Actions runner; customise with copilot-setup-steps.yml | Ephemeral GitHub Actions runner | Issues, PRs, agents panel, CLI, IDEs, Slack/Jira/Linear |
| [OpenAI Codex cloud](../platforms/codex-cloud.md) | Codex only | Plus: 2 vCPU / 8 GiB / 8 GiB disk; Pro/Business/Enterprise: 4 vCPU / 16 GiB / 32 GiB | Isolated VM workspace per task | Web, mobile, desktop, `codex cloud` CLI |
| [Coder](../platforms/coder.md) | Claude Code, Codex, any terminal agent; Coder Agents | Terraform templates (VMs, Kubernetes pods, Docker) | Whatever your template provisions | REST API, CLI, Terraform |
| [GitHub Codespaces](../platforms/github-codespaces.md) | Any CLI agent you install (devcontainer) | devcontainer.json; 2 to 32 core machines | Container on a dedicated VM | REST API, `gh codespace` CLI |
| [Ona (formerly Gitpod)](../platforms/ona.md) | Codex agent built in; Claude Code etc. inside environments | Dev Container config; Standard 4 vCPU / 16 GB | VM per environment | Ona CLI and API |
| [Daytona](../platforms/daytona.md) | Claude Code, Codex, OpenCode preinstalled; any agent | Snapshots (images); default 1 vCPU / 1 GB, max 4 vCPU / 8 GB per sandbox by default | Container by default; optional VM | Python/TS/Go/Java/Ruby SDKs, REST API, CLI |
| [E2B](../platforms/e2b.md) | Templates: Claude Code, Codex, Amp, OpenCode; any agent | Custom templates; 10 GiB disk (Hobby), 20 GiB (Pro) | Firecracker microVM | JS/Python SDK, REST API, CLI |
| [Modal Sandboxes](../platforms/modal.md) | Any agent you install; official Claude Code and OpenCode examples | Any image via `modal.Image` or a registry | gVisor or VM runtime (Modal picks if unset) | Python SDK; JavaScript and Go SDKs (beta); CLI |
| [Sprites (Fly.io)](../platforms/sprites.md) | Claude Code, Codex, Gemini CLI, Cursor preinstalled; any agent | Ubuntu 25.10, 100 GB volume | Hardware-isolated VM | REST/WebSocket API, SDKs, `sprite` CLI, MCP |
<!-- END GENERATED: features-agents -->

## Lifecycle

What happens to the workspace between tasks, when it's idle, and how long one session can run. This decides whether a platform suits long-running agents.

<!-- BEGIN GENERATED: features-lifecycle -->
| Platform | Persistence | When idle | Max session | Concurrency |
| --- | --- | --- | --- | --- |
| [Northflank Cloud Harness](../platforms/northflank.md) | Yes: persistent workspace volume, 5–100 GiB (on by default) | Runs until paused; paused = no compute charge | No limit | 1 harness on free projects; no limit on paid |
| [Claude Code on the web](../platforms/claude-code-web.md) | Setup snapshot cached ~7 days; session files kept while paused | VM pauses after a few idle minutes; may be reclaimed | not published | No published cap; shares plan rate limits |
| [Cursor Cloud Agents](../platforms/cursor-cloud-agents.md) | Environment snapshots kept 30 days of inactivity | Hibernated, then deleted on timers (values not published) | not published | No published limit |
| [GitHub Copilot cloud agent](../platforms/copilot-cloud-agent.md) | No (ephemeral); pushed commits kept | not published | 59 minutes (hard limit) | No published limit; one branch and PR per task |
| [OpenAI Codex cloud](../platforms/codex-cloud.md) | Task state recoverable up to 7 days | not published | not published | not published |
| [Coder](../platforms/coder.md) | Defined by template | Template autostop / inactivity timeout | No platform limit | Unlimited workspaces; 5 active Coder Agents on Community |
| [GitHub Codespaces](../platforms/github-codespaces.md) | Yes; stopped codespaces deleted after 30 days inactive | Stops after 30 min idle (5–240 configurable) | 12 hours | Limits exist but aren't published |
| [Ona (formerly Gitpod)](../platforms/ona.md) | Yes; archived after 3 days stopped (Core) | Auto-stop after 30 min (configurable) | No published limit | not published |
| [Daytona](../platforms/daytona.md) | Yes by default; archived after 7 days stopped | Containers auto-stop after 15 min idle; VMs auto-pause after 60 min (defaults) | No limit (auto-stop can be disabled) | Tiered vCPU/RAM pools (Tier 1: 10 vCPU) |
| [E2B](../platforms/e2b.md) | Opt-in pause/resume; paused kept indefinitely | Killed after 5 min timeout by default (can pause instead) | 1 h (Hobby) / 24 h (Pro) continuous; pausing resets | 20 (Hobby); 100–1,100 (Pro with add-ons) |
| [Modal Sandboxes](../platforms/modal.md) | Volumes; filesystem snapshots (30-day default TTL) | Optional `idle_timeout` terminates the sandbox | 5 min default, up to 24 h; snapshot to continue | Starter 100 / Team 5,000 containers |
| [Sprites (Fly.io)](../platforms/sprites.md) | Yes: disk persists; checkpoints | Pauses after ~30 s idle; no compute charge | No limit (persistent); task holds up to 1 h, renewable | Per-plan (Hero: 100 running) |
<!-- END GENERATED: features-lifecycle -->

## Access and integration

How you (and your teammates) reach the agent's environment, which git providers work, and how secrets get in.

<!-- BEGIN GENERATED: features-access -->
| Platform | Access | Git integration | Secrets |
| --- | --- | --- | --- |
| [Northflank Cloud Harness](../platforms/northflank.md) | Web terminal, SSH, VS Code / Cursor over SSH; teammates can share a harness | GitHub, GitLab, Bitbucket, Azure DevOps or self-hosted Git; clone a branch, create a new branch or a new repository, plus additional repositories | Runtime variables and secret files; agent API key or linked account |
| [Claude Code on the web](../platforms/claude-code-web.md) | Web/mobile/desktop UI; `claude --teleport` pulls a session local; no shell/SSH | GitHub (and GHE Server on Team/Enterprise); pushes branches | Env vars; network secrets injected by proxy outside the VM |
| [Cursor Cloud Agents](../platforms/cursor-cloud-agents.md) | Web/desktop UI; take control of the agent's remote desktop; no direct machine access | GitHub, GitLab, Bitbucket Cloud, Azure DevOps | Env vars, redacted runtime secrets, build secrets, OIDC |
| [GitHub Copilot cloud agent](../platforms/copilot-cloud-agent.md) | Session logs and PR on GitHub; no shell/SSH | GitHub only; one copilot/ branch per task | Repo/org 'Agents' secrets and variables |
| [OpenAI Codex cloud](../platforms/codex-cloud.md) | Web/mobile/desktop UI; `codex apply` pulls the diff local; no shell/SSH | GitHub only | Env vars; network secrets via proxy placeholder |
| [Coder](../platforms/coder.md) | Web terminal, SSH, VS Code, JetBrains, Cursor | Any provider (external auth) | User secrets, Vault integration |
| [GitHub Codespaces](../platforms/github-codespaces.md) | Browser VS Code, VS Code, JetBrains, `gh codespace ssh` | GitHub only | User/repo/org Codespaces secrets |
| [Ona (formerly Gitpod)](../platforms/ona.md) | Browser VS Code, VS Code, Cursor, JetBrains, SSH | GitHub, GitLab, Bitbucket, Azure DevOps | Org/project/user secrets |
| [Daytona](../platforms/daytona.md) | Web terminal, SSH, VS Code / JetBrains over SSH | SDK git operations (clone, commit, push) | Org secrets swapped in by outbound proxy |
| [E2B](../platforms/e2b.md) | SDK terminal (PTY); SSH via custom template + proxy | Via commands in the sandbox | Secrets store injected by egress proxy; env vars |
| [Modal Sandboxes](../platforms/modal.md) | `modal shell`, exec with PTY, Tunnels; no SSH | None built in; clone inside the sandbox | `modal.Secret` |
| [Sprites (Fly.io)](../platforms/sprites.md) | `sprite console` shell; no built-in SSH | git preinstalled; GitHub connector | Connectors via API gateway (agent never sees token) |
<!-- END GENERATED: features-access -->

## Network and deployment

Network controls and whether the platform can run inside your own cloud account.

<!-- BEGIN GENERATED: features-security -->
| Platform | Network controls | Run in your own cloud |
| --- | --- | --- |
| [Northflank Cloud Harness](../platforms/northflank.md) | Public/private ports, custom domains, per-port IP/SSO/basic-auth rules | Yes, self-serve: AWS, AWS European Sovereign Cloud, GCP, Azure, Oracle, Civo, CoreWeave, Nebius; or import your own Kubernetes cluster (BYOK) |
| [Claude Code on the web](../platforms/claude-code-web.md) | None / Trusted allowlist (default) / Full / Custom | Self-hosted runners, public beta (Team/Enterprise) |
| [Cursor Cloud Agents](../platforms/cursor-cloud-agents.md) | All / default + allowlist / allowlist only; Tailscale, PrivateLink | Self-hosted machines for tool execution (pools on Enterprise) |
| [GitHub Copilot cloud agent](../platforms/copilot-cloud-agent.md) | Firewall with allowlist on by default | Self-hosted Actions runners (firewall must be disabled) |
| [OpenAI Codex cloud](../platforms/codex-cloud.md) | Package managers / custom domains / unrestricted; Tailscale | not published |
| [Coder](../platforms/coder.md) | Your infrastructure; Agent Firewall (Premium) | Self-hosted only |
| [GitHub Codespaces](../platforms/github-codespaces.md) | Private/org/public forwarded ports; no egress allowlist documented | No |
| [Ona (formerly Gitpod)](../platforms/ona.md) | Standard on Ona Cloud; full (PrivateLink, VPN) on customer VPC | Enterprise: runners in your AWS or GCP |
| [Daytona](../platforms/daytona.md) | Restricted on Tier 1–2; allowlists/block-all on Tier 3–4 | Bring your own compute (custom regions) |
| [E2B](../platforms/e2b.md) | Internet on/off, CIDR/hostname allow and deny lists | Enterprise only (AWS, GCP, Azure) |
| [Modal Sandboxes](../platforms/modal.md) | `block_network`, CIDR and domain allowlists (beta) | No (not published) |
| [Sprites (Fly.io)](../platforms/sprites.md) | Opt-in DNS allow/deny policy | No |
<!-- END GENERATED: features-security -->

## Reading the matrix

- **"Run any agent CLI"** is the biggest structural difference. Managed harnesses (Northflank), cloud dev environments (Codespaces, Coder, Ona) and sandbox platforms (E2B, Daytona, Sprites, Modal) are agent-agnostic. Vendor-hosted products (Claude Code on the web, Codex cloud, Cursor) run their own agent.
- **Isolation** ranges from containers (Daytona's default) to a VM or microVM per workspace (Northflank, Codespaces, Ona, E2B, Cursor, Sprites, Claude Code on the web). For agents running untrusted code or reading untrusted input, prefer VM-level isolation. See [security and secrets](../guides/security-and-secrets.md).
- **Max session** matters for long migrations and multi-hour refactors. Copilot's 59-minute limit and Codespaces' 12-hour lifetime are hard limits. E2B's limit resets when you pause.

[← Back to the comparison](../README.md) · [Pricing](pricing.md) · [Methodology](../methodology.md)
