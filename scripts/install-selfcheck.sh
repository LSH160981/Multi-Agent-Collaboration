#!/usr/bin/env bash
set -euo pipefail

WORKSPACE="${1:-$HOME/.openclaw/workspace}"
SKILL_DIR="$WORKSPACE/skills/multi-agent-collaboration"
MAC_BRIDGE_DIR="$WORKSPACE/skills/mac"
SHARED_SKILLS_DIR="$HOME/.openclaw/skills"
SHARED_SKILL_DIR="$SHARED_SKILLS_DIR/multi-agent-collaboration"
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
echo "[INFO] /mac 是否能明显显示，取决于当前入口是否支持 slash-like skill entry 展示；即使不显示，也应把纯文本 '/mac ...' 作为强触发词。"
echo "[INFO] 推荐配置前提：tools.agentToAgent.enabled=true，并把允许通信的 agent id 全部写入 tools.agentToAgent.allow。"
echo "[INFO] 建议同时开启 commands.nativeSkills=auto；在支持的平台上，这会让 /mac 更容易显示为技能命令。"
echo "[INFO] 建议默认核心角色：main-ceo / pool-hr / review-judge / inspect-patrol。"
echo "[INFO] specialist 应按需创建或复用，不建议安装后预建过多。"

echo "[TODO] 建议按以下顺序验收："
echo "       1. 安装自检:              $REPO_ROOT/scripts/install-selfcheck.sh"
echo "       2. 握手测试:              $REPO_ROOT/tests/test_agent_handshake.py"
echo "       3. 静默任务测试:          $REPO_ROOT/tests/test_silent_task.py"
echo "       4. runtime orchestrator: $REPO_ROOT/tests/test_runtime_orchestrator_smoke.py"
echo "       5. stage3 smoke:         $REPO_ROOT/tests/test_stage3_smoke.py"
echo "       6. 恢复链路测试:          $REPO_ROOT/tests/test_recovery_pipeline_smoke.py"
echo "       7. 原生 session demo:    $REPO_ROOT/scripts/runtime_sessions.py \"/mac 搜索 GitHub 最近 7 天 star 涨得最快的 10 个项目，总结特点\""
echo "       8. 查看命令文档:         cat $REPO_ROOT/docs/guides/openclaw-agent-session-commands.md"
echo "       9. 查看 skill 参考:       cat "$SHARED_SKILL_DIR/SKILL.md" && ls "$SHARED_SKILL_DIR/references""
