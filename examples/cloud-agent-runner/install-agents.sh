#!/usr/bin/env bash
# Install one or more coding agent CLIs for the current (non-root) user.
#
# Usage: install-agents.sh <agent>... | all
#   e.g. install-agents.sh claude-code codex opencode
#
# Everything installs under $HOME: native installers use ~/.local/bin (or their own
# directory under ~), npm packages use ~/.npm-global, and if an npm-based agent is
# requested without Node.js 22+ available, Node.js 22 is downloaded to ~/.local/node.
# Nothing needs root, and on a Northflank empty-sandbox harness everything lands in
# the persistent workspace.
#
# The install line for each agent is generated from data/agents.json.
set -euo pipefail

# BEGIN GENERATED: agent-ids
AGENT_IDS="claude-code codex cursor-cli opencode pi omp devin-cli aider amp copilot-cli crush droid gemini-cli goose qwen-code"
# END GENERATED: agent-ids

[[ $# -ge 1 ]] || { echo "Usage: install-agents.sh <agent>... | all" >&2; echo "Agents: $AGENT_IDS" >&2; exit 64; }
AGENTS=" $* "
for a in $AGENTS; do
  [[ "$a" == all || " $AGENT_IDS " == *" $a "* ]] || { echo "install-agents.sh: unknown agent '$a' (known: $AGENT_IDS)" >&2; exit 64; }
done
if [[ $EUID -eq 0 ]]; then
  echo "install-agents.sh: run as a normal user; agents should not run as root" >&2
  exit 1
fi

mkdir -p "$HOME/.local/bin" "$HOME/.npm-global"
export PATH="$HOME/.local/bin:$HOME/.npm-global/bin:$HOME/.local/node/bin:$PATH"

# Use Node.js 22+ if present; otherwise install the latest 22.x release for this user.
ensure_node() {
  if command -v node >/dev/null && [[ "$(node -p 'process.versions.node.split(".")[0]')" -ge 22 ]]; then
    return 0
  fi
  local arch base file
  case "$(uname -m)" in
    x86_64) arch=x64 ;;
    aarch64|arm64) arch=arm64 ;;
    *) echo "install-agents.sh: no Node.js build for $(uname -m); install Node.js 22+ yourself" >&2; return 1 ;;
  esac
  base="https://nodejs.org/dist/latest-v22.x"
  file=$(curl -fsSL "$base/SHASUMS256.txt" | awk -v a="linux-${arch}.tar.xz" '$2 ~ a"$" {print $2; exit}')
  [[ -n "$file" ]] || { echo "install-agents.sh: couldn't find a Node.js 22 download" >&2; return 1; }
  echo "install-agents.sh: installing ${file%.tar.xz} into ~/.local/node" >&2
  rm -rf "$HOME/.local/node" && mkdir -p "$HOME/.local/node"
  curl -fsSL "$base/$file" | tar -xJ --strip-components=1 -C "$HOME/.local/node"
}

# BEGIN GENERATED: shell-install
case " $AGENTS " in *" claude-code "*|*" all "*) curl -fsSL https://claude.ai/install.sh | bash ;; esac
case " $AGENTS " in *" codex "*|*" all "*) ensure_node && npm install -g --prefix "$HOME/.npm-global" @openai/codex ;; esac
case " $AGENTS " in *" cursor-cli "*|*" all "*) curl https://cursor.com/install -fsS | bash ;; esac
case " $AGENTS " in *" opencode "*|*" all "*) ensure_node && npm install -g --prefix "$HOME/.npm-global" opencode-ai ;; esac
case " $AGENTS " in *" pi "*|*" all "*) ensure_node && npm install -g --prefix "$HOME/.npm-global" --ignore-scripts @earendil-works/pi-coding-agent ;; esac
case " $AGENTS " in *" omp "*|*" all "*) curl -fsSL https://omp.sh/install | sh -s -- --binary ;; esac
case " $AGENTS " in *" devin-cli "*|*" all "*) curl -fsSL https://cli.devin.ai/install.sh -o /tmp/devin-install.sh && { bash /tmp/devin-install.sh </dev/null || [ -x "$HOME/.local/bin/devin" ]; } ;; esac
case " $AGENTS " in *" aider "*|*" all "*) curl -LsSf https://aider.chat/install.sh | sh ;; esac
case " $AGENTS " in *" amp "*|*" all "*) curl -fsSL https://ampcode.com/install.sh | bash ;; esac
case " $AGENTS " in *" copilot-cli "*|*" all "*) curl -fsSL https://gh.io/copilot-install | bash ;; esac
case " $AGENTS " in *" crush "*|*" all "*) ensure_node && npm install -g --prefix "$HOME/.npm-global" @charmland/crush ;; esac
case " $AGENTS " in *" droid "*|*" all "*) ensure_node && npm install -g --prefix "$HOME/.npm-global" droid ;; esac
case " $AGENTS " in *" gemini-cli "*|*" all "*) ensure_node && npm install -g --prefix "$HOME/.npm-global" @google/gemini-cli ;; esac
case " $AGENTS " in *" goose "*|*" all "*) curl -fsSL https://github.com/aaif-goose/goose/releases/download/stable/download_cli.sh | CONFIGURE=false bash ;; esac
case " $AGENTS " in *" qwen-code "*|*" all "*) ensure_node && npm install -g --prefix "$HOME/.npm-global" @qwen-code/qwen-code ;; esac
# END GENERATED: shell-install

# Make the install directories available to future shells.
line='export PATH="$HOME/.local/bin:$HOME/.npm-global/bin:$HOME/.local/node/bin:$PATH"'
grep -qxF "$line" "$HOME/.bashrc" 2>/dev/null || echo "$line" >> "$HOME/.bashrc"
echo "install-agents.sh: done. Open a new shell (or: source ~/.bashrc) to use the agents." >&2
