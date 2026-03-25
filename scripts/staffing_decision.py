#!/usr/bin/env python3
"""staffing_decision.py

编组后的复用 / 启用决策器。

职责：
- 根据 group_plan 中的角色需求选择候选 agent。
- 优先复用已有 session；没有合适 session 时，给出新回合启用建议。
- 输出结构化 staffing decision，供 runtime orchestration 使用。
"""

import argparse
import json
from pathlib import Path

from runtime_lib import newest_session_for_agent, session_age_minutes

DEFAULT_AGENT_POOL = {
    "Lead": ["main-ceo", "pool-hr"],
    "Research": ["exec-worker-1", "exec-worker-2"],
    "Verification": ["review-judge", "exec-worker-1"],
    "Summary": ["main-ceo", "review-judge"],
    "Implementation": ["exec-worker-1", "exec-worker-2"],
    "Recovery": ["inspect-patrol"],
    "LogAnalysis": ["inspect-patrol"],
    "Test": ["review-judge", "exec-worker-2"],
    "Frontend": ["exec-worker-1", "exec-worker-2"],
}


def choose_candidate(role: str):
    return DEFAULT_AGENT_POOL.get(role, [])


def decide_member(member: dict) -> dict:
    role = member["role"]
    candidates = choose_candidate(role)
    if not candidates:
        return {
            "name": member["name"],
            "role": role,
            "decision": "hire",
            "agent_id": None,
            "reason": "没有可复用候选",
        }

    ranked = []
    for agent_id in candidates:
        session = newest_session_for_agent(agent_id)
        ranked.append({
            "agent_id": agent_id,
            "session": session,
            "age_minutes": session_age_minutes(session),
        })

    reusable = [r for r in ranked if r["session"]]
    if reusable:
        reusable.sort(key=lambda x: x.get("age_minutes") or 10**9)
        winner = reusable[0]
        return {
            "name": member["name"],
            "role": role,
            "decision": "reuse",
            "agent_id": winner["agent_id"],
            "session_key": winner["session"]["key"],
            "reason": "存在可复用 session",
        }

    return {
        "name": member["name"],
        "role": role,
        "decision": "hire",
        "agent_id": candidates[0],
        "reason": "有候选 agent，但无近期 session，按新回合启用",
    }


def build_staffing_decision(group_plan: dict) -> dict:
    result = {
        "task_id": group_plan.get("task_id"),
        "decisions": [],
        "summary": {"reuse": 0, "hire": 0},
    }
    for group in group_plan.get("groups", []):
        decided = []
        for member in group.get("members", []):
            item = decide_member(member)
            result["summary"][item["decision"]] += 1
            decided.append(item)
        result["decisions"].append({"group": group.get("group"), "members": decided})
    return result


def main():
    parser = argparse.ArgumentParser(description="Decide reuse vs hire for group members")
    parser.add_argument("group_plan_json")
    parser.add_argument("--output")
    args = parser.parse_args()

    group_plan = json.loads(Path(args.group_plan_json).read_text(encoding="utf-8"))
    result = build_staffing_decision(group_plan)
    rendered = json.dumps(result, ensure_ascii=False, indent=2)
    if args.output:
        Path(args.output).write_text(rendered + "\n", encoding="utf-8")
    print(rendered)


if __name__ == "__main__":
    main()
