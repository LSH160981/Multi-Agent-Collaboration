# 博客 - Openclaw 命令行 TUI 中 使用多 Agent 协同完成任务

来源: https://zelikk.blogspot.com/2026/03/openclaw-tui-agent-cooperate.html
抓取时间: 2026-03-25

## 摘要
- 作者强调要先让系统学习 OpenClaw 文档，特别是 agent 设置与 agent 间通信。
- 已有 agent 团队时，建议优先使用 `sessions_send`，而不是 `sessions_spawn`。
- 实操中建议做 agent-to-agent 通信测试，再开始复杂任务。
- 作者记录了若干真实坑：session 路由混乱、label 使用不稳定、交付物目录不理想、模型跑着跑着没反应等。

## 可借鉴点
1. **先通信测试再开工**：握手测试是必须项。
2. **区分已有 agent 与动态新建 agent**：已有团队优先 `sessions_send`。
3. **交付物路径要明确**：最好统一在 workspace 外独立 deliverables 目录。
4. **文档要诚实记录坑**：例如 /new vs /reset、label 误用、模型/超时问题。

## 对本仓库的启发
- 要保留 `test_agent_handshake.py` 与 `test_silent_task.py` 作为安装后必测。
- 要在文档中明确：已有会话优先 `sessions_send`，缺角色才 `sessions_spawn`。
- 要补“常见坑与规避”章节。
