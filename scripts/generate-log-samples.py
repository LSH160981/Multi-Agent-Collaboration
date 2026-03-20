#!/usr/bin/env python3
from datetime import datetime
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
OUT = REPO / "examples/generated"
OUT.mkdir(parents=True, exist_ok=True)

now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

(OUT / "main-agent-log.md").write_text(
    f"# 主Agent 日志样例\n\n- time: {now}\n- task_id: TASK-DEMO-001\n- action: 接收用户 /mac 调研任务\n- result: 已生成任务包并交给 AgentPool\n- next_step: 等待 A/B 组提交\n",
    encoding="utf-8",
)

(OUT / "inspection-log.md").write_text(
    f"# 检查Agent 日志样例\n\n- time: {now}\n- task_id: TASK-DEMO-001\n- action: 巡检 B组-检索专家\n- result: 发现 15 分钟无日志更新，已发送唤醒建议\n- next_step: 5 分钟后复检\n",
    encoding="utf-8",
)

print(f"已生成样例目录: {OUT}")
