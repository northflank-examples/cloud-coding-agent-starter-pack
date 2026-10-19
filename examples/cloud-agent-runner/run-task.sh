#!/usr/bin/env bash
# Run one headless coding-agent task on a fresh branch and commit the result.
#
# Usage: run-task.sh <agent> "<task prompt>"
#   agent: claude-code | codex | cursor-cli | opencode | pi | omp | devin-cli | aider | amp |
#          copilot-cli | crush | droid | gemini-cli | goose | qwen-code
#
# Each agent reads its own credentials from the environment (see .env.example and
# agents/<agent>.md). The per-agent commands below are generated from data/agents.json.
#
# Options:
#   TASK_BRANCH             branch to work on (default: agent/<agent>-<UTC timestamp>); reused if it exists
#   PUSH=1                  push the branch to origin when done
#   LOG_DIR                 where run logs are written (default: ~/agent-logs)
#   CLAUDE_ALLOWED_TOOLS    claude-code: tools allowed without asking (default Read,Edit,Write,Bash)
#   CLAUDE_MAX_BUDGET_USD   claude-code: stop once estimated spend reaches this amount
#   CODEX_SANDBOX           codex: read-only | workspace-write (default) | danger-full-access
#   OPENCODE_MODEL, PI_MODEL, OMP_MODEL, CRUSH_MODEL   provider/model for those agents
#   DEVIN_PERMISSION_MODE   devin-cli: dangerous (default) | accept-edits | smart
#   DROID_AUTO              droid: low | medium (default) | high
#   GEMINI_APPROVAL_MODE, QWEN_APPROVAL_MODE   default yolo; auto_edit / auto-edit to allow edits only
set -euo pipefail

# BEGIN GENERATED: agent-ids
AGENT_IDS="claude-code codex cursor-cli opencode pi omp devin-cli aider amp copilot-cli crush droid gemini-cli goose qwen-code"
# END GENERATED: agent-ids

usage() {
  echo "Usage: run-task.sh <agent> \"<task prompt>\"" >&2
  echo "Agents: $AGENT_IDS" >&2
  exit 64
}

[[ $# -eq 2 ]] || usage
agent=$1
prompt=$2
[[ " $AGENT_IDS " == *" $agent "* ]] || usage

if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  echo "run-task.sh: run this inside a git repository (set REPO_URL to clone one)" >&2
  exit 1
fi
if [[ -n "$(git status --porcelain)" ]]; then
  echo "run-task.sh: working tree is not clean; commit or stash first" >&2
  exit 1
fi

branch="${TASK_BRANCH:-agent/${agent}-$(date -u +%Y%m%d-%H%M%S)}"
log_dir="${LOG_DIR:-${HOME}/agent-logs}"
log_file="${log_dir}/${branch//\//_}.log"
mkdir -p "$log_dir"

if git show-ref --verify --quiet "refs/heads/${branch}"; then
  git switch --quiet "$branch"
else
  git switch --quiet -c "$branch"
fi
base=$(git rev-parse HEAD)
echo "run-task.sh: ${agent} working on ${branch}" >&2

run_agent() {
  case "$agent" in
    # BEGIN GENERATED: runner-cases
    claude-code)
      args=(-p "$prompt" --permission-mode acceptEdits --allowedTools "${CLAUDE_ALLOWED_TOOLS:-Read,Edit,Write,Bash}" --output-format json)
      [[ -n "${CLAUDE_MAX_BUDGET_USD:-}" ]] && args+=(--max-budget-usd "$CLAUDE_MAX_BUDGET_USD")
      claude "${args[@]}"
      ;;
    codex)
      codex exec --sandbox "${CODEX_SANDBOX:-workspace-write}" "$prompt"
      ;;
    cursor-cli)
      agent -p --force --trust --output-format text "$prompt"
      ;;
    opencode)
      opencode run --auto ${OPENCODE_MODEL:+-m "$OPENCODE_MODEL"} "$prompt"
      ;;
    pi)
      pi -p ${PI_MODEL:+--model "$PI_MODEL"} "$prompt"
      ;;
    omp)
      omp -p --yolo ${OMP_MODEL:+--model "$OMP_MODEL"} "$prompt"
      ;;
    devin-cli)
      devin -p "$prompt" --permission-mode "${DEVIN_PERMISSION_MODE:-dangerous}" --respect-workspace-trust false
      ;;
    aider)
      aider --message "$prompt" --yes-always --no-auto-commits --no-gitignore \
        --chat-history-file "$log_dir/aider.chat.history.md" --input-history-file "$log_dir/aider.input.history"
      ;;
    amp)
      amp -x "$prompt"
      ;;
    copilot-cli)
      copilot -p "$prompt" --allow-all-tools --no-ask-user
      ;;
    crush)
      crush run -q ${CRUSH_MODEL:+-m "$CRUSH_MODEL"} "$prompt"
      ;;
    droid)
      droid exec --auto "${DROID_AUTO:-medium}" "$prompt"
      ;;
    gemini-cli)
      gemini -p "$prompt" --approval-mode="${GEMINI_APPROVAL_MODE:-yolo}"
      ;;
    goose)
      goose run --no-session -t "$prompt"
      ;;
    qwen-code)
      qwen -p "$prompt" --approval-mode "${QWEN_APPROVAL_MODE:-yolo}"
      ;;
    # END GENERATED: runner-cases
  esac
}

# Keep stdout and stderr: several agents print progress on stderr and the result on stdout.
set +e
run_agent 2>&1 | tee "$log_file"
status=${PIPESTATUS[0]}
set -e
[[ $status -eq 0 ]] || echo "run-task.sh: ${agent} exited with status ${status}" >&2

# The agent may have left changes uncommitted, committed them itself, or both.
if [[ -n "$(git status --porcelain)" ]]; then
  git add -A
  git commit --quiet -m "${agent}: ${prompt:0:72}"
fi

if [[ "$(git rev-parse HEAD)" == "$base" ]]; then
  echo "run-task.sh: agent made no changes (log: ${log_file})" >&2
  exit "$status"
fi

git --no-pager log --oneline "${base}..HEAD"
git --no-pager diff --stat "${base}..HEAD"

if [[ "${PUSH:-0}" == 1 ]]; then
  git push --quiet -u origin "$branch"
  echo "run-task.sh: pushed ${branch}; open a pull request to review it" >&2
else
  echo "run-task.sh: changes are on ${branch} (not pushed; set PUSH=1 to push)" >&2
fi
echo "run-task.sh: log written to ${log_file}" >&2
exit "$status"
