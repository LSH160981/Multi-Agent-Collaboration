# 多agent协同案例提炼

这份文件把外部优秀作品里**真正有价值、能落地的部分**提取出来，避免只堆链接。

---

## 1. OpenClaw 官方文档

### 关键结论
- OpenClaw 本身就有 session、skill、slash command、tool、gateway、agent、sessions 等完整能力。
- `user-invocable` skill 可以暴露成 slash command。
- `openclaw agent` / `openclaw sessions` 在 CLI 上真实可用。

### 对本 skill 的启发
- `/mac` 可以做成真实命令桥。
- 原生多会话系统要站在 OpenClaw 现有能力上，而不是自己造假 runtime。

---

## 2. ClawHub - Agent Team Orchestration

### 关键结论
- 最小有用团队是 orchestrator + builder + reviewer。
- 任务必须有生命周期与 handoff 结构。
- 没有 review，质量会漂移。

### 可吸收优点
- 最小团队优先
- 任务状态机
- 交接包标准化
- orchestrator 不越权执行

---

## 3. OpenCrew

### 关键结论
- shared 协议、角色边界、DoD、checkpoint、closeout 非常重要。
- 组织纪律要写成规则，而不是靠模型“自己悟”。

### 可吸收优点
- 把 A2A 协议写死
- 把谁能派单给谁写死
- 把 checkpoint / closeout 模板固化

---

## 4. ClawTeam-OpenClaw

### 关键结论
- 团队管理、mailbox、watcher、workspace git 管理，是一套更工程化的结构。
- 恢复不是一句话，而是：状态 + 监听 + 任务台账 + 消息轨迹。

### 可吸收优点
- mailbox 思路
- watcher / patrol 思路
- team config / manager 思路
- git 留痕与工作目录管理

---

## 5. OpenMOSS

### 关键结论
- 规划 / 执行 / 审查 / 巡查 四角闭环非常适合多 agent 系统。
- 任务 / 子任务 / review / rule / score 的拆分方式很有参考价值。

### 可吸收优点
- 规划层与执行层分离
- reviewer / scorecard / patrol 形成管理闭环
- 系统适合接 OpenClaw session 版 runtime

---

## 6. zelikk 的两篇 TUI 实战

### 关键结论
- context 污染是多任务中的真实痛点
- 多 agent TUI 观察很适合调试
- 先测通信再跑复杂任务是必须动作
- label / session / deliverables / model timeout 都是常见坑

### 可吸收优点
- 握手测试必须保留
- 静默任务测试必须保留
- 文档里必须诚实写坑

---

## 7. 最终提炼成我们的规则

### 规则 1：Agent = OpenClaw session
不是概念，不是文档角色，而是能被 session 工具真实调度的会话。

### 规则 2：主Agent唯一用户出口
这是整个系统的最高纪律。

### 规则 3：已有会话优先复用
优先 `sessions_send`，再考虑 `sessions_spawn`。

### 规则 4：最小团队优先
不要没必要就上 A/B 双组。

### 规则 5：审核 / 巡检必须是真角色
不能只有设计图，没有运行单元。

### 规则 6：先测试通信，再开复杂任务
握手测试、静默任务测试、恢复测试是安装后的基本验收。

### 规则 7：自学习必须先 research，后审核，再吸收
不能直接让自动化脚本野蛮修改主 skill。
必须遵守：抓取外部资料 → 落 `research/` → 审核Agent 给出 should_absorb / code_first / doc_first → 主Agent 决定改 skill/docs/scripts → git 提交。

---

## 8. 我们自己的推荐实现路线

### P1
- 强化 `/mac` 命令桥
- 完成默认接管说明
- 跑通原生 session demo
- 跑通三类测试

### P2
- 补强 `sessions_send` / `sessions_history` 闭环
- 补更多状态机与恢复动作
- 统一 handoff / score / queue schema

### P3
- 自学习任务自动化
- git 日志压缩与记忆摘要化
- 更完整的平台接管方案
