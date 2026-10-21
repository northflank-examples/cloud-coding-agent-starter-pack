# How to run Codex CLI in the cloud

OpenAI's open-source terminal coding agent. This guide covers running Codex CLI on a remote machine instead of your laptop: on Northflank Cloud Harness, on any Linux VM, or in a container. It shows how to install it, log in without a browser, run tasks headlessly with permission prompts off, and what to watch for. Every fact below is quoted from or linked to the vendor's own documentation.

<!-- BEGIN GENERATED: agent:codex -->
Last verified: **2026-10-19** · Docs: <https://learn.chatgpt.com/docs/developer-commands?surface=cli> · Source: <https://github.com/openai/codex>

## At a glance

|  |  |
| --- | --- |
| Made by | OpenAI |
| Licence | Apache-2.0 (open source) |
| Models | OpenAI models by default; other providers via `model_providers` in `config.toml`; local models with `--oss` (Ollama, LM Studio) |
| Headless command | `codex exec "<task>"` |
| Skip permission prompts | `--sandbox workspace-write` (edits), `--approve-for-me`, or `--sandbox danger-full-access` in an isolated container. `--full-auto` was removed |
| JSON output | `--json` (JSON Lines events) |
| Resume a session | `codex exec resume --last` / `codex exec resume <id>` |
| Choose a model | `-m, --model` |
| Auth on a server | `CODEX_API_KEY`, or `codex login --device-auth` for ChatGPT plans |
| Instructions file | `AGENTS.md` (and `AGENTS.override.md`) |
| Config and credentials | `~/.codex/config.toml`; credentials in `~/.codex/auth.json` (plain text) unless you use the keyring |
| Built-in sandbox | Yes: bubblewrap + seccomp on Linux, Seatbelt on macOS; network off by default |
| MCP | Yes: `codex mcp add`, or `[mcp_servers]` in `config.toml` |
| Northflank Cloud Harness | built in |
| Billing | Included with ChatGPT plans (usage limits apply), or pay-per-token API |

## Option 1: Run Codex CLI on Northflank Cloud Harness

Codex CLI is one of the agents Cloud Harness sets up for you: each harness is an isolated microVM with Codex CLI preinstalled, your repository cloned, a persistent workspace, a web terminal and SSH access.

1. In [Northflank](https://app.northflank.com), open a project → **Harnesses** → **Create harness**.
2. Choose **Codex** as the agent, then pick Northflank's cloud or your own cloud account.
3. Authentication: an OpenAI API key, or sign in with your ChatGPT account in the harness terminal.
4. Select the repository and branch, then **Create harness**. The terminal opens with the agent ready.

To start one harness per task from a script instead, use [`launch.sh`](../examples/northflank-parallel-harnesses/README.md) with `AGENT=codex`:

```bash
AGENT=codex AGENT_API_KEY=... NF_PROJECT=my-project \
REPO_URL=https://github.com/your-org/your-repo \
  ./launch.sh tasks.txt
```

Pause the harness when you're done: compute stops and the workspace is kept. See the [Cloud Harness tutorial](../tutorials/northflank-cloud-harness/README.md).

## Option 2: Run Codex CLI on any Linux VM or container

### 1. Install

**npm** (requires Node.js 16+):

```bash
npm install -g @openai/codex
```

**Install script**:

```bash
curl -fsSL https://chatgpt.com/codex/install.sh | sh
```

Check it worked: `codex --version`. Install docs: <https://github.com/openai/codex>.

### 2. Authenticate without a browser

Cloud machines usually can't open a browser login, so use one of these:

| Method | Environment variables | How |
| --- | --- | --- |
| API key (per-run env var for exec) | `CODEX_API_KEY` | CODEX_API_KEY=<api-key> codex exec --json "<task>"; set it only for the codex invocation, not as a job-level env var in workflows running repo-controlled code. ([source](https://learn.chatgpt.com/docs/non-interactive-mode)) |
| API key (stored login) | `OPENAI_API_KEY` | printenv OPENAI_API_KEY \| codex login --with-api-key ([source](https://learn.chatgpt.com/docs/developer-commands?surface=cli)) |
| ChatGPT subscription via device code (headless) | — | codex login --device-auth, open the shown link on any device and enter the one-time code (beta). ([source](https://learn.chatgpt.com/docs/developer-commands?surface=cli)) |
| ChatGPT subscription via copied auth cache | `CODEX_HOME` | Log in on a machine with a browser, then copy ~/.codex/auth.json to ~/.codex/auth.json on the headless machine. Treat it like a password. Not for public/open-source repo CI. ([source](https://learn.chatgpt.com/docs/auth)) |
| ChatGPT subscription via SSH port forward | — | ssh -L 1455:localhost:1455 user@remote, then run codex login in that session and complete the browser flow locally. ([source](https://learn.chatgpt.com/docs/auth)) |

### 3. Run a task headlessly

Work on a branch, let the agent finish without prompts, then commit and push for review:

```bash
git switch -c agent/my-task
codex exec --sandbox workspace-write "Fix the failing tests"
git add -A && git commit -m "agent: my task" && git push -u origin HEAD
```

| Part | What it does |
| --- | --- |
| `exec` | Non-interactive: progress goes to stderr, the final message to stdout, then it exits |
| `--sandbox workspace-write` | Let Codex edit files in the repository. The default for `exec` is read-only |
| `--sandbox danger-full-access` | Alternative when the container or VM is your isolation boundary, or Codex's own sandbox can't start inside Docker |

- **Headless mode:** Streams progress to stderr and prints only the final agent message to stdout. Runs in a read-only sandbox by default. Requires running inside a Git repository unless --skip-git-repo-check. -o/--output-last-message <path> writes final message to a file; --ephemeral avoids persisting session files. Docs: "While `codex exec` runs, Codex streams progress to `stderr` and prints only the final agent message to `stdout`." ([source](https://learn.chatgpt.com/docs/non-interactive-mode))

- **Permissions:** --approve-for-me conflicts with --sandbox and --yolo. Docs: use danger-full-access only in a controlled environment such as an isolated CI runner or container; --yolo only inside an externally hardened environment. Docs: "`--full-auto` is no longer supported." ([source](https://learn.chatgpt.com/docs/non-interactive-mode))

### 4. Or use this repo's container

[`examples/cloud-agent-runner`](../examples/cloud-agent-runner/README.md) builds an image with Codex CLI (and any other agents you list) and runs one task per container:

```bash
cd examples/cloud-agent-runner
docker build --build-arg AGENTS="codex" -t cloud-agent .
docker run --rm --env-file .env cloud-agent run-task.sh codex "Fix the failing tests"
```

## Gotchas when running in the cloud

- --full-auto was removed; use --sandbox workspace-write or --approve-for-me. ([source](https://learn.chatgpt.com/docs/non-interactive-mode))
- codex exec defaults to a read-only sandbox, so edits fail unless you pass --sandbox workspace-write or higher. ([source](https://learn.chatgpt.com/docs/non-interactive-mode))
- codex exec refuses to run outside a Git repo unless --skip-git-repo-check. ([source](https://learn.chatgpt.com/docs/non-interactive-mode))
- In Docker the bubblewrap sandbox may fail if namespaces, setuid bwrap or seccomp are blocked; if the container is the boundary use --sandbox danger-full-access. ([source](https://learn.chatgpt.com/docs/agent-approvals-security))
- Sandbox network access is off by default; commands needing network (npm install, pip) need it enabled or full access. ([source](https://learn.chatgpt.com/docs/agent-approvals-security))
- ~/.codex/auth.json is plaintext and contains access tokens; treat like a password. ([source](https://learn.chatgpt.com/docs/auth))
- Do not set OPENAI_API_KEY or CODEX_API_KEY as job-level env vars in workflows running repository-controlled code. ([source](https://learn.chatgpt.com/docs/non-interactive-mode))
- Authenticate `codex exec` with `CODEX_API_KEY` (or `codex login --with-api-key`); reading `OPENAI_API_KEY` directly isn't documented. ([source](https://learn.chatgpt.com/docs/non-interactive-mode))
- To stop update checks in images, set `check_for_update_on_startup = false` in `~/.codex/config.toml`; there's no environment variable for it. ([source](https://learn.chatgpt.com/docs/config-file/config-reference))

## Sources

- <https://github.com/openai/codex>
- <https://learn.chatgpt.com/docs/agent-approvals-security>
- <https://learn.chatgpt.com/docs/agent-configuration/agents-md>
- <https://learn.chatgpt.com/docs/auth>
- <https://learn.chatgpt.com/docs/config-file/config-reference>
- <https://learn.chatgpt.com/docs/developer-commands?surface=cli>
- <https://learn.chatgpt.com/docs/non-interactive-mode>
- <https://learn.chatgpt.com/docs/permissions>
- <https://learn.chatgpt.com/docs/pricing>
<!-- END GENERATED: agent:codex -->

---

See all agents: [agent comparison](README.md) · [Run any agent in parallel on Northflank](../examples/northflank-parallel-harnesses/README.md) · [Running agents headlessly](../guides/running-agents-headless.md)
