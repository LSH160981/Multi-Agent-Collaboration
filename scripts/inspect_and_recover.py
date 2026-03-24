#!/usr/bin/env python3
import argparse
import json
import subprocess
from pathlib import Path
from runtime_lib import build_recovery_message, newest_session_for_agent, run_openclaw_agent

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
            mapped_agent_id = agent_map.get(item["agent"])
            session_info = newest_session_for_agent(mapped_agent_id) if mapped_agent_id else None
            action = {
                "agent_dir": item["agent"],
                "mapped_agent_id": mapped_agent_id,
                "issues": item["issues"],
                "latest_session": session_info,
                "suggestion": "发送唤醒消息并检查未完成任务；必要时重派或重建",
            }
            if args.execute and mapped_agent_id:
                message = build_recovery_message(item["agent"], item["issues"], session_info)
                action["runtime_result"] = run_openclaw_agent(mapped_agent_id, message)
            actions.append(action)

    print(json.dumps({"report": report, "actions": actions}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
