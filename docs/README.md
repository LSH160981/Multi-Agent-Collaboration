# docs

本目录只保留**长期有用**的工程文档，避免把阶段性草稿、重复导航、临时总结堆进来。

## architecture/
放系统骨架、协议、调度、恢复、接管、差距分析。

建议按这个顺序看：
- `architecture/项目骨架与逻辑执行流程.md`：总导航 / 总纲
- `architecture/runtime调度说明.md`：正式入口、辅助脚本、demo 边界
- `architecture/staged-runtime-pipeline.md`：staged pipeline 细节
- `architecture/runtime_orchestrator_vs_pipeline_gap.md`：runtime 与 staged 的当前差异状态
- `architecture/伪代码到代码映射.md`：哪些设计已经落地为脚本

## guides/
放安装、入口、命令、演示、落地说明。

## testing/
放 smoke、测试矩阵、验收与排障说明。

## research/
放已经提炼过、值得长期保留的方法总结。

当前建议优先阅读：
- `docs/research/多agent协同研究总纲-20260327.md`
- `docs/research/自动学习与审核后自进化.md`
- `docs/research/openmoss-任务包-2026-03-22.md`

## 顶层文件
- `PROJECT_STRUCTURE.md`：仓库结构总纲
- `ENTRYPOINTS.md`：正式入口矩阵
- `CODE_REVIEW_NOTES.md`：最近几轮重构结论

## 维护原则
- 能并入已有总纲的，不再单独新增“目录说明”类文档
- 阶段性草案优先合并进正式文档，不长期保留平行版本
- `docs/` 讲结论，原始资料和抓取过程放 `research/`
- 讲“当前状态差异”的文件，要明确自己是状态说明，不要伪装成长期总纲
