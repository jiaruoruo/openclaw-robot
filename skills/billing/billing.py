#!/usr/bin/env python3
"""
OpenClaw 计费系统 - Token 消耗追踪与报表
"""

import json
import os
import subprocess
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional

# 配置路径
SCRIPT_DIR = Path(__file__).parent
DATA_DIR = SCRIPT_DIR / "data"
CONFIG_FILE = SCRIPT_DIR / "config.json"
USAGE_FILE = DATA_DIR / "usage.json"

# 默认配置
DEFAULT_CONFIG = {
    "budget": 100.0,
    "alert_threshold": 80,
    "currency": "$",
    "models": {
        "MiniMax-M2.5": {"input": 15, "output": 60, "unit": "per 1M tokens"},
        "MiniMax-M2.1": {"input": 15, "output": 60, "unit": "per 1M tokens"},
        "MiniMax-VL-01": {"input": 15, "output": 60, "unit": "per 1M tokens"},
        "MiniMax-Portal": {"input": 0, "output": 0, "unit": "free"},
        "Qwen-Portal": {"input": 0, "output": 0, "unit": "free"}
    }
}

def ensure_data_dir():
    """确保数据目录存在"""
    DATA_DIR.mkdir(exist_ok=True)
    if not USAGE_FILE.exists():
        with open(USAGE_FILE, 'w', encoding='utf-8') as f:
            json.dump({"records": [], "daily": {}}, f, indent=2)

def load_config() -> Dict:
    """加载配置"""
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
            return {**DEFAULT_CONFIG, **json.load(f)}
    return DEFAULT_CONFIG.copy()

def save_config(config: Dict):
    """保存配置"""
    with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2, ensure_ascii=False)

def load_usage() -> Dict:
    """加载使用数据"""
    ensure_data_dir()
    with open(USAGE_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_usage(data: Dict):
    """保存使用数据"""
    ensure_data_dir()
    with open(USAGE_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def get_gateway_usage() -> Dict:
    """从 Gateway 获取使用数据"""
    try:
        # 使用完整路径
        openclaw_path = r"C:\Users\贾若\AppData\Roaming\npm\openclaw.ps1"
        result = subprocess.run(
            ['powershell', '-ExecutionPolicy', 'Bypass', '-File', openclaw_path, 'gateway', 'usage-cost'],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        output = result.stdout + result.stderr
        print(output)
        
        # 解析输出
        data = {
            "total_cost": 0.0,
            "total_tokens": 0,
            "latest_day": None,
            "latest_cost": 0.0,
            "latest_tokens": 0,
            "last_updated": datetime.now().isoformat()
        }
        
        # 解析输出 - 支持中英文混合输出 (· 或 路)
        import re
        total_match = re.search(r'Total:\s*\$?([\d.]+)\s*[·路]\s*([\d.]+)([kmKM]?)\s*tokens', output)
        if total_match:
            data["total_cost"] = float(total_match.group(1))
            tokens_val = float(total_match.group(2))
            tokens_unit = total_match.group(3).lower() if total_match.group(3) else ''
            if tokens_unit == 'k':
                data["total_tokens"] = int(tokens_val * 1000)
            elif tokens_unit == 'm':
                data["total_tokens"] = int(tokens_val * 1000000)
            else:
                data["total_tokens"] = int(tokens_val)
        
        # 解析 "Latest day: XXXX-XX-XX · $X.XXXX · X.Xk tokens" (支持中英文)
        latest_match = re.search(r'Latest day:\s*(\d{4}-\d{2}-\d{2})\s*[·路]\s*\$?([\d.]+)\s*[·路]\s*([\d.]+)([kmKM]?)\s*tokens', output)
        if latest_match:
            data["latest_day"] = latest_match.group(1)
            data["latest_cost"] = float(latest_match.group(2))
            tokens_val = float(latest_match.group(3))
            tokens_unit = latest_match.group(4).lower() if latest_match.group(4) else ''
            if tokens_unit == 'k':
                data["latest_tokens"] = int(tokens_val * 1000)
            elif tokens_unit == 'm':
                data["latest_tokens"] = int(tokens_val * 1000000)
            else:
                data["latest_tokens"] = int(tokens_val)
        
        return data
        
    except Exception as e:
        print(f"获取数据失败: {e}")
        return {"error": str(e)}

def refresh_usage():
    """刷新使用数据"""
    print("🔄 正在获取 Gateway 使用数据...")
    data = get_gateway_usage()
    
    if "error" in data:
        print(f"❌ 获取失败: {data['error']}")
        return False
    
    # 保存到历史记录
    usage_data = load_usage()
    
    # 更新最新数据
    usage_data["latest"] = data
    
    # 添加到历史记录
    if data.get("latest_day"):
        day = data["latest_day"]
        if "daily" not in usage_data:
            usage_data["daily"] = {}
        usage_data["daily"][day] = {
            "cost": data["latest_cost"],
            "tokens": data["latest_tokens"]
        }
    
    save_usage(usage_data)
    print(f"✅ 数据已更新: {data['latest_day']}")
    return True

def format_tokens(count: int) -> str:
    """格式化 Token 数量"""
    if count >= 1000000:
        return f"{count/1000000:.1f}M"
    elif count >= 1000:
        return f"{count/1000:.1f}K"
    return str(count)

def cmd_status():
    """显示当前状态"""
    config = load_config()
    usage_data = load_usage()
    
    print("\n" + "="*50)
    print("📊 OpenClaw 计费系统状态")
    print("="*50)
    
    # 预算信息
    budget = config.get("budget", 100)
    currency = config.get("currency", "$")
    
    if "latest" in usage_data:
        latest = usage_data["latest"]
        total_cost = latest.get("total_cost", 0)
        usage_pct = (total_cost / budget * 100) if budget > 0 else 0
        
        print(f"\n💰 预算设置: {currency}{budget}/月")
        print(f"💵 已使用: {currency}{total_cost:.2f}")
        print(f"📈 使用率: {usage_pct:.1f}%")
        
        # 进度条
        bar_length = 30
        filled = int(bar_length * min(usage_pct / 100, 1))
        bar = "█" * filled + "░" * (bar_length - filled)
        print(f"   [{bar}]")
        
        # 警告
        threshold = config.get("alert_threshold", 80)
        if usage_pct >= threshold:
            print(f"\n⚠️  警告: 已使用 {usage_pct:.1f}%，超过 {threshold}% 阈值!")
        elif usage_pct >= threshold * 0.8:
            print(f"\n💡 提示: 已使用 {usage_pct:.1f}%，注意预算使用")
    
    print("\n📅 Token 消耗:")
    if "latest" in usage_data:
        latest = usage_data["latest"]
        print(f"   累计: {format_tokens(latest.get('total_tokens', 0))} tokens")
        if latest.get("latest_day"):
            print(f"   今日: {format_tokens(latest.get('latest_tokens', 0))} tokens ({latest['latest_day']})")
    
    print("\n" + "="*50)

def cmd_today():
    """今日消耗"""
    usage_data = load_usage()
    
    print("\n📅 今日消耗")
    print("-"*30)
    
    if "latest" in usage_data:
        latest = usage_data["latest"]
        cost = latest.get("latest_cost", 0)
        tokens = latest.get("latest_tokens", 0)
        day = latest.get("latest_day", "未知")
        
        print(f"日期: {day}")
        print(f"费用: ${cost:.4f}")
        print(f"Token: {format_tokens(tokens)}")
    else:
        print("暂无数据，请先运行 'python billing.py refresh'")
    
    print()

def cmd_week():
    """本周消耗"""
    usage_data = load_usage()
    
    print("\n📅 本周消耗 (最近7天)")
    print("-"*30)
    
    daily = usage_data.get("daily", {})
    if not daily:
        print("暂无数据")
        return
    
    # 排序并获取最近7天
    sorted_days = sorted(daily.keys(), reverse=True)[:7]
    
    total_cost = 0
    total_tokens = 0
    
    for day in sorted_days:
        day_data = daily[day]
        cost = day_data.get("cost", 0)
        tokens = day_data.get("tokens", 0)
        total_cost += cost
        total_tokens += tokens
        print(f"{day}: ${cost:.4f} ({format_tokens(tokens)} tokens)")
    
    print("-"*30)
    print(f"本周合计: ${total_cost:.4f} ({format_tokens(total_tokens)} tokens)")
    print()

def cmd_month():
    """本月消耗"""
    usage_data = load_usage()
    
    print("\n📅 本月消耗")
    print("-"*30)
    
    daily = usage_data.get("daily", {})
    if not daily:
        print("暂无数据")
        return
    
    # 获取当月数据
    current_month = datetime.now().strftime("%Y-%m")
    month_data = {k: v for k, v in daily.items() if k.startswith(current_month)}
    
    if not month_data:
        print("本月暂无数据")
        return
    
    total_cost = sum(d.get("cost", 0) for d in month_data.values())
    total_tokens = sum(d.get("tokens", 0) for d in month_data.values())
    
    print(f"当前月份: {current_month}")
    print(f"活跃天数: {len(month_data)}")
    print(f"总费用: ${total_cost:.4f}")
    print(f"总Token: {format_tokens(total_tokens)}")
    
    # 对比预算
    config = load_config()
    budget = config.get("budget", 100)
    if budget > 0:
        pct = total_cost / budget * 100
        print(f"预算使用率: {pct:.1f}%")
    
    print()

def cmd_history():
    """历史记录"""
    usage_data = load_usage()
    
    print("\n📜 历史消耗记录")
    print("-"*40)
    
    daily = usage_data.get("daily", {})
    if not daily:
        print("暂无历史数据")
        return
    
    # 按日期排序
    sorted_days = sorted(daily.keys(), reverse=True)
    
    total_cost = 0
    total_tokens = 0
    
    for day in sorted_days[:30]:  # 最近30天
        day_data = daily[day]
        cost = day_data.get("cost", 0)
        tokens = day_data.get("tokens", 0)
        total_cost += cost
        total_tokens += tokens
        print(f"{day}: ${cost:.4f} ({format_tokens(tokens)} tokens)")
    
    print("-"*40)
    print(f"总计 (最近30天): ${total_cost:.4f} ({format_tokens(total_tokens)} tokens)")
    print()

def cmd_budget(amount: Optional[float] = None):
    """设置预算"""
    config = load_config()
    
    if amount is None:
        current = config.get("budget", 100)
        print(f"\n💰 当前月度预算: ${current}")
        return
    
    config["budget"] = float(amount)
    save_config(config)
    print(f"\n✅ 已设置月度预算: ${amount}")

def cmd_report():
    """生成详细报表"""
    config = load_config()
    usage_data = load_usage()
    
    print("\n" + "="*60)
    print("📊 OpenClaw 详细消耗报表")
    print("="*60)
    
    # 1. 概览
    print("\n【概览】")
    budget = config.get("budget", 100)
    currency = config.get("currency", "$")
    
    if "latest" in usage_data:
        latest = usage_data["latest"]
        total_cost = latest.get("total_cost", 0)
        total_tokens = latest.get("total_tokens", 0)
        
        print(f"  累计总费用: {currency}{total_cost:.2f}")
        print(f"  累计总Token: {format_tokens(total_tokens)}")
        print(f"  月度预算: {currency}{budget}")
        print(f"  使用率: {(total_cost/budget*100):.1f}%" if budget > 0 else "  未设置预算")
    
    # 2. 模型价格
    print("\n【模型价格参考】")
    models = config.get("models", {})
    for name, info in models.items():
        if info.get("input", 0) > 0:
            print(f"  {name}: ${info['input']}/M in, ${info['output']}/M out")
        else:
            print(f"  {name}: 免费")
    
    # 3. 最近30天
    print("\n【最近30天每日消耗】")
    daily = usage_data.get("daily", {})
    if daily:
        sorted_days = sorted(daily.keys(), reverse=True)[:30]
        for day in sorted_days:
            day_data = daily[day]
            cost = day_data.get("cost", 0)
            tokens = day_data.get("tokens", 0)
            print(f"  {day}: {currency}{cost:.4f} ({format_tokens(tokens)})")
    
    # 4. 统计
    print("\n【统计】")
    if daily:
        costs = [d.get("cost", 0) for d in daily.values()]
        tokens_list = [d.get("tokens", 0) for d in daily.values()]
        
        print(f"  平均日费用: ${sum(costs)/len(costs):.4f}")
        print(f"  最高日费用: ${max(costs):.4f}")
        print(f"  最低日费用: ${min(costs):.4f}")
        print(f"  平均日Token: {format_tokens(int(sum(tokens_list)/len(tokens_list)))}")
    
    print("\n" + "="*60)

def cmd_refresh():
    """刷新数据"""
    refresh_usage()

def main():
    """主入口"""
    if len(sys.argv) < 2:
        cmd_status()
        return
    
    command = sys.argv[1].lower()
    
    if command == "status":
        cmd_status()
    elif command == "today":
        cmd_today()
    elif command == "week":
        cmd_week()
    elif command == "month":
        cmd_month()
    elif command == "history":
        cmd_history()
    elif command == "budget":
        budget = float(sys.argv[2]) if len(sys.argv) > 2 else None
        cmd_budget(budget)
    elif command == "report":
        cmd_report()
    elif command == "refresh":
        cmd_refresh()
    elif command == "help":
        print("""
📖 OpenClaw 计费系统使用指南

用法: python billing.py <命令>

命令:
  status           显示当前状态 (默认)
  today            今日消耗
  week             本周消耗
  month            本月消耗
  history          历史记录
  budget [金额]    设置月度预算 (如: budget 50)
  report           生成详细报表
  refresh          刷新 Gateway 数据
  help             显示帮助

示例:
  python billing.py status
  python billing.py budget 50
  python billing.py report
""")
    else:
        print(f"未知命令: {command}")
        print("运行 'python billing.py help' 查看帮助")

if __name__ == "__main__":
    main()
