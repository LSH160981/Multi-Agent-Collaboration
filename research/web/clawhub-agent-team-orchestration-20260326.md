# ClawHub：Agent Team Orchestration（抓取时间 2026-03-26）

来源：https://clawhub.ai/arminnaimi/agent-team-orchestration

## 本次提炼重点

- 最小有用团队 = orchestrator + builder + reviewer。
- orchestrator 不亲自下场执行，而是负责路由、状态跟踪、结果汇报。
- 任务要有清晰状态机：Inbox → Assigned → In Progress → Review → Done | Failed。
- handoff 不能写空话，必须写清：做了什么、产物在哪里、怎么验证、已知问题、下一步。
- 如果没有 review，质量很快漂移。

## 对本仓库的直接启发

1. 主Agent 不要兼做所有执行细节，要把“统筹”和“执行”严格分开。
2. Reviewer 不能只是概念角色，必须是真可运行会话。
3. 任务状态、handoff、产物路径、验证命令，都要进入 task packet 或评分卡。
4. 最小团队原则很适合本 skill：默认先上小团队，确实需要时再扩到 A/B 双组。

## 可转化为我们自己的规则

- 主Agent：只做分析、派单、审核用户可见输出、去重。
- Worker：必须交付结构化结果，不许“Done, check files.” 这种无效交接。
- Reviewer：必须给出驳回理由和修正建议。
- 任务失败是合法终点，但必须记录失败原因与恢复建议。
