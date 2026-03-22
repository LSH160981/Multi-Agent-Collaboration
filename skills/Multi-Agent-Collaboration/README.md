# Multi-Agent-Collaboration Skill

这是本 skill 的文件目录，也是整个系统的核心方法论文档区。

## 说明

本 skill 在设计上**明确借鉴了 OpenMOSS 的优秀思路**，尤其是：

- 多 Agent 协作 IDE / 工作台式组织方式
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
- `命名规范.md`：任务/组/文件命名约定
- `消息治理规范.md`：用户消息治理规则
- `恢复策略.md`：中断恢复思路
- `git记录策略.md`：日志与记忆的 git 策略
- `自动自学习方案.md`：周期学习机制
- `测试脚本.md`：安装后测试模板
- `安装脚本.sh`：基础安装脚本

## 阅读建议

如果你想快速理解整个 skill，建议按这个顺序读：

1. `SKILL.md`
2. `安装与使用.md`
3. `伪代码.md`
4. `逻辑执行流程.md`
5. `通信协议.json`
6. `恢复策略.md`
7. `自动自学习方案.md`
8. `测试脚本.md`
