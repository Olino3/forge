# MCP Activation Protocol

> *When to summon each external conduit*

## Decision Matrix

Use the following matrix to determine which MCP server(s) to activate based on the current task.

### By Task Signal

| Signal in Request | Activate | Rationale |
|-------------------|----------|-----------|
| Library imports, API names, framework keywords | **context7** | Official documentation lookup |
| Complex debugging, `--think`, architecture analysis | **sequential-thinking** | Structured multi-step reasoning |
| `component`, `UI`, frontend layout | **magic** | Modern UI component generation |
| `test`, `e2e`, `browser`, visual validation | **playwright** | Real browser automation |
| Large codebase, symbol lookup, session persistence | **serena** | Semantic code understanding |
| Multi-file edits, bulk refactoring, migration | **morphllm-fast-apply** | Pattern-based code transforms |
| `research`, `latest`, current events, fact-check | **tavily** | Web search and retrieval |
| `performance`, `debug`, `LCP`, `CLS`, console errors | **chrome-devtools** | Chrome DevTools Protocol |

### By Forge Command

| Command | Auto-activate |
|---------|--------------|
| `/analyze` | sequential-thinking (complex analysis), context7 (framework detection) |
| `/implement` | context7 (patterns), magic (if UI task) |
| `/improve` | morphllm-fast-apply (multi-file), sequential-thinking (strategy) |
| `/test` | playwright (if E2E), sequential-thinking (test strategy) |
| `/brainstorm` | sequential-thinking (structured discovery), tavily (research) |
| `/build` | context7 (build tool docs) |

## Fallback Strategies

When an MCP server is unavailable (not installed, API key missing, or erroring), fall back to native capabilities.

| MCP Server | Fallback Strategy |
|------------|-------------------|
| sequential-thinking | Use native Claude reasoning (extended thinking) |
| context7 | Use WebSearch for documentation, read local node_modules |
| magic | Generate components manually using framework patterns |
| playwright | Use manual test instructions, suggest user run tests |
| serena | Use Grep/Glob for code navigation, Read for file contents |
| morphllm-fast-apply | Apply edits with Edit tool, one file at a time |
| tavily | Use WebSearch tool for web research |
| chrome-devtools | Suggest user run Lighthouse/DevTools manually |

## Anti-Patterns

- **Don't activate all servers** for simple tasks - each server adds overhead
- **Don't use sequential-thinking** for straightforward, single-step operations
- **Don't use context7** when you already know the API (use your training data)
- **Don't use morphllm-fast-apply** for single-file edits (use Edit tool)
- **Don't use tavily** for information within your training data cutoff
- **Don't use playwright** when unit tests suffice (no browser needed)

## Multi-Server Coordination

For complex tasks, servers can work together:

- **Full-stack feature**: context7 (patterns) + magic (UI) + playwright (E2E tests)
- **Architecture review**: sequential-thinking (analysis) + serena (code nav) + context7 (docs)
- **Performance audit**: chrome-devtools (profiling) + sequential-thinking (analysis) + playwright (verification)
- **Research + implementation**: tavily (research) + context7 (docs) + sequential-thinking (planning)

---

*Last Updated: 2026-02-10*
