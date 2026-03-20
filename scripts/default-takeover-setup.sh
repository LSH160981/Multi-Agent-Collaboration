#!/usr/bin/env bash
set -euo pipefail

WORKSPACE="${1:-$HOME/.openclaw/workspace}"
REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SHARED_SKILLS_DIR="$HOME/.openclaw/skills"
TARGET_SKILL_DIR="$SHARED_SKILLS_DIR/Multi-Agent-Collaboration"

mkdir -p "$SHARED_SKILLS_DIR"
rm -rf "$TARGET_SKILL_DIR"
cp -R "$REPO_ROOT/skills/Multi-Agent-Collaboration" "$TARGET_SKILL_DIR"

"$REPO_ROOT/scripts/init-mac-system.sh" "$WORKSPACE" >/dev/null

cat <<EOF
已完成默认接管基础安装：
- 共享 skill: $TARGET_SKILL_DIR
- 工作目录: $WORKSPACE/mac-system

这代表：
1. 所有本机 OpenClaw Agent 都能读到 Multi-Agent-Collaboration skill
2. mac-system 目录已初始化
3. 复杂任务现在可以默认按本 skill 的方法论处理

建议下一步：
- 运行: $REPO_ROOT/scripts/install-selfcheck.sh "$WORKSPACE"
- 新开一个 OpenClaw session
- 发送: /mac 调研最近 30 天值得关注的 OpenClaw 多Agent 项目
EOF
