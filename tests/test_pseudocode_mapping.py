#!/usr/bin/env python3
import json
import re
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
MAPPING = REPO / "docs" / "architecture" / "伪代码到代码映射.md"

CODE_PATTERNS = [
    re.compile(r"`((?:scripts|tests|skills|schemas|examples)/[^`]+)`"),
]


def extract_paths(text: str):
    found = []
    for pattern in CODE_PATTERNS:
        found.extend(pattern.findall(text))
    return sorted(set(found))


def main():
    text = MAPPING.read_text(encoding="utf-8")
    paths = extract_paths(text)
    checks = []
    ok = True
    for rel in paths:
        exists = (REPO / rel).exists()
        checks.append({"path": rel, "exists": exists})
        ok = ok and exists

    report = {
        "status": "ok" if ok else "fail",
        "mapping": str(MAPPING),
        "count": len(checks),
        "checks": checks,
    }
    print(json.dumps(report, ensure_ascii=False, indent=2))
    raise SystemExit(0 if ok else 1)


if __name__ == "__main__":
    main()
