#!/usr/bin/env python3
import argparse
import json
import subprocess
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
PY = "python3"


def main():
    parser = argparse.ArgumentParser(description="Smoke test: repair + resume pipeline state")
    parser.add_argument("--workspace", default="/root/.openclaw/workspace")
    parser.add_argument("--outdir", default=str(REPO / "examples" / "generated" / "staged-runtime"))
    args = parser.parse_args()

    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    state_path = outdir / "pipeline-state.json"

    broken = {
        "stage": "stage2_done",
        "task_packet": {
            "task_id": "TEST-RECOVERY",
            "goal": "test recovery",
            "task_type": "research"
        },
        "group_plan": {},
        "pool_result": {},
        "inspect_result": {},
        "worker_role": "Research"
    }
    state_path.write_text(json.dumps(broken, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    before = subprocess.run([PY, str(REPO / "scripts" / "validate_pipeline_state.py"), str(state_path)], capture_output=True, text=True)
    inspect = subprocess.check_output([
        PY, str(REPO / "scripts" / "inspect_and_recover.py"),
        args.workspace,
        "--auto-repair-pipeline",
        "--auto-resume-pipeline",
    ], text=True)
    after = subprocess.run([PY, str(REPO / "scripts" / "validate_pipeline_state.py"), str(state_path)], capture_output=True, text=True)

    result = {
        "before": before.stdout,
        "inspect": inspect,
        "after": after.stdout,
        "after_code": after.returncode,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
