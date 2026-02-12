# MCP Developer — Skill Memory Index

## Purpose

Stores project-specific memory for MCP server development, including architecture decisions, tool registries, resource schemas, and integration patterns discovered during implementation.

## Memory Files Per Project

Each project directory (e.g., `mcp-developer/{project-name}/`) may contain:

| File | Purpose |
|------|---------|
| `server_architecture.md` | Transport choice, server configuration, capability declarations, session management patterns |
| `tool_registry.md` | Registered tools with names, descriptions, input schemas, and implementation notes |
| `integration_patterns.md` | Client configurations, transport quirks, error handling patterns, and testing strategies |

## Usage

```
# Load project memory
memoryStore.getSkillMemory("mcp-developer", "{project-name}")

# Update after implementation
memoryStore.update("mcp-developer", "{project-name}", {
  file: "server_architecture.md",
  content: "..."
})

# Append new patterns discovered
memoryStore.append("mcp-developer", "{project-name}", {
  file: "integration_patterns.md",
  content: "..."
})
```

See [MemoryStore Interface](../../../interfaces/memory_store.md) for full method details.

## Evolution

- Memory entries are created on first MCP server implementation for a project
- Updated when architecture decisions change or new tools/resources are added
- Integration patterns accumulate as client-specific quirks are discovered
- Stale entries are pruned following [Memory Lifecycle](../../lifecycle.md) guidelines

## Related Documentation

- [MCP Developer SKILL.md](../../../skills/mcp-developer/SKILL.md)
- [MCP Developer examples.md](../../../skills/mcp-developer/examples.md)
- [MemoryStore Interface](../../../interfaces/memory_store.md)
- [Memory Lifecycle](../../lifecycle.md)
- [Memory Quality Guidance](../../quality_guidance.md)
