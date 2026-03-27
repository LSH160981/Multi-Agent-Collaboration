# Openclaw 命令行 TUI 中 使用多 Agent 协同完成任务

来源: https://zelikk.blogspot.com/2026/03/openclaw-tui-agent-cooperate.html
抓取日期: 2026-03-27

以下为抓取正文（外部网页转 Markdown，本地归档）：

## 核心内容摘要

- 建团队前，先让 OpenClaw 学习自身文档，尤其是 agent 设置与 agent 间通信
- 建议启用：
  - `tools.sessions.visibility = all`
  - `tools.agentToAgent.enabled = true`
- 已有 agent 之间通信优先用 `sessions_send`
- 尽量用 `sessionKey`，少依赖 label
- `sessions_send(timeoutSeconds = 0)` 可用于不阻塞等待的异步协作
- 正式复杂任务前，先做 agent 间通信测试
- 当前阶段建议用 `/reset`，少用 `/new`，避免把通信链路搞乱
- 交付物最好放在清晰的共享交付目录，而不是散落在各自 workspace

## 对本仓库的启发

- 安装验收必须强调“先通信测试，再复杂任务”
- 命令文档里应明确 `/reset` 与 `/new` 的区别
- 默认接管方案里应准确写出 agentToAgent / sessions visibility 配置字段
- 交付物目录策略值得继续强化
