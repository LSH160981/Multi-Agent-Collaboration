#!/usr/bin/env python3
"""stage1_plan.py

staged pipeline 的第一阶段：任务理解、编组、巡检策略初始化。

输出：
- task_packet
- group_plan
- pipeline-state.json（stage1_done）

作用：
- 把复杂任务从“用户输入”推进到“可执行计划”。
"""

import argparse
import json
import subprocess
from pathlib import Path
from runtime_lib import build_session_reuse_hint, probe_agents, run_openclaw_agent, write_json

REPO = Path(__file__).resolve().parent.parent


def compact_packet(task_packet: dict) -> dict:
    return {
        "task_id": task_packet.get("task_id"),
        "goal": task_packet.get("goal"),
        "task_type": task_packet.get("task_type"),
        "complexity": task_packet.get("complexity"),
        "specialists": task_packet.get("specialists", []),
        "constraints": task_packet.get("constraints", []),
        "output_requirements": task_packet.get("output_requirements", []),
        "execution_mode": task_packet.get("execution_mode"),
        "needs_clarification": task_packet.get("needs_clarification", False),
        "clarification_questions": task_packet.get("clarification_questions", []),
    }


def main():
    parser = argparse.ArgumentParser(description="Stage 1: parse task + recruit + planning")
    parser.add_argument("text", help="Raw /mac text")
    parser.add_argument("--main-agent", default="main-ceo")
    parser.add_argument("--pool-agent", default="pool-hr")
    parser.add_argument("--inspect-agent", default="inspect-patrol")
    parser.add_argument("--review-agent", default="review-judge")
    parser.add_argument("--worker-agent-a", default="exec-worker-1")
    parser.add_argument("--worker-agent-b", default="")
    parser.add_argument("--outdir", default=str(REPO / "examples" / "generated" / "staged-runtime"))
    args = parser.parse_args()

    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    task_packet_path = outdir / "task-packet.json"
    group_plan_path = outdir / "group-plan.json"
    state_path = outdir / "pipeline-state.json"

    subprocess.check_call([str(REPO / "scripts" / "mac_cli.py"), args.text, "--output", str(task_packet_path)])
    subprocess.check_call([str(REPO / "scripts" / "recruit_team.py"), str(task_packet_path), "--output", str(group_plan_path)])

    task_packet = json.loads(task_packet_path.read_text(encoding="utf-8"))
    group_plan = json.loads(group_plan_path.read_text(encoding="utf-8"))
    compact = compact_packet(task_packet)

    agent_map = {
        "main_agent": args.main_agent,
        "pool_agent": args.pool_agent,
        "inspect_agent": args.inspect_agent,
        "review_agent": args.review_agent,
        "worker_agent_a": args.worker_agent_a,
        "worker_agent_b": args.worker_agent_b or None,
    }
    session_probe_before = probe_agents([v for v in agent_map.values() if v])
    dispatch_hints = {k: build_session_reuse_hint(v) for k, v in agent_map.items() if v}

    pool_result = run_openclaw_agent(
        args.pool_agent,
        "你是AgentPool。请用 JSON 输出分工与招聘/复用判断："
        '{"role":"","why":"","plan":[""],"reuse":[""],"hire":[""],"boundaries":[""]}'
        + "\n\n"
        + json.dumps({"task": compact, "group_plan": group_plan, "agent_map": agent_map}, ensure_ascii=False),
        timeout=240,
    )
    inspect_result = run_openclaw_agent(
        args.inspect_agent,
        "你是检查Agent。请用 JSON 输出巡检策略："
        '{"watch":[""],"stale_rule":"","recover":[""],"escalation":[""]}',
        timeout=240,
    )

    state = {
        "stage": "stage1_done",
        "entry_text": args.text,
        "task_packet": compact,
        "group_plan": group_plan,
        "agent_map": agent_map,
        "dispatch_hints": dispatch_hints,
        "pool_result": pool_result,
        "inspect_result": inspect_result,
        "worker_role": (task_packet.get("specialists") or ["Generalist"])[0],
        "session_probe_before": session_probe_before,
        "resume_recommendation": {
            "next_stage": "stage2_workers",
            "reason": "stage1 已完成，可进入 worker 执行",
        },
    }
    write_json(state_path, state)
    print(json.dumps({"status": "ok", "stage": state["stage"], "outdir": str(outdir)}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
