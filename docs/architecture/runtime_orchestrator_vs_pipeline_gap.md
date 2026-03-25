# runtime_orchestrator 与 staged pipeline 收口差异

> 对应子任务：79cd8a7c-d316-46e1-994a-2adaafe01f2f
> 目的：把当前 real runtime orchestrator 与 staged pipeline 的字段差异明确写清，方便后续直接补齐后半段收口一致性。

## 当前已确认事实

### runtime_orchestrator 已稳定产出
- `task-packet.json`
- `group-plan.json`
- `staffing-decision.json`
- `runtime-results.json`

### runtime-results.json 当前已包含
- `task_packet`
- `group_plan`
- `staffing`
- `worker_a_result`
- `worker_b_result`
- `review_result`
- `final_result`
- `session_probe`

这说明：
- orchestrator 前半段已稳定落盘
- 审核与最终汇总结果也已经进入同一结果文件
- session 观测已并入收口结果

## 与 staged pipeline 的主要差异

### 1. inspection 结果未并入 runtime-results
staged pipeline 口径里，inspection 是显式阶段产物；
但 `runtime_orchestrator.py` 当前只是把 inspect agent 的回包放在 `coordinator_results.inspect_agent`，没有提升为顶层 `inspection_result`。

### 2. 缺少 stage 字段
staged pipeline 使用：
- `stage1_done`
- `stage2_done`
- `stage3_done`

而 runtime orchestrator 当前只有：
- `status: partial`
- `status: ok`

这会导致：
- staged 校验脚本无法直接把它当成 pipeline-state
- 恢复逻辑难以复用统一 stage 语义

### 3. 缺少 resume_recommendation
staged pipeline 收口时会写：
- `resume_recommendation`

用于说明：
- 下一步是什么
- 当前是否已经收口
- 若中断应从哪一阶段恢复

runtime orchestrator 当前没有这个字段，导致 inspect/recover 体系很难直接复用同一判断模板。

## 建议最小对齐方案

### 方案 A：保持 runtime-results 命名，但补 staged 核心字段
在 `runtime-results.json` 顶层补：

- `inspection_result`
- `stage`
- `resume_recommendation`

推荐映射：
- review/final/session_probe 都存在时 → `stage = "stage3_done"`
- 若仅 worker 结果存在 → `stage = "stage2_done"`
- 若只有 task/group/pool/inspect 初始化信息 → `stage = "stage1_done"`

### 方案 B：额外输出兼容版 pipeline-state.json
保留 runtime-results.json 不变；
同时从 orchestrator 结果生成一个兼容 `schemas/pipeline-state.schema.json` 的 `pipeline-state.json`。

优点：
- 不破坏已有 smoke 输出
- staged 校验/repair/resume 可直接复用

缺点：
- 多一份收口文件，维护成本略高

## 当前更推荐的方向

优先建议 **方案 A**：

> 直接把 `runtime-results.json` 补齐到足够接近 staged pipeline 口径。

原因：
- 当前主要收口目标就是减少分叉
- `runtime-results.json` 已经是 orchestrator 的单一结果出口
- 继续额外生一份 `pipeline-state.json` 会增加双写复杂度

## 建议字段映射

### inspection_result
来源：
- `coordinator_results.inspect_agent`

### stage
建议：
- 若 `review_result`、`final_result`、`session_probe` 都存在 → `stage3_done`
- 若 `worker_a_result` 存在但无 final → `stage2_done`
- 若只有 `task_packet`、`group_plan`、`staffing`、coordinator 初始化结果 → `stage1_done`

### resume_recommendation
建议：
- stage3_done → `{ "next_stage": null, "reason": "runtime orchestrator 已完成收口" }`
- stage2_done → `{ "next_stage": "stage3", "reason": "待审核与最终汇总" }`
- stage1_done → `{ "next_stage": "stage2", "reason": "待执行 worker 阶段" }`

## 一句话结论

当前 orchestrator 的主链路已经能跑到 review/final/session_probe；
真正还差的不是“能不能跑”，而是：

> **把 inspection_result + stage + resume_recommendation 补齐，让 runtime-results 与 staged pipeline 说同一种语言。**
