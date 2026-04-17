# Workflow

## 1. Entry conditions

Use this skill when the task is multi-step, benefits from decomposition, needs cross-checking, or should survive stalls and retries.

Hard triggers:

- User sends `/mac ...`
- User explicitly asks to use Multi-Agent-Collaboration
- The task is complex enough that one agent doing everything would reduce reliability

Do not force multi-agent orchestration onto trivial tasks.

## 2. Team shapes

Prefer a named team shape when the task type is obvious.

### research-team
- Main agent: scope and synthesize
- Worker A: gather facts and candidates
- Worker B: independently verify or challenge
- Optional reviewer: resolve conflicts or rank outputs

### implementation-team
- Main agent: define deliverables and integrate
- Worker A: implement
- Worker B: test or verify
- Optional reviewer: audit code quality, risks, and regressions

### debug-team
- Main agent: define failure, desired outcome, and evidence threshold
- Worker A: reproduce or inspect
- Worker B: propose fix
- Worker C: verify fix and search edge cases

### compare-team
- Worker A: approach A
- Worker B: approach B
- Reviewer: compare tradeoffs and recommend
- Main agent: present final recommendation

### review-team
- Worker A: review for gaps
- Worker B: verify critical claims or assumptions
- Main agent: merge findings into one actionable result

## 3. Role model

### Main agent
- Interpret user intent
- Decide whether multi-agent mode is necessary
- Choose team shape
- Build the task packet
- Coordinate other roles
- Produce the only user-visible reply

### Pool / HR
- Check which capabilities already exist
- Reuse before recruiting
- Form Group A and Group B when competition helps
- Define role boundaries clearly

### Reviewer / Judge
- Evaluate completeness, correctness, verifiability, and risk transparency
- Reject weak submissions
- Prefer evidence-backed outputs

### Patrol / Inspector
- Inspect logs, queues, latest activity, and artifacts
- Detect stale work
- Trigger ping, retry, reassignment, or rebuild
- Record lessons for future process updates

## 4. Context isolation

Prefer minimal context by default.

- Give each worker only the context required for its role.
- Do not broadcast the full conversation history to every worker.
- Prefer summary-first handoff over raw transcript sharing.
- Keep verification and review roles as independent as possible.
- Share intermediate results only when they are necessary for downstream execution.

This reduces token waste and improves independent judgment.

## 5. Model routing

When model choice is available, route by role instead of using the same model everywhere.

Suggested defaults:

- researcher: faster and cheaper exploration models
- implementer: stronger coding models
- verifier: a different model family from the implementer when possible
- reviewer: stronger long-context or synthesis models
- final synthesis: the highest-quality available model when the task matters

Use cheap-first exploration and stronger verification for expensive tasks.

## 6. Recommended execution sequence

1. Build a task packet.
2. Choose a team shape.
3. Decide whether to run solo, with a small team, or with A/B groups.
4. Assign work using structured messages.
5. Require artifacts and verification instructions.
6. Review before final delivery.
7. Run patrol if progress stalls.
8. Merge and deduplicate before replying to the user.

## 7. A/B competition

Use A/B groups when the task is important enough to justify comparison.

Suggested bias:

- Group A: conservative, verification-heavy, reproducible
- Group B: exploratory, faster, more creative, higher variance

Review should compare:

- completeness
- accuracy
- executability
- novelty
- risk clarity
- validation quality

## 8. Message governance and finalization

The user should see one clean answer, not internal chatter.

Before any user-visible reply:

- remove duplicate conclusions
- merge partial progress into one status
- discard invalid intermediate states
- keep only the latest valid result
- resolve conflicts or label them explicitly
- mark unsupported claims as uncertain
- rewrite the final answer as one coherent result, not a dump of worker outputs
