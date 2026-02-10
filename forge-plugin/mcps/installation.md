# MCP Server Installation Guide

> *Preparing the conduits for first use*

## Prerequisites

| Requirement | For Servers | Check Command |
|-------------|-------------|---------------|
| Node.js 18+ | All npx-based servers (7 of 8) | `node --version` |
| npx (included with Node.js) | sequential-thinking, context7, magic, playwright, morphllm-fast-apply, tavily, chrome-devtools | `npx --version` |
| Python 3.9+ and uv | serena | `python3 --version && uv --version` |

## Configuration

The `.mcp.json` file at the repo root defines all server configurations. It is auto-discovered by Claude Code via `enableAllProjectMcpServers: true` in `.claude/settings.local.json`.

No manual server registration is needed - servers start on demand when their tools are invoked.

## API Key Setup

Three servers require API keys. Set them as environment variables before starting Claude Code.

### Required Keys

```bash
# Magic - UI component generation (https://21st.dev)
export TWENTYFIRST_API_KEY="your_key_here"

# Morphllm - Fast code application (https://morph.so)
export MORPH_API_KEY="your_key_here"

# Tavily - Web search (https://app.tavily.com - free tier available)
export TAVILY_API_KEY="tvly-your_key_here"
```

### Persistence

Add exports to your shell profile for persistence:

```bash
# Add to ~/.bashrc, ~/.zshrc, or equivalent
echo 'export TWENTYFIRST_API_KEY="your_key"' >> ~/.bashrc
echo 'export MORPH_API_KEY="your_key"' >> ~/.bashrc
echo 'export TAVILY_API_KEY="your_key"' >> ~/.bashrc
```

## Scope

- **Free servers** (no API key): sequential-thinking, context7, playwright, serena, chrome-devtools - fully functional out of the box
- **Paid servers**: magic and morphllm-fast-apply require paid API keys
- **Freemium**: tavily offers a free tier at https://app.tavily.com

The Forge works without any API keys. Paid servers enhance capabilities but are not required.

## Verification

After setting up, verify servers are available:

1. Start a Claude Code session in the forge repo
2. Check that `.mcp.json` is detected (servers appear in MCP status)
3. Test a free server: ask Claude to use sequential-thinking for a reasoning task

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Server not found | Check Node.js version: `node --version` (need 18+) |
| context7 timeout | Clear npm cache: `npm cache clean --force` |
| magic/morphllm errors | Expected without API keys - these are paid services |
| serena not starting | Install uv: `curl -LsSf https://astral.sh/uv/install.sh \| sh` |
| Server timeout | Restart Claude Code session |
| All servers fail | Check internet connection (servers download on first use) |

---

*Last Updated: 2026-02-10*
