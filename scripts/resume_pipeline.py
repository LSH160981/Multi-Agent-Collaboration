#!/usr/bin/env python3
import argparse
import json
import subprocess
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
PY = "python3"


def main():
    parser = argparse.ArgumentParser(description="Resume staged runtime pipeline from pipeline-state.json")
    parser.add_argument("state_json", help="pipeline-state.json path")
    parser.add_argument("--main-agent", default="main-ceo")
    parser.add_argument("--pool-agent", default="pool-hr")
    parser.add_argument("--inspect-agent", default="inspect-patrol")
    parser.add_argument("--review-agent", default="review-judge")
    parser.add_argument("--worker-agent-a", default="exec-worker-1")
    parser.add_argument("--worker-agent-b", default="")
    args = parser.parse_args()

    state_path = Path(args.state_json)
    if not state_path.exists():
        raise SystemExit(f"state file not found: {state_path}")

    state = json.loads(state_path.read_text(encoding="utf-8"))
    stage = state.get("stage")

    if stage == "stage1_done":
        subprocess.check_call([
            PY,
            str(REPO / "scripts" / "stage2_workers.py"),
            str(state_path),
            "--worker-agent-a", args.worker_agent_a,
            "--worker-agent-b", args.worker_agent_b,
        ])
        state = json.loads(state_path.read_text(encoding="utf-8"))
        stage = state.get("stage")

    if stage == "stage2_done":
        subprocess.check_call([
            PY,
            str(REPO / "scripts" / "stage3_review_final.py"),
            str(state_path),
            "--main-agent", args.main_agent,
            "--review-agent", args.review_agent,
            "--inspect-agent", args.inspect_agent,
        ])

    print(state_path)


if __name__ == "__main__":
    main()
