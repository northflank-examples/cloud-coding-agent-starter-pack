# One repository, many agents: AGENTS.md, CLAUDE.md and friends

**Short answer:** put your project instructions in `AGENTS.md` at the repository root. Codex, OpenCode, Pi, OMP, Devin CLI, Amp, goose, Crush, Cursor CLI, Copilot CLI and Factory Droid read it directly. For the agents that look for their own file name, either point them at `AGENTS.md` in their config or add a one-line file that imports it. That way every agent, local or in the cloud, starts with the same build commands, conventions and rules.

## Who reads what

<!-- BEGIN GENERATED: agent-matrix-instructions -->
| Agent | Instructions file |
| --- | --- |
| [Claude Code](../agents/claude-code.md) | `CLAUDE.md`; reads `AGENTS.md` only when there's no `CLAUDE.md` |
| [Codex CLI](../agents/codex.md) | `AGENTS.md` (and `AGENTS.override.md`) |
| [Cursor CLI](../agents/cursor-cli.md) | `.cursor/rules`, `AGENTS.md`, `CLAUDE.md` |
| [OpenCode](../agents/opencode.md) | `AGENTS.md` (falls back to `CLAUDE.md` in OpenCode 1) |
| [Pi](../agents/pi.md) | `AGENTS.md` or `CLAUDE.md` |
| [OMP](../agents/omp.md) | `AGENTS.md` (also `.omp/AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, Cursor/Copilot rules) |
| [Devin CLI](../agents/devin-cli.md) | `AGENTS.md` (also `CLAUDE.md` and other tools' rule files) |
| [Aider](../agents/aider.md) | None loaded automatically; pass e.g. `--read CONVENTIONS.md` |
| [Amp](../agents/amp.md) | `AGENTS.md` |
| [Crush](../agents/crush.md) | `AGENTS.md`, `CRUSH.md`, `CLAUDE.md` |
| [Factory Droid](../agents/droid.md) | `AGENTS.md` (also `CLAUDE.md`) |
| [Gemini CLI](../agents/gemini-cli.md) | `GEMINI.md` (add `AGENTS.md` via `context.fileName`) |
| [GitHub Copilot CLI](../agents/copilot-cli.md) | `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, `.github/copilot-instructions.md` |
| [goose](../agents/goose.md) | `.goosehints` and `AGENTS.md` |
| [Qwen Code](../agents/qwen-code.md) | `QWEN.md` (configurable via `context.fileName`) |
<!-- END GENERATED: agent-matrix-instructions -->

## Making one file work for every agent

| Agent | How to make it read `AGENTS.md` |
| --- | --- |
| Claude Code | Reads `AGENTS.md` only when there's no `CLAUDE.md`. If you need a `CLAUDE.md`, make its first line `@AGENTS.md` to import it |
| Gemini CLI | Set `"context": { "fileName": ["AGENTS.md", "GEMINI.md"] }` in `.gemini/settings.json` |
| Qwen Code | Set `context.fileName` to include `AGENTS.md` in `.qwen/settings.json` (the docs disagree on whether it's read by default) |
| Aider | Nothing is loaded automatically: run `aider --read AGENTS.md`, or add `read: AGENTS.md` to `.aider.conf.yml` |
| goose | Reads `AGENTS.md` by default, alongside `.goosehints` |

A symlink (`ln -s AGENTS.md CLAUDE.md`) also works, but symlinks behave differently on Windows checkouts; an import line is more portable.

## What to put in it

Agents in the cloud can't ask you questions, so the file does more work than it does locally:

- **How to set up, build and test**, as exact commands: `npm ci`, `npm test -- --run`, `make lint`. An agent that can run your tests can check its own work.
- **What "done" means**: tests pass, lint is clean, no new dependencies without a reason, changes kept to the task.
- **Where things are**: the two or three directories that matter, and any generated code it mustn't edit.
- **Conventions** that a linter doesn't enforce.
- **What not to do**: don't touch migrations, don't change the public API, don't commit secrets.

Keep it short. Long instruction files fill the agent's context on every run, and Codex, for example, limits combined instruction files to 32 KiB by default.

## Treat it as code

Instructions files change agent behaviour, so review changes to them like code. They're also an input an attacker can control: an agent working on a repository you don't trust will read that repository's `AGENTS.md`. Some agents skip project-level configuration in headless mode until you trust the folder (Pi and Copilot CLI, for example); see [Security and secrets](security-and-secrets.md#6-repository-content-is-untrusted-input).
