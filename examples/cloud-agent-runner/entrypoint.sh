#!/usr/bin/env bash
# Prepare the agent workspace, then run the container command.
#
# Environment:
#   REPO_URL          HTTPS clone URL, e.g. https://github.com/acme/api.git (optional)
#   REPO_BRANCH       branch to check out (optional, default: the repo's default branch)
#   GITHUB_TOKEN      token used for HTTPS git operations against github.com (optional)
#   GIT_AUTHOR_NAME   commit author name  (default: cloud-coding-agent)
#   GIT_AUTHOR_EMAIL  commit author email (default: cloud-coding-agent@users.noreply.github.com)
set -euo pipefail

WORKSPACE="${WORKSPACE:-/workspace}"
REPO_DIR="${WORKSPACE}/repo"

git config --global user.name "${GIT_AUTHOR_NAME:-cloud-coding-agent}"
git config --global user.email "${GIT_AUTHOR_EMAIL:-cloud-coding-agent@users.noreply.github.com}"
git config --global init.defaultBranch main

if [[ -n "${GITHUB_TOKEN:-}" ]]; then
  # The helper reads the token from the environment on each git call,
  # so the token itself is never written to .gitconfig or .git/config.
  git config --global credential.https://github.com.helper \
    '!f() { echo username=x-access-token; echo "password=${GITHUB_TOKEN}"; }; f'
fi

if [[ -n "${REPO_URL:-}" ]]; then
  if [[ -d "${REPO_DIR}/.git" ]]; then
    echo "entrypoint: reusing existing clone in ${REPO_DIR}" >&2
    git -C "$REPO_DIR" fetch --prune origin
  else
    clone_args=(--filter=blob:none)
    [[ -n "${REPO_BRANCH:-}" ]] && clone_args+=(--branch "$REPO_BRANCH")
    git clone "${clone_args[@]}" "$REPO_URL" "$REPO_DIR"
  fi
  cd "$REPO_DIR"
fi

exec "$@"
