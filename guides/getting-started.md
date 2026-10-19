# Getting started: run your first AI coding agent in the cloud

This guide takes you from nothing to a coding agent working on your repository in a cloud environment, in five steps. It applies to any agent (Claude Code, Codex, Cursor CLI, OpenCode, Pi, Devin CLI, Gemini CLI, Copilot CLI, Amp, goose, Aider and others) and any infrastructure. For copy-paste walkthroughs of a specific agent, see its [agent guide](../agents/README.md).

**You'll need:** a git repository, an account with a coding agent provider, and somewhere to run a Linux environment.

---

## Step 1: Choose a cloud execution environment

There are four common options. They differ in how much you set up yourself and how easy it is to run many agents at once.

| Option | What it is | Setup effort | Isolation | Parallel agents | Best for |
| --- | --- | --- | --- | --- | --- |
| **Virtual machine** | A Linux VM on AWS EC2, GCE, Azure, etc. | Medium: OS, packages, SSH, firewall | Strong (separate VM) | One VM each, or shared with care | Long-lived personal workspace; full control |
| **Container** | A Docker image you run on a VM, Kubernetes, or a container platform | Medium: Dockerfile, runtime, secrets | Process/namespace level; stronger with gVisor or microVMs | Easy: one container per task | Ephemeral, reproducible, task-per-container runs |
| **Cloud development environment** | Hosted dev environments such as GitHub Codespaces, built mainly for humans | Low | Per-environment | Possible, but priced and designed for people | Developers who want an editor *and* an agent |
| **Cloud harness platform** | Managed environments built for coding agents, such as Northflank Cloud Harness | Low: pick an agent, connect a repo | Per-harness (Northflank uses microVMs) | Built in | Teams running agents regularly without building infra |

For a sourced, side-by-side comparison of 12 platforms (agents supported, isolation, session limits, BYOC and price), see the [feature matrix](../comparisons/feature-matrix.md) and [pricing](../comparisons/pricing.md).

Pick by how often you'll run agents and how many at once:

- **Trying it out** → a [Northflank Cloud Harness](../tutorials/northflank-cloud-harness/README.md) (free projects include one), or the [example container](../examples/cloud-agent-runner/README.md) on any Docker host.
- **One developer, daily use** → a persistent harness or VM you SSH into.
- **Many tasks in parallel, or a team** → one isolated environment per task: [harnesses created via the API](../examples/northflank-parallel-harnesses/README.md), or containers.

## Step 2: Connect a repository

The agent needs a clone of your repository and permission to push its work.

1. **Create a credential scoped to one repository.** On GitHub, use a [fine-grained personal access token](https://github.com/settings/personal-access-tokens/new) with access to only that repository, and grant `Contents: Read and write` and `Pull requests: Read and write`. For teams, a GitHub App installation token is better: it lasts one hour and isn't tied to a person.
2. **Inject it at runtime.** Pass it as an environment variable or platform secret. Never bake it into an image or commit it.
3. **Clone without storing the token.** Use a git credential helper that reads the token from the environment, rather than putting it in the remote URL (where it is saved in `.git/config`):

   ```bash
   git config --global credential.https://github.com.helper \
     '!f() { echo username=x-access-token; echo "password=${GITHUB_TOKEN}"; }; f'
   git clone https://github.com/your-org/your-repo.git
   ```

4. **Isolate work by branch.** Each task gets its own branch (for example `agent/claude-20261015-120000`). Protect `main` so the agent can only reach it through a pull request.

## Step 3: Install and authenticate a coding agent

Pick an agent. The [agent comparison](../agents/README.md) covers 15 of them; if you're not sure, start with the one whose models you already pay for, or with an open-source multi-provider agent such as OpenCode or Pi if you want to switch models freely.

Install it. Most agents have a one-line installer, and this repo's [`install-agents.sh`](../examples/cloud-agent-runner/install-agents.sh) installs any of them without root:

```bash
bash install-agents.sh claude-code opencode     # any of the agent ids in agents/
```

Cloud environments usually don't have a browser for the normal login flow, so authenticate with an environment variable instead:

<!-- BEGIN GENERATED: agents -->
| Agent | Made by | Licence | Models | Headless command | Auth on a server | On Northflank |
| --- | --- | --- | --- | --- | --- | --- |
| [Claude Code](../agents/claude-code.md) | Anthropic | Proprietary | Claude only | `claude -p "<task>"` | `ANTHROPIC_API_KEY`, or `CLAUDE_CODE_OAUTH_TOKEN` for a subscription | [built in](../agents/claude-code.md#option-1-run-claude-code-on-northflank-cloud-harness) |
| [Codex CLI](../agents/codex.md) | OpenAI | Apache-2.0 (open source) | OpenAI; others via config | `codex exec "<task>"` | `CODEX_API_KEY`, or `codex login --device-auth` for ChatGPT plans | [built in](../agents/codex.md#option-1-run-codex-cli-on-northflank-cloud-harness) |
| [Cursor CLI](../agents/cursor-cli.md) | Cursor (Anysphere) | Proprietary | Models on your Cursor plan | `agent -p "<task>"` | `CURSOR_API_KEY` | [built in](../agents/cursor-cli.md#option-1-run-cursor-cli-on-northflank-cloud-harness) |
| [OpenCode](../agents/opencode.md) | Anomaly (formerly SST) | MIT (open source) | 75+ providers, local models | `opencode run "<task>"` | Provider key, e.g. `ANTHROPIC_API_KEY` | [built in](../agents/opencode.md#option-1-run-opencode-on-northflank-cloud-harness) |
| [Pi](../agents/pi.md) | Earendil Works (by Mario Zechner) | MIT (open source) | 20+ providers, custom endpoints | `pi -p "<task>"` | Provider key, e.g. `ANTHROPIC_API_KEY`, or `/login` | [built in](../agents/pi.md#option-1-run-pi-on-northflank-cloud-harness) |
| [OMP](../agents/omp.md) | Stencil Labs (by Can Bölük) | MIT (open source) | 60+ providers, local | `omp -p "<task>"` | Provider key, e.g. `ANTHROPIC_API_KEY`, or `omp login <provider>` | [built in](../agents/omp.md#option-1-run-omp-on-northflank-cloud-harness) |
| [Devin CLI](../agents/devin-cli.md) | Cognition | Proprietary | Models via your Devin plan | `devin -p "<task>"` | `devin auth login --force-manual-token-flow`, or a copied `credentials.toml` | [built in](../agents/devin-cli.md#option-1-run-devin-cli-on-northflank-cloud-harness) |
| [Aider](../agents/aider.md) | Paul Gauthier and contributors | Apache-2.0 (open source) | Any LiteLLM provider, local | `aider --message "<task>"` | Provider key, e.g. `ANTHROPIC_API_KEY` | [install in an empty sandbox](../agents/aider.md#option-1-run-aider-on-northflank-cloud-harness) |
| [Amp](../agents/amp.md) | Amp (spun out of Sourcegraph) | Proprietary | Amp-served models; BYO keys | `amp -x "<task>"` | `AMP_API_KEY` | [install in an empty sandbox](../agents/amp.md#option-1-run-amp-on-northflank-cloud-harness) |
| [Crush](../agents/crush.md) | Charm | FSL-1.1-MIT (source-available) | Many providers, local | `crush run "<task>"` | Provider key, e.g. `ANTHROPIC_API_KEY` | [install in an empty sandbox](../agents/crush.md#option-1-run-crush-on-northflank-cloud-harness) |
| [Factory Droid](../agents/droid.md) | Factory | Proprietary | Factory models; BYO key | `droid exec "<task>"` | `FACTORY_API_KEY` | [install in an empty sandbox](../agents/droid.md#option-1-run-factory-droid-on-northflank-cloud-harness) |
| [Gemini CLI](../agents/gemini-cli.md) | Google | Apache-2.0 (open source) | Gemini only | `gemini -p "<task>"` | `GEMINI_API_KEY`, or a Vertex AI service account | [install in an empty sandbox](../agents/gemini-cli.md#option-1-run-gemini-cli-on-northflank-cloud-harness) |
| [GitHub Copilot CLI](../agents/copilot-cli.md) | GitHub | Proprietary | Copilot models; BYO key | `copilot -p "<task>"` | `COPILOT_GITHUB_TOKEN` (fine-grained PAT), or `copilot login --device-code` | [install in an empty sandbox](../agents/copilot-cli.md#option-1-run-github-copilot-cli-on-northflank-cloud-harness) |
| [goose](../agents/goose.md) | Agentic AI Foundation (Linux Foundation); created by Block | Apache-2.0 (open source) | 15+ providers, local | `goose run -t "<task>"` | `GOOSE_PROVIDER`, `GOOSE_MODEL` and the provider key | [install in an empty sandbox](../agents/goose.md#option-1-run-goose-on-northflank-cloud-harness) |
| [Qwen Code](../agents/qwen-code.md) | Alibaba Qwen team | Apache-2.0 (open source) | OpenAI-compatible, Anthropic, Gemini, local | `qwen -p "<task>"` | `OPENAI_API_KEY` and `OPENAI_BASE_URL` (any compatible API) | [install in an empty sandbox](../agents/qwen-code.md#option-1-run-qwen-code-on-northflank-cloud-harness) |
<!-- END GENERATED: agents -->

Also install whatever your project needs to build and test: language runtimes, package managers, databases for integration tests. **An agent can only verify its work if it can run your tests.**

## Step 4: Run your first task

There are two ways to work with a cloud agent.

**Interactive (you're watching).** SSH into the environment, start a `tmux` session so the agent survives disconnects, and run the agent:

```bash
ssh you@your-vm
tmux new -s agent
cd your-repo
opencode          # or: claude, codex, agent, pi, gemini, copilot, amp, goose, ...
```

Detach with `Ctrl-b d`, and reattach later with `tmux attach -t agent`. (On a Northflank Cloud Harness, closing the browser tab doesn't pause the harness, so the agent keeps working.)

**Headless (fire and forget).** Give the agent a task and let it run to completion with no prompts:

```bash
git switch -c agent/first-task
claude -p "Add a test for parseDate() and make it pass" \
  --permission-mode acceptEdits --allowedTools "Read,Edit,Write,Bash"
git add -A && git commit -m "agent: add parseDate test" && git push -u origin HEAD
```

The equivalent command for every agent is in [Running agents headlessly](running-agents-headless.md#the-command-for-each-agent). [`run-task.sh`](../examples/cloud-agent-runner/run-task.sh) wraps the branch → run → commit → push sequence for any of them: `run-task.sh opencode "Add a test for parseDate()"`.

Good first tasks are small and verifiable: "add a test for X", "fix this lint warning across the repo", "update the README to match the CLI's `--help` output". Avoid "refactor the whole app" until you trust the setup.

## Step 5: Secure and manage the environment

Before you run agents regularly, work through this list:

- [ ] Credentials are scoped to the single repository, and to the specific APIs, the agent needs.
- [ ] Secrets are injected at runtime, not stored in images or in the repo.
- [ ] The agent runs as a non-root user.
- [ ] `main` is protected, and agent work arrives as pull requests.
- [ ] Outbound network access is limited where your platform allows it.
- [ ] CPU and memory are sized for your test suite, and you've checked actual usage.
- [ ] Idle environments are paused or deleted automatically, or at least on a schedule.
- [ ] Each run's prompt, output, diff, and cost are logged.

Next, read:

- [Security and secrets](security-and-secrets.md)
- [Persistent vs ephemeral environments](persistent-vs-ephemeral.md)
- [Cost optimization](cost-optimization.md)
- [Running many agents in parallel](parallel-agents.md)
- [Managing agents in the cloud](managing-agents.md)
