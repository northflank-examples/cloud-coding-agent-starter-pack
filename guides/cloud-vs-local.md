# Cloud vs local: where should your coding agent run?

**Short answer:** run the agent locally when you're pairing with it on one task and watching every step. Move it to the cloud when you want it to keep working after you close your laptop, run several tasks at once, or work in an environment that holds nothing but the one repository it needs.

## Side-by-side comparison

| Consideration | Local execution | Cloud execution |
| --- | --- | --- |
| **Setup** | Install the CLI and go | Provision an environment, toolchain, and credentials |
| **Compute** | Your laptop's CPU and RAM, shared with your editor, browser, and builds | Sized per task, without slowing down your machine |
| **Availability** | Stops when the laptop sleeps, loses Wi-Fi, or reboots | Runs independently. Reconnect from anywhere |
| **Parallel agents** | 2–3 before builds, ports, and RAM collide | One environment per agent. Limited by budget, not hardware |
| **Isolation** | The agent runs as *you*: home directory, SSH keys, cloud CLIs, browser cookies | The agent sees only what you put in the environment |
| **Private resources** | Works through your existing VPN, keys, and tokens | Needs explicit access (scoped tokens, network rules, a VPN or Tailscale for internal services) |
| **Reproducibility** | "Works on my machine" | Same image or template every run |
| **Feedback loop** | Instant: you see every edit in your editor | Slightly slower: review via SSH, a web terminal, or the resulting PR |
| **Cost** | Hardware you already own, plus model usage | Infrastructure per hour, plus the same model usage |

## When local is the right choice

- You're exploring an unfamiliar codebase and want to steer the agent turn by turn.
- The task depends on something hard to reproduce remotely, such as a device attached to your machine or a local-only service.
- You run one agent at a time, for short sessions.

## When the cloud is the right choice

- **Long-running tasks.** Migrations, large refactors, and test-fix loops that take longer than you want your laptop to stay awake.
- **Parallel work.** Five independent tickets, five agents, five branches.
- **Least-privilege execution.** You want the agent to have one repository and one scoped token, not your whole developer identity.
- **Team and automation use.** Agents triggered from CI, issue trackers, or schedules need somewhere to run that isn't someone's laptop.
- **Heavy test suites.** Your tests need more CPU or RAM than your laptop has, or they need services (databases, queues) that are easy to provision next to the agent.

## Common misconceptions

**"The cloud is more secure."** Only if you configure it that way. Copying your personal GitHub token and `~/.aws` into a VM recreates your laptop's exposure on a machine you watch less closely. The security gain comes from giving the agent *less*. See [Security and secrets](security-and-secrets.md).

**"The cloud is more expensive."** The model usage is identical wherever the agent runs, and it is usually the larger cost. Infrastructure for a typical agent environment costs cents per hour. What gets expensive is environments left running for weeks. See [Cost optimization](cost-optimization.md).

**"I need a GPU."** You don't. Hosted models run on the provider's GPUs. Your environment runs the CLI, git, and your tests.

## A middle ground

Many developers do both. They use a local agent for interactive work, and a cloud environment that the same CLI can SSH into for long or parallel tasks. Most cloud environments, including VMs, containers with SSH, and Northflank Cloud Harness, also let you open the remote workspace in VS Code or Cursor over SSH, so the cloud workspace feels local.
