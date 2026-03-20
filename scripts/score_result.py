#!/usr/bin/env python3
import argparse
import json
from pathlib import Path


def score(payload: dict):
    completeness = min(10, len(payload.get("artifacts", [])) * 3 + len(payload.get("verification", [])) * 2)
    quality = 20 if payload.get("summary") else 0
    quality += 10 if not payload.get("risks") else 6
    metrics = min(10, len(payload.get("verification", [])) * 3 + (0 if payload.get("risks") else 2))
    total = completeness + quality + metrics
    decision = "pass" if total >= 28 else "reject"
    return {
        "task_id": payload["task_id"],
        "group": payload.get("group", "UNKNOWN"),
        "reviewer_score": completeness,
        "judge_score": quality,
        "metrics_score": metrics,
        "total_score": total,
        "decision": decision,
        "notes": "自动评分结果（原型）"
    }


def main():
    parser = argparse.ArgumentParser(description="Score a result package into a scorecard")
    parser.add_argument("result_json", help="Path to result JSON")
    parser.add_argument("--output", help="Optional output path")
    args = parser.parse_args()
    payload = json.loads(Path(args.result_json).read_text(encoding="utf-8"))
    result = score(payload)
    rendered = json.dumps(result, ensure_ascii=False, indent=2)
    if args.output:
        Path(args.output).write_text(rendered + "\n", encoding="utf-8")
    print(rendered)


if __name__ == "__main__":
    main()
