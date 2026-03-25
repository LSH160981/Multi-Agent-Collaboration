# PROJECT_STRUCTURE

## 目标

把 Multi-Agent-Collaboration 整理成更接近大厂工程项目的结构：
- 入口清晰
- 分层清晰
- 文档归类清晰
- 研究资料与产品实现分开
- 示例、协议、Schema、脚本各司其职

## 当前推荐结构

```text
Multi-Agent-Collaboration/
├── README.md
├── docs/
│   ├── PROJECT_STRUCTURE.md        # 本文件：总览与分层
│   ├── CODE_REVIEW_NOTES.md        # 代码审计与重构记录
│   ├── README.md                   # docs 目录导航
│   ├── architecture/               # 架构、骨架、接管、流程、差距
│   ├── guides/                     # 安装、命令、演示、发布、使用说明
│   ├── testing/                    # 测试矩阵、smoke、验收说明
│   └── research/                   # 外部资料提炼与方法总结
├── skills/
│   ├── Multi-Agent-Collaboration/  # 主 skill
│   └── mac/                        # /mac 命令桥
├── scripts/                        # 安装、解析、编排、恢复、测试脚本
├── schemas/                        # JSON Schema
├── examples/                       # 示例输入输出、协议样例、测试模板
├── agents/                         # 常驻角色骨架
├── templates/                      # 动态角色模板
└── research/                       # 外部资料、抓取结果、本地研究副本
```

## 分层原则

### 1. 产品层
- `skills/`
- `agents/`
- `templates/`

### 2. 工程实现层
- `scripts/`
- `schemas/`
- `examples/`

### 3. 文档层
- `docs/architecture/`
- `docs/guides/`
- `docs/testing/`
- `docs/research/`

### 4. 研究层
- `research/`

## 清理规则

- 删除空占位目录与重复目录。
- 避免同时维护两套 skill 根目录。
- 外部资料先沉淀到 `research/`，再提炼到 `docs/research/`。
- 核心脚本必须写模块注释、函数注释、参数含义。
- 尽量减少“功能重叠但名字不同”的脚本；保留时要在 `scripts/README.md` 说明边界。
