# magic

> *Modern UI component generation from 21st.dev patterns*

## Configuration

```json
{
  "command": "npx",
  "args": ["@21st-dev/magic"],
  "env": {
    "TWENTYFIRST_API_KEY": "${TWENTYFIRST_API_KEY}"
  }
}
```

**Transport**: npx | **API Key**: `TWENTYFIRST_API_KEY` (required) | **Runtime**: Node.js 18+

## Purpose

Generates modern, accessible UI components using patterns from 21st.dev. Produces production-ready component code following current design system best practices.

## Available Tools

- **21st_magic_component**: Generate UI components from natural language descriptions

## API Key Setup

```bash
# Get key from https://21st.dev
export TWENTYFIRST_API_KEY="your_key_here"
```

## Forge Integration

**When to activate:**
- UI component creation requests
- Frontend layout and design tasks
- Responsive component development
- Design system component generation

**Recommended with Forge commands:**
- `/implement` - When building UI features
- `/improve` - When modernizing UI components

**Pairs well with:** context7 (framework docs), playwright (visual testing)

## When Not to Use

- Backend-only development
- Non-UI tasks (API design, database work)
- When custom components aren't needed (simple HTML suffices)

## Fallback

If unavailable (no API key), generate components manually using framework-specific patterns and the Forge's Angular/frontend context files.

---

*Last Updated: 2026-02-10*
