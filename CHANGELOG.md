# Changelog

## 1.0.0-alpha

- 增加 runtime 调度辅助库 `runtime_lib.py`
- 增加真实 OpenClaw CLI 派单脚本 `runtime_dispatch.py`
- 增加真实 runtime 总控脚本 `runtime_orchestrator.py`
- 增加巡检后恢复唤醒脚本 `inspect_and_recover.py`
- 增加 parse→recruit→dispatch→score→dedupe 的 demo pipeline
- 增加 runtime 调度说明文档
- 实际跑通 demo pipeline

## 0.9.0

- 增加动态招聘原型代码 `recruit_team.py`
- 增加结构化派单原型代码 `dispatch_task.py`
- 增加结果评分原型代码 `score_result.py`
- 增加巡检原型代码 `inspect_agents.py`
- 增加用户结论去重原型代码 `dedupe_summary.py`
- 增加总控原型代码 `orchestrate_task.py`
- 增加伪代码到代码映射说明
- 实际运行并验证新增代码输出

## 0.8.0

- 增加默认接管基础安装脚本
- 增加 `/mac` 文本解析脚本 `mac_cli.py`
- 增加核心示例 JSON 校验脚本
- 增加日志样例生成脚本
- 增加代码落地说明文档
- 实际运行并验证脚本输出
