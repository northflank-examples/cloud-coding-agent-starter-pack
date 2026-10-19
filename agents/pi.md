# How to run Pi in the cloud

Minimal, extensible open-source terminal coding agent by Mario Zechner. This guide covers running Pi on a remote machine instead of your laptop: on Northflank Cloud Harness, on any Linux VM, or in a container. It shows how to install it, log in without a browser, run tasks headlessly with permission prompts off, and what to watch for. Every fact below is quoted from or linked to the vendor's own documentation.

<!-- BEGIN GENERATED: agent:pi -->
Last verified: **2026-10-19** · Docs: <https://pi.dev/docs/latest> · Source: <https://github.com/earendil-works/pi>

## At a glance

|  |  |
| --- | --- |
| Made by | Earendil Works (by Mario Zechner) |
| Licence | MIT (open source) |
| Models | Anthropic, OpenAI, Google, GitHub Copilot, Mistral, Groq, xAI, OpenRouter, Bedrock, Vertex, Azure and more, plus any OpenAI- or Anthropic-compatible endpoint |
| Headless command | `pi -p "<task>"` |
| Skip permission prompts | Not needed: Pi has no permission prompts. Limit tools with `--tools` / `--exclude-tools` |
| JSON output | `--mode json` (JSON Lines) |
| Resume a session | `-c, --continue` / `--session <id>` |
| Choose a model | `--model provider/id` |
| Auth on a server | Provider key, e.g. `ANTHROPIC_API_KEY`, or `/login` |
| Instructions file | `AGENTS.md` or `CLAUDE.md` |
| Config and credentials | `~/.pi/agent/` (`settings.json`, `auth.json`); project `.pi/` |
| Built-in sandbox | None; run it in a container or VM |
| MCP | Yes: `pi mcp add`, `~/.pi/agent/mcp.json` |
| Server / API mode | RPC mode: `pi --mode rpc` (JSON Lines over stdin/stdout), plus a TypeScript SDK |
| Northflank Cloud Harness | built in |
| Billing | Free (MIT); you pay your model provider |

## Option 1: Run Pi on Northflank Cloud Harness

Pi is one of the agents Cloud Harness sets up for you: each harness is an isolated microVM with Pi preinstalled, your repository cloned, a persistent workspace, a web terminal and SSH access.

1. In [Northflank](https://app.northflank.com), open a project → **Harnesses** → **Create harness**.
2. Choose **Pi** as the agent, then pick Northflank's cloud or your own cloud account.
3. Authentication: the harness uses account mode for Pi: run `/login` inside Pi, or add a provider key such as `ANTHROPIC_API_KEY` as a runtime variable.
4. Select the repository and branch, then **Create harness**. The terminal opens with the agent ready.

To start one harness per task from a script instead, use [`launch.sh`](../examples/northflank-parallel-harnesses/README.md) with `AGENT=pi`:

```bash
AGENT=pi AGENT_ENV="ANTHROPIC_API_KEY" NF_PROJECT=my-project \
REPO_URL=https://github.com/your-org/your-repo \
  ./launch.sh tasks.txt
```

Pause the harness when you're done: compute stops and the workspace is kept. See the [Cloud Harness tutorial](../tutorials/northflank-cloud-harness/README.md).

## Option 2: Run Pi on any Linux VM or container

### 1. Install

**Install script**:

```bash
curl -fsSL https://pi.dev/install.sh | sh
```

**npm** (requires Node.js 22.19+):

```bash
npm install -g --ignore-scripts @earendil-works/pi-coding-agent
```

Check it worked: `pi --version`. Install docs: <https://github.com/earendil-works/pi>.

### 2. Authenticate without a browser

Cloud machines usually can't open a browser login, so use one of these:

| Method | Environment variables | How |
| --- | --- | --- |
| API key env var | `ANTHROPIC_API_KEY`, `OPENAI_API_KEY`, `GEMINI_API_KEY`, `OPENROUTER_API_KEY`, `MISTRAL_API_KEY`, `GROQ_API_KEY`, `XAI_API_KEY`, `DEEPSEEK_API_KEY`, `COPILOT_GITHUB_TOKEN`, `OPENCODE_API_KEY` | export the provider's key before running pi (e.g. export ANTHROPIC_API_KEY=...; pi -p "..."). Check with: pi auth check --provider anthropic ([source](https://github.com/earendil-works/pi/blob/main/packages/coding-agent/docs/providers.md)) |
| subscription / OAuth login on headless | — | Run pi interactively, use /login, choose the provider; when the OAuth callback cannot reach the remote machine, paste the final redirect URL or authorization code back into Pi. Credentials are saved to ~/.pi/agent/auth.json. ([source](https://github.com/earendil-works/pi/blob/main/packages/coding-agent/docs/providers.md)) |
| Anthropic OAuth token env var | `ANTHROPIC_OAUTH_TOKEN`, `ANTHROPIC_AUTH_TOKEN` | Set ANTHROPIC_OAUTH_TOKEN (API credential) or ANTHROPIC_AUTH_TOKEN (bearer). Pi's containerization doc generates the token with `claude setup-token`. ([source](https://github.com/earendil-works/pi/blob/main/packages/coding-agent/docs/providers.md)) |

### 3. Run a task headlessly

Work on a branch, let the agent finish without prompts, then commit and push for review:

```bash
git switch -c agent/my-task
pi -p --model anthropic/claude-sonnet-5-5 "Fix the failing tests"
git add -A && git commit -m "agent: my task" && git push -u origin HEAD
```

| Part | What it does |
| --- | --- |
| `-p` | Print mode: run the prompt, print only the final answer and exit |
| `--model anthropic/claude-sonnet-5-5` | Provider and model. Pi has no approval prompts, so it edits and runs commands straight away |

- **Headless mode:** Print mode runs the prompt(s), writes only the final assistant text to stdout and exits. Piped stdin is prepended to the prompt (e.g. git diff | pi -p "Review this change"). If stdin or stdout is redirected and no JSON/RPC mode is chosen, Pi uses print mode automatically. Docs: "`-p`, `--print` | Run the supplied prompts, write the final assistant text to stdout, then exit" ([source](https://github.com/earendil-works/pi/blob/main/packages/coding-agent/docs/cli.md))

- **Permissions:** Because there is no approval system, isolation must come from the container/VM. In print/JSON/RPC mode, without a trust decision, project .pi resources (settings, extensions, project mcp.json) are skipped by default. Docs: "Pi does not include a built-in permission system for restricting filesystem, process, network, or credential access. By default, it runs with the permissions of the user and process that launched it." ([source](https://github.com/earendil-works/pi))

### 4. Or use this repo's container

[`examples/cloud-agent-runner`](../examples/cloud-agent-runner/README.md) builds an image with Pi (and any other agents you list) and runs one task per container:

```bash
cd examples/cloud-agent-runner
docker build --build-arg AGENTS="pi" -t cloud-agent .
docker run --rm --env-file .env cloud-agent run-task.sh pi "Fix the failing tests"
```

## Gotchas when running in the cloud

- npm package moved: @mariozechner/pi-coding-agent is deprecated with the message 'please use @earendil-works/pi-coding-agent instead going forward'. ([source](https://www.npmjs.com/package/@mariozechner/pi-coding-agent))
- No permission prompts and no built-in sandbox: Pi runs tools with the launching user's permissions, so run it in a container/VM. ([source](https://github.com/earendil-works/pi))
- Print, JSON and RPC modes cannot show the project-trust prompt; with the default defaultProjectTrust 'ask', project .pi resources are skipped unless you pass -a/--approve or save a trust decision. ([source](https://github.com/earendil-works/pi/blob/main/packages/coding-agent/docs/security.md))
- Official Dockerfile example uses node:24-bookworm-slim plus git and ripgrep, and mounts a volume at /root/.pi/agent to persist settings, credentials and sessions. ([source](https://github.com/earendil-works/pi/blob/main/packages/coding-agent/docs/containerization.md))
- JSON mode: stdout is strict JSONL; read it continuously or Pi can stall when the pipe buffer fills; diagnostics go to stderr. ([source](https://github.com/earendil-works/pi/blob/main/packages/coding-agent/docs/json.md))
- Credential-printing commands (pi auth print-api-key) write secrets to stdout; be careful in CI logs. ([source](https://github.com/earendil-works/pi/blob/main/packages/coding-agent/docs/cli.md))

## Not documented / open questions

- GitHub release tag is v1.3.0 (2026-10-15); npm @earendil-works/pi-coding-agent latest is also 1.3.0. The old @mariozechner package stops at 0.73.1.
- Exact exit codes of `pi -p` on model/tool failure are not documented in the pages reviewed.
- Whether the pi.dev install.sh script installs Node.js non-interactively in a minimal container was not verified.

## Sources

- <https://github.com/earendil-works/pi>
- <https://github.com/earendil-works/pi/blob/main/packages/coding-agent/docs/cli.md>
- <https://github.com/earendil-works/pi/blob/main/packages/coding-agent/docs/configuration.md>
- <https://github.com/earendil-works/pi/blob/main/packages/coding-agent/docs/containerization.md>
- <https://github.com/earendil-works/pi/blob/main/packages/coding-agent/docs/environment-variables.md>
- <https://github.com/earendil-works/pi/blob/main/packages/coding-agent/docs/json.md>
- <https://github.com/earendil-works/pi/blob/main/packages/coding-agent/docs/mcp.md>
- <https://github.com/earendil-works/pi/blob/main/packages/coding-agent/docs/providers.md>
- <https://github.com/earendil-works/pi/blob/main/packages/coding-agent/docs/rpc.md>
- <https://github.com/earendil-works/pi/blob/main/packages/coding-agent/docs/security.md>
- <https://www.npmjs.com/package/@mariozechner/pi-coding-agent>
<!-- END GENERATED: agent:pi -->

---

See all agents: [agent comparison](README.md) · [Run any agent in parallel on Northflank](../examples/northflank-parallel-harnesses/README.md) · [Running agents headlessly](../guides/running-agents-headless.md)
