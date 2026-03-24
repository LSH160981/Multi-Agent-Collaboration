# Workflow

## 1. Entry conditions

Use this skill when the task is multi-step, benefits from decomposition, needs cross-checking, or should survive stalls and retries.

Hard triggers:

- User sends `/mac ...`
- User explicitly asks to use Multi-Agent-Collaboration
- The task is complex enough that one agent doing everything would reduce reliability

## 2. Role model

### Main agent
- Interpret user intent
- Decide whether multi-agent mode is necessary
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

## 3. Recommended execution sequence

1. Build a task packet.
2. Decide whether to run solo, with a small team, or with A/B groups.
3. Assign work using structured messages.
4. Require artifacts and verification instructions.
5. Review before final delivery.
6. Run patrol if progress stalls.
7. Merge and deduplicate before replying to the user.

## 4. A/B competition

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

## 5. Message governance

The user should see one clean answer, not internal chatter.

Before any user-visible reply:

- remove duplicate conclusions
- merge partial progress into one status
- discard invalid intermediate states
- keep only the latest valid result
