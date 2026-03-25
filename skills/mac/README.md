# mac

这是 `/mac` 命令桥 skill。

## 定位

- 它不是完整方法论本体。
- 它只负责把输入显式切到 **Multi-Agent-Collaboration** 流程。
- 完整规则、边界、恢复、协议请看主 skill：`../Multi-Agent-Collaboration/`。

## 约定

- 安装后应作为 `user-invocable` skill 暴露为 slash command。
- 适合 TUI / GUI / Telegram 等支持技能命令暴露的界面。
- 如果当前平台不直接显示原生命令，纯文本 `/mac ...` 也应被主 skill 识别为强触发词。
