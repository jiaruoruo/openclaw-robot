---
name: voice-chat
description: Full voice conversation with AI assistant. Combines speech-to-text input and text-to-speech output for natural voice interaction.
---

# Voice Chat Skill

## Overview

Enable full duplex voice conversation with the AI assistant.

## Components

1. **Voice Input** → Speech-to-Text (STT)
2. **AI Processing** → LLM understands and responds
3. **Voice Output** → Text-to-Speech (TTS)

## Setup

### STT Options
| Service | Notes |
|---------|-------|
| Web Speech API | Free, browser-based, supports zh-CN |
| Whisper API | OpenAI, accurate, requires API key |
| sherpa-onnx | Local offline STT |

### TTS Options
| Service | Notes |
|---------|-------|
| sherpa-onnx-tts | Local offline, no internet |
| OpenAI TTS | High quality, requires API key |
| Browser Speech API | Free, basic quality |

## Quick Start

1. **Enable Voice Input**: Use browser's Speech Recognition
2. **Response via TTS**: Use `tts` tool with `asVoice: true`

## Example Workflow

```
User: [speaks Chinese]
    ↓ (Web Speech API)
"今天天气怎么样"
    ↓ (AI Processing)
"今天上海晴天，20度"
    ↓ (TTS)
[plays audio response]
```

## Configuration

For Chinese voice interaction:
- STT lang: `zh-CN`
- TTS voice: Select Chinese voice
- Keywords for activation: "小D" or custom wake word

## Notes
- Use `asVoice: true` in message to get voice responses
- Check `TOOLS.md` for preferred TTS voice settings
