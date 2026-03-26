---
name: mac
description: 强制进入 Multi-Agent-Collaboration 多会话协作模式。用法：`/mac <任务>`。适用于复杂任务拆解、并行研究、A/B 对比、交叉验证、调试恢复，是显式的 `/mac` 命令桥入口。
---

# /mac 命令桥

这是 **Multi-Agent-Collaboration** 的显式命令入口。

## 用法

- `/mac <任务>`
- 例如：`/mac 调研最近 7 天 GitHub star 增长最快的 10 个项目，并总结共同特点`

## 行为约定

- 把当前输入视为“强制进入多会话协作模式”
- 主 Agent 仍然是唯一用户出口
- 其他 session 只能做内部工作，禁止直接联系用户
- 若任务信息不足，先补问关键约束，再进入拆解
- 即使平台未显式展示 slash command，也要把纯文本 `/mac ...` 视为强触发词

## 处理规则

收到 `/mac` 时：

1. 去掉 `/mac` 前缀
2. 解析任务目标、约束、交付物、风险
3. 判断是最小团队、A/B 双组，还是需要 reviewer / inspect / specialist
4. 优先复用已有 session / agent；缺角色时再扩张
5. 通过 OpenClaw 原生 session 能力执行协作：
   - `sessions_spawn`
   - `sessions_send`
   - `sessions_list`
   - `sessions_history`
   - 必要时 `sessions_yield`
6. 最终只输出一条去重后的用户可见结论

## 输出纪律

- 不向用户暴露内部噪音
- 不转发原始 agent-to-agent 对话
- 合并异步回执
- 删除重复结论
- 保留最新、最可验证的版本

## 与主 skill 的关系

- `/mac` 是入口
- `Multi-Agent-Collaboration` 是完整方法论与运行体系
- 用户不写 `/mac`，但任务明显复杂时，也可以默认按 Multi-Agent-Collaboration 执行
