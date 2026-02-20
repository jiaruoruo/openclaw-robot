#!/usr/bin/env python3
"""
Moltbook 学习者 - 爬取脚本
自动获取 Moltbook 上关于 AI bot 进化、学习、技能的帖子
"""

import requests
import json
import os
from datetime import datetime

# 配置
API_KEY = "moltbook_sk_mBZlubCuTFQcbh1M-XQH3NI8Fy23i_u5"
API_BASE = "https://www.moltbook.com/api/v1"
DATA_DIR = os.path.join(os.path.dirname(__file__), "data", "posts")

# 关键词列表
KEYWORDS = [
    "evolution", "learning", "upgrade", "improve", "growth",
    "skill", "capability", "new feature", "tool",
    "self-evolution", "self-improve", "autonomous",
    "tutorial", "how-to", "guide", "tip",
    "security", "audit", "vulnerability", "safe"
]

def fetch_feed(limit=50):
    """获取 Feed"""
    url = f"{API_BASE}/feed"
    headers = {"Authorization": f"Bearer {API_KEY}"}
    params = {"limit": limit}
    
    try:
        resp = requests.get(url, headers=headers, params=params, timeout=30)
        data = resp.json()
        return data.get("posts", [])
    except Exception as e:
        print(f"Error fetching feed: {e}")
        return []

def filter_posts(posts):
    """根据关键词过滤相关帖子"""
    filtered = []
    for post in posts:
        title = post.get("title", "").lower()
        content = post.get("content", "").lower()
        text = title + " " + content
        
        # 检查是否包含关键词
        for kw in KEYWORDS:
            if kw.lower() in text:
                filtered.append(post)
                break
    
    return filtered

def save_posts(posts, filename=None):
    """保存帖子到文件"""
    if not filename:
        filename = f"posts_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    
    filepath = os.path.join(DATA_DIR, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump({
            "fetched_at": datetime.now().isoformat(),
            "count": len(posts),
            "posts": posts
        }, f, ensure_ascii=False, indent=2)
    
    print(f"✓ Saved {len(posts)} posts to {filename}")
    return filepath

def main():
    print("🤖 Moltbook Learner - Starting fetch...")
    print(f"📡 Fetching latest posts...")
    
    # 获取 Feed
    posts = fetch_feed(50)
    print(f"📥 Got {len(posts)} posts")
    
    # 过滤相关帖子
    filtered = filter_posts(posts)
    print(f"🔍 Filtered to {len(filterd)} relevant posts")
    
    # 保存
    if filtered:
        save_posts(filtered)
        print("\n📋 Sample posts:")
        for i, p in enumerate(filtered[:3], 1):
            print(f"  {i}. {p.get('title', 'Untitled')[:50]}...")
    else:
        print("⚠️ No relevant posts found")
    
    print("\n✅ Fetch complete!")

if __name__ == "__main__":
    main()
