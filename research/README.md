# 多 Agent 协同学习资料索引

本目录用于沉淀：
- 网页提取文本
- GitHub 仓库结构与架构观察
- ClawHub skill 方法论
- 可复用的伪代码、运行流程、通信协议、恢复策略

## 目录约定

- `web/`：网页原文提炼与学习笔记
- `github/repos/`：浅克隆下来的参考仓库
- `notes/`：按主题整理的观察笔记

## 当前重点主题

1. OpenClaw 原生 session 编排
2. 多 agent 角色分层
3. A/B 双组竞争 + reviewer 裁决
4. inspect / patrol / recover 闭环
5. JSON 任务包与 agent-to-agent 通信
6. 主Agent 唯一用户出口与去重治理
7. 自学习 / 自改进 / git 记忆压缩策略

## 已纳入的参考来源

- OpenClaw docs: Pi 集成架构
- ClawHub: Agent Team Orchestration
- ClawHub: Agent Directory
- OpenCrew
- OpenMOSS
- ClawTeam-OpenClaw
- zelikk 两篇博客

## 本轮重点提炼

### 1. OpenClaw 官方文档给出的硬边界
- OpenClaw 已经原生提供 session / tools / skill / slash command 体系。
- 所以本 skill 的正确方向不是“自己再实现一个假平台”，而是：
  - 用 skill 约束方法论
  - 用 `sessions_spawn` / `sessions_send` / `sessions_history` / `sessions_list` 串起真实协作
  - 用 `user-invocable` skill 暴露 `/mac`

### 2. ClawHub `agent-team-orchestration` 的优点
- 最小有用团队 = orchestrator + builder + reviewer
- 编排者只负责派单、追踪、汇报，不直接下场干活
- 任务状态机清晰：Inbox → Assigned → In Progress → Review → Done | Failed
- handoff 要写完整：产物、验证、问题、下一步

### 3. OpenCrew 的优点
- 用 shared protocol / workspace persona / task protocol 管理团队纪律
- 把“谁可以给谁派单”写成硬规则
- 强调 checkpoint / closeout / DoD

### 4. ClawTeam-OpenClaw 的优点
- 有可运行的 team lifecycle / mailbox / watcher / workspace git 管理骨架
- 很适合借鉴到本 skill 的：
  - mailbox / message log
  - watcher / 巡检器
  - team config 与成员边界
  - git worktree / workspace 留痕

### 5. zelikk 两篇博客给出的实战提醒
- 复杂任务要切 agent，避免上下文污染
- 先测试 agent-to-agent 通信，再开始复杂任务
- 已有团队优先 `sessions_send`，缺角色才 `sessions_spawn`
- TUI / 多 SSH 窗口观察 agent 是很好的调试方法
- 要诚实记录坑：label 误用、session 路由、交付物目录、模型跑飞

## 对本仓库的明确落地结论

1. **主Agent永远只做统筹、审核用户可见输出、去重合并**
2. **AgentPool 只负责招聘 / 复用 / 编组 / 角色边界，不直接越权联系用户**
3. **已有角色优先 `sessions_send`，缺口角色再 `sessions_spawn`**
4. **Reviewer 与 Inspect 都必须是可独立运行的 session，而不是只写在文档里**
5. **每个阶段都要有状态文件 / 队列 / 日志 / 评分卡，方便恢复**
6. **安装后必须先跑握手测试、静默任务测试、恢复测试，再进入长期使用**
7. **自学习先写入 research，再由主Agent审核后吸收进主 skill，不能自动野蛮改仓库**

> 原始资料不等于最终方案。
> 这里的目标是：提取“能落地的优点”，再改造成 OpenClaw 原生多会话版本。
