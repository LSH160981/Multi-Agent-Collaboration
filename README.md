# Multi-Agent-Collaboration

**OpenClaw 原生多会话协作系统**

这个仓库的目标不是堆很多角色名，而是把下面这件事做扎实：

> 以 OpenClaw session 作为 Agent 运行单元，以主Agent 作为唯一用户出口，把复杂任务拆解、并行、审核、恢复、去重收口，最终形成一个更接近企业级多会话协作系统的工程骨架。

---

## 一句话理解

- **Agent = OpenClaw session**
- **主Agent = 唯一用户出口**
- **`/mac` = 强制进入多会话协作模式**
- **复杂任务 = 默认接管**
- **研究资料 = 先 research，再审核吸收，不直接污染主实现**

---

## 当前项目结构

```text
Multi-Agent-Collaboration/
├── README.md
├── docs/
├── skills/
├── scripts/
├── schemas/
├── examples/
├── agents/
├── templates/
└── research/
```

详细说明看：
- `docs/PROJECT_STRUCTURE.md`
- `docs/CODE_REVIEW_NOTES.md`
- `docs/ENTRYPOINTS.md`
- `docs/README.md`

---

## 核心能力

- 主Agent 统筹拆解、去重、最终拍板
- AgentPool 动态招聘/复用角色，并写死边界
- A/B 双组竞争：稳健组 vs 激进组
- 审核Agent 三维审核：Reviewer / Judge / Metrics
- 检查Agent 巡检、催办、恢复、重派、重建
- JSON A2A 通信协议
- 独立 memory / logs / queue / abilities 目录骨架
- 握手测试、静默任务测试、恢复测试
- OpenClaw 原生 session 调度原型
- 自学习 research 资料库
- git 留痕与中文 commit

---

## 项目分层

### 1. skills/
真正给 OpenClaw 读取的 skill：
- `skills/Multi-Agent-Collaboration/`
- `skills/mac/`

### 2. scripts/
工程实现与测试脚本：
- 安装与初始化
- 协议与任务解析
- runtime / session / 恢复
- smoke / 回归 / 测试

### 3. docs/
工程文档，而不是所有东西都堆在 README。

### 4. research/
外部资料、网页抓取、GitHub 参考、副本、自动学习材料。

---

## 最重要的入口

### 使用者先看
- `skills/Multi-Agent-Collaboration/SKILL.md`
- `skills/mac/SKILL.md`
- `skills/Multi-Agent-Collaboration/安装与使用.md`
- `docs/guides/openclaw-agent-session-commands.md`

### 开发者先看
- `docs/PROJECT_STRUCTURE.md`
- `docs/CODE_REVIEW_NOTES.md`
- `docs/architecture/项目骨架与逻辑执行流程.md`
- `scripts/README.md`

### 学习者先看
- `research/README.md`
- `docs/research/多agent协同外部资料提炼-20260326.md`
- `docs/research/多agent协同优秀作品骨架与伪代码提炼-20260326.md`
- `research/web/*.md`
- `research/external/*`

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

### 4. 查看 OpenClaw session / 命令参考
```bash
cat docs/openclaw-agent-session-commands.md
```

### 5. 运行验收测试
```bash
./scripts/test_agent_handshake.py
./scripts/test_silent_task.py
./scripts/test_runtime_orchestrator_smoke.py
./scripts/test_recovery_pipeline_smoke.py
```

---

## 当前工程判断

这个仓库现在已经不是概念手稿，而是：
- 有 skill
- 有 `/mac` 命令桥
- 有 agent 骨架目录
- 有研究资料库
- 有 JSON A2A 样例
- 有 runtime 调度原型
- 有 inspect / recover 原型
- 有自动化测试脚本
- 有中文伪代码 / 执行流程 / 差距清单

但也要诚实：

> 它现在仍然处于“企业级骨架持续收敛期”，最重要的工作不是继续加角色，而是继续清理结构、统一协议、强化原生 session 闭环、减少重复实现。

---

## 原则

1. 只有主Agent 可以联系用户
2. 已有会话优先复用，再考虑扩张
3. 自学习先落 research，再审核吸收
4. 文档、脚本、协议、示例要分层维护
5. 不把 CLI 适配层误写成平台能力本身

---

## 致谢

本项目明确学习并吸收了以下来源的优点：
- OpenClaw 官方文档
- OpenMOSS
- OpenCrew
- ClawTeam-OpenClaw
- ClawHub 多 agent skill
- zelikk 的多 agent TUI 实战文章

目标不是复制，而是把优点转译成 **OpenClaw 原生多会话版 Multi-Agent-Collaboration**。
