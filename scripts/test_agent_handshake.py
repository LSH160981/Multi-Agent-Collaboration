#!/usr/bin/env python3
import argparse
import json
from datetime import datetime
from pathlib import Path

from runtime_lib import run_openclaw_agent, write_json


DEFAULT_CAPABILITIES = {
    "main-ceo": "主Agent，负责理解任务、拆解任务、统筹团队、去重并向用户输出唯一结论",
    "pool-hr": "AgentPool，负责识别能力缺口、复用或招聘角色、设计A/B双组编制",
    "review-judge": "审核Agent，负责从格式、质量、评分三个维度审核成果",
    "inspect-patrol": "检查Agent，负责巡检、识别stale、唤醒、恢复与重派建议",
}


def handshake_message(sender: str, target: str) -> str:
    return (
        f"你正在参加 Multi-Agent-Collaboration 的握手测试。\\n"
        f"发送方自报身份：我是{sender}，你是谁？\\n"
        f"请严格只用一句中文回复，格式：我是{target}，我的能力是XXX。"
    )


def main():
    parser = argparse.ArgumentParser(description="Pairwise handshake test for OpenClaw agents")
    parser.add_argument("--agents", nargs="+", default=["main-ceo", "pool-hr", "review-judge", "inspect-patrol"])
    parser.add_argument("--output", default="examples/generated/tests/handshake-report.json")
    parser.add_argument("--timeout", type=int, default=180)
    args = parser.parse_args()

    reports = []
    for sender in args.agents:
        for target in args.agents:
            if sender == target:
                continue
            result = run_openclaw_agent(target, handshake_message(sender, target), timeout=args.timeout)
            reports.append({
                "time": datetime.now().isoformat(),
                "sender": sender,
                "target": target,
                "expected_capability": DEFAULT_CAPABILITIES.get(target, ""),
                "result": result,
            })

    summary = {
        "generated_at": datetime.now().isoformat(),
        "agents": args.agents,
        "pair_count": len(reports),
        "reports": reports,
    }
    write_json(Path(args.output), summary)
    print(json.dumps({"status": "ok", "output": args.output, "pair_count": len(reports)}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
