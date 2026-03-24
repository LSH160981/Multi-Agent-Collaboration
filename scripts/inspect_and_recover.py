#!/usr/bin/env python3
import argparse
import json
import subprocess
from pathlib import Path
from runtime_lib import build_recovery_message, newest_session_for_agent, run_openclaw_agent

REPO = Path(__file__).resolve().parent.parent


def inspect_pipeline_state(workspace: str):
    state_path = Path(workspace) / "Multi-Agent-Collaboration" / "examples" / "generated" / "staged-runtime" / "pipeline-state.json"
    alt_state_path = REPO / "examples" / "generated" / "staged-runtime" / "pipeline-state.json"
    path = state_path if state_path.exists() else alt_state_path
    if not path.exists():
        return None
    data = json.loads(path.read_text(encoding="utf-8"))
    stage = data.get("stage")
    stage_issue = None
    if stage in {"stage1_done", "stage2_done"}:
        stage_issue = f"staged pipeline 停在 {stage}，可继续后续阶段"
    return {"path": str(path), "stage": stage, "issue": stage_issue}


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

    pipeline_state = inspect_pipeline_state(args.workspace)
    actions = []

    if pipeline_state and pipeline_state.get("issue"):
        actions.append({
            "type": "pipeline_resume",
            "stage": pipeline_state.get("stage"),
            "state_path": pipeline_state.get("path"),
            "suggestion": "运行 resume_pipeline.py 从当前阶段继续",
        })

    for item in report.get("reports", []):
        if item["status"] in {"stale", "watch"}:
            mapped_agent_id = agent_map.get(item["agent"])
            session_info = newest_session_for_agent(mapped_agent_id) if mapped_agent_id else None
            action = {
                "type": "agent_recover",
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

    print(json.dumps({"report": report, "pipeline_state": pipeline_state, "actions": actions}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
