# staged runtime pipeline

这一版把完整 runtime demo 拆成 3 个阶段 + 1 个恢复入口，目的是：

- 降低单次超时风险
- 中断后可以继续
- 给检查Agent明确的阶段状态
- 让恢复策略真正可落地

## 阶段

### stage1_plan.py
负责：
- 解析 `/mac`
- 生成 task-packet.json
- 生成 group-plan.json
- 调用 AgentPool 输出分工
- 调用 检查Agent 输出巡检策略
- 写入 `pipeline-state.json`

输出状态：`stage1_done`

### stage2_workers.py
负责：
- 读取 `pipeline-state.json`
- 执行 worker A
- 可选执行 worker B
- 把 worker 结果写回 state

输出状态：`stage2_done`

### stage3_review_final.py
负责：
- 审核Agent 比较 worker 结果
- 主Agent 做最终去重总结
- 附带 session_probe
- 写回 state

输出状态：`stage3_done`

### resume_pipeline.py
负责：
- 读取已有 `pipeline-state.json`
- 自动判断当前 stage
- 从中断点继续后续阶段

## 最关键的文件

- `examples/generated/staged-runtime/pipeline-state.json`

这是 staged pipeline 的单一事实源。

## 恢复意义

当流程在 stage2 或 stage3 中断时，不需要从 `/mac` 重新开始。
只要 `pipeline-state.json` 仍在，就可以从当前阶段继续。
