# Repository Map

## Purpose

This note explains how the skill-local references relate to the wider repository so maintainers know what to read first and what is only supporting material.

## Read order

When this skill triggers, prefer this order:

1. `SKILL.md`
2. `references/workflow.md`
3. `references/operations.md`
4. `references/protocol.md`
5. other references only if the task needs them

Treat the files above as the primary skill navigation layer.

## How repository folders map to the skill

### `skills/multi-agent-collaboration/`

This is the actual skill package.

- `SKILL.md`: trigger conditions, hard rules, navigation
- `references/`: reusable operational knowledge for execution

### `docs/`

Treat `docs/` as repository-level background and development notes.

Typical usage:

- `docs/guides/`: setup notes, bridge notes, operational guides
- `docs/testing/`: smoke-test and verification notes
- `docs/architecture/`: design rationale, gaps, staged pipeline notes
- `docs/research/`: research summaries and external inspiration

These files are useful, but they are not the first thing the skill should load.

### `examples/`

Treat `examples/` as canonical example inputs/outputs only when you need a concrete sample.

Use for:

- example JSON contracts
- example result packages
- example scorecards and final briefs
- example task packets and test prompts

### `examples/generated/`

Treat `examples/generated/` as evidence, demos, and runtime/test output.

Do **not** treat it as the default reference layer because:

- outputs are often time-specific
- paths may change between runs
- generated artifacts can bury the stable examples

### `schemas/`

Treat `schemas/` as the formal contract layer.

Read when you need:

- field definitions
- validation targets
- stable machine-readable output contracts

### `scripts/`

Treat `scripts/` as executable support, not primary narrative documentation.

Read only when you need to:

- inspect actual runtime behavior
- patch scripts
- verify that documentation still matches implementation

## Maintenance rule

When information exists in both a skill reference and a repository-level doc:

- keep the concise operational guidance in `skills/.../references/`
- keep deep rationale, experiments, and historical notes in `docs/`

## One-line rule

> Skill users should start in `skills/...`; repository readers can expand into `docs/`, `examples/`, `schemas/`, and `scripts/` only as needed.
