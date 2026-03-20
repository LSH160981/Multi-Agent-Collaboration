# Multi-Agent-Collaboration

**OpenClaw 原生多会话多 Agent 协作系统**

把复杂任务从“单 Agent 硬扛”升级为：

- 主Agent统筹
- AgentPool 动态招聘
- A/B 双组竞争
- 审核Agent 三维评分
- 检查Agent 巡检与恢复
- 最终只由主Agent向用户输出

## 核心卖点

- **Agent = OpenClaw session**
- **主Agent是唯一用户出口**
- **普通复杂任务默认可走本 skill 方法论**
- **支持 `/mac <任务>` 显式触发**
- **动态 specialist 招聘，而不是预建一堆空角色**
- **内置 JSON 协议、样例链、评分卡、队列、日志模板**
- **支持巡检、自学习、恢复、权重淘汰**

## 当前版本

`0.6.0`

## 适合什么任务

- 多步骤调研
- 复杂开发任务
- 故障排查与恢复
- 需要更高可靠性的协作任务
- 需要双路线对比择优的任务

## 当前已具备

1. skill 本体
2. 研究资料与提炼
3. 中文伪代码
4. 中文逻辑流程
5. JSON 通信协议与 A2A 样例链
6. 主Agent / 审核Agent / 检查Agent / AgentPool 骨架
7. specialist 模板
8. `/mac` 任务包协议
9. 安装脚本、初始化脚本、自检脚本、生成脚本
10. 权重系统与淘汰机制
11. 静默巡检模板与 cron 自学习模板
12. 任务看板/评分卡/日志/队列示例
13. 状态文件 JSON Schema
14. 演示跑通手册

## 目录概览

- `skills/Multi-Agent-Collaboration/`：正式 skill
- `agents/`：核心固定角色骨架
- `templates/`：动态 specialist 与共享模板
- `examples/`：任务样例、JSON 样例、运行痕迹样例
- `schemas/`：任务状态 / Agent 状态 / 评分卡 schema
- `scripts/`：初始化、自检、生成脚本
- `research/`：外部资料与提炼
- `docs/`：系统设计、演示手册与路线图

## 快速开始

### 1. 初始化目录

```bash
./scripts/init-mac-system.sh
```

### 2. 自检

```bash
./scripts/install-selfcheck.sh
```

### 3. 可选：批量生成一套 A/B 组 specialist 骨架

```bash
./scripts/generate-ab-team.sh
```

### 4. 开始任务

直接说：

```text
/mac 调研最近 30 天值得关注的 OpenClaw 多Agent 项目，提炼协同架构优点并给出改进建议。
```

## 阅读顺序建议

1. `docs/演示跑通手册.md`
2. `skills/Multi-Agent-Collaboration/SKILL.md`
3. `skills/Multi-Agent-Collaboration/mac任务包协议.md`
4. `examples/json/`
5. `examples/task-board-example.md`

## 项目状态

当前已经是一个**可安装、可初始化、可扩展、可继续自动化**的原型系统。
下一步重点将继续推进默认接管、自动化测试、以及更适合 ClawHub 发布的包装。
