#!/usr/bin/env python3
import argparse
import json
from pathlib import Path


def required_for_stage(stage: str):
    common = ["stage", "task_packet"]
    stage1 = common + [
        "group_plan", "agent_map", "dispatch_hints", "pool_result", "inspect_result",
        "worker_role", "session_probe_before", "resume_recommendation"
    ]
    stage2 = stage1 + [
        "worker_agent_a", "worker_a_result", "session_probe_after_workers"
    ]
    stage3 = stage2 + ["review_result", "final_result", "session_probe"]
    mapping = {
        "stage1_done": stage1,
        "stage2_done": stage2,
        "stage3_done": stage3,
    }
    return mapping.get(stage, common)


def main():
    parser = argparse.ArgumentParser(description="Validate pipeline-state.json with lightweight built-in rules")
    parser.add_argument("state_json")
    args = parser.parse_args()

    path = Path(args.state_json)
    data = json.loads(path.read_text(encoding="utf-8"))
    stage = data.get("stage")
    missing = [k for k in required_for_stage(stage) if k not in data]
    nested_issues = []
    if isinstance(data.get("task_packet"), dict):
        for key in ["task_id", "goal", "task_type"]:
            if key not in data["task_packet"]:
                nested_issues.append(f"task_packet.{key}")
    else:
        nested_issues.append("task_packet")

    result = {
        "stage": stage,
        "valid": not missing and not nested_issues,
        "missing": missing,
        "nested_issues": nested_issues,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    if missing or nested_issues:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
