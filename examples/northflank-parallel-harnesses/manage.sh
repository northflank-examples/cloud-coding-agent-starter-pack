#!/usr/bin/env bash
# List, pause, resume or delete the task harnesses created by launch.sh.
#
# Usage: manage.sh list
#        manage.sh pause|resume|delete <harness-id>... | --all
#
# --all acts on every harness in the project whose name starts with an agent id
# ("claude-code-", "opencode-", ...), as launch.sh names them.
# Environment: NF_API_TOKEN, NF_PROJECT
set -euo pipefail

API="https://api.northflank.com/v1"
: "${NF_API_TOKEN:?set NF_API_TOKEN}" "${NF_PROJECT:?set NF_PROJECT}"
command -v jq >/dev/null || { echo "manage.sh: jq is required" >&2; exit 1; }

# BEGIN GENERATED: agent-ids
AGENT_IDS="claude-code codex cursor-cli opencode pi omp devin-cli aider amp copilot-cli crush droid gemini-cli goose qwen-code"
# END GENERATED: agent-ids

nf() {
  local method=$1 path=$2
  curl -sS --fail-with-body -X "$method" \
    -H "Authorization: Bearer ${NF_API_TOKEN}" \
    "${API}/projects/${NF_PROJECT}/harnesses${path}"
}

task_harnesses() {
  local pattern="^(${AGENT_IDS// /|})-"
  nf GET "" | jq -r --arg re "$pattern" '.data.harnesses[] | select(.id | test($re)) | .id'
}

action=${1:-}
shift || true

case "$action" in
  list)
    # The list endpoint doesn't document status fields, so read each harness individually.
    printf 'ID\tPAUSED\tDEPLOYMENT\n'
    nf GET "" | jq -r '.data.harnesses[].id' | while IFS= read -r id; do
      nf GET "/${id}" | jq -r '[.data.id, (if .data.harnessPaused == null then "unknown" else (.data.harnessPaused | tostring) end), (.data.status.deployment.status // "unknown")] | @tsv'
    done
    ;;
  pause|resume|delete)
    if [[ "${1:-}" == --all ]]; then
      ids=()
      while IFS= read -r id; do ids+=("$id"); done < <(task_harnesses)
    else
      ids=("$@")
    fi
    [[ ${#ids[@]} -gt 0 && -n "${ids[0]}" ]] || { echo "manage.sh: no harnesses given" >&2; exit 64; }
    if [[ "$action" == delete ]]; then
      echo "This permanently deletes ${#ids[@]} harness(es) and their workspaces:" >&2
      printf '  %s\n' "${ids[@]}" >&2
      read -r -p "Type 'delete' to confirm: " answer
      [[ "$answer" == delete ]] || { echo "Aborted." >&2; exit 1; }
    fi
    for id in "${ids[@]}"; do
      case "$action" in
        pause)  nf POST "/${id}/pause" >/dev/null ;;
        resume) nf POST "/${id}/resume" >/dev/null ;;
        delete) nf DELETE "/${id}" >/dev/null ;;
      esac
      echo "${action}d ${id}"
    done
    ;;
  *)
    echo "Usage: manage.sh list | pause|resume|delete <harness-id>... | --all" >&2
    exit 64
    ;;
esac
