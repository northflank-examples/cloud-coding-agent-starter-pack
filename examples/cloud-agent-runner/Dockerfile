# A non-root environment for running any of the coding agents in this repo headlessly.
#
# Build with the agents you want (space-separated ids, or "all"):
#   docker build --build-arg AGENTS="claude-code codex opencode" -t cloud-agent .
FROM node:22-bookworm-slim

ARG AGENTS="claude-code codex"

RUN apt-get update \
 && apt-get install -y --no-install-recommends \
      git ca-certificates curl jq ripgrep openssh-client python3 bzip2 \
 && rm -rf /var/lib/apt/lists/*

COPY entrypoint.sh run-task.sh install-agents.sh /usr/local/bin/
RUN chmod 0755 /usr/local/bin/entrypoint.sh /usr/local/bin/run-task.sh /usr/local/bin/install-agents.sh \
 && mkdir -p /workspace \
 && chown node:node /workspace

# The node base image ships an unprivileged "node" user (uid 1000). Agents install
# into its home directory and run as it.
USER node
ENV PATH=/home/node/.local/bin:/home/node/.npm-global/bin:$PATH
RUN install-agents.sh $AGENTS

# The image is the version pin: stop agents updating themselves mid-run.
# Each setting is documented by its agent; see agents/<agent>.md.
# CODEX_SANDBOX: the container is the isolation boundary, and Codex's own sandbox often
# can't start inside Docker. Override with -e CODEX_SANDBOX=workspace-write if it can.
ENV DISABLE_AUTOUPDATER=1 \
    OPENCODE_DISABLE_AUTOUPDATE=1 \
    COPILOT_AUTO_UPDATE=false \
    AMP_SKIP_UPDATE_CHECK=1 \
    FACTORY_DROID_AUTO_UPDATE_ENABLED=false \
    AIDER_CHECK_UPDATE=false \
    PI_SKIP_VERSION_CHECK=1 \
    GOOSE_DISABLE_KEYRING=1 \
    WORKSPACE=/workspace \
    CODEX_SANDBOX=danger-full-access

WORKDIR /workspace
ENTRYPOINT ["entrypoint.sh"]
CMD ["bash"]
