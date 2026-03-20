#!/usr/bin/env python3
import argparse
import json
from pathlib import Path
from runtime_lib import run_openclaw_agent, write_json


def build_message(payload: dict) -> str:
    return (
        "你收到一条 Multi-Agent-Collaboration 结构化任务，请按 JSON 理解并处理。\n\n"
        + json.dumps(payload, ensure_ascii=False, indent=2)
    )


def main():
    parser = argparse.ArgumentParser(description="Dispatch a structured JSON task to a real OpenClaw agent via CLI")
    parser.add_argument("message_json", help="Path to dispatch message JSON")
    parser.add_argument("--agent-id", required=True, help="OpenClaw agent id to receive this task")
    parser.add_argument("--output", help="Optional output JSON file")
    parser.add_argument("--timeout", type=int, default=600)
    args = parser.parse_args()

    payload = json.loads(Path(args.message_json).read_text(encoding="utf-8"))
    result = run_openclaw_agent(args.agent_id, build_message(payload), timeout=args.timeout)
    rendered = {"agent_id": args.agent_id, "message": payload, "result": result}

    if args.output:
        write_json(Path(args.output), rendered)
    print(json.dumps(rendered, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
