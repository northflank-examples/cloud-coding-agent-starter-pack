# How to run Gemini CLI in the cloud

Google's open-source terminal agent for Gemini models. This guide covers running Gemini CLI on a remote machine instead of your laptop: on Northflank Cloud Harness, on any Linux VM, or in a container. It shows how to install it, log in without a browser, run tasks headlessly with permission prompts off, and what to watch for. Every fact below is quoted from or linked to the vendor's own documentation.

<!-- BEGIN GENERATED: agent:gemini-cli -->
Last verified: **2026-10-19** · Docs: <https://www.geminicli.com/docs/> · Source: <https://github.com/google-gemini/gemini-cli>

## At a glance

|  |  |
| --- | --- |
| Made by | Google |
| Licence | Apache-2.0 (open source) |
| Models | Gemini models only, via the Gemini API, Vertex AI or Code Assist |
| Headless command | `gemini -p "<task>"` |
| Skip permission prompts | `--approval-mode=yolo`; safer: `--approval-mode=auto_edit`. `--yolo` is deprecated |
| JSON output | `--output-format json` or `stream-json` |
| Resume a session | `--resume latest` |
| Choose a model | `-m, --model` |
| Auth on a server | `GEMINI_API_KEY`, or a Vertex AI service account |
| Instructions file | `GEMINI.md` (add `AGENTS.md` via `context.fileName`) |
| Config and credentials | `~/.gemini/settings.json` and `~/.gemini/.env` |
| Built-in sandbox | Optional: Docker, Podman, gVisor or Seatbelt (`--sandbox`) |
| MCP | Yes: `gemini mcp add`, `mcpServers` in settings |
| Northflank Cloud Harness | install in an empty sandbox |
| Billing | Gemini API key (pay-as-you-go), Vertex AI, or Code Assist Standard/Enterprise. Free Google sign-in moved to Antigravity CLI |

## Option 1: Run Gemini CLI on Northflank Cloud Harness

Cloud Harness doesn't preinstall Gemini CLI, but its **Empty sandbox** option gives you the same isolated microVM, persistent workspace, terminal and SSH access with no agent set up. Install Gemini CLI once and it stays installed across pauses:

1. **Harnesses** → **Create harness** → choose **Empty sandbox**, select your repository, and create it.
2. Under **Environment**, add the agent's credentials (`GEMINI_API_KEY`, or a Vertex AI service account) as runtime variables, then click **Update & restart**.
3. In the harness terminal, run the install command from [step 1 below](#1-install), then run Gemini CLI as in [step 3](#3-run-a-task-headlessly).

Install into the home directory (the persistent volume) rather than system directories, so the agent survives restarts. [`install-agents.sh`](../examples/cloud-agent-runner/install-agents.sh) does this for you: `bash install-agents.sh gemini-cli`.

To start one empty-sandbox harness per task from a script, with the installer and the task already in the workspace, use [`launch.sh`](../examples/northflank-parallel-harnesses/README.md):

```bash
AGENT=gemini-cli AGENT_ENV="GEMINI_API_KEY" NF_PROJECT=my-project \
REPO_URL=https://github.com/your-org/your-repo \
  ./launch.sh tasks.txt
```

Pause the harness when you're done: compute stops and the workspace is kept. See the [Cloud Harness tutorial](../tutorials/northflank-cloud-harness/README.md).

## Option 2: Run Gemini CLI on any Linux VM or container

### 1. Install

**npm** (requires Node.js 20+):

```bash
npm install -g @google/gemini-cli
```

Check it worked: `gemini --version`. Install docs: <https://github.com/google-gemini/gemini-cli>.

### 2. Authenticate without a browser

Cloud machines usually can't open a browser login, so use one of these:

| Method | Environment variables | How |
| --- | --- | --- |
| Gemini API key (Google AI Studio) | `GEMINI_API_KEY` | export GEMINI_API_KEY=...; headless runs use env vars when no cached credential exists. Can also be placed in .env (searched upward from cwd, then ~/.gemini/.env; first file found wins). ([source](https://github.com/google-gemini/gemini-cli)) |
| Vertex AI with service account JSON key (recommended for CI/non-interactive) | `GOOGLE_CLOUD_PROJECT`, `GOOGLE_CLOUD_LOCATION`, `GOOGLE_APPLICATION_CREDENTIALS`, `GOOGLE_GENAI_USE_VERTEXAI` | Unset GOOGLE_API_KEY and GEMINI_API_KEY; create service account with 'Vertex AI User' role; export GOOGLE_APPLICATION_CREDENTIALS=/abs/path/key.json, GOOGLE_CLOUD_PROJECT, GOOGLE_CLOUD_LOCATION. README also shows GOOGLE_GENAI_USE_VERTEXAI=true. ([source](https://geminicli.com/docs/get-started/authentication/)) |
| Vertex AI with Google Cloud API key | `GOOGLE_API_KEY`, `GOOGLE_GENAI_USE_VERTEXAI`, `GOOGLE_CLOUD_PROJECT`, `GOOGLE_CLOUD_LOCATION` | export GOOGLE_API_KEY=... and GOOGLE_GENAI_USE_VERTEXAI=true ([source](https://github.com/google-gemini/gemini-cli)) |
| Google Cloud metadata / ADC (Compute Engine, Cloud Shell) | — | On Compute Engine, Gemini CLI uses Application Default Credentials from the metadata server; Cloud Shell is automatic. ([source](https://geminicli.com/docs/get-started/authentication/)) |
| Sign in with Google (OAuth) — needs a browser; for paid Code Assist licenses set GOOGLE_CLOUD_PROJECT | `GOOGLE_CLOUD_PROJECT` | Not browser-free. Unpaid tier and Google One users were moved to Antigravity CLI on June 18, 2026. ([source](https://geminicli.com/docs/get-started/authentication/)) |

### 3. Run a task headlessly

Work on a branch, let the agent finish without prompts, then commit and push for review:

```bash
git switch -c agent/my-task
gemini -p "Fix the failing tests" --approval-mode=yolo
git add -A && git commit -m "agent: my task" && git push -u origin HEAD
```

| Part | What it does |
| --- | --- |
| `-p` | Headless mode: run the prompt and exit. Exit codes: 0 success, 1 error, 42 input error, 53 turn limit |
| `--approval-mode=yolo` | Approve every tool call. Use `auto_edit` to approve only file edits |

- **Headless mode:** Exit codes: 0 success, 1 general/API error, 42 input error, 53 turn limit exceeded. Docs: "Prompt text. Appended to stdin input if provided. Forces non-interactive mode." ([source](https://geminicli.com/docs/cli/cli-reference/))

- **Permissions:** Combine with --sandbox / GEMINI_SANDBOX for isolation. Docs: "Approval mode for tool execution. Choices: `default`, `auto_edit`, `yolo`, `plan`" ([source](https://geminicli.com/docs/cli/cli-reference/))

### 4. Or use this repo's container

[`examples/cloud-agent-runner`](../examples/cloud-agent-runner/README.md) builds an image with Gemini CLI (and any other agents you list) and runs one task per container:

```bash
cd examples/cloud-agent-runner
docker build --build-arg AGENTS="gemini-cli" -t cloud-agent .
docker run --rm --env-file .env cloud-agent run-task.sh gemini-cli "Fix the failing tests"
```

## Gotchas when running in the cloud

- Unpaid tier and Google One users: Gemini CLI was replaced by Antigravity CLI on June 18th, 2026; Google AI Pro/Ultra and Code Assist for individuals stop being served. ([source](https://github.com/google-gemini/gemini-cli))
- Gemini CLI is not optimized for Gemini 4 Argon; Google points to Antigravity for that model. ([source](https://github.com/google-gemini/gemini-cli))
- Sign in with Google needs a browser that can reach the terminal; on servers use GEMINI_API_KEY or Vertex service account. ([source](https://geminicli.com/docs/get-started/authentication/))
- For Vertex ADC/service-account auth, unset GOOGLE_API_KEY and GEMINI_API_KEY, which interfere. ([source](https://geminicli.com/docs/get-started/authentication/))
- .env is loaded from the first file found walking up from cwd, then ~/.gemini/.env; not merged. ([source](https://geminicli.com/docs/get-started/authentication/))
- Docker sandbox from inside a container requires sharing the host Docker socket and matching workspace paths. ([source](https://geminicli.com/docs/cli/sandbox/))
- Headless exit code 53 means turn limit exceeded, 42 input error. ([source](https://geminicli.com/docs/cli/headless/))
- general.enableAutoUpdate defaults to true; disable in images. ([source](https://geminicli.com/docs/reference/configuration/))

## Sources

- <https://developers.googleblog.com/an-important-update-transitioning-gemini-cli-to-antigravity-cli>
- <https://geminicli.com/docs/cli/cli-reference/>
- <https://geminicli.com/docs/cli/headless/>
- <https://geminicli.com/docs/cli/sandbox/>
- <https://geminicli.com/docs/get-started/authentication/>
- <https://geminicli.com/docs/reference/configuration/>
- <https://geminicli.com/docs/resources/quota-and-pricing/>
- <https://geminicli.com/docs/tools/mcp-server/>
- <https://github.com/google-gemini/gemini-cli>
<!-- END GENERATED: agent:gemini-cli -->

---

See all agents: [agent comparison](README.md) · [Run any agent in parallel on Northflank](../examples/northflank-parallel-harnesses/README.md) · [Running agents headlessly](../guides/running-agents-headless.md)
