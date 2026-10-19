# How to run OMP in the cloud

Batteries-included fork of the Pi coding agent, with a native Rust core and 60+ model providers. This guide covers running OMP on a remote machine instead of your laptop: on Northflank Cloud Harness, on any Linux VM, or in a container. It shows how to install it, log in without a browser, run tasks headlessly with permission prompts off, and what to watch for. Every fact below is quoted from or linked to the vendor's own documentation.

<!-- BEGIN GENERATED: agent:omp -->
Last verified: **2026-10-19** · Docs: <https://omp.sh/docs> · Source: <https://github.com/can1357/oh-my-pi>

## At a glance

|  |  |
| --- | --- |
| Made by | Stencil Labs (by Can Bölük) |
| Licence | MIT (open source) |
| Models | 60+ providers (Anthropic, OpenAI, Gemini, Vertex, xAI, DeepSeek, Mistral, Groq, Bedrock, Azure, OpenRouter, GitHub Copilot, Ollama and more) and custom OpenAI-compatible endpoints |
| Headless command | `omp -p "<task>"` |
| Skip permission prompts | Not needed: the default approval mode is `yolo`. `--yolo` makes it explicit; `--approval-mode write` or `always-ask` are stricter |
| JSON output | `--mode json` (JSON Lines events) |
| Resume a session | `-c, --continue` / `-r, --resume <id>` |
| Choose a model | `--model <id>` (e.g. `openai/gpt-5.2`, `opus`) |
| Auth on a server | Provider key, e.g. `ANTHROPIC_API_KEY`, or `omp login <provider>` |
| Instructions file | `AGENTS.md` (also `.omp/AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, Cursor/Copilot rules) |
| Config and credentials | `~/.omp/agent/` (`config.yml`, `models.yml`, `mcp.json`); project `.omp/` |
| Built-in sandbox | None; run it in a container or VM |
| MCP | Yes: `.omp/mcp.json`; imports other agents' MCP configs |
| Server / API mode | RPC mode: `omp --mode rpc` (JSON Lines over stdio), `omp acp`, plus a Node SDK |
| Northflank Cloud Harness | built in |
| Billing | Free (MIT); you pay your model provider |

## Option 1: Run OMP on Northflank Cloud Harness

OMP is one of the agents Cloud Harness sets up for you: each harness is an isolated microVM with OMP preinstalled, your repository cloned, a persistent workspace, a web terminal and SSH access.

1. In [Northflank](https://app.northflank.com), open a project → **Harnesses** → **Create harness**.
2. Choose **OMP** as the agent, then pick Northflank's cloud or your own cloud account.
3. Authentication: the harness uses account mode for OMP: run `omp login <provider>` in the harness terminal, or add a provider key such as `ANTHROPIC_API_KEY` as a runtime variable.
4. Select the repository and branch, then **Create harness**. The terminal opens with the agent ready.

To start one harness per task from a script instead, use [`launch.sh`](../examples/northflank-parallel-harnesses/README.md) with `AGENT=omp`:

```bash
AGENT=omp AGENT_ENV="ANTHROPIC_API_KEY" NF_PROJECT=my-project \
REPO_URL=https://github.com/your-org/your-repo \
  ./launch.sh tasks.txt
```

Pause the harness when you're done: compute stops and the workspace is kept. See the [Cloud Harness tutorial](../tutorials/northflank-cloud-harness/README.md).

## Option 2: Run OMP on any Linux VM or container

### 1. Install

**Install script**:

```bash
curl -fsSL https://omp.sh/install | sh
```

**bun** (requires bun 1.3.14+):

```bash
bun install -g @oh-my-pi/pi-coding-agent
```

Check it worked: `omp --version`. Install docs: <https://github.com/can1357/oh-my-pi/blob/main/README.md>, <https://omp.sh/install>.

### 2. Authenticate without a browser

Cloud machines usually can't open a browser login, so use one of these:

| Method | Environment variables | How |
| --- | --- | --- |
| Provider API key via environment variable | `ANTHROPIC_API_KEY`, `OPENAI_API_KEY`, `GEMINI_API_KEY`, `OPENROUTER_API_KEY`, `XAI_API_KEY`, `GROQ_API_KEY`, `MISTRAL_API_KEY`, `AZURE_OPENAI_API_KEY`, `AWS_BEARER_TOKEN_BEDROCK` | Export the provider's key (or put it in ~/.omp/agent/.env, ~/.omp/.env, ~/.env or project .env, which omp loads for unset keys), then run `omp -p --model <provider/model> "..."`. `--api-key <key>` also accepted. ([source](https://github.com/can1357/oh-my-pi/blob/main/docs/providers.md)) |
| OAuth/subscription token via environment variable | `ANTHROPIC_OAUTH_TOKEN`, `OPENAI_CODEX_OAUTH_TOKEN`, `COPILOT_GITHUB_TOKEN`, `CURSOR_ACCESS_TOKEN`, `XAI_OAUTH_TOKEN` | Supply an existing OAuth token for subscription providers through these env vars; ANTHROPIC_OAUTH_TOKEN takes precedence over ANTHROPIC_API_KEY. ([source](https://github.com/can1357/oh-my-pi/blob/main/docs/environment-variables.md)) |
| omp login (terminal OAuth / key login) | — | Run `omp login <provider>` over SSH: it prints the auth URL and reads prompts from stdin; open the URL on your laptop. For flows needing a pasted callback, use `/login <redirect-url>` inside a session to complete. Credentials are stored in local agent.db. ([source](https://github.com/can1357/oh-my-pi/blob/main/docs/providers.md)) |
| Auth broker (remote credential vault) | `OMP_AUTH_BROKER_URL`, `OMP_AUTH_BROKER_TOKEN` | For headless/remote fleets, point omp at a shared auth broker; manage with `omp auth-broker login <provider>`. ([source](https://github.com/can1357/oh-my-pi/blob/main/docs/providers.md)) |

### 3. Run a task headlessly

Work on a branch, let the agent finish without prompts, then commit and push for review:

```bash
git switch -c agent/my-task
omp -p --yolo --model anthropic/claude-sonnet-5-5 "Fix the failing tests"
git add -A && git commit -m "agent: my task" && git push -u origin HEAD
```

| Part | What it does |
| --- | --- |
| `-p` | Print mode: run the prompt, print the final answer and exit |
| `--yolo` | Auto-approve reads, writes and commands. This is already the default; passing it guards against a config that changes it |
| `--model anthropic/claude-sonnet-5-5` | Provider and model; any of the 60+ supported providers |

- **Headless mode:** Writes only the last assistant response to stdout after the turn completes (not streamed); 'Working...' goes to stderr. Piped/non-TTY stdin is read as the prompt and selects print mode (`echo '...' | omp -p`). Terminal turn failures give a nonzero exit. Useful extras: --no-session (ephemeral), --max-time 10m, --no-title / PI_NO_TITLE. Docs: "`--print` / `-p` runs `omp` non-interactively: it processes the prompts, writes the last assistant response to stdout, and exits without entering the TUI." ([source](https://github.com/can1357/oh-my-pi/blob/main/docs/cli-reference.md))

- **Permissions:** Stricter modes: `write` (prompts for exec) and `always-ask`. Explicit tool/user deny or prompt policies still apply even under --yolo. Behaviour of a prompting tool in -p mode (no UI) is not documented in what was read. Docs: "| `yolo` (default) | `read`, `write`, `exec` | none            |" ([source](https://github.com/can1357/oh-my-pi/blob/main/docs/approval-mode.md))

### 4. Or use this repo's container

[`examples/cloud-agent-runner`](../examples/cloud-agent-runner/README.md) builds an image with OMP (and any other agents you list) and runs one task per container:

```bash
cd examples/cloud-agent-runner
docker build --build-arg AGENTS="omp" -t cloud-agent .
docker run --rm --env-file .env cloud-agent run-task.sh omp "Fix the failing tests"
```

## Gotchas when running in the cloud

- Default approval mode is yolo, so the agent runs shell commands without prompting unless you set tools.approvalMode or --approval-mode. ([source](https://github.com/can1357/oh-my-pi/blob/main/docs/approval-mode.md))
- Starting omp in the home directory auto-switches to a temp dir unless --allow-home is passed; cd into the repo or use --cwd. ([source](https://github.com/can1357/oh-my-pi/blob/main/docs/cli-reference.md))
- The install script puts the binary in ~/.local/bin by default (PI_INSTALL_DIR overrides) and only warns if it is not on PATH. ([source](https://omp.sh/install))
- If bun is present on the host the install script installs via bun instead of the standalone binary; pass `sh -s -- --binary` to force the binary. ([source](https://omp.sh/install))
- Alpine/musl prebuilt binary needs `apk add libstdc++ libgcc`. ([source](https://github.com/can1357/oh-my-pi/blob/main/README.md))
- Print mode output arrives after the turn completes, not streamed; use --mode json for live event lines. ([source](https://github.com/can1357/oh-my-pi/blob/main/docs/cli-reference.md))
- Print mode waits for MCP servers before its first turn; set OMP_MCP_REQUIRE_READY=1 to fail fast or OMP_MCP_TIMEOUT_MS to bound waits. ([source](https://github.com/can1357/oh-my-pi/blob/main/docs/environment-variables.md))
- omp loads .env files (project, ~/.omp/agent/.env, ~/.omp/.env, ~/.env) for unset keys, so secrets can be supplied without exporting. ([source](https://github.com/can1357/oh-my-pi/blob/main/docs/environment-variables.md))
- Opening a repository loads its project settings, extensions, hooks, tools and MCP config by design; use --no-extensions / --config overlay with mcp.enableProjectConfig:false for untrusted repos. ([source](https://github.com/can1357/oh-my-pi/blob/main/README.md))
- plan.defaultOnStartup is ignored in print mode; use --plan-yolo for unattended plan-then-implement. ([source](https://github.com/can1357/oh-my-pi/blob/main/docs/cli-reference.md))

## Not documented / open questions

- Vendor attribution: README says 'Built by Stencil Labs'; npm author is 'Stencil Labs, Inc.'; repo lives under personal account can1357 (Can Bölük). Exact corporate relationship not documented.
- No documented env var/setting found to disable the compiled binary's startup update check (update.* settings exist but specific keys were not confirmed).
- What happens in -p (print) mode if a tool requires approval under always-ask/write mode (no UI to answer) is not documented in sources read.
- Whether 'omp login <provider>' for Anthropic/Codex OAuth works fully over SSH without a local browser (callback-paste vs device code) varies per provider; only factory-droid is explicitly documented as device-code.
- Homepage teases 'omp², soon!' — no details on a future product or pricing.

## Sources

- <https://github.com/can1357/oh-my-pi/blob/main/README.md>
- <https://github.com/can1357/oh-my-pi/blob/main/docs/approval-mode.md>
- <https://github.com/can1357/oh-my-pi/blob/main/docs/cli-reference.md>
- <https://github.com/can1357/oh-my-pi/blob/main/docs/context-files.md>
- <https://github.com/can1357/oh-my-pi/blob/main/docs/environment-variables.md>
- <https://github.com/can1357/oh-my-pi/blob/main/docs/mcp-config.md>
- <https://github.com/can1357/oh-my-pi/blob/main/docs/providers.md>
- <https://github.com/can1357/oh-my-pi/blob/main/docs/settings.md>
- <https://omp.sh/install>
<!-- END GENERATED: agent:omp -->

---

See all agents: [agent comparison](README.md) · [Run any agent in parallel on Northflank](../examples/northflank-parallel-harnesses/README.md) · [Running agents headlessly](../guides/running-agents-headless.md)
