# 多 Agent 协同学习资料索引

本目录用于沉淀：
- 网页提取文本
- GitHub 仓库结构与架构观察
- ClawHub skill 方法论
- 可复用的伪代码、运行流程、通信协议、恢复策略

## 目录约定

- `sources/raw/pages/`：网页原文抓取
- `sources/raw/github/`：拉下来的 GitHub 仓库
- `sources/extracted/`：提炼后的重点内容
- `sources/notes/`：按主题整理的观察笔记

## 当前重点主题

1. OpenClaw 原生 session 编排
2. 多 agent 角色分层
3. A/B 双组竞争 + reviewer 裁决
4. inspect / patrol / recover 闭环
5. JSON 任务包与 agent-to-agent 通信
6. 主Agent 唯一用户出口与去重治理
7. 自学习 / 自改进 / git 记忆压缩策略

## 已纳入的参考来源

- OpenClaw docs: Pi 集成架构
- ClawHub: Agent Team Orchestration
- ClawHub: Agent Directory
- OpenCrew
- OpenMOSS
- ClawTeam-OpenClaw
- zelikk 两篇博客

> 原始资料不等于最终方案。
> 这里的目标是：提取“能落地的优点”，再改造成 OpenClaw 原生多会话版本。
