#!/usr/bin/env python3
import json
import subprocess
from pathlib import Path


def run_openclaw_agent(agent_id: str, message: str, timeout: int = 600):
    cmd = [
        "openclaw", "agent",
        "--agent", agent_id,
        "--message", message,
        "--json",
        "--timeout", str(timeout),
    ]
    out = subprocess.check_output(cmd, text=True)
    try:
        return json.loads(out)
    except json.JSONDecodeError:
        return {"raw": out}


def list_sessions_json():
    cmd = ["openclaw", "sessions", "--json", "--all-agents"]
    out = subprocess.check_output(cmd, text=True)
    try:
        return json.loads(out)
    except json.JSONDecodeError:
        return {"raw": out}


def write_json(path: Path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
