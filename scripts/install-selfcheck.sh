#!/usr/bin/env bash
set -euo pipefail

WORKSPACE="${1:-$HOME/.openclaw/workspace}"
SKILL_DIR="$WORKSPACE/skills/Multi-Agent-Collaboration"
MAC_BRIDGE_DIR="$WORKSPACE/skills/mac"
SHARED_MAC_BRIDGE_DIR="$HOME/.openclaw/skills/mac"
MAC_DIR="$WORKSPACE/mac-system"
REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"

printf '%s\n' '== Multi-Agent-Collaboration 自检 =='

if [ -d "$SKILL_DIR" ]; then
  echo "[OK] 主 skill 已安装：$SKILL_DIR"
else
  echo "[WARN] 未发现主 skill：$SKILL_DIR"
fi

if [ -d "$MAC_BRIDGE_DIR" ]; then
  echo "[OK] /mac 命令桥 skill 已安装（workspace）：$MAC_BRIDGE_DIR"
elif [ -d "$SHARED_MAC_BRIDGE_DIR" ]; then
  echo "[OK] /mac 命令桥 skill 已安装（shared）：$SHARED_MAC_BRIDGE_DIR"
else
  echo "[WARN] 未发现 /mac 命令桥 skill：$MAC_BRIDGE_DIR 或 $SHARED_MAC_BRIDGE_DIR"
fi

for dir in "$MAC_DIR" "$MAC_DIR/agents" "$MAC_DIR/shared" "$MAC_DIR/tasks" "$MAC_DIR/logs" "$MAC_DIR/research"; do
  if [ -d "$dir" ]; then
    echo "[OK] 目录存在：$dir"
  else
    echo "[WARN] 缺少目录：$dir"
  fi
done

echo "[INFO] OpenClaw 原生命令参考：openclaw help / openclaw agent --help / openclaw sessions --help / openclaw agents --help"
echo "[INFO] 若要看到原生命令 /mac，请确认 skills/mac 已作为 user-invocable skill 安装。"
echo "[INFO] 推荐配置前提：tools.agentToAgent.enabled=true，并把允许通信的 agent id 写入 tools.agentToAgent.allow。"

echo "[TODO] 建议按以下顺序验收："
echo "       1. 握手测试:  $REPO_ROOT/scripts/test_agent_handshake.py"
echo "       2. 静默任务:  $REPO_ROOT/scripts/test_silent_task.py"
echo "       3. runtime smoke: $REPO_ROOT/scripts/test_runtime_orchestrator_smoke.py"
echo "       4. 恢复测试:  $REPO_ROOT/scripts/test_recovery_pipeline_smoke.py"
echo "       5. 原生demo:  $REPO_ROOT/scripts/runtime_sessions.py \"/mac 调研最近 30 天值得关注的 OpenClaw 多Agent 项目\""
echo "       6. 查看文档:  cat $REPO_ROOT/docs/测试脚本.md"
