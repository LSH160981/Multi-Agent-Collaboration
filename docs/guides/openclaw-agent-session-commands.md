# OpenClaw Agent / Session / 多会话命令参考

这份文件专门给 **Multi-Agent-Collaboration** 使用。
目标：把“OpenClaw 原生多会话协作”真正落到 **agent / agents / sessions / tui / acp / session tools** 上。

---

## 一、先分清三层

### 1. 平台内工具层（给 agent 调用）
这些是主 skill 真正依赖的核心能力：

- `sessions_spawn`
- `sessions_send`
- `sessions_list`
- `sessions_history`
- `sessions_yield`

这 5 个才是 **OpenClaw 原生多会话协作** 的主心骨。

### 2. CLI 层（给人排障/查看/演示）
这些命令适合人工安装、自检、排障、TUI 使用：

- `openclaw help`
- `openclaw status`
- `openclaw agent --help`
- `openclaw agents --help`
- `openclaw sessions --help`
- `openclaw tui --help`
- `openclaw acp --help`
- `openclaw gateway --help`

### 3. TUI slash commands 层（给用户和操作者）
这些是 TUI 里常见、最有价值的命令：

- `/help`
- `/status`
- `/agent`
- `/agents`
- `/session`
- `/sessions`
- `/reset`
- `/abort`
- `/think`
- `/model`
- `/subagents ...`

> 结论：**skill 运行靠工具层，人工理解与验收靠 CLI / TUI 层。不要把 CLI 适配层误写成平台能力本身。**

---

## 二、工具层：真正可调用的多会话能力

## 1. `sessions_spawn`

用途：创建隔离会话或持久会话，是最核心的多 Agent 调度能力。

常用参数：
- `runtime: "subagent" | "acp"`
- `mode: "run" | "session"`
- `thread: true | false`
- `label`
- `task`
- `agentId`
- `model`
- `thinking`
- `runTimeoutSeconds`
- `cleanup: "keep" | "delete"`

建议：
- 一次性后台工作：`mode: "run"`
- 需要持续接收补充指令：`thread: true` + `mode: "session"`
- 如果用户明确要 codex / claude code / gemini：使用 `runtime: "acp"`

### 在本 skill 中的定位

```text
主Agent 判断需要新角色
-> AgentPool 决定创建哪类 session
-> 用 sessions_spawn 创建 reviewer / verifier / debugger / researcher 等内部会话
```

---

## 2. `sessions_send`

用途：给已有内部会话继续发指令，形成真正的 agent-to-agent 调度链。

适合：
- 追加约束
- 纠偏
- 催办
- 要求返工
- 传递 reviewer 反馈
- 恢复时二次激活

### 在本 skill 中的定位

```text
worker 跑偏
-> review / inspect 发现问题
-> 主Agent 或检查Agent 用 sessions_send 补发纠偏消息
```

---

## 3. `sessions_list`

用途：按需查看当前可见会话。

适合：
- 查 session 是否存在
- 查 label / sessionKey
- 排查是否起多了、绑错了、跑飞了
- 查看近期活跃会话

### 在本 skill 中的定位

```text
恢复前先看：目标 session 还在不在、最近有没有活性、是不是已经存在更合适的可复用会话
```

---

## 4. `sessions_history`

用途：读取目标 session 历史。

适合：
- 审核 agent 是否真的在工作
- 检查 stale / 卡住 / 跑偏
- 恢复中断任务时回放上下文
- 看是否已经产出过可复用结果

### 在本 skill 中的定位

```text
检查Agent 读取最近历史
-> 判断是“真卡住”还是“只是慢”
-> 决定 retry / redispatch / rebuild
```

---

## 5. `sessions_yield`

用途：当前回合先结束，等待子会话完成后由系统推送结果回来。

适合：
- 多个后台任务已发起
- 当前无需继续占着前台轮询
- 明确想走推送式收尾

### 在本 skill 中的定位

```text
主Agent 已完成派单
-> 当前无需继续等待
-> sessions_yield 交还前台，等子任务完成再收口
```

---

## 三、CLI 层：安装、自检、排障时最有用的真实命令

## 1. `openclaw help`

用途：看全局命令树。

本轮实测可见的重点子命令包括：
- `agent`
- `agents`
- `sessions`
- `gateway`
- `status`
- `tui`
- `acp`
- `skills`
- `message`
- `cron`

---

## 2. `openclaw status`

用途：看整体运行状态。

本轮实测可以直接看到：
- Gateway 是否正常
- 默认 agent
- 当前 agents 数量
- sessions 数量
- heartbeat 配置
- 安全告警
- 最近活跃会话

### 推荐场景
- 安装后总览
- 排查默认 agent 是否正确
- 看 review / inspect / pool / worker 是否都在线

---

## 3. `openclaw agent --help`

用途：**人工触发一个 agent turn**。

本轮实测关键参数：
- `--agent <id>`：指定 agent id
- `--message <text>`：消息体
- `--json`：机器可读输出
- `--timeout <seconds>`：超时
- `--thinking <level>`：思考级别
- `--deliver`：把回复发回渠道
- `--session-id <id>`：指定 session

### 推荐场景
- 手动烟测某个 agent
- 用脚本做握手测试
- 在没有直接 tool 调度时做演示适配

> 注意：它是 CLI 入口，不等于 skill 内部真正的多会话编排能力。

---

## 4. `openclaw agents --help`

用途：管理隔离 agents。

本轮实测子命令：
- `add`
- `bind`
- `bindings`
- `delete`
- `list`
- `set-identity`
- `unbind`

### 这对本 skill 的意义
- 可以作为安装后创建/管理 agent 的辅助命令
- 有助于让 `main-ceo / pool-hr / review-judge / inspect-patrol` 形成固定身份

---

## 5. `openclaw sessions --help`

用途：查看存储的会话列表。

本轮实测关键参数：
- `--active <minutes>`
- `--agent <id>`
- `--all-agents`
- `--json`
- `--store <path>`
- `cleanup`

### 推荐场景
- 查看最近活跃会话
- 核查某 agent 是否已经有主会话
- 查看 session 是否过多、过旧、需要清理

---

## 6. `openclaw tui --help`

用途：打开 TUI。

本轮实测关键参数：
- `--session <key>`
- `--message <text>`
- `--thinking <level>`
- `--deliver`
- `--timeout-ms <ms>`

### 对本 skill 的价值
- 方便人工切换不同 agent / session 看协作过程
- 适合验收通信、观察 leader / reviewer / inspector 的行为

---

## 7. `openclaw acp --help`

用途：对接 ACP bridge。

关键参数：
- `--session <key>`
- `--session-label <label>`
- `--require-existing`
- `--reset-session`
- `client`

### 对本 skill 的价值
- 当用户说“用 codex / claude code / gemini 干这个”时，说明 ACP 会话接入点在这里
- 这类需求应由 `sessions_spawn(runtime="acp")` 落地，而不是乱走 PTY 自造流程

---

## 四、TUI 常见 slash commands（适合安装后实际使用）

### Core
- `/help`
- `/status`
- `/agent <id>`
- `/agents`
- `/session <key>`
- `/sessions`
- `/model <provider/model>`
- `/models`

### Session controls
- `/think <off|minimal|low|medium|high>`
- `/fast <status|on|off>`
- `/verbose <on|full|off>`
- `/reasoning <on|off|stream>`
- `/usage <off|tokens|full>`
- `/elevated <on|off|ask|full>`
- `/activation <mention|always>`
- `/deliver <on|off>`

### Session lifecycle
- `/new`
- `/reset`
- `/abort`
- `/settings`
- `/exit`

### 与 subagents / thread binding 相关
- `/subagents list`
- `/subagents kill <id|#|all>`
- `/subagents log <id|#>`
- `/subagents info <id|#>`
- `/subagents send <id|#> <message>`
- `/subagents steer <id|#> <message>`
- `/subagents spawn <agentId> <task>`
- `/focus <target>`
- `/unfocus`
- `/session idle <duration|off>`
- `/session max-age <duration|off>`

### 特别提醒
- 做多 agent 协作时，**先少用 `/new`**，避免意外新建 session 把通信链路搞乱
- 更稳的是：固定 agent 身份 + 固定主 session + 明确用工具层调度

---

## 五、对本 skill 的落地建议

## 1. 主Agent 只做三件事
1. 分析任务
2. 调度 session
3. 合并后对用户输出唯一结论

不要让主Agent下场充当普通 worker。

---

## 2. AgentPool 不要伪造 agent

AgentPool 的本质应该是：
- 判断缺什么角色
- 决定要不要新建 session
- 决定新 session 的 prompt / task packet / 边界
- 决定复用谁、淘汰谁、重建谁

不是只在文档里写“它会招聘”。

---

## 3. Reviewer / Inspect 也应是 session

不要只把 reviewer / inspect 写成文档角色。
它们都应该是：
- 可被 `sessions_spawn` 建立的独立会话
- 可被 `sessions_send` 纠偏的独立执行单元
- 可被 `sessions_history` 审核的独立对象

---

## 4. 检查 / 恢复链要真正闭环

最小闭环：
1. `sessions_list` 找目标
2. `sessions_history` 看最近产出
3. 判定 stale
4. `sessions_send` 发恢复动作
5. 必要时重新 `sessions_spawn`
6. 主Agent 最终做去重与收口

---

## 六、安装后推荐人工验收顺序

```text
1. openclaw status
   看 agent/sessions/heartbeat 是否正常

2. openclaw agents list（或在平台里确认已有 agent）
   看 main-ceo / pool-hr / review-judge / inspect-patrol 是否存在

3. ./scripts/test_agent_handshake.py
   测核心控制层会不会互相识别

4. 用 TUI 的 /agent 切到不同 agent 看 session
   必要时多开几个 SSH/TUI 窗口观察

5. ./scripts/test_silent_task.py
   看静默任务时是否有中间噪音泄漏

6. ./scripts/test_runtime_orchestrator_smoke.py
   看落盘与收口是否完整

7. ./scripts/test_recovery_pipeline_smoke.py
   看恢复链是否断
```

---

## 七、中文伪代码（简版）

```text
当用户发来任务：
  如果任务简单：
    主Agent 单会话完成
    输出结果
    结束

  如果任务复杂或用户写了 /mac：
    主Agent 生成任务包
    AgentPool 判断缺少哪些角色
    按需 sessions_spawn 创建多个内部 session
    向每个 session 下发 JSON 任务包

    如果需要竞争：
      创建 稳健组 与 激进组
      两组并行产出

    如果需要审核：
      sessions_spawn reviewer
      汇总两组结果交给 reviewer 打分

    如果发现某 session 长时间无产出：
      sessions_history 查看最近状态
      sessions_send 催办 / 纠偏 / 要求返工
      必要时重建 session

    主Agent 最后统一去重、合并、压缩噪音
    仅由主Agent向用户输出
```

---

## 八、结论

要把 **Multi-Agent-Collaboration** 做成真正的 OpenClaw 原生多会话系统，关键不是“写很多角色名”，而是把：

- `sessions_spawn`
- `sessions_send`
- `sessions_list`
- `sessions_history`
- `sessions_yield`

真正串成一条稳定、可恢复、可审计、可验收的运行链。

CLI / TUI 命令的价值，是帮助安装、调试、验收与观察；
**真正的平台原生协作能力，仍然应该以 session tools 为中心。**
