---
name: voice-input
description: Voice input for OpenClaw using system microphone. Converts speech to text for voice interaction with the AI assistant.
---

# Voice Input Skill

## Overview

Enable voice interaction with the AI assistant by converting speech to text.

## Requirements

- Microphone access
- Speech recognition API or local STT model

## Usage

### Option 1: Web Speech API (Browser)
```javascript
// In browser console
const recognition = new webkitSpeechRecognition();
recognition.lang = 'zh-CN';
recognition.start();
```

### Option 2: Use OS Native
- **Windows**: Use Windows Speech Recognition (built-in)
- **macOS**: Use Siri / Dictation
- **Linux**: Use Whisper or Pocketsphinx

## Workflow

1. User speaks → STT converts to text
2. Text sent to AI assistant
3. AI responds → TTS converts to speech
4. Play audio response

## Notes
- Combine with `sherpa-onnx-tts` for local voice output
- For Chinese (中文), set lang to `zh-CN`
