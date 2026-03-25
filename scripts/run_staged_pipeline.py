#!/usr/bin/env python3
"""run_staged_pipeline.py

当前推荐的 staged pipeline 主入口。

职责：
- 统一驱动 stage1 / stage2 / stage3 三段式运行。
- 支持在任意阶段停下，方便调试、恢复和回归测试。
- 输出稳定的 pipeline-state.json 路径，供后续脚本继续处理。

说明：
- 相比早期原型脚本，这个文件更适合作为标准入口保留。
"""

import argparse
import subprocess
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
PY = "python3"


def main():
    parser = argparse.ArgumentParser(description="Unified staged runtime pipeline runner")
    parser.add_argument("text", help="Raw /mac text")
    parser.add_argument("--main-agent", default="main-ceo")
    parser.add_argument("--pool-agent", default="pool-hr")
    parser.add_argument("--inspect-agent", default="inspect-patrol")
    parser.add_argument("--review-agent", default="review-judge")
    parser.add_argument("--worker-agent-a", default="exec-worker-1")
    parser.add_argument("--worker-agent-b", default="")
    parser.add_argument("--outdir", default=str(REPO / "examples" / "generated" / "staged-runtime"))
    parser.add_argument("--stop-after", choices=["stage1", "stage2", "stage3"], default="stage3")
    args = parser.parse_args()

    outdir = Path(args.outdir)
    state_path = outdir / "pipeline-state.json"

    subprocess.check_call([
        PY,
        str(REPO / "scripts" / "stage1_plan.py"),
        args.text,
        "--main-agent", args.main_agent,
        "--pool-agent", args.pool_agent,
        "--inspect-agent", args.inspect_agent,
        "--review-agent", args.review_agent,
        "--worker-agent-a", args.worker_agent_a,
        "--worker-agent-b", args.worker_agent_b,
        "--outdir", str(outdir),
    ])
    if args.stop_after == "stage1":
        print(state_path)
        return

    subprocess.check_call([
        PY,
        str(REPO / "scripts" / "stage2_workers.py"),
        str(state_path),
        "--worker-agent-a", args.worker_agent_a,
        "--worker-agent-b", args.worker_agent_b,
    ])
    if args.stop_after == "stage2":
        print(state_path)
        return

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
