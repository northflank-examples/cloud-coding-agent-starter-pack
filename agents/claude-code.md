# How to run Claude Code in the cloud

Anthropic's terminal coding agent. This guide covers running Claude Code on a remote machine instead of your laptop: on Northflank Cloud Harness, on any Linux VM, or in a container. It shows how to install it, log in without a browser, run tasks headlessly with permission prompts off, and what to watch for. Every fact below is quoted from or linked to the vendor's own documentation.

<!-- BEGIN GENERATED: agent:claude-code -->
Last verified: **2026-10-19** · Docs: <https://code.claude.com/docs/en/overview> · Source: <https://github.com/anthropics/claude-code>

## At a glance

|  |  |
| --- | --- |
| Made by | Anthropic |
| Licence | Proprietary |
| Models | Claude models only: Anthropic API or subscription, Amazon Bedrock, Google Vertex AI, Microsoft Foundry, or an Anthropic-compatible gateway |
| Headless command | `claude -p "<task>"` |
| Skip permission prompts | `--permission-mode acceptEdits` plus `--allowedTools`; `--dangerously-skip-permissions` for full bypass (refused as root) |
| JSON output | `--output-format json` or `stream-json` |
| Resume a session | `--continue` / `--resume <session-id>` |
| Choose a model | `--model <alias or name>` |
| Auth on a server | `ANTHROPIC_API_KEY`, or `CLAUDE_CODE_OAUTH_TOKEN` for a subscription |
| Instructions file | `CLAUDE.md`; reads `AGENTS.md` only when there's no `CLAUDE.md` |
| Config and credentials | `~/.claude/` and `~/.claude.json`; Linux credentials in `~/.claude/.credentials.json` |
| Built-in sandbox | Optional: bubblewrap on Linux, Seatbelt on macOS (shell commands only) |
| MCP | Yes: `claude mcp add`, `.mcp.json`, `--mcp-config` |
| Northflank Cloud Harness | built in |
| Billing | Claude Pro, Max, Team or Enterprise subscription, or pay-per-token API |

## Option 1: Run Claude Code on Northflank Cloud Harness

Claude Code is one of the agents Cloud Harness sets up for you: each harness is an isolated microVM with Claude Code preinstalled, your repository cloned, a persistent workspace, a web terminal and SSH access.

1. In [Northflank](https://app.northflank.com), open a project → **Harnesses** → **Create harness**.
2. Choose **Claude Code** as the agent, then pick Northflank's cloud or your own cloud account.
3. Authentication: an Anthropic API key, or sign in with your Claude account in the harness terminal.
4. Select the repository and branch, then **Create harness**. The terminal opens with the agent ready.

To start one harness per task from a script instead, use [`launch.sh`](../examples/northflank-parallel-harnesses/README.md) with `AGENT=claude-code`:

```bash
AGENT=claude-code AGENT_API_KEY=... NF_PROJECT=my-project \
REPO_URL=https://github.com/your-org/your-repo \
  ./launch.sh tasks.txt
```

Pause the harness when you're done: compute stops and the workspace is kept. See the [Cloud Harness tutorial](../tutorials/northflank-cloud-harness/README.md).

## Option 2: Run Claude Code on any Linux VM or container

### 1. Install

**Install script**:

```bash
curl -fsSL https://claude.ai/install.sh | bash
```

**npm** (requires Node.js 22+):

```bash
npm install -g @anthropic-ai/claude-code
```

Check it worked: `claude --version`. Install docs: <https://code.claude.com/docs/en/setup>.

### 2. Authenticate without a browser

Cloud machines usually can't open a browser login, so use one of these:

| Method | Environment variables | How |
| --- | --- | --- |
| API key (Claude Console) | `ANTHROPIC_API_KEY` | export ANTHROPIC_API_KEY=sk-ant-...; in -p mode the key is always used when present, no browser needed. Required for --bare mode. ([source](https://code.claude.com/docs/en/authentication)) |
| Subscription (Pro/Max/Team/Enterprise) long-lived OAuth token | `CLAUDE_CODE_OAUTH_TOKEN` | Run `claude setup-token` on a machine with a browser (one-year token, printed not saved), then export CLAUDE_CODE_OAUTH_TOKEN=<token> on the server. Not read in --bare mode. Can only make model requests (no Remote Control / claude.ai connectors). ([source](https://code.claude.com/docs/en/authentication)) |
| Subscription interactive login over SSH/container | — | Run `claude`, open the printed login URL in any browser, then paste the code shown back into the terminal at 'Paste code here if prompted'. Credentials saved to ~/.claude/.credentials.json (mode 0600) on Linux. ([source](https://code.claude.com/docs/en/authentication)) |
| Cloud provider (Amazon Bedrock, Google Cloud Agent Platform/Vertex AI, Microsoft Foundry) | `CLAUDE_CODE_USE_BEDROCK`, `CLAUDE_CODE_USE_VERTEX`, `CLAUDE_CODE_USE_FOUNDRY` | Set the provider env var plus that provider's normal credentials before running claude; no browser login needed. ([source](https://code.claude.com/docs/en/authentication)) |
| LLM gateway / proxy bearer token | `ANTHROPIC_AUTH_TOKEN`, `ANTHROPIC_BASE_URL` | Set ANTHROPIC_BASE_URL to the gateway and ANTHROPIC_AUTH_TOKEN to its bearer token. ([source](https://code.claude.com/docs/en/authentication)) |

### 3. Run a task headlessly

Work on a branch, let the agent finish without prompts, then commit and push for review:

```bash
git switch -c agent/my-task
claude -p "Fix the failing tests" --permission-mode acceptEdits \
  --allowedTools "Read,Edit,Write,Bash" --output-format json
git add -A && git commit -m "agent: my task" && git push -u origin HEAD
```

| Part | What it does |
| --- | --- |
| `-p` | Print mode: run the task without the interactive UI, print the result and exit |
| `--permission-mode acceptEdits` | File edits don't need approval |
| `--allowedTools "Read,Edit,Write,Bash"` | These tools run without prompting. `Bash` allows any command, so use it only in an isolated environment |
| `--output-format json` | One JSON object with the result, `session_id` and `total_cost_usd` |

- **Headless mode:** Prints the response to stdout and exits. Exit code 0 on success, non-zero on failure; failures inside the run (e.g. missing auth) are printed as the result on stdout. Reads piped stdin (capped at 10MB). --bare skips hooks, plugins, MCP, CLAUDE.md, auto memory and is recommended for scripts/CI. SIGTERM exits with code 143. Docs: "Claude Code exits with code 0 on success and a non-zero code when the run fails, so your scripts can branch on the exit status." ([source](https://code.claude.com/docs/en/headless))

- **Permissions:** Docs recommend bypassPermissions only in isolated containers/VMs. On Linux/macOS Claude Code refuses --dangerously-skip-permissions when running as root or under sudo (check skipped inside a recognized sandbox); run as a non-root user. Deny rules still apply in bypassPermissions. Docs: "Run fully unattended inside a container | `claude -p "<prompt>" --dangerously-skip-permissions`" ([source](https://code.claude.com/docs/en/permission-modes))

### 4. Or use this repo's container

[`examples/cloud-agent-runner`](../examples/cloud-agent-runner/README.md) builds an image with Claude Code (and any other agents you list) and runs one task per container:

```bash
cd examples/cloud-agent-runner
docker build --build-arg AGENTS="claude-code" -t cloud-agent .
docker run --rm --env-file .env cloud-agent run-task.sh claude-code "Fix the failing tests"
```

## Gotchas when running in the cloud

- --dangerously-skip-permissions is refused when running as root or under sudo on Linux/macOS; create a non-root user in the container. ([source](https://code.claude.com/docs/en/permission-modes))
- --bare does not read CLAUDE_CODE_OAUTH_TOKEN or OAuth/keychain credentials; use ANTHROPIC_API_KEY or apiKeyHelper with --bare. ([source](https://code.claude.com/docs/en/headless))
- Without --bare, a -p session runs project hooks and connects .mcp.json servers even in an untrusted folder, with no trust dialog. ([source](https://code.claude.com/docs/en/headless))
- Login in SSH/containers: browser can't reach the local callback, so paste the code shown in the browser back into the terminal. ([source](https://code.claude.com/docs/en/authentication))
- Bubblewrap sandbox fails in unprivileged containers ('Can't mount proc'); set enableWeakerNestedSandbox=true only when the container is the isolation boundary. ([source](https://code.claude.com/docs/en/sandboxing))
- Ubuntu 24.04+ AppArmor blocks bubblewrap user namespaces by default. ([source](https://code.claude.com/docs/en/sandboxing))
- Alpine/musl requires bash, curl, libgcc, libstdc++, ripgrep and USE_BUILTIN_RIPGREP=0. ([source](https://code.claude.com/docs/en/setup))
- Native install auto-updates in the background; set DISABLE_AUTOUPDATER or DISABLE_UPDATES to pin versions in images. ([source](https://code.claude.com/docs/en/setup))
- A -p run may wait up to 10 minutes idle for background work before exiting (CLAUDE_CODE_PRINT_BG_WAIT_CEILING_MS). ([source](https://code.claude.com/docs/en/headless))
- In -p, an unset permission mode takes the built-in starting mode, which can be auto; pass --permission-mode explicitly. ([source](https://code.claude.com/docs/en/headless))

## Not documented / open questions

- Exact Bedrock/Vertex/Foundry companion env vars (AWS_REGION, ANTHROPIC_VERTEX_PROJECT_ID, CLOUD_ML_REGION etc.) not verified in this pass; see provider pages.
- npm latest (2.1.301) may differ from the native installer 'stable' channel version.
- Which environments count as a 'recognized sandbox' that skips the root check is not enumerated in the fetched docs.

## Sources

- <https://code.claude.com/docs/en/authentication>
- <https://code.claude.com/docs/en/cli-reference>
- <https://code.claude.com/docs/en/env-vars>
- <https://code.claude.com/docs/en/headless>
- <https://code.claude.com/docs/en/mcp>
- <https://code.claude.com/docs/en/memory>
- <https://code.claude.com/docs/en/permission-modes>
- <https://code.claude.com/docs/en/sandboxing>
- <https://code.claude.com/docs/en/setup>
- <https://github.com/anthropics/claude-code/blob/main/LICENSE.md>
<!-- END GENERATED: agent:claude-code -->

---

See all agents: [agent comparison](README.md) · [Run any agent in parallel on Northflank](../examples/northflank-parallel-harnesses/README.md) · [Running agents headlessly](../guides/running-agents-headless.md)
