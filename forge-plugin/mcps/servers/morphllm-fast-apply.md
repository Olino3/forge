# morphllm-fast-apply

> *Fast pattern-based code transformations*

## Configuration

```json
{
  "command": "npx",
  "args": ["@morph-llm/morph-fast-apply"],
  "env": {
    "MORPH_API_KEY": "${MORPH_API_KEY}"
  }
}
```

**Transport**: npx | **API Key**: `MORPH_API_KEY` (required) | **Runtime**: Node.js 18+

## Purpose

Efficiently applies code transformations across multiple files using pattern-based matching. Optimized for bulk edits, framework migrations, and consistent refactoring patterns.

## Available Tools

- **morph_apply**: Apply code transformations to files using pattern descriptions

## API Key Setup

```bash
# Get key from https://morph.so
export MORPH_API_KEY="your_key_here"
```

## Forge Integration

**When to activate:**
- Multi-file refactoring with consistent patterns
- Framework or library migrations
- Bulk code transformations (rename patterns, update APIs)
- Applying the same change across many files

**Recommended with Forge commands:**
- `/improve` - Large-scale refactoring operations
- `/implement` - When changes span many files

**Pairs well with:** serena (find all references first), sequential-thinking (plan the transformation)

## When Not to Use

- Single-file edits (use Edit tool directly)
- Changes requiring unique logic per file
- Non-code files

## Fallback

If unavailable (no API key), apply edits sequentially using the Edit tool. This is slower but achieves the same result for smaller change sets.

---

*Last Updated: 2026-02-10*
