# runtime 闭环现状

这份文档用来诚实说明：当前仓库哪些已经接到 OpenClaw 原生能力，哪些还需要继续推进。

## 一、已经接上的部分

### 1. 真实 agent turn
当前 `runtime_orchestrator.py`、`runtime_dispatch.py`、`runtime_sessions.py` 都已经调用真实 OpenClaw agent turn，而不是只生成本地 JSON。

### 2. session 观测
当前已经接入：
- `openclaw sessions --json --all-agents`
- `session_probe.py`
- `runtime_lib.py` 中的 `sessions_for_agent()` / `newest_session_for_agent()`

这意味着：
- 可以看到某个角色最近有没有真实 session
- 可以获取最近 session key / updatedAt / ageMs
- 可以把这些信息用于 stale 判断和恢复提示

### 3. inspect + recover 增强
`inspect_and_recover.py` 现在已经会：
- 先看目录日志与队列
- 再结合角色映射到 agent id
- 再探测该 agent 最近 session
- 在恢复消息里附带最近 session 信息

### 4. orchestrator 结果留痕增强
`runtime_orchestrator.py` 现在除了保存各角色返回结果，还会输出：
- main / pool / review / inspect 各自最近 session 观测结果

---

## 二、还没完全接上的部分

### 1. `sessions_send` 真正点对点派单
当前仍主要是：
- 用 `openclaw agent --agent <id> --message ...`

这已经是真实 agent turn，但还不是工具层面的 `sessions_send(sessionKey=..., message=...)` 闭环。

### 2. `sessions_spawn` 真正动态招募
当前仓库里已经有“招聘 / A/B 编组 / specialist 规划”的逻辑和文档，
但还没有直接通过 OpenClaw 工具层 `sessions_spawn` 真正建立一批持久 worker 会话。

### 3. session 历史级恢复
当前恢复更多是：
- 看目录日志
- 看最近 session 元信息
- 发恢复消息

后续还应补：
- 读取目标 session 历史
- 判断最近回复是不是空转 / 跑偏 / 停滞
- 决定催办、返工、重派还是重建

---

## 三、当前阶段的正确理解

现在这个仓库已经不是“纯静态原型”，而是：
- 有真实 OpenClaw agent turn
- 有真实 session 观测
- 有测试脚本
- 有恢复链路基础版

但如果要达到你目标里的“OpenClaw 原生多会话协作系统”最终态，下一步仍需要继续推进：

1. `sessions_send` 派单
2. `sessions_spawn` 动态建组
3. session history 级恢复
4. reviewer / inspect / dedupe / final summary 完整流水线

---

## 四、结论

当前阶段最准确的描述是：

> 已经从“只会生成 JSON 的多 agent 文档系统”，推进到了“会真实调用 OpenClaw agent turn，并结合 session 状态做观测与恢复增强的半闭环系统”。

下一步要做的，就是把这个“半闭环”继续推到真正的工具级原生多会话闭环。
