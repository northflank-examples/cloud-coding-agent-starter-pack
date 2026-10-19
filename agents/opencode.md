# How to run OpenCode in the cloud

Open-source terminal coding agent that works with 75+ model providers. This guide covers running OpenCode on a remote machine instead of your laptop: on Northflank Cloud Harness, on any Linux VM, or in a container. It shows how to install it, log in without a browser, run tasks headlessly with permission prompts off, and what to watch for. Every fact below is quoted from or linked to the vendor's own documentation.

<!-- BEGIN GENERATED: agent:opencode -->
Last verified: **2026-10-19** · Docs: <https://opencode.ai/docs/> · Source: <https://github.com/anomalyco/opencode>

## At a glance

|  |  |
| --- | --- |
| Made by | Anomaly (formerly SST) |
| Licence | MIT (open source) |
| Models | 75+ providers (Anthropic, OpenAI, Bedrock, Vertex, Azure, OpenRouter, GitHub Copilot, local models and more) |
| Headless command | `opencode run "<task>"` |
| Skip permission prompts | `opencode run --auto`, or `"permission": "allow"` in `opencode.json`. Most actions are allowed by default |
| JSON output | `--format json` |
| Resume a session | `-c, --continue` / `-s, --session <id>` |
| Choose a model | `-m provider/model` |
| Auth on a server | Provider key, e.g. `ANTHROPIC_API_KEY` |
| Instructions file | `AGENTS.md` (falls back to `CLAUDE.md` in OpenCode 1) |
| Config and credentials | `~/.config/opencode/opencode.json`; keys in `~/.local/share/opencode/auth.json` |
| Built-in sandbox | None; permission rules only |
| MCP | Yes: `mcp` in `opencode.json`, `opencode mcp add` |
| Server / API mode | `opencode serve` (HTTP API with OpenAPI spec), `opencode run --attach <url>` |
| Northflank Cloud Harness | built in |
| Billing | Free (MIT); you pay your model provider. Optional OpenCode Zen and Go plans |

## Option 1: Run OpenCode on Northflank Cloud Harness

OpenCode is one of the agents Cloud Harness sets up for you: each harness is an isolated microVM with OpenCode preinstalled, your repository cloned, a persistent workspace, a web terminal and SSH access.

1. In [Northflank](https://app.northflank.com), open a project → **Harnesses** → **Create harness**.
2. Choose **OpenCode** as the agent, then pick Northflank's cloud or your own cloud account.
3. Authentication: the harness uses account mode for OpenCode: connect a provider inside the agent, or add a provider key such as `ANTHROPIC_API_KEY` as a runtime variable.
4. Select the repository and branch, then **Create harness**. The terminal opens with the agent ready.

To start one harness per task from a script instead, use [`launch.sh`](../examples/northflank-parallel-harnesses/README.md) with `AGENT=opencode`:

```bash
AGENT=opencode AGENT_ENV="ANTHROPIC_API_KEY" NF_PROJECT=my-project \
REPO_URL=https://github.com/your-org/your-repo \
  ./launch.sh tasks.txt
```

Pause the harness when you're done: compute stops and the workspace is kept. See the [Cloud Harness tutorial](../tutorials/northflank-cloud-harness/README.md).

## Option 2: Run OpenCode on any Linux VM or container

### 1. Install

**Install script**:

```bash
curl -fsSL https://opencode.ai/install | bash
```

**npm**:

```bash
npm install -g opencode-ai
```

Check it worked: `opencode --version`. Install docs: <https://opencode.ai/docs/>.

### 2. Authenticate without a browser

Cloud machines usually can't open a browser login, so use one of these:

| Method | Environment variables | How |
| --- | --- | --- |
| API key env var / .env | `ANTHROPIC_API_KEY`, `OPENAI_API_KEY`, `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_PROFILE`, `AWS_BEARER_TOKEN_BEDROCK` | Export the provider's key in the environment (or a project .env) before running opencode; OpenCode picks it up at startup. Config can also reference keys with {env:VAR}. ([source](https://opencode.ai/docs/cli/)) |
| opencode auth login (API key stored in file) | — | Run `opencode auth login` (optionally --provider <id> --method <label>) in an SSH terminal and paste the key; stored in ~/.local/share/opencode/auth.json. Copy that file into the container/VM to reuse. ([source](https://opencode.ai/docs/cli/)) |
| subscription login (GitHub Copilot device code) | — | /connect -> GitHub Copilot, then open github.com/login/device on any machine and enter the code. ChatGPT Plus/Pro and Claude Pro/Max options in V1 docs open a browser; headless behaviour not documented. ([source](https://opencode.ai/docs/providers/)) |
| OpenCode 2: env var must be on the server process | `ANTHROPIC_API_KEY` | V2 runs a shared background server; use `ANTHROPIC_API_KEY=... opencode --standalone` or `opencode service set env ANTHROPIC_API_KEY ...`. V2 credentials live in SQLite (~/.local/share/opencode/opencode.db). ([source](https://opencode.ai/v2/docs/cli/providers/)) |

### 3. Run a task headlessly

Work on a branch, let the agent finish without prompts, then commit and push for review:

```bash
git switch -c agent/my-task
opencode run --auto -m anthropic/claude-sonnet-5-5 "Fix the failing tests"
git add -A && git commit -m "agent: my task" && git push -u origin HEAD
```

| Part | What it does |
| --- | --- |
| `run` | Non-interactive mode: run one prompt and exit |
| `--auto` | Approve anything that isn't explicitly denied in your permission config |
| `-m anthropic/claude-sonnet-5-5` | Provider and model, as `provider/model`. Use any model your provider key has access to |

- **Headless mode:** Non-interactive mode; prints formatted output by default (--format json for raw JSON events). Can attach to a running server with --attach http://host:4096 to avoid MCP cold boot. Exit-code behaviour not documented. Same `opencode run` command exists in OpenCode 2. Docs: "Run opencode in non-interactive mode by passing a prompt directly." ([source](https://opencode.ai/docs/cli/))

- **Permissions:** Defaults are already permissive: most permissions default to allow; doom_loop and external_directory default to ask; .env reads denied. --auto approves anything not explicitly denied; explicit deny rules still apply. OpenCode 2 uses an ordered `permissions` array instead of the V1 `permission` map, and allows external_directory by default. Docs: "Start OpenCode with --auto to automatically approve permission requests that are not explicitly denied." ([source](https://opencode.ai/docs/permissions/))

### 4. Or use this repo's container

[`examples/cloud-agent-runner`](../examples/cloud-agent-runner/README.md) builds an image with OpenCode (and any other agents you list) and runs one task per container:

```bash
cd examples/cloud-agent-runner
docker build --build-arg AGENTS="opencode" -t cloud-agent .
docker run --rm --env-file .env cloud-agent run-task.sh opencode "Fix the failing tests"
```

## Gotchas when running in the cloud

- Two major versions are live: OpenCode 1 (opencode.ai/docs, npm opencode-ai, GitHub releases v1.19.x) and OpenCode 2 (opencode.ai/v2/docs, npm @opencode/cli 2.0.x). Both install the `opencode` command and cannot be installed side by side. ([source](https://opencode.ai/docs/))
- serve defaults to hostname 127.0.0.1 port 4096; set --hostname 0.0.0.0 to expose it and set OPENCODE_SERVER_PASSWORD for basic auth. ([source](https://opencode.ai/docs/server/))
- OpenCode auto-downloads updates at startup unless autoupdate is false / OPENCODE_DISABLE_AUTOUPDATE is set; pin versions in images. ([source](https://opencode.ai/docs/config/))
- V2: the CLI starts/uses one shared background server per user; env vars like ANTHROPIC_API_KEY must be set on that server (opencode service set env) or use --standalone. ([source](https://opencode.ai/v2/docs/cli/providers/))
- V2: API-key entry and paste-code OAuth in `opencode auth login` require an interactive terminal. ([source](https://opencode.ai/v2/docs/cli/providers/))
- Docs state Anthropic prohibits using Claude Pro/Max via third-party plugins; bundled plugins were removed as of 1.3.0, so use an Anthropic API key. ([source](https://opencode.ai/docs/providers/))
- Official Docker image: ghcr.io/anomalyco/opencode. ([source](https://opencode.ai/docs/))

## Not documented / open questions

- Which major version the guide should target: README on the dev branch installs @opencode/cli (V2), but opencode.ai/docs and GitHub releases are still V1 (1.19.3).
- V2 CLI docs do not list `opencode run` flags (--auto, --format json, -m, -c); assumed unchanged from V1 per the migration guide's compatibility statement, but not explicitly documented for V2.
- Exit codes of `opencode run` on failure are not documented.
- Behaviour of `opencode run` when a permission resolves to "ask" without --auto (block, fail, or auto-reject) is not documented.
- Whether ChatGPT Plus/Pro login works on a headless server (device code vs browser) in V1 is not documented; V2 TUI mentions 'Codex device code (legacy)'.
- No telemetry opt-out documented.

## Sources

- <https://github.com/anomalyco/opencode/blob/dev/LICENSE>
- <https://opencode.ai/docs/>
- <https://opencode.ai/docs/cli/>
- <https://opencode.ai/docs/config/>
- <https://opencode.ai/docs/mcp-servers/>
- <https://opencode.ai/docs/permissions/>
- <https://opencode.ai/docs/providers/>
- <https://opencode.ai/docs/rules/>
- <https://opencode.ai/docs/server/>
- <https://opencode.ai/v2/docs/>
- <https://opencode.ai/v2/docs/cli/providers/>
<!-- END GENERATED: agent:opencode -->

---

See all agents: [agent comparison](README.md) · [Run any agent in parallel on Northflank](../examples/northflank-parallel-harnesses/README.md) · [Running agents headlessly](../guides/running-agents-headless.md)
