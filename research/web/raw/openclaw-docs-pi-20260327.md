# OpenClaw Pi 集成架构

来源: https://docs.openclaw.ai/zh-CN/pi
抓取日期: 2026-03-27

以下为抓取正文（外部网页转 Markdown，本地归档）：

SECURITY NOTICE: external untrusted content via web_fetch.

# Pi 集成架构

本文档描述了 OpenClaw 如何与 pi-coding-agent 及其相关包（`pi-ai`、`pi-agent-core`、`pi-tui`）集成以实现其 AI 智能体能力。

## 关键要点摘录

- OpenClaw 通过 `createAgentSession()` 直接导入并实例化 pi 的 `AgentSession`
- 平台原生提供 session 生命周期、工具注入、系统提示拼装、事件订阅、工具策略过滤、会话持久化、认证轮换、模型切换
- OpenClaw 工具侧包含 session/message/browser/cron/gateway 等能力
- skill 层应建立在这些平台能力之上，而不是重复发明平台

## 本地研究关注点

- session / tool / skill / prompt 的平台分层
- `tools/session*.ts` 与 `skills.ts` 的组织思路
- `buildAgentSystemPrompt()` 如何拼装技能、文档、工作区、静默回复、心跳、reply tags 等运行时规则
- OpenClaw 与 Pi CLI 的差异：我们应强调“原生 session tool 编排”，而不是长期把 CLI 适配层写成平台本体

---

原文较长，完整抓取可通过同源 URL 再获取；本地先保留与本 skill 最相关的结构性摘要，避免资料库无意义膨胀。
