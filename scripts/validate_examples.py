#!/usr/bin/env python3
import json
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def validate_task_state(data: dict):
    required = ["task_id", "title", "status", "goal"]
    missing = [k for k in required if k not in data]
    return missing


def validate_agent_state(data: dict):
    required = ["agent_name", "role", "status"]
    missing = [k for k in required if k not in data]
    return missing


def validate_scorecard(data: dict):
    required = ["task_id", "group", "total_score", "decision"]
    missing = [k for k in required if k not in data]
    return missing


def main():
    failures = []

    queue_example = load_json(REPO / "examples/queue-example.json")
    missing = validate_task_state(queue_example)
    if missing:
        failures.append(("examples/queue-example.json", missing))

    agent_example = load_json(REPO / "examples/agent-state-example.json")
    missing = validate_agent_state(agent_example)
    if missing:
        failures.append(("examples/agent-state-example.json", missing))

    score_example = load_json(REPO / "examples/scorecard-example.json")
    missing = validate_scorecard(score_example)
    if missing:
        failures.append(("examples/scorecard-example.json", missing))

    for path in sorted((REPO / "examples/json").glob("*.json")):
        load_json(path)

    if failures:
        print("校验失败：")
        for path, missing in failures:
            print(f"- {path}: 缺少字段 {missing}")
        raise SystemExit(1)

    print("所有核心示例 JSON 校验通过")


if __name__ == "__main__":
    main()
