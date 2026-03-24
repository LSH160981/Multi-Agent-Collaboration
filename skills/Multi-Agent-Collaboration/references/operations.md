# Operations

## Installation

Install these skill directories into the OpenClaw workspace `skills/` folder:

- `skills/Multi-Agent-Collaboration/`
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

## Final delivery rule

Only the main agent may send user-visible output. Always merge, deduplicate, and clean the message first.
