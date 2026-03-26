#!/usr/bin/env python3
"""test_stage3_smoke.py

Smoke test for stage3 review/final.

改进点：
- 不再假设外部已经手工准备好 state_json。
- 如果目标 state_json 不存在，可自动先运行 stage1 + stage2 生成前置状态。
- 这样 stage3 smoke 本身就是一条更完整、可回归的测试链。
"""

import argparse
import json
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
PY = "python3"
DEFAULT_TASK = "/mac 调研 OpenClaw 多agent 协同方案，给出结构化建议"


def ensure_state_ready(state_path: Path, args) -> dict:
    """Ensure stage2 state exists before stage3 smoke runs."""
    if state_path.exists():
        try:
            state = json.loads(state_path.read_text(encoding="utf-8"))
            if state.get("stage") in {"stage2_done", "stage3_done"}:
                return {
                    "prepared": False,
                    "reason": f"existing state stage={state.get('stage')}",
                }
        except json.JSONDecodeError:
            pass

    state_path.parent.mkdir(parents=True, exist_ok=True)
    cmd = [
        PY,
        str(REPO / "scripts" / "run_staged_pipeline.py"),
        args.task,
        "--main-agent", args.main_agent,
        "--pool-agent", args.pool_agent,
        "--inspect-agent", args.inspect_agent,
        "--review-agent", args.review_agent,
        "--worker-agent-a", args.worker_agent_a,
        "--worker-agent-b", args.worker_agent_b,
        "--outdir", str(state_path.parent),
        "--stop-after", "stage2",
    ]
    proc = subprocess.run(cmd, capture_output=True, text=True)
    return {
        "prepared": True,
        "command": cmd,
        "exit_code": proc.returncode,
        "stdout": proc.stdout[-4000:],
        "stderr": proc.stderr[-4000:],
    }


def main():
    parser = argparse.ArgumentParser(description="Smoke test for stage3 review/final")
    parser.add_argument("state_json", nargs="?", default=str(REPO / "examples" / "generated" / "staged-runtime" / "pipeline-state.json"), help="pipeline-state.json path")
    parser.add_argument("--task", default=DEFAULT_TASK, help="用于自动准备 stage1/stage2 前置状态的任务")
    parser.add_argument("--main-agent", default="main-ceo")
    parser.add_argument("--pool-agent", default="pool-hr")
    parser.add_argument("--review-agent", default="review-judge")
    parser.add_argument("--inspect-agent", default="inspect-patrol")
    parser.add_argument("--worker-agent-a", default="exec-worker-1")
    parser.add_argument("--worker-agent-b", default="")
    args = parser.parse_args()

    state_path = Path(args.state_json)
    prep = ensure_state_ready(state_path, args)

    if prep.get("prepared") and prep.get("exit_code") != 0:
        print(json.dumps({
            "status": "error",
            "stage": "prepare_stage2_failed",
            "state_json": str(state_path),
            "prepare": prep,
        }, ensure_ascii=False, indent=2))
        sys.exit(1)

    cmd = [
        PY,
        str(REPO / "scripts" / "stage3_review_final.py"),
        str(state_path),
        "--main-agent", args.main_agent,
        "--review-agent", args.review_agent,
        "--inspect-agent", args.inspect_agent,
    ]
    proc = subprocess.run(cmd, capture_output=True, text=True)

    if proc.returncode != 0:
        print(json.dumps({
            "status": "error",
            "stage": "stage3_failed",
            "state_json": str(state_path),
            "prepare": prep,
            "command": cmd,
            "stdout": proc.stdout[-4000:],
            "stderr": proc.stderr[-4000:],
        }, ensure_ascii=False, indent=2))
        sys.exit(proc.returncode)

    state = json.loads(state_path.read_text(encoding="utf-8"))
    checks = {
        "status": "ok",
        "state_json": str(state_path),
        "prepare": prep,
        "stage": state.get("stage"),
        "has_review_result": "review_result" in state,
        "has_final_result": "final_result" in state,
        "has_session_probe": "session_probe" in state,
    }
    print(json.dumps(checks, ensure_ascii=False, indent=2))
    sys.exit(0 if checks["stage"] == "stage3_done" and checks["has_review_result"] and checks["has_final_result"] and checks["has_session_probe"] else 1)


if __name__ == "__main__":
    main()
