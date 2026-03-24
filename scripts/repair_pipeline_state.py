#!/usr/bin/env python3
import argparse
import json
from pathlib import Path


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
    data.setdefault("task_packet", {"task_id": "UNKNOWN", "goal": "REPAIR_REQUIRED", "task_type": "mixed"})
    data["repair_note"] = args.note

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": "ok", "path": str(path), "stage": data.get("stage"), "repair_note": data.get("repair_note")}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
