# runtime 调度说明

这份文件只讲 **运行时脚本边界与当前定位**，不再重复 staged pipeline 的详细阶段说明。

## 当前核心脚本

### 正式入口
- `scripts/runtime_orchestrator.py`
- `scripts/run_staged_pipeline.py`
- `scripts/inspect_and_recover.py`

### 辅助 / 子阶段脚本
- `scripts/runtime_lib.py`
- `scripts/runtime_dispatch.py`
- `scripts/stage1_plan.py`
- `scripts/stage2_workers.py`
- `scripts/stage3_review_final.py`
- `scripts/resume_pipeline.py`

### demo / 验收型脚本
- `scripts/runtime_sessions.py`

> `runtime_sessions.py` 仍应视为 **原生 session 风格 demo / 验收脚本**，而不是长期生产调度主入口。

---

## 1. runtime_dispatch.py

作用：
- 读取结构化任务 JSON
- 通过 `openclaw agent --agent <id> --message ... --json` 向 agent 发任务

定位：
- 底层派发辅助
- 不是最终用户入口

## 2. runtime_orchestrator.py

作用：
- 用 `mac_cli.py` 解析任务
- 用 `recruit_team.py` 生成 A/B 组计划
- 向主Agent / AgentPool / 审核Agent / 检查Agent / worker 发出真实 turn
- 把收口结果写入 `runtime-results.json`

定位：
- 当前推荐的 runtime 主入口
- 面向 smoke / 验收 / 真实运行链实验

## 3. run_staged_pipeline.py

作用：
- 统一驱动 stage1 → stage2 → stage3
- 支持 stop-after / resume / repair 相关链路
- 输出稳定的 `pipeline-state.json`

定位：
- 当前推荐的 staged pipeline 主入口
- 更适合恢复、阶段排障、可恢复执行

## 4. inspect_and_recover.py

作用：
- 巡检 stale / watch agent
- 结合 pipeline-state 给出 repair / resume / rebuild 建议
- 当前已能给出明确 `rebuild_agent.py` 调用命令

定位：
- 巡检与恢复入口
- 不负责完整业务编排

## 5. runtime_sessions.py

作用：
- 以主Agent / AgentPool / 审核Agent / 检查Agent 视角发起一轮真实 task demo
- 写出 native-session-results.json 供人工审计和示例验证

定位：
- demo / 示例 / 验收脚本
- 适合验证“已经接上 OpenClaw 原生 agent/session 能力”
- 不应被描述为长期自治调度器

---

## 当前限制

当前仓库已经具备 runtime orchestration 的代码骨架，但还没有把以下部分做成平台原生长期自治系统：

1. 会话级状态追踪
2. `sessions_send` / `sessions_history` 接口版调度器
3. 自动恢复动作和状态机联动
4. 完整的长期守护 / 定时自学习执行器

也就是说：

- 现在已经不是“只写本地 JSON”
- 已经能用 OpenClaw 原生 agent/session 能力跑真实调度 demo
- 但 **正式主入口** 与 **demo / 适配层** 仍要明确区分

---

## 建议阅读顺序

- 看 runtime 与 staged 的差异：`runtime_orchestrator_vs_pipeline_gap.md`
- 看 staged pipeline 本身：`staged-runtime-pipeline.md`
- 看伪代码与实现映射：`伪代码到代码映射.md`
