# How to run goose in the cloud

Open-source, extensible AI agent, now part of the Linux Foundation's Agentic AI Foundation. This guide covers running goose on a remote machine instead of your laptop: on Northflank Cloud Harness, on any Linux VM, or in a container. It shows how to install it, log in without a browser, run tasks headlessly with permission prompts off, and what to watch for. Every fact below is quoted from or linked to the vendor's own documentation.

<!-- BEGIN GENERATED: agent:goose -->
Last verified: **2026-10-19** · Docs: <https://goose-docs.ai/docs/category/getting-started> · Source: <https://github.com/aaif-goose/goose>

## At a glance

|  |  |
| --- | --- |
| Made by | Agentic AI Foundation (Linux Foundation); created by Block |
| Licence | Apache-2.0 (open source) |
| Models | Anthropic, OpenAI, Gemini, Ollama, OpenRouter, Azure, Bedrock, Groq, GitHub Copilot, custom OpenAI-compatible endpoints and more |
| Headless command | `goose run -t "<task>"` |
| Skip permission prompts | `GOOSE_MODE=auto` (the default): acts without asking |
| JSON output | `--output-format json` or `stream-json` |
| Resume a session | `goose run --resume` |
| Choose a model | `--provider` and `--model` (or `GOOSE_PROVIDER` / `GOOSE_MODEL`) |
| Auth on a server | `GOOSE_PROVIDER`, `GOOSE_MODEL` and the provider key |
| Instructions file | `.goosehints` and `AGENTS.md` |
| Config and credentials | `~/.config/goose/config.yaml`; secrets in the keyring or `secrets.yaml` |
| Built-in sandbox | None for its own shell commands |
| MCP | Yes: extensions are MCP servers |
| Server / API mode | `goose serve` (ACP over HTTP), `goose acp` |
| Northflank Cloud Harness | install in an empty sandbox |
| Billing | Free (Apache-2.0); you pay your model provider |

## Option 1: Run goose on Northflank Cloud Harness

Cloud Harness doesn't preinstall goose, but its **Empty sandbox** option gives you the same isolated microVM, persistent workspace, terminal and SSH access with no agent set up. Install goose once and it stays installed across pauses:

1. **Harnesses** → **Create harness** → choose **Empty sandbox**, select your repository, and create it.
2. Under **Environment**, add the agent's credentials (`GOOSE_PROVIDER`, `GOOSE_MODEL` and the provider key) as runtime variables, then click **Update & restart**.
3. In the harness terminal, run the install command from [step 1 below](#1-install), then run goose as in [step 3](#3-run-a-task-headlessly).

Install into the home directory (the persistent volume) rather than system directories, so the agent survives restarts. [`install-agents.sh`](../examples/cloud-agent-runner/install-agents.sh) does this for you: `bash install-agents.sh goose`.

To start one empty-sandbox harness per task from a script, with the installer and the task already in the workspace, use [`launch.sh`](../examples/northflank-parallel-harnesses/README.md):

```bash
AGENT=goose AGENT_ENV="ANTHROPIC_API_KEY GOOSE_PROVIDER GOOSE_MODEL" NF_PROJECT=my-project \
REPO_URL=https://github.com/your-org/your-repo \
  ./launch.sh tasks.txt
```

Pause the harness when you're done: compute stops and the workspace is kept. See the [Cloud Harness tutorial](../tutorials/northflank-cloud-harness/README.md).

## Option 2: Run goose on any Linux VM or container

### 1. Install

**Install script**:

```bash
curl -fsSL https://github.com/aaif-goose/goose/releases/download/stable/download_cli.sh | CONFIGURE=false bash
```

Check it worked: `goose --version`. Install docs: <https://goose-docs.ai/docs/getting-started/installation>.

### 2. Authenticate without a browser

Cloud machines usually can't open a browser login, so use one of these:

| Method | Environment variables | How |
| --- | --- | --- |
| API key env var (no keyring) | `GOOSE_PROVIDER`, `GOOSE_MODEL`, `ANTHROPIC_API_KEY`, `OPENAI_API_KEY`, `GOOGLE_API_KEY`, `OPENROUTER_API_KEY`, `GOOSE_DISABLE_KEYRING` | Install with CONFIGURE=false, then export GOOSE_PROVIDER, GOOSE_MODEL and the provider key (e.g. ANTHROPIC_API_KEY). Set GOOSE_DISABLE_KEYRING=1 on servers without a keyring service. Provider env vars take precedence over stored secrets. API keys placed in config.yaml are ignored. ([source](https://goose-docs.ai/docs/guides/config-files)) |
| config file written by script (CI pattern) | `GOOSE_PROVIDER`, `GOOSE_MODEL` | Write ~/.config/goose/config.yaml containing GOOSE_PROVIDER, GOOSE_MODEL and `keyring: false`, and supply the API key via env. ([source](https://goose-docs.ai/docs/tutorials/cicd)) |
| subscription via ACP providers (Claude Code / ChatGPT Plus/Pro) | — | Install and authenticate the vendor's agent (e.g. Claude Code with claude-agent-acp) on the server, then select the ACP provider in goose. Session resume/fork not supported for ACP providers. ([source](https://goose-docs.ai/docs/guides/acp-providers)) |

### 3. Run a task headlessly

Work on a branch, let the agent finish without prompts, then commit and push for review:

```bash
git switch -c agent/my-task
GOOSE_PROVIDER=anthropic GOOSE_MODEL=claude-sonnet-5-5 \
  goose run --no-session -t "Fix the failing tests"
git add -A && git commit -m "agent: my task" && git push -u origin HEAD
```

| Part | What it does |
| --- | --- |
| `run -t` | Run the text as a task and exit when it's done |
| `--no-session` | Don't save a session for this one-off run |
| `GOOSE_PROVIDER / GOOSE_MODEL` | Which provider and model to use, with that provider's key (e.g. `ANTHROPIC_API_KEY`) in the environment |

- **Headless mode:** Starts a session, executes, and exits when the task is complete. -q/--quiet prints only the model response to stdout. Docs recommend checking the exit code in scripts. --max-turns caps autonomy (default 1000). Docs: "The `goose run` command starts a new session, begins executing using any arguments provided and exits the session automatically once the task is complete." ([source](https://goose-docs.ai/docs/guides/running-tasks))

- **Permissions:** Autonomous mode is the default, so goose edits files and runs shell commands without asking unless GOOSE_MODE is changed. The headless tutorial explicitly sets GOOSE_MODE=auto for non-interactive execution. Docs: "| `GOOSE_MODE` | Controls how goose handles tool execution | "auto", "approve", "chat", "smart_approve" | "auto" |" ([source](https://goose-docs.ai/docs/guides/environment-variables))

### 4. Or use this repo's container

[`examples/cloud-agent-runner`](../examples/cloud-agent-runner/README.md) builds an image with goose (and any other agents you list) and runs one task per container:

```bash
cd examples/cloud-agent-runner
docker build --build-arg AGENTS="goose" -t cloud-agent .
docker run --rm --env-file .env cloud-agent run-task.sh goose "Fix the failing tests"
```

## Gotchas when running in the cloud

- Repo moved from block/goose to aaif-goose/goose and docs to goose-docs.ai; github.com/block/goose redirects. ([source](https://github.com/aaif-goose/goose))
- Default GOOSE_MODE is auto, so goose acts without approval by default; run it in an isolated container/VM. ([source](https://goose-docs.ai/docs/guides/environment-variables))
- Headless servers/containers have no keyring: secrets fall back to plain-text ~/.config/goose/secrets.yaml; prefer GOOSE_DISABLE_KEYRING=1 plus env vars. ([source](https://goose-docs.ai/docs/guides/config-files))
- Unattended processes can block indefinitely on keyring access; docs show GOOSE_DISABLE_KEYRING=1 with env credentials. ([source](https://goose-docs.ai/docs/guides/goose-cli-commands))
- Pin GOOSE_VERSION in CI to avoid 404s when the stable tag lacks CLI assets. ([source](https://goose-docs.ai/docs/tutorials/cicd))
- goose serve binds 127.0.0.1:3284 by default and requires GOOSE_SERVER__SECRET_KEY. ([source](https://goose-docs.ai/docs/guides/goose-cli-commands))
- Use --no-session for one-off runs and --max-turns to cap runaway execution. ([source](https://goose-docs.ai/docs/tutorials/headless-goose))
- Homebrew formula/cask names still use the old 'block-goose' prefix. ([source](https://goose-docs.ai/docs/getting-started/installation))

## Not documented / open questions

- Exact exit-code semantics of `goose run` on tool/model failure are not documented beyond 'check exit codes'.
- No documented OS-level sandbox for the developer extension's shell commands.
- Whether `goose run` accepts the prompt as a positional argument (vs -t/-i) is not documented; use -t.
- Whether the CLI auto-updates on its own: not documented; only manual `goose update` is described.

## Sources

- <https://github.com/aaif-goose/goose>
- <https://github.com/aaif-goose/goose/blob/main/LICENSE>
- <https://goose-docs.ai/docs/getting-started/installation>
- <https://goose-docs.ai/docs/getting-started/providers>
- <https://goose-docs.ai/docs/guides/acp-providers>
- <https://goose-docs.ai/docs/guides/config-files>
- <https://goose-docs.ai/docs/guides/environment-variables>
- <https://goose-docs.ai/docs/guides/goose-cli-commands>
- <https://goose-docs.ai/docs/guides/running-tasks>
- <https://goose-docs.ai/docs/tutorials/cicd>
- <https://goose-docs.ai/docs/tutorials/headless-goose>
<!-- END GENERATED: agent:goose -->

---

See all agents: [agent comparison](README.md) · [Run any agent in parallel on Northflank](../examples/northflank-parallel-harnesses/README.md) · [Running agents headlessly](../guides/running-agents-headless.md)
