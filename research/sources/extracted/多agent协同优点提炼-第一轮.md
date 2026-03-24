# 多 Agent 协同优点提炼（第一轮）

## 一、来自 OpenClaw 文档（Pi 集成架构）的关键启发

来源：`https://docs.openclaw.ai/zh-CN/pi`

### 可直接吸收的点

1. **OpenClaw 本身就是嵌入式 session runtime**
   - 不是简单“开子进程”
   - 而是围绕 session 生命周期、事件、工具、历史、压缩、模型切换构建
   - 这意味着我们的 skill 应该围绕 session 编排，而不是自己发明第二套 runtime

2. **工具注入 / 系统提示 / 会话持久化都已经是现成能力**
   - 我们不需要再造底层框架
   - 应把精力放在：任务包协议、角色分工、调度、恢复、审核

3. **会话事件是核心观测点**
   - turn_start / turn_end
   - tool_execution_start / end
   - auto_compaction
   - 这给“检查Agent / 质量巡检 / 超时恢复”留下了天然接口思路

### 对本 skill 的改造价值

- 把“检查Agent 看日志”升级为“检查 session 状态 + 历史 + 最近产出”
- 把“平台级默认接管”理解为：主Agent 优先使用当前 skill 方法论，而不是接管底层 runtime

---

## 二、来自 ClawHub《Agent Team Orchestration》的关键启发

来源：`https://clawhub.ai/arminnaimi/agent-team-orchestration`

### 核心骨架

最小有用团队：
- orchestrator
- builder
- reviewer

### 可直接吸收的点

1. **先做最小 2~3 agent 团队，再扩展**
   - 不是一上来就铺满角色
   - 先能跑通：编排 → 产出 → 审查 → 交付

2. **任务状态必须明确**
   - Inbox → Assigned → In Progress → Review → Done | Failed
   - 状态迁移要有注释：谁做的、为什么、下一步是什么

3. **handoff 必须结构化**
   - 做了什么
   - 产物在哪
   - 怎么验证
   - 已知问题
   - 下一步做什么

4. **编排者不能亲自下场干执行**
   - 编排者一旦“顺手做一点”，整体视野就丢了

### 对本 skill 的改造价值

- 主Agent 只保留：分析 / 派发 / 汇总 / 对外输出
- specialist / reviewer 的 handoff 模板必须固定化
- 每个队列文档都应该记录状态流转

---

## 三、来自 ClawTeam-OpenClaw 的关键启发

来源：`research/sources/raw/github/ClawTeam-OpenClaw`

### 可直接吸收的点

1. **任务板 + inbox + 生命周期 是协作底座**
2. **锁、等待、阻塞、解阻塞** 是成熟多 agent 系统的关键
3. **消息与任务不要混为一谈**
   - message 是沟通
   - task 是状态机
4. **idle / watcher / mailbox** 这些机制很值得借鉴

### 对本 skill 的改造价值

- 把“agent 通信 JSON”与“任务状态 JSON”分开
- 增加任务等待、阻塞、恢复的明确定义
- 检查Agent 不只是催促，还要维护状态正确性

---

## 四、来自 OpenCrew 的关键启发

来源：`research/sources/raw/github/opencrew`

### 可直接吸收的点

1. **A2A 两步触发非常务实**
   - 可见锚点
   - 真正触发靠 sessions_send

2. **shared 协议文件非常重要**
   - workflow
   - task protocol
   - closeout
   - self-update
   - review protocol

3. **用户可见消息与内部回执必须分层**
   - 内部产出给上游 agent
   - 用户/审计留痕给 thread / 可见面

### 对本 skill 的改造价值

- 我们的 JSON 协议与任务包已经有基础，下一步要补成“可直接丢给 sessions_send 的稳定结构”
- 主Agent 去重和异步回执合并，必须成为硬规则

---

## 五、来自 OpenMOSS 的关键启发

来源：`research/sources/raw/github/OpenMOSS`

### 可直接吸收的点

1. **planner / executor / reviewer / patrol 这套四角闭环很强**
2. **积分、审查、返工、巡检形成持续改进机制**
3. **任务系统明确、适合长期运行**

### 对本 skill 的改造价值

- 保留其优点，但转译为 OpenClaw session 版本：
  - planner → 主Agent / AgentPool
  - executor → specialists
  - reviewer → 审核Agent
  - patrol → 检查Agent

---

## 六、建议沉淀成最终骨架的部分

### 推荐骨架
1. 主Agent CEO
2. AgentPool / HR
3. 稳健组长 + 稳健 specialists
4. 激进组长 + 激进 specialists
5. 审核Agent（Reviewer/Judge/Metrics）
6. 检查Agent（heartbeat / stale / recover）

### 强制规则
- 主Agent 是唯一用户出口
- 所有内部 agent 只能用 JSON 通信
- 每个 agent 都要有 queue / logs / memory / capability 文件
- 每个任务都有状态机与 handoff 文档
- 中断恢复必须依赖 session 历史 + 队列，而不是纯靠记忆

---

## 七、下一步该补的代码点

1. 把 dispatch 彻底接到 `sessions_send`
2. 把 recruit 接到 `sessions_spawn`
3. 把 inspect 接到 `sessions_list + sessions_history`
4. 把 score / dedupe / review 串成完整 demo pipeline
5. 增加 `/mac` 命令桥 skill 的安装链路
6. 增加静默测试与 agent 两两握手测试模板
