# Agent Team Orchestration — 学习摘录

来源：<https://clawhub.ai/arminnaimi/agent-team-orchestration>

## 关键观点

- 最小可用团队 = Orchestrator + Builder
- 更稳的闭环 = Builder 产出后必须进入 Reviewer
- 任务状态机清晰：Inbox → Assigned → In Progress → Review → Done | Failed
- 状态流转由编排者掌控，不把状态更新责任完全丢给执行 Agent
- handoff 必须标准化：做了什么、产物在哪、如何验证、已知问题、下一步是什么

## 可借鉴点

1. **角色单一职责**
   - 编排者负责分配/跟踪
   - 执行者负责产出
   - 审核者负责反驳和把关

2. **状态机先于自由发挥**
   - 多 Agent 容易“都在工作，但没人知道进行到哪”
   - 用任务状态机强制把自由协作落到可审计状态

3. **交接包标准化**
   - 坏交接：Done, check files.
   - 好交接：位置、验证、风险、下一步都明确

## 对本 skill 的启发

- 我们要把“任务队列文档”做成核心，不是附属品
- 我们的主 Agent 不负责直接干活，而负责：理解任务、招聘、派单、汇总、去重、对用户输出
- 每个 Agent 的汇报都应当是结构化 JSON + Markdown 双份
