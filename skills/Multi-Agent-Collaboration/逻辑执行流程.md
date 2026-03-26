# Multi-Agent-Collaboration 逻辑执行流程（中文，最终版）

## 一、入口层

用户可以通过三种方式进入系统：

1. 直接提出复杂任务
2. 输入 `/mac XXX任务`
3. 明确说“使用 Multi-Agent-Collaboration skill 完成 XXX任务”

系统对入口的统一理解是：

- 复杂任务默认接管
- `/mac` 是强制进入协作模式
- 主 skill 是平台级方法论
- `mac` skill 是命令桥入口

---

## 二、主Agent 先理解，不盲目开工

主Agent 是唯一能和用户说话的角色。

它接到任务后，先做四步：

1. 判断任务是否复杂
2. 判断是否缺关键细节
3. 判断需要哪些角色与能力
4. 判断是否启用双组竞争

如果缺细节：
- 主Agent 先向用户补问
- 不允许直接让下游乱做

如果信息足够：
- 进入控制层初始化

---

## 三、控制层固定存在

系统固定控制层由四个角色构成：

- 主Agent `main-ceo`
- AgentPool `pool-hr`
- 审核Agent `review-judge`
- 检查Agent `inspect-patrol`

这四个角色不是临时拼凑，而是整个系统的常设管理层。

### 主Agent
负责：
- 理解任务
- 拆任务
- 指挥全局
- 汇总结果
- 唯一用户出口

### AgentPool
负责：
- 分析能力缺口
- 决定复用还是招聘
- 组建 A/B 组
- 写死角色边界

### 审核Agent
负责：
- 从 Reviewer / Judge / Metrics 三维审查结果
- 驳回滥竽充数结果
- 对各组打分
- 为权重系统提供依据

### 检查Agent
负责：
- 盯活性
- 查日志
- 查队列
- 查是否真在工作
- 发现 stale 就唤醒 / retry / 重派 / 重建

---

## 四、AgentPool 不是盲目扩编，而是按需招聘

系统目标不是“子 agent 越多越强”，而是：

- 缺什么，补什么
- 能复用，就复用
- 不够，再招聘
- 始终给每个角色写死边界

### 默认编组原则

- A组：稳定优先
- B组：激进优先

每组至少有：
- 一名组长 Lead
- 若干 specialist

specialist 可能包括：
- Research
- Verification
- Summary
- Implementation
- Test
- Ops

而且名字要一眼看出用途，例如：
- A组-Research
- B组-Verification
- A组长-Lead
- B组-Implementation

---

## 五、任务不是口头说说，而是结构化任务包

主Agent 把用户需求解析成标准任务包。

任务包里至少要有：
- task_id
- goal
- task_type
- complexity
- required_roles
- specialists
- output_requirements
- constraints

这一步的意义：
- 避免下游理解漂移
- 方便中断恢复
- 方便审核
- 方便后续 git 留档与复盘

---

## 六、Agent 间通信统一 JSON

所有 Agent 的内部通信都应优先走 JSON 协议。

支持三类通信：

1. 广播：所有相关 Agent 一起收到
2. 点对点：一个 Agent 发给一个 Agent
3. 共享上下文：把公共事实写入共享文件，而不是来回重复对话

通信消息类型包括：
- `task_assign`
- `task_ack`
- `task_progress`
- `task_result`
- `task_reject`
- `agent_ping`
- `agent_intro`

这样做的好处：
- 能追踪
- 能恢复
- 能审计
- 能自动化处理

---

## 七、双组竞争是默认质量上限机制

对中高复杂任务，系统默认双组竞争。

### A组：稳定策略
特点：
- 保守
- 重验证
- 重可复现
- 结果扎实

### B组：激进策略
特点：
- 更愿意探索新路径
- 更可能提出创新结构
- 风险更高，但上限也更高

这样设计的原因：
1. 防止单一路线思维固化
2. 允许横向对比
3. 给审核Agent提供可比较样本
4. 给权重系统提供真实反馈数据

---

## 八、检查Agent 不只是“监控”，而是强制活化器

检查Agent 的职责不是被动看日志，而是要确保整个系统一直在工作。

它会持续检查：
- 有没有最近动作
- 日志有没有新增
- 队列是否推进
- 有没有应该有产物却没有产物
- 有没有假装工作

如果发现异常：
1. 先发送激活消息
2. 再 retry
3. 再重派单
4. 再重建 Agent

目标不是“发现问题”，而是“把系统重新拉起来”。

---

## 九、审核Agent 用三维结构做裁决

审核Agent 会对每组结果做三维评分：

### Reviewer
检查：
- 格式完整性
- 输出项是否齐全
- 是否符合交付模板

### Judge
检查：
- 内容质量
- 推导是否可靠
- 证据是否支撑结论
- 是否跑题

### Metrics
检查：
- 可验证性
- 稳定性
- 可执行性
- 风险透明度

根据评分，可能产生这些决策：
- 通过
- 驳回重做
- 降权保留
- 提高权重
- 整组淘汰重建

---

## 十、主Agent 最后的核心工作不是“总结”，而是“消息治理”

主Agent 绝不能把内部噪音直接发给用户。

用户可见输出前必须做：
- 去重
- 合并异步回执
- 删除无效中间状态
- 删除内部噪音
- 只保留最新有效结论

这一步是整个 skill 最重要的用户体验边界。

只有这样，用户看到的才是：
- 一个出口
- 一份结论
- 一套清晰建议
而不是一堆 agent 的嘈杂回音。

---

## 十一、每个 Agent 都必须有自己的工作痕迹

每个 Agent 都需要：
- 独立记忆目录 `memory/`
- 独立日志目录 `logs/`
- 独立任务队列 `queue/`
- 能力边界文档 `abilities.md`
- 产物目录 `artifacts/`

任务队列至少记录：
- 接收了什么任务
- 做到哪一步
- 当前阻塞点
- 最近一次动作时间
- 是否完成
- 如果中断，从哪里恢复

---

## 十二、恢复逻辑必须是系统内建能力

### Specialist 挂掉
- 先读 queue 和 logs
- 能恢复就恢复
- 不能恢复就新建同角色接手

### Lead 挂掉
- 从组内 specialist 的日志和队列反推进度
- 临时改任新的组长

### Group 整体失败
- 审核Agent 记录失败原因
- AgentPool 解散低效组
- 重新招聘新组

### Review 中断
- 保留已评分条目
- 从未完成项继续

### Inspection 中断
- 优先恢复检查Agent
- 因为它关系到整套系统活性

### 主Agent 中断
- 必须先回看对用户说过什么
- 防止恢复后给用户重复发同意思的话

---

## 十三、为什么这是 OpenClaw 原生版

因为这里的 Agent 不是外部虚构 worker，而是：

- OpenClaw 原生 session
- 原生 agent identity
- 原生工具能力
- 原生上下文与日志体系

所以这个 skill 不是“模拟多 agent”，而是：

**在 OpenClaw 的原生多会话能力之上，再加一层公司化协作纪律、评分机制、巡检恢复和消息治理。**

---

## 十四、安装后的验收闭环

安装完必须做四类测试：

1. Agent 两两握手测试
2. 静默任务测试
3. stale 恢复测试
4. 原生 runtime session 调度测试

当前仓库已经具备：
- `/mac` 命令桥
- 任务包生成
- 编组方案生成
- 原生 session 调度样例
- 审核 / 巡检 / AgentPool 的真实运行样例

这说明系统已经不只是文档，而是开始进入“可运行协作系统”阶段。

---

## 十五、测试链与恢复链如何真正落地

为了避免“测试脚本存在，但必须手工先造前置文件”的假验收，当前工程推荐这样理解测试链：

### 1. runtime orchestrator smoke
- 目标：验证一轮完整 runtime orchestrator 闭环是否能落盘
- 核心产物：
  - `task-packet.json`
  - `group-plan.json`
  - `staffing-decision.json`
  - `runtime-results.json`

### 2. stage3 smoke
- 目标：验证审核 + 最终收口链路
- 现在已经支持：
  - 如果 `pipeline-state.json` 不存在
  - 自动先跑 stage1 + stage2 生成前置状态
  - 再执行 stage3
- 这样就不会再卡在“缺少前置文件”这种伪故障上

### 3. recovery smoke
- 目标：验证 pipeline-state 缺项时，能否 repair + resume
- 重点不是看结果漂不漂亮，而是看：
  - 是否能发现状态损坏
  - 是否能自动修复最小状态
  - 是否能继续推进下一阶段

### 4. silent task test
- 目标：验证协作过程中不会把中间噪音直接抛给用户
- 真正关注的是：
  - 只有主Agent 是用户出口
  - worker / reviewer / inspect 的中间回执不会直接污染用户侧

### 5. 推荐验收顺序

```text
安装完成
-> install-selfcheck
-> test_agent_handshake
-> test_silent_task
-> test_runtime_orchestrator_smoke
-> test_stage3_smoke
-> test_recovery_pipeline_smoke
-> 必要时再人工多开 TUI 观察各 agent session
```

这样做的意义是：
- 先确认角色在不在
- 再确认会不会互相说话
- 再确认不会乱对用户说话
- 再确认闭环能跑
- 再确认中断后能恢复

这才是你要的“安装完就能验收”的多 Agent 协作系统，而不是只有概念图。
