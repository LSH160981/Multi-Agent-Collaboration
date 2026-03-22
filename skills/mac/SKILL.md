---
name: mac
description: Command bridge for Multi-Agent-Collaboration. Use when the user types `/mac <task>` or otherwise wants to force OpenClaw native multi-session orchestration with a single main agent, dynamic recruitment, optional A/B competition, review, patrol, and one clean final reply.
---

# mac

Interpret `/mac <task>` as a hard trigger for the full Multi-Agent-Collaboration workflow.

## Rules

1. Strip the `/mac` prefix and extract the real task.
2. If the task is empty, ask only for the missing goal.
3. Route the task into Multi-Agent-Collaboration orchestration.
4. Keep the main agent as the only user-facing role.
5. Deduplicate and merge all internal outputs before replying.

If the platform has no native slash-command registration, still treat plain text `/mac ...` as an explicit trigger.
