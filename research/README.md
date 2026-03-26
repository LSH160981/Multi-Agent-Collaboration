# 多 Agent 协同学习资料索引

本目录只保留两类东西：
- **值得持续参考的原始资料摘要**
- **会影响主 skill / docs / scripts 演进的研究沉淀**

## 目录约定

- `web/`：网页资料的**保留版摘要**，优先保留带日期的新版本
- `external/`：本地参考仓库副本（不作为主仓库实现的一部分）
- `sources/`：主题化摘录与观察笔记
- `auto/`：自动学习抓取、审核建议、吸收计划
- 顶层 `*.md`：跨来源综合提炼

> 纪律：外部资料先进入 `research/`，不得直接跳过审核去修改主 skill。
> 正确闭环：抓取 → research 落盘 → 审核判断 → 主 Agent 决定吸收 → git 记录。

## 当前重点主题

1. OpenClaw 原生 session 编排
2. 多 agent 角色分层
3. A/B 双组竞争 + reviewer 裁决
4. inspect / patrol / recover 闭环
5. JSON 任务包与 agent-to-agent 通信
6. 主 Agent 唯一用户出口与去重治理
7. 自学习 / 自改进 / git 记忆压缩策略

## 保留策略

- 同一网页有多份抓取时，优先保留**较新、带日期、信息更完整**的一份
- 原始网页长文不直接大段塞仓库，只保留可复用摘要
- GitHub 外部仓库主要用于学习，不把它们当主项目的一部分维护

## 当前建议优先阅读

### 网页摘要
- `web/openclaw-docs-pi-20260326.md`
- `web/clawhub-agent-team-orchestration-20260326.md`
- `web/clawhub-agent-directory.md`
- `web/zelikk-openclaw-tui-agent-20260326.md`
- `web/zelikk-openclaw-tui-agent-cooperate-20260326.md`

### 综合提炼
- `../docs/research/多agent协同外部资料提炼-20260326.md`
- `../docs/research/多agent协同优秀作品骨架与伪代码提炼-20260326.md`
- `多Agent协同提炼.md`

## 结论

`research/` 的目标不是“收藏一切”，而是给主 skill 的下一次演进留下高价值、低噪音的依据。
