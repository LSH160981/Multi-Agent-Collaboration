#!/usr/bin/env bash
set -euo pipefail

WORKSPACE="${1:-$HOME/.openclaw/workspace}"
ROOT="$WORKSPACE/mac-system"

mkdir -p "$ROOT/agents/主Agent" "$ROOT/agents/审核Agent" "$ROOT/agents/检查Agent" "$ROOT/agents/AgentPool"
mkdir -p "$ROOT/shared" "$ROOT/tasks" "$ROOT/logs" "$ROOT/research"

for agent in 主Agent 审核Agent 检查Agent AgentPool; do
  mkdir -p "$ROOT/agents/$agent/queue" "$ROOT/agents/$agent/logs" "$ROOT/agents/$agent/memory" "$ROOT/agents/$agent/artifacts"
  touch "$ROOT/agents/$agent/queue/.gitkeep" "$ROOT/agents/$agent/logs/.gitkeep" "$ROOT/agents/$agent/memory/.gitkeep" "$ROOT/agents/$agent/artifacts/.gitkeep"
done

echo "已初始化：$ROOT"
echo "建议下一步："
echo "1. 运行 scripts/install-selfcheck.sh"
echo "2. 按 skills/Multi-Agent-Collaboration/测试脚本.md 执行测试"
