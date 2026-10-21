# How to run GitHub Copilot CLI in the cloud

GitHub Copilot's coding agent in the terminal. This guide covers running GitHub Copilot CLI on a remote machine instead of your laptop: on Northflank Cloud Harness, on any Linux VM, or in a container. It shows how to install it, log in without a browser, run tasks headlessly with permission prompts off, and what to watch for. Every fact below is quoted from or linked to the vendor's own documentation.

<!-- BEGIN GENERATED: agent:copilot-cli -->
Last verified: **2026-10-19** · Docs: <https://docs.github.com/copilot/concepts/agents/about-copilot-cli> · Source: <https://github.com/github/copilot-cli>

## At a glance

|  |  |
| --- | --- |
| Made by | GitHub |
| Licence | Proprietary |
| Models | Copilot-hosted Claude, GPT and Gemini models; bring-your-own-key providers via `providers.json` |
| Headless command | `copilot -p "<task>"` |
| Skip permission prompts | `--allow-all-tools` (or `--allow-all` / `--yolo`); safer: `--allow-tool='shell(git:*)'`, `--deny-tool` |
| JSON output | `--output-format=json` (JSON Lines) |
| Resume a session | `--resume[=id]`, `--continue` |
| Choose a model | `--model=<model>` |
| Auth on a server | `COPILOT_GITHUB_TOKEN` (fine-grained PAT), or `copilot login --device-code` |
| Instructions file | `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, `.github/copilot-instructions.md` |
| Config and credentials | `~/.copilot/`; tokens in the system keychain, or plain text under `~/.copilot/` without one |
| Built-in sandbox | Optional: bubblewrap on Linux, off by default |
| MCP | Yes: GitHub MCP server built in; `~/.copilot/mcp-config.json` |
| Northflank Cloud Harness | install in an empty sandbox |
| Billing | Requires a Copilot subscription; usage draws on its AI credits |

## Option 1: Run GitHub Copilot CLI on Northflank Cloud Harness

Cloud Harness doesn't preinstall GitHub Copilot CLI, but its **Empty sandbox** option gives you the same isolated microVM, persistent workspace, terminal and SSH access with no agent set up. Install GitHub Copilot CLI once and it stays installed across pauses:

1. **Harnesses** → **Create harness** → choose **Empty sandbox**, select your repository, and create it.
2. Under **Environment**, add the agent's credentials (`COPILOT_GITHUB_TOKEN` (fine-grained PAT), or `copilot login --device-code`) as runtime variables, then click **Update & restart**.
3. In the harness terminal, run the install command from [step 1 below](#1-install), then run GitHub Copilot CLI as in [step 3](#3-run-a-task-headlessly).

Install into the home directory (the persistent volume) rather than system directories, so the agent survives restarts. [`install-agents.sh`](../examples/cloud-agent-runner/install-agents.sh) does this for you: `bash install-agents.sh copilot-cli`.

To start one empty-sandbox harness per task from a script, with the installer and the task already in the workspace, use [`launch.sh`](../examples/northflank-parallel-harnesses/README.md):

```bash
AGENT=copilot-cli AGENT_ENV="COPILOT_GITHUB_TOKEN" NF_PROJECT=my-project \
REPO_URL=https://github.com/your-org/your-repo \
  ./launch.sh tasks.txt
```

Pause the harness when you're done: compute stops and the workspace is kept. See the [Cloud Harness tutorial](../tutorials/northflank-cloud-harness/README.md).

## Option 2: Run GitHub Copilot CLI on any Linux VM or container

### 1. Install

**Install script**:

```bash
curl -fsSL https://gh.io/copilot-install | bash
```

**npm**:

```bash
npm install -g @github/copilot
```

Check it worked: `copilot --version`. Install docs: <https://github.com/github/copilot-cli>.

### 2. Authenticate without a browser

Cloud machines usually can't open a browser login, so use one of these:

| Method | Environment variables | How |
| --- | --- | --- |
| Token env var | `COPILOT_GITHUB_TOKEN`, `GH_TOKEN`, `GITHUB_TOKEN` | Create a fine-grained PAT (github.com/settings/personal-access-tokens/new) with the 'Copilot Requests' permission and export it as COPILOT_GITHUB_TOKEN (checked first, then GH_TOKEN, then GITHUB_TOKEN). Classic ghp_ PATs are not supported. ([source](https://docs.github.com/en/copilot/reference/cli-command-reference)) |
| login on headless (device code) | — | Run `copilot login --device-code` (the default over SSH, in dev containers and in CI). Enter the shown code at github.com on any device. Or pipe a token: `copilot login --with-token < token.txt`. ([source](https://docs.github.com/en/copilot/reference/cli-command-reference)) |

### 3. Run a task headlessly

Work on a branch, let the agent finish without prompts, then commit and push for review:

```bash
git switch -c agent/my-task
copilot -p "Fix the failing tests" --allow-all-tools --no-ask-user
git add -A && git commit -m "agent: my task" && git push -u origin HEAD
```

| Part | What it does |
| --- | --- |
| `-p` | Run the prompt non-interactively and exit |
| `--allow-all-tools` | Run tools, including shell commands, without asking. Narrow it with `--allow-tool` / `--deny-tool` |
| `--no-ask-user` | Don't stop to ask clarifying questions |

- **Headless mode:** Runs the prompt and exits when done. Prints the response to stdout. -s/--silent drops usage stats. Piping a prompt on stdin also works. The exit summary includes a `copilot --resume=SESSION-ID` hint. -p waits up to COPILOT_TASK_WAIT_TIMEOUT_SECONDS (default 600) for background tasks. Docs: "Execute a prompt programmatically (exits after completion)." ([source](https://docs.github.com/en/copilot/reference/cli-command-reference))

- **Permissions:** The docs recommend minimal --allow-tool grants and say to avoid --allow-all outside a sandbox. permissions.disableBypassPermissionsMode can block the allow-all options. Docs: "Allow all tools to run automatically without confirmation. Required when using the CLI programmatically (env: `COPILOT_ALLOW_ALL`)." ([source](https://docs.github.com/en/copilot/reference/cli-command-reference))

### 4. Or use this repo's container

[`examples/cloud-agent-runner`](../examples/cloud-agent-runner/README.md) builds an image with GitHub Copilot CLI (and any other agents you list) and runs one task per container:

```bash
cd examples/cloud-agent-runner
docker build --build-arg AGENTS="copilot-cli" -t cloud-agent .
docker run --rm --env-file .env cloud-agent run-task.sh copilot-cli "Fix the failing tests"
```

## Gotchas when running in the cloud

- Classic PATs (ghp_) are not supported. Use a fine-grained PAT with the 'Copilot Requests' permission. ([source](https://docs.github.com/en/copilot/reference/cli-command-reference))
- With no system credential store, which is typical in containers, a token from `copilot login` is saved in plain text under ~/.copilot/. ([source](https://docs.github.com/en/copilot/reference/cli-command-reference))
- Use --no-ask-user in automation so the agent doesn't stop to ask questions. ([source](https://docs.github.com/en/copilot/how-tos/copilot-cli/automate-copilot-cli/automate-with-actions))
- In -p mode, workspace MCP servers, repo extensions and repo hooks are off by default. Opt in with GITHUB_COPILOT_PROMPT_MODE_* env vars or --trust-folder. ([source](https://docs.github.com/en/copilot/reference/cli-command-reference))
- Local sandboxing is off by default, so shell commands run with your user's full access. The Linux sandbox needs bwrap >= 0.5.0 and slirp4netns, and is switched off for the session if the host doesn't support it. ([source](https://docs.github.com/en/copilot/concepts/about-cloud-and-local-sandboxes))
- COPILOT_GITHUB_TOKEN and GITHUB_TOKEN values are redacted from output by default. Use --secret-env-vars to redact other variables from shell and MCP environments. ([source](https://docs.github.com/en/copilot/reference/cli-command-reference))
- Org or enterprise admins can disable the CLI by policy. ([source](https://github.com/github/copilot-cli))

## Sources

- <https://docs.github.com/copilot/concepts/agents/about-copilot-cli>
- <https://docs.github.com/en/copilot/concepts/about-cloud-and-local-sandboxes>
- <https://docs.github.com/en/copilot/how-tos/copilot-cli/automate-copilot-cli/automate-with-actions>
- <https://docs.github.com/en/copilot/reference/cli-command-reference>
- <https://github.com/github/copilot-cli>
- <https://github.com/github/copilot-cli/blob/main/LICENSE.md>
<!-- END GENERATED: agent:copilot-cli -->

---

See all agents: [agent comparison](README.md) · [Run any agent in parallel on Northflank](../examples/northflank-parallel-harnesses/README.md) · [Running agents headlessly](../guides/running-agents-headless.md)
