# 🏎️ 汽车电子嵌入式开发 Agent 团队配置

## 概述

本目录包含用于汽车电子嵌入式软件开发的多个专业 Agent 配置。

## Agent 列表

| Agent ID | 名称 | 角色 | 主要职责 |
|----------|------|------|----------|
| `arch-chief` | 小A | 首席架构师 | 项目管理、架构设计、代码整合 |
| `req-analyst` | 小R | 需求分析师 | 需求收集、文档编写 |
| `safety-engineer` | 小S | 安全工程师 | HARA分析、安全需求 |
| `tech-architect` | 小T | 技术架构师 | AUTOSAR设计、技术选型 |
| `asw-engineer` | 小App | 应用软件工程师 | SWC开发 |
| `bsw-engineer` | 小B | 底层软件工程师 | BSW开发 |
| `driver-engineer` | 小D | 驱动工程师 | 外设驱动开发 |
| `unit-test-engineer` | 小U | 单元测试工程师 | 单元测试 |
| `integration-test-engineer` | 小I | 集成测试工程师 | 集成测试 |
| `devops` | 小Dev | DevOps工程师 | CI/CD |

## 快速开始

### 1. 初始化项目

```bash
# 创建项目目录
mkdir automotive_project
cd automotive_project

# 初始化 Agent 团队
python ../agents/automotive/create_agents.py
```

### 2. 启动开发流程

```bash
# 运行 BCM 项目
python ../agents/automotive/workflow.py
```

### 3. 创建自定义项目

```python
from workflow import ProjectCoordinator

coordinator = ProjectCoordinator("My_Project")
workflow = coordinator.start_project("功能列表")
board = coordinator.run()
```

## 工作流

```
用户需求
    │
    ▼
需求分析 → 安全分析 → 架构设计
    │           │           │
    ▼           ▼           ▼
         应用层开发 ←→ 底层开发 ←→ 驱动开发
              │           │           │
              └───────────┼───────────┘
                          ▼
                    单元测试 ←→ 集成测试
                          │
                          ▼
                      代码整合
```

## 任务状态

| 状态 | 描述 |
|------|------|
| pending | 待处理 |
| in_progress | 进行中 |
| blocked | 阻塞 |
| completed | 已完成 |
| rejected | 已拒绝 |

## 输出文档

- `requirements/` - 需求文档
- `architecture/` - 架构设计
- `safety/` - 安全文档
- `src/` - 源代码
- `tests/` - 测试代码
- `deployment/` - 部署配置

## 技术栈

- **架构**: AUTOSAR CP/AP
- **语言**: C, Python
- **安全**: ISO 26262
- **流程**: ASPICE
- **芯片**: ARM Cortex-M, Infineon TriCore, NXP S32K

---

*版本: 1.0 | 2026-02-20*
