#!/usr/bin/env bash
set -euo pipefail

WORKSPACE="${1:-$HOME/.openclaw/workspace}"
SKILL_DIR="$WORKSPACE/skills/Multi-Agent-Collaboration"
MAC_BRIDGE_DIR="$WORKSPACE/skills/mac"
MAC_DIR="$WORKSPACE/mac-system"

printf '%s\n' '== Multi-Agent-Collaboration 自检 =='

if [ -d "$SKILL_DIR" ]; then
  echo "[OK] 主 skill 已安装：$SKILL_DIR"
else
  echo "[WARN] 未发现主 skill：$SKILL_DIR"
fi

if [ -d "$MAC_BRIDGE_DIR" ]; then
  echo "[OK] /mac 命令桥 skill 已安装：$MAC_BRIDGE_DIR"
else
  echo "[WARN] 未发现 /mac 命令桥 skill：$MAC_BRIDGE_DIR"
fi

for dir in "$MAC_DIR" "$MAC_DIR/agents" "$MAC_DIR/shared" "$MAC_DIR/tasks" "$MAC_DIR/logs" "$MAC_DIR/research"; do
  if [ -d "$dir" ]; then
    echo "[OK] 目录存在：$dir"
  else
    echo "[WARN] 缺少目录：$dir"
  fi
done

echo "[INFO] 若要看到原生命令 /mac，请确认已安装 user-invocable skill: skills/mac"
echo "[TODO] 请按 测试脚本.md 执行："
echo "       1. Agent 两两握手测试"
echo "       2. 静默任务测试"
echo "       3. 恢复测试"
echo "       4. 原生 session 调度 demo：./scripts/runtime_sessions.py \"/mac 调研最近 30 天值得关注的 OpenClaw 多Agent 项目\""
