# 多会话自动测试与 session 观测矩阵

> 对应子任务：79aec0d1-8d05-4c38-970d-f3fe686f6772
> 目标：把现有 `session_probe.py`、握手测试、静默任务测试、恢复测试及 smoke 脚本统一成一套可直接执行的测试/排障矩阵。

## 1. 已具备的核心脚本

### session 观测
- `scripts/session_probe.py`
- `scripts/runtime_sessions.py`

### 自动测试
- `tests/test_agent_handshake.py`
- `tests/test_silent_task.py`
- `tests/test_runtime_orchestrator_smoke.py`
- `tests/test_recovery_pipeline_smoke.py`
- `tests/test_stage3_smoke.py`

## 2. 推荐执行顺序

### 第一层：安装后冒烟
1. `scripts/install-selfcheck.sh`
2. `tests/test_agent_handshake.py`
3. `tests/test_silent_task.py`

目标：确认技能、角色、基础多会话协作路径可用。

### 第二层：runtime 收口
4. `tests/test_runtime_orchestrator_smoke.py`
5. `tests/test_stage3_smoke.py`

目标：确认编组、派发、review、final、session_probe 等关键落盘结果存在。

### 第三层：恢复链路
6. `tests/test_recovery_pipeline_smoke.py`

目标：确认 broken state、inspect、repair、resume 这条恢复链不断。

### 第四层：排障辅助
- `scripts/session_probe.py`
- `scripts/runtime_sessions.py`

目标：当测试失败或运行期卡住时，查看最近 session、定位 stale，并根据输出的 `probe / resume / redispatch / rebuild` 建议决定下一步动作。

## 3. 各脚本职责

| 脚本 | 用途 | 典型输出 |
|---|---|---|
| `install-selfcheck.sh` | 检查技能、目录、协议、模板是否齐 | 安装完整性检查结果 |
| `test_agent_handshake.py` | 验证主Agent、审核Agent、检查Agent、AgentPool 能互认 | 角色互认结果 |
| `test_silent_task.py` | 验证静默任务不会向用户泄漏过程噪音 | 静默调研链结果 |
| `test_runtime_orchestrator_smoke.py` | 检查 task-packet/group-plan/staffing-decision/runtime-results 是否落盘 | smoke 通过/失败 |
| `test_stage3_smoke.py` | 检查 review_result / final_result / session_probe 是否落盘 | stage3 收口结果 |
| `test_recovery_pipeline_smoke.py` | 验证 inspect → repair/resume → validate 整体闭环 | 恢复 pipeline smoke 结果 |
| `session_probe.py` | 查看 agent 最近 session、时效与推荐动作 | session 观测信息（含 probe / resume / redispatch / rebuild 建议） |
| `runtime_sessions.py` | 用原生 session 方式发起多会话任务 demo | session 调度结果 |

## 4. 推荐最小验收组合

如果只想快速判断“这套多会话系统是不是还活着”，最少跑这 4 个：

1. `tests/test_agent_handshake.py`
2. `tests/test_silent_task.py`
3. `tests/test_runtime_orchestrator_smoke.py`
4. `tests/test_recovery_pipeline_smoke.py`

这 4 个分别覆盖：
- 角色互认
- 静默任务
- orchestrator 收口
- 恢复闭环

## 5. 推荐排障路径

### 场景 A：任务没跑起来
先看：
- `scripts/install-selfcheck.sh`
- `scripts/session_probe.py`

### 场景 B：worker 跑了但没收口
先看：
- `tests/test_runtime_orchestrator_smoke.py`
- `tests/test_stage3_smoke.py`
- `scripts/session_probe.py`

### 场景 C：恢复逻辑可疑
先看：
- `tests/test_recovery_pipeline_smoke.py`
- `scripts/session_probe.py`

## 6. 文档锚点

相关文档建议配套阅读：

- `scripts/README.md`
- `examples/tests/README.md`
- `docs/openclaw-agent-session-commands.md`
- `docs/runtime-orchestrator-smoke.md`
- `skills/multi-agent-collaboration/安装与使用.md`

## 7. 收口结论

当前仓库已经满足本子任务 acceptance 点名的关键项：

- `scripts/session_probe.py`
- `tests/test_agent_handshake.py`
- `tests/test_silent_task.py`
并且还补齐了：
- runtime orchestrator smoke
- stage3 smoke
- recovery pipeline smoke
- session 调度 demo

也就是说，这里已经不是“零散脚本”，而是具备 **安装后测试 → runtime 收口 → 恢复闭环 → session 排障** 的完整测试矩阵。
