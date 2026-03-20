# Multi-Agent-Collaboration

OpenClaw 原生多会话多 Agent 协作系统。

核心定位：

- **Agent = OpenClaw session**
- **主 Agent 是唯一用户出口**
- **子 Agent 只与 Agent 通信，不与用户通信**
- **按需创建子 Agent，而不是预先堆满角色**
- **双组竞争 + 审核 + 巡检 + 记忆/日志/任务队列**

## 当前进度

当前版本：`0.3.0`

已具备：

1. skill 本体
2. 研究资料与提炼
3. 中文伪代码
4. 中文逻辑流程
5. JSON 通信协议
6. 主Agent / 审核Agent / 检查Agent / AgentPool 骨架
7. specialist 模板
8. `/mac` 任务包协议
9. 安装脚本、测试脚本、恢复策略、git 策略、自学习方案
10. 三类真实任务样例

## 仓库结构

- `skills/Multi-Agent-Collaboration/`：正式 skill
- `agents/`：核心固定角色骨架
- `templates/`：动态生成 specialist 与共享模板
- `examples/`：任务样例
- `research/`：外部资料、学习摘录、优秀设计提炼
- `docs/`：系统设计与路线图

## 快速开始

安装到 OpenClaw 的 `skills/` 目录后，新会话中可直接：

- 直接自然语言下达复杂任务（默认使用本 skill 的多 Agent 方法论）
- 使用 `/mac <任务>`
- 或说：`使用 Multi-Agent-Collaboration skill 完成 XXX任务`

## 下一步重点

后续将继续补：

- 更强的 `/mac` 触发与安装自检
- 更完整的 JSON 消息样例库
- 更细的权重/淘汰机制
- 更接近可发布到 ClawHub 的包装
