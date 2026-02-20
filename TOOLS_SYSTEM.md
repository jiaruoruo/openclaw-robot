# 工具系统 (Tool System)

小D 的工具箱，包含技能(Skills)和功能(Tools)的完整系统。

---

## 📁 工具分类

### 🎯 核心工具 (Core Tools)

| 工具 | 功能 | 状态 |
|------|------|------|
| **exec** | 执行命令 | ✅ 正常 (需要 pty:true) |
| **read** | 读取文件 | ✅ 正常 |
| **write** | 写入文件 | ✅ 正常 |
| **edit** | 编辑文件 | ✅ 正常 |
| **browser** | 浏览器控制 | ⚠️ 不稳定 |
| **message** | 发送消息 | ✅ 正常 |
| **tts** | 语音合成 | ❌ 需配置 |
| **cron** | 定时任务 | ✅ 正常 |

---

### 🧠 技能 (Skills) - 27个

```
workspace/skills/
├── moltbook/          # 社交平台
├── memory/           # 记忆管理
├── weather/          # 天气查询
├── github/           # GitHub
├── notion/           # Notion
├── summarize/        # 摘要
├── spotify-player/  # Spotify
├── slack/            # Slack
├── discord/          # Discord
├── obsidian/         # Obsidian
├── coding-agent/     # 编程
├── tmux/             # 终端
├── openai-image-gen/ # AI绘图
├── blogwatcher/      # 博客监控
├── apple-notes/      # Apple笔记
├── apple-reminders/ # Apple提醒
├── bear-notes/       # Bear笔记
├── things-mac/       # Things
├── trello/          # Trello
├── gog/             # 游戏
├── goplaces/        # 地点
├── food-order/      # 外卖
├── voice-call/      # 通话
├── nano-pdf/        # PDF
├── video-frames/    # 视频
├── sherpa-onnx-tts/ # 本地TTS
├── voice-input/      # 语音输入
└── voice-chat/      # 语音对话
```

---

## 🔧 常用命令

### 文件操作
```bash
# 读取文件
read(path: "C:\Users\贾若\.openclaw\workspace\MEMORY.md")

# 写入文件
write(content: "内容", path: "C:\Users\贾若\.openclaw\workspace\test.md")

# 编辑文件
edit(file_path: "xxx", oldText: "旧内容", newText: "新内容")
```

### 执行命令 (PowerShell)
```bash
exec(command: "powershell -Command \"Get-Date\"", pty: true, timeout: 30)
```

### 浏览器
```bash
# 打开网页
browser(action: "navigate", profile: "openclaw", targetUrl: "https://example.com")

# 截图
browser(action: "screenshot", profile: "openclaw", targetId: "xxx")
```

### 定时任务
```bash
cron(action: "add", job: {
  name: "my-task",
  schedule: { kind: "every", everyMs: 3600000 },
  payload: { kind: "systemEvent", text: "提醒内容" },
  sessionTarget: "main"
})
```

---

## ⚡ 快速使用模板

### 发帖到 Moltbook
```bash
# 1. 检查状态
exec(command: "powershell -Command \"Invoke-RestMethod -Uri 'https://www.moltbook.com/api/v1/agents/status' -Headers @{'Authorization'='Bearer moltbook_sk_xxx'}\"", pty: true)

# 2. 发帖
exec(command: "powershell -Command \"Invoke-RestMethod -Uri 'https://www.moltbook.com/api/v1/posts' -Method Post -Headers @{'Authorization'='Bearer moltbook_sk_xxx'; 'Content-Type'='application/json'} -Body (ConvertTo-Json @{title='标题'; submolt_name='general'})\"", pty: true)
```

### 查天气
```bash
exec(command: "curl -s \"wttr.in/Shanghai?format=3\"", pty: true)
```

### 查日历
```bash
cron(action: "list")
```

---

## 🔐 敏感信息

| 服务 | 位置 | 说明 |
|------|------|------|
| Moltbook API | TOOLS.md | moltbook_sk_xxx |
| Proxy | openclaw.json | 127.0.0.1:7897 |
| Gateway Port | openclaw.json | 18789 |

---

## 🐛 已知问题

1. **TTS** - 文件生成但为空 (0字节)，需配置 TTS 服务
2. **Browser** - 有时不稳定，CDP 超时
3. **Exec** - 需要 `pty: true` 参数才能正常输出

---

## 📝 待配置

- [ ] TTS 服务 (OpenAI API 或 sherpa-onnx)
- [ ] 语音输入 (Web Speech API 或本地 STT)
- [ ] Brave Search API (web_search)

---

## 🎓 学习体系

详见 `LEARNING.md`

| 类别 | 说明 |
|------|------|
| 短期记忆 | memory/YYYY-MM-DD.md |
| 长期记忆 | MEMORY.md |
| 技能记忆 | skills/*/SKILL.md |

---

*最后更新: 2026-02-19*
