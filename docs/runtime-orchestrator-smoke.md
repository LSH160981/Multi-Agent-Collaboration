# runtime orchestrator smoke

新增测试脚本：

```bash
./scripts/test_runtime_orchestrator_smoke.py
```

## 目标

验证这 4 个文件是否稳定落盘：
- `task-packet.json`
- `group-plan.json`
- `staffing-decision.json`
- `runtime-results.json`

并进一步检查 `runtime-results.json` 是否包含关键收口字段：
- `inspection_result`
- `review_result`
- `final_result`
- `session_probe`
- `stage`
- `resume_recommendation`

## 意义

它是当前 skill 从“解析/编组/决策”走向“真实 orchestrator 收口”的关键 smoke。

如果这个 smoke 稳定通过，说明：
- `/mac` 入口
- 编组
- staffing reuse/hire 决策
- coordinator dispatch
- worker/review/final 收口

至少已经串成一条完整 demo 链。
