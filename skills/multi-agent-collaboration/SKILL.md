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
- 优先追求隔离、异构与清晰边界，而不是一味追求更多并行
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

## Team Shape Catalog

当任务类型比较明确时，优先使用命名好的团队形态。这样可以减少编排噪音，并提高协作一致性。

### research-team
用于调研、信息汇总、交叉核验。

- 主 Agent：定义范围 + 最终汇总
- Worker A：收集事实与样本
- Worker B：独立复核 / 反驳 / 补证据
- 可选 Reviewer：冲突裁决、排名择优

### implementation-team
用于实现、编码、交付。

- 主 Agent：定义目标 + 集成结果
- Worker A：实现
- Worker B：测试 / 验证 / 查回归
- 可选 Reviewer：审代码质量、风险与边界

### debug-team
用于排障、恢复、问题定位。

- 主 Agent：定义故障现象与期望结果
- Worker A：复现 / 检查
- Worker B：提出修复方案
- Worker C：验证修复并补边界用例

### compare-team
用于 A/B 对比、方案选择、决策支持。

- Worker A：方案 A
- Worker B：方案 B
- Reviewer：比较优缺点并给建议
- 主 Agent：输出最终建议

### review-team
用于已有结果的审核、质检、挑错与收口。

- Worker A：找缺口与漏洞
- Worker B：复核关键事实或假设
- 主 Agent：合并为一个可执行结论

## 默认角色

按需选，不必全开：

- 主 Agent：理解任务、决定是否启用多会话、派发、对比、收口、对用户输出唯一答案
- Worker：research / implement / verify / debug 等具体执行位
- Reviewer：比较结果、找漏洞、提出驳回或择优建议
- Inspect / Patrol：巡检 stale、触发恢复动作
- Pool / HR：复用或招聘角色、决定 A/B 编组、收紧边界

每个 worker 最少要拿到：

- 明确目标
- 必要上下文
- 约束条件
- 输出格式
- 完成判定
- 当模型差异会影响成本或质量时，给出模型路由提示

## 执行模式

### Pattern A：按阶段拆

适用于调研、分析、汇总型任务。

1. 主 Agent 界定目标
2. Worker A 收集事实
3. Worker B 交叉验证或挑战
4. 主 Agent 综合输出

### Pattern B：按方法拆

适用于两种路径都值得独立尝试的任务。

1. 主 Agent 定义目标
2. Worker A 走方法 A
3. Worker B 走方法 B
4. Reviewer 或主 Agent 比较取舍
5. 主 Agent 输出去重后的最终结论

### Pattern C：按专业拆

适用于工程、运维、排障。

例如：

- Worker A：复现 / 检查
- Worker B：修补 / 实现
- Worker C：测试 / 验证

## Task Packet

需要时，把内部任务结构化为一个紧凑的数据包：

```json
{
  "task_id": "TASK-YYYYMMDD-HHMMSS",
  "goal": "清晰目标",
  "team_shape": "research-team|implementation-team|debug-team|compare-team|review-team",
  "role": "researcher|implementer|verifier|reviewer|debugger",
  "inputs": ["files", "links", "prior findings"],
  "constraints": ["no user contact", "cite sources", "keep changes minimal"],
  "deliverables": ["summary", "patch", "tests", "risks"],
  "done_when": ["specific completion checks"],
  "context_scope": "minimal|shared|isolated",
  "model_policy": "fast|strong-coding|long-context|heterogeneous-verification",
  "fallback_policy": "retry-once|switch-model|escalate-reviewer",
  "escalate_when": ["conflict remains", "evidence is weak", "worker stalls"]
}
```

如果 JSON 反而增加负担，就用自然语言，但尽量保留这些字段语义。

## Context Isolation Rules

默认走最小上下文原则。

- 每个 worker 只给完成当前角色所需的上下文
- 不要把完整聊天历史广播给所有 worker
- 优先用摘要交接，而不是直接甩原始 transcript
- verify / reviewer / challenger 尽量保持独立，降低从众偏差
- 中间产物只在下游确实需要时共享
- 如果任务没有明确要求共享上下文，审查类角色默认隔离

这样做可以：

- 节省 token
- 提高独立判断质量
- 降低跨 worker 污染
- 让验证更像真正的交叉验证

## Model Routing Heuristics

当宿主环境允许不同模型时，不要把所有角色都绑到同一个模型上。

建议：

- researcher：优先快、便宜、吞吐高的模型
- implementer：优先代码能力更强的模型
- verifier：尽量和 implementer 使用不同模型族，减少同质偏差
- reviewer：优先长上下文或综合判断更强的模型
- final synthesis：重要任务优先用质量最高的模型收口

启发式策略：

- 先低成本探索，再高质量复核
- 验证位优先异构模型
- worker 卡住、偏题、低置信时切换 fallback 模型
- 不要无脑把最贵模型铺给所有 worker

## Message Hygiene

对用户输出之前，主 Agent 必须：

- 移除重复发现
- 清理内部 chatter
- 把碎片更新压成一个连贯结果
- 诚实暴露不确定性
- 只保留最新有效结论
- 除非用户明确要求，否则不要把 worker 原话直接转发给用户

## Recovery Rules

当某个 worker 卡住、偏题、质量差时：

1. 先检查它已经产出了什么
2. 决定是 steer、retry、replace，还是忽略
3. 保留有价值的部分结果
4. 除非必要，不要整个流程推倒重来

优先做定点恢复，不要全局重启。

可选恢复动作：

- 用更清晰的约束重试一次
- 如果怀疑上下文过载，就缩小上下文
- 如果输出质量差，就切换更合适的模型
- 如果连续偏题，就更换 worker
- 如果结论冲突，就补 verifier 或 challenger
- 如果冲突重要且无法裁决，就升级 reviewer

## Finalization Protocol

在正式回复用户前，主 Agent 要确认整个流程已经真正收敛。

至少检查：

- 重复信息是否已删除
- 冲突结论是否已解决，或被明确标注
- 缺证据的判断是否已标记为不确定
- 承诺的 deliverables 是否都已完成
- 最终答案是否是“一个完整结果”，而不是 worker 输出堆叠

必要时，最终答案可以按以下结构组织：

1. 结论
2. 依据 / 证据
3. 剩余不确定性 / 风险
4. 下一步建议

始终只有主 Agent 对外输出最终合并结果。

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
