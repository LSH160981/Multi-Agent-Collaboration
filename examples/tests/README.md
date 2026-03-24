# tests

这里放自动化测试任务模板与测试辅助文件。

## 当前已补的自动化脚本

- `../../scripts/test_agent_handshake.py`：Agent 两两握手测试
- `../../scripts/test_silent_task.py`：静默任务回归测试
- `../../scripts/test_recovery_loop.py`：恢复链路测试
- `../../scripts/session_probe.py`：session 观测与排障
- `agent-map.example.json`：目录角色到 OpenClaw agent id 的映射样例

建议未来结合：

- `scripts/mac_cli.py`
- `scripts/validate_examples.py`
- `schemas/`

把这些模板逐步升级成更强的自动化验收流程。
