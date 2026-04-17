#!/usr/bin/env python3
import json
import shutil
import subprocess
import tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent


def main():
    tmp = Path(tempfile.mkdtemp(prefix="mac-rebuild-agent-"))
    try:
        workspace = tmp / "workspace"
        cmd = [
            "python3",
            str(REPO / "scripts" / "rebuild_agent.py"),
            str(workspace),
            "research-worker-1",
            "--role-name",
            "Research Worker 1",
            "--role-kind",
            "research",
        ]
        proc = subprocess.run(cmd, capture_output=True, text=True)
        target = workspace / "mac-system" / "agents" / "research-worker-1"
        file_checks = {
            "target_exists": target.exists(),
            "agents_md_exists": (target / "AGENTS.md").exists(),
            "abilities_md_exists": (target / "abilities.md").exists(),
            "queue_exists": (target / "queue").exists(),
            "logs_exists": (target / "logs").exists(),
            "memory_exists": (target / "memory").exists(),
            "artifacts_exists": (target / "artifacts").exists(),
        }
        report = {
            "status": "ok" if proc.returncode == 0 and all(file_checks.values()) else "fail",
            "command": cmd,
            "stdout": proc.stdout,
            "stderr": proc.stderr,
            "checks": {
                "exit_code": proc.returncode,
                **file_checks,
            },
        }
        print(json.dumps(report, ensure_ascii=False, indent=2))
        raise SystemExit(0 if report["status"] == "ok" else 1)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    main()
