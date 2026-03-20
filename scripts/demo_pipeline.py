#!/usr/bin/env python3
import argparse
import json
import subprocess
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent


def run(cmd):
    return subprocess.check_output(cmd, text=True)


def main():
    parser = argparse.ArgumentParser(description="Run a demo pipeline: parse -> recruit -> dispatch(local files) -> score -> dedupe")
    parser.add_argument("text", help="Raw /mac text")
    parser.add_argument("--workspace", default=str(Path.home() / ".openclaw/workspace"))
    parser.add_argument("--outdir", default=str(REPO / "examples" / "generated" / "demo-pipeline"))
    args = parser.parse_args()

    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    task_packet = outdir / "task-packet.json"
    group_plan = outdir / "group-plan.json"
    dispatch_result = outdir / "dispatch-result.json"
    score_result = outdir / "scorecard.json"
    dedupe_result = outdir / "dedupe-result.json"

    subprocess.check_call([str(REPO / "scripts" / "mac_cli.py"), args.text, "--output", str(task_packet)])
    subprocess.check_call([str(REPO / "scripts" / "recruit_team.py"), str(task_packet), "--output", str(group_plan)])
    subprocess.check_call([str(REPO / "scripts" / "dispatch_task.py"), args.workspace, str(REPO / "examples" / "dispatch-message-example.json")], stdout=dispatch_result.open("w", encoding="utf-8"))
    subprocess.check_call([str(REPO / "scripts" / "score_result.py"), str(REPO / "examples" / "result-package-example.json")], stdout=score_result.open("w", encoding="utf-8"))
    subprocess.check_call([str(REPO / "scripts" / "dedupe_summary.py"), str(REPO / "examples" / "dedupe-input.json")], stdout=dedupe_result.open("w", encoding="utf-8"))

    print(json.dumps({"status": "ok", "outdir": str(outdir)}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
