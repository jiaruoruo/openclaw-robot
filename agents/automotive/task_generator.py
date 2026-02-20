#!/usr/bin/env python3
"""
汽车电子多智能体任务系统 - 使用 OpenClaw sessions_spawn
"""

import json
import os

# 任务定义
TASKS = {
    "BCM": {
        "name": "BCM 车身控制模块",
        "features": ["车门控制", "灯光控制", "雨刮控制", "喇叭控制", "防盗报警"],
        "workflow": [
            {"step": 1, "agent": "req-analyst", "task": "需求分析", "inputs": {"type": "BCM"}},
            {"step": 2, "agent": "safety-engineer", "task": "HARA分析", "deps": [1]},
            {"step": 3, "agent": "tech-architect", "task": "架构设计", "deps": [1]},
            {"step": 4, "agent": "asw-engineer", "task": "应用层开发", "deps": [2, 3]},
            {"step": 5, "agent": "bsw-engineer", "task": "底层开发", "deps": [3]},
            {"step": 6, "agent": "unit-test", "task": "单元测试", "deps": [4, 5]},
            {"step": 7, "agent": "integration-test", "task": "集成测试", "deps": [6]},
        ]
    }
}

# Agent 提示词模板
AGENT_PROMPTS = {
    "req-analyst": """你是一个专业的汽车电子需求工程师。
    
请为以下功能编写软件需求规范:
{features}

输出格式要求:
1. 功能列表 (带优先级 P0/P1/P2)
2. 输入输出定义
3. 性能要求
4. 安全要求 (如适用)

请直接输出 Markdown 格式的需求文档。""",

    "safety-engineer": """你是一个资深的汽车功能安全工程师。

请对以下功能进行 HARA 分析:
{features}

请输出:
1. 危害列表
2. ASIL 评级
3. 安全目标
4. 安全需求

参考 ISO 26262 标准。""",

    "tech-architect": """你是一个资深的汽车电子技术架构师。

请设计以下功能的 AUTOSAR 架构:
{features}

请输出:
1. SWC 组件设计
2. 接口定义
3. 通信矩阵 (CAN/LIN)
4. 架构决策记录 (ADR)""",

    "asw-engineer": """你是一个资深的汽车嵌入式应用软件工程师。

请实现以下功能的应用层代码:
{features}

要求:
1. 符合 AUTOSAR SWC 标准
2. 遵循 MISRA C 规范
3. 包含状态机实现
4. 输出 C 源代码""",

    "bsw-engineer": """你是一个资深的汽车电子底层软件工程师。

请实现底层软件:
{features}

要求:
1. AUTOSAR BSW 层
2. MCAL 驱动接口
3. 通信堆栈 (CanIf)
4. 输出 C 源代码""",

    "unit-test": """你是一个资深的嵌入式测试工程师。

请为以下功能编写单元测试:
{features}

要求:
1. 使用 Google Test/Unity 框架
2. 覆盖率达到 MC/DC > 90%
3. 输出测试代码和报告""",

    "integration-test": """你是一个资深的集成测试工程师。

请设计集成测试:
{features}

要求:
1. 接口测试
2. 故障注入测试
3. HIL 测试场景
4. 输出测试用例和报告"""
}

def generate_task_prompt(agent_type, features):
    """生成任务提示"""
    features_str = "\n".join([f"- {f}" for f in features])
    template = AGENT_PROMPTS.get(agent_type, "请完成以下任务: {features}")
    return template.format(features=features_str)

def create_subagent_task(project_type="BCM"):
    """创建子任务"""
    project = TASKS.get(project_type, TASKS["BCM"])
    features = project["features"]
    workflow = project["workflow"]
    
    tasks = []
    for step in workflow:
        task = {
            "step": step["step"],
            "agent": step["agent"],
            "task": step["task"],
            "prompt": generate_task_prompt(step["agent"], features)
        }
        tasks.append(task)
    
    return {
        "project": project["name"],
        "features": features,
        "tasks": tasks
    }

# CLI 接口
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        project_type = sys.argv[1]
    else:
        project_type = "BCM"
    
    result = create_subagent_task(project_type)
    
    print(json.dumps(result, ensure_ascii=False, indent=2))
