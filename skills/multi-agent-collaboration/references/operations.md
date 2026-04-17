# Operations

## Installation

Install these skill directories into the OpenClaw workspace `skills/` folder:

- `skills/multi-agent-collaboration/`
- `skills/mac/` for the `/mac` command bridge

Reload skills by starting a new session or restarting the gateway if needed.

## Entry points

### Natural trigger
Complex tasks may implicitly activate this skill.

### Explicit trigger

```text
/mac 帮我做一个需要拆解、审查和恢复能力的复杂任务
```

### Named trigger

```text
使用 Multi-Agent-Collaboration skill 完成这个任务
```

## Recommended operating defaults

Unless the task clearly needs more, default to:

- the smallest viable team
- one user-facing main agent
- minimal context distribution
- structured task packets when work is delegated
- reviewer / verifier isolation when independent judgment matters
- model routing by role when the runtime supports it

## Testing after installation

### Handshake test
Have agents introduce themselves to each other and state their abilities.

### Silent task test
Use a non-trivial research task and verify:

- workers keep progressing
- review happens
- the main agent produces one deduplicated answer

### Native session demo
Run:

```bash
./scripts/runtime_sessions.py "/mac 调研最近 30 天值得关注的 OpenClaw 多Agent 项目，并给出改造建议"
```

This generates task packets, group plans, and sample native session outputs under `examples/generated/native-sessions/`.

## Stall detection

Treat a worker as stale when any of these happens:

- no recent log growth
- queue status does not advance
- expected artifacts never appear
- the worker keeps acknowledging without delivering
- the same blocker persists without a recovery action

Recovery order:

1. ping
2. resend context
3. retry
4. reassign
5. rebuild the role

If low output quality or repeated drift is suspected, also consider:

- shrinking context
- switching model
- adding a verifier or challenger
- escalating to reviewer for conflict resolution

## Final delivery rule

Only the main agent may send user-visible output.

Before delivery, always:

- merge and deduplicate
- clean internal chatter
- resolve or label conflicts
- mark uncertainty honestly
- rewrite worker outputs into one coherent final answer
