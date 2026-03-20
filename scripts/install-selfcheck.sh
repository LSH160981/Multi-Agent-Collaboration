#!/usr/bin/env bash
set -euo pipefail

WORKSPACE="${1:-$HOME/.openclaw/workspace}"
SKILL_DIR="$WORKSPACE/skills/Multi-Agent-Collaboration"
MAC_DIR="$WORKSPACE/mac-system"

printf '%s\n' '== Multi-Agent-Collaboration 自检 =='

if [ -d "$SKILL_DIR" ]; then
  echo "[OK] skill 已安装：$SKILL_DIR"
else
  echo "[WARN] 未发现 skill：$SKILL_DIR"
fi

for dir in "$MAC_DIR" "$MAC_DIR/agents" "$MAC_DIR/shared" "$MAC_DIR/tasks" "$MAC_DIR/logs" "$MAC_DIR/research"; do
  if [ -d "$dir" ]; then
    echo "[OK] 目录存在：$dir"
  else
    echo "[WARN] 缺少目录：$dir"
  fi
done

echo "[TODO] 请按 测试脚本.md 执行："
echo "       1. Agent 两两握手测试"
echo "       2. 静默任务测试"
echo "       3. 恢复测试"
