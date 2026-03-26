---
name: mac
description: 显式 `/mac <任务>` 入口。把当前请求强制路由到 Multi-Agent-Collaboration 多会话协作模式。适用于复杂任务拆解、并行研究、A/B 对比、交叉验证、调试恢复等需要明确进入多会话编排的场景。
---

# /mac 命令桥

这是 **Multi-Agent-Collaboration** 的显式入口，不是完整方法论文档。

## 什么时候用

当用户写出以下形式时触发：

- `/mac <任务>`

例如：

- `/mac 调研最近 7 天 GitHub star 增长最快的 10 个项目，并总结共同特点`

## 入口职责

`mac` 只负责这几件事：

1. 识别 `/mac` 前缀
2. 去掉前缀并提取真实任务
3. 把请求强制路由到 **Multi-Agent-Collaboration** 协作模式
4. 保持主会话仍是唯一用户出口

## 处理规则

收到 `/mac` 后：

1. 去掉 `/mac` 前缀
2. 解析任务目标、约束、交付物、风险
3. 判断是单人、最小团队，还是需要 A/B + review / inspect
4. 优先复用已有 session / agent；缺角色时再补
5. 用 OpenClaw 原生 session 能力执行协作
6. 最终只输出一条去重后的用户可见结论

## 硬约束

- 只有主 Agent 可以对用户发言
- 子会话只做内部工作
- 不能把内部 A2A 对话直接转发给用户
- 不要因为写了 `/mac` 就默认无限扩张团队

## 该去哪里看完整规则

`mac` 只是入口。

完整规则、角色分工、恢复、协议、消息治理，都看：

- `../multi-agent-collaboration/SKILL.md`
- `../multi-agent-collaboration/references/workflow.md`
- `../multi-agent-collaboration/references/operations.md`
- `../multi-agent-collaboration/references/protocol.md`

## 一句话

> `/mac` = 强制进入 Multi-Agent-Collaboration；真正的协作规则由主 skill 负责。 
