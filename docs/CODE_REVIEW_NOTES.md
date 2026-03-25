# CODE_REVIEW_NOTES

## 本轮审计发现

### 结构问题
- 存在重复目录：`skill/` 与 `skills/`，其中 `skill/` 为空占位，应删除。
- `research/` 内容体量很大，必须与主实现层严格分离。
- 文档较多，但此前没有按 architecture / guides / testing / research 分层。

### 代码问题
- 核心脚本已有一定可用性，但模块头注释不足。
- 一些脚本命名属于同一条能力链，容易被误解为重复实现。
- 需要在 `scripts/README.md` 中明确：
  - 安装类
  - 编排类
  - 恢复类
  - smoke/test 类
  - research/辅助类

### 当前处理原则
- 先做结构收敛与注释增强。
- 不做大规模“推倒重写”，避免破坏当前可运行原型。
- 先删明显无用/空目录，再补文档和注释，再看是否继续合并脚本。

## 下一步建议
- 将 docs 逐步迁移到分层子目录。
- 对 runtime、protocol、session、test 相关脚本统一加模块说明和函数说明。
- 进一步识别可以合并的 demo/test 脚本。
