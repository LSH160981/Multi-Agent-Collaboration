# Agent Team Orchestration — ClawHub

来源: https://clawhub.ai/arminnaimi/agent-team-orchestration
抓取日期: 2026-03-27

以下为抓取正文（外部网页转 Markdown，本地归档）：

Production playbook for running multi-agent teams with clear roles, structured task flow, and quality gates.

## Quick Start: Minimal 2-Agent Team

A builder and a reviewer. The simplest useful team.

### 1. Define Roles

- Orchestrator — Route tasks, track state, report results
- Builder agent — Execute work, produce artifacts

### 2. Spawn a Task

1. Create task record (file, DB, or task board)
2. Spawn builder with:
   - Task ID and description
   - Output path for artifacts
   - Handoff instructions
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

Handoff message includes:
- What was done
- Where artifacts are
- How to verify
- Known issues
- What's next

### Reviews

- Builders review specs
- Reviewers check builds
- Orchestrator reviews priorities

## Common Pitfalls

- No clear artifact output paths
- No review step
- Agents not commenting on task progress
- Assigning tasks without capability checks
- Orchestrator doing execution work

## 对本仓库的启发

- 最小有用团队不是十几个角色，而是 orchestrator + builder + reviewer
- handoff 五件套值得写成硬协议
- Failed 应作为合法终态写进恢复与流程文档
- Orchestrator 不下场抢 worker 的活
