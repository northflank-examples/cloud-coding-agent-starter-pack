#!/usr/bin/env bash
# Bootstrap a fresh Ubuntu 22.04+ or Debian 12+ VM for running coding agents.
# Run as a normal user with sudo rights, not as root:
#   bash bootstrap-vm.sh claude-code codex opencode     # or: bash bootstrap-vm.sh all
set -euo pipefail

if [[ $EUID -eq 0 ]]; then
  echo "bootstrap-vm.sh: run as a normal user; agents should not run as root" >&2
  exit 1
fi
[[ $# -ge 1 ]] || { echo "Usage: bootstrap-vm.sh <agent>... | all" >&2; exit 64; }

here="$(cd "$(dirname "$0")" && pwd)"

sudo apt-get update
sudo apt-get install -y --no-install-recommends git ca-certificates curl jq ripgrep tmux python3 xz-utils bzip2

# install-agents.sh installs Node.js 22 for this user if an npm-based agent needs it.

bash "$here/install-agents.sh" "$@"
install -m 0755 "$here/run-task.sh" "$HOME/.local/bin/run-task.sh"

cat <<'EOF'

Done. Open a new login shell so PATH picks up the new binaries, then authenticate
each agent: see agents/<agent>.md, section "Authenticate without a browser".
EOF
