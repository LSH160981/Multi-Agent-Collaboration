# /mac 任务包协议

当用户输入：

```text
/mac <任务内容>
```

主Agent 应把它解析成标准任务包。

## 标准任务包结构

```json
{
  "entry": "mac",
  "task_id": "TASK-20260321-001",
  "user_intent": "任务内容原文",
  "goal": "主Agent提炼后的目标",
  "task_type": "research | coding | ops | mixed",
  "complexity": "low | medium | high",
  "needs_clarification": false,
  "clarification_questions": [],
  "required_roles": ["主Agent", "AgentPool", "审核Agent", "检查Agent"],
  "specialists": ["Research", "Verification"],
  "execution_mode": "single-group | dual-group",
  "output_requirements": ["总结", "验证步骤"],
  "constraints": ["禁止非主Agent联系用户"]
}
```

## 解析规则

### 1. 判断是否复杂任务

以下情况默认认为是复杂任务：

- 多步骤
- 需要搜索/验证
- 需要编码/调试
- 需要多角色协同
- 需要更高可靠性

### 2. 判断执行模式

- 简单任务：`single-group`
- 中高复杂任务：`dual-group`

### 3. 判断是否先澄清

如果任务缺少以下关键要素，应先提问：

- 目标不明确
- 输出形式不明确
- 约束不明确
- 时间范围不明确

## 主Agent 执行动作

1. 解析 `/mac`
2. 生成任务包
3. 若需澄清，先向用户提问
4. 否则启动多 Agent 流程
