#!/usr/bin/env python3
import argparse
import json
from pathlib import Path

from mac_cli import build_packet
from protocol_lib import build_task_assign
from recruit_team import build_group_plan
from runtime_lib import newest_session_for_agent, run_openclaw_agent, write_json
from staffing_decision import build_staffing_decision

REPO = Path(__file__).resolve().parent.parent


def compact_packet(task_packet: dict) -> dict:
    return {
        "task_id": task_packet.get("task_id"),
        "goal": task_packet.get("goal"),
        "task_type": task_packet.get("task_type"),
        "complexity": task_packet.get("complexity"),
        "specialists": task_packet.get("specialists", []),
        "constraints": task_packet.get("constraints", []),
        "output_requirements": task_packet.get("output_requirements", []),
        "execution_mode": task_packet.get("execution_mode"),
    }


def worker_prompt(task_packet: dict, worker_role: str, style: str, staffing: dict) -> str:
    payload = {
        "task": compact_packet(task_packet),
        "worker_role": worker_role,
        "style": style,
        "staffing": staffing,
    }
    return (
        f"你是执行Agent，角色={worker_role}，风格={style}。"
        "只输出 JSON："
        '{"summary":"","findings":[""],"risks":[""],"next":"","deliverables":[""]}'
        + "\n\n"
        + json.dumps(payload, ensure_ascii=False)
    )


def review_prompt(task_packet: dict, worker_a: dict, worker_b: dict | None) -> str:
    payload = {
        "task": compact_packet(task_packet),
        "worker_a": worker_a,
        "worker_b": worker_b,
    }
    return (
        "你是审核Agent。比较两个worker结果。"
        "只输出 JSON："
        '{"pass":true,"winner":"A|B|tie","scores":{"A":0,"B":0},"issues":[""],"merge_advice":[""],"rework_needed":false}'
        + "\n\n"
        + json.dumps(payload, ensure_ascii=False)
    )


def final_prompt(task_packet: dict, worker_a: dict, worker_b: dict | None, review_result: dict) -> str:
    payload = {
        "task": compact_packet(task_packet),
        "worker_a": worker_a,
        "worker_b": worker_b,
        "review": review_result,
    }
    return (
        "你是主Agent，也是唯一用户出口。"
        "只输出 JSON："
        '{"final_summary":"","key_points":[""],"risks":[""],"next_steps":[""],"dedupe_notes":[""]}'
        + "\n\n"
        + json.dumps(payload, ensure_ascii=False)
    )


def latest_for(agent_id: str):
    return newest_session_for_agent(agent_id) if agent_id else None


def persist_partial(path: Path, payload: dict):
    write_json(path, payload)


def main():
    parser = argparse.ArgumentParser(description="Runtime orchestrator using real OpenClaw agents via CLI")
    parser.add_argument("text", help="Raw /mac text")
    parser.add_argument("--main-agent", required=True, help="Main/OpenClaw agent id")
    parser.add_argument("--review-agent", required=True, help="Review agent id")
    parser.add_argument("--inspect-agent", required=True, help="Inspection agent id")
    parser.add_argument("--pool-agent", required=True, help="AgentPool agent id")
    parser.add_argument("--worker-agent-a", default="exec-worker-1")
    parser.add_argument("--worker-agent-b", default="exec-worker-2")
    parser.add_argument("--outdir", default=str(REPO / "examples" / "generated" / "runtime"))
    args = parser.parse_args()

    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    runtime_results_path = outdir / "runtime-results.json"

    task_packet = build_packet(args.text)
    group_plan = build_group_plan(task_packet)
    staffing = build_staffing_decision(group_plan)
    worker_role = (task_packet.get("specialists") or ["Generalist"])[0]

    write_json(outdir / "task-packet.json", task_packet)
    write_json(outdir / "group-plan.json", group_plan)
    write_json(outdir / "staffing-decision.json", staffing)

    runtime_results = {
        "status": "partial",
        "task_packet": task_packet,
        "group_plan": group_plan,
        "staffing": staffing,
        "worker_role": worker_role,
        "coordinator_packets": {},
        "coordinator_results": {},
        "worker_a_result": None,
        "worker_b_result": None,
        "review_result": None,
        "final_result": None,
        "inspection_result": None,
        "session_probe": {},
        "stage": None,
        "resume_recommendation": None,
    }
    persist_partial(runtime_results_path, runtime_results)

    coordinator_packets = {
        "main_agent": build_task_assign(task_packet["task_id"], "system", args.main_agent, task_packet["goal"], status="orchestrating", inputs=[compact_packet(task_packet)]),
        "pool_agent": build_task_assign(task_packet["task_id"], "main-ceo", args.pool_agent, "根据任务包与编组做复用/招聘决策", status="planning", inputs=[compact_packet(task_packet), group_plan, staffing]),
        "review_agent": build_task_assign(task_packet["task_id"], "main-ceo", args.review_agent, "准备后续审核与评分", status="standby", inputs=[compact_packet(task_packet)]),
        "inspect_agent": build_task_assign(task_packet["task_id"], "main-ceo", args.inspect_agent, "启动巡检与恢复预案", status="watching", inputs=[compact_packet(task_packet), staffing]),
    }
    runtime_results["coordinator_packets"] = coordinator_packets
    persist_partial(runtime_results_path, runtime_results)

    for name, agent_id, packet in [
        ("main_agent", args.main_agent, coordinator_packets["main_agent"]),
        ("pool_agent", args.pool_agent, coordinator_packets["pool_agent"]),
        ("review_agent", args.review_agent, coordinator_packets["review_agent"]),
        ("inspect_agent", args.inspect_agent, coordinator_packets["inspect_agent"]),
    ]:
        runtime_results["coordinator_results"][name] = run_openclaw_agent(agent_id, json.dumps(packet, ensure_ascii=False, indent=2), timeout=240)
        if name == "inspect_agent":
            runtime_results["inspection_result"] = runtime_results["coordinator_results"][name]
        persist_partial(runtime_results_path, runtime_results)

    runtime_results["worker_a_result"] = run_openclaw_agent(args.worker_agent_a, worker_prompt(task_packet, worker_role, "stable", staffing), timeout=360)
    persist_partial(runtime_results_path, runtime_results)

    if args.worker_agent_b:
        runtime_results["worker_b_result"] = run_openclaw_agent(args.worker_agent_b, worker_prompt(task_packet, worker_role, "aggressive", staffing), timeout=360)
        persist_partial(runtime_results_path, runtime_results)

    runtime_results["review_result"] = run_openclaw_agent(args.review_agent, review_prompt(task_packet, runtime_results["worker_a_result"], runtime_results["worker_b_result"]), timeout=300)
    persist_partial(runtime_results_path, runtime_results)

    runtime_results["final_result"] = run_openclaw_agent(args.main_agent, final_prompt(task_packet, runtime_results["worker_a_result"], runtime_results["worker_b_result"], runtime_results["review_result"]), timeout=300)

    runtime_results["session_probe"] = {
        "main_agent": latest_for(args.main_agent),
        "pool_agent": latest_for(args.pool_agent),
        "review_agent": latest_for(args.review_agent),
        "inspect_agent": latest_for(args.inspect_agent),
        "worker_agent_a": latest_for(args.worker_agent_a),
        "worker_agent_b": latest_for(args.worker_agent_b),
    }
    if runtime_results["review_result"] and runtime_results["final_result"] and runtime_results["session_probe"]:
        runtime_results["stage"] = "stage3_done"
        runtime_results["resume_recommendation"] = {
            "next_stage": None,
            "reason": "runtime orchestrator 已完成收口",
        }
    elif runtime_results["worker_a_result"]:
        runtime_results["stage"] = "stage2_done"
        runtime_results["resume_recommendation"] = {
            "next_stage": "stage3",
            "reason": "待审核与最终汇总",
        }
    else:
        runtime_results["stage"] = "stage1_done"
        runtime_results["resume_recommendation"] = {
            "next_stage": "stage2",
            "reason": "待执行 worker 阶段",
        }
    runtime_results["status"] = "ok"
    persist_partial(runtime_results_path, runtime_results)

    print(json.dumps({"status": runtime_results["status"], "outdir": str(outdir), "worker_role": worker_role, "stage": runtime_results["stage"]}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
