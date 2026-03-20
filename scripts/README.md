# scripts

- `default-takeover-setup.sh`：把 skill 安装到共享目录并初始化默认接管基础环境
- `install-selfcheck.sh`：安装后自检
- `generate-agent.sh`：快速生成一个新的 Agent 目录骨架
- `generate-ab-team.sh`：批量生成 A/B 两组 specialist 骨架
- `init-mac-system.sh`：初始化 `mac-system/` 多 Agent 工作目录
- `mac_cli.py`：把 `/mac` 文本解析成结构化任务包
- `recruit_team.py`：根据任务包生成 A/B 组编组方案
- `dispatch_task.py`：把结构化派单写入日志与队列
- `score_result.py`：把结果包转成评分卡
- `inspect_agents.py`：巡检 Agent 目录的日志与队列状态
- `dedupe_summary.py`：对候选结论做去重汇总
- `orchestrate_task.py`：串起 `/mac` 解析与 A/B 编组的总控原型
- `validate_examples.py`：校验核心 JSON 示例
- `generate-log-samples.py`：生成额外日志样例
