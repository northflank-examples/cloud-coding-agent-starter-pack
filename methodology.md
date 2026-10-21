# Methodology

How values in this repository are collected, normalised and calculated, so you can check or reproduce any of them.

## Scope

**Agents.** An agent is included if it's a coding agent developers can run from a terminal against their own repository, with a documented non-interactive mode, so it can run on a remote machine without a person at the keyboard. Fifteen agents qualify today; IDE-only assistants are out of scope.

**Platforms.** A platform is included if developers can use it to **run an AI coding agent against a repository in a cloud environment**: a managed harness, a vendor-hosted agent, a cloud development environment, or a sandbox platform with documented coding-agent support.

## Sources

- Only **official vendor sources** are used: pricing pages, documentation, API references and the vendor's own blog or changelog. Third-party comparisons and sales quotes are not used.
- Each platform has a `last_verified` date in [`data/platforms.json`](data/platforms.json). Values are re-checked at least quarterly and whenever a vendor announces a change.
- Pricing pages are quoted **verbatim** in `raw_quotes`, so normalisation can be checked.

## How agent data is collected

- Each agent's entry in [`data/agents.json`](data/agents.json) comes from the vendor's own documentation, its official repository, or its official package registry entry (npm, PyPI). Every fact keeps a verbatim `quote` and its `source` URL, and the guides link them.
- Flags are taken from the vendor's current CLI reference on the `last_verified` date. Where two official pages disagree (for example, Cursor's docs on whether print mode applies edits without `--force`), the recommended command uses the setting that works either way, and the guide says so under Gotchas.
- The recommended unattended command for each agent (`run.unattended`) and the commands in [`run-task.sh`](examples/cloud-agent-runner/run-task.sh) and [`install-agents.sh`](examples/cloud-agent-runner/install-agents.sh) are generated from the same entry, so the guides and the scripts can't disagree.
- Agent CLIs change quickly. The commands are checked against the documentation, but they haven't all been run end to end against every agent's live service; issues and pull requests reporting a changed flag are the fastest way to fix one.

## Missing and uncertain data

- `null` / **not published** means the vendor doesn't publish the value, or it couldn't be verified. It never means free, unlimited or unsupported.
- Assumptions that affect a platform's numbers are listed under its **Caveats**. Where an agent's docs are ambiguous or contradict each other, the guide's recommended command uses the setting that works either way, and the practical consequence appears under **Gotchas**.

## Normalisation

| Issue | How it's handled |
| --- | --- |
| Reference size | Per-hour prices are quoted for **2 vCPU / 4 GiB**, a common starting size for one coding agent (Claude Code's documented minimum is 4 GB RAM). |
| Fixed sizes (Northflank plans, Codespaces machines) | The cheapest size with at least the requested vCPU and memory is billed. |
| Per-core pricing without published RAM (Codespaces) | The machine is assumed to fit the requested memory. This is flagged on the platform page. |
| Usage billing (Sprites) | CPU is billed at the scenario's stated utilisation, and memory at the full stated size. |
| Per-core CPU pricing (Modal) | Modal prices CPU per physical core and states that 1 core = 2 vCPU, so its per-core rate is halved to get a per-vCPU rate. Modal bills the higher of requested and used resources, so it's treated as allocated billing at the requested size. Sandbox rates are used, not Modal's lower Function rates. |
| GB vs GiB | Treated as equal (the difference is about 7%). |
| Persistent storage | Billed per GB-month for every month the workspace is kept. Free allowances (Daytona's first 5 GiB, Modal's 1 TiB of Volumes) are subtracted first. Sprites' "hot" storage is added for running hours. |
| Subscription, credit and licence pricing | Not converted to per-hour prices, because the VM cost isn't separable from plan usage limits. Shown separately. |

## Cost formula

```
billed size = cheapest size that fits (fixed-size platforms) or the requested size
hourly      = vCPU × CPU rate × (utilisation, usage-billed only) + GiB × memory rate
              (or the vendor's published price for that fixed size)
storage     = GB × storage rate × months kept  [+ GB × running-storage rate × hours]
total       = environments × (hours × hourly) + environments × storage
```

The implementation is [`scripts/model.py`](scripts/model.py), with no dependencies.

## Validation

[`scripts/validate.py`](scripts/validate.py) runs in CI and checks that:

- every platform has every required field, and every non-empty feature value has a source URL;
- the model reproduces prices the vendors publish themselves (`published_checks`), such as Northflank's `nf-compute-200` at $0.0667/hr, Codespaces' 2-core machine at $0.18/hr, and E2B's calculator at $0.1656/hr for 2 vCPU / 4 GiB.

[`scripts/generate.py --check`](scripts/generate.py) fails CI if any generated table is out of date with the data.

## What's excluded from scenario totals

- Free credits and included quotas (for example, Codespaces' 120 free core-hours for personal accounts)
- Plan fees, which are shown separately
- Egress, snapshots and taxes
- **Model and token usage**, which is the same wherever the agent runs

## Known limitations

- **Not a benchmark.** A vCPU isn't identical across platforms (CPU generation, oversubscription, VM overhead), and boot time isn't measured.
- **Utilisation is an assumption.** Sprites' usage billing is sensitive to it.
- **Subscription products can't be compared per hour.** Their real cost depends on how much of your plan's usage limits the agents consume.
- **Point-in-time.** Vendors change prices and features often, so always confirm on the official page.

## Conflict of interest

This repository is maintained by Northflank, one of the platforms compared. To keep that from biasing the comparison:

- Northflank is held to the same sourcing rules as every other platform.
- All calculations are open source and reproducible.
- Cases where other platforms are stronger, such as Sprites' auto-pause or Copilot's and Claude Code's built-in network firewalls, are reported as prominently as Northflank's strengths.
- Any vendor can submit corrections (see [CONTRIBUTING.md](CONTRIBUTING.md)).
