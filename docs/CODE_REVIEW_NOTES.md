# CODE REVIEW NOTES

## 2026-03-26 结构重审结论

本轮重点不是继续加功能，而是清理项目结构、入口和 skill 骨架。

### 已处理

1. **主 skill 收紧为更标准的 skill skeleton**
   - `skills/Multi-Agent-Collaboration/` 根目录现在只保留：
     - `SKILL.md`
     - `references/`
   - 原先平铺在 skill 根目录的大量说明文件已迁入 `references/` 子目录
   - 分类为：
     - `references/guides/`
     - `references/governance/`
     - `references/operations/`
     - `references/protocols/`
     - `references/strategy/`
     - `references/testing/`
     - `references/workflow*.md`

2. **删除 skill 内多余 README**
   - 删除：
     - `skills/Multi-Agent-Collaboration/README.md`
     - `skills/mac/README.md`
   - 原因：它们不属于最终 skill 骨架的必要组成，且和 `SKILL.md` 职责重叠

3. **删除重复安装脚本**
   - 删除：`skills/Multi-Agent-Collaboration/安装脚本.sh`
   - 原因：仓库级正式安装入口已经存在于 `scripts/default-takeover-setup.sh`

4. **停止跟踪 generated 运行产物**
   - `examples/generated/` 已移出 git 跟踪
   - 原因：这些是测试/运行产物，不应作为稳定项目骨架的一部分长期版本化

5. **清理缓存与本地大文件目录**
   - `.gitignore` 已补充：
     - `__pycache__/`
     - `*.pyc`
     - `examples/generated/`
     - `research/external/`
   - 目的：减少仓库噪音与无意义提交

6. **统一入口路径引用**
   - README、自检脚本、skill 说明中的路径已对齐新的 `references/` 结构

### 仍保留但后续可继续优化

1. `docs/` 目录仍然较多，后续可再精简合并
2. `research/web/` 里仍有部分旧版/新版同主题抓取，可再做一次去重
3. runtime 代码仍以 CLI 适配层为主，后续应进一步向 OpenClaw session tools 靠拢

### 当前判断

这轮之后，仓库更接近：
- 正规 skill skeleton
- 清楚的仓库级入口矩阵
- 清楚的工程层 / 文档层 / 研究层分离
- 减少 generated / cache / 重复说明 的污染

下一阶段如果继续重构，最值得做的是：
- 继续精简 `docs/`
- 进一步统一 `research/` 去重
- 让 runtime 编排更直接使用 OpenClaw 原生 session tools
