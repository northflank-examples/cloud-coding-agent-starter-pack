# Security and secrets for cloud coding agents

**Short answer:** give the agent an environment that contains only what the task needs: one repository, credentials scoped to that repository, limited network access, and a non-root user. Review everything it produces through a pull request. Treat any content the agent reads as potentially hostile.

## Threat model in one paragraph

A coding agent runs arbitrary shell commands, chosen by a model, based on text it reads. That text includes your repository, its dependencies, issue descriptions, web pages, and tool output, any of which can contain instructions written by someone else (**prompt injection**). The model can also simply make mistakes. So design the environment so that the worst thing the agent can do is limited to *a bad commit on a branch you review*. It should not be able to reach production data, other repositories, or a pushed release.

## 1. Repository access

| Method | Scope | Lifetime | Use when |
| --- | --- | --- | --- |
| **GitHub App installation token** | Selected repos, fine-grained permissions | 1 hour | Teams and automation. Not tied to a person |
| **Fine-grained personal access token** | Selected repos, fine-grained permissions | You choose (set an expiry) | Individuals getting started |
| **Deploy key** (SSH) | One repository | Until removed | A single long-lived workspace for one repo |
| ~~Classic PAT~~ | Every repo you can access | Often no expiry | Avoid |

Minimum permissions for an agent that pushes branches and opens PRs: **Contents: read & write**, **Pull requests: read & write**, **Metadata: read**. Add others (Issues, Actions) only when a task needs them.

**Protect the default branch.** Require pull requests and reviews on `main`, so a compromised or confused agent can't merge or force-push there, even with a write token.

**Don't store the token in the remote URL.** `https://TOKEN@github.com/...` is written to `.git/config`, where the agent (or anything it runs) can read it. Use a credential helper that reads the token from the environment, as [`entrypoint.sh`](../examples/cloud-agent-runner/entrypoint.sh) does.

## 2. Model API credentials

| Agent | Credential | Notes |
| --- | --- | --- |
| Claude Code | `ANTHROPIC_API_KEY` | Pay-per-token from the Claude Console. Create a dedicated key per environment or team, so you can revoke it and attribute cost |
| Claude Code | `CLAUDE_CODE_OAUTH_TOKEN` | Generated with `claude setup-token` and valid for one year. Tied to your subscription, so treat it like a password |
| Claude Code | Bedrock, Vertex AI, Foundry | Uses your cloud provider's IAM, so you can use workload identity instead of static keys |
| Codex | `CODEX_API_KEY` | Pass it only to the `codex exec` invocation that needs it |
| Codex | `~/.codex/auth.json` | Created by `codex login`. Contains access tokens, so never commit or share it |
| Cursor CLI | `CURSOR_API_KEY` | A user API key from the Cursor dashboard |
| GitHub Copilot CLI | `COPILOT_GITHUB_TOKEN` | A fine-grained PAT with only the "Copilot Requests" permission. Keep it separate from the token the agent pushes with. Without a system keychain, `copilot login` stores its token in plain text under `~/.copilot/` |
| Amp | `AMP_API_KEY` | A long-lived `sgamp_` access token |
| Factory Droid | `FACTORY_API_KEY` | From Factory's API key settings |
| Devin CLI | `~/.local/share/devin/credentials.toml` | Created by `devin auth login --force-manual-token-flow`. The token doesn't expire by default, so mount it as a secret file and revoke it when you're done |
| OpenCode, Pi, OMP, Crush, Aider, goose, Qwen Code | The provider's own key (`ANTHROPIC_API_KEY`, `OPENAI_API_KEY`, ...) | You pay the provider directly. Keys saved through the agent's own login land in plain-text files (`~/.local/share/opencode/auth.json`, `~/.pi/agent/auth.json`, goose's `secrets.yaml` when there's no keyring), so prefer environment variables |
| Gemini CLI | `GEMINI_API_KEY`, or a Vertex AI service account | For Vertex, use the cloud's workload identity where you can instead of a key file |

Each [agent guide](../agents/README.md) lists every documented credential option and where it's stored.

Set spending limits on API keys in the provider's console. For Claude Code headless runs, `--max-budget-usd` stops a single run at a spending cap.

## 3. Secret injection

- **Inject at runtime**: environment variables, your platform's secret store, or mounted secret files.
- **Never bake secrets into images.** Image layers are easy to extract and are often pushed to shared registries.
- **Don't expose secrets to code that doesn't need them.** If the agent runs your test suite, the tests can read every environment variable in the process. OpenAI's Codex docs specifically advise against setting API keys as job-wide variables in CI workflows that run repository-controlled code. Scope them to the agent invocation:

  ```bash
  CODEX_API_KEY="$(cat /run/secrets/codex)" codex exec --sandbox workspace-write "..."
  ```

- **Keep `.env` out of git.** This repo's [`.gitignore`](../.gitignore) does this.

## 4. Isolation

- **Run as a non-root user**, even in a container. The [example Dockerfile](../examples/cloud-agent-runner/Dockerfile) uses the image's built-in `node` user.
- **One task, one environment.** Don't let parallel agents share a working tree, a home directory, or credentials they don't each need.
- **Choose the isolation strength to match the input.** Standard containers share the host kernel. For untrusted input, or for multi-tenant platforms, use VMs, microVMs (Firecracker, Kata Containers), or gVisor. Northflank Cloud Harness, for example, runs each harness in its own microVM.
- **Agent-level sandboxing is in addition to this, not a replacement.** Codex's `--sandbox read-only|workspace-write`, Claude Code's permission modes and Factory Droid's `--auto` levels limit what the agent does inside the environment. Some agents (Pi, OMP, Amp, goose, Crush's `run` mode) don't ask before acting at all, so for them the environment is the only boundary. The environment's isolation limits what everything in it, including your test suite, can do.

## 5. Network access

- Allow outbound traffic to what the task needs: your git host, the model API, and package registries. Deny everything else where your platform supports egress policies.
- Don't put agent environments on the same network as production databases or internal admin services.
- If the agent needs an internal service (a staging API, a private package registry), grant that specific route, for example through a VPN or Tailscale ACL. Don't open up the whole network.
- Be careful exposing development servers publicly. Prefer authenticated port-forwarding or SSH tunnels.

## 6. Repository content is untrusted input

- **Headless runs execute project configuration.** Without `--bare`, `claude -p` loads the repository's `.claude/settings.json` hooks and `.mcp.json` servers *without* a trust prompt. For repositories or branches you don't control, run with `claude --bare -p ...` (which requires `ANTHROPIC_API_KEY`), or review those files first.
- **Issue and PR text are prompts.** An agent that triages public issues is reading text from strangers. Give it read-only access and no secrets.
- **Dependencies run code.** `npm install` and `pip install` execute install scripts. An agent that installs dependencies is running third-party code, so the isolation above applies.

## 7. Audit and review

- Log every run: who triggered it, the prompt, the agent's output (`--output-format json` / `codex exec --json`), the resulting diff, and the cost.
- All agent changes arrive as pull requests and go through the same CI and review as human changes.
- Rotate long-lived tokens on a schedule, and immediately if a log or workspace may have leaked one.

## Checklist

- [ ] Repository token scoped to one repo, with an expiry or short lifetime
- [ ] Default branch protected
- [ ] Token not in `.git/config` or the image
- [ ] Model API key dedicated to this use, with a spending limit
- [ ] Non-root user
- [ ] One environment per task (or per worktree)
- [ ] Egress limited where possible
- [ ] `--bare` (or reviewed config) for untrusted repositories
- [ ] Runs logged, and changes reviewed via PR
