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


def main():
    parser = argparse.ArgumentParser(description="Probe OpenClaw stored sessions for Multi-Agent-Collaboration diagnostics")
    parser.add_argument("--output", help="Optional output JSON path")
    parser.add_argument("--all-agents", action="store_true", default=True)
    args = parser.parse_args()

    data = list_sessions(all_agents=args.all_agents)
    if isinstance(data, list):
        summary = {
            "session_count": len(data),
            "sessions": data,
        }
    else:
        summary = data

    rendered = json.dumps(summary, ensure_ascii=False, indent=2)
    if args.output:
        out = Path(args.output)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(rendered + "\n", encoding="utf-8")
    print(rendered)


if __name__ == "__main__":
    main()
