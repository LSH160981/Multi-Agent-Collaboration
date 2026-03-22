# OpenMOSS 学习笔记

来源：

- `research/github/OpenMOSS/README_CN.md`
- OpenMOSS 仓库整体结构与说明

参考项目：
- https://github.com/uluckyXH/OpenMOSS

## 为什么要学 OpenMOSS

因为 OpenMOSS 不只是一个普通多 Agent demo，它更像一个：

- 多 Agent orchestration workspace
- 协作 IDE / 工作台
- 带有规划、执行、审查、巡查闭环的系统化方案

这对我们构建 `Multi-Agent-Collaboration` 很有参考价值。

## 优点提取

1. **规划 / 执行 / 审查 / 巡查 四角闭环**
2. **cron 唤醒 + 自动巡检 + 异常恢复**
3. **评分/排行榜/激励系统**
4. **任务三级结构：Task / Module / Sub-Task**
5. **闭环质量控制：审查 → 驳回返工 → 再审**
6. **平台只管协作，能力由 skill / 角色决定**
7. **IDE / 工作台式组织方式清晰，适合长期演进**

## 特别值得借鉴的逻辑

- 人类只下目标
- Planner 拆模块和子任务
- Executor 领取并执行
- Reviewer 审查评分
- Patrol 检测卡死并告警/恢复
- 整个系统围绕任务状态推进，而不是单轮对话堆叠

## 我们吸收后的改造方向

- 保留“主 Agent / 审核 Agent / 检查 Agent / 动态 AgentPool”骨架
- 增加“双组竞争”机制：同题双做，对比择优
- 增加“淘汰/重招”机制：低分 Agent 组解散并重建
- 增加“用户消息唯一出口”机制：只有主 Agent 能联系用户
- 把 OpenMOSS 的 IDE / orchestration 思路，转译为 **OpenClaw 原生 session 协作系统**

## 明确边界

我们不是直接复刻 OpenMOSS。

我们的目标是：

- 学它的优点
- 吸收它的协作骨架
- 保留它值得借鉴的 IDE / 工作台思路
- 但运行实体改成 OpenClaw session
- 组织纪律改成“主Agent唯一用户出口”
- 通信与恢复适配 OpenClaw 原生工具链
