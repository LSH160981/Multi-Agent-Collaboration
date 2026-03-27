# /mac 命令桥、安装链路与使用说明

> 目标：把 `skills/mac`、默认接管安装脚本、自检、主 skill 文档与 session 参考统一串成一条可执行路径。

## 1. 组件对照

### `/mac` 命令桥
- `skills/mac/SKILL.md`

作用：提供显式的 `/mac <任务>` 入口，让用户强制进入多会话协作模式。

### 主 skill
- `skills/multi-agent-collaboration/SKILL.md`
- `skills/multi-agent-collaboration/references/guides/安装与使用.md`

作用：提供完整的方法论、默认接管、主 Agent 唯一出口、恢复与消息治理规则。

### 安装脚本
- `scripts/default-takeover-setup.sh`
- `scripts/init-mac-system.sh`

作用：把主 skill 和 `/mac` 命令桥复制到共享技能目录，并初始化 `mac-system` 工作目录。

### 自检与会话参考
- `scripts/install-selfcheck.sh`
- `docs/guides/openclaw-agent-session-commands.md`
- `scripts/runtime_sessions.py`

作用：校验安装是否完整，并说明后续如何用原生 session 能力派单、观测、恢复。

## 2. 推荐安装路径

### 安装前建议先确认的 OpenClaw 配置

至少建议满足：

- `tools.agentToAgent.enabled = true`
- `tools.agentToAgent.allow` 中包含 `main-ceo / pool-hr / review-judge / inspect-patrol` 以及你后续允许互通的 specialist
- 建议 `tools.sessions.visibility = all`
- 建议 `commands.nativeSkills = auto`，这样在支持的平台上 `/mac` 更容易显示为技能命令

可直接参考：
- `examples/openclaw.agent-to-agent.sample.json5`


### 一步安装

```bash
./scripts/default-takeover-setup.sh
```

安装后应完成：

1. `skills/multi-agent-collaboration` 被复制到共享技能目录
2. `skills/mac` 被复制到共享技能目录
3. `mac-system` 工作目录被初始化
4. 新开 session 后，主 skill 与 `/mac` 命令桥都可被读取

### 补充初始化

如需单独初始化工作目录：

```bash
./scripts/init-mac-system.sh
```

## 3. 安装后自检顺序

建议固定按下面顺序跑：

1. `./scripts/install-selfcheck.sh`
2. `python3 tests/test_agent_handshake.py`
3. `python3 tests/test_silent_task.py`
4. `python3 tests/test_runtime_orchestrator_smoke.py`
5. `python3 tests/test_recovery_pipeline_smoke.py`

## 4. 用户入口说明

### 入口 A：默认接管
安装后，复杂任务默认先由主 Agent 接住，再判断是否扩成多会话协作。

### 入口 B：显式 `/mac`

```text
/mac 调研最近 7 天 GitHub star 增长最快的 10 个项目，并总结共同特点
```

含义：
- 强制进入 Multi-Agent-Collaboration
- 允许拆解、并行、A/B、review、inspect 等内部协作
- 仍然只允许主 Agent 向用户输出最终结果

### 入口 C：纯文本兜底
如果当前平台没有显式展示技能入口，纯文本 `/mac ...` 仍应被主 skill 识别为强触发词。

## 5. 与原生 session 能力的关系

`/mac` 只是入口，不是实现本身。

真正的协作落地要依赖：
- `sessions_spawn`
- `sessions_send`
- `sessions_list`
- `sessions_history`
- `sessions_yield`

参考：
- `docs/guides/openclaw-agent-session-commands.md`
- `scripts/runtime_sessions.py`

原则：
- 先复用已有 session
- 缺角色再扩张
- 不用 shell 假装 session 原生能力

## 6. 输出纪律

无论从哪个入口进入，都必须遵守：

- 只有主 Agent 可以对用户说话
- 非主 Agent 禁止直接联系用户
- reviewer / inspect / specialist 只回传结构化结果
- `/mac` 不等于“把所有内部过程都展示给用户”
- 最终必须输出一条去重后的用户可见结论

## 7. 推荐主阅读顺序

1. `skills/mac/SKILL.md`
2. `skills/multi-agent-collaboration/SKILL.md`
3. `skills/multi-agent-collaboration/references/guides/安装与使用.md`
4. `docs/guides/openclaw-agent-session-commands.md`

## 8. 收口结论

当前仓库里，`/mac` 命令桥、默认接管安装链路、自检脚本与主 skill 文档已经形成闭环：

- `skills/mac` 负责显式入口
- `multi-agent-collaboration` 负责完整方法论
- `default-takeover-setup.sh` 负责复制与初始化
- `install-selfcheck.sh` 与测试脚本负责验收
- session 参考文档负责说明底层派单/恢复机制
