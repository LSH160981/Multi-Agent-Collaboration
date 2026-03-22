# Multi-Agent-Collaboration Skill

本目录现在按“主 skill 轻量化、细节按需下沉”的方式组织。

## 核心文件

- `SKILL.md`：触发说明 + 核心执行规约
- `references/workflow.md`：角色模型、端到端流程、A/B 竞争与消息治理
- `references/protocol.md`：任务包字段、JSON 通信协议、共享上下文与恢复读取顺序
- `references/operations.md`：安装、`/mac` 入口、测试、巡检与恢复操作

## 保留的历史手稿

以下文件保留为补充手稿与设计素材，供后续继续提炼，不再作为主入口：

- `安装与使用.md`
- `伪代码.md`
- `逻辑执行流程.md`
- `消息治理规范.md`
- `恢复策略.md`
- 以及同目录下其他中文设计稿

原则：

1. 优先维护 `SKILL.md` 和 `references/` 下的现行版本
2. 历史手稿用于提炼思想，不要让多个文件同时承担“唯一规范”职责
3. 如果新增复杂说明，优先放入 `references/`，避免再次把 `SKILL.md` 写胖
