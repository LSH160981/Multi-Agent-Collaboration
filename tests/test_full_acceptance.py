#!/usr/bin/env python3
"""test_full_acceptance.py

Multi-Agent-Collaboration 一键全链路验收入口。

目标：
- 把“agent 两两互问 + 静默任务测试 + runtime orchestrator smoke + stage3 smoke + 恢复测试”串成一条统一回归链
- 统一产出 JSON 报告，便于人工审计与 CI / cron / install-selfcheck 后续接入
- 允许按需跳过依赖真实 agent 环境的阶段，避免在未完成安装时整条链直接不可用

说明：
- 这是仓库测试层入口，不是 OpenClaw 平台原生命令。
- 依赖真实 agent / session 的阶段仍以当前本机 OpenClaw 运行状态为准。
"""

import argparse
import json
import subprocess
import sys
import time
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
PY = "python3"
DEFAULT_TASK = "/mac 搜索 GitHub 最近 7 天 star 涨得最快的 10 个项目，总结共同特点。"


def run_step(name: str, cmd: list[str], timeout: int, cwd: Path | None = None) -> dict:
    started = time.time()
    try:
        proc = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout,
            cwd=str(cwd) if cwd else None,
        )
        duration = round(time.time() - started, 2)
        return {
            "name": name,
            "command": cmd,
            "timeout_seconds": timeout,
            "duration_seconds": duration,
            "exit_code": proc.returncode,
            "ok": proc.returncode == 0,
            "stdout": proc.stdout[-8000:],
            "stderr": proc.stderr[-8000:],
        }
    except subprocess.TimeoutExpired as exc:
        duration = round(time.time() - started, 2)
        return {
            "name": name,
            "command": cmd,
            "timeout_seconds": timeout,
            "duration_seconds": duration,
            "exit_code": None,
            "ok": False,
            "timed_out": True,
            "stdout": (exc.stdout or "")[-8000:] if isinstance(exc.stdout, str) else "",
            "stderr": (exc.stderr or "")[-8000:] if isinstance(exc.stderr, str) else "",
        }


def build_report(args, steps: list[dict]) -> dict:
    failed = [s["name"] for s in steps if not s.get("ok")]
    return {
        "status": "ok" if not failed else "failed",
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "task": args.task,
        "outdir": str(args.outdir),
        "agents": {
            "main": args.main_agent,
            "pool": args.pool_agent,
            "review": args.review_agent,
            "inspect": args.inspect_agent,
            "worker_a": args.worker_agent_a,
            "worker_b": args.worker_agent_b,
        },
        "selected_steps": [s["name"] for s in steps],
        "failed_steps": failed,
        "steps": steps,
    }


def main():
    parser = argparse.ArgumentParser(description="Full acceptance pipeline for Multi-Agent-Collaboration")
    parser.add_argument("--task", default=DEFAULT_TASK)
    parser.add_argument("--main-agent", default="main-ceo")
    parser.add_argument("--pool-agent", default="pool-hr")
    parser.add_argument("--review-agent", default="review-judge")
    parser.add_argument("--inspect-agent", default="inspect-patrol")
    parser.add_argument("--worker-agent-a", default="exec-worker-1")
    parser.add_argument("--worker-agent-b", default="exec-worker-2")
    parser.add_argument("--outdir", default=str(REPO / "examples" / "generated" / "tests" / "full-acceptance"))

    parser.add_argument("--skip-handshake", action="store_true")
    parser.add_argument("--skip-silent-task", action="store_true")
    parser.add_argument("--skip-runtime", action="store_true")
    parser.add_argument("--skip-stage3", action="store_true")
    parser.add_argument("--skip-recovery", action="store_true")

    parser.add_argument("--handshake-timeout", type=int, default=900)
    parser.add_argument("--silent-timeout", type=int, default=1200)
    parser.add_argument("--runtime-timeout", type=int, default=1800)
    parser.add_argument("--stage3-timeout", type=int, default=1800)
    parser.add_argument("--recovery-timeout", type=int, default=600)

    args = parser.parse_args()
    args.outdir = Path(args.outdir)
    args.outdir.mkdir(parents=True, exist_ok=True)

    steps: list[dict] = []

    if not args.skip_handshake:
        cmd = [
            PY,
            str(REPO / "tests" / "test_agent_handshake.py"),
            "--agents",
            args.main_agent,
            args.pool_agent,
            args.review_agent,
            args.inspect_agent,
            "--output",
            str(args.outdir / "handshake-report.json"),
            "--timeout",
            str(min(args.handshake_timeout, 300)),
        ]
        steps.append(run_step("handshake", cmd, timeout=args.handshake_timeout, cwd=REPO))

    if not args.skip_silent_task:
        cmd = [
            PY,
            str(REPO / "tests" / "test_silent_task.py"),
            "--task",
            args.task,
            "--main-agent",
            args.main_agent,
            "--pool-agent",
            args.pool_agent,
            "--review-agent",
            args.review_agent,
            "--inspect-agent",
            args.inspect_agent,
            "--outdir",
            str(args.outdir / "silent-task"),
        ]
        steps.append(run_step("silent-task", cmd, timeout=args.silent_timeout, cwd=REPO))

    if not args.skip_runtime:
        cmd = [
            PY,
            str(REPO / "tests" / "test_runtime_orchestrator_smoke.py"),
            "--task",
            args.task,
            "--main-agent",
            args.main_agent,
            "--pool-agent",
            args.pool_agent,
            "--review-agent",
            args.review_agent,
            "--inspect-agent",
            args.inspect_agent,
            "--worker-agent-a",
            args.worker_agent_a,
            "--worker-agent-b",
            args.worker_agent_b,
            "--outdir",
            str(args.outdir / "runtime-orchestrator"),
        ]
        steps.append(run_step("runtime-orchestrator", cmd, timeout=args.runtime_timeout, cwd=REPO))

    if not args.skip_stage3:
        cmd = [
            PY,
            str(REPO / "tests" / "test_stage3_smoke.py"),
            "--task",
            args.task,
            "--main-agent",
            args.main_agent,
            "--pool-agent",
            args.pool_agent,
            "--review-agent",
            args.review_agent,
            "--inspect-agent",
            args.inspect_agent,
            "--worker-agent-a",
            args.worker_agent_a,
            "--worker-agent-b",
            args.worker_agent_b,
            str(args.outdir / "staged-runtime" / "pipeline-state.json"),
        ]
        steps.append(run_step("stage3-smoke", cmd, timeout=args.stage3_timeout, cwd=REPO))

    if not args.skip_recovery:
        cmd = [
            PY,
            str(REPO / "tests" / "test_recovery_pipeline_smoke.py"),
            "--workspace",
            "/root/.openclaw/workspace",
            "--outdir",
            str(args.outdir / "recovery"),
        ]
        steps.append(run_step("recovery-pipeline", cmd, timeout=args.recovery_timeout, cwd=REPO))

    report = build_report(args, steps)
    report_path = args.outdir / "full-acceptance-report.json"
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    sys.exit(0 if report["status"] == "ok" else 1)


if __name__ == "__main__":
    main()
