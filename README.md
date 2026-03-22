# Multi-Agent-Collaboration

**OpenClaw 原生多会话多 Agent 协作系统**

把复杂任务从“单 Agent 硬扛”升级为：

- 主Agent统筹
- AgentPool 动态招聘
- A/B 双组竞争
- 审核Agent 三维评分
- 检查Agent 巡检与恢复
- 最终只由主Agent向用户输出

---

## 致谢与来源说明

本项目在设计与整理过程中，**明确参考并吸收了 OpenMOSS 的优秀思路**，尤其是它在：

- 规划 / 执行 / 审查 / 巡查 四角闭环
- 任务分层
- 多 Agent 协作工作台式组织方式
- 巡检、恢复、返工、评分机制

这些方面给了本项目很大启发。

这里要明确说明：

- **我们借鉴了 OpenMOSS 的思路与部分设计主意**
- 它对本项目的文档结构、协作骨架、运行链路整理有直接启发
- 本项目不是 OpenMOSS 的复制品，而是把这些优点**转译为 OpenClaw 原生多会话版**
- 本项目最终落脚点是：**Agent = OpenClaw session**

参考项目：
- OpenMOSS: https://github.com/uluckyXH/OpenMOSS

---

## 使用方式（最简版）

只记住 3 种：

1. **直接说任务**：复杂任务默认归它管
2. **用 `/mac`**：强制进入多 Agent 协作
3. **点名 skill**：`使用 Multi-Agent-Collaboration skill 完成这个任务`

一句话版：

> **安装完后，复杂任务默认走它；想强制进入多 Agent，就用 `/mac`。**

---

## 核心卖点

- **Agent = OpenClaw session**
- **主Agent是唯一用户出口**
- **普通复杂任务默认可走本 skill 方法论**
- **支持 `/mac <任务>` 显式触发**
- **动态 specialist 招聘，而不是预建一堆空角色**
- **内置 JSON 协议、样例链、评分卡、队列、日志模板**
- **支持巡检、自学习、恢复、权重淘汰**
- **已经具备一批可运行原型代码：解析、编组、派单、评分、巡检、去重、总控**
- **已开始接入真实 OpenClaw runtime 调度能力**

## 当前版本

`1.0.0-alpha`

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
8. `/mac` 任务包协议与解析脚本
9. 安装脚本、初始化脚本、自检脚本、生成脚本、A/B 批量编组脚本
10. 权重系统、淘汰机制与实例
11. 静默巡检模板与 cron 自学习模板
12. 任务看板/评分卡/日志/队列/Agent 状态示例
13. 状态文件 JSON Schema
14. 演示跑通手册
15. 自动化测试任务模板
16. 发布说明草案
17. 示例校验脚本与日志样例生成脚本
18. 默认接管基础安装脚本
19. 动态招聘 / 派单 / 评分 / 巡检 / 去重 / 总控原型代码
20. 伪代码到代码映射说明
21. runtime dispatch / runtime orchestrator / inspect-and-recover / demo pipeline
22. `/mac` 命令桥 skill
23. 原生 session 调度样例

## 快速开始

### 1. 初始化目录

```bash
./scripts/init-mac-system.sh
```

### 2. 自检

```bash
./scripts/install-selfcheck.sh
```

### 3. 试跑 demo pipeline

```bash
./scripts/demo_pipeline.py "/mac 调研最近 30 天值得关注的 OpenClaw 多Agent 项目，提炼协同架构优点并给出改进建议。"
```

### 4. 原生 session 调度样例

```bash
./scripts/runtime_sessions.py "/mac 调研最近 30 天值得关注的 OpenClaw 多Agent 项目，并给出改造建议"
```

## 项目状态

当前已经是一个**高完成度原型仓库**：

- 可安装
- 可初始化
- 可演示
- 可扩展
- 已有可运行原型代码
- 已接入一部分真实 OpenClaw runtime 调度能力
- 已明确吸收 OpenMOSS 的优秀思路，并完成 OpenClaw 原生化改造
