# Cost optimization for cloud coding agents

**Short answer:** running a coding agent in the cloud has two costs: **model usage** and **infrastructure**. Model usage is usually the larger one and doesn't depend on where the agent runs. Infrastructure for an agent environment is cheap per hour but adds up when environments sit idle. Right-size the environment, pause or delete it when idle, and cap model spend per task.

## The two bills

| | Model usage | Infrastructure |
| --- | --- | --- |
| **What** | Tokens sent to and from the model, or a flat subscription | CPU, RAM, disk, and network for the environment |
| **Scales with** | Task size, context size, number of turns, model choice | Instance size × hours running × number of environments |
| **Same locally and in the cloud?** | Yes | No. Locally it's hardware you already own |
| **Main levers** | Smaller tasks, cheaper models for simple work, spending caps | Right-sizing, idle shutdown, ephemeral environments |

## Infrastructure: a worked example

Agent environments don't need GPUs. A **2 vCPU / 4 GB** instance is enough for many repositories. At about **$0.067/hour** (Northflank's public price for its `nf-compute-200` plan as of October 2026; general-purpose VMs of this size on major clouds are in a similar range), the schedule matters far more than the instance size:

| Usage pattern | Hours/month | Approx. cost |
| --- | --- | --- |
| Always on (24 × 30) | 720 | ~$48 |
| Working hours only (8 × 22) | 176 | ~$12 |
| Ephemeral, 20 tasks/day × 15 min | 110 | ~$7 |

Prices change, so check your provider's current pricing. The ratio is the point: **an idle always-on environment costs four to seven times as much as one that runs only when needed.**

Persistent storage is billed separately and usually continues while the environment is paused. A few GB of workspace disk typically costs much less than the compute.

## Infrastructure levers

1. **Pause or delete idle environments.** This is the single biggest saving. Persistent workspaces should pause automatically or on a schedule. Paused environments on most platforms (including Northflank Cloud Harness) stop compute charges and keep the disk.
2. **Prefer ephemeral for automated work.** A container that exists only for the duration of a task costs only for that duration.
3. **Right-size from measurements.** Start at 2 vCPU / 4 GB (Claude Code's documented minimum is 4 GB RAM). Watch CPU and memory for a few real runs, then size for your *test suite's* peak, since the agent itself is light.
4. **Cache dependencies.** Re-installing `node_modules` on every ephemeral run costs time, and therefore compute. Use a persistent cache volume or pre-built images. See [Persistent vs ephemeral](persistent-vs-ephemeral.md).
5. **Watch storage growth.** Persistent volumes on many platforms can grow but not shrink. Start small.
6. **Run many small agents, not one huge machine,** when tasks are independent. It's easier to pause, easier to isolate, and you pay for exactly the parallelism you use.

## Model usage levers

1. **Cap spend per run** where the agent supports it (Claude Code: `claude -p "..." --max-budget-usd 2`), and cap turns where it doesn't (goose `--max-turns`; Gemini CLI and Qwen Code exit with code 53 when a turn limit is hit). Also set monthly limits on API keys in the provider console.
2. **Measure per task.** Use the agent's JSON output (for example `claude -p ... --output-format json` includes `total_cost_usd`, and Gemini CLI's JSON includes token stats) and log it with each task so you know what each kind of task costs.
3. **Write tighter tasks.** "Fix the failing test in `tests/date.test.ts`" uses far fewer tokens than "make the tests pass". Point the agent at the relevant files.
4. **Keep context small.** Large generated files, lockfiles, and vendored code in the agent's search path inflate context. Use ignore files and focused instructions.
5. **Match the model to the task.** Use smaller, cheaper models for mechanical changes and the most capable models for hard reasoning.
6. **Subscriptions vs API keys.** For one person's interactive use, a Claude or ChatGPT subscription is often more predictable than pay-per-token. For automation at scale, API keys give per-key attribution and limits. Check each provider's terms for automated use.

## Observability

You can't optimize what you don't measure. At minimum, record for each run:

- environment size and wall-clock duration → infrastructure cost
- model, tokens, or `total_cost_usd` → model cost
- outcome: merged, revised, or discarded → what you actually got for the money

A task type that costs $3 a run but whose PRs are always discarded is the first thing to cut.
