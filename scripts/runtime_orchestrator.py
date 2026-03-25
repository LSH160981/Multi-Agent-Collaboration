#!/usr/bin/env python3
import argparse
import json
import subprocess
from pathlib import Path

from protocol_lib import build_task_assign
from runtime_lib import newest_session_for_agent, run_openclaw_agent, write_json

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
    }


def main():
    parser = argparse.ArgumentParser(description="Runtime orchestrator using real OpenClaw agents via CLI")
    parser.add_argument("text", help="Raw /mac text")
    parser.add_argument("--main-agent", required=True, help="Main/OpenClaw agent id")
    parser.add_argument("--review-agent", required=True, help="Review agent id")
    parser.add_argument("--inspect-agent", required=True, help="Inspection agent id")
    parser.add_argument("--pool-agent", required=True, help="AgentPool agent id")
    parser.add_argument("--outdir", default=str(REPO / "examples" / "generated" / "runtime"))
    args = parser.parse_args()

    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    task_packet_path = outdir / "task-packet.json"
    group_plan_path = outdir / "group-plan.json"
    staffing_path = outdir / "staffing-decision.json"

    subprocess.check_call([str(REPO / "scripts" / "mac_cli.py"), args.text, "--output", str(task_packet_path)])
    subprocess.check_call([str(REPO / "scripts" / "recruit_team.py"), str(task_packet_path), "--output", str(group_plan_path)])
    subprocess.check_call(["python3", str(REPO / "scripts" / "staffing_decision.py"), str(group_plan_path), "--output", str(staffing_path)])

    task_packet = json.loads(task_packet_path.read_text(encoding="utf-8"))
    group_plan = json.loads(group_plan_path.read_text(encoding="utf-8"))
    staffing = json.loads(staffing_path.read_text(encoding="utf-8"))

    coordinator_packets = {
        "main_agent": build_task_assign(task_packet["task_id"], "system", args.main_agent, task_packet["goal"], status="orchestrating", inputs=[compact_packet(task_packet)]),
        "pool_agent": build_task_assign(task_packet["task_id"], "main-ceo", args.pool_agent, "根据任务包与编组做复用/招聘决策", status="planning", inputs=[compact_packet(task_packet), group_plan, staffing]),
        "review_agent": build_task_assign(task_packet["task_id"], "main-ceo", args.review_agent, "准备后续审核与评分", status="standby", inputs=[compact_packet(task_packet)]),
        "inspect_agent": build_task_assign(task_packet["task_id"], "main-ceo", args.inspect_agent, "启动巡检与恢复预案", status="watching", inputs=[compact_packet(task_packet), staffing]),
    }

    results = {
        name: run_openclaw_agent(agent_id, json.dumps(packet, ensure_ascii=False, indent=2))
        for name, agent_id, packet in [
            ("main_agent", args.main_agent, coordinator_packets["main_agent"]),
            ("pool_agent", args.pool_agent, coordinator_packets["pool_agent"]),
            ("review_agent", args.review_agent, coordinator_packets["review_agent"]),
            ("inspect_agent", args.inspect_agent, coordinator_packets["inspect_agent"]),
        ]
    }

    session_probe = {
        "main_agent": newest_session_for_agent(args.main_agent),
        "pool_agent": newest_session_for_agent(args.pool_agent),
        "review_agent": newest_session_for_agent(args.review_agent),
        "inspect_agent": newest_session_for_agent(args.inspect_agent),
    }

    write_json(outdir / "runtime-results.json", {
        "task_packet": task_packet,
        "group_plan": group_plan,
        "staffing": staffing,
        "coordinator_packets": coordinator_packets,
        "results": results,
        "session_probe": session_probe,
    })
    print(json.dumps({"status": "ok", "outdir": str(outdir), "session_probe": session_probe}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
