# Openclaw 命令行 TUI 中使用多 Agent 协同完成任务 — 学习摘录

来源：<https://zelikk.blogspot.com/2026/03/openclaw-tui-agent-cooperate.html>

## 关键点

- 多 Agent 团队应优先基于已有 agent/session 通信，不必强依赖 subagent
- A2A 通信推荐 `sessions_send(sessionKey=..., timeoutSeconds=0)`，不要等待同步阻塞式回包
- 真实环境中，通信是否成功必须做专门测试，不要一上来就跑复杂任务
- 用多个 TUI 观察不同 agent 的 session，有助于理解协同过程
- `label` 路由容易出问题，`sessionKey` 更稳
- 交付物应放到清晰统一的交付目录，而不是混在工作区里

## 对本 skill 的启发

- 安装后必须内置 **Agent 两两互发握手测试**
- 安装后必须内置 **静默任务测试**
- 所有 A2A 通信优先采用 `sessionKey`
- 通信要异步化，避免主 Agent 被阻塞
