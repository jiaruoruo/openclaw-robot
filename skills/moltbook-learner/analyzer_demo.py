#!/usr/bin/env python3
"""
Moltbook 学习者 - 分析脚本 (Demo版)
"""

import json
import os
from datetime import datetime

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
POSTS_DIR = os.path.join(DATA_DIR, "posts")
ANALYZED_DIR = os.path.join(DATA_DIR, "analyzed")
LEARNED_DIR = os.path.join(DATA_DIR, "learned")

# 确保目录存在
os.makedirs(ANALYZED_DIR, exist_ok=True)
os.makedirs(LEARNED_DIR, exist_ok=True)

def load_latest_posts():
    files = sorted([f for f in os.listdir(POSTS_DIR) if f.endswith(".json")])
    if not files:
        print("No posts found!")
        return None
    
    latest = os.path.join(POSTS_DIR, files[-1])
    print(f"Loading: {latest}")
    with open(latest, encoding="utf-8") as f:
        return json.load(f)

def analyze_post(post):
    title = post.get("title", "")
    content = post.get("content", "")
    author = post.get("author", {}).get("name", "Unknown") if isinstance(post.get("author"), dict) else post.get("author", "Unknown")
    upvotes = post.get("upvotes", 0)
    
    # 评估价值
    novelty = 3
    if any(kw in content.lower() for kw in ["new", "first", "original", "innovate"]):
        novelty = 4
    
    feasibility = 3
    if any(kw in content.lower() for kw in ["code", "example", "step", "implement"]):
        feasibility = 4
    
    practicality = 3
    if upvotes > 100:
        practicality = 4
    if upvotes > 300:
        practicality = 5
    
    total_score = (novelty + feasibility + practicality) / 3
    
    # 分类
    category = "general"
    content_lower = content.lower()
    if "skill" in content_lower or "tool" in content_lower:
        category = "skill"
    elif "learn" in content_lower or "evolution" in content_lower:
        category = "learning"
    elif "security" in content_lower or "audit" in content_lower:
        category = "security"
    elif "practice" in content_lower or "guide" in content_lower or "tip" in content_lower:
        category = "tutorial"
    
    return {
        "title": title,
        "content": content[:500],
        "author": author,
        "upvotes": upvotes,
        "category": category,
        "scores": {
            "novelty": novelty,
            "feasibility": feasibility,
            "practicality": practicality,
            "total": round(total_score, 2)
        },
        "analyzed_at": datetime.now().isoformat()
    }

def extract_key_points(content):
    sentences = content.replace("!", ".").replace("?", ".").split(".")
    points = [s.strip() for s in sentences if len(s.strip()) > 20][:5]
    return points

def internalize(analyzed):
    learned = []
    for post in analyzed:
        if post["scores"]["total"] >= 3.5:
            entry = {
                "title": post["title"],
                "author": post["author"],
                "category": post["category"],
                "key_points": extract_key_points(post["content"]),
                "score": post["scores"]["total"],
                "learned_at": datetime.now().isoformat()
            }
            learned.append(entry)
    return learned

def save_learned(learned):
    if not learned:
        print("No high-value content to internalize")
        return
    
    filename = f"learned_{datetime.now().strftime('%Y%m%d')}.md"
    filepath = os.path.join(LEARNED_DIR, filename)
    
    md = f"# 🤖 Moltbook 每日学习\n\n"
    md += f"**日期**: {datetime.now().strftime('%Y-%m-%d')}\n\n"
    md += f"**学习条目**: {len(learned)}\n\n---\n\n"
    
    for i, item in enumerate(learned, 1):
        md += f"## {i}. {item['title']}\n\n"
        md += f"- **作者**: {item['author']}\n"
        md += f"- **分类**: {item['category']}\n"
        md += f"- **评分**: ⭐{item['score']}\n"
        md += f"- **要点**:\n"
        for point in item['key_points']:
            md += f"  - {point}\n"
        md += "\n---\n\n"
    
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(md)
    
    print(f"✓ Saved to: {filepath}")
    return filepath

def main():
    print("🧠 Moltbook Learner - Demo Analysis")
    print("=" * 40)
    
    data = load_latest_posts()
    if not data:
        return
    
    posts = data.get("posts", [])
    print(f"📥 Analyzing {len(posts)} posts...\n")
    
    analyzed = [analyze_post(p) for p in posts]
    analyzed.sort(key=lambda x: x["scores"]["total"], reverse=True)
    
    learned = internalize(analyzed)
    save_learned(learned)
    
    print(f"\n📊 Analysis Summary:")
    print(f"  - Total posts: {len(analyzed)}")
    print(f"  - High-value: {len(learned)}")
    
    print(f"\n🌟 Top Learnings:")
    for i, item in enumerate(learned[:3], 1):
        print(f"  {i}. {item['title'][:45]}... (⭐{item['score']})")
    
    print("\n✅ Demo complete!")

if __name__ == "__main__":
    main()
