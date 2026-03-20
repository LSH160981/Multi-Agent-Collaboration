# OpenCrew 学习笔记

来源：

- `research/github/opencrew/README.md`
- `research/github/opencrew/shared/A2A_PROTOCOL.md`

## 优点提取

1. **频道 = 岗位，线程 = 任务**
   - 这是非常强的组织抽象，天然适合消息平台。

2. **A2A 双通道留痕**
   - Agent 间真实触发靠 `sessions_send`
   - 对用户可见的轨迹靠频道/线程消息锚点
   - 这避免了“系统内部做了很多事，但用户什么都看不见”

3. **Closeout / Checkpoint 强制化**
   - 多 Agent 最怕中间状态杂乱和结果无验证
   - 结构化收尾让复盘成为可能

4. **Autonomy Ladder**
   - 把“什么能自己做，什么必须请示”写死，减少越权

5. **知识沉淀分层**
   - 原始对话
   - 结构化 closeout
   - 可复用知识

## 缺点/我们要改进的地方

1. 更偏平台频道组织，不够“OpenClaw 原生多会话”
2. 真实触发依赖平台线程/频道模型，跨平台一致性一般
3. 一些 A2A 稳定性依赖补丁和纪律约束

## 我们吸收后的改造方向

- 把“频道=岗位，线程=任务”提升为“**会话=Agent，任务=队列项，平台线程只是展示层**”
- 即使没有 Slack/Discord 线程，也能在 TUI / GUI / TG 中工作
- 保留双通道留痕思想：
  - 内部 JSON 通信记录
  - 外部用户可见汇总结论
