# Run any coding agent in the cloud with Northflank Cloud Harness

By the end of this tutorial you'll have a coding agent (Claude Code, Codex, Cursor, OpenCode, Pi, Devin CLI, OMP, or any other agent you install) running in an isolated cloud workspace on Northflank, connected to your repository. You'll work with it from the browser, from your own terminal over SSH, and from VS Code or Cursor. The workspace persists when you pause it, so you can pick up where you left off.

**Time:** about 5 minutes · **Cost:** free projects include one harness (up to 1 vCPU / 1 GB); after that, compute is billed per second with no seat or per-agent fees (2 vCPU / 4 GB is $0.0667/hr) and stops while the harness is paused. See [Northflank's platform page](../../platforms/northflank.md).

## Why a harness instead of a VM?

A Cloud Harness is a workspace built for coding agents:

- **Agent preinstalled:** Claude Code, Codex, Cursor, OpenCode, Pi, Devin CLI or OMP, or an empty sandbox for any other agent (Gemini CLI, Copilot CLI, Amp, goose, Aider, Crush, Factory Droid, Qwen Code...).
- **Isolated:** each harness runs in its own Kata microVM, with its own kernel.
- **Keeps working without you:** closing your laptop or terminal doesn't stop the agent. Start a task, disconnect, and review it later.
- **Persistent:** the workspace (5–100 GiB) survives pauses, restarts and redeploys, including the repo, installed dependencies and the agent's sign-in.
- **Reachable:** web terminal, SSH, and VS Code / Cursor over SSH. Teammates can join a Team-privacy harness.
- **Runs where you need it:** Northflank's cloud, or your own AWS (including the European Sovereign Cloud), GCP, Azure, Oracle, Civo, CoreWeave or Nebius account (BYOC), or an existing Kubernetes cluster you import (BYOK). Harness nodes need microVM support.
- **Scriptable:** a REST API and CLI to create, pause, resume and delete harnesses. See [running many in parallel](../../examples/northflank-parallel-harnesses/README.md).

## Prerequisites

- A [Northflank account](https://app.northflank.com/signup). Free projects support one harness; add a payment method to run more, or larger ones
- Your Git provider [linked to Northflank](https://northflank.com/docs/v1/application/getting-started/link-your-git-account): GitHub, GitLab, Bitbucket or Azure DevOps
- A credential for your agent: an API key or an account to sign in with. Each [agent guide](../../agents/README.md) lists the options under *Authenticate without a browser*.

## Step 1: Create the harness

1. In Northflank, open a project (or create one) and go to **Harnesses** → **Create harness**.
2. **Agent:** choose one of the built-in agents, or **Empty sandbox** for anything else:

   | Agent | What to choose | Authentication |
   | --- | --- | --- |
   | Claude Code | **Claude Code** | Anthropic API key, or sign in with your Claude account |
   | Codex | **Codex** | OpenAI API key, or sign in with your ChatGPT account |
   | Cursor CLI | **Cursor** | Cursor API key, or sign in with your Cursor account |
   | OpenCode | **OpenCode** | Sign in inside the agent, or add a provider key (e.g. `ANTHROPIC_API_KEY`) as a runtime variable |
   | Pi | **Pi** | `/login` inside Pi, or add a provider key as a runtime variable |
   | OMP | **OMP** | `omp login <provider>` in the terminal, or add a provider key as a runtime variable |
   | Devin CLI | **Devin CLI** | Sign in to your Devin account in the terminal (`devin auth login --force-manual-token-flow`) |
   | Any other agent | **Empty sandbox** | Add the agent's key as a runtime variable, then install it in step 2 |

3. **Name and environment:** name it (for example `opencode-api-tests`) and choose Northflank's managed cloud or a BYOC cluster.
4. **Authentication:** for Claude Code, Codex and Cursor, choose **API key** and paste your key, or choose account sign-in to log in from the terminal.
5. **Repository:** select your repository and branch, or create a new branch. You can also create a new repository here, or skip this step. Additional repositories can be cloned into the same workspace (`additionalRepositories` in the [API](https://northflank.com/docs/v1/api/project/harnesses/create-harness)). The harness pushes through a proxy scoped to its branch, with credentials that refresh automatically.
6. **Advanced** (optional):
   - **Privacy:** **Team** lets permitted teammates connect and enables SSH. **Private** restricts access to you, through the in-app terminal only. You can't change this later, and your team must allow private harnesses first. Team admins can also restrict which agents members may run, under **Configuration → Harness policies** ([docs](https://northflank.com/docs/v1/application/cloud-harness/configure-and-manage-cloud-harnesses)).
   - **Runtime variables:** add anything your project needs, such as `GITHUB_TOKEN` or test database URLs.
   - **Resources:** 2 vCPU / 4 GB is a good start. Size up for heavy test suites.
   - **Workspace storage:** leave **Persist workspace files** on.
7. Click **Create harness**.

Northflank opens the harness terminal, with your repository cloned into the workspace. If you chose account sign-in, follow the agent's login prompt once. Because the workspace persists, you won't need to log in again after pauses.

> Prefer the CLI? `northflank create harness --projectId <project>` creates one interactively, and the [REST API](https://northflank.com/docs/v1/api/project/harnesses/create-harness) accepts the same options as the form.

## Step 2: Give the agent its first task

**Empty sandbox only:** install your agent first. Anything in the home directory persists, and this repo's installer puts everything there:

```bash
curl -fsSLO https://raw.githubusercontent.com/northflank-examples/cloud-coding-agent-starter-pack/main/examples/cloud-agent-runner/install-agents.sh
bash install-agents.sh gemini-cli      # or: amp, goose, copilot-cli, aider, crush, droid, qwen-code
source ~/.bashrc
```

In the harness terminal, start the agent (`claude`, `codex`, `agent`, `opencode`, `pi`, `gemini`, ...) and give it a small task it can verify:

```text
> Add unit tests for the date parsing helper, run the test suite, and fix anything you broke.
```

Or run it headless on a branch. The exact command for each agent is in [Every agent, headless, in one line](../../README.md#every-agent-headless-in-one-line); for example:

```bash
git switch -c agent/date-tests
opencode run --auto "Add unit tests for the date parsing helper and run the test suite"
git add -A && git commit -m "Add date parsing tests" && git push -u origin HEAD
```

Or use this repo's runner, which does the branch, run, commit and log for any agent:

```bash
curl -fsSLO https://raw.githubusercontent.com/northflank-examples/cloud-coding-agent-starter-pack/main/examples/cloud-agent-runner/run-task.sh
cd /home/harness/repo && PUSH=1 bash ~/run-task.sh opencode "Add unit tests for the date parsing helper"
```

Closing the browser tab or minimizing the terminal dock doesn't pause the harness, so a long task continues without you. Come back to the same terminal later to check on it.

## Step 3: Connect from your own terminal or editor

**Terminal:** on the harness overview, click **Connect** under *Local access* and run the SSH command it shows. You need the Northflank CLI:

```bash
npm i -g @northflank/cli
northflank login
```

**VS Code or Cursor:** add your public SSH key to your Northflank SSH identities, then start the proxy:

```bash
northflank dev ssh --projectId <project-id> --harnessId <harness-id> --proxyOnly
```

In VS Code (with the Remote - SSH extension) or Cursor, connect to the address it prints as the `harness` user, and open `/home/harness`. Your editor and the agent now share the same files.

## Step 4: Preview what the agent builds

If the agent runs a dev server, open the **Networking** panel → **Add port**. Enter the port (for example `3000`), choose the protocol, and enable **Publicly expose** to get a URL. You can also add custom domains, or protect the port with IP rules, SSO or basic auth.

## Step 5: Pause, resume, delete

- **Pause** when you're done: compute billing stops, and the workspace (repo, dependencies, agent sign-in) is kept.
- **Resume** to pick up where you left off.
- **Delete** removes the harness and its workspace permanently, so push your branches first.

From the CLI: `northflank pause harness`, `northflank resume harness`, `northflank delete harness`.

## Next steps

- **Run many agents at once:** [one harness and one branch per task, via the API](../../examples/northflank-parallel-harnesses/README.md)
- **Run in your own cloud:** [Northflank BYOC](https://northflank.com/docs/v1/application/sandboxes/sandboxes-in-your-own-cloud). The cluster needs a microVM runtime.
- **Lock it down:** [security and secrets](../../guides/security-and-secrets.md)
- **Compare platforms:** [feature matrix](../../comparisons/feature-matrix.md) and [pricing](../../comparisons/pricing.md)
- **Agent-specific details:** [agent guides](../../agents/README.md)
- Official docs: [Cloud Harness quickstart](https://northflank.com/docs/v1/application/cloud-harness/quickstart), [configure and manage harnesses](https://northflank.com/docs/v1/application/cloud-harness/configure-and-manage-cloud-harnesses)
