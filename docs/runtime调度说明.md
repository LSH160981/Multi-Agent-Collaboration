# runtime 调度说明

这批脚本开始把系统从“本地生成 JSON”推进到“通过 OpenClaw CLI 真实调度 agent”。

## 新增脚本

- `scripts/runtime_lib.py`
- `scripts/runtime_dispatch.py`
- `scripts/runtime_orchestrator.py`
- `scripts/inspect_and_recover.py`
- `scripts/demo_pipeline.py`

## 1. runtime_dispatch.py

作用：

- 读取结构化任务 JSON
- 通过 `openclaw agent --agent <id> --message ... --json` 真正把任务发给一个 OpenClaw agent

## 2. runtime_orchestrator.py

作用：

- 先用 `mac_cli.py` 解析任务
- 再用 `recruit_team.py` 生成 A/B 组计划
- 然后分别向主Agent / AgentPool / 审核Agent / 检查Agent 对应的 OpenClaw agent id 发消息

注意：

- 这里的 `--main-agent` / `--pool-agent` / `--review-agent` / `--inspect-agent` 需要传入真实存在的 OpenClaw agent id
- 例如当前系统里可见的 agent id 有：`smart` / `speed` / `text`

## 3. inspect_and_recover.py

作用：

- 先用 `inspect_agents.py` 发现 stale / watch agent
- 再根据目录名 → OpenClaw agent id 的映射，可选执行真正的恢复唤醒消息

## 4. demo_pipeline.py

作用：

- 串起 parse → recruit → dispatch(local files) → score → dedupe
- 当前这是最稳的演示流水线，不依赖修改你现有 agent 配置

## 当前限制

当前仓库已经具备 runtime orchestration 的代码骨架，但想完全跑成“主Agent / 审核Agent / 检查Agent / AgentPool”真实调度，还需要你本机先真正创建并绑定这些 OpenClaw agent。
