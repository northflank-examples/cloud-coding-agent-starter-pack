# How to run Devin CLI in the cloud

Cognition's terminal coding agent (formerly Devin for Terminal), using models served through your Devin account. This guide covers running Devin CLI on a remote machine instead of your laptop: on Northflank Cloud Harness, on any Linux VM, or in a container. It shows how to install it, log in without a browser, run tasks headlessly with permission prompts off, and what to watch for. Every fact below is quoted from or linked to the vendor's own documentation.

<!-- BEGIN GENERATED: agent:devin-cli -->
Last verified: **2026-10-19** · Docs: <https://docs.devin.ai/cli>

## At a glance

|  |  |
| --- | --- |
| Made by | Cognition |
| Licence | Proprietary |
| Models | Models served through your Devin account: Anthropic, OpenAI, Google and Cognition's SWE models, plus open models; no documented bring-your-own-key for the CLI |
| Headless command | `devin -p "<task>"` |
| Skip permission prompts | `--permission-mode dangerous` (alias `yolo`); safer: `accept-edits`, `smart`, or `autonomous` with `--sandbox` |
| JSON output | not documented |
| Resume a session | `-c` (latest) / `-r <session-id>` |
| Choose a model | `--model` (or `DEVIN_MODEL`) |
| Auth on a server | `devin auth login --force-manual-token-flow`, or a copied `credentials.toml` |
| Instructions file | `AGENTS.md` (also `CLAUDE.md` and other tools' rule files) |
| Config and credentials | `~/.config/devin/config.json`; credentials in `~/.local/share/devin/` |
| Built-in sandbox | Optional (preview): bubblewrap + seccomp on Linux via `--sandbox` |
| MCP | Yes: `devin mcp add` |
| Server / API mode | `devin acp` (Agent Client Protocol over stdio) |
| Northflank Cloud Harness | built in |
| Billing | Devin Pro, Max or Teams plan (shared usage quota); Enterprise billed in ACUs |

## Option 1: Run Devin CLI on Northflank Cloud Harness

Devin CLI is one of the agents Cloud Harness sets up for you: each harness is an isolated microVM with Devin CLI preinstalled, your repository cloned, a persistent workspace, a web terminal and SSH access.

1. In [Northflank](https://app.northflank.com), open a project → **Harnesses** → **Create harness**.
2. Choose **Devin CLI** as the agent, then pick Northflank's cloud or your own cloud account.
3. Authentication: the harness uses account mode for Devin CLI: sign in to your Devin account in the harness terminal (`devin auth login --force-manual-token-flow`).
4. Select the repository and branch, then **Create harness**. The terminal opens with the agent ready.

To start one harness per task from a script instead, use [`launch.sh`](../examples/northflank-parallel-harnesses/README.md) with `AGENT=devin-cli`:

```bash
AGENT=devin-cli NF_PROJECT=my-project \
REPO_URL=https://github.com/your-org/your-repo \
  ./launch.sh tasks.txt
```

Pause the harness when you're done: compute stops and the workspace is kept. See the [Cloud Harness tutorial](../tutorials/northflank-cloud-harness/README.md).

## Option 2: Run Devin CLI on any Linux VM or container

### 1. Install

**Install script**:

```bash
curl -fsSL https://cli.devin.ai/install.sh | bash
```

Check it worked: `devin --version`. Install docs: <https://docs.devin.ai/cli>.

### 2. Authenticate without a browser

Cloud machines usually can't open a browser login, so use one of these:

| Method | Environment variables | How |
| --- | --- | --- |
| Devin account login with manual token paste (no browser on the server) | — | On the server run `devin auth login --force-manual-token-flow` (or `devin setup --force-manual-token-flow`), complete sign-in in a browser on another machine and paste the token. Verify with `devin auth status`. Token is stored in $XDG_DATA_HOME/devin/credentials.toml (default ~/.local/share/devin/credentials.toml). ([source](https://docs.devin.ai/cli/reference/commands)) |
| Copy credentials file from an already-logged-in machine | `XDG_DATA_HOME` | Copy credentials.toml to ~/.local/share/devin/credentials.toml (or $XDG_DATA_HOME/devin/credentials.toml) on the server; treat as a secret (mount as a secret file). Token does not expire by default. ([source](https://docs.devin.ai/cli/enterprise/devin-auth)) |
| WINDSURF_API_KEY env var (documented for `devin acp` only) | `WINDSURF_API_KEY` | The ACP server (`devin acp`) reads WINDSURF_API_KEY if set. Not documented as an auth method for plain `devin`/`devin -p`. ([source](https://docs.devin.ai/cli/reference/commands)) |

### 3. Run a task headlessly

Work on a branch, let the agent finish without prompts, then commit and push for review:

```bash
git switch -c agent/my-task
devin -p "Fix the failing tests" --permission-mode dangerous \
  --respect-workspace-trust false
git add -A && git commit -m "agent: my task" && git push -u origin HEAD
```

| Part | What it does |
| --- | --- |
| `-p` | Print mode: run one turn, print the response and exit |
| `--permission-mode dangerous` | Approve every action (alias `yolo`). `accept-edits` approves file edits only |
| `--respect-workspace-trust false` | Skip the workspace-trust prompt, which print mode can't show; without it `-p` fails in an untrusted directory |

- **Headless mode:** -p/--print = single turn, prints response to stdout and exits. --prompt-file <FILE> loads the prompt from a file. In an untrusted directory -p fails because it cannot show the trust prompt, so pass --respect-workspace-trust false in scripts/CI. Truncated responses (max output tokens) exit non-zero in pipe mode. `devin --cloud -p` drives a Devin Cloud session instead of the local agent. Docs: "Non-interactive `--print` mode cannot show the workspace trust prompt, so it fails in an untrusted directory. Pass `--respect-workspace-trust false` to skip the check in scripts and CI." ([source](https://docs.devin.ai/cli/reference/commands))

- **Permissions:** Org-level deny/ask rules from Team Settings still apply in bypass/smart/autonomous. In autonomous mode direct edit/write tool calls still prompt, so it is not fully unattended in -p. Smart mode may not be enabled on every account. Docs: "`--permission-mode <MODE>` | | `DEVIN_PERMISSION_MODE` | Permission mode: `normal` (alias `auto`, the default), `accept-edits`, `smart`, `dangerous` (aliases `yolo`, `bypass`), or `autonomous` (requires `--sandbox`)." ([source](https://docs.devin.ai/cli/reference/commands))

### 4. Or use this repo's container

[`examples/cloud-agent-runner`](../examples/cloud-agent-runner/README.md) builds an image with Devin CLI (and any other agents you list) and runs one task per container:

```bash
cd examples/cloud-agent-runner
docker build --build-arg AGENTS="devin-cli" -t cloud-agent .
docker run --rm --env-file .env cloud-agent run-task.sh devin-cli "Fix the failing tests"
```

## Gotchas when running in the cloud

- The install script ends by running `devin setup`, an interactive auth/MCP setup wizard, so piping it in an unattended Dockerfile/provisioning step may need care. ([source](https://cli.devin.ai/install.sh))
- The installer symlinks ~/.local/bin/devin into ~/.local/share/devin/cli/_versions/current, so ~/.local/bin must be on PATH and the data dir must persist across restarts. ([source](https://cli.devin.ai/install.sh))
- `devin -p` fails in an untrusted directory; pass --respect-workspace-trust false in scripts and CI. ([source](https://docs.devin.ai/cli/reference/commands))
- On a headless box, log in with `devin auth login --force-manual-token-flow`, or copy credentials.toml; the token does not expire by default, so store it as a secret. ([source](https://docs.devin.ai/cli/enterprise/devin-auth))
- --sandbox on Linux needs bubblewrap and socat installed and refuses to start without them (fail-closed). ([source](https://docs.devin.ai/cli/sandbox))
- Background auto-update rewrites the install on macOS/Linux; pin behavior with "auto_update": false in config.json for reproducible images. ([source](https://docs.devin.ai/cli/changelog/stable))
- Agent shell commands inherit the login shell environment (.bashrc/.zshrc), so the server's shell profile affects what the agent sees. ([source](https://docs.devin.ai/cli/changelog/stable))
- Devin CLI does not yet support Knowledge, Playbooks or Secrets from your Devin account; pass secrets via the server environment. ([source](https://docs.devin.ai/cli))
- On legacy Windsurf Enterprise, `devin auth login` can succeed while requests fail with 'CLI access is disabled for this user' if the admin has not enabled CLI access. ([source](https://docs.devin.ai/cli/enterprise/windsurf-auth))
- DEVIN_SESSIONS_DIR can move the session history database, e.g. off an NFS home directory. ([source](https://docs.devin.ai/cli/changelog/stable))
- There's no JSON output for `devin -p`; use `--export <path>` to save the conversation to a file. ([source](https://docs.devin.ai/cli/reference/commands))

## Sources

- <https://cli.devin.ai/install.sh>
- <https://docs.devin.ai/admin/billing/self-serve>
- <https://docs.devin.ai/cli>
- <https://docs.devin.ai/cli/changelog/stable>
- <https://docs.devin.ai/cli/enterprise/devin-auth>
- <https://docs.devin.ai/cli/enterprise/windsurf-auth>
- <https://docs.devin.ai/cli/extensibility/rules>
- <https://docs.devin.ai/cli/models>
- <https://docs.devin.ai/cli/reference/commands>
- <https://docs.devin.ai/cli/reference/configuration/config-file>
- <https://docs.devin.ai/cli/sandbox>
<!-- END GENERATED: agent:devin-cli -->

---

See all agents: [agent comparison](README.md) · [Run any agent in parallel on Northflank](../examples/northflank-parallel-harnesses/README.md) · [Running agents headlessly](../guides/running-agents-headless.md)
