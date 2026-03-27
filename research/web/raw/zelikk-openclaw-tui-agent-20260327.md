# Openclaw 命令行 TUI 中 使用多 Agent

来源: https://zelikk.blogspot.com/2026/03/openclaw-tui-agent.html
抓取日期: 2026-03-27

以下为抓取正文（外部网页转 Markdown，本地归档）：

## 核心内容摘要

- 复杂临时问题不要污染当前复杂任务上下文
- 简单临时问题可用 subagent；复杂且可能需要交互的问题，更适合独立 agent/session
- 在 TUI 中可通过 `/agent` 快速切换或创建 agent
- 不同 agent 的 session 记录彼此隔离
- 可以在多个 SSH 会话中同时打开不同 agent 的 TUI 进行观察

## 对本仓库的启发

- `/agent` 与 agent/session 区分需要写进命令文档
- 复杂协作前先把 agent/session 基础使用说明清楚
- 监控多个 agent 时，多终端/多 TUI 观察是有效验收方式
