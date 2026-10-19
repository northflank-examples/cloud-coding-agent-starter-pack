# How to run Aider in the cloud

Open-source AI pair programmer that edits files and commits to git. This guide covers running Aider on a remote machine instead of your laptop: on Northflank Cloud Harness, on any Linux VM, or in a container. It shows how to install it, log in without a browser, run tasks headlessly with permission prompts off, and what to watch for. Every fact below is quoted from or linked to the vendor's own documentation.

<!-- BEGIN GENERATED: agent:aider -->
Last verified: **2026-10-19** · Docs: <https://aider.chat/docs/> · Source: <https://github.com/Aider-AI/aider>

## At a glance

|  |  |
| --- | --- |
| Made by | Paul Gauthier and contributors |
| Licence | Apache-2.0 (open source) |
| Models | Any provider LiteLLM supports (OpenAI, Anthropic, Gemini, DeepSeek, OpenRouter and more) and local models |
| Headless command | `aider --message "<task>"` |
| Skip permission prompts | `--yes-always`. Aider has no tool-permission system |
| JSON output | not documented |
| Resume a session | `--restore-chat-history` |
| Choose a model | `--model` (or `AIDER_MODEL`) |
| Auth on a server | Provider key, e.g. `ANTHROPIC_API_KEY` |
| Instructions file | None loaded automatically; pass e.g. `--read CONVENTIONS.md` |
| Config and credentials | `.aider.conf.yml` and `.env` (home, git root, current directory) |
| Built-in sandbox | None |
| MCP | Not documented |
| Northflank Cloud Harness | install in an empty sandbox |
| Billing | Free (Apache-2.0); you pay your model provider |

## Option 1: Run Aider on Northflank Cloud Harness

Cloud Harness doesn't preinstall Aider, but its **Empty sandbox** option gives you the same isolated microVM, persistent workspace, terminal and SSH access with no agent set up. Install Aider once and it stays installed across pauses:

1. **Harnesses** → **Create harness** → choose **Empty sandbox**, select your repository, and create it.
2. Under **Environment**, add the agent's credentials (Provider key, e.g. `ANTHROPIC_API_KEY`) as runtime variables, then click **Update & restart**.
3. In the harness terminal, run the install command from [step 1 below](#1-install), then run Aider as in [step 3](#3-run-a-task-headlessly).

Install into the home directory (the persistent volume) rather than system directories, so the agent survives restarts. [`install-agents.sh`](../examples/cloud-agent-runner/install-agents.sh) does this for you: `bash install-agents.sh aider`.

To start one empty-sandbox harness per task from a script, with the installer and the task already in the workspace, use [`launch.sh`](../examples/northflank-parallel-harnesses/README.md):

```bash
AGENT=aider AGENT_ENV="OPENAI_API_KEY" NF_PROJECT=my-project \
REPO_URL=https://github.com/your-org/your-repo \
  ./launch.sh tasks.txt
```

Pause the harness when you're done: compute stops and the workspace is kept. See the [Cloud Harness tutorial](../tutorials/northflank-cloud-harness/README.md).

## Option 2: Run Aider on any Linux VM or container

### 1. Install

**Install script**:

```bash
curl -LsSf https://aider.chat/install.sh | sh
```

**pip**:

```bash
python -m pip install aider-install && aider-install
```

Check it worked: `aider --version`. Install docs: <https://aider.chat/docs/install.html>.

### 2. Authenticate without a browser

Cloud machines usually can't open a browser login, so use one of these:

| Method | Environment variables | How |
| --- | --- | --- |
| Provider API key env vars / .env | `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, `GEMINI_API_KEY`, `OPENROUTER_API_KEY`, `DEEPSEEK_API_KEY`, `<PROVIDER>_API_KEY` | Export the provider key, put it in a .env file (home dir, git root, cwd, or --env-file), or pass --api-key provider=<key> / --openai-api-key / --anthropic-api-key. There's no Aider account or login. ([source](https://aider.chat/docs/config/api-keys.html)) |

### 3. Run a task headlessly

Work on a branch, let the agent finish without prompts, then commit and push for review:

```bash
git switch -c agent/my-task
aider --message "Fix the failing tests" --yes-always --no-auto-commits
git add -A && git commit -m "agent: my task" && git push -u origin HEAD
```

| Part | What it does |
| --- | --- |
| `--message` | Run one instruction, apply the edits and exit |
| `--yes-always` | Answer yes to every confirmation |
| `--no-auto-commits` | Leave changes uncommitted so your script commits them. By default Aider commits every edit |

- **Headless mode:** Runs the single instruction, applies the edits to the files and exits. -m/--msg are aliases. --message-file / -f reads the prompt from a file. Edits are git-committed by default. Docs: "It will do that one thing, apply the edits to the files and then exit." ([source](https://aider.chat/docs/scripting.html))

- **Permissions:** The scripting page lists the flag as `--yes`. The options reference lists `--yes-always`. Aider has no tool-permission system. It suggests shell commands rather than running tools autonomously. Docs: "Always say yes to every confirmation" ([source](https://aider.chat/docs/config/options.html))

### 4. Or use this repo's container

[`examples/cloud-agent-runner`](../examples/cloud-agent-runner/README.md) builds an image with Aider (and any other agents you list) and runs one task per container:

```bash
cd examples/cloud-agent-runner
docker build --build-arg AGENTS="aider" -t cloud-agent .
docker run --rm --env-file .env cloud-agent run-task.sh aider "Fix the failing tests"
```

## Gotchas when running in the cloud

- Aider git-commits every edit by default, and commits pre-existing dirty changes first. Use --no-auto-commits / --no-dirty-commits to keep the working tree for your own pipeline. ([source](https://aider.chat/docs/git.html))
- Commits get a Co-authored-by trailer and aider author/committer attribution by default. Control this with --attribute-* flags. ([source](https://aider.chat/docs/config/options.html))
- Launched outside a git repo, Aider asks to create one. Run it inside a repo, or pass --no-git. ([source](https://aider.chat/docs/git.html))
- Pass the files to edit on the command line, because --message works on the files given. ([source](https://aider.chat/docs/scripting.html))
- In the official Docker image, run as your own UID (--user $(id -u):$(id -g)) and mount the repo at /app. ([source](https://aider.chat/docs/install/docker.html))
- The pipx install supports only Python 3.9-3.12. aider-install / uv provision Python 3.12 automatically. ([source](https://aider.chat/docs/install.html))
- Since there's no account, billing goes straight to whichever model provider's API key you use. ([source](https://aider.chat/docs/config/api-keys.html))

## Not documented / open questions

- The official docs don't mention MCP support.
- There's no JSON or machine-readable output mode in the options reference.
- It's not documented whether --yes-always auto-runs suggested shell commands in --message mode. To be safe, use --no-suggest-shell-commands.
- The scripting page uses `--yes`, while the current options reference lists `--yes-always`.
- The newest GitHub release (v0.86.0) is from 2025-08-09, while PyPI has 0.86.2. How actively it's maintained should be checked.

## Sources

- <https://aider.chat/docs/config/aider_conf.html>
- <https://aider.chat/docs/config/api-keys.html>
- <https://aider.chat/docs/config/options.html>
- <https://aider.chat/docs/git.html>
- <https://aider.chat/docs/install.html>
- <https://aider.chat/docs/install/docker.html>
- <https://aider.chat/docs/llms/other.html>
- <https://aider.chat/docs/more/analytics.html>
- <https://aider.chat/docs/scripting.html>
- <https://aider.chat/docs/usage/conventions.html>
- <https://github.com/Aider-AI/aider/blob/main/LICENSE.txt>
<!-- END GENERATED: agent:aider -->

---

See all agents: [agent comparison](README.md) · [Run any agent in parallel on Northflank](../examples/northflank-parallel-harnesses/README.md) · [Running agents headlessly](../guides/running-agents-headless.md)
