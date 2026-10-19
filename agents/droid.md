# How to run Factory Droid in the cloud

Factory's coding agent CLI. This guide covers running Factory Droid on a remote machine instead of your laptop: on Northflank Cloud Harness, on any Linux VM, or in a container. It shows how to install it, log in without a browser, run tasks headlessly with permission prompts off, and what to watch for. Every fact below is quoted from or linked to the vendor's own documentation.

<!-- BEGIN GENERATED: agent:droid -->
Last verified: **2026-10-19** · Docs: <https://docs.factory.com/droid-cli/overview>

## At a glance

|  |  |
| --- | --- |
| Made by | Factory |
| Licence | Proprietary |
| Models | Factory-hosted models (Anthropic, OpenAI and others); bring-your-own models in `~/.factory/settings.json` |
| Headless command | `droid exec "<task>"` |
| Skip permission prompts | `droid exec --auto low\|medium\|high`; `--skip-permissions-unsafe` for disposable environments. Read-only by default |
| JSON output | `-o json` or `stream-json` |
| Resume a session | `droid exec -s <session-id>` |
| Choose a model | `-m, --model` |
| Auth on a server | `FACTORY_API_KEY` |
| Instructions file | `AGENTS.md` (also `CLAUDE.md`) |
| Config and credentials | `~/.factory/settings.json`; project `.factory/` |
| Built-in sandbox | Optional: bubblewrap + seccomp on Linux |
| MCP | Yes: `droid mcp add`, `.factory/mcp.json` |
| Northflank Cloud Harness | install in an empty sandbox |
| Billing | Factory Pro, Plus or Max plan |

## Option 1: Run Factory Droid on Northflank Cloud Harness

Cloud Harness doesn't preinstall Factory Droid, but its **Empty sandbox** option gives you the same isolated microVM, persistent workspace, terminal and SSH access with no agent set up. Install Factory Droid once and it stays installed across pauses:

1. **Harnesses** → **Create harness** → choose **Empty sandbox**, select your repository, and create it.
2. Under **Environment**, add the agent's credentials (`FACTORY_API_KEY`) as runtime variables, then click **Update & restart**.
3. In the harness terminal, run the install command from [step 1 below](#1-install), then run Factory Droid as in [step 3](#3-run-a-task-headlessly).

Install into the home directory (the persistent volume) rather than system directories, so the agent survives restarts. [`install-agents.sh`](../examples/cloud-agent-runner/install-agents.sh) does this for you: `bash install-agents.sh droid`.

To start one empty-sandbox harness per task from a script, with the installer and the task already in the workspace, use [`launch.sh`](../examples/northflank-parallel-harnesses/README.md):

```bash
AGENT=droid AGENT_ENV="FACTORY_API_KEY" NF_PROJECT=my-project \
REPO_URL=https://github.com/your-org/your-repo \
  ./launch.sh tasks.txt
```

Pause the harness when you're done: compute stops and the workspace is kept. See the [Cloud Harness tutorial](../tutorials/northflank-cloud-harness/README.md).

## Option 2: Run Factory Droid on any Linux VM or container

### 1. Install

**npm** (requires Node.js 20+):

```bash
npm install -g droid
```

**Install script**:

```bash
curl -fsSL https://app.factory.ai/cli | sh
```

Check it worked: `droid --version`. Install docs: <https://docs.factory.com/droid-cli/quickstart>.

### 2. Authenticate without a browser

Cloud machines usually can't open a browser login, so use one of these:

| Method | Environment variables | How |
| --- | --- | --- |
| API key env var | `FACTORY_API_KEY` | Generate a key at https://app.factory.ai/settings/api-keys and export FACTORY_API_KEY=fk-... ([source](https://docs.factory.com/droid-cli/cli-reference)) |

### 3. Run a task headlessly

Work on a branch, let the agent finish without prompts, then commit and push for review:

```bash
git switch -c agent/my-task
droid exec --auto medium "Fix the failing tests"
git add -A && git commit -m "agent: my task" && git push -u origin HEAD
```

| Part | What it does |
| --- | --- |
| `exec` | One-shot run that exits when done. Read-only unless you pass `--auto` |
| `--auto medium` | Allow edits, installs, builds, tests and local commits. `low` allows edits only; `high` adds pushes and deploys |

- **Headless mode:** One-shot run that writes to stdout/stderr and exits. Read-only by default. If an action needs more autonomy than allowed, it exits non-zero without making partial changes. Docs: "`droid exec` runs as a one-shot command that completes a task and exits" ([source](https://docs.factory.com/droid-exec/overview))

- **Permissions:** low allows file edits. medium adds installs, builds, tests and local git commits. high adds git push, deploys and migrations. Permission-rule blocks still apply even with --skip-permissions-unsafe. Preview them with `droid rules check`. Docs: "The default is spec-mode, where the agent is only allowed to execute read-only operations; add `--auto` to enable edits and commands, with risk tiers gating what can run." ([source](https://docs.factory.com/droid-exec/overview))

### 4. Or use this repo's container

[`examples/cloud-agent-runner`](../examples/cloud-agent-runner/README.md) builds an image with Factory Droid (and any other agents you list) and runs one task per container:

```bash
cd examples/cloud-agent-runner
docker build --build-arg AGENTS="droid" -t cloud-agent .
docker run --rm --env-file .env cloud-agent run-task.sh droid "Fix the failing tests"
```

## Gotchas when running in the cloud

- droid exec is read-only unless you pass --auto. Use --auto low for edits and --auto medium for installs, tests and commits. ([source](https://docs.factory.com/droid-exec/overview))
- Permission rules that resolve to 'ask' can't be approved in a one-shot run, even with --auto high. Rule blocks apply even with --skip-permissions-unsafe. ([source](https://docs.factory.com/droid-exec/overview))
- Use --skip-permissions-unsafe only in disposable containers, VMs or ephemeral CI runners. The docs show a docker run alpine example. ([source](https://docs.factory.com/droid-exec/overview))
- Standalone installs auto-update. Pin them with FACTORY_DROID_AUTO_UPDATE_ENABLED=false and `droid update --version X`, or install a pinned npm version. ([source](https://docs.factory.com/droid-cli/cli-reference))
- The docs recommend installing xdg-utils on Linux. ([source](https://docs.factory.com/droid-cli/quickstart))
- With the sandbox on and per-command mode, a command is blocked, not run unsandboxed, when bubblewrap or seccomp isn't available. ([source](https://docs.factory.com/autonomy-and-safety/sandbox))
- In `droid exec`, -r means --reasoning-effort, not --resume. ([source](https://docs.factory.com/droid-cli/cli-reference))

## Not documented / open questions

- Docs have moved from docs.factory.ai to docs.factory.com. Both links appear in the docs; install URLs still use app.factory.ai.
- There is no documented browserless or device-code login. Interactive sign-in uses the browser, so use FACTORY_API_KEY on servers.
- No env var for disabling telemetry was found in the CLI docs. An enterprise telemetry page exists but wasn't checked.
- The npm metadata points at a repo (github.com/Factory-AI/factory) that may not be public. The license is UNLICENSED.

## Sources

- <https://docs.factory.com/autonomy-and-safety/sandbox>
- <https://docs.factory.com/droid-cli/cli-reference>
- <https://docs.factory.com/droid-cli/quickstart>
- <https://docs.factory.com/droid-cli/settings>
- <https://docs.factory.com/droid-exec/overview>
- <https://docs.factory.com/harness/agents-md>
- <https://docs.factory.com/harness/mcp>
- <https://docs.factory.com/pricing/individuals>
- <https://www.npmjs.com/package/droid>
<!-- END GENERATED: agent:droid -->

---

See all agents: [agent comparison](README.md) · [Run any agent in parallel on Northflank](../examples/northflank-parallel-harnesses/README.md) · [Running agents headlessly](../guides/running-agents-headless.md)
