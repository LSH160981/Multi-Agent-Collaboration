#!/usr/bin/env bash
set -euo pipefail

WORKSPACE="${1:-$HOME/.openclaw/workspace}"
ROOT="$WORKSPACE/mac-system/agents"

mkdir -p "$ROOT"

make_agent() {
  local dir_name="$1"
  local role_name="$2"
  mkdir -p "$ROOT/$dir_name/queue" "$ROOT/$dir_name/logs" "$ROOT/$dir_name/memory" "$ROOT/$dir_name/artifacts"
  cat > "$ROOT/$dir_name/AGENTS.md" <<EOF
# $role_name

你是 Multi-Agent-Collaboration 系统中的 $role_name。

- 不直接联系用户
- 遵守能力边界
- 维护 queue / logs / memory / artifacts
EOF
  cat > "$ROOT/$dir_name/abilities.md" <<EOF
# abilities

## 角色
- $role_name

## 可以做
- 根据具体任务补充

## 不能做
- 不直接联系用户
EOF
}

make_agent "A组-组长-Lead" "A组组长"
make_agent "A组-前端专家-Frontend" "A组前端专家"
make_agent "A组-测试专家-Test" "A组测试专家"
make_agent "B组-组长-Lead" "B组组长"
make_agent "B组-检索专家-Research" "B组检索专家"
make_agent "B组-验证专家-Verification" "B组验证专家"

echo "已生成 A/B 两组 specialist 骨架：$ROOT"
