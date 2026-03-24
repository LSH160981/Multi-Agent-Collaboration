#!/usr/bin/env python3
import argparse
import json
import subprocess
from pathlib import Path
from runtime_lib import newest_session_for_agent, run_openclaw_agent, write_json

REPO = Path(__file__).resolve().parent.parent


def worker_prompt(task_packet: dict, worker_role: str) -> str:
    return (
        f"你是执行Agent，当前承担角色：{worker_role}。\\n"
        "请根据下面任务包完成你的执行视角输出，严格返回：1.你的理解 2.执行计划 3.初步产出 4.风险。\\n\\n"
        + json.dumps(task_packet, ensure_ascii=False, indent=2)
    )


def review_prompt(task_packet: dict, worker_result: dict) -> str:
    return (
        "你是审核Agent。请基于任务包与执行Agent的结果，从 Reviewer（格式）、Judge（质量）、Metrics（评分）三个维度给出审核。\\n"
        "严格输出：1.是否通过 2.三维评分 3.问题 4.修改建议。\\n\\n"
        + json.dumps({"task_packet": task_packet, "worker_result": worker_result}, ensure_ascii=False, indent=2)
    )


def final_prompt(task_packet: dict, worker_result: dict, review_result: dict) -> str:
    return (
        "你是主Agent，且你是唯一允许对用户输出的人。\\n"
        "请基于任务包、执行Agent结果、审核Agent结果，生成去重后的最终结论。\\n"
        "严格输出：1.最终摘要 2.关键发现 3.风险与下一步。\\n\\n"
        + json.dumps(
            {
                "task_packet": task_packet,
                "worker_result": worker_result,
                "review_result": review_result,
            },
            ensure_ascii=False,
            indent=2,
        )
    )


def main():
    parser = argparse.ArgumentParser(description="Fuller runtime demo with main/pool/worker/review/inspect chain")
    parser.add_argument("text", help="Raw /mac text")
    parser.add_argument("--main-agent", default="main-ceo")
    parser.add_argument("--pool-agent", default="pool-hr")
    parser.add_argument("--worker-agent", default="exec-worker-1")
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

    pool_result = run_openclaw_agent(args.pool_agent, f"你是AgentPool，请基于任务包和编组方案说明为什么此时应启用 {args.worker_agent} 承担 {worker_role} 角色。\\n\\n" + json.dumps({"task_packet": task_packet, "group_plan": group_plan}, ensure_ascii=False, indent=2))
    inspect_result = run_openclaw_agent(args.inspect_agent, "你是检查Agent，请给出本轮执行前巡检清单，并说明将如何识别 stale / watch / retry。")
    worker_result = run_openclaw_agent(args.worker_agent, worker_prompt(task_packet, worker_role), timeout=900)
    review_result = run_openclaw_agent(args.review_agent, review_prompt(task_packet, worker_result), timeout=900)
    final_result = run_openclaw_agent(args.main_agent, final_prompt(task_packet, worker_result, review_result), timeout=900)

    session_probe = {
        "main_agent": newest_session_for_agent(args.main_agent),
        "pool_agent": newest_session_for_agent(args.pool_agent),
        "worker_agent": newest_session_for_agent(args.worker_agent),
        "review_agent": newest_session_for_agent(args.review_agent),
        "inspect_agent": newest_session_for_agent(args.inspect_agent),
    }

    result = {
        "task_packet": task_packet,
        "group_plan": group_plan,
        "worker_role": worker_role,
        "pool_result": pool_result,
        "inspect_result": inspect_result,
        "worker_result": worker_result,
        "review_result": review_result,
        "final_result": final_result,
        "session_probe": session_probe,
    }
    write_json(outdir / "full-runtime-demo.json", result)
    print(json.dumps({"status": "ok", "outdir": str(outdir), "worker_role": worker_role}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
