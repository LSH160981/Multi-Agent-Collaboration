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
- 共享 skill: $TARGET_SKILL_DIR
- /mac 命令桥: $TARGET_MAC_BRIDGE_DIR
- 工作目录: $WORKSPACE/mac-system

这代表：
1. 所有本机 OpenClaw Agent 都能读到 Multi-Agent-Collaboration skill
2. /mac 已作为 user-invocable skill 暴露候选入口
3. mac-system 目录已初始化
4. 复杂任务现在可以默认按本 skill 的方法论处理
5. 即使平台没有显式注册 /mac，纯文本 '/mac ...' 也应被视为强触发词

建议下一步：
- 运行: $REPO_ROOT/scripts/install-selfcheck.sh "$WORKSPACE"
- 先跑握手测试: $REPO_ROOT/scripts/test_agent_handshake.py
- 再跑静默任务: $REPO_ROOT/scripts/test_silent_task.py
- 再跑恢复测试: $REPO_ROOT/scripts/test_recovery_pipeline_smoke.py
- 新开一个 OpenClaw session
- 发送: /mac 调研最近 30 天值得关注的 OpenClaw 多Agent 项目
EOF
