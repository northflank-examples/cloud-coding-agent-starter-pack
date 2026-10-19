# Persistent vs ephemeral environments for coding agents

**Short answer:** use **ephemeral** environments, created per task and destroyed afterwards, for automated, parallel, or untrusted work. Use a **persistent** workspace when a person comes back to the same environment repeatedly and the setup time (dependencies, builds, agent sign-in) would otherwise dominate. Many teams use a **hybrid**: persistent caches with an ephemeral working tree.

## The three patterns

### 1. Ephemeral: one environment per task

```
create env → clone → run agent → push branch → destroy env
```

- ✅ Clean, reproducible starting state every time
- ✅ Nothing leaks between tasks: no stale files, credentials, or half-finished work
- ✅ Parallelism is trivial, since each task is just another environment
- ❌ Pays setup cost on every run (clone, dependency install, warm-up)
- ❌ The agent's session history is lost unless you export it

**Use for:** CI-triggered agents, batch jobs ("fix this lint rule in 40 repos"), running agents on untrusted input such as public issues.

**Example:** `docker run --rm ... run-task.sh` in [`examples/cloud-agent-runner`](../examples/cloud-agent-runner/README.md).

### 2. Persistent: a long-lived workspace

```
create env once → (connect → work → disconnect) × N → delete when done
```

- ✅ Fast restarts: dependencies, build caches, and the agent's sign-in are already there
- ✅ The agent's conversation history and project memory carry over between sessions
- ✅ Feels like a remote laptop: SSH or editor in and continue where you left off
- ❌ State drifts over time: leftover branches, untracked files, global installs
- ❌ Costs money while idle unless you pause it
- ❌ Credentials on disk persist too, so rotate them

**Use for:** a developer's daily cloud workspace, long multi-session tasks, large monorepos where a fresh install takes many minutes.

**Example:** a VM set up with [`bootstrap-vm.sh`](../examples/cloud-agent-runner/bootstrap-vm.sh), or a Northflank Cloud Harness with **Persist workspace files** enabled. That option is on by default and keeps the home directory across pauses and restarts.

### 3. Hybrid: persistent caches, ephemeral working tree

```
persistent volume:  package caches, toolchains, a shared git clone
per task:           fresh worktree/branch → run agent → push → remove worktree
```

- ✅ Most of the speed of persistent, most of the cleanliness of ephemeral
- ✅ Works well for parallel agents on one large machine: one `git worktree` per agent, all sharing the same object store and caches
- ❌ More moving parts to set up

**Example with git worktrees:**

```bash
# once, on the persistent disk
git clone https://github.com/your-org/your-repo.git ~/cache/your-repo

# per task
git -C ~/cache/your-repo fetch origin
git -C ~/cache/your-repo worktree add -b agent/task-42 ~/tasks/task-42 origin/main
cd ~/tasks/task-42 && claude -p "..." --permission-mode acceptEdits --allowedTools "Read,Edit,Write,Bash"
git push -u origin agent/task-42
cd ~ && git -C ~/cache/your-repo worktree remove ~/tasks/task-42
```

## Decision table

| If... | Choose |
| --- | --- |
| A human connects to the same environment day after day | Persistent |
| Tasks are triggered automatically, or run in parallel | Ephemeral |
| The agent processes untrusted input (public issues, external PRs) | Ephemeral, always |
| Dependency install takes more than a few minutes | Hybrid, or persistent with care |
| You must be able to reproduce exactly what the agent saw | Ephemeral from a pinned image |
| Budget is tight and usage is bursty | Ephemeral, or persistent with auto-pause |

## What to persist and what not to

| Persist | Don't persist |
| --- | --- |
| Package manager caches (`~/.npm`, `~/.cache/pip`, `~/.cargo`) | Long-lived credentials in plain files, when you can inject them per run |
| Build caches | Uncommitted agent changes. Push them to a branch instead |
| A shared git clone (object store) | Other tasks' working trees |
| The agent's project memory files, if you rely on them | Secrets the agent wrote to disk while debugging |

## Handling interruptions

Whichever pattern you use, assume the environment can disappear mid-task:

- **Commit early, push often.** Ask the agent to commit after each working step, and push branches regularly. A pushed branch survives anything.
- **Run interactive sessions in `tmux`** so an SSH drop doesn't kill the agent.
- **Resume where possible.** Most agents can continue a previous session in the same environment: `claude -p "..." --continue`, `codex exec resume --last`, `opencode run --continue`, `pi -p --continue`, `gemini --resume latest`. Session files live in the agent's state directory (`~/.claude`, `~/.codex`, `~/.local/share/opencode`, `~/.pi/agent`, ...), so they only survive if that directory is on persistent storage. The *Resume a session* column in the [agent comparison](../agents/README.md#running-them-headlessly) has the flag for each agent.
