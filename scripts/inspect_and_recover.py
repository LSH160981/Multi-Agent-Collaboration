#!/usr/bin/env python3
import argparse
import json
import subprocess
from pathlib import Path
from runtime_lib import build_recovery_message, newest_session_for_agent, run_openclaw_agent

REPO = Path(__file__).resolve().parent.parent
PY = "python3"


def state_candidates(workspace: str):
    return [
        Path(workspace) / "Multi-Agent-Collaboration" / "examples" / "generated" / "staged-runtime" / "pipeline-state.json",
        REPO / "examples" / "generated" / "staged-runtime" / "pipeline-state.json",
    ]


def validate_state(path: Path):
    cmd = [PY, str(REPO / 'scripts' / 'validate_pipeline_state.py'), str(path)]
    try:
        out = subprocess.check_output(cmd, text=True, stderr=subprocess.STDOUT)
        return json.loads(out)
    except subprocess.CalledProcessError as e:
        try:
            return json.loads(e.output)
        except Exception:
            return {"stage": None, "valid": False, "missing": ["unknown"]}


def inspect_pipeline_state(workspace: str):
    path = next((p for p in state_candidates(workspace) if p.exists()), None)
    if not path:
        return None
    data = json.loads(path.read_text(encoding="utf-8"))
    stage = data.get("stage")
    fields = set(data.keys())
    precise_action = None
    issue = None
    repair_action = None

    if stage == "stage1_done":
        precise_action = f"{PY} {REPO / 'scripts' / 'stage2_workers.py'} {path} --worker-agent-b exec-worker-2"
        issue = "stage1 已完成，等待 worker 执行"
    elif stage == "stage2_done":
        precise_action = f"{PY} {REPO / 'scripts' / 'stage3_review_final.py'} {path}"
        issue = "stage2 已完成，等待 review/final"
    elif stage == "stage3_done":
        issue = None
    else:
        issue = f"未知 stage: {stage}"
        repair_action = f"{PY} {REPO / 'scripts' / 'repair_pipeline_state.py'} {path} --set-stage stage1_done --note 修复未知stage"

    if stage == "stage2_done" and not {"worker_a_result", "worker_agent_a"}.issubset(fields):
        issue = "stage2 状态不完整，建议重跑 stage2_workers.py"
        precise_action = f"{PY} {REPO / 'scripts' / 'stage2_workers.py'} {path} --worker-agent-b exec-worker-2"
    if stage == "stage3_done" and not {"review_result", "final_result", "session_probe"}.issubset(fields):
        issue = "stage3 状态不完整，建议重跑 stage3_review_final.py"
        precise_action = f"{PY} {REPO / 'scripts' / 'stage3_review_final.py'} {path}"

    validation = validate_state(path)
    valid = validation.get("valid", True)
    missing = validation.get("missing", [])
    if not valid and not repair_action:
        repair_action = f"{PY} {REPO / 'scripts' / 'repair_pipeline_state.py'} {path} --note 缺少字段:{','.join(missing)}"
        issue = issue or f"pipeline-state 缺少字段: {missing}"

    return {
        "path": str(path),
        "stage": stage,
        "issue": issue,
        "precise_action": precise_action,
        "repair_action": repair_action,
        "valid": valid,
        "missing": missing,
    }


def maybe_run(cmd_str: str):
    return subprocess.check_output(cmd_str, shell=True, text=True, stderr=subprocess.STDOUT)


def recommend_session_action(session_info, stale_minutes: int):
    if session_info is None:
        return "rebuild"
    age_ms = session_info.get("ageMs")
    if age_ms is None:
        return "probe"
    age_minutes = age_ms / 60000.0
    if age_minutes <= stale_minutes:
        return "resume"
    if age_minutes <= stale_minutes * 4:
        return "redispatch"
    return "rebuild"


def infer_role_kind(agent_dir_name: str) -> str:
    lowered = agent_dir_name.lower()
    if "research" in lowered or "调研" in agent_dir_name:
        return "research"
    if "test" in lowered or "verify" in lowered or "检查" in agent_dir_name:
        return "test"
    if "front" in lowered or "ui" in lowered:
        return "frontend"
    return "general"


def build_rebuild_command(workspace: str, agent_dir_name: str) -> str:
    role_kind = infer_role_kind(agent_dir_name)
    return f'{PY} {REPO / "scripts" / "rebuild_agent.py"} "{workspace}" "{agent_dir_name}" --role-name "{agent_dir_name}" --role-kind {role_kind}'


def main():
    parser = argparse.ArgumentParser(description="Inspect agents and optionally send recovery nudges through real OpenClaw agents")
    parser.add_argument("workspace", help="OpenClaw workspace path")
    parser.add_argument("--stale-minutes", type=int, default=30)
    parser.add_argument("--recovery-agent-map", help="JSON file mapping directory names to OpenClaw agent ids")
    parser.add_argument("--execute", action="store_true", help="Actually send recovery nudges")
    parser.add_argument("--auto-resume-pipeline", action="store_true", help="Automatically execute precise pipeline resume action when available")
    parser.add_argument("--auto-repair-pipeline", action="store_true", help="Automatically execute pipeline repair action when available")
    args = parser.parse_args()

    inspect_cmd = [str(REPO / "scripts" / "inspect_agents.py"), args.workspace, "--stale-minutes", str(args.stale_minutes)]
    report = json.loads(subprocess.check_output(inspect_cmd, text=True))

    agent_map = {}
    if args.recovery_agent_map:
        agent_map = json.loads(Path(args.recovery_agent_map).read_text(encoding="utf-8"))

    pipeline_state = inspect_pipeline_state(args.workspace)
    actions = []

    if pipeline_state and pipeline_state.get("issue"):
        action = {
            "type": "pipeline_resume",
            "stage": pipeline_state.get("stage"),
            "state_path": pipeline_state.get("path"),
            "suggestion": pipeline_state.get("issue"),
            "precise_action": pipeline_state.get("precise_action"),
            "repair_action": pipeline_state.get("repair_action"),
            "valid_before": pipeline_state.get("valid"),
            "missing_before": pipeline_state.get("missing"),
        }
        state_path = Path(pipeline_state["path"])
        if args.auto_repair_pipeline and pipeline_state.get("repair_action"):
            action["repair_result"] = maybe_run(pipeline_state["repair_action"])
            action["validation_after_repair"] = validate_state(state_path)
        if args.auto_resume_pipeline and pipeline_state.get("precise_action"):
            action["resume_result"] = maybe_run(pipeline_state["precise_action"])
            action["state_after_resume"] = json.loads(state_path.read_text(encoding="utf-8")) if state_path.exists() else None
            action["validation_after_resume"] = validate_state(state_path) if state_path.exists() else None
        actions.append(action)

    for item in report.get("reports", []):
        if item["status"] in {"stale", "watch"}:
            mapped_agent_id = agent_map.get(item["agent"])
            session_info = newest_session_for_agent(mapped_agent_id) if mapped_agent_id else None
            recommended_action = recommend_session_action(session_info, args.stale_minutes)
            suggestion_map = {
                "probe": "先观察 session 细节并确认是否真的卡住",
                "resume": "优先续跑现有 session，避免重复派单",
                "redispatch": "session 偏旧，优先重派当前任务并保留旧 session 供审计",
                "rebuild": "session 长期 stale 或缺失，优先重建链路",
            }
            action = {
                "type": "agent_recover",
                "agent_dir": item["agent"],
                "mapped_agent_id": mapped_agent_id,
                "issues": item["issues"],
                "latest_session": session_info,
                "recommended_action": recommended_action,
                "suggestion": suggestion_map[recommended_action],
                "rebuild_command": build_rebuild_command(args.workspace, item["agent"]) if recommended_action == "rebuild" else None,
            }
            if args.execute and mapped_agent_id:
                message = build_recovery_message(item["agent"], item["issues"], session_info)
                action["runtime_result"] = run_openclaw_agent(mapped_agent_id, message)
            actions.append(action)

    print(json.dumps({"report": report, "pipeline_state": pipeline_state, "actions": actions}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
