#!/usr/bin/env python3
import argparse
import json
from datetime import datetime
from pathlib import Path


def ensure_dir(path: Path):
    path.mkdir(parents=True, exist_ok=True)


def append_log(agent_dir: Path, message: dict):
    ensure_dir(agent_dir / "logs")
    log_file = agent_dir / "logs" / f"{datetime.now().strftime('%Y-%m-%d')}.md"
    with log_file.open("a", encoding="utf-8") as f:
        f.write(f"- time: {datetime.now().isoformat()}\n")
        f.write(f"- type: {message['type']}\n")
        f.write(f"- task_id: {message['task_id']}\n")
        f.write(f"- from: {message['from']}\n")
        f.write(f"- to: {message['to']}\n")
        f.write(f"- goal: {message.get('goal', '')}\n\n")


def write_queue(agent_dir: Path, message: dict):
    ensure_dir(agent_dir / "queue")
    queue_file = agent_dir / "queue" / f"{message['task_id']}.json"
    queue_file.write_text(json.dumps(message, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description="Write structured dispatch message into sender/receiver logs and receiver queue")
    parser.add_argument("workspace", help="OpenClaw workspace path")
    parser.add_argument("message_json", help="Path to message JSON")
    args = parser.parse_args()

    workspace = Path(args.workspace)
    mac_agents = workspace / "mac-system" / "agents"
    message = json.loads(Path(args.message_json).read_text(encoding="utf-8"))

    sender_dir = mac_agents / message["from"]
    receiver_dir = mac_agents / message["to"]
    ensure_dir(sender_dir)
    ensure_dir(receiver_dir)

    append_log(sender_dir, message)
    append_log(receiver_dir, message)
    write_queue(receiver_dir, message)

    print(json.dumps({
        "status": "ok",
        "sender_log": str(sender_dir / 'logs'),
        "receiver_log": str(receiver_dir / 'logs'),
        "receiver_queue": str(receiver_dir / 'queue' / f"{message['task_id']}.json")
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
