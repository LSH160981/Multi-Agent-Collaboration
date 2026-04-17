# Protocol

## Task packet

Represent the user request as a structured packet whenever work is distributed.

Recommended fields:

```json
{
  "task_id": "TASK-20260322-001",
  "goal": "What success looks like",
  "task_type": "research | coding | debugging | ops | mixed",
  "team_shape": "research-team | implementation-team | debug-team | compare-team | review-team",
  "complexity": "low | medium | high",
  "required_roles": ["lead", "research", "review"],
  "specialists": ["A-research", "B-research"],
  "constraints": ["only main agent talks to user"],
  "output_requirements": ["final report", "verification steps"],
  "context_paths": ["shared/context.md"],
  "context_scope": "minimal | shared | isolated",
  "model_policy": "fast | strong-coding | long-context | heterogeneous-verification",
  "fallback_policy": "retry-once | switch-model | escalate-reviewer",
  "escalate_when": ["conflict remains", "evidence is weak", "worker stalls"]
}
```

Use plain language when JSON would add overhead, but try to preserve the same fields.

## Agent-to-agent messages

Prefer JSON for internal coordination.

Common message types:

- `task_assign`
- `task_ack`
- `task_progress`
- `task_result`
- `task_reject`
- `agent_ping`
- `agent_intro`

Example:

```json
{
  "type": "task_assign",
  "task_id": "TASK-20260322-001",
  "from": "main-ceo",
  "to": "A-research",
  "goal": "Collect and verify recent examples",
  "inputs": ["docs/spec.md", "shared/context.md"],
  "constraints": ["do not contact the user"],
  "deliverables": ["summary", "sources", "risks", "verification steps"],
  "reply_to": "A-lead",
  "status": "assigned"
}
```

## Minimum worker output contract

Every worker should report:

1. what was done
2. where the artifacts are
3. how to verify the result
4. what risks or unknowns remain

## Shared context

If the same facts need to be reused by multiple agents, write them into a shared file instead of copying the same prompt repeatedly.

Even then:

- prefer summaries over raw transcripts
- keep verifier and reviewer inputs as independent as practical
- avoid giving every worker the entire task history unless it is necessary

## Recovery data sources

When recovering, check in this order:

1. queue
2. logs
3. latest artifacts
4. latest valid review state

## Recovery actions

Prefer targeted recovery over full restart.

Suggested order:

1. ping
2. resend clearer context
3. retry once
4. switch model
5. reassign role
6. escalate to reviewer or challenger
7. rebuild the role only if needed
