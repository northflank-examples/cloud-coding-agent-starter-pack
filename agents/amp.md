# How to run Amp in the cloud

Amp's agentic coding tool (originally from Sourcegraph). This guide covers running Amp on a remote machine instead of your laptop: on Northflank Cloud Harness, on any Linux VM, or in a container. It shows how to install it, log in without a browser, run tasks headlessly with permission prompts off, and what to watch for. Every fact below is quoted from or linked to the vendor's own documentation.

<!-- BEGIN GENERATED: agent:amp -->
Last verified: **2026-10-19** · Docs: <https://ampcode.com/docs>

## At a glance

|  |  |
| --- | --- |
| Made by | Amp (spun out of Sourcegraph) |
| Licence | Proprietary |
| Models | Models served and billed by Amp, chosen per mode; can route through your own API keys or subscriptions |
| Headless command | `amp -x "<task>"` |
| Skip permission prompts | Not needed: Amp runs tools without asking. Restrict with a policy plugin |
| JSON output | `--stream-json` (with `-x`) |
| Resume a session | `amp threads continue <thread-id>` |
| Choose a model | not documented |
| Auth on a server | `AMP_API_KEY` |
| Instructions file | `AGENTS.md` |
| Config and credentials | `~/.config/amp/settings.json`; workspace `.amp/settings.json` |
| Built-in sandbox | None locally |
| MCP | Yes: `amp mcp add`, `--mcp-config` |
| Northflank Cloud Harness | install in an empty sandbox |
| Billing | Monthly tiers include usage; beyond that, prepaid credits at cost |

## Option 1: Run Amp on Northflank Cloud Harness

Cloud Harness doesn't preinstall Amp, but its **Empty sandbox** option gives you the same isolated microVM, persistent workspace, terminal and SSH access with no agent set up. Install Amp once and it stays installed across pauses:

1. **Harnesses** → **Create harness** → choose **Empty sandbox**, select your repository, and create it.
2. Under **Environment**, add the agent's credentials (`AMP_API_KEY`) as runtime variables, then click **Update & restart**.
3. In the harness terminal, run the install command from [step 1 below](#1-install), then run Amp as in [step 3](#3-run-a-task-headlessly).

Install into the home directory (the persistent volume) rather than system directories, so the agent survives restarts. [`install-agents.sh`](../examples/cloud-agent-runner/install-agents.sh) does this for you: `bash install-agents.sh amp`.

To start one empty-sandbox harness per task from a script, with the installer and the task already in the workspace, use [`launch.sh`](../examples/northflank-parallel-harnesses/README.md):

```bash
AGENT=amp AGENT_ENV="AMP_API_KEY" NF_PROJECT=my-project \
REPO_URL=https://github.com/your-org/your-repo \
  ./launch.sh tasks.txt
```

Pause the harness when you're done: compute stops and the workspace is kept. See the [Cloud Harness tutorial](../tutorials/northflank-cloud-harness/README.md).

## Option 2: Run Amp on any Linux VM or container

### 1. Install

**Install script**:

```bash
curl -fsSL https://ampcode.com/install.sh | bash
```

Check it worked: `amp version`. Install docs: <https://ampcode.com/docs/cli>.

### 2. Authenticate without a browser

Cloud machines usually can't open a browser login, so use one of these:

| Method | Environment variables | How |
| --- | --- | --- |
| API key env var | `AMP_API_KEY` | Create an access token (starts with sgamp_) at https://ampcode.com/settings/security#access-token and export AMP_API_KEY=... It takes precedence over saved accounts. ([source](https://ampcode.com/docs/cli/execute-mode)) |
| interactive login | — | `amp login` adds a saved account. The docs don't describe a browserless or device-code flow for it, so use AMP_API_KEY on servers. ([source](https://ampcode.com/docs/cli)) |

### 3. Run a task headlessly

Work on a branch, let the agent finish without prompts, then commit and push for review:

```bash
git switch -c agent/my-task
amp -x "Fix the failing tests"
git add -A && git commit -m "agent: my task" && git push -u origin HEAD
```

| Part | What it does |
| --- | --- |
| `-x` | Execute mode: send the prompt, wait for the agent to finish, print the final message and exit |
| `(no approval flag)` | Amp runs tools, including shell commands, without asking, so run it only in an isolated environment |

- **Headless mode:** Sends the prompt, waits for the agent to end its turn, prints the final message to stdout, then exits. Stdin can be piped in as well. Redirecting stdout turns execute mode on automatically. Execute mode uses Standard mode unless you pass --fast. `-ox` runs the prompt in a remote orb and returns the thread URL right away. Docs: "it sends the message
provided to `-x` to the agent, waits until the agent ends its turn, prints its final message, and
exits." ([source](https://ampcode.com/docs/cli/execute-mode))

- **Permissions:** The current docs do not mention the --dangerously-allow-all flag from the hint. The only documented way to restrict tools is a policy plugin. Docs: "By default, Amp does not ask for approval before running tools." ([source](https://ampcode.com/docs/tools))

### 4. Or use this repo's container

[`examples/cloud-agent-runner`](../examples/cloud-agent-runner/README.md) builds an image with Amp (and any other agents you list) and runs one task per container:

```bash
cd examples/cloud-agent-runner
docker build --build-arg AGENTS="amp" -t cloud-agent .
docker run --rm --env-file .env cloud-agent run-task.sh amp "Fix the failing tests"
```

## Gotchas when running in the cloud

- Amp never asks before running tools, including shell commands. Run it in an isolated container or VM. ([source](https://ampcode.com/docs/tools))
- AMP_API_KEY must be a long-lived sgamp_ access token. The session token from `amp login` is rejected because it expires within an hour. ([source](https://ampcode.com/docs/cli/execute-mode))
- The installer symlinks amp into ~/.local/bin, so make sure that directory is on PATH. ([source](https://ampcode.com/install.sh))
- By default agent commits get 'Amp-Thread-ID' and 'Co-authored-by: Amp' trailers. Turn them off with AMP_DISABLE_AMP_THREAD_TRAILER=1 / AMP_DISABLE_AMP_COAUTHOR_TRAILER=1. ([source](https://ampcode.com/docs/cli/settings))
- Amp auto-installs updates in the background. Pin a version with AMP_SKIP_UPDATE_CHECK=1 or amp.updates.mode. ([source](https://ampcode.com/docs/cli))
- With plugins, pass --plugin-ready-timeout so execute mode waits for them to load. Otherwise agent.start/agent.end events are skipped. ([source](https://ampcode.com/docs/cli/execute-mode))
- A server can act as a 'runner' (`amp --no-tui --runner-id <id>`) that runs threads started from other clients. ([source](https://ampcode.com/docs/cli))

## Sources

- <https://ampcode.com/docs/cli>
- <https://ampcode.com/docs/cli/execute-mode>
- <https://ampcode.com/docs/cli/settings>
- <https://ampcode.com/docs/cli/streaming-json>
- <https://ampcode.com/docs/customize/agents-md>
- <https://ampcode.com/docs/customize/mcp>
- <https://ampcode.com/docs/customize/model-routing>
- <https://ampcode.com/docs/pricing>
- <https://ampcode.com/docs/the-dial>
- <https://ampcode.com/docs/threads>
- <https://ampcode.com/docs/tools>
- <https://ampcode.com/install.sh>
- <https://www.npmjs.com/package/@sourcegraph/amp>
<!-- END GENERATED: agent:amp -->

---

See all agents: [agent comparison](README.md) · [Run any agent in parallel on Northflank](../examples/northflank-parallel-harnesses/README.md) · [Running agents headlessly](../guides/running-agents-headless.md)
