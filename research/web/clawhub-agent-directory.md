# ClawHub：Agent Directory（2026-03-26 抓取）

来源：`https://clawhub.ai/aerialcombat/agent-directory`
抓取方式：web_fetch
说明：外部网页文本，作为学习资料落地保存。

---

## 核心结论

这个页面更像“agent 服务目录”，价值不在 orchestration 本身，而在：

1. 强调 skill/documentation 对 agent 可读性的重要性
2. 强调“先发现服务，再读 skill，再决定如何集成”的流程

## 对我们 skill 的启发

- 自动学习模块不要直接乱搜乱改
- 应先抓取 skill / 文档
- 然后整理进 `research/`
- 最后由审核Agent与主Agent决定是否吸收

## 推荐闭环

```text
discover -> fetch skill/docs -> summarize -> review -> absorb
```

这正适合做成我们的“自学习但受审核”的机制。
