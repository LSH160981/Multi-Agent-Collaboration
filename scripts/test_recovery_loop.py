#!/usr/bin/env python3
import argparse
import json
import subprocess
from pathlib import Path

from runtime_lib import write_json

REPO = Path(__file__).resolve().parent.parent


def main():
    parser = argparse.ArgumentParser(description="Recovery loop test for Multi-Agent-Collaboration")
    parser.add_argument("workspace", help="OpenClaw workspace path")
    parser.add_argument("--stale-minutes", type=int, default=1)
    parser.add_argument("--recovery-agent-map", help="JSON file mapping dir names to agent ids")
    parser.add_argument("--execute", action="store_true")
    parser.add_argument("--output", default=str(REPO / "examples" / "generated" / "tests" / "recovery-report.json"))
    args = parser.parse_args()

    cmd = [
        str(REPO / "scripts" / "inspect_and_recover.py"),
        args.workspace,
        "--stale-minutes", str(args.stale_minutes),
    ]
    if args.recovery_agent_map:
        cmd.extend(["--recovery-agent-map", args.recovery_agent_map])
    if args.execute:
        cmd.append("--execute")

    out = subprocess.check_output(cmd, text=True)
    data = json.loads(out)
    write_json(Path(args.output), data)
    print(json.dumps({"status": "ok", "output": args.output}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
