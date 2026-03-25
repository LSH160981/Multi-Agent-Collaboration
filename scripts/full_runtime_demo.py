#!/usr/bin/env python3
import argparse
import json
import subprocess
from pathlib import Path
from runtime_lib import newest_session_for_agent, run_openclaw_agent, write_json

REPO = Path(__file__).resolve().parent.parent


def compact_packet(task_packet: dict) -> dict:
    return {
        "task_id": task_packet.get("task_id"),
        "goal": task_packet.get("goal"),
        "task_type": task_packet.get("task_type"),
        "specialists": task_packet.get("specialists", []),
        "constraints": task_packet.get("constraints", []),
        "output_requirements": task_packet.get("output_requirements", []),
    }


def worker_prompt(task_packet: dict, worker_role: str, style: str) -> str:
    slim = compact_packet(task_packet)
    return (
        f"你是执行Agent，角色={worker_role}，风格={style}。"
        "请用极简结构输出 JSON："
        '{"summary":"","findings":[""],"risks":[""],"next":""}'
        "。只给结论，不写长解释。\n\n"
        + json.dumps(slim, ensure_ascii=False)
    )


def review_prompt(task_packet: dict, worker_a: dict, worker_b: dict | None) -> str:
    payload = {
        "task": compact_packet(task_packet),
        "worker_a": worker_a,
        "worker_b": worker_b,
    }
    return (
        "你是审核Agent。比较两个worker结果。"
        "请输出 JSON："
        '{"pass":true,"winner":"A|B|tie","scores":{"A":0,"B":0},"issues":[""],"merge_advice":[""]}'
        "。\n\n"
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
        "请输出 JSON："
        '{"final_summary":"","key_points":[""],"risks":[""],"next_steps":[""]}'
        "。去重，只保留最新有效结论。\n\n"
        + json.dumps(payload, ensure_ascii=False)
    )


def main():
    parser = argparse.ArgumentParser(description="Compact full runtime demo with dual-worker comparison")
    parser.add_argument("text", help="Raw /mac text")
    parser.add_argument("--main-agent", default="main-ceo")
    parser.add_argument("--pool-agent", default="pool-hr")
    parser.add_argument("--worker-agent-a", default="exec-worker-1")
    parser.add_argument("--worker-agent-b", default="")
    parser.add_argument("--review-agent", default="review-judge")
    parser.add_argument("--inspect-agent", default="inspect-patrol")
    parser.add_argument("--outdir", default=str(REPO / "examples" / "generated" / "full-runtime-demo"))
    args = parser.parse_args()

    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    task_packet_path = outdir / "task-packet.json"
    group_plan_path = outdir / "group-plan.json"

    subprocess.check_call([str(REPO / "scripts" / "mac_cli.py"), args.text, "--output", str(task_packet_path)])
    subprocess.check_call([str(REPO / "scripts" / "recruit_team.py"), str(task_packet_path), "--output", str(group_plan_path)])

    task_packet = json.loads(task_packet_path.read_text(encoding="utf-8"))
    group_plan = json.loads(group_plan_path.read_text(encoding="utf-8"))
    worker_role = (task_packet.get("specialists") or ["Generalist"])[0]

    pool_result = run_openclaw_agent(
        args.pool_agent,
        "你是AgentPool。请用 JSON 简短说明本轮如何分工："
        '{"role":"","why":"","plan":[""]}'
        + "\n\n"
        + json.dumps({"task": compact_packet(task_packet), "group_plan": group_plan}, ensure_ascii=False),
        timeout=300,
    )
    inspect_result = run_openclaw_agent(
        args.inspect_agent,
        "你是检查Agent。请用 JSON 输出巡检策略："
        '{"watch":[""],"stale_rule":"","recover":[""]}',
        timeout=300,
    )
    worker_a_result = run_openclaw_agent(args.worker_agent_a, worker_prompt(task_packet, worker_role, "stable"), timeout=450)
    worker_b_result = None
    if args.worker_agent_b:
        worker_b_result = run_openclaw_agent(args.worker_agent_b, worker_prompt(task_packet, worker_role, "aggressive"), timeout=450)
    review_result = run_openclaw_agent(args.review_agent, review_prompt(task_packet, worker_a_result, worker_b_result), timeout=450)
    final_result = run_openclaw_agent(args.main_agent, final_prompt(task_packet, worker_a_result, worker_b_result, review_result), timeout=450)

    session_probe = {
        "main_agent": newest_session_for_agent(args.main_agent),
        "pool_agent": newest_session_for_agent(args.pool_agent),
        "worker_agent_a": newest_session_for_agent(args.worker_agent_a),
        "worker_agent_b": newest_session_for_agent(args.worker_agent_b) if args.worker_agent_b else None,
        "review_agent": newest_session_for_agent(args.review_agent),
        "inspect_agent": newest_session_for_agent(args.inspect_agent),
    }

    result = {
        "task_packet": compact_packet(task_packet),
        "group_plan": group_plan,
        "worker_role": worker_role,
        "pool_result": pool_result,
        "inspect_result": inspect_result,
        "worker_a_result": worker_a_result,
        "worker_b_result": worker_b_result,
        "review_result": review_result,
        "final_result": final_result,
        "session_probe": session_probe,
    }
    write_json(outdir / "full-runtime-demo.json", result)
    print(json.dumps({"status": "ok", "outdir": str(outdir), "worker_role": worker_role, "dual_worker": bool(args.worker_agent_b)}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
