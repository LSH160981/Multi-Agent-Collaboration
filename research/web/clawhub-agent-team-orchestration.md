# ClawHub - Agent Team Orchestration

来源: https://clawhub.ai/arminnaimi/agent-team-orchestration
抓取时间: 2026-03-25

## 摘要
- 最小有用团队是 2-agent：builder + reviewer。
- orchestrator 只负责路由、跟踪状态、汇报结果，不直接下场做执行。
- 任务状态建议走固定生命周期：Inbox → Assigned → In Progress → Review → Done | Failed。
- handoff 必须包含：做了什么、产物路径、如何验证、已知问题、下一步。
- 没有 review 的团队会快速质量漂移。
- 编排层必须知道 agent 能力边界，否则会把任务派给不合适的执行者。

## 可借鉴点
1. **最小团队优先**：不是一上来就全员拉满。
2. **Orchestrator 不执行**：主Agent保持统筹视角。
3. **状态机清晰**：利于恢复和巡检。
4. **交接包完整**：便于 A2A 与 reviewer 复核。

## 对本仓库的启发
- 主Agent / AgentPool / 审核Agent / 检查Agent 的职责边界应更硬。
- 队列与 handoff JSON 要有统一 schema。
- 文档要强调“先最小团队，后扩张”。
