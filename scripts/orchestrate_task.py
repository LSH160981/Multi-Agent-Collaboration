#!/usr/bin/env python3
import argparse
import json
import subprocess
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent


def run_json(cmd):
    out = subprocess.check_output(cmd, text=True)
    return json.loads(out)


def main():
    parser = argparse.ArgumentParser(description="Prototype orchestrator: parse /mac -> recruit A/B -> write planning artifacts")
    parser.add_argument("text", help="Raw /mac text")
    parser.add_argument("--workspace", default=str(Path.home() / ".openclaw/workspace"))
    parser.add_argument("--outdir", default=str(REPO / "examples" / "generated" / "orchestrator"))
    args = parser.parse_args()

    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    task_packet_path = outdir / "task-packet.json"
    group_plan_path = outdir / "group-plan.json"

    subprocess.check_call([str(REPO / "scripts" / "mac_cli.py"), args.text, "--output", str(task_packet_path)])
    subprocess.check_call([str(REPO / "scripts" / "recruit_team.py"), str(task_packet_path), "--output", str(group_plan_path)])

    task = json.loads(task_packet_path.read_text(encoding="utf-8"))
    group_plan = json.loads(group_plan_path.read_text(encoding="utf-8"))

    plan = {
        "task": task,
        "group_plan": group_plan,
        "next_actions": [
            "主Agent 审核任务包是否需要补充澄清",
            "AgentPool 根据 group_plan 生成具体 specialist 目录",
            "主Agent 向 A/B 组长派单",
            "检查Agent 启动巡检"
        ]
    }
    (outdir / "orchestration-plan.json").write_text(json.dumps(plan, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": "ok", "outdir": str(outdir)}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
