# OpenClaw Docs - Pi 集成架构

来源: https://docs.openclaw.ai/zh-CN/pi
抓取时间: 2026-03-25

重点：OpenClaw 通过嵌入式 `createAgentSession()` 接 Pi/AgentSession，而不是子进程 RPC；工具、session、system prompt、事件订阅、session 文件持久化、模型轮换、provider failover 都是平台内建能力。这说明 Multi-Agent-Collaboration 应该优先站在 OpenClaw 原生 session / tool / skill / slash command 能力之上，而不是自己再发明一套伪运行时。

原始提取文本已在本次会话中抓取，因篇幅过长，这里保留学习结论与索引；如需完整原文，可重新抓取或查阅原链接。
