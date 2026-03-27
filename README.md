# Multi-Agent-Collaboration

**OpenClaw 原生多会话协作系统**

这个仓库的目标不是堆很多角色名，而是把下面这件事做扎实：

> 以 OpenClaw session 作为 Agent 运行单元，以主 Agent 作为唯一用户出口，把复杂任务拆解、并行、审核、恢复、去重收口，形成一个更像正规工程项目的多会话协作骨架。

---

## 一句话理解

- **Agent = OpenClaw session**
- **主 Agent = 唯一用户出口**
- **`/mac` = 强制进入多会话协作模式**
- **复杂任务 = 按需接管，不盲目拉团队**
- **研究资料 = 先 research，再审核吸收，不直接污染主实现**

---

## 现在的仓库结构

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
- `docs/architecture/OpenClaw原生多会话改造方案-20260327.md`

推荐配置样例：
- `examples/openclaw.agent-to-agent.sample.json5`

---

## 核心能力

- 主 Agent 统筹拆解、去重、最终拍板
- AgentPool 动态招聘/复用角色，并收紧边界
- A/B 双组竞争：稳健组 vs 激进组
- 审核 Agent 做质量审核与择优
- 检查 Agent 做巡检、恢复、重派、重建建议
- JSON A2A 通信协议
- 独立 memory / logs / queue / abilities 骨架
- OpenClaw 原生 session 调度原型
- 自学习 research 资料库

---

## 分层说明

### 1. `skills/`
真正给 OpenClaw 读取的 skill：
- `skills/multi-agent-collaboration/`
- `skills/mac/`

### 2. `scripts/`
正式入口与可复用实现：
- 安装与初始化
- 协议与任务解析
- runtime / session / 恢复
- staged pipeline

### 3. `tests/`
测试与回归：
- smoke 测试
- 恢复测试
- 样例校验

### 4. `docs/`
工程文档与方法说明。

### 5. `research/`
外部资料、网页抓取、参考仓库、本地研究沉淀。

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
- `scripts/README.md`
- `tests/README.md`

### 脚本分层提醒
- `scripts/` 根层：正式入口与核心运行链
- `scripts/bootstrap/`：骨架生成器与脚手架
- `scripts/analysis/`：评分、去重、自学习等分析脚本

### 学习资料
- `research/README.md`
- `docs/research/多agent协同研究总纲-20260327.md`

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

### 4. 运行核心测试
```bash
python3 tests/test_agent_handshake.py
python3 tests/test_silent_task.py
python3 tests/test_runtime_orchestrator_smoke.py
python3 tests/test_recovery_pipeline_smoke.py
```

---

## 这轮重构后的判断

现在仓库比之前更像一个正规的 skill 工程仓库：
- 主 skill 目录名规范化
- skill 入口、references、安装脚本引用统一
- `scripts/` 与 `tests/` 职责拆开
- 生成物与缓存不再污染主结构
- 正式入口矩阵更清楚

但也别自我感动，后面仍值得继续收敛：
- `docs/` 还能继续精简
- `research/` 还可以继续去重
- runtime 编排还可以进一步贴近 OpenClaw 原生 session tools

---

## 原则

1. 只有主 Agent 可以联系用户
2. 已有会话优先复用，再考虑扩张
3. 自学习先落 research，再审核吸收
4. 文档、脚本、协议、示例、测试分层维护
5. 不把 CLI 适配层误写成平台能力本身
