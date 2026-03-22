# ClawHub / OpenClaw 相关多 Agent 经验提炼

> 说明：本文件主要总结从 OpenClaw 本地文档、技能机制、slash command 机制，以及现有多 Agent 实践里提炼出的可复用设计点。由于当前在线搜索 token 不可用，外部 Web 搜索未完全展开；后续可由自学习流程继续补齐。

## 1. 与本 skill 强相关的 OpenClaw 机制

### 1.1 skill 命令暴露

根据 OpenClaw 本地文档 `docs/tools/slash-commands.md`：

- `user-invocable: true` 的 skill 会暴露为 slash command
- skill 名会被清洗成 `a-z0-9_`
- 因此如果要得到 `/mac`，最稳方式不是只靠主 skill 名 `Multi-Agent-Collaboration`
- 而是额外提供一个名字就是 `mac` 的命令桥 skill

### 1.2 复杂任务默认走 skill 方法论

OpenClaw 的 skill 更适合承担：

- 角色纪律
- 流程规则
- 工具使用规范
- 触发词识别

而不是把所有能力都塞进一个大脚本。

### 1.3 Agent = session 比 label 更稳

从 OpenClaw 多会话实践看：

- `sessionKey` 比 label 更稳定
- 长任务更适合隔离 session
- 主Agent 应该是唯一用户可见出口
- 内部 Agent 应尽量通过结构化协议通信

## 2. 其他优秀 skill / 系统可借鉴的点

### 2.1 命令桥设计

优秀 skill 往往会做两层入口：

1. 默认自然语言触发
2. 显式 slash/text command 触发

我们吸收后形成：

- 普通复杂任务默认由 Multi-Agent-Collaboration 接管
- `/mac ...` 作为强制入口
- `使用 Multi-Agent-Collaboration skill 完成...` 作为口头强制入口

### 2.2 把“协作系统”和“执行技能”分离

OpenMOSS 的好处之一是：

- 平台只负责协作
- 每个 agent 真正能干什么，交给 skill 决定

我们吸收后形成：

- 协作骨架固定：主Agent / AgentPool / 审核Agent / 检查Agent
- specialist 动态招聘
- specialist 的能力边界写入 `abilities.md`

### 2.3 先有协议，再有自动化

优秀实现的共同点：

- 先定义任务包
- 再定义状态机
- 再定义回执结构
- 最后才补调度自动化

这比一开始就写一个“大一统控制器”更稳。

## 3. 对我们仓库的直接改造结论

1. 新增 `skills/mac/SKILL.md`，把 `/mac` 做成命令桥
2. 保留 `Multi-Agent-Collaboration` 作为主 skill、本体文档与方法论核心
3. 继续强化 session-based runtime orchestration，而不是只写本地 JSON
4. 所有伪代码、执行流程、恢复策略，都保留中文独立文件，方便人读和 agent 学习
5. 用 git + 中文 commit 持续记录结构迭代
