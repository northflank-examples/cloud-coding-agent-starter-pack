# How to run Qwen Code in the cloud

Alibaba's open-source terminal agent, forked from Gemini CLI. This guide covers running Qwen Code on a remote machine instead of your laptop: on Northflank Cloud Harness, on any Linux VM, or in a container. It shows how to install it, log in without a browser, run tasks headlessly with permission prompts off, and what to watch for. Every fact below is quoted from or linked to the vendor's own documentation.

<!-- BEGIN GENERATED: agent:qwen-code -->
Last verified: **2026-10-19** · Docs: <https://qwenlm.github.io/qwen-code-docs/en/users/overview> · Source: <https://github.com/QwenLM/qwen-code>

## At a glance

|  |  |
| --- | --- |
| Made by | Alibaba Qwen team |
| Licence | Apache-2.0 (open source) |
| Models | Any OpenAI-compatible API, Anthropic, Gemini, Qwen/DashScope, OpenRouter, and local models (Ollama, vLLM) |
| Headless command | `qwen -p "<task>"` |
| Skip permission prompts | `--approval-mode yolo` (or `-y`); safer: `auto-edit` |
| JSON output | `--output-format json` or `stream-json` |
| Resume a session | `--continue` / `--resume <id>` |
| Choose a model | `-m, --model` (or `OPENAI_MODEL`) |
| Auth on a server | `OPENAI_API_KEY` and `OPENAI_BASE_URL` (any compatible API) |
| Instructions file | `QWEN.md` (configurable via `context.fileName`) |
| Config and credentials | `~/.qwen/settings.json` |
| Built-in sandbox | Optional: Docker, Podman or Seatbelt; bubblewrap for tool execution |
| MCP | Yes: `qwen mcp add` |
| Northflank Cloud Harness | install in an empty sandbox |
| Billing | Pay your provider's API rates, or Alibaba Cloud Coding Plan. The free Qwen OAuth tier ended on 2026-04-15 |

## Option 1: Run Qwen Code on Northflank Cloud Harness

Cloud Harness doesn't preinstall Qwen Code, but its **Empty sandbox** option gives you the same isolated microVM, persistent workspace, terminal and SSH access with no agent set up. Install Qwen Code once and it stays installed across pauses:

1. **Harnesses** → **Create harness** → choose **Empty sandbox**, select your repository, and create it.
2. Under **Environment**, add the agent's credentials (`OPENAI_API_KEY` and `OPENAI_BASE_URL` (any compatible API)) as runtime variables, then click **Update & restart**.
3. In the harness terminal, run the install command from [step 1 below](#1-install), then run Qwen Code as in [step 3](#3-run-a-task-headlessly).

Install into the home directory (the persistent volume) rather than system directories, so the agent survives restarts. [`install-agents.sh`](../examples/cloud-agent-runner/install-agents.sh) does this for you: `bash install-agents.sh qwen-code`.

To start one empty-sandbox harness per task from a script, with the installer and the task already in the workspace, use [`launch.sh`](../examples/northflank-parallel-harnesses/README.md):

```bash
AGENT=qwen-code AGENT_ENV="OPENAI_API_KEY" NF_PROJECT=my-project \
REPO_URL=https://github.com/your-org/your-repo \
  ./launch.sh tasks.txt
```

Pause the harness when you're done: compute stops and the workspace is kept. See the [Cloud Harness tutorial](../tutorials/northflank-cloud-harness/README.md).

## Option 2: Run Qwen Code on any Linux VM or container

### 1. Install

**npm** (requires Node.js 22+):

```bash
npm install -g @qwen-code/qwen-code@latest
```

**Install script**:

```bash
curl -fsSL https://qwen-code-assets.oss-cn-hangzhou.aliyuncs.com/installation/install-qwen-standalone.sh | bash
```

Check it worked: `qwen --version`. Install docs: <https://github.com/QwenLM/qwen-code>.

### 2. Authenticate without a browser

Cloud machines usually can't open a browser login, so use one of these:

| Method | Environment variables | How |
| --- | --- | --- |
| OpenAI-compatible API key (any provider or self-hosted endpoint) | `OPENAI_API_KEY`, `OPENAI_BASE_URL`, `OPENAI_MODEL` | export OPENAI_API_KEY, OPENAI_BASE_URL, OPENAI_MODEL (or set in .env / settings.json env). Precedence: shell export > .env > settings.json env. ([source](https://qwenlm.github.io/qwen-code-docs/en/users/configuration/auth/)) |
| Alibaba Cloud Coding Plan (subscription) | `OPENAI_API_KEY`, `OPENAI_BASE_URL` | Use the sk-sp-... Coding Plan key with endpoint https://coding-intl.dashscope.aliyuncs.com/v1 (international) or https://coding.dashscope.aliyuncs.com/v1 (China), via env vars or settings.json modelProviders. ([source](https://qwenlm.github.io/qwen-code-docs/en/users/configuration/auth/)) |
| Provider-specific keys (DashScope, Anthropic, Gemini) | `DASHSCOPE_API_KEY`, `ANTHROPIC_API_KEY`, `GEMINI_API_KEY` | Set the key and select protocol via security.auth.selectedType (openai\|anthropic\|gemini) and modelProviders in ~/.qwen/settings.json. ([source](https://qwenlm.github.io/qwen-code-docs/en/users/configuration/auth/)) |

### 3. Run a task headlessly

Work on a branch, let the agent finish without prompts, then commit and push for review:

```bash
git switch -c agent/my-task
qwen -p "Fix the failing tests" --approval-mode yolo
git add -A && git commit -m "agent: my task" && git push -u origin HEAD
```

| Part | What it does |
| --- | --- |
| `-p` | Headless mode: run the prompt and exit |
| `--approval-mode yolo` | Approve every action. Use `auto-edit` to approve only file edits |

- **Headless mode:** Documented exit codes: 53 turn-cap exceeded, 55 run-level budget abort, 130 SIGINT; full table not documented. Docs: "Use the `--prompt` (or `-p`) flag to run in headless mode:" ([source](https://qwenlm.github.io/qwen-code-docs/en/users/features/headless/))

- **Permissions:** Use with sandbox (-s / QWEN_SANDBOX) for isolation. Docs: "Set approval mode (`plan`, `default`, `auto-edit`, `auto`, `yolo`)" ([source](https://qwenlm.github.io/qwen-code-docs/en/users/features/headless/))

### 4. Or use this repo's container

[`examples/cloud-agent-runner`](../examples/cloud-agent-runner/README.md) builds an image with Qwen Code (and any other agents you list) and runs one task per container:

```bash
cd examples/cloud-agent-runner
docker build --build-arg AGENTS="qwen-code" -t cloud-agent .
docker run --rm --env-file .env cloud-agent run-task.sh qwen-code "Fix the failing tests"
```

## Gotchas when running in the cloud

- Qwen OAuth free tier was discontinued on 2026-04-15; use an API key or Coding Plan on servers. ([source](https://qwenlm.github.io/qwen-code-docs/en/users/configuration/auth/))
- In CI, SSH, or containers you typically cannot complete the OAuth browser login. ([source](https://qwenlm.github.io/qwen-code-docs/en/users/configuration/auth/))
- npm install requires Node.js 22+. ([source](https://github.com/QwenLM/qwen-code))
- Env precedence: shell export > .env > settings.json env. ([source](https://qwenlm.github.io/qwen-code-docs/en/users/configuration/auth/))
- general.enableAutoUpdate defaults to true and installs updates on startup; disable in images. ([source](https://qwenlm.github.io/qwen-code-docs/en/users/configuration/settings/))
- Docker sandbox mounts workspace and ~/.qwen and pulls a published sandbox image on demand. ([source](https://qwenlm.github.io/qwen-code-docs/en/users/features/sandbox/))
- Linux execution sandbox expects bwrap at /usr/bin/bwrap. ([source](https://qwenlm.github.io/qwen-code-docs/en/users/features/sandbox/))
- Forked from Google Gemini CLI v0.8.2, developed independently since v0.1, so flags resemble Gemini CLI but differ. ([source](https://github.com/QwenLM/qwen-code))
- To make sure Qwen Code reads `AGENTS.md`, add it to `context.fileName` in `.qwen/settings.json`. ([source](https://qwenlm.github.io/qwen-code-docs/en/users/features/memory/))

## Sources

- <https://github.com/QwenLM/qwen-code>
- <https://qwenlm.github.io/qwen-code-docs/en/users/configuration/auth/>
- <https://qwenlm.github.io/qwen-code-docs/en/users/configuration/settings/>
- <https://qwenlm.github.io/qwen-code-docs/en/users/features/headless/>
- <https://qwenlm.github.io/qwen-code-docs/en/users/features/mcp/>
- <https://qwenlm.github.io/qwen-code-docs/en/users/features/memory/>
- <https://qwenlm.github.io/qwen-code-docs/en/users/features/sandbox/>
<!-- END GENERATED: agent:qwen-code -->

---

See all agents: [agent comparison](README.md) · [Run any agent in parallel on Northflank](../examples/northflank-parallel-harnesses/README.md) · [Running agents headlessly](../guides/running-agents-headless.md)
