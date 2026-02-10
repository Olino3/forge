# context7

> *Official library documentation access*

## Configuration

```json
{
  "command": "npx",
  "args": ["-y", "@upstash/context7-mcp@latest"]
}
```

**Transport**: npx | **API Key**: None | **Runtime**: Node.js 18+

## Purpose

Provides access to official, up-to-date library documentation and patterns. Resolves library names to documentation sources and retrieves relevant content for specific APIs, functions, and patterns.

## Available Tools

- **resolve-library-id**: Find the Context7-compatible library ID for a package
- **get-library-docs**: Retrieve documentation for a specific library topic

## Forge Integration

**When to activate:**
- Import statements reference unfamiliar libraries
- Framework-specific patterns needed (React, Angular, FastAPI, etc.)
- Documentation lookup for specific API usage
- Version-specific behavior questions

**Recommended with Forge commands:**
- `/implement` - Get official patterns for implementation
- `/analyze` - Verify code against official documentation
- `/build` - Build tool documentation reference

## When Not to Use

- When you already know the API from training data
- For general programming concepts (not library-specific)
- For internal/proprietary libraries (not in Context7 database)

## Fallback

If unavailable, use WebSearch to find official documentation, or consult local `node_modules`/package source code with Read tool.

---

*Last Updated: 2026-02-10*
