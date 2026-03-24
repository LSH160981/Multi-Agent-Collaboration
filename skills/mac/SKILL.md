---
name: mac
description: Command bridge for native OpenClaw multi-session orchestration. Use when the user types `/mac <task>` or explicitly wants multi-agent collaboration, parallel verification, A/B comparison, or a higher-reliability coordinated workflow with one main user-facing agent.
---

# mac

Interpret `/mac <task>` as a hard trigger for the Multi-Agent-Collaboration workflow.

## Rules

1. Strip the `/mac` prefix and extract the real task.
2. If the task is empty, ask only for the missing goal.
3. Route the task into native multi-session orchestration.
4. Keep the main agent as the only user-facing role.
5. Prefer the smallest useful team instead of spawning a large org by default.
6. Use A/B workers, review, or patrol only when the task complexity actually justifies them.
7. Deduplicate and merge all internal outputs before replying.

## Execution notes

- Treat `/mac` as an explicit user preference, even if the platform has no real slash-command registration.
- Use OpenClaw-native primitives such as `sessions_spawn`, `sessions_send`, and `sessions_yield`.
- Do not let worker sessions message the user directly.
- Escalate only when decomposition, parallelism, or verification provides real value.

## Companion skill

For the fuller operating model, role structure, references, and bundled assets, follow:

- `/root/.openclaw/workspace/Multi-Agent-Collaboration/skills/Multi-Agent-Collaboration/SKILL.md`
