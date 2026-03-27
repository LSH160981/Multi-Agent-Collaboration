# tests

本目录只放测试与回归脚本，不再和 `scripts/` 混放。

## smoke / 集成测试
- `test_agent_handshake.py`
- `test_silent_task.py`
- `test_runtime_orchestrator_smoke.py`
- `test_recovery_pipeline_smoke.py`
- `test_stage3_smoke.py`
- `test_full_acceptance.py`
- `test_recovery_scenarios.py`

## 轻量校验
- `test_session_probe_example.py`
- `test_inspect_and_recover_actions.py`

## 设计原则
- `scripts/` 放正式入口与可复用实现
- `tests/` 放 smoke、回归、样例校验
- 测试如果依赖 `scripts/` 公共库，应显式把 `scripts/` 加入 `sys.path`
- 生成物统一落到 `examples/generated/`

## 运行示例
```bash
python3 tests/test_runtime_orchestrator_smoke.py
python3 tests/test_recovery_pipeline_smoke.py
python3 tests/test_stage3_smoke.py
python3 tests/test_full_acceptance.py
```

### 一键全链路验收
```bash
python3 tests/test_full_acceptance.py
```

### 跳过依赖真实 agent 的重阶段
```bash
python3 tests/test_full_acceptance.py --skip-runtime --skip-stage3
```
