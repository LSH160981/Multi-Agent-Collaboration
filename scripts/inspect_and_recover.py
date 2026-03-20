#!/usr/bin/env python3
import argparse
import json
import subprocess
from pathlib import Path
from runtime_lib import run_openclaw_agent

REPO = Path(__file__).resolve().parent.parent


def main():
    parser = argparse.ArgumentParser(description="Inspect agents and optionally send recovery nudges through real OpenClaw agents")
    parser.add_argument("workspace", help="OpenClaw workspace path")
    parser.add_argument("--stale-minutes", type=int, default=30)
    parser.add_argument("--recovery-agent-map", help="JSON file mapping directory names to OpenClaw agent ids")
    parser.add_argument("--execute", action="store_true", help="Actually send recovery nudges")
    args = parser.parse_args()

    inspect_cmd = [str(REPO / "scripts" / "inspect_agents.py"), args.workspace, "--stale-minutes", str(args.stale_minutes)]
    report = json.loads(subprocess.check_output(inspect_cmd, text=True))

    agent_map = {}
    if args.recovery_agent_map:
        agent_map = json.loads(Path(args.recovery_agent_map).read_text(encoding="utf-8"))

    actions = []
    for item in report.get("reports", []):
        if item["status"] in {"stale", "watch"}:
            action = {
                "agent_dir": item["agent"],
                "issues": item["issues"],
                "suggestion": "发送唤醒消息并检查未完成任务"
            }
            if args.execute and item["agent"] in agent_map:
                message = "你被检查Agent判定为需要恢复，请检查你的日志、队列和未完成任务，并立即汇报当前状态。"
                action["runtime_result"] = run_openclaw_agent(agent_map[item["agent"]], message)
            actions.append(action)

    print(json.dumps({"report": report, "actions": actions}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
