---
name: multi-agent-collaboration
description: OpenClaw 原生多会话协作技能。用于复杂任务拆解、并行研究、A/B 对比、交叉验证、调试恢复，以及显式 `/mac` 路由后的协作执行。要求主会话是唯一用户出口，其他会话只做内部工作；优先最小团队，并在回复前完成汇总、去重、审查与风险收口。
---

# Multi-Agent-Collaboration

把这个 skill 当成 **OpenClaw 原生多会话协作模式**，不是默认永远拉一大群 agent。

## 核心规则

- 只保留一个用户出口：当前主会话 / 主 Agent
- 其他会话只做内部工作，禁止直接联系用户
- 优先使用最小够用团队，不盲目扩张
- 只有在拆解、交叉验证、A/B 比较、并行实现确实提升质量时，才进入多会话协作
- 用户可见输出前，主 Agent 必须完成：去重、合并、清理内部噪音、保留最新有效结论

## 什么时候用

满足以下任一情况时使用：

- 用户明确要求多会话 / 多 Agent / A/B 对比 / 交叉验证
- 用户写 `/mac <任务>`，由 `mac` skill 显式路由进来
- 任务天然分阶段：规划 → 收集 → 验证 → 汇总
- 需要独立验证、恢复机制或 review / inspect 兜底
- 单会话完成会变慢、变乱、容易漏项

简单任务不要硬套。

## OpenClaw 里的真实做法

优先使用平台原生能力：

- `sessions_spawn`
- `sessions_send`
- `sessions_yield`
- `sessions_list`
- `sessions_history`

不要依赖：

- 不存在的 slash 注册能力
- worker 直接对用户发消息
- 用 shell 包装伪造平台原生能力
- 每个任务都固定建一整支永久团队

## 默认角色

按需选，不必全开：

- 主 Agent：理解任务、决定是否启用多会话、派发、对比、收口、对用户输出唯一答案
- Worker：research / implement / verify / debug 等具体执行位
- Reviewer：比较结果、找漏洞、提出驳回或择优建议
- Inspect / Patrol：巡检 stale、触发恢复动作
- Pool / HR：复用或招聘角色、决定 A/B 编组、收紧边界

## 需要时再读的 references

只按需读取，不要一次性全灌进上下文：

- `references/workflow.md`：工作流、角色分工、A/B 协作
- `references/operations.md`：安装、入口、测试、恢复顺序
- `references/protocol.md`：task packet、A2A 消息、最小输出契约
- `references/repository-map.md`：skill references 与仓库 `docs/`、`examples/`、`schemas/`、`scripts/` 的映射关系
- `references/workflows-逻辑执行流程.md`：中文逻辑执行流程
- `references/workflows-伪代码.md`：中文伪代码

如果 references 与仓库根级 `docs/`、`examples/`、`schemas/` 有交叉，优先把这里视为 skill 导航入口。

## 一句话规则

> 需要多会话协作时，不论是显式 `/mac` 还是复杂任务自然触发，都走这里；用户永远只看到主 Agent 收口后的一个答案。
