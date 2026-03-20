#!/usr/bin/env python3
import argparse
import json
from pathlib import Path

ROLE_MAP = {
    "coding": ["Frontend", "Test", "Verification"],
    "research": ["Research", "Verification", "Summary"],
    "ops": ["LogAnalysis", "Recovery", "Verification"],
    "mixed": ["Research", "Implementation", "Verification"],
}


def build_group(group_name: str, task_type: str):
    specialists = ROLE_MAP.get(task_type, ROLE_MAP["mixed"])
    members = [{"name": f"{group_name}组长-Lead", "role": "Lead"}]
    for role in specialists:
        members.append({"name": f"{group_name}组-{role}", "role": role})
    return {"group": group_name, "members": members}


def main():
    parser = argparse.ArgumentParser(description="Generate A/B group plan from task type")
    parser.add_argument("task_packet", help="Path to task packet JSON")
    parser.add_argument("--output", help="Optional output JSON path")
    args = parser.parse_args()

    packet = json.loads(Path(args.task_packet).read_text(encoding="utf-8"))
    task_type = packet.get("task_type", "mixed")
    result = {
        "task_id": packet["task_id"],
        "task_type": task_type,
        "groups": [build_group("A", task_type), build_group("B", task_type)]
    }
    rendered = json.dumps(result, ensure_ascii=False, indent=2)
    if args.output:
        Path(args.output).write_text(rendered + "\n", encoding="utf-8")
    print(rendered)


if __name__ == "__main__":
    main()
