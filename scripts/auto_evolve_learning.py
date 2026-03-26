#!/usr/bin/env python3
import argparse
import json
import urllib.request
from datetime import datetime
from pathlib import Path

from runtime_lib import run_openclaw_agent, write_json

REPO = Path(__file__).resolve().parent.parent
DEFAULT_SOURCES = [
    {"name": "openclaw-docs-pi", "kind": "url", "url": "https://docs.openclaw.ai/zh-CN/pi"},
    {"name": "clawhub-agent-team-orchestration", "kind": "url", "url": "https://clawhub.ai/arminnaimi/agent-team-orchestration"},
    {"name": "clawhub-agent-directory", "kind": "url", "url": "https://clawhub.ai/aerialcombat/agent-directory"},
    {"name": "blog-openclaw-tui-agent", "kind": "url", "url": "https://zelikk.blogspot.com/2026/03/openclaw-tui-agent.html"},
    {"name": "blog-openclaw-tui-agent-cooperate", "kind": "url", "url": "https://zelikk.blogspot.com/2026/03/openclaw-tui-agent-cooperate.html"},
]


def fetch_url(url: str) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 Multi-Agent-Collaboration"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return resp.read().decode("utf-8", errors="ignore")


def build_local_summary(items: list[dict]) -> str:
    lines = [
        "# 自动学习候选报告",
        "",
        "本报告由 auto_evolve_learning.py 自动生成。",
        "原则：先抓取资料，先落 research，再交给审核Agent判断是否值得吸收。",
        "",
        "## 本轮来源摘要",
    ]
    for item in items:
        lines.append(f"- {item['name']}: status={item['status']} chars={item.get('chars', 0)}")
    lines += [
        "",
        "## 建议审核问题",
        "1. 哪些点值得吸收进主 skill？",
        "2. 哪些只是参考，不应直接照搬？",
        "3. 哪些点需要补代码而不是补文档？",
        "4. 哪些点会和主Agent唯一出口规则冲突？",
        "5. 如果要吸收，应该改哪些文件？",
    ]
    return "\n".join(lines) + "\n"


def build_evolve_plan(review_result: dict | None) -> dict:
    if not isinstance(review_result, dict):
        return {
            "status": "needs-review",
            "targets": ["research/README.md", "docs/research/多agent协同案例提炼.md", "docs/自动学习与审核后自进化.md"],
            "actions": ["等待审核Agent给出 should_absorb/code_first/doc_first 结论"],
        }
    text = json.dumps(review_result, ensure_ascii=False)
    targets = ["research/README.md", "docs/research/多agent协同案例提炼.md"]
    if "code_first" in text:
        targets += ["scripts/runtime_orchestrator.py", "scripts/protocol_lib.py", "scripts/staffing_decision.py"]
    if "doc_first" in text:
        targets += ["skills/multi-agent-collaboration/SKILL.md", "docs/architecture/项目骨架与逻辑执行流程.md"]
    return {
        "status": "reviewed",
        "targets": targets,
        "actions": [
            "先把外部观点整理进 research",
            "再由主Agent审核是否更新 skill/docs/scripts",
            "涉及运行逻辑时优先小步提交",
        ],
    }


def main():
    parser = argparse.ArgumentParser(description="Fetch learning sources, store locally, and optionally ask review agent for evolution advice")
    parser.add_argument("--outdir", default=str(REPO / "research" / "auto"))
    parser.add_argument("--review-agent", default="review-judge")
    parser.add_argument("--with-review", action="store_true")
    args = parser.parse_args()

    outdir = Path(args.outdir)
    raw_dir = outdir / "raw"
    raw_dir.mkdir(parents=True, exist_ok=True)

    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    items = []
    for source in DEFAULT_SOURCES:
        entry = {"name": source["name"], "kind": source["kind"], "url": source["url"]}
        try:
            text = fetch_url(source["url"])
            target = raw_dir / f"{source['name']}-{stamp}.html"
            target.write_text(text, encoding="utf-8")
            entry.update({"status": "ok", "chars": len(text), "saved_to": str(target)})
        except Exception as e:
            entry.update({"status": "error", "error": str(e)})
        items.append(entry)

    summary_md = build_local_summary(items)
    summary_path = outdir / f"learning-summary-{stamp}.md"
    summary_path.write_text(summary_md, encoding="utf-8")

    packet = {
        "generated_at": stamp,
        "sources": items,
        "summary_path": str(summary_path),
        "review_result": None,
        "evolve_plan": None,
    }

    if args.with_review:
        prompt = (
            "你是审核Agent。请审查这批自动学习候选资料。只输出 JSON："
            '{"should_absorb":[""],"should_not_absorb":[""],"code_first":[""],"doc_first":[""],"risks":[""],"file_targets":[""]}'
            + "\n\n"
            + summary_md
        )
        packet["review_result"] = run_openclaw_agent(args.review_agent, prompt, timeout=300)

    packet["evolve_plan"] = build_evolve_plan(packet.get("review_result"))

    write_json(outdir / f"learning-packet-{stamp}.json", packet)
    print(json.dumps({"status": "ok", "summary": str(summary_path), "review": bool(args.with_review), "evolve_plan": packet['evolve_plan']}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
