#!/usr/bin/env python3
"""recruit_team.py

根据任务包生成编组方案。

职责：
- 基于 task_type 和 execution_mode 生成单组或双组结构。
- 为组长和 specialist 赋予基础角色边界。
- 输出 group_plan，供 staffing、runtime、review 链路复用。
"""

import argparse
import json
from pathlib import Path

ROLE_MAP = {
    "coding": ["Frontend", "Test", "Verification"],
    "research": ["Research", "Verification", "Summary"],
    "ops": ["LogAnalysis", "Recovery", "Verification"],
    "mixed": ["Research", "Implementation", "Verification"],
}


def build_group(group_name: str, task_type: str, strategy: str):
    specialists = ROLE_MAP.get(task_type, ROLE_MAP["mixed"])
    members = [{"name": f"{group_name}组长-Lead", "role": "Lead", "boundary": "组内汇总，不直接联系用户"}]
    for role in specialists:
        members.append({
            "name": f"{group_name}组-{role}",
            "role": role,
            "boundary": "只处理分配任务，不直接联系用户",
        })
    return {"group": group_name, "strategy": strategy, "members": members}


def build_group_plan(packet: dict) -> dict:
    task_type = packet.get("task_type", "mixed")
    execution_mode = packet.get("execution_mode", "single-group")
    groups = [build_group("A", task_type, "stable")]
    if execution_mode == "dual-group":
        groups.append(build_group("B", task_type, "aggressive"))
    return {
        "task_id": packet["task_id"],
        "task_type": task_type,
        "execution_mode": execution_mode,
        "groups": groups,
    }


def main():
    parser = argparse.ArgumentParser(description="Generate group plan from task type and execution mode")
    parser.add_argument("task_packet", help="Path to task packet JSON")
    parser.add_argument("--output", help="Optional output JSON path")
    args = parser.parse_args()

    packet = json.loads(Path(args.task_packet).read_text(encoding="utf-8"))
    result = build_group_plan(packet)
    rendered = json.dumps(result, ensure_ascii=False, indent=2)
    if args.output:
        Path(args.output).write_text(rendered + "\n", encoding="utf-8")
    print(rendered)


if __name__ == "__main__":
    main()
