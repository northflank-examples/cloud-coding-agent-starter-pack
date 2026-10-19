# Northflank Cloud Harness: running coding agents in the cloud

MicroVM-isolated cloud workspaces preconfigured for a coding agent (Claude Code, Codex, Cursor, OpenCode, Pi, Devin CLI or OMP) or as an empty sandbox for any agent, on Northflank's cloud or in your own cloud account, with a web terminal, SSH/IDE access and a persistent /home/harness workspace.

> Disclosure: this repository is maintained by Northflank. Northflank's data follows the same methodology as every other platform here.

<!-- BEGIN GENERATED: platform:northflank -->
Last verified: **2026-10-19** · Official pricing: <https://northflank.com/pricing>

## At a glance

|  |  |
| --- | --- |
| Type | Managed agent harness |
| Coding agents | Claude Code, Codex, Cursor, OpenCode, Pi, Devin CLI, OMP; any other agent in an empty sandbox |
| Environment / image | Northflank harness image, your own build, or any registry image; CPU/RAM from 0.1 to 32 vCPU plans |
| Isolation | Kata microVM per harness |
| API / programmatic | REST API, JavaScript SDK, Python SDK, CLI, dashboard |
| Persistence | Yes: persistent workspace volume, 5–100 GiB (on by default) |
| When idle | Runs until paused; paused = no compute charge |
| Max session | No limit |
| Concurrency | 1 harness on free projects; no limit on paid |
| Access | Web terminal, SSH, VS Code / Cursor over SSH; teammates can share a harness |
| Git integration | GitHub, GitLab, Bitbucket, Azure DevOps or self-hosted Git; clone a branch, create a new branch or a new repository, plus additional repositories |
| Secrets | Runtime variables and secret files; agent API key or linked account |
| Network controls | Public/private ports, custom domains, per-port IP/SSO/basic-auth rules |
| Run in your own cloud | Yes, self-serve: AWS, AWS European Sovereign Cloud, GCP, Azure, Oracle, Civo, CoreWeave, Nebius; or import your own Kubernetes cluster (BYOK) |
| Billing model | fixed machine sizes, while running |
| Price (2 vCPU / 4 GiB) | $0.0667/hr |
| Storage | Volumes $0.15/GB-month |
| Plan fee | None (pay-as-you-go) |
| Free tier / credits | Free projects: 1 harness, up to 1 vCPU / 1 GB |

## Details

- **Coding agents:** Claude Code, Codex, Cursor, OpenCode, Pi, Devin CLI, OMP; any other agent in an empty sandbox. Vendor docs: "`type`: (string) (required) The harness environment type to run. (enum: codex, claude, pi, omp, devin, opencode, cursor, none)" ([source](https://northflank.com/docs/v1/api/project/harnesses/create-harness))
- **Environment / image:** Northflank harness image, your own build, or any registry image; CPU/RAM from 0.1 to 32 vCPU plans. Vendor docs: "Container image source. Managed uses the Northflank harness image, internal uses a Northflank build service, and external uses a registry image. (enum: managed, internal, external)" ([source](https://northflank.com/docs/v1/api/project/harnesses/create-harness.md))
- **Isolation:** Each harness runs in its own microVM with its own kernel. BYOC clusters need a microVM runtime (Kata Containers) on nodes that support it. Vendor docs: "Each Harness runs in its own isolated microVM, separating its workloads from other Harnesses and the underlying host infrastructure." ([source](https://northflank.com/blog/how-to-run-remote-coding-agents))
- **API / programmatic:** REST endpoints under /v1/projects/{projectId}/harnesses (list, create, put, get, patch, delete, logs, pause, restart, resume); JavaScript SDK `@northflank/js-client`, Python SDK `northflank` (pip), and the `northflank` CLI (`northflank dev ssh` connects from a terminal or editor). Vendor docs: "You create them, run commands, access files, and destroy them programmatically with the JavaScript or Python SDK." ([source](https://northflank.com/docs/v1/application/sandboxes/quickstart))
- **Persistence:** Persist workspace files is on by default and keeps the workspace across pauses, restarts and redeploys. The volume is 5,120–102,400 MiB, can grow but not shrink, and persistence can only be set at creation. Vendor docs: "Persist workspace files is enabled by default under Advanced → Workspace storage. It preserves files in `/home/harness` across stops, restarts, and redeployments. Files outside this directory are temporary." ([source](https://northflank.com/docs/v1/application/cloud-harness/configure-and-manage-cloud-harnesses))
- **When idle:** There is no automatic sleep. Pausing scales the harness to zero and stops compute billing, and persisted files remain. Vendor docs: "Compute is billed per second, and pausing a Harness stops compute billing." ([source](https://northflank.com/blog/how-to-run-remote-coding-agents))
- **Max session:** No limit. Vendor docs: "An active Cloud Harness runs continuously until you pause or delete it." ([source](https://northflank.com/docs/v1/application/cloud-harness/quickstart))
- **Concurrency:** 1 harness on free projects; no limit on paid. Vendor docs: "Free projects support one harness, including paused harnesses." ([source](https://northflank.com/docs/v1/application/cloud-harness/quickstart))
- **Access:** Web terminal, SSH, VS Code / Cursor over SSH; teammates can share a harness. Vendor docs: "Access your Cloud Harness from your terminal, Visual Studio Code, or Cursor using SSH." ([source](https://northflank.com/docs/v1/application/cloud-harness/quickstart))
- **Git integration:** `source` links an existing repository and branch; `branchData` creates a new branch from a base branch; `repositoryData` creates a new repository (public or private) on a linked account; `additionalRepositories` clones more repositories alongside the primary one; `cloneDirectory` sets where the repo is cloned. Pushes go through a proxy scoped to the harness branch, with credentials that refresh automatically. Vendor docs: "`projectType`: (string) (required) The VCS provider to use. (enum: bitbucket, gitlab, github, self-hosted, azure, origin)" ([source](https://northflank.com/docs/v1/api/project/harnesses/create-harness))
- **Secrets:** Runtime variables and secret files; agent API key or linked account. Team admins choose which harness types members can create (Harness policies). ([source](https://northflank.com/docs/v1/application/cloud-harness/configure-and-manage-cloud-harnesses))
- **Network controls:** Add HTTP, HTTP/2, TCP or UDP ports, public or private, with custom domains and per-port security rules. No outbound egress allowlist for harnesses is documented. ([source](https://northflank.com/docs/v1/application/cloud-harness/configure-and-manage-cloud-harnesses))
- **Run in your own cloud:** Northflank provisions and manages the cluster in your account, on the provider's managed Kubernetes service (EKS, GKE, AKS, OKE, Civo Kubernetes, CKS, Nebius Managed Kubernetes). Harnesses need nodes that support a microVM runtime (Kata Containers). Vendor docs: "You can also import an existing Kubernetes cluster (BYOK) for Northflank to manage." ([source](https://northflank.com/docs/v1/application/bring-your-own-cloud/use-other-cloud-providers-with-northflank))
- **BYOC pricing:** $0.02083/vCPU-hour management fee, $0 memory; cloud costs paid to your provider

## Published pricing (verbatim)

- "CPU $ 0.01667 / vCPU / hour"
- "Memory $ 0.00833 / GB / hour"
- "Disk $ 0.15 / GB / month"
- "nf-compute-200 vCPU 2 dedicated Memory 4096 MB Price $ 48.00 /month ($ 0.0667 /hr)"
- "Free projects support one harness, including paused harnesses."
- "Compute is billed per second, and pausing a Harness stops compute billing."

## Cost in the standard scenarios

| Scenario | Compute | Storage | Total |
| --- | --- | --- | --- |
| [1 dev, workdays](../scenarios/solo-developer.md) | $11.73 | $3.00 | $14.73 |
| [10 agents × 1 h](../scenarios/parallel-agents.md) | $0.67 | $0.00 | $0.67 |
| [100 tasks × 30 min](../scenarios/batch-tasks.md) | $3.33 | $0.00 | $3.33 |
| [10 × 24/7 (month)](../scenarios/team-always-on.md) | $486.62 | $30.00 | $516.62 |

## Caveats and open questions

- Harnesses are billed on Northflank's standard compute plans: the create-harness API requires billing.deploymentPlan. The pricing page doesn't mention harnesses by name.
- The default harness size isn't published. The workspace volume is 5,120–102,400 MiB per the API; its default when omitted isn't stated.
- No outbound egress allowlist for harnesses is documented.
- Devin CLI and OMP harness types are documented in the create-harness API reference; Northflank's quickstart and product pages will list them in an upcoming docs update.
- Some Cloud Harness details here (Kata microVMs, agents continuing to run after you disconnect, branch-scoped git push credentials, and a free-plan harness limit of 1 vCPU / 1 GB) come from Northflank's Cloud Harness product page, which isn't public yet as of 2026-10-19. Source links will be added when it's live.

## Sources

- <https://api.northflank.com/v1/plans>
- <https://northflank.com/blog/how-to-run-remote-coding-agents>
- <https://northflank.com/docs/v1/api/project/harnesses/create-harness>
- <https://northflank.com/docs/v1/api/project/harnesses/create-harness.md>
- <https://northflank.com/docs/v1/application/bring-your-own-cloud/use-other-cloud-providers-with-northflank>
- <https://northflank.com/docs/v1/application/cloud-harness/configure-and-manage-cloud-harnesses>
- <https://northflank.com/docs/v1/application/cloud-harness/quickstart>
- <https://northflank.com/docs/v1/application/sandboxes/quickstart>
- <https://northflank.com/pricing>
<!-- END GENERATED: platform:northflank -->

[← Back to the comparison](../README.md) · [Feature matrix](../comparisons/feature-matrix.md) · [Pricing](../comparisons/pricing.md)
