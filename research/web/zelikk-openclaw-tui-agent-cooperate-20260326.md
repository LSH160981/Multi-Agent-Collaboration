# zelikk：OpenClaw TUI 中多 Agent 协同完成任务（抓取时间 2026-03-26）

来源：https://zelikk.blogspot.com/2026/03/openclaw-tui-agent-cooperate.html

## 本次提炼重点

- 先让系统理解 OpenClaw 文档、agent 设置、agent 间通信，再做协作，是现实做法。
- 多 Agent 协作前，必须先测试 agent-to-agent 通信是否正常。
- 已有团队优先 `sessions_send`，不要动不动 `sessions_spawn`。
- 调试时别混乱地新建 session；需要区分 agent 和 session 生命周期。
- 作者明确记录了常见坑：label 参数误用、交付物目录不合理、模型跑飞、无响应、超时。

## 对本仓库的直接启发

1. 握手测试必须保留，而且要放在安装验收前列。
2. 文档里要诚实写出当前已知坑，不要只写理想流程。
3. `sessions_send` 复用优先，是本 skill 的硬规则之一。
4. 交付目录、session 路由、恢复策略需要明确，不然公司化协作会很快失控。
