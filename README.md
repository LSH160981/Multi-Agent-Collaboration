# Multi-Agent-Collaboration

OpenClaw 原生多会话多 Agent 协作系统。

核心定位：

- **Agent = OpenClaw session**
- **主 Agent 是唯一用户出口**
- **子 Agent 只与 Agent 通信，不与用户通信**
- **按需创建子 Agent，而不是预先堆满角色**
- **双组竞争 + 审核 + 巡检 + 记忆/日志/任务队列**

## 仓库结构

- `skills/Multi-Agent-Collaboration/`：正式 skill
- `research/`：外部资料、学习摘录、优秀设计提炼

## 快速开始

安装到 OpenClaw 的 `skills/` 目录后，新会话中可直接：

- 直接自然语言下达复杂任务（默认使用本 skill 的多 Agent 方法论）
- 使用 `/mac <任务>`
- 或说：`使用 Multi-Agent-Collaboration skill 完成 XXX任务`

## 当前版本

这是第一版骨架，重点先落地：

1. skill 说明
2. 角色架构
3. 任务协议
4. JSON 通信协议
5. 中文伪代码
6. 中文逻辑流程
7. 外部资料学习摘录

后续可继续补：

- 自动安装/配置脚本
- OpenClaw config patch 模板
- 多平台 `/mac` 分发方案
- 自动自学习 cron/heartbeat 模块
