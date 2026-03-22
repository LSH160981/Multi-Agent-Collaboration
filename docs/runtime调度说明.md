# runtime 调度说明

这批脚本开始把系统从“本地生成 JSON”推进到“通过 OpenClaw 原生 session / agent turn 真实调度 agent”。

## 新增脚本

- `scripts/runtime_lib.py`
- `scripts/runtime_dispatch.py`
- `scripts/runtime_orchestrator.py`
- `scripts/runtime_sessions.py`
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

## 3. runtime_sessions.py

作用：

- 默认适配当前仓库已经存在的四个角色 agent：`main-ceo` / `pool-hr` / `review-judge` / `inspect-patrol`
- 如你的环境不同，也可以通过参数覆盖这些 agent id
- 直接通过 OpenClaw 原生 `agent turn` 发起四个角色视角的真实任务
- 用来验证：本系统已经不只是“本地写 JSON”，而是确实开始接 OpenClaw 原生运行面

运行后会：

1. 解析 `/mac` 为任务包
2. 生成 A/B 编组方案
3. 分别以主Agent / AgentPool / 审核Agent / 检查Agent 的角色提示发起真实 turn
4. 把结果写入 `examples/generated/native-sessions/native-session-results.json`

## 4. inspect_and_recover.py

作用：

- 先用 `inspect_agents.py` 发现 stale / watch agent
- 再根据目录名 → OpenClaw agent id 的映射，可选执行真正的恢复唤醒消息

## 5. demo_pipeline.py

作用：

- 串起 parse → recruit → dispatch(local files) → score → dedupe
- 当前这是最稳的演示流水线，不依赖修改你现有 agent 配置

## 当前限制

当前仓库已经具备 runtime orchestration 的代码骨架，但想完全跑成“主Agent / 审核Agent / 检查Agent / AgentPool”长期自治系统，还需要继续补：

1. 会话级状态追踪
2. sessions_send / sessions_history 接口版调度器
3. 自动恢复动作和状态机联动
4. 安装后自动化验收闭环

不过现在已经跨过关键一步：

- 不再只是写本地 JSON
- 已经能用 OpenClaw 原生 agent/session 能力做真实调度 demo
