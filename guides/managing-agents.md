# Managing coding agents in the cloud

**Short answer:** once agents run somewhere other than your laptop, you need to handle five things yourself: their **lifecycle** (start, pause, delete), their **versions**, their **logs**, their **cost**, and **who can reach them**. None of it is agent-specific: the same practices apply to Claude Code, Codex, OpenCode, Cursor CLI, Pi or any other agent.

## 1. Lifecycle

Every environment is in one of three states. Make the transitions deliberate.

| State | Compute billed | Workspace kept | When |
| --- | --- | --- | --- |
| Running | yes | yes | The agent is working, or you're connected |
| Paused / stopped | no | yes (disk is still billed) | Between sessions, overnight, waiting for review |
| Deleted | no | no | The branch is pushed and the work is merged or discarded |

- **Nothing pauses itself unless you set it up.** A closed browser tab or SSH session doesn't stop a VM, container or harness. Check what your platform does when idle (see the "When idle" column in the [feature matrix](../comparisons/feature-matrix.md)).
- **Push before you delete.** A deleted environment takes any unpushed commits with it.
- **Script it.** For Northflank harnesses, [`manage.sh`](../examples/northflank-parallel-harnesses/manage.sh) lists, pauses, resumes and deletes them in bulk; the CLI equivalents are `northflank pause harness`, `northflank resume harness` and `northflank delete harness`. For containers, `docker run --rm` deletes the container when the task ends.
- **Put an end-of-day pause on a schedule** for persistent workspaces, so a forgotten one costs a night, not a month.

## 2. Versions and updates

Agent CLIs release often, sometimes several times a week, and flags change between versions.

- **Pin versions in automated environments.** Install a specific version in your image (`npm install -g <package>@<version>`) and update on purpose, after testing, rather than mid-run.
- **Turn off self-updating** where the agent supports it, so a run doesn't change behaviour halfway through. Each [agent guide](../agents/README.md) lists the relevant setting where one is documented.
- **Interactive workspaces can stay on latest.** A developer working in a persistent harness benefits from fixes; the risk is in unattended runs.
- **Re-check flags after upgrades.** Headless flags in particular have been renamed or removed between versions (for example, Codex no longer supports `--full-auto`).

## 3. Logs and results

An unattended run you can't inspect afterwards is a run you can't trust. For each task keep:

- the **prompt**, the **agent and version**, and the **model**;
- the agent's **output**, ideally its JSON or JSON Lines mode, so you can extract the final message, token use and cost;
- the **diff** (the branch), the **test result**, and how long it took;
- the **outcome**: merged, revised or discarded.

[`run-task.sh`](../examples/cloud-agent-runner/run-task.sh) writes each run's output to `~/agent-logs/` and prints the diff summary. Ship those logs somewhere that outlives the environment if you delete environments after each task.

## 4. Cost

There are two bills, and they're managed differently:

- **Model usage** (tokens or a subscription) is usually the larger one. Cap it per run where the agent supports a budget flag, set spending limits on the API key itself, and log cost per task.
- **Compute** for agent environments is small per hour but grows with idle time. Pausing idle environments matters more than picking the cheapest platform.

See [Cost optimization](cost-optimization.md), and the [cost scenarios](../scenarios/README.md) for what common workloads cost on each platform.

## 5. Access

- **Who can open an environment** is who can read its secrets and push with its tokens. Restrict it to the people who need it. On Northflank, team admins can restrict which agent types members may run (**Harness policies**), and a harness's privacy setting controls whether teammates can see and connect to it.
- **Give each environment its own credentials** where you can (a per-repository GitHub token, a per-workload model API key), so you can revoke one without stopping everything.
- **Prefer short-lived tokens** for automation: GitHub App installation tokens expire after an hour.

More in [Security and secrets](security-and-secrets.md).

## Checklist

- [ ] Every environment has an owner and a way to find it again (naming convention, labels).
- [ ] Idle environments pause on a schedule or automatically.
- [ ] Automated environments pin agent versions and don't self-update.
- [ ] Each run's prompt, output, diff, cost and outcome are logged outside the environment.
- [ ] Model API keys have spending limits.
- [ ] Credentials are per-repository and per-workload, and can be revoked individually.
