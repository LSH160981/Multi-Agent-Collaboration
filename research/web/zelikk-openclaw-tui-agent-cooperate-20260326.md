# zelikk：OpenClaw 命令行 TUI 中多 Agent 协同完成任务（2026-03-26 抓取）

来源：`https://zelikk.blogspot.com/2026/03/openclaw-tui-agent-cooperate.html`
抓取方式：web_fetch
说明：外部网页文本，作为学习资料落地保存。

---

## 核心结论

这篇文章最有价值的不是成功案例，而是暴露了真实问题：

- agent-to-agent 通信很容易出错
- `sessions_send` 的使用必须强调
- session 混乱会直接拖垮协作
- 先做通信测试，再做复杂任务
- 交付物路径、session 绑定、角色约束都必须写死

## 对我们 skill 的启发

1. 安装后必须先做握手测试与互发测试
2. 非主Agent 的交付物路径、能力边界、消息协议要写死
3. 不要把复杂任务建立在“通信可能能用”的侥幸上
4. `/new` 这类可能扰乱 session 的行为，在协作场景里要谨慎

## 推荐加入本 skill 的流程纪律

```text
先看 agent/sessions 状态
-> 再做 agent 间互发测试
-> 再让 leader 派真实任务
-> 通信不过，不进入复杂任务
```
