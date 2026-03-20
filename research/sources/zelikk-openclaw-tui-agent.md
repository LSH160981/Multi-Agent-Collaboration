# Openclaw 命令行 TUI 中使用多 Agent — 学习摘录

来源：<https://zelikk.blogspot.com/2026/03/openclaw-tui-agent.html>

## 关键点

- 在复杂任务进行中，临时插入另一个复杂任务，最好新建独立 agent/session，避免上下文污染
- TUI 可以通过 `/agent` 快速切换或新建 agent
- 不同 agent/session 的上下文相互隔离
- 复杂交互问题适合单独 agent 持续处理，而不是临时 subagent 一次性跑完

## 对本 skill 的启发

- `Agent = OpenClaw session` 是成立的，而且是原生能力
- 复杂任务必须 session 隔离，否则主对话会越来越脏
- 我们的 skill 应默认把复杂任务转入多 session 协同，而不是让单一上下文无限膨胀
