# OpenClaw 官方文档：Pi 集成架构（抓取时间 2026-03-26）

来源：https://docs.openclaw.ai/zh-CN/pi

> 说明：以下为外部网页提取后的本地学习资料，供本仓库内部研究使用。

## 本次提炼重点

- OpenClaw 不是把 pi 当黑盒子 shell 调起来，而是直接嵌入 `createAgentSession()` 生命周期。
- 会话、工具、系统提示、session 文件、扩展、事件订阅、流式输出，本来就是平台级原生能力。
- 真正的多 Agent 方向不应该是再造一层“假 runtime”，而是站在现有 session / tool / skill / command 体系上做约束和编排。
- OpenClaw 已经有 session 相关工具、命令、事件、system prompt 注入与 skill 子系统；这正是 Multi-Agent-Collaboration 应该对接的硬基础。

## 与本 skill 直接相关的结论

1. **Agent = session** 这个方向是对的。
2. **技能负责方法论，平台负责会话运行**，不要混淆边界。
3. **主Agent唯一出口** 应该通过 system prompt / skill 纪律来保证，不靠口头约定。
4. **多会话协作最关键的不是角色名，而是会话生命周期、事件、工具调度、恢复与状态留痕。**
5. `/mac` 应被视为进入原生多会话协作的入口，而不是另起一套伪平台。

## 建议吸收到仓库的点

- 在安装文档中明确：协作系统建立在 OpenClaw 原生 session 能力之上。
- 在 session 命令参考中强调：`sessions_spawn`、`sessions_send`、`sessions_history`、`sessions_list`、`sessions_yield` 是第一优先级。
- 在项目骨架文档中区分：skill 层方法论 vs CLI/脚本层烟测适配。
- 在测试文档中增加：不要把 CLI 自检脚本误写成平台能力本身。

## 原文摘录（节选）

该文档核心强调：OpenClaw 使用 pi SDK 将 AI 编码智能体嵌入到 Gateway 架构中，直接导入并实例化 `AgentSession`，从而实现对会话生命周期、事件处理、自定义工具、系统提示、会话持久化、认证轮换、模型切换等能力的完全控制。

并且工具体系、session 管理、压缩、provider 适配、streaming、sandbox 与 TUI 都是平台的一部分。

这意味着：**Multi-Agent-Collaboration 应该尽量调用和约束这些已有能力，而不是重新发明一套平台。**
