# How to run Cursor CLI in the cloud

Cursor's coding agent in the terminal (command: `agent`). This guide covers running Cursor CLI on a remote machine instead of your laptop: on Northflank Cloud Harness, on any Linux VM, or in a container. It shows how to install it, log in without a browser, run tasks headlessly with permission prompts off, and what to watch for. Every fact below is quoted from or linked to the vendor's own documentation.

<!-- BEGIN GENERATED: agent:cursor-cli -->
Last verified: **2026-10-19** · Docs: <https://cursor.com/docs/cli/overview>

## At a glance

|  |  |
| --- | --- |
| Made by | Cursor (Anysphere) |
| Licence | Proprietary |
| Models | Models available on your Cursor account (Anthropic, OpenAI and others, or `auto`); bring-your-own AWS Bedrock |
| Headless command | `agent -p "<task>"` |
| Skip permission prompts | `--force` (alias `--yolo`) plus `--trust` in headless mode; or allow/deny rules in `cli-config.json` |
| JSON output | `--output-format json` or `stream-json` |
| Resume a session | `--resume [chatId]`, `--continue` |
| Choose a model | `--model <model>` (`agent models` lists them) |
| Auth on a server | `CURSOR_API_KEY` |
| Instructions file | `.cursor/rules`, `AGENTS.md`, `CLAUDE.md` |
| Config and credentials | `~/.cursor/cli-config.json`; project `.cursor/cli.json` |
| Built-in sandbox | Yes on Linux: Landlock + seccomp (kernel 6.2+); falls back to asking |
| MCP | Yes: shares the editor's `mcp.json`; `agent mcp ...` |
| Northflank Cloud Harness | built in |
| Billing | Uses your Cursor account's plan; the CLI docs don't state which plans include it |

## Option 1: Run Cursor CLI on Northflank Cloud Harness

Cursor CLI is one of the agents Cloud Harness sets up for you: each harness is an isolated microVM with Cursor CLI preinstalled, your repository cloned, a persistent workspace, a web terminal and SSH access.

1. In [Northflank](https://app.northflank.com), open a project → **Harnesses** → **Create harness**.
2. Choose **Cursor** as the agent, then pick Northflank's cloud or your own cloud account.
3. Authentication: a Cursor API key, or sign in with your Cursor account in the harness terminal.
4. Select the repository and branch, then **Create harness**. The terminal opens with the agent ready.

To start one harness per task from a script instead, use [`launch.sh`](../examples/northflank-parallel-harnesses/README.md) with `AGENT=cursor-cli`:

```bash
AGENT=cursor-cli AGENT_API_KEY=... NF_PROJECT=my-project \
REPO_URL=https://github.com/your-org/your-repo \
  ./launch.sh tasks.txt
```

Pause the harness when you're done: compute stops and the workspace is kept. See the [Cloud Harness tutorial](../tutorials/northflank-cloud-harness/README.md).

## Option 2: Run Cursor CLI on any Linux VM or container

### 1. Install

**Install script**:

```bash
curl https://cursor.com/install -fsS | bash
```

Check it worked: `agent --version`. Install docs: <https://cursor.com/docs/cli/installation>.

### 2. Authenticate without a browser

Cloud machines usually can't open a browser login, so use one of these:

| Method | Environment variables | How |
| --- | --- | --- |
| API key env var | `CURSOR_API_KEY` | Generate a user API key at https://cursor.com/dashboard/api, then export CURSOR_API_KEY=... (or pass --api-key <key>). ([source](https://cursor.com/docs/cli/reference/authentication)) |
| login on headless | `NO_OPEN_BROWSER` | Run `NO_OPEN_BROWSER=1 agent login`, open the printed URL in a browser on any machine and complete the login. Check with `agent status`. ([source](https://cursor.com/docs/cli/reference/authentication)) |

### 3. Run a task headlessly

Work on a branch, let the agent finish without prompts, then commit and push for review:

```bash
git switch -c agent/my-task
agent -p --force --trust --output-format text "Fix the failing tests"
git add -A && git commit -m "agent: my task" && git push -u origin HEAD
```

| Part | What it does |
| --- | --- |
| `-p` | Print mode: run without the interactive UI and print the final response |
| `--force` | Apply file changes and run commands without asking (alias `--yolo`) |
| `--trust` | Trust the workspace without the interactive trust prompt |
| `--output-format text` | Plain text output. Use `json` for one JSON result |

- **Headless mode:** Print mode prints the final response. Default output format is text. On failure the process exits non-zero and writes an error to stderr. Print mode is also inferred when stdout is not a TTY or stdin is piped. Docs: "Use print mode (`-p, --print`) for non-interactive scripting and automation." ([source](https://cursor.com/docs/cli/headless))

- **Permissions:** Headless docs say that without --force changes are only proposed, not applied. The 'Using' page says 'Cursor has full write access in non-interactive mode'. The two pages conflict. Docs: "Combine `--print` with `--force` (or `--yolo`) to modify files in scripts:" ([source](https://cursor.com/docs/cli/headless))

### 4. Or use this repo's container

[`examples/cloud-agent-runner`](../examples/cloud-agent-runner/README.md) builds an image with Cursor CLI (and any other agents you list) and runs one task per container:

```bash
cd examples/cloud-agent-runner
docker build --build-arg AGENTS="cursor-cli" -t cloud-agent .
docker run --rm --env-file .env cloud-agent run-task.sh cursor-cli "Fix the failing tests"
```

## Gotchas when running in the cloud

- The install script puts the binary in ~/.local/bin, which you must add to PATH. ([source](https://cursor.com/docs/cli/installation))
- Auto-updates by default. The CLI pages document no switch to turn this off. ([source](https://cursor.com/docs/cli/installation))
- Use --trust to skip the workspace-trust prompt in headless mode. ([source](https://cursor.com/docs/cli/reference/parameters))
- Linux sandbox needs kernel 6.2+ with Landlock v3 and unprivileged user namespaces. The standalone CLI does not ship the AppArmor profile, so you may need the cursor-sandbox-apparmor package. ([source](https://cursor.com/docs/agent/security/run-modes))
- Behind a firewall, allowlist *.cursor.sh and *.cursorapi.com. HTTP_PROXY/HTTPS_PROXY and NODE_USE_ENV_PROXY=1 are supported, and network.useHttp1ForAgent helps with proxies that can't do HTTP/2. ([source](https://cursor.com/help/integrations/cli))
- With --output-format json, a failed run exits non-zero and emits no JSON object, only stderr. ([source](https://cursor.com/docs/cli/reference/output-format))
- Agent commits and PRs get a 'Made with Cursor' trailer/footer by default (attribution.* in cli-config.json). ([source](https://cursor.com/docs/cli/reference/configuration))
- The binary is `agent`; the install script also creates a legacy `cursor-agent` symlink, both in `~/.local/bin` (checked in the script on 2026-10-16). ([source](https://cursor.com/install))
- Always pass `--force` in headless runs: Cursor's docs disagree on whether print mode applies edits without it. ([source](https://cursor.com/docs/cli/headless))

## Sources

- <https://cursor.com/docs/agent/security/run-modes>
- <https://cursor.com/docs/cli/changelog>
- <https://cursor.com/docs/cli/github-actions>
- <https://cursor.com/docs/cli/headless>
- <https://cursor.com/docs/cli/installation>
- <https://cursor.com/docs/cli/mcp>
- <https://cursor.com/docs/cli/overview>
- <https://cursor.com/docs/cli/reference/authentication>
- <https://cursor.com/docs/cli/reference/configuration>
- <https://cursor.com/docs/cli/reference/output-format>
- <https://cursor.com/docs/cli/reference/parameters>
- <https://cursor.com/docs/cli/using>
- <https://cursor.com/help/integrations/cli>
- <https://cursor.com/install>
<!-- END GENERATED: agent:cursor-cli -->

---

See all agents: [agent comparison](README.md) · [Run any agent in parallel on Northflank](../examples/northflank-parallel-harnesses/README.md) · [Running agents headlessly](../guides/running-agents-headless.md)
