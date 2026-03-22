# Multi-Agent-Collaboration Skill

这是本 skill 的核心方法论文档区。

## 一句话理解

**安装完后，复杂任务默认走它；想强制进入多 Agent，就用 `/mac`。**

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

## 核心文件

- `SKILL.md`：主 skill 说明
- `安装与使用.md`：安装与入口方法
- `伪代码.md`：中文伪代码
- `逻辑执行流程.md`：中文流程
- `通信协议.json`：Agent JSON 消息协议
- `mac任务包协议.md`：`/mac` 任务包协议
- `恢复策略.md`：中断恢复思路
- `自动自学习方案.md`：周期学习机制
- `测试脚本.md`：安装后测试模板
