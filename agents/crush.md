# How to run Crush in the cloud

Charm's terminal coding agent. This guide covers running Crush on a remote machine instead of your laptop: on Northflank Cloud Harness, on any Linux VM, or in a container. It shows how to install it, log in without a browser, run tasks headlessly with permission prompts off, and what to watch for. Every fact below is quoted from or linked to the vendor's own documentation.

<!-- BEGIN GENERATED: agent:crush -->
Last verified: **2026-10-19** · Docs: <https://github.com/charmbracelet/crush#readme> · Source: <https://github.com/charmbracelet/crush>

## At a glance

|  |  |
| --- | --- |
| Made by | Charm |
| Licence | FSL-1.1-MIT (source-available) |
| Models | Anthropic, OpenAI, Gemini, OpenRouter, Bedrock, Vertex, Azure, Groq, Charm Hyper, local models and any OpenAI- or Anthropic-compatible API |
| Headless command | `crush run "<task>"` |
| Skip permission prompts | `crush run` approves every action on its own; `--yolo` exists only for the interactive UI |
| JSON output | not documented |
| Resume a session | `crush run --continue` / `--session <id>` |
| Choose a model | `-m provider/model` |
| Auth on a server | Provider key, e.g. `ANTHROPIC_API_KEY` |
| Instructions file | `AGENTS.md`, `CRUSH.md`, `CLAUDE.md` |
| Config and credentials | `crushrc` (project or `~/.config/crush/`); state in `~/.local/share/crush/` |
| Built-in sandbox | None; permission rules only |
| MCP | Yes: stdio, HTTP and SSE |
| Server / API mode | `crush server` |
| Northflank Cloud Harness | install in an empty sandbox |
| Billing | Free with your own provider keys; optional Charm Hyper subscription |

## Option 1: Run Crush on Northflank Cloud Harness

Cloud Harness doesn't preinstall Crush, but its **Empty sandbox** option gives you the same isolated microVM, persistent workspace, terminal and SSH access with no agent set up. Install Crush once and it stays installed across pauses:

1. **Harnesses** → **Create harness** → choose **Empty sandbox**, select your repository, and create it.
2. Under **Environment**, add the agent's credentials (Provider key, e.g. `ANTHROPIC_API_KEY`) as runtime variables, then click **Update & restart**.
3. In the harness terminal, run the install command from [step 1 below](#1-install), then run Crush as in [step 3](#3-run-a-task-headlessly).

Install into the home directory (the persistent volume) rather than system directories, so the agent survives restarts. [`install-agents.sh`](../examples/cloud-agent-runner/install-agents.sh) does this for you: `bash install-agents.sh crush`.

To start one empty-sandbox harness per task from a script, with the installer and the task already in the workspace, use [`launch.sh`](../examples/northflank-parallel-harnesses/README.md):

```bash
AGENT=crush AGENT_ENV="ANTHROPIC_API_KEY" NF_PROJECT=my-project \
REPO_URL=https://github.com/your-org/your-repo \
  ./launch.sh tasks.txt
```

Pause the harness when you're done: compute stops and the workspace is kept. See the [Cloud Harness tutorial](../tutorials/northflank-cloud-harness/README.md).

## Option 2: Run Crush on any Linux VM or container

### 1. Install

**npm**:

```bash
npm install -g @charmland/crush
```

**Go**:

```bash
go install github.com/charmbracelet/crush@latest
```

Check it worked: `crush --version`. Install docs: <https://github.com/charmbracelet/crush>.

### 2. Authenticate without a browser

Cloud machines usually can't open a browser login, so use one of these:

| Method | Environment variables | How |
| --- | --- | --- |
| API key env var | `ANTHROPIC_API_KEY`, `OPENAI_API_KEY`, `GEMINI_API_KEY`, `OPENROUTER_API_KEY`, `HYPER_API_KEY`, `GROQ_API_KEY`, `VERCEL_API_KEY`, `OPENCODE_API_KEY`, `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_REGION`, `AZURE_OPENAI_API_KEY`, `VERTEXAI_PROJECT`, `VERTEXAI_LOCATION`, `AWS_PROFILE`, `AWS_BEARER_TOKEN_BEDROCK`, `HF_TOKEN` | Export the provider's env var before running crush/crush run; no browser needed. ([source](https://github.com/charmbracelet/crush)) |
| crushrc provider definition | — | Define a provider in ~/.config/crush/crushrc with `provider add <id> --type ... --base-url ... --api-key "$(...)"` (Bash-based config). ([source](https://github.com/charmbracelet/crush)) |
| subscription / platform login | — | `crush login [hyper\|copilot\|openai\|grok]`. Whether these flows work without a local browser is not documented. ([source](https://github.com/charmbracelet/crush/blob/main/internal/cmd/login.go)) |

### 3. Run a task headlessly

Work on a branch, let the agent finish without prompts, then commit and push for review:

```bash
git switch -c agent/my-task
crush run -q "Fix the failing tests"
git add -A && git commit -m "agent: my task" && git push -u origin HEAD
```

| Part | What it does |
| --- | --- |
| `run` | Run one prompt non-interactively. It approves every permission request for that run |
| `-q` | Hide the spinner, so output is clean in logs |

- **Headless mode:** Runs a single prompt non-interactively and exits; output goes to stdout (redirectable). -q/--quiet hides the spinner, -v/--verbose shows logs. Fails with 'no providers configured' if no provider is set up. Documented in CLI help/source, not in the README. Docs: "Run a single prompt in non-interactive mode and exit." ([source](https://github.com/charmbracelet/crush/blob/main/internal/cmd/run.go))

- **Permissions:** Per source code, RunNonInteractive calls AutoApproveSession for the run's session. --yolo is defined on the root command only (rootCmd.Flags, not persistent), so it is not a documented `crush run` flag. Tools can be hidden entirely with `permissions deny bash ...`. Docs: "// Automatically approve all permission requests for this non-interactive
	// session.
	app.Permissions.AutoApproveSession(sess.ID)" ([source](https://github.com/charmbracelet/crush/blob/main/internal/app/app.go))

### 4. Or use this repo's container

[`examples/cloud-agent-runner`](../examples/cloud-agent-runner/README.md) builds an image with Crush (and any other agents you list) and runs one task per container:

```bash
cd examples/cloud-agent-runner
docker build --build-arg AGENTS="crush" -t cloud-agent .
docker run --rm --env-file .env cloud-agent run-task.sh crush "Fix the failing tests"
```

## Gotchas when running in the cloud

- crush run errors with 'no providers configured - please run 'crush' to set up a provider interactively' when nothing is configured; set a provider env var or crushrc first. ([source](https://github.com/charmbracelet/crush/blob/main/internal/cmd/run.go))
- crushrc runs as full Bash and $(...) in crush.json executes at load time; don't run Crush in a cloned repo whose .crushrc you haven't reviewed. ([source](https://github.com/charmbracelet/crush))
- License is FSL-1.1-MIT (source-available, not OSI open source until the MIT conversion). ([source](https://github.com/charmbracelet/crush/blob/main/LICENSE.md))
- Pseudonymous usage metrics are on by default; disable with CRUSH_DISABLE_METRICS=1 or DO_NOT_TRACK=1. ([source](https://github.com/charmbracelet/crush))
- Provider list auto-updates from Catwalk; disable with CRUSH_DISABLE_PROVIDER_AUTO_UPDATE=1 for offline/air-gapped containers. ([source](https://github.com/charmbracelet/crush))
- With a shared `crush serve` backend, --yolo is first-wins per workspace. ([source](https://github.com/charmbracelet/crush))

## Not documented / open questions

- `crush run` flags and its auto-approval behaviour are only documented in source/--help, not the README; re-verify with `crush run --help` on the pinned version.
- No JSON / machine-readable output flag found for `crush run`.
- Whether `crush login` (hyper/copilot/openai/grok) works without a browser on a headless server is not documented.
- Exact file where API keys entered via the TUI/`crush login` are stored (likely the global data config ~/.local/share/crush/crush.json) is not explicitly documented.
- README calls it `crush serve` in one place while the command defined in source is `crush server`.

## Sources

- <https://github.com/charmbracelet/crush>
- <https://github.com/charmbracelet/crush/blob/main/LICENSE.md>
- <https://github.com/charmbracelet/crush/blob/main/internal/app/app.go>
- <https://github.com/charmbracelet/crush/blob/main/internal/cmd/login.go>
- <https://github.com/charmbracelet/crush/blob/main/internal/cmd/run.go>
<!-- END GENERATED: agent:crush -->

---

See all agents: [agent comparison](README.md) · [Run any agent in parallel on Northflank](../examples/northflank-parallel-harnesses/README.md) · [Running agents headlessly](../guides/running-agents-headless.md)
