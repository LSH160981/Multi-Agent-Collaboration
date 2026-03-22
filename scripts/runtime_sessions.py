#!/usr/bin/env python3
import argparse
import json
import subprocess
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent


def run(cmd: list[str]) -> str:
    return subprocess.check_output(cmd, text=True, stderr=subprocess.STDOUT)


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def spawn(role: str, task: str, agent_id: str, timeout: int = 1200):
    cmd = [
        "openclaw", "agent",
        "--agent", agent_id,
        "--message", task,
        "--json",
        "--timeout", str(timeout),
    ]
    try:
        out = run(cmd)
        return {"role": role, "agent_id": agent_id, "ok": True, "raw": out}
    except subprocess.CalledProcessError as e:
        return {
            "role": role,
            "agent_id": agent_id,
            "ok": False,
            "exit_code": e.returncode,
            "raw": e.output,
            "cmd": cmd,
        }


ROLE_PROMPTS = {
    "main": "你是主Agent CEO。你是唯一允许联系用户的 agent。你的任务是理解需求、拆解任务、统筹团队、合并去重、最终拍板。禁止把内部噪音直接发给用户。",
    "pool": "你是 AgentPool / HR。你的任务是根据任务能力缺口招聘或复用角色，优先控制人数，缺什么补什么，并默认生成 A/B 双组竞争方案。",
    "review": "你是审核Agent。你的任务是从 Reviewer（格式）、Judge（质量）、Metrics（评分）三个维度审查提交物，驳回不达标结果，并输出结构化评分卡。",
    "inspect": "你是检查Agent。你的任务是持续巡检是否有 agent 卡住、无产出、队列未推进，并给出 retry、唤醒、重派、重建建议。",
}


def main():
    parser = argparse.ArgumentParser(description="Run a native-session Multi-Agent-Collaboration demo")
    parser.add_argument("text", help="Raw task text, usually /mac ...")
    parser.add_argument("--main-agent", default="main-ceo", help="主Agent 对应的 OpenClaw agent id")
    parser.add_argument("--pool-agent", default="pool-hr", help="AgentPool 对应的 OpenClaw agent id")
    parser.add_argument("--review-agent", default="review-judge", help="审核Agent 对应的 OpenClaw agent id")
    parser.add_argument("--inspect-agent", default="inspect-patrol", help="检查Agent 对应的 OpenClaw agent id")
    parser.add_argument("--outdir", default=str(REPO / "examples" / "generated" / "native-sessions"))
    args = parser.parse_args()

    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    packet_path = outdir / "task-packet.json"
    group_path = outdir / "group-plan.json"

    subprocess.check_call([str(REPO / "scripts" / "mac_cli.py"), args.text, "--output", str(packet_path)])
    subprocess.check_call([str(REPO / "scripts" / "recruit_team.py"), str(packet_path), "--output", str(group_path)])

    packet = read_json(packet_path)
    group = read_json(group_path)

    agent_map = {
        "main": args.main_agent,
        "pool": args.pool_agent,
        "review": args.review_agent,
        "inspect": args.inspect_agent,
    }

    role_messages = {
        "main": ROLE_PROMPTS["main"] + "\n\n请阅读以下任务包，并输出：1.任务理解 2.是否缺失信息 3.执行拆解 4.用户侧最终应保持单一出口。\n\n" + json.dumps(packet, ensure_ascii=False, indent=2),
        "pool": ROLE_PROMPTS["pool"] + "\n\n请阅读以下任务包与编组方案，并输出：1.复用/招聘策略 2.A/B 组人员建议 3.每个角色边界。\n\n" + json.dumps({"task_packet": packet, "group_plan": group}, ensure_ascii=False, indent=2),
        "review": ROLE_PROMPTS["review"] + "\n\n请基于以下任务包，先给出审核标准模板，说明后续如何审查 A/B 两组结果。\n\n" + json.dumps(packet, ensure_ascii=False, indent=2),
        "inspect": ROLE_PROMPTS["inspect"] + "\n\n请基于以下任务包与编组方案，给出巡检计划、stale 判断条件、恢复动作优先级。\n\n" + json.dumps({"task_packet": packet, "group_plan": group}, ensure_ascii=False, indent=2),
    }

    results = {
        "task_packet": packet,
        "group_plan": group,
        "agent_map": agent_map,
        "roles": {},
    }

    for role, msg in role_messages.items():
        results["roles"][role] = spawn(role, msg, agent_id=agent_map[role])

    write_json(outdir / "native-session-results.json", results)

    summary = {
        "status": "ok",
        "outdir": str(outdir),
        "role_status": {role: data.get("ok", False) for role, data in results["roles"].items()},
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
