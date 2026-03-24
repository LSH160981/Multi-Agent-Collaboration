# pipeline-state schema 说明

本文件定义 staged runtime 的单一事实源：`pipeline-state.json`。

## 位置

- schema: `schemas/pipeline-state.schema.json`
- 校验脚本: `scripts/validate_pipeline_state.py`
- 修复脚本: `scripts/repair_pipeline_state.py`

## 基础字段

必需：
- `stage`
- `task_packet`

### stage 枚举
- `stage1_done`
- `stage2_done`
- `stage3_done`

## 分阶段必需字段

### stage1_done
- `group_plan`
- `pool_result`
- `inspect_result`
- `worker_role`

### stage2_done
- `worker_agent_a`
- `worker_a_result`

### stage3_done
- `review_result`
- `final_result`
- `session_probe`

## 修复原则

如果 stage 存在但关键字段缺失：
- 优先重跑当前阶段脚本
- 若 stage 非法或 task_packet 缺失，则先运行 repair 脚本补最小字段

## inspect 自动恢复

`inspect_and_recover.py` 现在支持：
- 识别 pipeline-state 缺字段
- 给出 `precise_action`
- 给出 `repair_action`
- 可选 `--auto-resume-pipeline`
- 可选 `--auto-repair-pipeline`
- 输出 `valid_before / missing_before`
- 自动恢复后输出 `validation_after_repair / validation_after_resume / state_after_resume`
