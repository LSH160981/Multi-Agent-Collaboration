# /mac 任务包协议（OpenClaw 原生多会话版）

当用户输入：

```text
/mac <任务内容>
```

主Agent 必须把它解析成标准任务包，作为后续调度、审核、恢复、留档的统一输入。

---

## 一、标准任务包结构

```json
{
  "entry": "mac",
  "task_id": "TASK-20260322-001",
  "user_intent": "任务内容原文",
  "goal": "主Agent 提炼后的任务目标",
  "task_type": "research | coding | ops | mixed",
  "complexity": "low | medium | high",
  "needs_clarification": false,
  "clarification_questions": [],
  "required_roles": ["主Agent", "AgentPool", "审核Agent", "检查Agent"],
  "specialists": ["Research", "Verification", "Summary"],
  "execution_mode": "single-group | dual-group",
  "output_requirements": ["总结", "验证步骤", "风险说明"],
  "constraints": ["禁止非主Agent联系用户"],
  "priority": "normal | high | critical",
  "sources_hint": ["GitHub", "ClawHub", "OpenClaw Docs"],
  "done_when": ["列出完成判据"],
  "created_by": "main-ceo",
  "created_at": "ISO-8601"
}
```

---

## 二、解析规则

### 1. 判断是否复杂任务

以下情况默认认为是复杂任务：
- 多步骤
- 需要搜索 / 验证
- 需要编码 / 调试
- 需要跨角色协同
- 需要更高可靠性
- 用户明确要求多 Agent

### 2. 判断任务类型

- `research`：调研、搜索、对比、提炼
- `coding`：实现、改代码、修 bug、重构
- `ops`：排障、部署、巡检、恢复
- `mixed`：同时包含调研 + 开发 + 验证

### 3. 判断复杂度

- `low`：可由单条稳定路径快速完成
- `medium`：需要拆分、验证、比对
- `high`：需要并行竞争、多轮审核、持续巡检

### 4. 判断执行模式

- `low` → 默认 `single-group`
- `medium/high` → 默认 `dual-group`

### 5. 判断是否先澄清

如果缺以下关键要素，先问用户：
- 目标不明确
- 输出形式不明确
- 约束不明确
- 时间范围不明确
- 成功标准不明确

---

## 三、主Agent 执行动作

1. 识别 `/mac`
2. 提炼用户真实目标
3. 生成标准任务包
4. 如需澄清，先提问
5. 如无需澄清，交给 AgentPool 编组
6. 将任务包写入共享任务目录与日志

---

## 四、与 OpenMOSS 风格一致的设计点

本协议吸收的核心思路是：

- 任务必须先结构化
- 调度必须围绕任务包进行
- 审核、巡检、恢复都应基于同一个 task_id
- 任务包不是文档装饰，而是运行时核心数据结构

---

## 五、任务包派生物

一个 `task-packet.json` 生成后，通常还会派生出：

- `group-plan.json`：A/B 双组方案
- `review-scorecard.json`：审核评分卡
- `inspection-report.json`：巡检与恢复报告
- `final-brief.json`：主Agent 最终交付摘要

这样整个任务链路就能完整追踪。
