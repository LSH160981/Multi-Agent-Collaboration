# CODE REVIEW NOTES

## 2026-03-26 再次结构重审结论

这轮不是继续堆内容，而是继续把仓库朝**正规 skill 工程骨架**收紧。

### 本轮已处理

1. **主 skill 目录规范化**
   - 主 skill 从 `skills/Multi-Agent-Collaboration/` 统一为：
     - `skills/multi-agent-collaboration/`
   - 原因：更符合常见 skill / package 命名习惯，避免大小写路径混乱。

2. **主 skill skeleton 继续收紧**
   - 主 skill 根目录仍只保留：
     - `SKILL.md`
     - `references/`
   - 协议文件统一位于：
     - `skills/multi-agent-collaboration/references/protocols/通信协议.json`

3. **测试与实现分层**
   - 所有测试脚本从 `scripts/` 迁到 `tests/`
   - 新增：`tests/README.md`
   - 原因：`scripts/` 应只放正式入口和可复用实现，不该混杂 smoke / regression。

4. **修复测试迁移后的导入与路径问题**
   - 为测试脚本显式加入 `scripts/` 到 `sys.path`
   - 修复 `protocol_lib.py` 的协议路径引用
   - 避免“目录搬了但测试全坏”的半截重构

5. **统一安装、自检、README、入口文档引用**
   - 安装脚本、自检脚本、README、ENTRYPOINTS、PROJECT_STRUCTURE 等路径引用统一到新结构
   - 测试命令统一改为 `python3 tests/...`

6. **继续控制仓库噪音**
   - 清理 `__pycache__/`
   - `examples/generated/` 继续作为生成物目录，不作为稳定骨架的一部分强调维护

### 这一轮之后更合理的分层

```text
skills/   -> 给 OpenClaw 读的 skill 骨架
scripts/  -> 正式入口 + 可复用实现
tests/    -> smoke / regression / example checks
docs/     -> 工程文档
research/ -> 外部资料与研究沉淀
```

### 仍然可继续优化的地方

1. `docs/` 中文档数量仍偏多，可继续合并导航
2. `research/` 仍有同主题重复抓取，可继续去重
3. 某些脚本仍偏 CLI 适配层，后续可继续向 OpenClaw 原生 session 能力收口
4. `skills/mac/SKILL.md` 仍以“命令桥语义”描述，但应避免依赖非标准 frontmatter 字段

## 2026-03-27 结构与入口再次收口结论

这一轮继续处理的是“结构像工程仓库，但脚本层仍稍显平铺”的问题。

### 本轮已处理

1. **脚本目录再次分层**
   - 新增：
     - `scripts/bootstrap/`
     - `scripts/analysis/`
   - 迁移：
     - `generate-agent.sh` -> `scripts/bootstrap/`
     - `generate-ab-team.sh` -> `scripts/bootstrap/`
     - `auto_evolve_learning.py` -> `scripts/analysis/`
     - `score_result.py` -> `scripts/analysis/`
     - `dedupe_summary.py` -> `scripts/analysis/`

2. **保留根层正式入口稳定**
   - 安装、自检、runtime、staged pipeline、恢复入口仍保留在 `scripts/` 根层
   - 原因：主入口不应频繁深层跳转，辅助/分析类脚本才适合下沉分组

3. **文档与入口矩阵同步更新**
   - 更新 `README.md`
   - 更新 `docs/PROJECT_STRUCTURE.md`
   - 更新 `docs/ENTRYPOINTS.md`
   - 更新 `scripts/README.md`
   - 修正自学习与伪代码映射中的旧路径引用

4. **清理明显噪音**
   - 删除 `scripts/__pycache__/`
   - 删除 `tests/__pycache__/`

### 这一轮之后的结构判断

更合理的脚本分层应理解为：

```text
scripts/
  根层        -> 正式入口 / 主链路
  bootstrap/  -> 骨架生成、脚手架
  analysis/   -> 分析、评分、去重、自学习
```

### 暂未大动的部分

1. `research/` 仍然体量很大，但这里优先保证“研究资料不污染主链路”，暂不做激进删除
2. `docs/research/` 仍有部分主题邻近文档，可继续再合并，但本轮先以修入口和分层为主
3. `agents/`、`templates/` 仍是骨架资产，后续可继续收紧说明与模板边界

### 当前结论

这轮之后，仓库从“已经能跑”进一步收敛到“结构更像正规 skill 工程”：
- 主入口留在根层
- 辅助脚本归位
- 文档与路径引用一致
- 测试入口矩阵更完整
- 明显缓存噪音已清掉
