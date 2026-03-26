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

### 当前结论

这轮之后，仓库更接近一个能长期维护的 skill 工程仓库，而不是“文档 + 脚本 + 生成物混在一起”的资料包。
