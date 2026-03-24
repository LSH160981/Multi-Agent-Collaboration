---
name: Multi-Agent-Collaboration
description: 中文兼容入口：把复杂任务转为 OpenClaw 原生多会话协作。用于 /mac、多步骤研究、并行实现、交叉验证、A/B 对比、调试恢复等场景；主会话是唯一用户出口，其他会话只做内部工作。
---

# Multi-Agent-Collaboration

这是 **中文兼容入口**。

默认把它视为主多会话协作技能的中文包装层：

- **主技能负责核心执行规则**
- **本技能负责中文触发、中文导航、中文参考资料入口**
- 不要再维护两套彼此漂移的主流程

## 使用原则

- 只有当前主会话可以对用户说话
- 其他会话只做内部工作，禁止直接联系用户
- 优先用最小够用团队，不要无脑扩张
- 只有在拆解、交叉验证、A/B 比较、并行实现确实有价值时，才进入多会话协作
- 回复用户前必须：去重、合并、降噪、保留唯一有效结论

## 默认解释

当用户出现以下意图时，触发本技能：

- `/mac <任务>`
- 明确要求多 Agent / 多会话协作
- 复杂研发任务、调试任务、调研任务、恢复任务
- 需要更高可靠性、交叉验证、双方案比较

## 实际执行时怎么做

优先遵循主技能 `mac` 的规则，以及其背后的 Multi-Agent-Collaboration 工作流：

- 主触发技能：`/root/.openclaw/workspace/Multi-Agent-Collaboration/skills/mac/SKILL.md`
- 复杂编排技能：`/root/.openclaw/workspace/Multi-Agent-Collaboration/skills/Multi-Agent-Collaboration/SKILL.md`

## 本目录保留内容的定位

本目录只保留 **中文增强材料和历史兼容资源**，按需读取：

- `references/workflow.md`：工作流 / 角色 / 编排步骤
- `references/protocol.md`：任务包、结构化消息、输出约束
- `references/operations.md`：运行、巡检、恢复、/mac 入口相关说明

## 不要做的事

- 不要把这个中文入口再写成另一套独立主流程
- 不要假设存在平台级 slash command 注册能力
- 不要让 worker 直接联系用户
- 不要把内部 chatter 直接转发给用户

## 一句话规则

**需要中文入口时走这里；真正执行仍遵守主多会话协作技能的规则。**
