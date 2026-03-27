# research

本目录只放**原始资料、本地抓取、自动学习中间产物、外部仓库研究副本**。

和 `docs/research/` 的区别：

- `research/`：原料层、过程层、抓取层、本地研究缓存
- `docs/research/`：提炼后的长期结论层

## 当前边界

- `research/auto/`
  - 自动学习抓取结果
  - 学习摘要
  - learning packet

- `research/web/`
  - 外部网页抓取后的本地归档
  - 保留轻量 Markdown 版原始文本与摘要

- `research/github/`
  - GitHub 研究来源的**唯一轻量入口**
  - 只保留说明、必要笔记、少量原始文本
  - 不长期纳入重量级仓库副本

- `research/inbox/`
  - 本地临时拉取区
  - 用于 clone / grep / diff / 对照研究
  - 不应纳入主仓库版本控制

- `research/external/`
  - 历史重副本区
  - 已不再作为正式入口，后续应逐步清出主仓库版本控制

- `research/sources/`
  - 来源清单、网页原始提取、观察笔记

## 维护原则

1. 原始资料先放这里，不直接污染主 skill
2. 值得长期保留的结论，再提炼进 `docs/research/`
3. 重量级外部仓库副本只保留在本地，不纳入主仓库版本控制
4. 自动学习脚本只允许把候选资料落这里，不允许直接重写主 skill
5. `research/github/` 是 GitHub 研究来源的唯一正式轻量入口；`research/inbox/` 只是本地临时拉取区
