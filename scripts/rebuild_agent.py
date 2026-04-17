#!/usr/bin/env python3
"""rebuild_agent.py

重建或补齐 mac-system/agents 下的 Agent 骨架。

职责：
- 为缺失或损坏的 agent 目录重新生成最小可运行骨架。
- 统一创建 AGENTS.md / abilities.md / queue / logs / memory / artifacts。
- 作为 inspect_and_recover / 手工排障里的明确 rebuild 执行器。

说明：
- 这是仓库脚本层的“角色骨架重建器”，不是 OpenClaw 平台能力本身。
- 默认只补齐缺失内容；传 --overwrite 才会覆盖已有文档文件。
"""

import argparse
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
TEMPLATES = REPO / "templates"


def read_text(path: Path, fallback: str) -> str:
    if path.exists():
        return path.read_text(encoding="utf-8")
    return fallback


def render_agents_md(role_name: str, role_kind: str) -> str:
    template = read_text(
        TEMPLATES / "agent" / "AGENTS.md",
        "# Agent 模板\n\n- 不直接联系用户（若非主Agent）\n",
    )
    return (
        f"# {role_name}\n\n"
        f"你是 Multi-Agent-Collaboration 系统中的 {role_name}。\n"
        f"角色类型：{role_kind}\n\n"
        + template
    )


def render_abilities_md(role_name: str, role_kind: str) -> str:
    specialist_template_map = {
        "research": TEMPLATES / "specialist" / "abilities-research.md",
        "test": TEMPLATES / "specialist" / "abilities-test.md",
        "frontend": TEMPLATES / "specialist" / "abilities-frontend.md",
    }
    base = read_text(TEMPLATES / "agent" / "abilities.md", "# abilities\n")
    specialist = specialist_template_map.get(role_kind)
    specialist_text = read_text(specialist, "") if specialist else ""
    header = (
        "# abilities.md\n\n"
        "## 角色名称\n\n"
        f"- 名称：{role_name}\n"
        f"- 英文名：{role_kind}\n\n"
    )
    return header + (specialist_text.strip() + "\n\n" if specialist_text else "") + base


def ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def write_if_needed(path: Path, content: str, overwrite: bool) -> str:
    if path.exists() and not overwrite:
        return "kept"
    path.write_text(content.rstrip() + "\n", encoding="utf-8")
    return "written" if overwrite or not path.exists() else "kept"


def rebuild_agent(workspace: Path, agent_dir_name: str, role_name: str, role_kind: str, overwrite: bool) -> dict:
    target = workspace / "mac-system" / "agents" / agent_dir_name
    ensure_dir(target)
    for child in ["queue", "logs", "memory", "artifacts"]:
        ensure_dir(target / child)

    agents_status = write_if_needed(target / "AGENTS.md", render_agents_md(role_name, role_kind), overwrite)
    abilities_status = write_if_needed(target / "abilities.md", render_abilities_md(role_name, role_kind), overwrite)

    return {
        "agent_dir": agent_dir_name,
        "role_name": role_name,
        "role_kind": role_kind,
        "target": str(target),
        "agents_md": agents_status,
        "abilities_md": abilities_status,
        "overwrite": overwrite,
    }


def main():
    parser = argparse.ArgumentParser(description="Rebuild or repair a mac-system agent skeleton")
    parser.add_argument("workspace", help="OpenClaw workspace path")
    parser.add_argument("agent_dir_name", help="Directory name under mac-system/agents")
    parser.add_argument("--role-name", help="Displayed role name", default="")
    parser.add_argument("--role-kind", help="Role kind: research|test|frontend|general", default="general")
    parser.add_argument("--overwrite", action="store_true", help="Overwrite AGENTS.md / abilities.md if they already exist")
    args = parser.parse_args()

    workspace = Path(args.workspace)
    role_name = args.role_name or args.agent_dir_name
    result = rebuild_agent(workspace, args.agent_dir_name, role_name, args.role_kind.lower(), args.overwrite)
    import json
    print(json.dumps({"status": "ok", **result}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
