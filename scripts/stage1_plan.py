#!/usr/bin/env python3
import argparse
import json
import subprocess
from pathlib import Path
from runtime_lib import run_openclaw_agent, write_json

REPO = Path(__file__).resolve().parent.parent


def compact_packet(task_packet: dict) -> dict:
    return {
        "task_id": task_packet.get("task_id"),
        "goal": task_packet.get("goal"),
        "task_type": task_packet.get("task_type"),
        "specialists": task_packet.get("specialists", []),
        "constraints": task_packet.get("constraints", []),
        "output_requirements": task_packet.get("output_requirements", []),
    }


def main():
    parser = argparse.ArgumentParser(description="Stage 1: parse task + recruit + planning")
    parser.add_argument("text", help="Raw /mac text")
    parser.add_argument("--main-agent", default="main-ceo")
    parser.add_argument("--pool-agent", default="pool-hr")
    parser.add_argument("--inspect-agent", default="inspect-patrol")
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

    pool_result = run_openclaw_agent(
        args.pool_agent,
        "你是AgentPool。请用 JSON 输出分工："
        '{"role":"","why":"","plan":[""]}'
        + "\n\n"
        + json.dumps({"task": compact, "group_plan": group_plan}, ensure_ascii=False),
        timeout=240,
    )
    inspect_result = run_openclaw_agent(
        args.inspect_agent,
        "你是检查Agent。请用 JSON 输出巡检策略："
        '{"watch":[""],"stale_rule":"","recover":[""]}',
        timeout=240,
    )

    state = {
        "stage": "stage1_done",
        "task_packet": compact,
        "group_plan": group_plan,
        "pool_result": pool_result,
        "inspect_result": inspect_result,
        "worker_role": (task_packet.get("specialists") or ["Generalist"])[0],
    }
    write_json(state_path, state)
    print(json.dumps({"status": "ok", "stage": state["stage"], "outdir": str(outdir)}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
