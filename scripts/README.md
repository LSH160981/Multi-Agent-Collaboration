# scripts

本目录按工程职责可以分成 5 类。

## 1. 安装与初始化
- `default-takeover-setup.sh`：把 skill 安装到共享目录并初始化默认接管基础环境
- `install-selfcheck.sh`：安装后自检
- `init-mac-system.sh`：初始化 `mac-system/` 多 Agent 工作目录
- `generate-agent.sh`：快速生成一个新的 Agent 目录骨架
- `generate-ab-team.sh`：批量生成 A/B 两组 specialist 骨架

## 2. 协议与任务解析
- `mac_cli.py`：把 `/mac` 文本解析成结构化任务包
- `protocol_lib.py`：读取协议定义并构造标准 JSON 消息
- `recruit_team.py`：根据任务包生成 A/B 组编组方案
- `staffing_decision.py`：把编组结果收口为 staffing 决策
- `dispatch_task.py`：把结构化派单写入日志与队列
- `score_result.py`：把结果包转成评分卡
- `dedupe_summary.py`：对候选结论做去重汇总

## 3. runtime / session / 恢复
- `runtime_lib.py`：OpenClaw runtime 调度辅助库
- `runtime_dispatch.py`：通过 OpenClaw CLI 向 agent 发结构化任务
- `runtime_orchestrator.py`：更完整的一轮 runtime 闭环
- `runtime_sessions.py`：原生 session 风格 demo
- `full_runtime_demo.py`：主Agent / AgentPool / Worker / 审核 / 检查 五段式 demo
- `inspect_agents.py`：巡检 Agent 目录状态
- `inspect_and_recover.py`：巡检并执行恢复动作
- `session_probe.py`：探测当前 OpenClaw sessions，辅助排障与恢复
- `repair_pipeline_state.py`：修复最小 pipeline state
- `resume_pipeline.py`：继续推进已有 pipeline
- `run_staged_pipeline.py`：统一入口，串起 stage1 → stage2 → stage3

## 4. 分阶段 pipeline 原型
- `stage1_plan.py`
- `stage2_workers.py`
- `stage3_review_final.py`
- `run_staged_pipeline.py`

> 已删除早期重复原型：`orchestrate_task.py`、`demo_pipeline.py`。
> 原因：它们已被 staged pipeline 与 runtime orchestrator 覆盖，继续保留只会制造入口混乱。

## 5. 校验与测试
- `validate_pipeline_state.py`
- `validate_examples.py`
- `generate-log-samples.py`
- `test_agent_handshake.py`
- `test_silent_task.py`
- `test_runtime_orchestrator_smoke.py`
- `test_recovery_pipeline_smoke.py`
- `test_recovery_loop.py`
- `test_stage3_smoke.py`

## 维护原则
- 新脚本必须写模块说明。
- 能复用公共逻辑时，优先放进 `runtime_lib.py` / `protocol_lib.py`。
- demo、smoke、生产型总控不要混名混责。
- 如果两个脚本功能高度重合，优先合并或在此文件写清边界。
