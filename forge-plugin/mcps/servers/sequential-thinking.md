# sequential-thinking

> *Structured multi-step reasoning for complex problems*

## Configuration

```json
{
  "command": "npx",
  "args": ["-y", "@modelcontextprotocol/server-sequential-thinking"]
}
```

**Transport**: npx | **API Key**: None | **Runtime**: Node.js 18+

## Purpose

Provides structured step-by-step reasoning for complex problems. Breaks down multi-faceted tasks into sequential thinking steps, enabling systematic analysis, debugging, and architectural evaluation.

## Available Tools

- **sequential_thinking**: Create and manage a chain of reasoning steps with branching and revision support

## Forge Integration

**When to activate:**
- Complex debugging requiring root cause analysis
- Architecture evaluation with multiple trade-offs
- Multi-step planning before implementation
- Code review of complex logic paths

**Recommended with Forge commands:**
- `/analyze` - Systematic code quality assessment
- `/brainstorm` - Structured requirements discovery
- `/improve` - Strategic refactoring planning

## When Not to Use

- Simple, single-step tasks
- Straightforward code generation
- Tasks where native Claude reasoning suffices

## Fallback

If unavailable, use Claude's native extended thinking capabilities. The reasoning quality is comparable for most tasks.

---

*Last Updated: 2026-02-10*
