#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
TARGET_WORKSPACE="${1:-$HOME/.openclaw/workspace}"
TARGET_SKILLS_DIR="$TARGET_WORKSPACE/skills"
TARGET_SKILL_DIR="$TARGET_SKILLS_DIR/Multi-Agent-Collaboration"

mkdir -p "$TARGET_SKILLS_DIR"
rm -rf "$TARGET_SKILL_DIR"
cp -R "$REPO_ROOT/skills/Multi-Agent-Collaboration" "$TARGET_SKILL_DIR"

mkdir -p "$TARGET_WORKSPACE/mac-system/agents"
mkdir -p "$TARGET_WORKSPACE/mac-system/shared"
mkdir -p "$TARGET_WORKSPACE/mac-system/tasks"
mkdir -p "$TARGET_WORKSPACE/mac-system/logs"
mkdir -p "$TARGET_WORKSPACE/mac-system/research"

echo "安装完成：$TARGET_SKILL_DIR"
echo "建议下一步："
echo "1. 新开一个 OpenClaw session 或刷新 skills"
echo "2. 阅读 $TARGET_SKILL_DIR/安装与使用.md"
echo "3. 按 测试脚本.md 执行握手测试和静默任务测试"
