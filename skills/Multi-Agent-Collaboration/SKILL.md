---
name: Multi-Agent-Collaboration
description: OpenClaw 原生多会话多 Agent 协作技能。用于复杂任务拆解、并行研究、A/B 对比、交叉验证、调试恢复，以及 `/mac` 显式协作触发。要求主会话是唯一用户出口，其他会话只做内部工作，最终由主 Agent 合并输出。
user-invocable: true
---

# Multi-Agent-Collaboration

这是仓库内 **唯一保留的多会话协作主 skill**。

把它当成 OpenClaw 原生多会话协作模式，而不是“永远开大团队”的承诺。

## 先读这 8 份

第一次接手时，按这个顺序读即可：

1. `SKILL.md`
2. `安装与使用.md`
3. `逻辑执行流程.md`
4. `伪代码.md`
5. `消息治理规范.md`
6. `恢复策略.md`
7. `mac任务包协议.md`
8. `通信协议.json`

其余 `references/`、`docs/`、`examples/`、`schemas/`、`scripts/` 都是参考层，不应和主入口抢位置。

## 核心规则

- **只有当前主会话可以对用户说话**。
- 其他会话只做内部工作，禁止直接联系用户。
- 优先使用**最小够用团队**，不要盲目扩张。
- 只有在拆解、交叉验证、A/B 比较、并行实现确实有价值时，才进入多会话协作。
- 主 Agent 在回复前必须做：**去重、合并、清理内部噪音、输出唯一结论**。

## 默认接管

安装完成后的默认目标态：

- 复杂任务默认先由 **主Agent** 接住并判断是否需要多会话协作。
- 用户显式输入 `/mac <任务>` 时，必须进入多会话协作流程。
- 默认常驻核心角色只保留：**主Agent / 审核Agent / 检查Agent / AgentPool**。
- 其他 specialist 仅按需创建或复用，不常驻对外。
- 自动测试、巡检、恢复过程中，**非主Agent 仍不得直接面向用户发言**。

如果默认接管导致普通任务被过度拆解，优先退回主Agent 单会话或最小团队，而不是继续扩张。

## 何时使用

满足以下任一情况时使用：

- 任务天然分阶段：规划 → 收集 → 验证 → 汇总
- 两条独立思路能显著提高正确率
- 用户明确说 `/mac`、要求多 Agent、要求交叉验证或更高可靠性
- 单会话完成会变慢、变乱、容易漏项

简单任务不要硬套本 skill。

## `/mac` 约定

当用户写 `/mac <任务>` 时，把它理解成：

- 明确偏好使用本 skill 的多会话协作方式
- 即使平台没有真实注册 slash command，也要把纯文本 `/mac ...` 识别成强触发词

处理规则：

1. 去掉 `/mac` 前缀，提取真实任务
2. 如果任务为空，只追问缺失目标
3. 把任务路由到本技能的多会话协作流程
4. 仍然保持主会话是唯一用户出口

## OpenClaw 里的真实做法

使用 OpenClaw 现成能力，不要假设不存在的平台特性。

### 优先使用的原生能力

- `sessions_spawn`：创建内部工作会话
- `sessions_send`：给已有会话补充指令或纠偏
- `sessions_yield`：长任务等待推送完成，而不是自己死轮询
- `sessions_list` / `sessions_history`：只在需要排障或核查时使用
- ACP harness 请求：用 `sessions_spawn`，`runtime="acp"`

### 不要依赖

- 不存在的斜杠命令注册能力
- worker 直接给用户发消息
- 用 shell 包一层去假装原生功能
- 每个任务都固定建一整支永久团队

## 默认角色形状

按需选，不必全开。

### 1. 主 Agent

职责：

- 理解任务
- 识别缺失约束
- 判断是否真的需要多会话
- 定义交付物
- 派发 worker
- 对比结果
- 给用户输出唯一答案

### 2. Worker 会话

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
- 必须返回的格式
- 完成标准

### 3. Reviewer 会话

只在质量要求值得多一轮审查时使用。

职责：

- 比较不同 worker 的结果
- 找矛盾、漏洞、无证据结论、缺失测试
- 推荐最佳版本或合并方案

## 日志、记忆与状态目录约定

主文档层统一约定如下：

- `schemas/`：状态结构、评分卡、任务状态等 schema
- `examples/`：消息样例、结果样例、测试任务模板
- `scripts/`：调度、恢复、测试、自检脚本
- `references/`：只在需要时加载的补充说明

运行期至少要能区分三类留痕：

1. **日志**：发生了什么、谁做了什么、恢复动作是什么
2. **记忆/状态**：当前任务、队列、pipeline state、review 状态
3. **结果产物**：task packet、group plan、staffing decision、runtime results、final brief

原则：不同任务、不同 session 的状态和结果必须隔离，避免上下文污染与串线。

## 术语表

- **主Agent**：唯一用户出口、最终汇总者
- **审核Agent**：负责审查结果、给出通过/驳回意见
- **检查Agent**：负责巡检、告警、恢复建议
- **AgentPool**：负责招聘、编组、替换与回收 specialist
- **lead**：某个工作组的组长，负责收集组内 worker 结果
- **specialist / worker**：按专长执行子任务的内部会话
- **review**：对候选结果做比较、打分、驳回或通过
- **inspect / patrol**：运行期健康检查与恢复触发

## 恢复底线

恢复时优先遵守这 4 条：

1. 先收敛用户出口，不能放大成多 agent 同时对用户说话
2. 先 probe / 催办 / 续跑，再考虑重派或重建
3. 恢复动作必须带证据：session 观测、日志、状态文件、落盘产物
4. 同一故障要有冷却时间和重试上限，避免恢复风暴

典型高风险场景包括：worker 掉线、lead 掉线、review 中断、inspection 中断、消息重复、错误唤醒、上下文污染、默认接管副作用、`/mac` 入口失效、A/B 结果失控。

## 常见执行模式

### 模式 A：按阶段拆

适合研究、分析、交付流水线。

1. 主 Agent 定义范围
2. Worker A 收集事实
3. Worker B 做核查 / 质疑
4. 主 Agent 汇总

### 模式 B：按方法拆

适合需要独立解法的任务。

1. 主 Agent 定义目标
2. Worker A 走方案 A
3. Worker B 走方案 B
4. Reviewer 或主 Agent 比较优劣
5. 主 Agent 输出去重后的最终结论

### 模式 C：按专长拆

适合工程、调试、运维。

例如：

- worker A：复现 / 检查
- worker B：实现 / 修补
- worker C：测试 / 验证

## 推荐按需阅读的参考资料

- `references/workflow.md`：工作流 / 角色 / 编排步骤
- `references/protocol.md`：任务包、结构化消息、输出约束
- `references/operations.md`：运行、巡检、恢复、/mac 入口相关说明

## 一句话规则

**只保留这一份主 skill；需要多会话协作时，不论是复杂任务还是 `/mac` 触发，都走这里。**
