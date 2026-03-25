# ENTRYPOINTS

本文件定义当前仓库的正式入口矩阵，避免多个脚本都像“主入口”。

## 正式保留入口

### 1. 用户入口
- `skills/Multi-Agent-Collaboration/SKILL.md`
- `skills/mac/SKILL.md`

### 2. 安装入口
- `scripts/default-takeover-setup.sh`
- `scripts/install-selfcheck.sh`
- `scripts/init-mac-system.sh`

### 3. 任务入口
- `scripts/mac_cli.py`

### 4. staged pipeline 主入口
- `scripts/run_staged_pipeline.py`

### 5. runtime 主入口
- `scripts/runtime_orchestrator.py`
- `scripts/runtime_sessions.py`

### 6. 恢复与巡检入口
- `scripts/inspect_and_recover.py`
- `scripts/session_probe.py`

### 7. 测试入口
- `scripts/test_agent_handshake.py`
- `scripts/test_silent_task.py`
- `scripts/test_runtime_orchestrator_smoke.py`
- `scripts/test_recovery_pipeline_smoke.py`

## 辅助脚本

这些脚本保留，但不是面向最终用户的主入口：
- `scripts/protocol_lib.py`
- `scripts/runtime_lib.py`
- `scripts/recruit_team.py`
- `scripts/staffing_decision.py`
- `scripts/stage1_plan.py`
- `scripts/stage2_workers.py`
- `scripts/stage3_review_final.py`
- `scripts/dispatch_task.py`
- `scripts/runtime_dispatch.py`
- `scripts/inspect_agents.py`
- `scripts/repair_pipeline_state.py`
- `scripts/resume_pipeline.py`
- `scripts/validate_examples.py`
- `scripts/validate_pipeline_state.py`

## 已删除的重复旧入口

- `scripts/orchestrate_task.py`
- `scripts/demo_pipeline.py`
- `scripts/generate-log-samples.py`

删除原因：
- 与现有主链路重复
- 增加理解成本
- 不符合“正式入口少而清晰”的工程要求
