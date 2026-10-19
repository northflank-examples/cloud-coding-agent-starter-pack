# Contributing

Corrections and additions are welcome, especially from vendors keeping their own listing accurate.

## Updating an agent

Agent CLIs change often. If a flag, install command or login method has changed:

1. Edit the agent's entry in [`data/agents.json`](data/agents.json): the short `value` used in tables, plus the `quote` and `source` from the vendor's docs. The recommended headless command is `run.unattended`; the commands the example scripts run are `container.install` and `container.run`.
2. Set `last_verified` to today's date.
3. Run `python3 scripts/generate.py`. This rewrites the agent's guide, every comparison table, and the generated blocks in `run-task.sh`, `install-agents.sh`, `launch.sh` and `manage.sh`.
4. Run `python3 scripts/validate.py`, and open a pull request linking the official page.

## Adding an agent

An agent qualifies if it's a terminal coding agent with a documented non-interactive mode. Copy an existing entry in `data/agents.json`, fill in every field from official sources (use `null` for anything undocumented), then create `agents/<id>.md` with a title, a one-paragraph introduction and an empty generated block:

```
<!-- BEGIN GENERATED: agent:<id> -->
<!-- END GENERATED: agent:<id> -->
```

Run `python3 scripts/generate.py`: the agent then appears in the README, the comparison tables, the FAQ and the example scripts.

## Updating a platform value

1. Edit the platform's entry in [`data/platforms.json`](data/platforms.json):
   - update the feature `value` (short, for tables) and optional `detail`, with its `source` URL and, ideally, a verbatim `quote`
   - for prices, update the rate and its `raw_quotes` (verbatim text from the official page)
   - set `last_verified` to today's date (YYYY-MM-DD)
   - add or adjust `open_questions` if anything is ambiguous
2. Regenerate every table: `python3 scripts/generate.py`
3. Check: `python3 scripts/validate.py`
4. Open a pull request with a link to the **official** page and the date you checked it.

CI runs `scripts/validate.py` and `scripts/generate.py --check`, and fails if the tables are out of sync with the data.

## Adding a platform

A platform qualifies if developers can use it to run an AI coding agent against a repository in a cloud environment, and it publishes enough documentation to fill the feature table.

To add one, copy an existing entry in `data/platforms.json`, then create `platforms/<id>.md` with a one-paragraph factual summary and an empty generated block:

```
<!-- BEGIN GENERATED: platform:<id> -->
<!-- END GENERATED: platform:<id> -->
```

Then run `python3 scripts/generate.py`.

## Tutorials and examples

- Every command must have been run on the platform it describes. Note the agent versions you tested with.
- Tutorials end with a result the reader can verify, such as a commit on a branch or a running agent.
- Examples use scoped tokens, non-root users and runtime secret injection, and never put credentials in images, URLs or committed files.
- Check shell scripts with `bash -n` (and `shellcheck` if you have it).

## Editorial rules

- **Facts only.** Describe what an agent or platform does and charges, not how good it is.
- **Leave unknowns as `null`.** Never fill in a guess. The tables will say "not published".
- **Hand-written prose must not contradict the data.** If you add a number to prose, prefer a generated block.
- **Northflank is held to the same standard** as every other platform, and every agent gets the same guide structure whether or not Northflank has a built-in harness type for it.

## License

Content contributions are licensed under CC BY 4.0, and code under MIT. See [LICENSE](LICENSE).
