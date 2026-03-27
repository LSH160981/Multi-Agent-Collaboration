# research/github

本目录现在作为 **GitHub 研究来源的唯一轻量入口**。

## 边界

- `research/github/`
  - 只保留：轻量说明、必要笔记、少量可追溯原始文本
  - 不再把重量级外部仓库副本长期纳入主仓库版本控制

- `research/inbox/`
  - 本地临时拉取区
  - 用于临时 clone / diff / grep / 对照研究
  - 不应纳入主仓库版本控制

- `research/external/`
  - 历史重副本目录
  - 已不再作为正式入口，后续应逐步清出主仓库版本控制

## 推荐做法

如果需要重新拉取外部仓库，只在本地临时使用：

```bash
git clone --depth=1 https://github.com/AlexAnys/opencrew.git research/inbox/opencrew
git clone --depth=1 https://github.com/uluckyXH/OpenMOSS.git research/inbox/OpenMOSS
git clone --depth=1 https://github.com/win4r/ClawTeam-OpenClaw.git research/inbox/ClawTeam-OpenClaw
git clone --depth=1 https://github.com/golutra/golutra.git research/inbox/golutra
```

研究完成后：
- 提炼结论进 `docs/research/`
- 原始仓库副本保留在本地即可
- 不把它们继续纳入主仓库历史
