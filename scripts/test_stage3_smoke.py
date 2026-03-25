#!/usr/bin/env python3
import argparse
import json
import subprocess
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent


def main():
    parser = argparse.ArgumentParser(description="Smoke test for stage3 review/final")
    parser.add_argument("state_json", help="pipeline-state.json path")
    parser.add_argument("--main-agent", default="main-ceo")
    parser.add_argument("--review-agent", default="review-judge")
    parser.add_argument("--inspect-agent", default="inspect-patrol")
    args = parser.parse_args()

    cmd = [
        "python3", str(REPO / "scripts" / "stage3_review_final.py"),
        args.state_json,
        "--main-agent", args.main_agent,
        "--review-agent", args.review_agent,
        "--inspect-agent", args.inspect_agent,
    ]
    subprocess.check_call(cmd)

    state = json.loads(Path(args.state_json).read_text(encoding="utf-8"))
    checks = {
        "stage": state.get("stage"),
        "has_review_result": "review_result" in state,
        "has_final_result": "final_result" in state,
        "has_session_probe": "session_probe" in state,
    }
    print(json.dumps(checks, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
