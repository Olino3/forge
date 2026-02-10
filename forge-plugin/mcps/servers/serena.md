# serena

> *Semantic code understanding and project navigation*

## Configuration

```json
{
  "command": "uvx",
  "args": ["--from", "git+https://github.com/oraios/serena", "serena", "start-mcp-server", "--context", "ide-assistant"]
}
```

**Transport**: uvx | **API Key**: None | **Runtime**: Python 3.9+, uv package manager

## Purpose

Provides semantic code understanding with project-level intelligence. Uses language-aware parsing to understand symbols, references, and project structure beyond simple text search.

## Available Tools

- **find_symbol**: Find symbol definitions across the project
- **find_references**: Find all references to a symbol
- **get_file_summary**: Get a structural summary of a file
- **get_project_summary**: Get project-wide structural overview

## Prerequisites

Requires Python and uv (not just Node.js):

```bash
# Install uv if not present
curl -LsSf https://astral.sh/uv/install.sh | sh
```

## Forge Integration

**When to activate:**
- Large codebase navigation and understanding
- Symbol lookup across multiple files
- Refactoring that requires knowing all references
- Initial project exploration

**Recommended with Forge commands:**
- `/analyze` - Deep structural analysis of codebases
- `/improve` - Find all references before refactoring
- `/implement` - Understand existing patterns before adding code

**Pairs well with:** sequential-thinking (analysis), morphllm-fast-apply (bulk edits)

## When Not to Use

- Small, single-file tasks
- When Grep/Glob provide sufficient results
- Non-code files (documentation, config)

## Fallback

If unavailable, use Grep for text-based symbol search, Glob for file discovery, and Read for file contents. These tools cover most use cases but lack semantic understanding.

---

*Last Updated: 2026-02-10*
