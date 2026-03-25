# 博客 - Openclaw 命令行 TUI 中 使用多 Agent

来源: https://zelikk.blogspot.com/2026/03/openclaw-tui-agent.html
抓取时间: 2026-03-25

## 摘要
- 适合把复杂临时问题切到新 agent，避免污染当前主任务上下文。
- TUI 中可以通过 `/agent` 新建/切换 agent。
- 不同 agent 的 session 彼此隔离。
- 在不同 SSH 会话中可同时打开多个 TUI，对不同 agent 并行观察。

## 可借鉴点
1. **上下文隔离价值**：复杂任务中切分 agent 很有必要。
2. **用户视角教学**：应把 `/agent`、多窗口观察写进演示文档。
3. **简洁安装体验**：普通用户更偏好自然语言或简单命令入口。

## 对本仓库的启发
- 演示手册应补充 TUI 观察多 agent 的方法。
- `/mac` 之外，也要说明 `/agent` / TUI 如何配合调试团队行为。
