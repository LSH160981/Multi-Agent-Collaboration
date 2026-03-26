#!/usr/bin/env python3
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import inspect_and_recover as mod


def main():
    stale = 30
    cases = [
        (None, "rebuild"),
        ({}, "probe"),
        ({"ageMs": 5 * 60 * 1000}, "resume"),
        ({"ageMs": 120 * 60 * 1000}, "redispatch"),
        ({"ageMs": 360 * 60 * 1000}, "rebuild"),
    ]
    results = []
    ok = True
    for payload, expected in cases:
        actual = mod.recommend_session_action(payload, stale)
        passed = actual == expected
        results.append({
            "input": payload,
            "expected": expected,
            "actual": actual,
            "passed": passed,
        })
        ok = ok and passed

    report = {"status": "ok" if ok else "fail", "results": results}
    print(json.dumps(report, ensure_ascii=False, indent=2))
    raise SystemExit(0 if ok else 1)


if __name__ == "__main__":
    main()
