# Multi-Agent-Collaboration

**OpenClaw 原生多会话协作系统 / Skill 工程仓库**

这个仓库的目标不是堆很多角色名，而是把下面这件事做扎实：

> 以 OpenClaw session 作为 Agent 运行单元，以主 Agent 作为唯一用户出口，把复杂任务拆解、并行、审核、恢复、去重收口，形成一个更像正规工程项目的多会话协作骨架。

---

## 一句话理解

- **Agent = OpenClaw session**
- **主 Agent = 唯一用户出口**
- **`/mac` = 强制进入多会话协作模式**
- **复杂任务 = 按需接管，不盲目拉团队**
- **多会话不是越多越强，而是越清晰、越隔离、越可收口越强**

---

## 当前已经落地的核心能力

- 主 Agent 统筹拆解、去重、最终拍板
- AgentPool 动态招聘 / 复用角色，并收紧边界
- A/B 双组竞争：稳健组 vs 激进组
- 审核 Agent 做质量审核与择优
- 检查 Agent 做巡检、恢复、重派、重建建议
- JSON A2A 通信协议
- staged pipeline：stage1 → stage2 → stage3
- runtime orchestrator：真实 agent turn / session 风格调度闭环
- `rebuild` 执行器：可重建 agent 骨架，不再只是口头建议
- 伪代码 → 代码映射校验，避免文档和实现继续漂移

---

## 仓库结构

```text
Multi-Agent-Collaboration/
├── README.md
├── docs/
├── skills/
│   ├── multi-agent-collaboration/
│   └── mac/
├── scripts/
├── tests/
├── schemas/
├── examples/
├── agents/
├── templates/
└── research/
```

详细说明看：
- `docs/PROJECT_STRUCTURE.md`
- `docs/ENTRYPOINTS.md`
- `docs/CODE_REVIEW_NOTES.md`
- `docs/README.md`

推荐配置样例：
- `examples/openclaw.agent-to-agent.sample.json5`

---

## skill 层已经对齐到的新协作规则

主 skill `skills/multi-agent-collaboration/SKILL.md` 已经补齐并对齐了这些关键能力：

- **Team Shape Catalog**
  - `research-team`
  - `implementation-team`
  - `debug-team`
  - `compare-team`
  - `review-team`

- **Context Isolation Rules**
  - 默认最小上下文
  - verify / reviewer 尽量独立
  - 不广播完整历史给所有 worker

- **Model Routing Heuristics**
  - researcher / implementer / verifier / reviewer 走不同模型策略
  - 支持 cheap-first + strong-verification 思路

- **Recovery Rules**
  - retry / replace / challenger / reviewer escalation
  - 优先定点恢复，不全局重启

- **Finalization Protocol**
  - 去重
  - 冲突标注
  - 不确定性标注
  - 最终只保留一个对外结果

也就是说，这个仓库现在不只是“多开几个 agent”，而是已经有了更明确的**编排协议**。

---

## 最重要的入口

### 使用者先看
- `skills/multi-agent-collaboration/SKILL.md`
- `skills/mac/SKILL.md`
- `skills/multi-agent-collaboration/references/guides/安装与使用.md`
- `docs/guides/openclaw-agent-session-commands.md`

### 开发者先看
- `docs/PROJECT_STRUCTURE.md`
- `docs/ENTRYPOINTS.md`
- `docs/README.md`
- `scripts/README.md`
- `tests/README.md`

### architecture 阅读顺序
- `docs/architecture/项目骨架与逻辑执行流程.md`：总导航 / 总纲
- `docs/architecture/runtime调度说明.md`：正式入口、辅助脚本、demo 边界
- `docs/architecture/staged-runtime-pipeline.md`：staged pipeline 细节
- `docs/architecture/runtime_orchestrator_vs_pipeline_gap.md`：runtime 与 staged 的当前差异状态
- `docs/architecture/伪代码到代码映射.md`：哪些设计已经落地为脚本

---

## scripts 分层说明

### 正式入口
- `scripts/default-takeover-setup.sh`
- `scripts/install-selfcheck.sh`
- `scripts/init-mac-system.sh`
- `scripts/mac_cli.py`
- `scripts/run_staged_pipeline.py`
- `scripts/runtime_orchestrator.py`
- `scripts/inspect_and_recover.py`
- `scripts/session_probe.py`

### 辅助 / 子阶段脚本
- `scripts/protocol_lib.py`
- `scripts/runtime_lib.py`
- `scripts/runtime_dispatch.py`
- `scripts/recruit_team.py`
- `scripts/staffing_decision.py`
- `scripts/stage1_plan.py`
- `scripts/stage2_workers.py`
- `scripts/stage3_review_final.py`
- `scripts/repair_pipeline_state.py`
- `scripts/resume_pipeline.py`

### demo / 验收型脚本
- `scripts/runtime_sessions.py`

> `runtime_sessions.py` 当前定位是 **原生 session 风格 demo / 验收脚本**，不是长期生产调度主入口。

### 新增恢复执行器
- `scripts/rebuild_agent.py`

作用：
- 重建 `mac-system/agents/<agent>` 骨架
- 自动补齐：
  - `AGENTS.md`
  - `abilities.md`
  - `queue/`
  - `logs/`
  - `memory/`
  - `artifacts/`

这意味着：

> `rebuild` 现在已经不再只是建议动作，而是有明确执行器。

---

## tests 分层说明

### 核心 smoke / 回归
- `tests/test_agent_handshake.py`
- `tests/test_silent_task.py`
- `tests/test_runtime_orchestrator_smoke.py`
- `tests/test_stage3_smoke.py`
- `tests/test_recovery_pipeline_smoke.py`
- `tests/test_recovery_scenarios.py`
- `tests/test_full_acceptance.py`

### 轻量校验
- `tests/test_session_probe_example.py`
- `tests/test_inspect_and_recover_actions.py`
- `tests/test_rebuild_agent.py`
- `tests/test_pseudocode_mapping.py`

其中新增的两项很关键：

#### `test_rebuild_agent.py`
验证 `rebuild_agent.py` 能真正生成完整 agent 骨架。

#### `test_pseudocode_mapping.py`
自动检查 `docs/architecture/伪代码到代码映射.md` 中列出的脚本路径是否真实存在，防止文档继续漂移。

---

## 快速开始

### 1. 初始化系统目录
```bash
./scripts/init-mac-system.sh
```

### 2. 安装主 skill 与 `/mac` 命令桥
```bash
./scripts/default-takeover-setup.sh
```

### 3. 运行自检
```bash
./scripts/install-selfcheck.sh
```

### 4. 运行最小验收测试集
```bash
python3 tests/test_agent_handshake.py
python3 tests/test_silent_task.py
python3 tests/test_runtime_orchestrator_smoke.py
python3 tests/test_recovery_pipeline_smoke.py
```

### 5. 一键全链路验收
```bash
python3 tests/test_full_acceptance.py
```

如果当前机器还没准备好完整 agent/runtime 环境，可先跳过重阶段：

```bash
python3 tests/test_full_acceptance.py --skip-runtime --skip-stage3
```

---

## 当前工程判断

现在仓库比早期版本更像一个正规的 skill 工程仓库：

- 主 skill 与 `/mac` 入口规则已经对齐
- references 已同步到新的编排语义
- `scripts/` 与 `tests/` 职责明确分开
- 文档、实现、测试之间的映射更清楚
- `rebuild` 从概念变成真实能力
- runtime / staged / recovery / demo 的边界更清晰

但当前仍要保持清醒：

- runtime orchestrator 仍然部分依赖 CLI 适配层
- `runtime_sessions.py` 仍是 demo，不应误写成长期自治调度器
- `docs/architecture/` 仍有继续收敛空间
- 研究层与工程层还可以继续去重

---

## 原则

1. 只有主 Agent 可以联系用户
2. 已有会话优先复用，再考虑扩张
3. 自学习先落 research，再审核吸收
4. 文档、脚本、协议、示例、测试分层维护
5. 不把 CLI 适配层误写成平台能力本身
6. 不把 demo/验收脚本误写成正式主入口

---

## 相关导航

- 仓库结构：`docs/PROJECT_STRUCTURE.md`
- 正式入口矩阵：`docs/ENTRYPOINTS.md`
- scripts 边界：`scripts/README.md`
- docs 导航：`docs/README.md`
- 测试入口与说明：`tests/README.md`
