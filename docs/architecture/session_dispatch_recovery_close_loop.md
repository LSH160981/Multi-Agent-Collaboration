# session 调度闭环与恢复链增强说明

> 对应子任务：7b7bad54-9b28-4215-9be0-f9657e703b72
> 目标：把当前仓库里已经存在的 session 调度、session 探测、pipeline 恢复、runtime smoke 这些代码化能力串成一条更明确的闭环。

## 当前已具备的代码能力

### 1. session 调度
- `scripts/runtime_orchestrator.py`
- `scripts/runtime_sessions.py`
- `scripts/runtime_dispatch.py`
- `scripts/runtime_lib.py`

### 2. session 观测
- `scripts/session_probe.py`
- `runtime_lib.newest_session_for_agent()`
- `runtime_lib.probe_agents()`
- `runtime_lib.build_session_reuse_hint()`

### 3. 恢复链
- `scripts/inspect_and_recover.py`
- `scripts/repair_pipeline_state.py`
- `scripts/resume_pipeline.py`
- `scripts/validate_pipeline_state.py`
- `scripts/test_recovery_pipeline_smoke.py`

## 当前闭环已经能做到什么

1. 通过 runtime orchestrator 跑出 task/group/staffing/runtime-results
2. 把 review/final/session_probe 收进同一结果文件
3. 用 session_probe / newest_session_for_agent 看最近 session 是否存在
4. 用 inspect_and_recover 对 staged pipeline 给出 repair/resume 建议
5. 对 broken pipeline 做 repair → resume → validate 的 smoke

## 当前还不够顺的地方

### A. session 观测与 orchestrator 收口还没完全共用一套动作语义
目前：
- orchestrator 已经会写 `session_probe`
- inspect_and_recover 也会看 session / pipeline state

但两边还没有统一成一套“stale → probe → resume → re-dispatch”的明确动作链。

### B. runtime_sessions.py 更像 demo，不像恢复闭环的一环
它现在更偏展示型脚本：
- 能调起多角色
- 能落 `native-session-results.json`

但还没被纳入统一恢复链里。

### C. recover 主要盯 staged pipeline，没把 runtime-results 路径一起纳进来
当前 inspect_and_recover 更偏：
- 检查 staged runtime 的 `pipeline-state.json`

但 orchestrator 侧现在更多产物是：
- `runtime-results.json`

这两条线还没有完全打通。

## 建议增强方向

### 方向 1：统一“session 调度状态”最小语义
建议后续统一成下面 4 个动作：

1. `probe`：查看 agent 最近 session 与 age
2. `resume`：若已有 session，优先继续该 session
3. `redispatch`：若 session 不可用，重新下发任务
4. `rebuild`：若状态损坏或长期 stale，重建链路

### 方向 2：让 inspect_and_recover 认识 runtime-results.json
除了 staged pipeline 之外，还应支持：
- 检查 `runtime-results.json` 的 `status`
- 检查 `stage`
- 检查 `review_result` / `final_result` / `session_probe`
- 如果缺 `inspection_result` / `resume_recommendation` / `stage`，直接给出精确修复建议

### 方向 3：把 session 级恢复提示复用到 orchestrator 路径
当前 `build_recovery_message()` 已经可生成恢复提示。
建议后续把它用于：
- stale worker
- stale review agent
- stale inspect agent
- stale main/pool 协调者

## 本轮已经落地的代码化进展

截至当前，这条子任务已经不只是方向说明，而是有实际代码落点：

1. `scripts/session_probe.py` 已新增：
   - `--stale-minutes`
   - `age_minutes`
   - `recommended_action`
2. `recommended_action` 已统一输出为：
   - `probe`
   - `resume`
   - `redispatch`
   - `rebuild`
3. `docs/testing/session_probe_and_test_matrix.md` 与 `scripts/README.md` 已同步更新，确保文档和脚本输出一致。
4. 已做最小行为验证，确认：
   - `action_legend` 实际存在
   - session 条目里实际存在 `age_minutes` / `recommended_action`

## 当前阶段结论

这条子任务当前最现实的推进方式，不是重新发明一套新系统，而是：

> **把 runtime_orchestrator、runtime_sessions、session_probe、inspect_and_recover 这四块已有代码，逐步拉到同一套 session 调度/恢复动作语义上。**

## 一句话总结

当前仓库已经有 session 调度、session 观测、pipeline 恢复、runtime smoke 四块代码基础；
当前这轮已经先把 `session_probe.py` 推进成真正输出恢复动作建议的脚本。
下一步真正要补的是：

> **让这些动作建议被 inspect / runtime / recover 脚本进一步复用起来，变成完整闭环。**
