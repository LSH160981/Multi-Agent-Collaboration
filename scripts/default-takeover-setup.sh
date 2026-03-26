#!/usr/bin/env bash
set -euo pipefail

WORKSPACE="${1:-$HOME/.openclaw/workspace}"
REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SHARED_SKILLS_DIR="$HOME/.openclaw/skills"
TARGET_SKILL_DIR="$SHARED_SKILLS_DIR/Multi-Agent-Collaboration"
TARGET_MAC_BRIDGE_DIR="$SHARED_SKILLS_DIR/mac"

mkdir -p "$SHARED_SKILLS_DIR"
rm -rf "$TARGET_SKILL_DIR" "$TARGET_MAC_BRIDGE_DIR"
cp -R "$REPO_ROOT/skills/Multi-Agent-Collaboration" "$TARGET_SKILL_DIR"
cp -R "$REPO_ROOT/skills/mac" "$TARGET_MAC_BRIDGE_DIR"

"$REPO_ROOT/scripts/init-mac-system.sh" "$WORKSPACE" >/dev/null

cat <<EOF
已完成默认接管基础安装：
- 共享主 skill: $TARGET_SKILL_DIR
- /mac 命令桥: $TARGET_MAC_BRIDGE_DIR
- 工作目录: $WORKSPACE/mac-system

现在这套安装代表：
1. 所有本机 OpenClaw Agent 都能读到 Multi-Agent-Collaboration skill
2. /mac 已作为 user-invocable skill 暴露候选入口
3. mac-system 目录已初始化
4. 复杂任务现在可以默认按本 skill 的方法论处理
5. 即使平台没有显式注册 /mac，纯文本 '/mac ...' 也应被视为强触发词
6. 默认常驻核心角色应为：main-ceo / pool-hr / review-judge / inspect-patrol
7. specialist 不应预建过多，缺什么再复用或招聘

安装后请务必确认 OpenClaw 配置至少满足：
- tools.agentToAgent.enabled = true
- tools.agentToAgent.allow 包含当前需要互通的全部 agent id
- （建议）tools.sessions.visibility = all

推荐下一步顺序：
- 运行安装自检:
  $REPO_ROOT/scripts/install-selfcheck.sh "$WORKSPACE"
- 运行核心角色互认测试:
  $REPO_ROOT/scripts/test_agent_handshake.py
- 运行静默任务测试:
  $REPO_ROOT/scripts/test_silent_task.py
- 运行 runtime smoke:
  $REPO_ROOT/scripts/test_runtime_orchestrator_smoke.py
- 运行恢复链路测试:
  $REPO_ROOT/scripts/test_recovery_pipeline_smoke.py
- 需要人工观察时，多开 TUI 并切换 /agent 查看各角色 session
- 试发一条强触发任务:
  /mac 调研最近 30 天值得关注的 OpenClaw 多Agent 项目，并总结可吸收到本 skill 的优点
EOF
