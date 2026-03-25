# zelikk：OpenClaw TUI 中使用多 Agent（抓取时间 2026-03-26）

来源：https://zelikk.blogspot.com/2026/03/openclaw-tui-agent.html

## 本次提炼重点

- 多任务并行时，单一会话很容易产生上下文污染。
- TUI 内可以切换 agent / session，适合做多 Agent 观察与调试。
- 使用不同 agent 可以让对话记录天然隔离。
- 这类实践说明：多 Agent 的一个核心价值就是把复杂任务与临时插入任务分开，减少相互干扰。

## 对本仓库的直接启发

1. Multi-Agent-Collaboration 不是为了“热闹”，而是为了解决复杂任务中的上下文串线问题。
2. 调试文档里应该明确写：多个 TUI / SSH 窗口观察不同 agent，是排障利器。
3. 普通复杂任务默认接管、临时复杂支线另起会话，都是合理的用户体验方向。
