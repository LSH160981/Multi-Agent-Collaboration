#!/usr/bin/env python3
import json
import subprocess
from pathlib import Path
from typing import Any


def _run(cmd: list[str]) -> str:
    return subprocess.check_output(cmd, text=True, stderr=subprocess.STDOUT)


def _try_json(text: str, fallback_cmd: list[str] | None = None):
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return {"raw": text, "cmd": fallback_cmd or []}


def run_openclaw_agent(agent_id: str, message: str, timeout: int = 600):
    cmd = [
        "openclaw", "agent",
        "--agent", agent_id,
        "--message", message,
        "--json",
        "--timeout", str(timeout),
    ]
    out = _run(cmd)
    payload = _try_json(out, cmd)
    if isinstance(payload, dict):
        payload.setdefault("_meta", {})
        payload["_meta"].update({
            "agent_id": agent_id,
            "timeout": timeout,
            "message_chars": len(message),
        })
    return payload


def list_sessions_json(all_agents: bool = True):
    cmd = ["openclaw", "sessions", "--json"]
    if all_agents:
        cmd.append("--all-agents")
    out = _run(cmd)
    return _try_json(out, cmd)


def extract_sessions(payload) -> list[dict[str, Any]]:
    if isinstance(payload, dict):
        return payload.get("sessions", [])
    if isinstance(payload, list):
        return payload
    return []


def sessions_for_agent(agent_id: str, all_agents: bool = True) -> list[dict[str, Any]]:
    if not agent_id:
        return []
    payload = list_sessions_json(all_agents=all_agents)
    sessions = extract_sessions(payload)
    return [s for s in sessions if s.get("agentId") == agent_id]


def newest_session_for_agent(agent_id: str, all_agents: bool = True):
    sessions = sessions_for_agent(agent_id, all_agents=all_agents)
    if not sessions:
        return None
    return sorted(sessions, key=lambda x: x.get("updatedAt", 0), reverse=True)[0]


def session_age_minutes(session: dict[str, Any] | None) -> float | None:
    if not session:
        return None
    age_ms = session.get("ageMs")
    if age_ms is None:
        return None
    return round(age_ms / 60000.0, 2)


def probe_agents(agent_ids: list[str]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for agent_id in agent_ids:
        if not agent_id:
            continue
        session = newest_session_for_agent(agent_id)
        result[agent_id] = {
            "agent_id": agent_id,
            "session": session,
            "age_minutes": session_age_minutes(session),
            "has_existing_session": bool(session),
        }
    return result


def choose_dispatch_mode(agent_id: str) -> str:
    session = newest_session_for_agent(agent_id)
    return "reuse-existing-session" if session else "fresh-agent-turn"


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


def build_session_reuse_hint(agent_id: str) -> dict[str, Any]:
    session = newest_session_for_agent(agent_id)
    return {
        "agent_id": agent_id,
        "dispatch_mode": "reuse-existing-session" if session else "fresh-agent-turn",
        "session_key": session.get("key") if session else None,
        "session_age_minutes": session_age_minutes(session),
    }


def ensure_json_dict(value: Any) -> dict[str, Any]:
    if isinstance(value, dict):
        return value
    return {"raw": str(value)}


def write_json(path: Path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
