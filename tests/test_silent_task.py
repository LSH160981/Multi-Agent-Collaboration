#!/usr/bin/env python3
import argparse
import json
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "scripts"))

from runtime_lib import write_json

DEFAULT_TASK = "/mac 搜索 GitHub 最近 7 天 star 涨得最快的 10 个项目，总结共同特点。"


def main():
    parser = argparse.ArgumentParser(description="Silent task regression test for Multi-Agent-Collaboration")
    parser.add_argument("--task", default=DEFAULT_TASK)
    parser.add_argument("--main-agent", default="main-ceo")
    parser.add_argument("--pool-agent", default="pool-hr")
    parser.add_argument("--review-agent", default="review-judge")
    parser.add_argument("--inspect-agent", default="inspect-patrol")
    parser.add_argument("--outdir", default=str(REPO / "examples" / "generated" / "tests" / "silent-task"))
    args = parser.parse_args()

    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    cmd = [
        str(REPO / "scripts" / "runtime_sessions.py"),
        args.task,
        "--main-agent", args.main_agent,
        "--pool-agent", args.pool_agent,
        "--review-agent", args.review_agent,
        "--inspect-agent", args.inspect_agent,
        "--outdir", str(outdir),
    ]
    subprocess.check_call(cmd)

    expected = [
        outdir / "task-packet.json",
        outdir / "group-plan.json",
        outdir / "native-session-results.json",
    ]
    report = {
        "task": args.task,
        "outdir": str(outdir),
        "checks": [{"path": str(p), "exists": p.exists()} for p in expected],
    }
    write_json(outdir / "silent-task-report.json", report)
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
