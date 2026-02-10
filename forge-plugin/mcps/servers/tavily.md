# tavily

> *Web search and real-time information retrieval*

## Configuration

```json
{
  "command": "npx",
  "args": ["-y", "tavily-mcp@latest"],
  "env": {
    "TAVILY_API_KEY": "${TAVILY_API_KEY}"
  }
}
```

**Transport**: npx | **API Key**: `TAVILY_API_KEY` (required, free tier available) | **Runtime**: Node.js 18+

## Purpose

Provides intelligent web search and research capabilities. Performs comprehensive searches with ranking, filtering, and content extraction for research tasks.

## Available Tools

- **tavily_search**: Web search with relevance ranking
- **tavily_extract**: Extract full-text content from URLs

## API Key Setup

```bash
# Get free key from https://app.tavily.com
export TAVILY_API_KEY="tvly-your_key_here"
```

## Forge Integration

**When to activate:**
- Research tasks requiring current information
- "Latest" or "current" version lookups
- Fact-checking and verification
- Technology comparison research
- Finding solutions to obscure errors

**Recommended with Forge commands:**
- `/brainstorm` - Research phase of requirements discovery
- `/analyze` - Lookup best practices for detected patterns
- `/implement` - Find current API documentation

**Pairs well with:** sequential-thinking (structured research), context7 (library-specific docs)

## When Not to Use

- Information within Claude's training data
- Library-specific documentation (use context7 instead)
- Internal/proprietary information (not on the web)

## Fallback

If unavailable, use the built-in WebSearch tool for web research. It provides similar search capabilities.

---

*Last Updated: 2026-02-10*
