#!/usr/bin/env python3
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

REPO = Path(__file__).resolve().parent.parent
PROTOCOL_PATH = REPO / "skills" / "Multi-Agent-Collaboration" / "通信协议.json"


def load_protocol() -> dict[str, Any]:
    return json.loads(PROTOCOL_PATH.read_text(encoding="utf-8"))


def iso_now() -> str:
    return datetime.now(timezone.utc).astimezone().isoformat()


def required_fields(message_type: str) -> list[str]:
    protocol = load_protocol()
    return protocol["message_types"].get(message_type, {}).get("required", [])


def optional_fields(message_type: str) -> list[str]:
    protocol = load_protocol()
    return protocol["message_types"].get(message_type, {}).get("optional", [])


def build_message(message_type: str, **kwargs) -> dict[str, Any]:
    msg = {
        "message_type": message_type,
        "timestamp": kwargs.pop("timestamp", iso_now()),
        **kwargs,
    }
    validate_message(msg)
    return msg


def validate_message(msg: dict[str, Any]) -> None:
    message_type = msg.get("message_type")
    if not message_type:
        raise ValueError("message_type is required")
    req = required_fields(message_type)
    if not req:
        raise ValueError(f"unknown message_type: {message_type}")
    missing = [k for k in req if k not in msg or msg.get(k) in (None, "")]
    if missing:
        raise ValueError(f"message missing required fields: {missing}")


def build_task_assign(task_id: str, from_agent: str, to_agent: str, goal: str, **kwargs) -> dict[str, Any]:
    payload = {
        "task_id": task_id,
        "from": from_agent,
        "to": to_agent,
        "goal": goal,
        "status": kwargs.pop("status", "assigned"),
        **kwargs,
    }
    return build_message("task_assign", **payload)


def build_review_scorecard(task_id: str, from_agent: str, to_agent: str, **kwargs) -> dict[str, Any]:
    payload = {
        "task_id": task_id,
        "from": from_agent,
        "to": to_agent,
        "status": kwargs.pop("status", "reviewed"),
        **kwargs,
    }
    return build_message("review_scorecard", **payload)


def build_recovery_action(task_id: str, from_agent: str, to_agent: str, reason: str, **kwargs) -> dict[str, Any]:
    payload = {
        "task_id": task_id,
        "from": from_agent,
        "to": to_agent,
        "status": kwargs.pop("status", "recover"),
        "reason": reason,
        **kwargs,
    }
    return build_message("recovery_action", **payload)
