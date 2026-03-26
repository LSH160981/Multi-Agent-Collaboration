# ClawHub：Agent Team Orchestration（2026-03-26 抓取）

来源：`https://clawhub.ai/arminnaimi/agent-team-orchestration`
抓取方式：web_fetch
说明：外部网页文本，作为学习资料落地保存。

---

## 核心结论

这个 skill 最值得学习的，不是“大团队”，而是它先定义了 **最小有用团队**：

- Orchestrator
- Builder
- Reviewer（按需加）

并且把多 agent 协作推导成：

```text
角色 -> 状态机 -> handoff -> review -> 质量闭环
```

## 最值得吸收的点

1. Orchestrator 只调度，不下场抢活
2. Task state 必须有定义明确的生命周期
3. Handoff 必须说清：做了什么 / 产物在哪 / 怎么验证 / 已知问题 / 下一步是谁接
4. Reviewer 是阻止质量漂移的关键，不应省略
5. Failed 是合法终态，而不是系统异常

## 对我们 skill 的启发

- 默认不要预建巨大团队
- 先让最小闭环跑通
- 再按需要扩成 A/B 双组竞争
- 所有 agent-to-agent 消息都应该结构化
- 所有 review 和 recovery 都应有明确定义

## 可吸收到本 skill 的伪代码

```text
如果任务简单:
  主Agent 单会话完成
否则:
  主Agent 拆任务
  worker 产出
  reviewer 检查
  inspect 观察是否卡住
  主Agent 最终收口
```
