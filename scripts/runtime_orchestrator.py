#!/usr/bin/env python3
import argparse
import json
import subprocess
from pathlib import Path
from runtime_lib import run_openclaw_agent, write_json

REPO = Path(__file__).resolve().parent.parent


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

    subprocess.check_call([str(REPO / "scripts" / "mac_cli.py"), args.text, "--output", str(task_packet_path)])
    subprocess.check_call([str(REPO / "scripts" / "recruit_team.py"), str(task_packet_path), "--output", str(group_plan_path)])

    task_packet = json.loads(task_packet_path.read_text(encoding="utf-8"))
    group_plan = json.loads(group_plan_path.read_text(encoding="utf-8"))

    results = {
        "main_agent": run_openclaw_agent(args.main_agent, f"你是主Agent，请阅读并确认任务包：\n{json.dumps(task_packet, ensure_ascii=False, indent=2)}"),
        "pool_agent": run_openclaw_agent(args.pool_agent, f"你是AgentPool，请阅读并确认编组方案：\n{json.dumps(group_plan, ensure_ascii=False, indent=2)}"),
        "review_agent": run_openclaw_agent(args.review_agent, "你是审核Agent，请等待后续结果包并准备评分。"),
        "inspect_agent": run_openclaw_agent(args.inspect_agent, "你是检查Agent，请启动巡检，关注是否存在 stale agent 与未推进任务。"),
    }

    write_json(outdir / "runtime-results.json", results)
    print(json.dumps({"status": "ok", "outdir": str(outdir)}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
