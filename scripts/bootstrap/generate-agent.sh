#!/usr/bin/env bash
set -euo pipefail

if [ "$#" -lt 3 ]; then
  echo "用法: $0 <workspace> <agent-dir-name> <role-name>"
  exit 1
fi

WORKSPACE="$1"
AGENT_DIR_NAME="$2"
ROLE_NAME="$3"
TARGET_DIR="$WORKSPACE/mac-system/agents/$AGENT_DIR_NAME"

mkdir -p "$TARGET_DIR/queue" "$TARGET_DIR/logs" "$TARGET_DIR/memory" "$TARGET_DIR/artifacts"

cat > "$TARGET_DIR/AGENTS.md" <<EOF
# $ROLE_NAME

你是 Multi-Agent-Collaboration 系统中的 $ROLE_NAME。

- 不直接联系用户（除非这是主Agent）
- 遵守能力边界
- 维护 queue / logs / memory / artifacts
EOF

cat > "$TARGET_DIR/abilities.md" <<EOF
# abilities

## 角色
- $ROLE_NAME

## 可以做
- 根据具体任务补充

## 不能做
- 不直接联系用户（若非主Agent）
EOF

echo "已生成 Agent 目录：$TARGET_DIR"
