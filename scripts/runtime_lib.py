#!/usr/bin/env python3
import json
import subprocess
from pathlib import Path
from typing import Any


def _run(cmd: list[str]) -> str:
    return subprocess.check_output(cmd, text=True, stderr=subprocess.STDOUT)


def run_openclaw_agent(agent_id: str, message: str, timeout: int = 600):
    cmd = [
        "openclaw", "agent",
        "--agent", agent_id,
        "--message", message,
        "--json",
        "--timeout", str(timeout),
    ]
    out = _run(cmd)
    try:
        return json.loads(out)
    except json.JSONDecodeError:
        return {"raw": out, "cmd": cmd}


def list_sessions_json(all_agents: bool = True):
    cmd = ["openclaw", "sessions", "--json"]
    if all_agents:
        cmd.append("--all-agents")
    out = _run(cmd)
    try:
        return json.loads(out)
    except json.JSONDecodeError:
        return {"raw": out, "cmd": cmd}


def sessions_for_agent(agent_id: str, all_agents: bool = True) -> list[dict[str, Any]]:
    payload = list_sessions_json(all_agents=all_agents)
    sessions = payload.get("sessions", []) if isinstance(payload, dict) else payload
    return [s for s in sessions if s.get("agentId") == agent_id]


def newest_session_for_agent(agent_id: str, all_agents: bool = True):
    sessions = sessions_for_agent(agent_id, all_agents=all_agents)
    if not sessions:
        return None
    return sorted(sessions, key=lambda x: x.get("updatedAt", 0), reverse=True)[0]


def session_age_minutes(session: dict[str, Any]) -> float | None:
    age_ms = session.get("ageMs")
    if age_ms is None:
        return None
    return round(age_ms / 60000.0, 2)


def build_recovery_message(agent_dir: str, issues: list[str], session_info: dict[str, Any] | None) -> str:
    lines = [
        "你被检查Agent判定为需要恢复，请立即自检并汇报。",
        f"目录角色：{agent_dir}",
        f"发现问题：{'；'.join(issues) if issues else '未知'}",
    ]
    if session_info:
        lines.append(f"最近session：{session_info.get('key', '-')}")
        lines.append(f"最近活动距今（分钟）：{session_age_minutes(session_info)}")
    lines.append("请按以下格式回复：1. 当前状态 2. 卡点 3. 下一步 4. 是否需要重派/重建。")
    return "\n".join(lines)


def write_json(path: Path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
