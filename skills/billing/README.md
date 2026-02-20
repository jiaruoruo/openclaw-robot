# 计费系统 (Billing System)

一个追踪 OpenClaw Token 消耗、生成报表、并在超出预算时提醒的系统。

## 功能

- ✅ 每日/每周/每月 Token 消耗追踪
- ✅ 支持多模型费用区分
- ✅ 预算提醒 (可配置阈值)
- ✅ 详细报表生成
- ✅ 历史数据存储

## 使用方法

### 1. 查询当前消耗
```bash
python billing.py status
```

### 2. 查看今日消耗
```bash
python billing.py today
```

### 3. 查看本周消耗
```bash
python billing.py week
```

### 4. 查看本月消耗
```bash
python billing.py month
```

### 5. 查看所有历史
```bash
python billing.py history
```

### 6. 设置预算提醒
```bash
python billing.py budget 50  # 设置每月预算 $50
```

### 7. 生成详细报表
```bash
python billing.py report
```

## 配置

在 `config.json` 中配置:
- `budget`: 月度预算 (美元)
- `alert_threshold`: 提醒阈值 (百分比，如 80 表示 80% 时提醒)
- `currency`: 货币符号

## 数据存储

消耗数据存储在 `data/usage.json` 中。
