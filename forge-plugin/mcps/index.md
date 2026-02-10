# MCP Server Integration

> *External knowledge conduits extending the Forge's reach*

## Server Catalog

| Server | Transport | API Key | Purpose |
|--------|-----------|---------|---------|
| [sequential-thinking](servers/sequential-thinking.md) | npx | No | Step-by-step reasoning for complex problems |
| [context7](servers/context7.md) | npx | No | Library documentation access |
| [magic](servers/magic.md) | npx | Yes (`TWENTYFIRST_API_KEY`) | UI component generation |
| [playwright](servers/playwright.md) | npx | No | Browser automation and testing |
| [serena](servers/serena.md) | uvx | No | Code intelligence and navigation |
| [morphllm-fast-apply](servers/morphllm-fast-apply.md) | npx | Yes (`MORPH_API_KEY`) | Fast code application/editing |
| [tavily](servers/tavily.md) | npx | Yes (`TAVILY_API_KEY`) | Web search and research |
| [chrome-devtools](servers/chrome-devtools.md) | npx | No | Chrome DevTools Protocol access |

**Free servers (no API key):** sequential-thinking, context7, playwright, serena, chrome-devtools
**Paid servers (API key required):** magic, morphllm-fast-apply, tavily (free tier available)

## Task-to-Server Quick Reference

| Task Type | Primary Server | Secondary |
|-----------|---------------|-----------|
| Complex debugging / architecture analysis | sequential-thinking | serena |
| Library docs / framework patterns | context7 | - |
| UI component development | magic | context7 |
| Browser / E2E testing | playwright | chrome-devtools |
| Large codebase navigation | serena | sequential-thinking |
| Multi-file refactoring | morphllm-fast-apply | serena |
| Web research / current info | tavily | - |
| Performance profiling / debugging | chrome-devtools | playwright |

## Forge Skill Integration

| Forge Skill/Command | Recommended MCP Servers |
|---------------------|------------------------|
| `/analyze` | sequential-thinking, serena, context7 |
| `/implement` | context7, magic (for UI), serena |
| `/improve` | morphllm-fast-apply, serena, sequential-thinking |
| `/test` | playwright (E2E), sequential-thinking |
| `/brainstorm` | sequential-thinking, tavily |
| `skill:python-code-review` | sequential-thinking, context7 |
| `skill:angular-code-review` | context7, sequential-thinking |
| `skill:generate-jest-unit-tests` | playwright (E2E), context7 |

## Configuration

MCP servers are configured in `/.mcp.json` at the repo root. Auto-discovered via `enableAllProjectMcpServers: true` in `.claude/settings.local.json`.

## Related Documentation

- [Activation Protocol](activation_protocol.md) - When to activate each server
- [Installation Guide](installation.md) - Prerequisites and setup
- [Context Loading Protocol](../context/loading_protocol.md) - How context is loaded

---

*Last Updated: 2026-02-10*
