# OpenMOSS 学习笔记

来源：

- `research/github/OpenMOSS/README_CN.md`

## 优点提取

1. **规划 / 执行 / 审查 / 巡查 四角闭环**
2. **cron 唤醒 + 自动巡检 + 异常恢复**
3. **评分/排行榜/激励系统**
4. **任务三级结构：Task / Module / Sub-Task**
5. **闭环质量控制：审查 → 驳回返工 → 再审**
6. **平台只管协作，能力由 skill 决定**

## 特别值得借鉴的逻辑

- 人类只下目标
- Planner 拆模块和子任务
- Executor 领取并执行
- Reviewer 审查评分
- Patrol 检测卡死并告警/恢复

## 我们吸收后的改造方向

- 保留“主 Agent / 审核 Agent / 检查 Agent / 动态 AgentPool”骨架
- 增加“双组竞争”机制：同题双做，对比择优
- 增加“淘汰/重招”机制：低分 Agent 组解散并重建
- 增加“用户消息唯一出口”机制：只有主 Agent 能联系用户
