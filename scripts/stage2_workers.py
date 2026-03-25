#!/usr/bin/env python3
import argparse
import json
from pathlib import Path
from runtime_lib import build_session_reuse_hint, newest_session_for_agent, run_openclaw_agent, session_age_minutes, write_json


def worker_prompt(task_packet: dict, worker_role: str, style: str) -> str:
    return (
        f"你是执行Agent，角色={worker_role}，风格={style}。"
        "请输出 JSON："
        '{"summary":"","findings":[""],"risks":[""],"next":"","deliverables":[""]}'
        "。只保留结论。\n\n"
        + json.dumps(task_packet, ensure_ascii=False)
    )


def run_worker(agent_id: str, task_packet: dict, worker_role: str, style: str):
    before = newest_session_for_agent(agent_id)
    result = run_openclaw_agent(agent_id, worker_prompt(task_packet, worker_role, style), timeout=360)
    after = newest_session_for_agent(agent_id)
    return {
        "agent_id": agent_id,
        "style": style,
        "dispatch_hint": build_session_reuse_hint(agent_id),
        "session_before": before,
        "session_after": after,
        "session_age_after_minutes": session_age_minutes(after),
        "result": result,
    }


def main():
    parser = argparse.ArgumentParser(description="Stage 2: run one or two workers")
    parser.add_argument("state_json", help="pipeline-state.json from stage1")
    parser.add_argument("--worker-agent-a", default="exec-worker-1")
    parser.add_argument("--worker-agent-b", default="")
    args = parser.parse_args()

    state_path = Path(args.state_json)
    state = json.loads(state_path.read_text(encoding="utf-8"))

    task_packet = state["task_packet"]
    worker_role = state["worker_role"]

    worker_a_result = run_worker(args.worker_agent_a, task_packet, worker_role, "stable")
    worker_b_result = None
    if args.worker_agent_b:
        worker_b_result = run_worker(args.worker_agent_b, task_packet, worker_role, "aggressive")

    state["worker_agent_a"] = args.worker_agent_a
    state["worker_agent_b"] = args.worker_agent_b or None
    state["worker_a_result"] = worker_a_result
    state["worker_b_result"] = worker_b_result
    state["session_probe_after_workers"] = {
        "worker_agent_a": worker_a_result.get("session_after"),
        "worker_agent_b": worker_b_result.get("session_after") if worker_b_result else None,
    }
    state["resume_recommendation"] = {
        "next_stage": "stage3_review_final",
        "reason": "worker 已执行完成，可进入审核与最终汇总",
    }
    state["stage"] = "stage2_done"

    write_json(state_path, state)
    print(json.dumps({"status": "ok", "stage": state["stage"], "dual_worker": bool(args.worker_agent_b)}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
