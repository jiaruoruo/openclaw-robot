---
name: billing
description: OpenClaw 计费系统 - Token 消耗追踪、预算提醒与详细报表
---

# 计费系统 (Billing System)

追踪 OpenClaw Token 消耗、生成报表、并在超出预算时提醒。

## 快速开始

```bash
# 进入计费目录
cd C:\Users\贾若\.openclaw\workspace\skills\billing

# 查看当前状态
python billing.py status

# 刷新数据
python billing.py refresh

# 设置月度预算
python billing.py budget 50
```

## 命令列表

| 命令 | 说明 |
|------|------|
| `status` | 显示当前状态 (默认) |
| `today` | 今日消耗 |
| `week` | 本周消耗 (最近7天) |
| `month` | 本月消耗 |
| `history` | 历史记录 (最近30天) |
| `budget [金额]` | 设置月度预算 |
| `report` | 生成详细报表 |
| `refresh` | 刷新 Gateway 数据 |
| `help` | 显示帮助 |

## 功能说明

### 1. Token 消耗追踪
- 每日/每周/每月消耗统计
- 历史数据存储 (最多30天)
- Token 数量格式化 (K/M)

### 2. 多模型费用区分
系统内置模型价格参考:
- MiniMax-M2.5: $15/M 输入, $60/M 输出
- MiniMax-M2.1: $15/M 输入, $60/M 输出
- MiniMax-Portal: 免费
- Qwen-Portal: 免费

### 3. 预算提醒
设置月度预算后，系统会:
- 计算使用百分比
- 在超过阈值时发出警告
- 默认阈值: 80%

### 4. 详细报表
生成包含以下内容的报表:
- 概览 (总费用、Token、预算使用率)
- 模型价格参考
- 每日消耗明细
- 统计分析 (平均/最高/最低)

## 配置

配置文件: `config.json`

```json
{
    "budget": 100.0,
    "alert_threshold": 80,
    "currency": "$",
    "models": {
        "MiniMax-M2.5": {"input": 15, "output": 60, "unit": "per 1M tokens"},
        "MiniMax-Portal": {"input": 0, "output": 0, "unit": "free"}
    }
}
```

## 数据存储

- 使用数据: `data/usage.json`
- 配置文件: `config.json`

## 集成到 Heartbeat

可以将计费检查添加到 HEARTBEAT.md:

```markdown
## 预算检查 (每周)
- [ ] 运行 python billing.py status 检查预算使用
- [ ] 如果使用率 > 80%，记录提醒
```

## 示例输出

```
==================================================
📊 OpenClaw 计费系统状态
==================================================

💰 预算设置: $100/月
💵 已使用: $20.83
📈 使用率: 20.8%
   [██████░░░░░░░░░░░░░░░░░░░░░░░]

📅 Token 消耗:
   累计: 74.7M tokens
   今日: 10.4K tokens (2026-02-20)

==================================================
```
