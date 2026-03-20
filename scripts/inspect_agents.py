#!/usr/bin/env python3
import argparse
import json
from datetime import datetime, timedelta
from pathlib import Path


def inspect_agent(agent_dir: Path, stale_minutes: int):
    logs_dir = agent_dir / "logs"
    queue_dir = agent_dir / "queue"
    result = {"agent": agent_dir.name, "status": "ok", "issues": []}

    latest_log_mtime = None
    if logs_dir.exists():
        files = list(logs_dir.glob("*.md"))
        if files:
            latest = max(files, key=lambda p: p.stat().st_mtime)
            latest_log_mtime = datetime.fromtimestamp(latest.stat().st_mtime)

    if latest_log_mtime is None or latest_log_mtime < datetime.now() - timedelta(minutes=stale_minutes):
        result["status"] = "stale"
        result["issues"].append("日志长时间未更新")

    if queue_dir.exists():
        for qf in queue_dir.glob("*.json"):
            payload = json.loads(qf.read_text(encoding="utf-8"))
            if payload.get("status") in {"pending", "assigned", "in_progress"}:
                result["issues"].append(f"存在未完成任务: {payload.get('task_id')}")
                if result["status"] == "ok":
                    result["status"] = "watch"
    return result


def main():
    parser = argparse.ArgumentParser(description="Inspect agent directories for stale logs and unfinished queue items")
    parser.add_argument("workspace", help="OpenClaw workspace path")
    parser.add_argument("--stale-minutes", type=int, default=30)
    args = parser.parse_args()

    agents_root = Path(args.workspace) / "mac-system" / "agents"
    reports = []
    if agents_root.exists():
        for child in sorted(agents_root.iterdir()):
            if child.is_dir():
                reports.append(inspect_agent(child, args.stale_minutes))
    print(json.dumps({"generated_at": datetime.now().isoformat(), "reports": reports}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
