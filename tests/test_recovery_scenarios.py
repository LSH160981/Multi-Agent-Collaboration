#!/usr/bin/env python3
"""test_recovery_scenarios.py

更贴近真实恢复链路的场景矩阵测试。

覆盖目标：
- Worker / Lead / Reviewer / Pipeline 不同坏法时，系统至少能给出一致的恢复建议
- 不再只测“repair pipeline-state 最小字段”，而是补齐更像真实故障的判定矩阵
- 输出统一 JSON，方便纳入 full acceptance 或人工审计
"""

import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "scripts"))

from inspect_and_recover import inspect_pipeline_state, recommend_session_action
from repair_pipeline_state import ensure_stage_shape


def write_state(path: Path, data: dict):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def scenario_unknown_stage(tmpdir: Path):
    state = {"stage": "mystery_stage", "task_packet": {"task_id": "SCN-001"}}
    path = tmpdir / "pipeline-state.json"
    write_state(path, state)
    result = inspect_pipeline_state(str(tmpdir.parent.parent))
    return {
        "name": "unknown-stage-needs-repair",
        "expected": {
            "stage": "mystery_stage",
            "repair_action_contains": "repair_pipeline_state.py",
        },
        "actual": result,
        "passed": result is not None and result.get("stage") == "mystery_stage" and "repair_pipeline_state.py" in (result.get("repair_action") or ""),
    }


def scenario_stage1_resume(tmpdir: Path):
    state = {
        "stage": "stage1_done",
        "task_packet": {"task_id": "SCN-002", "goal": "resume from stage1", "task_type": "research"},
        "group_plan": {},
    }
    path = tmpdir / "pipeline-state.json"
    write_state(path, state)
    result = inspect_pipeline_state(str(tmpdir.parent.parent))
    return {
        "name": "stage1-should-resume-stage2-workers",
        "expected": {"precise_action_contains": "stage2_workers.py"},
        "actual": result,
        "passed": result is not None and "stage2_workers.py" in (result.get("precise_action") or ""),
    }


def scenario_stage2_incomplete(tmpdir: Path):
    state = {
        "stage": "stage2_done",
        "task_packet": {"task_id": "SCN-003", "goal": "worker result missing", "task_type": "research"},
        "group_plan": {},
        "agent_map": {},
        "dispatch_hints": {},
        "pool_result": {},
        "inspect_result": {},
        "worker_role": "Research",
        "session_probe_before": {},
        "resume_recommendation": {},
        # 故意缺少 worker_agent_a / worker_a_result / session_probe_after_workers
    }
    path = tmpdir / "pipeline-state.json"
    write_state(path, state)
    result = inspect_pipeline_state(str(tmpdir.parent.parent))
    return {
        "name": "stage2-incomplete-should-rerun-workers",
        "expected": {"issue_contains": "stage2 状态不完整", "precise_action_contains": "stage2_workers.py"},
        "actual": result,
        "passed": result is not None and "stage2 状态不完整" in (result.get("issue") or "") and "stage2_workers.py" in (result.get("precise_action") or ""),
    }


def scenario_stage3_incomplete(tmpdir: Path):
    state = {
        "stage": "stage3_done",
        "task_packet": {"task_id": "SCN-004", "goal": "review missing", "task_type": "research"},
        "group_plan": {},
        "agent_map": {},
        "dispatch_hints": {},
        "pool_result": {},
        "inspect_result": {},
        "worker_role": "Research",
        "session_probe_before": {},
        "resume_recommendation": {},
        "worker_agent_a": "exec-worker-1",
        "worker_a_result": {},
        "session_probe_after_workers": {},
        # 故意缺少 review_result / final_result / session_probe
    }
    path = tmpdir / "pipeline-state.json"
    write_state(path, state)
    result = inspect_pipeline_state(str(tmpdir.parent.parent))
    return {
        "name": "stage3-incomplete-should-rerun-review-final",
        "expected": {"issue_contains": "stage3 状态不完整", "precise_action_contains": "stage3_review_final.py"},
        "actual": result,
        "passed": result is not None and "stage3 状态不完整" in (result.get("issue") or "") and "stage3_review_final.py" in (result.get("precise_action") or ""),
    }


def scenario_repair_shape_matrix():
    cases = []
    base = {"task_packet": {"task_id": "SCN-005", "goal": "repair shape", "task_type": "mixed"}}
    for stage, required in [
        ("stage1_done", ["task_packet", "group_plan", "agent_map", "dispatch_hints", "session_probe_before", "resume_recommendation"]),
        ("stage2_done", ["worker_agent_a", "worker_a_result", "session_probe_after_workers"]),
        ("stage3_done", ["review_result", "final_result", "session_probe"]),
    ]:
        data = dict(base)
        data["stage"] = stage
        ensure_stage_shape(data, stage)
        missing = [k for k in required if k not in data]
        cases.append({
            "stage": stage,
            "required": required,
            "missing": missing,
            "passed": not missing,
        })
    return {
        "name": "repair-shape-matrix",
        "actual": cases,
        "passed": all(c["passed"] for c in cases),
    }


def scenario_session_age_matrix():
    cases = [
        {"name": "lead-missing-session", "session": None, "expected": "rebuild"},
        {"name": "worker-fresh-session", "session": {"ageMs": 5 * 60 * 1000}, "expected": "resume"},
        {"name": "worker-warm-session", "session": {"ageMs": 90 * 60 * 1000}, "expected": "redispatch"},
        {"name": "reviewer-stale-session", "session": {"ageMs": 8 * 60 * 60 * 1000}, "expected": "rebuild"},
        {"name": "inspect-unknown-age", "session": {}, "expected": "probe"},
    ]
    results = []
    for case in cases:
        actual = recommend_session_action(case["session"], stale_minutes=30)
        results.append({
            "name": case["name"],
            "expected": case["expected"],
            "actual": actual,
            "passed": actual == case["expected"],
        })
    return {
        "name": "session-age-recommendation-matrix",
        "actual": results,
        "passed": all(r["passed"] for r in results),
    }


def main():
    outdir = REPO / "examples" / "generated" / "tests" / "recovery-scenarios"
    runtime_dir = REPO / "examples" / "generated" / "staged-runtime"
    runtime_dir.mkdir(parents=True, exist_ok=True)
    outdir.mkdir(parents=True, exist_ok=True)

    # inspect_pipeline_state 会优先读默认 staged-runtime 路径，因此每个场景都覆盖这个文件。
    state_path = runtime_dir / "pipeline-state.json"

    scenarios = []
    scenarios.append(scenario_unknown_stage(runtime_dir))
    scenarios.append(scenario_stage1_resume(runtime_dir))
    scenarios.append(scenario_stage2_incomplete(runtime_dir))
    scenarios.append(scenario_stage3_incomplete(runtime_dir))
    scenarios.append(scenario_repair_shape_matrix())
    scenarios.append(scenario_session_age_matrix())

    report = {
        "status": "ok" if all(item.get("passed") for item in scenarios) else "failed",
        "scenario_count": len(scenarios),
        "scenarios": scenarios,
    }
    (outdir / "recovery-scenarios-report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    raise SystemExit(0 if report["status"] == "ok" else 1)


if __name__ == "__main__":
    main()
