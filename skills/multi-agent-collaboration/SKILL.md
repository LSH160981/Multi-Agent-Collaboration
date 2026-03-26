---
name: multi-agent-collaboration
description: OpenClaw 原生多会话协作技能。用于复杂任务拆解、并行研究、A/B 对比、交叉验证、调试恢复，以及 `/mac` 显式触发。要求主会话是唯一用户出口，其他会话只做内部工作，最终由主 Agent 合并、去重、审核后输出。适用于需要 session 编排、review、inspect、recover、message hygiene 的任务。
---

# Multi-Agent-Collaboration

把这个 skill 当成 **OpenClaw 原生多会话协作模式**，不是“默认永远拉一大群 agent”。

## 核心规则

- 只保留一个用户出口：**当前主会话 / 主Agent**。
- 其他会话只做内部工作，禁止直接联系用户。
- 优先使用**最小够用团队**，不要盲目扩张。
- 只有在拆解、交叉验证、A/B 比较、并行实现确实提升质量时，才进入多会话协作。
- 用户可见输出前，主Agent 必须做：**去重、合并、清理内部噪音、只保留最新有效结论**。

## 触发规则

满足以下任一情况时使用：

- 用户写 `/mac <任务>`
- 用户明确要求用 Multi-Agent-Collaboration / 多 Agent / 多会话协作
- 任务天然分阶段：规划 → 收集 → 验证 → 汇总
- 两条独立思路并行能显著提高正确率
- 单会话完成会变慢、变乱、容易漏项

简单任务不要硬套本 skill。

## `/mac` 约定

当用户写 `/mac <任务>` 时：

1. 去掉 `/mac` 前缀
2. 提取真实任务、约束、交付物
3. 把任务路由到本技能的多会话协作流程
4. 仍然保持主会话是唯一用户出口

即使平台没有真实 slash command 注册能力，也要把纯文本 `/mac ...` 识别为强触发词。

## OpenClaw 中的真实做法

优先使用平台现成能力，不假设不存在的平台特性。

### 优先使用
- `sessions_spawn`
- `sessions_send`
- `sessions_yield`
- `sessions_list`
- `sessions_history`

### 不要依赖
- 不存在的斜杠命令注册能力
- worker 直接给用户发消息
- shell 包装去伪造平台原生能力
- 每个任务都固定建一整支永久团队

## 默认角色

按需选，不必全开。

### 主Agent
- 理解任务
- 识别缺失约束
- 判断是否真的需要多会话
- 定义交付物
- 派发 worker
- 对比结果
- 给用户输出唯一答案

### Worker 会话
常见类型：
- researcher
- implementer
- verifier
- debugger
- reviewer

每个 worker 都必须拿到：
- 清晰目标
- 输入材料
- 约束条件
- 返回格式
- 完成标准

### Reviewer / Inspect / Pool
- Reviewer：比较结果、找漏洞、提出驳回或择优建议
- Inspect：巡检、发现 stale、触发恢复动作
- Pool：复用/招聘角色、设计 A/B 编组、收紧角色边界

## 按需阅读的 references

只在需要时读，不要一次性全灌进上下文：

- `references/guides/安装与使用.md`：安装、入口、安装后测试
- `references/workflow.md`：整体工作流与角色分工
- `references/workflows-逻辑执行流程.md`：中文逻辑执行流程
- `references/workflows-伪代码.md`：中文伪代码
- `references/governance/消息治理规范.md`：主Agent 唯一出口与去重规则
- `references/operations/恢复策略.md`：中断恢复与故障处理
- `references/protocol.md`：任务包、结构化消息、最小输出契约
- `references/protocols/mac任务包协议.md`：`/mac` 任务包协议
- `references/protocols/通信协议.json`：A2A JSON 协议
- `references/operations/git记录策略.md`：git 留痕与压缩原则
- `references/operations/自动自学习方案.md`：research → review → absorb 自进化机制
- `references/testing/测试脚本.md`：安装后测试入口
- `references/strategy/权重系统与淘汰机制.md`：竞争、权重、淘汰策略

## 一句话规则

**需要多会话协作时，不论是复杂任务还是 `/mac` 触发，都走这里；用户永远只看到主Agent 收口后的一个答案。**
