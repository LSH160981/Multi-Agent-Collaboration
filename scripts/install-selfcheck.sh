#!/usr/bin/env bash
set -euo pipefail

WORKSPACE="${1:-$HOME/.openclaw/workspace}"
SKILL_DIR="$WORKSPACE/skills/Multi-Agent-Collaboration"
MAC_BRIDGE_DIR="$WORKSPACE/skills/mac"
SHARED_SKILLS_DIR="$HOME/.openclaw/skills"
SHARED_SKILL_DIR="$SHARED_SKILLS_DIR/Multi-Agent-Collaboration"
SHARED_MAC_BRIDGE_DIR="$SHARED_SKILLS_DIR/mac"
MAC_DIR="$WORKSPACE/mac-system"
REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"

printf '%s\n' '== Multi-Agent-Collaboration 自检 =='

if [ -d "$SKILL_DIR" ]; then
  echo "[OK] 主 skill 已安装（workspace）：$SKILL_DIR"
elif [ -d "$SHARED_SKILL_DIR" ]; then
  echo "[OK] 主 skill 已安装（shared）：$SHARED_SKILL_DIR"
else
  echo "[WARN] 未发现主 skill：$SKILL_DIR 或 $SHARED_SKILL_DIR"
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

echo "[INFO] OpenClaw 命令参考：openclaw help / openclaw status / openclaw agent --help / openclaw agents --help / openclaw sessions --help / openclaw tui --help"
echo "[INFO] /mac 是否能明显显示，取决于当前入口是否支持 user-invocable skill 展示；即使不显示，也应把纯文本 '/mac ...' 作为强触发词。"
echo "[INFO] 推荐配置前提：tools.agentToAgent.enabled=true，并把允许通信的 agent id 全部写入 tools.agentToAgent.allow。"
echo "[INFO] 建议默认核心角色：main-ceo / pool-hr / review-judge / inspect-patrol。"
echo "[INFO] specialist 应按需创建或复用，不建议安装后预建过多。"

echo "[TODO] 建议按以下顺序验收："
echo "       1. 安装自检:              $REPO_ROOT/scripts/install-selfcheck.sh"
echo "       2. 握手测试:              $REPO_ROOT/scripts/test_agent_handshake.py"
echo "       3. 静默任务测试:          $REPO_ROOT/scripts/test_silent_task.py"
echo "       4. runtime orchestrator: $REPO_ROOT/scripts/test_runtime_orchestrator_smoke.py"
echo "       5. 恢复链路测试:          $REPO_ROOT/scripts/test_recovery_pipeline_smoke.py"
echo "       6. 原生 session demo:    $REPO_ROOT/scripts/runtime_sessions.py \"/mac 搜索 GitHub 最近 7 天 star 涨得最快的 10 个项目，总结特点\""
echo "       7. 查看命令文档:         cat $REPO_ROOT/docs/guides/openclaw-agent-session-commands.md"
