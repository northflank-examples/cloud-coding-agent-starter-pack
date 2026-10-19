#!/usr/bin/env bash
# Create one Northflank Cloud Harness per task, each on its own new branch, for any coding agent.
#
# Usage: launch.sh <tasks-file>
#   tasks-file: one task per line, "<short-name>: <prompt>", e.g.
#     signup-validation: Add input validation to the signup endpoint and tests for it
#
# Environment:
#   NF_API_TOKEN   Northflank API token (API tokens in your team or organization settings)
#   NF_PROJECT     Northflank project ID
#   REPO_URL       e.g. https://github.com/your-org/your-repo (linked to Northflank)
#   REPO_TYPE      github | gitlab | bitbucket | azure | self-hosted (default: github)
#   BASE_BRANCH    branch to start from (default: main)
#   AGENT          claude-code (default) | codex | cursor-cli | opencode | pi | omp | devin-cli run natively;
#                  aider | amp | copilot-cli | crush | droid | gemini-cli | goose | qwen-code
#                  run in an empty-sandbox harness with the agent installed by install-agents.sh
#   AGENT_API_KEY  claude-code, codex, cursor-cli: provider API key stored by the harness.
#                  Leave unset to sign in to the agent inside the harness instead.
#   AGENT_ENV      names of variables to copy from your shell into each harness, e.g.
#                  "ANTHROPIC_API_KEY GOOSE_PROVIDER GOOSE_MODEL" (provider keys for the other agents)
#   PLAN           Northflank compute plan (default: nf-compute-200 = 2 vCPU / 4 GB)
#   DRY_RUN=1      print the request bodies (secrets masked) instead of sending them
set -euo pipefail

API="https://api.northflank.com/v1"
here="$(cd "$(dirname "$0")" && pwd)"
runner="${here}/../cloud-agent-runner"

[[ $# -eq 1 && -f "$1" ]] || { echo "Usage: launch.sh <tasks-file>" >&2; exit 64; }
command -v jq >/dev/null || { echo "launch.sh: jq is required" >&2; exit 1; }
: "${NF_PROJECT:?set NF_PROJECT}" "${REPO_URL:?set REPO_URL}"
[[ "${DRY_RUN:-0}" == 1 ]] || : "${NF_API_TOKEN:?set NF_API_TOKEN}"

agent="${AGENT:-claude-code}"
# Harness type per agent, generated from data/agents.json. Only Claude Code, Codex and
# Cursor accept a stored API key; the API requires account sign-in for OpenCode, Pi, OMP and Devin CLI.
case "$agent" in
  # BEGIN GENERATED: harness-agents
  claude-code) harness_type=claude; key_auth=yes ;;
  codex) harness_type=codex; key_auth=yes ;;
  cursor-cli) harness_type=cursor; key_auth=yes ;;
  opencode) harness_type=opencode; key_auth=no ;;
  pi) harness_type=pi; key_auth=no ;;
  omp) harness_type=omp; key_auth=no ;;
  devin-cli) harness_type=devin; key_auth=no ;;
  aider) harness_type=none; key_auth=no ;;
  amp) harness_type=none; key_auth=no ;;
  copilot-cli) harness_type=none; key_auth=no ;;
  crush) harness_type=none; key_auth=no ;;
  droid) harness_type=none; key_auth=no ;;
  gemini-cli) harness_type=none; key_auth=no ;;
  goose) harness_type=none; key_auth=no ;;
  qwen-code) harness_type=none; key_auth=no ;;
  # END GENERATED: harness-agents
  *) echo "launch.sh: unknown AGENT '$agent'" >&2; exit 64 ;;
esac

b64() { base64 < "$1" | tr -d '\n'; }

# Provider keys and settings copied into every harness's runtime environment.
env_json='{}'
for var in ${AGENT_ENV:-}; do
  [[ -n "${!var:-}" ]] || { echo "launch.sh: AGENT_ENV lists $var but it isn't set" >&2; exit 64; }
  env_json=$(jq --arg k "$var" --arg v "${!var}" '. + {($k): $v}' <<<"$env_json")
done

while IFS= read -r line || [[ -n "$line" ]]; do
  [[ -z "${line// }" || "$line" == \#* ]] && continue
  name="${line%%:*}"
  prompt="${line#*:}"
  prompt="${prompt# }"
  if [[ "$name" == "$line" || -z "$prompt" ]]; then
    echo "launch.sh: skipping malformed line (want 'name: prompt'): $line" >&2
    continue
  fi
  if ! [[ "$name" =~ ^[a-z][a-z0-9-]{1,30}$ ]]; then
    echo "launch.sh: task name must be lowercase letters, digits and dashes: $name" >&2
    continue
  fi
  branch="agent/${agent}-${name}"

  # The workspace gets the task (TASK.md, $TASK), this repo's runner, and for agents
  # without a built-in harness type, the installer.
  files=$(jq -n \
    --arg task "$(printf '%s\n' "$prompt" | base64 | tr -d '\n')" \
    --arg run "$(b64 "${runner}/run-task.sh")" \
    --arg inst "$(b64 "${runner}/install-agents.sh")" \
    --arg native "$([[ "$harness_type" == none ]] && echo no || echo yes)" \
    '{
      "/home/harness/TASK.md": { data: $task, encoding: "utf-8" },
      "/home/harness/run-task.sh": { data: $run, encoding: "utf-8" }
    } + (if $native == "no" then { "/home/harness/install-agents.sh": { data: $inst, encoding: "utf-8" } } else {} end)')

  harness=$(jq -n --arg type "$harness_type" --arg key "${AGENT_API_KEY:-}" --arg key_auth "$key_auth" '
    { type: $type, cloneDirectory: "/home/harness/repo" }
    + (if $type == "none" then {}
       elif $key_auth == "yes" and $key != "" then { authMode: "apiKey", apiKey: $key }
       else { authMode: "account" } end)')

  body=$(jq -n \
    --arg name "${agent}-${name}" \
    --arg plan "${PLAN:-nf-compute-200}" \
    --arg url "$REPO_URL" \
    --arg type "${REPO_TYPE:-github}" \
    --arg base "${BASE_BRANCH:-main}" \
    --arg branch "$branch" \
    --arg agent "$agent" \
    --arg prompt "$prompt" \
    --argjson harness "$harness" \
    --argjson env "$env_json" \
    --argjson files "$files" \
    '{
      name: $name,
      description: ("Coding agent task (" + $agent + ")"),
      billing: { deploymentPlan: $plan },
      deployment: { persistentWorkspace: true, workspaceSize: 10240 },
      source: { projectUrl: $url, projectType: $type, projectBranch: $base },
      branchData: {
        source: { projectUrl: $url, projectType: $type, projectBranch: $base },
        name: $branch
      },
      harness: $harness,
      runtimeEnvironment: ($env + { TASK: $prompt, TASK_BRANCH: $branch, AGENT: $agent }),
      runtimeFiles: $files
    }')

  if [[ "${DRY_RUN:-0}" == 1 ]]; then
    jq --argjson env "$env_json" '
      (if .harness.apiKey then .harness.apiKey = "***" else . end)
      | .runtimeEnvironment |= with_entries(.key as $k | if ($env | has($k)) then .value = "***" else . end)
      | .runtimeFiles |= with_entries(.value.data = "<\(.value.data | length) base64 chars>")' <<<"$body"
    continue
  fi

  response=$(curl -sS -w '\n%{http_code}' \
    -H "Authorization: Bearer ${NF_API_TOKEN}" \
    -H "Content-Type: application/json" \
    -X POST "${API}/projects/${NF_PROJECT}/harnesses" \
    --data-binary @- <<<"$body")
  status=${response##*$'\n'}
  json=${response%$'\n'*}

  if [[ "$status" == 2* ]]; then
    echo "created $(jq -r '.data.id' <<<"$json")  branch ${branch}"
  else
    echo "failed  ${agent}-${name} (HTTP ${status}): $(jq -r '.error.message // .' <<<"$json" 2>/dev/null || echo "$json")" >&2
  fi
done < "$1"
