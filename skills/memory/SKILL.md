---
name: memory
description: Manage agent memory files. Use for reading, writing, and updating memory files in the workspace memory/ directory.
---

# Memory Management Skill

## File Structure

```
memory/
├── MEMORY.md              # Long-term curated memory
├── 2026-02-19.md         # Daily logs (create new each day)
└── heartbeat-state.json   # State tracking (last checks, etc.)
```

## When to Update Memory

### Daily (write to memory/YYYY-MM-DD.md)
- Conversations and tasks
- Technical discoveries
-临时 notes

### Important (update MEMORY.md)
- Identity/personality changes
- New skills or capabilities
- Key preferences about user
- Long-term decisions

## Usage

### Read Memory
Use `read` tool to read memory files.

### Write Memory
Use `write` tool with `path` parameter.

### Search Memory
Use `memory_search` tool for semantic search across all memory files.

## Best Practices
- Write immediately after significant events
- Don't rely on "mental notes"
- Update MEMORY.md periodically (during heartbeats)
- Include timestamps in daily logs
