# OpenClaw Agent Session / 多会话能力参考

这份文件专门给 **Multi-Agent-Collaboration** 使用。
目标：把“OpenClaw 原生多会话协作”真正落到 session / spawn / send / history / slash commands 上。

## 一、工具层：真正可调用的多会话能力

### 1. `sessions_spawn`
用途：创建隔离会话或持久会话，是最核心的多 agent 调度能力。

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

### 2. `sessions_send`
用途：给已有内部会话继续发指令，形成真正的 agent-to-agent 调度链。

适合：
- 追加约束
- 纠偏
- 催办
- 要求返工
- 传递 reviewer 反馈

### 3. `sessions_list`
用途：按需查看当前可见会话。

适合：
- 查 session 是否存在
- 查 label / sessionKey
- 排查是否起多了、绑错了、跑飞了

### 4. `sessions_history`
用途：读取目标 session 历史。

适合：
- 审核 agent 是否真的在工作
- 检查 stale / 卡住 / 跑偏
- 恢复中断任务时回放上下文

### 5. `sessions_yield`
用途：当前回合先结束，等待子会话完成后由系统推送结果回来。

适合：
- 多个后台任务已发起
- 当前无需继续占着前台轮询

## 二、用户侧 slash commands / TUI 命令参考

### Core
- `/help`
- `/status`
- `/agent <id>` / `/agents`
- `/session <key>` / `/sessions`
- `/model <provider/model>` / `/models`

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
- `/agents`
- `/session idle <duration|off>`
- `/session max-age <duration|off>`

## 三、对本 skill 的落地建议

### 1. 主Agent 只做三件事
1. 分析任务
2. 调度 session
3. 合并后对用户输出唯一结论

### 2. AgentPool 不要伪造 agent
AgentPool 的本质应该是：
- 判断缺什么角色
- 决定要不要新建 session
- 决定新 session 的 prompt / task packet / 边界

### 3. Reviewer / Inspect 也应是 session
不要只把 reviewer / inspect 写成文档角色。
它们都应该是：
- 可被 `sessions_spawn` 建立的独立会话
- 可被 `sessions_send` 纠偏的独立执行单元

### 4. 检查/恢复链要真正闭环
最小闭环：
1. `sessions_list` 找目标
2. `sessions_history` 看最近产出
3. 判定 stale
4. `sessions_send` 发恢复动作
5. 必要时重新 `sessions_spawn`

## 四、推荐默认拓扑

### 最小团队
- 主Agent CEO
- specialist-1
- reviewer

### 标准团队
- 主Agent CEO
- AgentPool / HR
- 稳健组长 + 2 specialist
- 激进组长 + 2 specialist
- 审核Agent
- 检查Agent

### 极简原则
- 能不用 reviewer 就不用 reviewer
- 能不用 inspect 常驻就按需启动
- 能单组完成就不强行双组
- 只有质量、可靠性、交叉验证价值足够高时才上 A/B 竞争

## 五、中文伪代码（简版）

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

## 六、结论

要把 **Multi-Agent-Collaboration** 做成真正的 OpenClaw 原生多会话系统，关键不是“写很多角色名”，而是把：

- `sessions_spawn`
- `sessions_send`
- `sessions_list`
- `sessions_history`
- `sessions_yield`

真正串成一条稳定可恢复的运行链。
