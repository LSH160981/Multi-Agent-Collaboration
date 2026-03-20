# JSON 消息样例库说明

目录：`examples/json/`

这些样例展示了一个典型任务在系统中的消息流：

1. 主Agent → AgentPool
2. AgentPool → A组组长
3. 组长 → specialist
4. specialist → 组长（进度）
5. 组长 → 审核Agent
6. 审核Agent → 驳回某组
7. 审核Agent → 主Agent（通过）

用途：

- 作为开发时的协议参考
- 作为写日志和队列的参考
- 作为后续自动化脚本的输入/输出样板
