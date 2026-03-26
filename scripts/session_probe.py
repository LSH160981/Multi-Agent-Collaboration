#!/usr/bin/env python3
import argparse
import json
import subprocess
from pathlib import Path


def run(cmd: list[str]) -> str:
    return subprocess.check_output(cmd, text=True, stderr=subprocess.STDOUT)


def list_sessions(all_agents: bool = True):
    cmd = ["openclaw", "sessions", "--json"]
    if all_agents:
        cmd.append("--all-agents")
    out = run(cmd)
    try:
        return json.loads(out)
    except json.JSONDecodeError:
        return {"raw": out}


def normalize_sessions(payload):
    if isinstance(payload, list):
        return payload
    if isinstance(payload, dict):
        return payload.get("sessions", [])
    return []


def recommend_action(session: dict, stale_minutes: int):
    age_ms = session.get("ageMs")
    if age_ms is None:
        return "probe"
    age_minutes = age_ms / 60000.0
    if age_minutes <= stale_minutes:
        return "resume"
    if age_minutes <= stale_minutes * 4:
        return "redispatch"
    return "rebuild"


def enrich_sessions(sessions, stale_minutes: int):
    enriched = []
    for s in sessions:
        age_ms = s.get("ageMs")
        age_minutes = round(age_ms / 60000.0, 2) if age_ms is not None else None
        item = dict(s)
        item["age_minutes"] = age_minutes
        item["recommended_action"] = recommend_action(s, stale_minutes)
        enriched.append(item)
    return enriched


def main():
    parser = argparse.ArgumentParser(description="Probe OpenClaw stored sessions for Multi-Agent-Collaboration diagnostics")
    parser.add_argument("--output", help="Optional output JSON path")
    parser.add_argument("--all-agents", action="store_true", default=True)
    parser.add_argument("--stale-minutes", type=int, default=30)
    args = parser.parse_args()

    data = list_sessions(all_agents=args.all_agents)
    sessions = normalize_sessions(data)
    enriched = enrich_sessions(sessions, args.stale_minutes)
    summary = {
        "session_count": len(enriched),
        "stale_minutes": args.stale_minutes,
        "action_legend": {
            "probe": "缺少足够时效信息，先观察",
            "resume": "最近 session 仍新鲜，优先续跑",
            "redispatch": "session 偏旧，优先重派当前任务",
            "rebuild": "session 长期 stale，优先重建链路",
        },
        "sessions": enriched,
    }

    rendered = json.dumps(summary, ensure_ascii=False, indent=2)
    if args.output:
        out = Path(args.output)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(rendered + "\n", encoding="utf-8")
    print(rendered)


if __name__ == "__main__":
    main()
