# Running coding agents headlessly

**Short answer:** every terminal coding agent has a non-interactive mode that takes a prompt, works until it's done and exits. To run one in the cloud you need four things: the agent's **headless command**, a **credential in an environment variable** instead of a browser login, a way to **skip permission prompts**, and an **isolated environment** where skipping them is safe. The pattern is the same for every agent; only the flags differ.

## The pattern

```bash
# 1. Credentials come from the environment, never from a browser
export ANTHROPIC_API_KEY=...            # or the agent's own variable

# 2. Work on a branch
git switch -c agent/fix-flaky-test

# 3. Run the agent headlessly, with prompts off, and keep its output
<agent headless command> "Fix the flaky test in tests/auth.test.ts" > run.log 2>&1

# 4. Commit and push for review
git add -A && git commit -m "agent: fix flaky auth test" && git push -u origin HEAD
```

[`run-task.sh`](../examples/cloud-agent-runner/run-task.sh) does all four for any agent: `run-task.sh <agent> "<task>"`.

## The command for each agent

Each line runs one task to completion with no prompts. Run them only in an isolated environment (a container, VM or Cloud Harness) holding nothing but one repository and scoped credentials.

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

The flags, and the safer alternatives to approving everything, are explained in each [agent guide](../agents/README.md).

## Approving actions up front

Agents fall into three groups:

| Approach | Agents | What to do |
| --- | --- | --- |
| **Ask by default; a flag approves** | Claude Code, Codex, Cursor CLI, Devin CLI, Copilot CLI, Gemini CLI, Qwen Code, Factory Droid, Aider, OpenCode | Pass the approval flag. Most have a middle setting that allows file edits but not arbitrary commands, or an allowlist of commands |
| **Never ask** | Pi, OMP (`yolo` is its default approval mode), Amp, goose (`GOOSE_MODE=auto` is the default), Crush in `crush run` | Nothing to switch off. Isolation has to come from the environment |
| **Built-in sandbox** | Claude Code, Codex, Cursor CLI, Devin CLI, Copilot CLI, Gemini CLI, Qwen Code, Factory Droid (optional or default, see each guide) | Sandboxes use OS features (bubblewrap, Landlock, Seatbelt) that often aren't available inside containers. When the container or microVM is your boundary, turning the agent's own sandbox off is the documented approach |

Prefer the narrowest setting that lets the task finish. "Edit files and run the test command" is often enough; "run any command" is needed when the agent has to install dependencies.

## Getting results out

- **Exit code.** Most agents exit non-zero on failure, but few document their exit codes. Gemini CLI does: 0 success, 1 error, 42 input error, 53 turn limit exceeded. Don't rely on the exit code alone: check whether the branch has commits and whether the tests pass.
- **JSON output.** Claude Code, Codex, Cursor CLI, OpenCode, Pi, OMP, Copilot CLI, Gemini CLI, Qwen Code, goose, Amp and Factory Droid can emit JSON or JSON Lines, which you can parse for the final message, token use and cost. Aider, Crush and Devin CLI print text only (Devin CLI can export the conversation to a file with `--export`).
- **The diff is the result.** Whatever the agent says, the branch is what you review. Log the prompt, agent and version, output, diff and test result together. See [Managing agents](managing-agents.md#3-logs-and-results).

## Continuing a session

Most agents can resume a previous session in a later headless call, which is useful for follow-ups ("now add tests for the error cases") without re-explaining the task. The flag is usually `--continue` (most recent) or `--resume <id>`; see the *Resume a session* column in the [agent comparison](../agents/README.md#running-them-headlessly). On an ephemeral container, sessions disappear with the container unless the agent's state directory is on a persistent volume, which a Northflank Cloud Harness keeps by default.

## Related

- [Agent guides](../agents/README.md): install, authenticate and run each agent
- [Running many agents in parallel](parallel-agents.md)
- [Security and secrets](security-and-secrets.md)
