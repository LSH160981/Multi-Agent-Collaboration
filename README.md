# Multi-Agent-Collaboration

**OpenClaw 原生多会话协作系统**

不是“堆很多角色名”的文档仓库，而是：

- 以 **OpenClaw session** 作为 Agent 运行单元
- 以 **主Agent** 作为唯一用户出口
- 以 **AgentPool / 审核Agent / 检查Agent** 作为可按需启用的内部能力
- 以 **`/mac`** 作为显式强制入口
- 以 **复杂任务默认接管** 作为日常工作方式

---

## 你要的最终方向

这个 skill 的目标很明确：

> **安装后，普通复杂任务默认走它；用户也可以用 `/mac XXX` 显式进入多会话协作；整个系统最终变成 OpenClaw 原生多 session 的协作框架。**

也就是说：

1. **默认接管复杂任务**
2. **`/mac` 是显式命令入口**
3. **Agent = OpenClaw session**
4. **只有主Agent能和用户说话**
5. **其他 agent 只做内部协作，不得直连用户**

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

## 与别家方案的区别

### 不是本地 JSON 自嗨
本仓库已经开始接 OpenClaw 原生 runtime：
- `openclaw agent`
- `openclaw sessions`
- 文档层面对应 `sessions_spawn` / `sessions_send` / `sessions_history` / `sessions_list`

### 不是永久预建一堆空 agent
安装后默认只保留：
- 主Agent
- 审核Agent
- 检查Agent
- AgentPool

真正 specialist 在理解用户任务之后再按需生成或复用。

### 不是所有 agent 都能碰用户
主Agent 是**唯一**用户出口；其余 agent 一律禁止联系用户。

---

## 入口方式

### 方式 1：直接说复杂任务
安装后，复杂任务默认按本 skill 方法论处理。

### 方式 2：显式使用 `/mac`

```text
/mac 搜索 GitHub 最近 7 天 star 涨得最快的 10 个项目，总结共同特点
```

### 方式 3：点名 skill

```text
使用 Multi-Agent-Collaboration skill 完成 XXX 任务
```

---

## 仓库里最值得先看的文件

### 给使用者
- `skills/Multi-Agent-Collaboration/SKILL.md`
- `skills/mac/SKILL.md`
- `docs/openclaw-agent-session-commands.md`
- `docs/演示跑通手册.md`
- `docs/测试脚本.md`

### 给设计/开发者
- `docs/项目骨架与逻辑执行流程.md`
- `docs/多agent协同案例提炼.md`
- `docs/对照手稿的落地差距清单.md`
- `docs/runtime调度说明.md`
- `docs/runtime闭环现状.md`
- `docs/伪代码到代码映射.md`

### 给学习者
- `research/README.md`
- `research/web/*.md`
- `research/github/repos/*`

---

## 快速开始

### 1. 初始化系统目录

```bash
./scripts/init-mac-system.sh
```

### 2. 安装共享 skill 与 `/mac` 命令桥

```bash
./scripts/default-takeover-setup.sh
```

### 3. 运行自检

```bash
./scripts/install-selfcheck.sh
```

### 4. 看 OpenClaw session / 命令参考

```bash
cat docs/openclaw-agent-session-commands.md
```

### 5. 先跑握手测试

```bash
./scripts/test_agent_handshake.py
```

### 6. 再跑静默任务测试

```bash
./scripts/test_silent_task.py
```

### 7. 再跑恢复测试

```bash
./scripts/test_recovery_pipeline_smoke.py
```

---

## 默认运行策略

### 简单任务
主Agent 单会话完成，不强行拉团队。

### 复杂任务
主Agent 分析任务后决定：
- 单组
- 双组竞争
- 是否需要 reviewer
- 是否需要 inspect
- 是否需要按需招聘 specialist

### 已有团队时
优先：`sessions_send`

### 缺少角色时
再考虑：`sessions_spawn`

---

## `/mac` 命令目标

你提的目标是：
- TUI / GUI / TG 都要有 `/mac` 的效果
- 安装后让用户感觉自己就在和这个 skill 的主Agent 对话

本仓库当前实现方式是：

1. `skills/mac/SKILL.md` 暴露为 `user-invocable` skill，支持 slash command 场景
2. 即使平台侧没把 `/mac` 真注册出来，也要求把纯文本 `/mac xxx` 当成强触发词
3. `default-takeover-setup.sh` 把主 skill 与 `/mac` 命令桥一起安装到共享 skill 目录
4. 复杂任务默认由主 skill 接管

---

## 项目现状

现在它已经不是“概念手稿”，而是：

- 有 skill
- 有 `/mac` 命令桥
- 有 agent 骨架目录
- 有 research 资料库
- 有 JSON A2A 样例
- 有 runtime 调度原型
- 有 inspect / recover 原型
- 有自动化测试脚本
- 有中文伪代码 / 执行流程 / 差距清单

但也诚实地说：

> 真正的“长期自治公司化系统”还在持续推进中，重点仍然是把 `sessions_send` / `sessions_spawn` / `sessions_history` 串成更硬的原生闭环。

---

## 参考与致谢

这个项目明确参考、学习并吸收了下列来源中的优秀思路：

- OpenClaw 官方文档
- OpenMOSS
- OpenCrew
- ClawTeam-OpenClaw
- ClawHub 上的多 agent skill
- zelikk 的多 agent TUI 实战文章

但最终目标不是复制别人，而是：

> **把这些优点转译成 OpenClaw 原生多会话版的 Multi-Agent-Collaboration。**
