#!/usr/bin/env python3
import argparse
import json
from pathlib import Path
from runtime_lib import newest_session_for_agent, run_openclaw_agent, write_json


def review_prompt(task_packet: dict, worker_a: dict, worker_b: dict | None) -> str:
    return (
        "你是审核Agent。请比较两个worker结果并输出 JSON："
        '{"pass":true,"winner":"A|B|tie","scores":{"A":0,"B":0},"issues":[""],"merge_advice":[""]}'
        + "\n\n"
        + json.dumps({"task": task_packet, "worker_a": worker_a, "worker_b": worker_b}, ensure_ascii=False)
    )


def final_prompt(task_packet: dict, worker_a: dict, worker_b: dict | None, review_result: dict) -> str:
    return (
        "你是主Agent，唯一用户出口。请输出 JSON："
        '{"final_summary":"","key_points":[""],"risks":[""],"next_steps":[""]}'
        + "\n\n"
        + json.dumps({"task": task_packet, "worker_a": worker_a, "worker_b": worker_b, "review": review_result}, ensure_ascii=False)
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

    review_result = run_openclaw_agent(
        args.review_agent,
        review_prompt(state["task_packet"], state.get("worker_a_result"), state.get("worker_b_result")),
        timeout=360,
    )
    final_result = run_openclaw_agent(
        args.main_agent,
        final_prompt(state["task_packet"], state.get("worker_a_result"), state.get("worker_b_result"), review_result),
        timeout=360,
    )

    state["review_result"] = review_result
    state["final_result"] = final_result
    state["session_probe"] = {
        "main_agent": newest_session_for_agent(args.main_agent),
        "review_agent": newest_session_for_agent(args.review_agent),
        "inspect_agent": newest_session_for_agent(args.inspect_agent),
        "worker_agent_a": newest_session_for_agent(state.get("worker_agent_a")) if state.get("worker_agent_a") else None,
        "worker_agent_b": newest_session_for_agent(state.get("worker_agent_b")) if state.get("worker_agent_b") else None,
    }
    state["stage"] = "stage3_done"

    write_json(state_path, state)
    print(json.dumps({"status": "ok", "stage": state["stage"]}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
