#!/usr/bin/env python3
import argparse
import json
from pathlib import Path


def ensure_stage_shape(data: dict, stage: str):
    data.setdefault("task_packet", {"task_id": "UNKNOWN", "goal": "REPAIR_REQUIRED", "task_type": "mixed"})
    data.setdefault("group_plan", {})
    data.setdefault("agent_map", {})
    data.setdefault("dispatch_hints", {})
    data.setdefault("pool_result", {})
    data.setdefault("inspect_result", {})
    data.setdefault("worker_role", "Generalist")
    data.setdefault("session_probe_before", {})
    data.setdefault("resume_recommendation", {})

    if stage in {"stage2_done", "stage3_done"}:
        data.setdefault("worker_agent_a", "exec-worker-1")
        data.setdefault("worker_a_result", {})
        data.setdefault("session_probe_after_workers", {})
    if stage == "stage3_done":
        data.setdefault("review_result", {})
        data.setdefault("final_result", {})
        data.setdefault("session_probe", {})
    return data


def main():
    parser = argparse.ArgumentParser(description="Repair pipeline-state.json minimal fields")
    parser.add_argument("state_json")
    parser.add_argument("--set-stage", choices=["stage1_done", "stage2_done", "stage3_done"])
    parser.add_argument("--note", default="auto repair")
    args = parser.parse_args()

    path = Path(args.state_json)
    data = json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}

    if args.set_stage:
        data["stage"] = args.set_stage
    stage = data.get("stage", "stage1_done")
    ensure_stage_shape(data, stage)
    data["repair_note"] = args.note

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": "ok", "path": str(path), "stage": data.get("stage"), "repair_note": data.get("repair_note")}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
