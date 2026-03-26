# zelikk：OpenClaw 命令行 TUI 中使用多 Agent（2026-03-26 抓取）

来源：`https://zelikk.blogspot.com/2026/03/openclaw-tui-agent.html`
抓取方式：web_fetch
说明：外部网页文本，作为学习资料落地保存。

---

## 核心结论

这篇文章的重点是：

- TUI 中可以快速切换/新建 agent
- 不同 agent 的 session 可以隔离上下文
- 复杂临时问题适合单开 agent 处理，避免污染主上下文

## 对我们 skill 的启发

1. agent 与 session 必须分清
2. 多 agent 协作时，人工观察最好多开 TUI 窗口
3. 普通复杂任务可交给主Agent 决定是否需要单独新建内部会话
4. 用 `/agent` 切换观察不同角色很有价值

## 可以吸收的实践

- 安装后验收文档里明确推荐用 `/agent` 观察
- 主Agent 处理复杂任务时优先考虑“隔离上下文污染”
- session 作为 agent 运行单元的概念要继续强化
