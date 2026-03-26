#!/usr/bin/env python3
"""test_runtime_orchestrator_smoke.py

runtime_orchestrator 的烟雾测试。

测试目标：
- 脚本可执行
- 关键产物文件能落盘
- runtime-results.json 中关键字段完整
- 最终阶段能收敛到 stage3_done

说明：
- 这是偏集成测试的 smoke，不是纯单元测试。
- 失败时尽量保留 stdout/stderr 与中间结果，便于回溯。
"""

import argparse
import json
import subprocess
import sys
import time
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
DEFAULT_RUNTIME_DIR = REPO / "examples" / "generated" / "runtime"


def load_runtime_results(runtime_path: Path):
    if not runtime_path.exists():
        return {}
    try:
        return json.loads(runtime_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}


def wait_for_final_runtime(runtime_path: Path, timeout_seconds: int = 30, interval_seconds: float = 0.5):
    started = time.time()
    latest = load_runtime_results(runtime_path)
    while time.time() - started < timeout_seconds:
        latest = load_runtime_results(runtime_path)
        if latest.get("status") == "ok" and latest.get("stage") == "stage3_done":
            return latest, round(time.time() - started, 2)
        time.sleep(interval_seconds)
    return latest, round(time.time() - started, 2)


def main():
    parser = argparse.ArgumentParser(description="Smoke test for runtime_orchestrator")
    parser.add_argument("--task", default="/mac 调研 OpenClaw 多agent 协同方案，给出结构化建议")
    parser.add_argument("--main-agent", default="main-ceo")
    parser.add_argument("--pool-agent", default="pool-hr")
    parser.add_argument("--review-agent", default="review-judge")
    parser.add_argument("--inspect-agent", default="inspect-patrol")
    parser.add_argument("--worker-agent-a", default="exec-worker-1")
    parser.add_argument("--worker-agent-b", default="exec-worker-2")
    parser.add_argument("--outdir", default=str(REPO / "examples" / "generated" / "tests" / "runtime-orchestrator"))
    args = parser.parse_args()

    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    cmd = [
        "python3", str(REPO / "scripts" / "runtime_orchestrator.py"),
        args.task,
        "--main-agent", args.main_agent,
        "--pool-agent", args.pool_agent,
        "--review-agent", args.review_agent,
        "--inspect-agent", args.inspect_agent,
        "--worker-agent-a", args.worker_agent_a,
        "--worker-agent-b", args.worker_agent_b,
        "--outdir", str(outdir),
    ]

    proc = subprocess.run(cmd, capture_output=True, text=True)

    expected = [
        outdir / "task-packet.json",
        outdir / "group-plan.json",
        outdir / "staffing-decision.json",
        outdir / "runtime-results.json",
    ]

    runtime_path = outdir / "runtime-results.json"
    runtime_results, wait_seconds = wait_for_final_runtime(runtime_path)

    required_runtime_keys = [
        "task_packet",
        "group_plan",
        "staffing",
        "inspection_result",
        "review_result",
        "final_result",
        "session_probe",
        "stage",
        "resume_recommendation",
    ]
    required_non_null = [
        "inspection_result",
        "review_result",
        "final_result",
        "session_probe",
        "stage",
        "resume_recommendation",
    ]

    missing_keys = [k for k in required_runtime_keys if k not in runtime_results]
    null_keys = [k for k in required_non_null if runtime_results.get(k) is None]
    stage_ok = runtime_results.get("stage") == "stage3_done"
    status_ok = runtime_results.get("status") == "ok"

    report = {
        "task": args.task,
        "outdir": str(outdir),
        "default_runtime_dir": str(DEFAULT_RUNTIME_DIR),
        "command_exit_code": proc.returncode,
        "command_stdout": proc.stdout[-4000:],
        "command_stderr": proc.stderr[-4000:],
        "waited_for_final_seconds": wait_seconds,
        "checks": [{"path": str(p), "exists": p.exists()} for p in expected],
        "runtime_result_checks": {
            "present_keys": sorted(runtime_results.keys()),
            "required_keys": required_runtime_keys,
            "missing_keys": missing_keys,
            "required_non_null": required_non_null,
            "null_keys": null_keys,
            "stage": runtime_results.get("stage"),
            "status": runtime_results.get("status"),
            "stage_ok": stage_ok,
            "status_ok": status_ok,
        },
    }
    report_text = json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    (outdir / "runtime-orchestrator-smoke-report.json").write_text(report_text, encoding="utf-8")
    DEFAULT_RUNTIME_DIR.mkdir(parents=True, exist_ok=True)
    (DEFAULT_RUNTIME_DIR / "runtime-orchestrator-smoke-report.json").write_text(report_text, encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))

    files_ok = all(p.exists() for p in expected)
    success = proc.returncode == 0 and files_ok and not missing_keys and not null_keys and stage_ok and status_ok
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
