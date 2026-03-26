# OpenClaw 官方文档：Pi 集成架构（2026-03-26 抓取）

来源：`https://docs.openclaw.ai/zh-CN/pi`
抓取方式：web_fetch
说明：外部网页文本，作为学习资料落地保存。

---

以下为本轮提炼摘要：

## 核心结论

OpenClaw 的 agent 运行不是简单 shell 包装，而是平台内嵌 session / tool / prompt / event / auth / model / history / compaction / sandbox / streaming 的组合系统。

这意味着：

- 我们的 `Multi-Agent-Collaboration` 不该再造平台
- 应该站在 OpenClaw 已有 session 能力之上做 orchestration
- 重点应放在 task packet、角色边界、审核、恢复、消息治理

## 值得吸收的点

1. 明确区分平台层与 skill 层
2. 通过 session 能力形成多 Agent 闭环
3. 工具、prompt、history、compaction 都是平台已提供的能力
4. skill 只做方法论、纪律、工作流、恢复与收口

## 建议和本 skill 对齐的骨架

```text
平台层:
  session lifecycle
  tool injection
  prompt builder
  event subscription
  auth/model resolution

skill层:
  task routing
  staffing decision
  review policy
  recovery policy
  dedupe policy
  user-output governance
```

---

原始网页内容较长，已在本次会话中抓取并阅读；此处保存为学习资料摘要，避免把过长网页原文重复塞进仓库。
