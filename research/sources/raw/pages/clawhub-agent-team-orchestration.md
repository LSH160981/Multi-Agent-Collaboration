# ClawHub - Agent Team Orchestration（抓取）

来源：https://clawhub.ai/arminnaimi/agent-team-orchestration

Production playbook for running multi-agent teams with clear roles, structured task flow, and quality gates.

## Quick Start: Minimal 2-Agent Team

A builder and a reviewer. The simplest useful team.

### 1. Define Roles

Orchestrator (you) — Route tasks, track state, report results
Builder agent — Execute work, produce artifacts

### 2. Spawn a Task

1. Create task record (file, DB, or task board)
2. Spawn builder with:
 - Task ID and description
 - Output path for artifacts
 - Handoff instructions (what to produce, where to put it)
3. On completion: review artifacts, mark done, report

### 3. Add a Reviewer

Builder produces artifact → Reviewer checks it → Orchestrator ships or returns

## Core Concepts

### Roles

Every agent has one primary role. Overlap causes confusion.

### Task States

Inbox → Assigned → In Progress → Review → Done | Failed

Rules:
- Orchestrator owns state transitions
- Every transition gets a comment
- Failed is a valid end state

### Handoffs

Handoff 必须包含：
- What was done
- Where artifacts are
- How to verify
- Known issues
- What's next

### Reviews

Cross-role reviews prevent quality drift.

## Common Pitfalls

- 没写清楚 artifact output path
- 跳过 review 导致质量漂移
- agent 没有进度评论
- 分配任务前没核能力
- orchestrator 自己下场干执行
