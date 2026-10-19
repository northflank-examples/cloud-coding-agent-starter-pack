# Run AI Coding Agents in the Cloud (2026): Claude Code, Codex, OpenCode, Cursor CLI, Devin CLI, Pi, Gemini CLI, Copilot CLI, Amp, goose, Aider & more

A hands-on starter pack that teaches developers **how to run and manage AI coding agents in the cloud**. Covers 15 terminal coding agents and 12 places to run them:

- **How to run each agent on a server**: install it, log in without a browser, run it headlessly with prompts off, get JSON out, and avoid each agent's cloud-specific gotchas.
- **Where to run them**: Northflank Cloud Harness, Claude Code on the web, Codex cloud, Cursor, Copilot, Codespaces, Ona, Coder, E2B, Daytona, Sprites and Modal, compared on isolation, persistence, session limits, BYOC and cost.
- **How to manage them**: running many in parallel, persistence, secrets, logs, updates and cost.
- **Runnable examples**: one runner script and container for every agent, and a launcher that starts one isolated Northflank harness per task for any agent.

**Agents:** [Claude Code](agents/claude-code.md) · [Codex](agents/codex.md) · [Cursor CLI](agents/cursor-cli.md) · [OpenCode](agents/opencode.md) · [Pi](agents/pi.md) · [OMP](agents/omp.md) · [Devin CLI](agents/devin-cli.md) · [Aider](agents/aider.md) · [Amp](agents/amp.md) · [Crush](agents/crush.md) · [Factory Droid](agents/droid.md) · [Gemini CLI](agents/gemini-cli.md) · [GitHub Copilot CLI](agents/copilot-cli.md) · [goose](agents/goose.md) · [Qwen Code](agents/qwen-code.md)

<!-- BEGIN GENERATED: last-updated -->
**Last verified:** 2026-10-19. Every fact links to the vendor's own docs and is generated from [`data/agents.json`](data/agents.json) and [`data/platforms.json`](data/platforms.json). Anything a vendor doesn't document is marked as such, never guessed.
<!-- END GENERATED: last-updated -->

> **Disclosure:** this repository is maintained by [Northflank](https://northflank.com). Northflank Cloud Harness is one of the platforms compared, and has built-in support for Claude Code, Codex, Cursor, OpenCode, Pi, Devin CLI and OMP. To keep it fair, every agent and platform uses the same [methodology](methodology.md), every value links to its source, and corrections from any vendor or user are welcome via [pull request](CONTRIBUTING.md).

## Contents

- [Pick an agent](#pick-an-agent)
- [Every agent, headless, in one line](#every-agent-headless-in-one-line)
- [Run any agent in the cloud in 5 minutes](#run-any-agent-in-the-cloud-in-5-minutes)
- [Run many agents in parallel](#run-many-agents-in-parallel)
- [Where to run coding agents](#where-to-run-coding-agents)
- [Learn: guides](#learn-guides)
- [FAQ](#faq)
- [Methodology and sources](#methodology-and-sources)

## Pick an agent

Each agent links to a full guide: Northflank, any VM, or a container; install; browserless login; headless runs; gotchas; sources.

<!-- BEGIN GENERATED: agents -->
| Agent | Made by | Licence | Models | Headless command | Auth on a server | On Northflank |
| --- | --- | --- | --- | --- | --- | --- |
| [Claude Code](agents/claude-code.md) | Anthropic | Proprietary | Claude only | `claude -p "<task>"` | `ANTHROPIC_API_KEY`, or `CLAUDE_CODE_OAUTH_TOKEN` for a subscription | [built in](agents/claude-code.md#option-1-run-claude-code-on-northflank-cloud-harness) |
| [Codex CLI](agents/codex.md) | OpenAI | Apache-2.0 (open source) | OpenAI; others via config | `codex exec "<task>"` | `CODEX_API_KEY`, or `codex login --device-auth` for ChatGPT plans | [built in](agents/codex.md#option-1-run-codex-cli-on-northflank-cloud-harness) |
| [Cursor CLI](agents/cursor-cli.md) | Cursor (Anysphere) | Proprietary | Models on your Cursor plan | `agent -p "<task>"` | `CURSOR_API_KEY` | [built in](agents/cursor-cli.md#option-1-run-cursor-cli-on-northflank-cloud-harness) |
| [OpenCode](agents/opencode.md) | Anomaly (formerly SST) | MIT (open source) | 75+ providers, local models | `opencode run "<task>"` | Provider key, e.g. `ANTHROPIC_API_KEY` | [built in](agents/opencode.md#option-1-run-opencode-on-northflank-cloud-harness) |
| [Pi](agents/pi.md) | Earendil Works (by Mario Zechner) | MIT (open source) | 20+ providers, custom endpoints | `pi -p "<task>"` | Provider key, e.g. `ANTHROPIC_API_KEY`, or `/login` | [built in](agents/pi.md#option-1-run-pi-on-northflank-cloud-harness) |
| [OMP](agents/omp.md) | Stencil Labs (by Can Bölük) | MIT (open source) | 60+ providers, local | `omp -p "<task>"` | Provider key, e.g. `ANTHROPIC_API_KEY`, or `omp login <provider>` | [built in](agents/omp.md#option-1-run-omp-on-northflank-cloud-harness) |
| [Devin CLI](agents/devin-cli.md) | Cognition | Proprietary | Models via your Devin plan | `devin -p "<task>"` | `devin auth login --force-manual-token-flow`, or a copied `credentials.toml` | [built in](agents/devin-cli.md#option-1-run-devin-cli-on-northflank-cloud-harness) |
| [Aider](agents/aider.md) | Paul Gauthier and contributors | Apache-2.0 (open source) | Any LiteLLM provider, local | `aider --message "<task>"` | Provider key, e.g. `ANTHROPIC_API_KEY` | [install in an empty sandbox](agents/aider.md#option-1-run-aider-on-northflank-cloud-harness) |
| [Amp](agents/amp.md) | Amp (spun out of Sourcegraph) | Proprietary | Amp-served models; BYO keys | `amp -x "<task>"` | `AMP_API_KEY` | [install in an empty sandbox](agents/amp.md#option-1-run-amp-on-northflank-cloud-harness) |
| [Crush](agents/crush.md) | Charm | FSL-1.1-MIT (source-available) | Many providers, local | `crush run "<task>"` | Provider key, e.g. `ANTHROPIC_API_KEY` | [install in an empty sandbox](agents/crush.md#option-1-run-crush-on-northflank-cloud-harness) |
| [Factory Droid](agents/droid.md) | Factory | Proprietary | Factory models; BYO key | `droid exec "<task>"` | `FACTORY_API_KEY` | [install in an empty sandbox](agents/droid.md#option-1-run-factory-droid-on-northflank-cloud-harness) |
| [Gemini CLI](agents/gemini-cli.md) | Google | Apache-2.0 (open source) | Gemini only | `gemini -p "<task>"` | `GEMINI_API_KEY`, or a Vertex AI service account | [install in an empty sandbox](agents/gemini-cli.md#option-1-run-gemini-cli-on-northflank-cloud-harness) |
| [GitHub Copilot CLI](agents/copilot-cli.md) | GitHub | Proprietary | Copilot models; BYO key | `copilot -p "<task>"` | `COPILOT_GITHUB_TOKEN` (fine-grained PAT), or `copilot login --device-code` | [install in an empty sandbox](agents/copilot-cli.md#option-1-run-github-copilot-cli-on-northflank-cloud-harness) |
| [goose](agents/goose.md) | Agentic AI Foundation (Linux Foundation); created by Block | Apache-2.0 (open source) | 15+ providers, local | `goose run -t "<task>"` | `GOOSE_PROVIDER`, `GOOSE_MODEL` and the provider key | [install in an empty sandbox](agents/goose.md#option-1-run-goose-on-northflank-cloud-harness) |
| [Qwen Code](agents/qwen-code.md) | Alibaba Qwen team | Apache-2.0 (open source) | OpenAI-compatible, Anthropic, Gemini, local | `qwen -p "<task>"` | `OPENAI_API_KEY` and `OPENAI_BASE_URL` (any compatible API) | [install in an empty sandbox](agents/qwen-code.md#option-1-run-qwen-code-on-northflank-cloud-harness) |
<!-- END GENERATED: agents -->

Flags, JSON output, resume, server modes, instruction files, sandboxes and MCP for every agent: [agent comparison](agents/README.md).

## Every agent, headless, in one line

The command that runs one task to completion with no prompts. Run these only inside an isolated environment (a container, VM or Cloud Harness) with one repository and scoped credentials. Why and how: [Running agents headlessly](guides/running-agents-headless.md).

<!-- BEGIN GENERATED: cheatsheet -->
```bash
# Claude Code
claude -p "Fix the failing tests" --permission-mode acceptEdits \
  --allowedTools "Read,Edit,Write,Bash" --output-format json
# Codex CLI
codex exec --sandbox workspace-write "Fix the failing tests"
# Cursor CLI
agent -p --force --trust --output-format text "Fix the failing tests"
# OpenCode
opencode run --auto -m anthropic/claude-sonnet-5-5 "Fix the failing tests"
# Pi
pi -p --model anthropic/claude-sonnet-5-5 "Fix the failing tests"
# OMP
omp -p --yolo --model anthropic/claude-sonnet-5-5 "Fix the failing tests"
# Devin CLI
devin -p "Fix the failing tests" --permission-mode dangerous \
  --respect-workspace-trust false
# Aider
aider --message "Fix the failing tests" --yes-always --no-auto-commits
# Amp
amp -x "Fix the failing tests"
# Crush
crush run -q "Fix the failing tests"
# Factory Droid
droid exec --auto medium "Fix the failing tests"
# Gemini CLI
gemini -p "Fix the failing tests" --approval-mode=yolo
# GitHub Copilot CLI
copilot -p "Fix the failing tests" --allow-all-tools --no-ask-user
# goose
GOOSE_PROVIDER=anthropic GOOSE_MODEL=claude-sonnet-5-5 \
  goose run --no-session -t "Fix the failing tests"
# Qwen Code
qwen -p "Fix the failing tests" --approval-mode yolo
```
<!-- END GENERATED: cheatsheet -->

## Run any agent in the cloud in 5 minutes

**On Northflank Cloud Harness** (walkthrough: [tutorials/northflank-cloud-harness](tutorials/northflank-cloud-harness/README.md)):

1. In [Northflank](https://app.northflank.com), open a project → **Harnesses** → **Create harness**.
2. Choose **Claude Code**, **Codex**, **Cursor**, **OpenCode**, **Pi**, **Devin CLI** or **OMP**, or **Empty sandbox** for any other agent.
3. Pick your repository and branch, choose API key or account sign-in, then click **Create harness**.
4. The terminal opens in an isolated Kata microVM with a persistent workspace and the agent ready. Closing the tab doesn't pause it, and pausing stops compute while keeping the workspace. Connect over SSH or from VS Code/Cursor too. For an empty-sandbox harness, install your agent with [`install-agents.sh`](examples/cloud-agent-runner/install-agents.sh), e.g. `bash install-agents.sh gemini-cli`.

**Anywhere with Docker** (any VM, Kubernetes cluster or container platform):

```bash
cd examples/cloud-agent-runner
docker build --build-arg AGENTS="claude-code opencode goose" -t cloud-agent .
cp .env.example .env   # repo URL, GitHub token, agent keys
docker run --rm --env-file .env cloud-agent run-task.sh opencode "Add tests for parseDate()"
```

**On a plain VM:** `bash examples/cloud-agent-runner/bootstrap-vm.sh claude-code codex pi`, then follow the agent's guide.

## Run many agents in parallel

Give every task its own isolated environment and its own branch, run them all at once, and review each result as a pull request. With Northflank, [`launch.sh`](examples/northflank-parallel-harnesses/README.md) turns a task list into one harness per task, for any agent:

```bash
export NF_API_TOKEN=... NF_PROJECT=my-project REPO_URL=https://github.com/your-org/your-repo
AGENT=claude-code AGENT_API_KEY=$ANTHROPIC_API_KEY ./launch.sh tasks.txt   # built-in harness type
AGENT=opencode    AGENT_ENV="ANTHROPIC_API_KEY"   ./launch.sh tasks.txt   # built-in, provider key passed in
AGENT=gemini-cli  AGENT_ENV="GEMINI_API_KEY"      ./launch.sh tasks.txt   # empty-sandbox harness + installer
./manage.sh pause --all                                                    # stop compute, keep workspaces
```

Running the same task through several agents is the quickest way to find out which one works best on your codebase. See [Running many agents in parallel](guides/parallel-agents.md).

## Where to run coding agents

### Platforms at a glance

There are four kinds of places you can run a coding agent in the cloud:

- **Managed agent harnesses** give you an isolated workspace for *any* agent CLI.
- **Vendor-hosted agents** run *their own* agent in *their* cloud.
- **Cloud dev environments** are remote workstations built for humans, which can also host agents.
- **Sandbox platforms** are SDK-driven isolated machines that you assemble into an agent environment yourself.

<!-- BEGIN GENERATED: overview -->
| Platform | Type | Coding agents | Run any agent CLI? | Isolation | Persistent workspace | SSH access | Run in your own cloud | Price (2 vCPU / 4 GiB) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| [Northflank Cloud Harness](platforms/northflank.md) | Managed agent harness | Claude Code, Codex, Cursor, OpenCode, Pi, Devin CLI, OMP; any other agent in an empty sandbox | yes | Kata microVM per harness | Yes: persistent workspace volume, 5–100 GiB (on by default) | yes | Yes, self-serve: AWS, AWS European Sovereign Cloud, GCP, Azure, Oracle, Civo, CoreWeave, Nebius; or import your own Kubernetes cluster (BYOK) | $0.0667/hr |
| [Claude Code on the web](platforms/claude-code-web.md) | Vendor-hosted agent | Claude Code only | no | Isolated VM per session | Setup snapshot cached ~7 days; session files kept while paused | no | Self-hosted runners, public beta (Team/Enterprise) | Included in Claude plans (Pro $20/mo and up) |
| [Cursor Cloud Agents](platforms/cursor-cloud-agents.md) | Vendor-hosted agent | Cursor agent only | no | Firecracker microVM per agent | Environment snapshots kept 30 days of inactivity | no | Self-hosted machines for tool execution (pools on Enterprise) | Cursor Premium ($30/mo) or higher + model usage at API rates |
| [GitHub Copilot cloud agent](platforms/copilot-cloud-agent.md) | Vendor-hosted agent | Copilot; Claude and Codex agents (preview) | no | Ephemeral GitHub Actions runner | No (ephemeral); pushed commits kept | no | Self-hosted Actions runners (firewall must be disabled) | Copilot plan + Actions minutes + AI credits |
| [OpenAI Codex cloud](platforms/codex-cloud.md) | Vendor-hosted agent | Codex only | no | Isolated VM workspace per task | Task state recoverable up to 7 days | no | not published | Included in ChatGPT plans (Plus $20/mo and up) |
| [Coder](platforms/coder.md) | Cloud dev environment | Claude Code, Codex, any terminal agent; Coder Agents | yes | Whatever your template provisions | Defined by template | yes | Self-hosted only | Free (open source) or per-user licence, plus your cloud |
| [GitHub Codespaces](platforms/github-codespaces.md) | Cloud dev environment | Any CLI agent you install (devcontainer) | yes | Container on a dedicated VM | Yes; stopped codespaces deleted after 30 days inactive | yes | No | $0.1800/hr (billed as 2 vCPU / RAM not published) |
| [Ona (formerly Gitpod)](platforms/ona.md) | Cloud dev environment | Codex agent built in; Claude Code etc. inside environments | yes | VM per environment | Yes; archived after 3 days stopped (Core) | yes | Enterprise: runners in your AWS or GCP | Enterprise via sales (credits) |
| [Daytona](platforms/daytona.md) | Sandbox platform | Claude Code, Codex, OpenCode preinstalled; any agent | yes | Container by default; optional VM | Yes by default; archived after 7 days stopped | yes | Bring your own compute (custom regions) | $0.1656/hr |
| [E2B](platforms/e2b.md) | Sandbox platform | Templates: Claude Code, Codex, Amp, OpenCode; any agent | yes | Firecracker microVM | Opt-in pause/resume; paused kept indefinitely | yes | Enterprise only (AWS, GCP, Azure) | $0.1656/hr |
| [Modal Sandboxes](platforms/modal.md) | Sandbox platform | Any agent you install; official Claude Code and OpenCode examples | yes | gVisor or VM runtime (Modal picks if unset) | Volumes; filesystem snapshots (30-day default TTL) | not published | No (not published) | $0.2380/hr |
| [Sprites (Fly.io)](platforms/sprites.md) | Sandbox platform | Claude Code, Codex, Gemini CLI, Cursor preinstalled; any agent | yes | Hardware-isolated VM | Yes: disk persists; checkpoints | no | No | $0.1067/hr at 25% CPU busy |
<!-- END GENERATED: overview -->

Full feature tables: [comparisons/feature-matrix.md](comparisons/feature-matrix.md).

### Cost by workload

Four standard coding-agent workloads, priced on every platform that sells compute by the hour. Totals are **compute plus persistent workspace storage, at list price**. They exclude free credits, plan fees, egress and model/token usage (which is the same wherever the agent runs).

<!-- BEGIN GENERATED: scenarios -->
| Platform | [1 dev, workdays](scenarios/solo-developer.md) | [10 agents × 1 h](scenarios/parallel-agents.md) | [100 tasks × 30 min](scenarios/batch-tasks.md) | [10 × 24/7 (month)](scenarios/team-always-on.md) |
| --- | --- | --- | --- | --- |
| [Northflank Cloud Harness](platforms/northflank.md) | $14.73 | $0.67 | $3.33 | $516.62 |
| [Sprites (Fly.io)](platforms/sprites.md) | $21.59 | $1.07 | $5.34 | $798.62 |
| [E2B](platforms/e2b.md) | $29.15 | $1.66 | $8.28 | $1,208.88 |
| [Daytona](platforms/daytona.md) | $30.33 | $1.66 | $8.28 | $1,220.71 |
| [GitHub Codespaces](platforms/github-codespaces.md) | $33.08 | $1.80 | $9.00 | $1,328.00 |
| [Modal Sandboxes](platforms/modal.md) | $41.88 | $2.38 | $11.90 | $1,737.11 |

- **1 dev, workdays**: one developer's persistent agent workspace (2 vCPU, 4 GiB, 20 GB), running 8 h × 22 working days (176 h) and paused the rest of the month.
- **10 agents × 1 h**: 10 coding agents working in parallel for one hour on separate tasks (2 vCPU, 4 GiB each), discarded afterwards.
- **100 tasks × 30 min**: 100 short agent tasks such as dependency bumps or lint fixes (2 vCPU, 4 GiB), 30 minutes each, ephemeral.
- **10 × 24/7 (month)**: 10 always-on agent workspaces for a team (2 vCPU, 4 GiB, 20 GB each), running 24/7 for a 730-hour month.
<!-- END GENERATED: scenarios -->

Platforms that include compute in a subscription, or that are self-hosted, can't be priced per hour:

<!-- BEGIN GENERATED: subscription -->
| Platform | Pricing model | What you pay |
| --- | --- | --- |
| [Claude Code on the web](platforms/claude-code-web.md) | included in a subscription | Included in Claude Pro ($20/mo), Max (from $100/mo), Team and Enterprise; counts toward plan usage limits |
| [Cursor Cloud Agents](platforms/cursor-cloud-agents.md) | included in a subscription | Cursor Premium ($30/mo), Super ($100/mo), Ultra ($200/mo), Teams or Enterprise; Free and Plus don't include cloud agents; model usage billed at API pricing; infrastructure included |
| [GitHub Copilot cloud agent](platforms/copilot-cloud-agent.md) | usage-based credits | Copilot plan (Pro $10/mo to Enterprise $39/seat/mo) plus GitHub Actions minutes and AI credits per session |
| [OpenAI Codex cloud](platforms/codex-cloud.md) | included in a subscription | Included in ChatGPT Plus ($20/mo), Pro ($100–$500/mo), Business and Enterprise; shares the plan's Codex allowance; not available with API keys |
| [Coder](platforms/coder.md) | self-hosted licence + your cloud | Community edition free (AGPL); Premium per-user licence (price not published); compute is your own cloud bill |
| [Ona (formerly Gitpod)](platforms/ona.md) | usage-based credits | Enterprise via sales, billed in credits; legacy Core plan billed in OCUs (price per OCU not published); new signups closed |
<!-- END GENERATED: subscription -->

**Key takeaways (for these assumptions):**

- **Northflank has the lowest list price per environment-hour** in this comparison: $0.0667/hr for 2 vCPU / 4 GiB, about 2.5× cheaper than E2B or Daytona ($0.1656/hr) GitHub Codespaces' 2-core machine ($0.18/hr) and Modal's Sandbox rates ($0.238/hr). It is the cheapest option in all four scenarios.
- **Session limits matter as much as price for long-running agents.** Copilot's cloud agent stops at 59 minutes, Codespaces at 12 hours, and E2B and Modal at 24 hours of continuous runtime (E2B Pro; 1 hour on E2B Hobby). Northflank, Daytona, Sprites, Ona and Coder publish no maximum session length.
- **Vendor-hosted agents lock you to one agent.** Claude Code on the web runs only Claude Code, Codex cloud runs only Codex, and Cursor runs only Cursor's agent. Northflank, Codespaces, Coder, E2B, Daytona, Sprites and Modal let you run any agent CLI, and more than one, side by side.
- **Usage-billed platforms change the order for mostly idle agents.** Sprites bills only the CPU actually used and pauses after about 30 s idle, so an agent that mostly waits can cost less than the totals shown. See [pricing](comparisons/pricing.md).
- **The model bill is usually larger than the infrastructure bill.** A 2 vCPU environment for a full working month costs $12–$32 on the metered platforms here. Agent token usage for the same month is often more. See [cost optimization](guides/cost-optimization.md).

### Which platform should I use?

| If you want… | Consider |
| --- | --- |
| Isolated cloud workspaces for **any coding agent** (Claude Code, Codex, Cursor, OpenCode, Pi, Devin CLI and OMP built in), with SSH/IDE access, no session limit, and the option to run in your own AWS/GCP/Azure account | [Northflank Cloud Harness](platforms/northflank.md) |
| The **zero-setup** experience for one vendor's agent, paid through a subscription you already have | [Claude Code on the web](platforms/claude-code-web.md), [Codex cloud](platforms/codex-cloud.md), [Cursor Cloud Agents](platforms/cursor-cloud-agents.md) |
| Agents triggered **from GitHub issues**, with short tasks under an hour | [GitHub Copilot cloud agent](platforms/copilot-cloud-agent.md) |
| A **human dev environment** that can also host an agent, on GitHub | [GitHub Codespaces](platforms/github-codespaces.md) |
| **Self-hosted** workspaces on infrastructure you operate | [Coder](platforms/coder.md), or Northflank BYOC (managed control plane, your cloud) |
| To **build your own agent product** on SDK-driven sandboxes | [E2B](platforms/e2b.md), [Daytona](platforms/daytona.md), [Sprites](platforms/sprites.md), [Modal](platforms/modal.md), or [Northflank Sandboxes](https://northflank.com/docs/v1/application/sandboxes/sandboxes-on-northflank-cloud) |

### Estimate your own workload

**In the browser:** the [Agent Sandbox Pricing estimator](https://p01--sandbox-pricing-estimator--wdgpv6bn4jz8.code.run/) prices your workload (how many environments, how many at once, runtime, vCPU, RAM, disk) across eight sandbox providers at list price: Northflank, E2B, Daytona, Modal, Vercel Sandbox, Cloudflare Sandbox, Runloop and Sprites. It's built from Northflank's sibling repo, [agent-sandbox-pricing](https://github.com/northflank-examples/agent-sandbox-pricing), which uses the same sourcing rules as this one.

**From the command line**, for the 12 platforms in this repo, with no dependencies beyond Python 3.9+:

```bash
git clone https://github.com/northflank-examples/cloud-coding-agent-starter-pack.git
cd cloud-coding-agent-starter-pack
python3 scripts/estimate.py --environments 5 --hours 176 --vcpu 2 --memory 4 --disk 20 --months 1
```

It prints the billed size, per-hour price, compute, storage and total for every metered platform, and summarises the subscription-priced ones.

## Learn: guides

| Guide | Question it answers |
| --- | --- |
| [Getting started](guides/getting-started.md) | How do I go from zero to an agent working on my repo in the cloud? |
| [Running agents headlessly](guides/running-agents-headless.md) | How do I run an agent with no browser and no prompts, and get results out? |
| [Running many agents in parallel](guides/parallel-agents.md) | How do I run ten tasks, or ten agents, at once without conflicts? |
| [Managing agents in the cloud](guides/managing-agents.md) | Lifecycle, versions, logs, cost and access once agents run remotely |
| [One repository, many agents](guides/agent-instructions-files.md) | `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`: how do I give every agent the same instructions? |
| [Cloud vs local](guides/cloud-vs-local.md) | When is it worth moving my agent off my laptop? |
| [Persistent vs ephemeral](guides/persistent-vs-ephemeral.md) | Should the workspace survive between tasks? |
| [Security and secrets](guides/security-and-secrets.md) | How do I give an agent repo and API access without over-granting? |
| [Cost optimization](guides/cost-optimization.md) | What drives the bill, and how do I cut it? |

## FAQ

<!-- BEGIN GENERATED: faq-agents -->
### How do I run Claude Code in the cloud?

Install it with `curl -fsSL https://claude.ai/install.sh | bash`, authenticate with `ANTHROPIC_API_KEY`, or `CLAUDE_CODE_OAUTH_TOKEN` for a subscription, then run a task headlessly with no prompts:

```bash
claude -p "Fix the failing tests" --permission-mode acceptEdits \
  --allowedTools "Read,Edit,Write,Bash" --output-format json
```

On Northflank Cloud Harness, choose **Claude Code** when you create a harness and it's preinstalled. Full guide: [Claude Code in the cloud](agents/claude-code.md).

### How do I run Codex CLI in the cloud?

Install it with `npm install -g @openai/codex`, authenticate with `CODEX_API_KEY`, or `codex login --device-auth` for ChatGPT plans, then run a task headlessly with no prompts:

```bash
codex exec --sandbox workspace-write "Fix the failing tests"
```

On Northflank Cloud Harness, choose **Codex** when you create a harness and it's preinstalled. Full guide: [Codex CLI in the cloud](agents/codex.md).

### How do I run Cursor CLI in the cloud?

Install it with `curl https://cursor.com/install -fsS | bash`, authenticate with `CURSOR_API_KEY`, then run a task headlessly with no prompts:

```bash
agent -p --force --trust --output-format text "Fix the failing tests"
```

On Northflank Cloud Harness, choose **Cursor** when you create a harness and it's preinstalled. Full guide: [Cursor CLI in the cloud](agents/cursor-cli.md).

### How do I run OpenCode in the cloud?

Install it with `curl -fsSL https://opencode.ai/install | bash`, authenticate with Provider key, e.g. `ANTHROPIC_API_KEY`, then run a task headlessly with no prompts:

```bash
opencode run --auto -m anthropic/claude-sonnet-5-5 "Fix the failing tests"
```

On Northflank Cloud Harness, choose **OpenCode** when you create a harness and it's preinstalled. Full guide: [OpenCode in the cloud](agents/opencode.md).

### How do I run Pi in the cloud?

Install it with `curl -fsSL https://pi.dev/install.sh | sh`, authenticate with Provider key, e.g. `ANTHROPIC_API_KEY`, or `/login`, then run a task headlessly with no prompts:

```bash
pi -p --model anthropic/claude-sonnet-5-5 "Fix the failing tests"
```

On Northflank Cloud Harness, choose **Pi** when you create a harness and it's preinstalled. Full guide: [Pi in the cloud](agents/pi.md).

### How do I run OMP in the cloud?

Install it with `curl -fsSL https://omp.sh/install | sh`, authenticate with Provider key, e.g. `ANTHROPIC_API_KEY`, or `omp login <provider>`, then run a task headlessly with no prompts:

```bash
omp -p --yolo --model anthropic/claude-sonnet-5-5 "Fix the failing tests"
```

On Northflank Cloud Harness, choose **OMP** when you create a harness and it's preinstalled. Full guide: [OMP in the cloud](agents/omp.md).

### How do I run Devin CLI in the cloud?

Install it with `curl -fsSL https://cli.devin.ai/install.sh | bash`, authenticate with `devin auth login --force-manual-token-flow`, or a copied `credentials.toml`, then run a task headlessly with no prompts:

```bash
devin -p "Fix the failing tests" --permission-mode dangerous \
  --respect-workspace-trust false
```

On Northflank Cloud Harness, choose **Devin CLI** when you create a harness and it's preinstalled. Full guide: [Devin CLI in the cloud](agents/devin-cli.md).

### How do I run Aider in the cloud?

Install it with `curl -LsSf https://aider.chat/install.sh | sh`, authenticate with Provider key, e.g. `ANTHROPIC_API_KEY`, then run a task headlessly with no prompts:

```bash
aider --message "Fix the failing tests" --yes-always --no-auto-commits
```

On Northflank Cloud Harness, create an **Empty sandbox** harness and install it with `install-agents.sh aider`. Full guide: [Aider in the cloud](agents/aider.md).

### How do I run Amp in the cloud?

Install it with `curl -fsSL https://ampcode.com/install.sh | bash`, authenticate with `AMP_API_KEY`, then run a task headlessly with no prompts:

```bash
amp -x "Fix the failing tests"
```

On Northflank Cloud Harness, create an **Empty sandbox** harness and install it with `install-agents.sh amp`. Full guide: [Amp in the cloud](agents/amp.md).

### How do I run Crush in the cloud?

Install it with `npm install -g @charmland/crush`, authenticate with Provider key, e.g. `ANTHROPIC_API_KEY`, then run a task headlessly with no prompts:

```bash
crush run -q "Fix the failing tests"
```

On Northflank Cloud Harness, create an **Empty sandbox** harness and install it with `install-agents.sh crush`. Full guide: [Crush in the cloud](agents/crush.md).

### How do I run Factory Droid in the cloud?

Install it with `npm install -g droid`, authenticate with `FACTORY_API_KEY`, then run a task headlessly with no prompts:

```bash
droid exec --auto medium "Fix the failing tests"
```

On Northflank Cloud Harness, create an **Empty sandbox** harness and install it with `install-agents.sh droid`. Full guide: [Factory Droid in the cloud](agents/droid.md).

### How do I run Gemini CLI in the cloud?

Install it with `npm install -g @google/gemini-cli`, authenticate with `GEMINI_API_KEY`, or a Vertex AI service account, then run a task headlessly with no prompts:

```bash
gemini -p "Fix the failing tests" --approval-mode=yolo
```

On Northflank Cloud Harness, create an **Empty sandbox** harness and install it with `install-agents.sh gemini-cli`. Full guide: [Gemini CLI in the cloud](agents/gemini-cli.md).

### How do I run GitHub Copilot CLI in the cloud?

Install it with `curl -fsSL https://gh.io/copilot-install | bash`, authenticate with `COPILOT_GITHUB_TOKEN` (fine-grained PAT), or `copilot login --device-code`, then run a task headlessly with no prompts:

```bash
copilot -p "Fix the failing tests" --allow-all-tools --no-ask-user
```

On Northflank Cloud Harness, create an **Empty sandbox** harness and install it with `install-agents.sh copilot-cli`. Full guide: [GitHub Copilot CLI in the cloud](agents/copilot-cli.md).

### How do I run goose in the cloud?

Install it with `curl -fsSL https://github.com/aaif-goose/goose/releases/download/stable/download_cli.sh | CONFIGURE=false bash`, authenticate with `GOOSE_PROVIDER`, `GOOSE_MODEL` and the provider key, then run a task headlessly with no prompts:

```bash
GOOSE_PROVIDER=anthropic GOOSE_MODEL=claude-sonnet-5-5 \
  goose run --no-session -t "Fix the failing tests"
```

On Northflank Cloud Harness, create an **Empty sandbox** harness and install it with `install-agents.sh goose`. Full guide: [goose in the cloud](agents/goose.md).

### How do I run Qwen Code in the cloud?

Install it with `npm install -g @qwen-code/qwen-code@latest`, authenticate with `OPENAI_API_KEY` and `OPENAI_BASE_URL` (any compatible API), then run a task headlessly with no prompts:

```bash
qwen -p "Fix the failing tests" --approval-mode yolo
```

On Northflank Cloud Harness, create an **Empty sandbox** harness and install it with `install-agents.sh qwen-code`. Full guide: [Qwen Code in the cloud](agents/qwen-code.md).
<!-- END GENERATED: faq-agents -->

### Which coding agents are open source?

Codex, OpenCode, Pi, OMP, Aider, Gemini CLI, goose and Qwen Code are open source (Apache-2.0 or MIT). Crush is source-available under FSL-1.1-MIT, which converts to MIT later. Claude Code, Cursor CLI, Devin CLI, GitHub Copilot CLI, Amp and Factory Droid are proprietary. Licences are linked from each [agent guide](agents/README.md).

### Which coding agents work with any model provider?

OpenCode, Pi, OMP, goose, Crush, Aider and Qwen Code work with Anthropic, OpenAI, Google, OpenRouter and local models, and you pay the provider directly. Claude Code uses Claude models only (including through Bedrock and Vertex AI), Gemini CLI uses Gemini only, and Codex defaults to OpenAI with other providers configurable. Cursor CLI, Devin CLI, Copilot CLI, Amp and Factory Droid serve models through their own plans.

### Which agents don't ask for permission at all?

Pi has no permission system, OMP defaults to its `yolo` approval mode, Amp runs tools without asking by default, goose defaults to `GOOSE_MODE=auto`, and Crush's `crush run` approves every request for its session. They're convenient for automation, but the environment has to be the security boundary. See [Running agents headlessly](guides/running-agents-headless.md#approving-actions-up-front).

### Can I run different coding agents side by side?

Yes. Give each its own isolated environment: one Northflank harness per agent (built-in types for Claude Code, Codex, Cursor, OpenCode, Pi, Devin CLI and OMP, empty-sandbox harnesses for the rest), one container per agent with [the runner image](examples/cloud-agent-runner/README.md), or any platform that runs arbitrary CLIs (Codespaces, Coder, E2B, Daytona, Sprites, Modal). Vendor-hosted products run only their own agent; Copilot's cloud agent offers Claude and Codex as partner agents in preview.

### What is the cheapest way to run coding agents in the cloud?

For per-hour compute, **Northflank** has the lowest list price in this comparison:

<!-- BEGIN GENERATED: answer:cheapest-hour -->
- Northflank Cloud Harness: $0.0667/hr
- Sprites (Fly.io): $0.1067/hr
- Daytona: $0.1656/hr
- E2B: $0.1656/hr
- GitHub Codespaces: $0.1800/hr
- Modal Sandboxes: $0.2380/hr
<!-- END GENERATED: answer:cheapest-hour -->

Subscription products (Claude Code on the web, Codex cloud) don't charge separately for the VM, but they count toward your plan's usage limits and run only their own agent.

### How much does it cost to run 10 coding agents in parallel?

Ten 2 vCPU / 4 GiB environments for one hour cost, in compute:

<!-- BEGIN GENERATED: answer:scenario-parallel-agents -->
- Northflank Cloud Harness: $0.67
- Sprites (Fly.io): $1.07
- Daytona: $1.66
- E2B: $1.66
- GitHub Codespaces: $1.80
- Modal Sandboxes: $2.38
<!-- END GENERATED: answer:scenario-parallel-agents -->

Model usage is extra and the same on every platform. Details: [scenarios/parallel-agents.md](scenarios/parallel-agents.md).

### Which platforms let a coding agent run for hours or days?

Northflank, Daytona, Sprites, Ona and Coder publish no maximum session length. GitHub Codespaces stops at 12 hours. E2B limits continuous runtime to 1 hour on Hobby and 24 hours on Pro, though pausing resets the clock. Modal Sandboxes default to 5 minutes and run for at most 24 hours; Modal documents snapshotting into a new sandbox to continue. Copilot's cloud agent has a hard 59-minute limit per session. Claude Code on the web, Codex cloud and Cursor don't publish a maximum.

### Can I run cloud coding agents in my own AWS, GCP or Azure account?

- **Northflank:** self-serve BYOC into AWS (including the AWS European Sovereign Cloud), GCP, Azure, Oracle, Civo, CoreWeave or Nebius, or import an existing Kubernetes cluster (BYOK), all managed from Northflank's control plane.
- **Coder:** fully self-hosted.
- **Ona:** Enterprise runners in AWS or GCP.
- **E2B:** BYOC on Enterprise only.
- **Daytona:** bring your own compute.
- **Claude Code on the web:** self-hosted runners in public beta for Team and Enterprise.
- **Cursor and Copilot:** self-hosted machines or runners.

Codespaces and Sprites don't offer BYOC, and Codex cloud and Modal don't publish an option.

### Do cloud coding agents need GPUs?

No. Coding agents call hosted models over HTTPS (unless you point an open-source agent at a local model). The environment only runs the agent CLI, git and your project's build and test tools. 2 vCPU / 4 GiB is a common starting size, and Claude Code's documented minimum is 4 GB RAM.

### Are cloud coding agents more secure than running them locally?

Only if the environment gives the agent less access than your laptop does. That means isolation (microVM or VM per agent), credentials scoped to one repo, egress limits, and changes arriving as pull requests. See [security and secrets](guides/security-and-secrets.md) and the isolation column in the [feature matrix](comparisons/feature-matrix.md).

### What's the difference between a coding agent and an agent harness?

The **agent** (Claude Code, Codex, OpenCode, Pi...) decides what to do. The **harness** is the environment it runs in: compute, filesystem, shell, repository checkout, credentials, network rules and persistence. Managed harnesses like Northflank Cloud Harness provide that environment for any agent. Vendor-hosted products bundle one agent with their own environment.

## Methodology and sources

- Values come only from **official vendor sources**: docs, official repositories and package registries, linked from each [agent guide](agents/README.md) and [platform page](platforms/). Anything not documented is marked as such, never assumed.
- Agent flags were checked against each vendor's current CLI reference on the date shown. Agent CLIs change often, so each guide lists its open questions.
- Platform prices are **list prices** for the default/US region, normalised to a 2 vCPU / 4 GiB environment. [`scripts/validate.py`](scripts/validate.py) checks the cost model against vendor-published prices.
- CI fails if any generated table, agent guide or script block is out of date with the data. Details in [methodology.md](methodology.md).

## Repository layout

```
README.md                         ← you are here
agents/                           one guide per coding agent + comparison (README.md)
guides/                           headless runs, parallel agents, management, security, cost
tutorials/northflank-cloud-harness/   any agent on Northflank in 5 minutes
examples/
  cloud-agent-runner/             install-agents.sh, run-task.sh, Dockerfile: any agent, any machine
  northflank-parallel-harnesses/  one harness + branch per task, for any agent, via the API
platforms/                        one page per place to run agents (features, pricing, sources)
comparisons/                      platform feature matrix and pricing
scenarios/                        four standard coding-agent workloads, priced
data/agents.json                  source of truth for agents
data/platforms.json               source of truth for platforms
scripts/                          generate.py · validate.py · estimate.py
methodology.md                    how values are collected and checked
```

## Contributing

An agent changed a flag, or a platform changed a price? Edit `data/agents.json` or `data/platforms.json`, run `python3 scripts/generate.py`, and open a PR with a link to the official source. Want another agent covered? See [CONTRIBUTING.md](CONTRIBUTING.md). Vendors are welcome to correct their own listings.

## License

Content is licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/): reuse it freely with attribution. Scripts and examples are MIT. Prices and features belong to the respective vendors and change often, so always confirm on the official page.
