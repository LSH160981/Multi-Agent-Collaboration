---
name: Multi-Agent-Collaboration
description: Coordinate complex work across multiple OpenClaw sessions with a single user-facing main agent. Use when a task benefits from decomposition, parallel research or implementation, A/B competition, review and scoring, patrol-based recovery, structured agent-to-agent messages, or explicit `/mac`-style orchestration. Best for multi-step research, complex coding, debugging, verification, recovery planning, and high-reliability tasks where only the main agent should talk to the user.
---

# Multi-Agent-Collaboration

Treat this skill as an operating model for running a small AI company on top of OpenClaw's native multi-session runtime.

Core stance:

- Treat each agent as a real OpenClaw session, not a fake inner monologue worker.
- Keep exactly one user-facing agent: the main agent.
- Route all other work through structured tasking, artifacts, logs, and reviews.
- Prefer OpenClaw-native primitives first: sessions, tools, cron, logs, files, and message routing.

## Mandatory rules

1. Only the main agent may talk to the user.
2. Non-main agents must report through structured messages or artifacts.
3. Before any user-visible reply, the main agent must deduplicate, merge asynchronous updates, remove internal noise, and send one clean conclusion.
4. For complex tasks, default to decomposition instead of solo execution.
5. Reuse existing agents when possible; recruit only for missing capabilities.
6. For medium/high-risk tasks, prefer A/B group competition plus review.
7. Patrol and recovery are part of execution, not an afterthought.

## Default control plane

Use these four persistent roles as the management layer:

- `main-ceo`: understand the request, plan, assign, merge, and deliver the final answer
- `pool-hr`: recruit or reuse workers, define boundaries, form groups
- `review-judge`: review outputs, score quality, approve or reject
- `inspect-patrol`: detect stalls, trigger recovery, record failure patterns

Specialists are dynamic. Add them only when the task clearly needs them.

## Execution flow

1. Parse the user request into a task packet.
2. Decide whether the task needs multi-agent handling.
3. If requirements are missing, the main agent asks only for critical gaps.
4. Form or reuse the control plane and recruit specialists as needed.
5. For substantial work, create Group A and Group B with different execution biases.
6. Dispatch structured task messages and require deliverables, verification steps, and risk notes.
7. Send outputs through review.
8. Let patrol inspect stalled work and recover from the latest valid state.
9. Have the main agent merge the winning result into one user-facing reply.

## How to use bundled references

Read only what is needed:

- `references/workflow.md` — end-to-end operating flow, role model, and orchestration checkpoints
- `references/protocol.md` — task packet fields, agent-to-agent JSON message types, and output expectations
- `references/operations.md` — installation, `/mac` entry, testing, patrol, and recovery guidance

## Practical guidance

- Prefer shared context files over repeatedly pasting the same background into many sessions.
- Require every worker to state: what was done, where artifacts live, how to verify, and what risks remain.
- When recovering, resume from queue/log/artifact state instead of restarting the whole task.
- When the task is simple, stay lightweight; do not force a full org chart for trivial work.

## `/mac` convention

If the user says `/mac <task>`, treat it as an explicit request to use this full orchestration model. If the platform lacks native slash commands, still interpret the text `/mac ...` as a hard trigger.
