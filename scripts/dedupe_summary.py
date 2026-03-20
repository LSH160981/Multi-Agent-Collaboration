#!/usr/bin/env python3
import argparse
import json
from pathlib import Path


def normalize(line: str) -> str:
    return "".join(line.split()).lower()


def dedupe(items):
    seen = set()
    kept = []
    for item in items:
        key = normalize(item)
        if key and key not in seen:
            seen.add(key)
            kept.append(item)
    return kept


def main():
    parser = argparse.ArgumentParser(description="Dedupe candidate lines into a user-facing concise summary")
    parser.add_argument("input_json", help="JSON file containing {items:[...]} or a raw list")
    parser.add_argument("--output", help="Optional output path")
    args = parser.parse_args()

    data = json.loads(Path(args.input_json).read_text(encoding="utf-8"))
    items = data["items"] if isinstance(data, dict) else data
    kept = dedupe(items)
    result = {"items": kept, "summary": "\n".join(f"- {x}" for x in kept)}
    rendered = json.dumps(result, ensure_ascii=False, indent=2)
    if args.output:
        Path(args.output).write_text(rendered + "\n", encoding="utf-8")
    print(rendered)


if __name__ == "__main__":
    main()
