# Multi-Agent-Collaboration Skill

这是本 skill 的核心方法论文档区。

## 一句话理解

**安装完后，复杂任务默认走它；想强制进入多 Agent，就用 `/mac`。**

## 主入口阅读顺序

第一次接手时，建议固定按下面顺序读：

1. `SKILL.md`
2. `安装与使用.md`
3. `逻辑执行流程.md`
4. `伪代码.md`
5. `消息治理规范.md`
6. `恢复策略.md`
7. `mac任务包协议.md`
8. `通信协议.json`

补充资料再按需看：`references/`、`docs/`、`examples/`、`schemas/`、`scripts/`。

## 说明

本 skill 在设计上明确借鉴了 OpenMOSS 的优秀思路，尤其是：

- 多 Agent 协作工作台式组织方式
- 规划 / 执行 / 审查 / 巡查 四角闭环
- 任务拆解、评分、巡检、恢复逻辑

但本 skill 的最终实现目标不是复刻 OpenMOSS，而是：

**把这些优点落到 OpenClaw 原生多会话体系里。**

也就是说：
- OpenMOSS 给了我们重要启发
- OpenClaw session 是我们的运行实体
- 主Agent唯一对用户输出是我们的硬约束

参考：
- OpenMOSS: https://github.com/uluckyXH/OpenMOSS

## 当前主文档已经明确的几件事

- **默认接管**：复杂任务默认先到主Agent，再决定是否扩成多会话
- **唯一用户出口**：只有主Agent 可以面向用户输出
- **核心角色**：主Agent / 审核Agent / 检查Agent / AgentPool
- **恢复底线**：先收敛出口，再 probe/催办/续跑，最后才重派或重建
- **目录分层**：主文档层、参考层、schema/examples/scripts 分层已固定

## 核心文件

- `SKILL.md`：主 skill 说明与硬约束
- `安装与使用.md`：安装、入口、安装后测试
- `伪代码.md`：中文伪代码
- `逻辑执行流程.md`：中文流程
- `消息治理规范.md`：主Agent唯一出口与去重规则
- `恢复策略.md`：中断恢复思路
- `通信协议.json`：Agent JSON 消息协议
- `mac任务包协议.md`：`/mac` 任务包协议
- `自动自学习方案.md`：周期学习机制
- `测试脚本.md`：安装后测试模板
- `../../docs/openclaw-agent-session-commands.md`：OpenClaw agent session / slash commands 参考
