---
name: mac
description: Multi-Agent-Collaboration 的命令桥入口。用于把 /mac <任务> 识别为显式多 Agent 协作触发词；适用于 TUI、Telegram、GUI、WebChat 等支持技能命令或文本命令的场景。用户一旦输入 /mac，就立即进入 Multi-Agent-Collaboration 的主Agent统筹、动态招募、双组竞争、审核评分、巡检恢复流程。
user-invocable: true
---

# mac

把 `/mac <任务>` 视为 **强制进入 Multi-Agent-Collaboration** 的入口。

执行要求：

1. 去掉前缀 `/mac`，提取真实任务。
2. 如果用户只发了 `/mac` 或任务为空，要求主Agent提示用户补充任务目标。
3. 把该任务按 **Multi-Agent-Collaboration** 的方法论处理：
   - 主Agent 理解任务
   - AgentPool 动态招聘/复用角色
   - 默认采用双组竞争
   - 审核Agent 评分
   - 检查Agent 巡检与恢复
   - 最终只由主Agent向用户输出
4. 非主Agent禁止联系用户。
5. 用户可见输出前必须去重、合并异步回执、删除内部噪音。

如果平台支持原生 skill slash command，则此 skill 会暴露为 `/mac`。
如果平台不支持原生 slash command，也要把用户发来的纯文本 `/mac xxx` 视为明确触发词。
