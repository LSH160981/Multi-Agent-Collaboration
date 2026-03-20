#!/usr/bin/env python3
import argparse
import json
import re
from datetime import datetime
from pathlib import Path


def infer_task_type(text: str) -> str:
    lowered = text.lower()
    if any(k in lowered for k in ["开发", "编码", "代码", "debug", "bug", "网页", "app", "api"]):
        return "coding"
    if any(k in lowered for k in ["调研", "搜索", "研究", "对比", "总结", "资料"]):
        return "research"
    if any(k in lowered for k in ["排查", "故障", "恢复", "运维", "监控", "日志"]):
        return "ops"
    return "mixed"


def infer_complexity(text: str) -> str:
    signals = 0
    for key in ["并", "同时", "比较", "总结", "验证", "排查", "开发", "调研", "优化", "多"]:
        if key in text:
            signals += 1
    if len(text) > 50:
        signals += 1
    if signals >= 4:
        return "high"
    if signals >= 2:
        return "medium"
    return "low"


def infer_specialists(task_type: str):
    mapping = {
        "coding": ["Frontend", "Test", "Verification"],
        "research": ["Research", "Verification", "Summary"],
        "ops": ["LogAnalysis", "Recovery", "Verification"],
        "mixed": ["Research", "Implementation", "Verification"],
    }
    return mapping.get(task_type, ["Research", "Verification"])


def needs_clarification(text: str) -> bool:
    if len(text.strip()) < 8:
        return True
    unclear_patterns = [r"帮我弄一下", r"做一个", r"看看这个", r"处理一下"]
    return any(re.search(p, text) for p in unclear_patterns) and len(text) < 20


def build_packet(raw: str):
    content = raw.strip()
    if content.startswith("/mac"):
        content = content[4:].strip()
    now = datetime.now().strftime("%Y%m%d-%H%M%S")
    task_type = infer_task_type(content)
    complexity = infer_complexity(content)
    clarification = needs_clarification(content)
    return {
        "entry": "mac",
        "task_id": f"TASK-{now}",
        "user_intent": content,
        "goal": content,
        "task_type": task_type,
        "complexity": complexity,
        "needs_clarification": clarification,
        "clarification_questions": ["请补充更明确的目标、输出形式或约束。"] if clarification else [],
        "required_roles": ["主Agent", "AgentPool", "审核Agent", "检查Agent"],
        "specialists": infer_specialists(task_type),
        "execution_mode": "dual-group" if complexity in {"medium", "high"} else "single-group",
        "output_requirements": ["总结", "验证步骤", "风险说明"],
        "constraints": ["禁止非主Agent联系用户"]
    }


def main():
    parser = argparse.ArgumentParser(description="Parse /mac task text into a structured task packet")
    parser.add_argument("text", help="Raw /mac text or plain complex-task text")
    parser.add_argument("--output", help="Optional output JSON path")
    args = parser.parse_args()

    packet = build_packet(args.text)
    rendered = json.dumps(packet, ensure_ascii=False, indent=2)
    if args.output:
        Path(args.output).write_text(rendered + "\n", encoding="utf-8")
    print(rendered)


if __name__ == "__main__":
    main()
