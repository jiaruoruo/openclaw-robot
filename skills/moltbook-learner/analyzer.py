#!/usr/bin/env python3
"""
Moltbook 学习者 - 分析脚本
分析帖子内容，提取关键知识，评估价值
"""

import json
import os
from datetime import datetime

# 配置
DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
POSTS_DIR = os.path.join(DATA_DIR, "posts")
ANALYZED_DIR = os.path.join(DATA_DIR, "analyzed")
LEARNED_DIR = os.path.join(DATA_DIR, "learned")

def load_latest_posts():
    """加载最新的帖子文件"""
    files = sorted([f for f in os.listdir(POSTS_DIR) if f.endswith(".json")])
    if not files:
        return None
    
    latest = os.path.join(POSTS_DIR, files[-1])
    with open(latest, encoding="utf-8") as f:
        return json.load(f)

def analyze_post(post):
    """分析单个帖子"""
    title = post.get("title", "")
    content = post.get("content", "")
    author = post.get("author", {}).get("name", "Unknown")
    upvotes = post.get("upvotes", 0)
    
    # 提取关键词
    keywords = []
    tech_keywords = ["API", "skill", "tool", "function", "method", "system"]
    for kw in tech_keywords:
        if kw.lower() in content.lower():
            keywords.append(kw)
    
    # 评估价值
    novelty = 3  # 基础分
    if "new" in content.lower() or "first" in content.lower():
        novelty = 4
    if "original" in content.lower() or "innovate" in content.lower():
        novelty = 5
    
    feasibility = 3  # 基础分
    if "code" in content.lower() or "example" in content.lower():
        feasibility = 4
    if "implement" in content.lower() or "step" in content.lower():
        feasibility = 5
    
    practicality = 3  # 基础分
    if upvotes > 100:
        practicality = 4
    if upvotes > 1000:
        practicality = 5
    
    # 总分
    total_score = (novelty + feasibility + practicality) / 3
    
    # 分类
    category = "general"
    if "skill" in content.lower() or "tool" in content.lower():
        category = "skill"
    elif "learning" in content.lower() or "evolution" in content.lower():
        category = "learning"
    elif "security" in content.lower() or "audit" in content.lower():
        category = "security"
    elif "tutorial" in content.lower() or "guide" in content.lower():
        category = "tutorial"
    
    return {
        "title": title,
        "content": content[:500],  # 保留前500字符
        "author": author,
        "upvotes": upvotes,
        "category": category,
        "keywords": keywords,
        "scores": {
            "novelty": novelty,
            "feasibility": feasibility,
            "practicality": practicality,
            "total": round(total_score, 2)
        },
        "analyzed_at": datetime.now().isoformat()
    }

def internalize(analyzed):
    """将分析结果内化为可执行的知识"""
    learned = []
    
    for post in analyzed:
        if post["scores"]["total"] >= 4.0:  # 高价值内容
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

def extract_key_points(content):
    """提取关键要点"""
    # 简单提取：以句号分隔的句子
    sentences = content.split("。")
    points = [s.strip() for s in sentences if len(s.strip()) > 20][:5]
    return points

def save_analysis(analyzed):
    """保存分析结果"""
    filename = f"analyzed_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    filepath = os.path.join(ANALYZED_DIR, filename)
    
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(analyzed, f, ensure_ascii=False, indent=2)
    
    print(f"✓ Saved analysis to {filename}")
    return filepath

def save_learned(learned):
    """保存已内化的知识"""
    if not learned:
        print("⚠️ No high-value content to internalize")
        return
    
    filename = f"learned_{datetime.now().strftime('%Y%m%d')}.md"
    filepath = os.path.join(LEARNED_DIR, filename)
    
    # 转换为 Markdown
    md = f"# 🤖 Moltbook 每日学习\n\n"
    md += f"**日期**: {datetime.now().strftime('%Y-%m-%d')}\n\n"
    md += f"**学习条目**: {len(learned)}\n\n"
    md += "---\n\n"
    
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
    
    print(f"✓ Saved learned knowledge to {filename}")
    return filepath

def main():
    print("🧠 Moltbook Learner - Starting analysis...")
    
    # 加载帖子
    data = load_latest_posts()
    if not data:
        print("⚠️ No posts found. Run fetcher.py first!")
        return
    
    posts = data.get("posts", [])
    print(f"📥 Analyzing {len(posts)} posts...")
    
    # 分析
    analyzed = [analyze_post(p) for p in posts]
    analyzed.sort(key=lambda x: x["scores"]["total"], reverse=True)
    
    # 保存分析
    save_analysis(analyzed)
    
    # 内化
    learned = internalize(analyzed)
    save_learned(learned)
    
    # 打印摘要
    print(f"\n📊 Analysis Summary:")
    print(f"  - Total posts: {len(analyzed)}")
    print(f"  - High-value (⭐4+): {len(learned)}")
    
    if learned:
        print(f"\n🌟 Top learnings:")
        for i, item in enumerate(learned[:3], 1):
            print(f"  {i}. {item['title'][:50]}... (⭐{item['score']})")
    
    print("\n✅ Analysis complete!")

if __name__ == "__main__":
    main()
