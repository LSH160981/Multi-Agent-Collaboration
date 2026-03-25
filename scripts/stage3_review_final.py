#!/usr/bin/env python3
import argparse
import json
from pathlib import Path
from runtime_lib import build_session_reuse_hint, newest_session_for_agent, probe_agents, run_openclaw_agent, write_json


def slim(value):
    if isinstance(value, dict):
        return value
    return {"raw": str(value)[:800]}


def review_prompt(task_packet: dict, worker_a: dict, worker_b: dict | None) -> str:
    payload = {
        "task": task_packet,
        "worker_a": slim(worker_a),
        "worker_b": slim(worker_b) if worker_b is not None else None,
    }
    return (
        "你是审核Agent。只输出 JSON："
        '{"pass":true,"winner":"A|B|tie","scores":{"A":0,"B":0},"issues":[""],"merge_advice":[""],"rework_needed":false}'
        + "\n\n"
        + json.dumps(payload, ensure_ascii=False)
    )


def final_prompt(task_packet: dict, review_result: dict, worker_a: dict, worker_b: dict | None) -> str:
    payload = {
        "task": task_packet,
        "review": slim(review_result),
        "worker_a": slim(worker_a),
        "worker_b": slim(worker_b) if worker_b is not None else None,
    }
    return (
        "你是主Agent，唯一用户出口。只输出 JSON："
        '{"final_summary":"","key_points":[""],"risks":[""],"next_steps":[""],"dedupe_notes":[""]}'
        + "\n\n"
        + json.dumps(payload, ensure_ascii=False)
    )


def main():
    parser = argparse.ArgumentParser(description="Stage 3: review + final summary")
    parser.add_argument("state_json", help="pipeline-state.json from previous stages")
    parser.add_argument("--main-agent", default="main-ceo")
    parser.add_argument("--review-agent", default="review-judge")
    parser.add_argument("--inspect-agent", default="inspect-patrol")
    args = parser.parse_args()

    state_path = Path(args.state_json)
    state = json.loads(state_path.read_text(encoding="utf-8"))

    review_before = newest_session_for_agent(args.review_agent)
    review_result = run_openclaw_agent(
        args.review_agent,
        review_prompt(state["task_packet"], state.get("worker_a_result"), state.get("worker_b_result")),
        timeout=240,
    )
    final_before = newest_session_for_agent(args.main_agent)
    final_result = run_openclaw_agent(
        args.main_agent,
        final_prompt(state["task_packet"], review_result, state.get("worker_a_result"), state.get("worker_b_result")),
        timeout=240,
    )

    state["review_result"] = {
        "dispatch_hint": build_session_reuse_hint(args.review_agent),
        "session_before": review_before,
        "session_after": newest_session_for_agent(args.review_agent),
        "result": review_result,
    }
    state["final_result"] = {
        "dispatch_hint": build_session_reuse_hint(args.main_agent),
        "session_before": final_before,
        "session_after": newest_session_for_agent(args.main_agent),
        "result": final_result,
    }
    state["session_probe"] = probe_agents([
        args.main_agent,
        args.review_agent,
        args.inspect_agent,
        state.get("worker_agent_a"),
        state.get("worker_agent_b"),
    ])
    state["resume_recommendation"] = {
        "next_stage": None,
        "reason": "stage3 已完成，当前 pipeline 已收口",
    }
    state["stage"] = "stage3_done"

    write_json(state_path, state)
    print(json.dumps({"status": "ok", "stage": state["stage"]}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
