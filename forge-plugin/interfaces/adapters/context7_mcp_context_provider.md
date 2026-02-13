# Context7 MCP Context Provider Adapter

**Version**: 0.3.0-alpha
**Status**: Future Adapter Specification (Design Only)
**Implements**: [`context_provider.md`](../context_provider.md) (ContextProvider interface)

---

## Overview

The Context7MCPContextProvider is a future hybrid adapter that combines the Context7 MCP server (live framework documentation) with the existing MarkdownFileContextProvider (curated Forge context). It implements the ContextProvider interface, routing queries to Context7 for framework-specific content while preserving Forge-curated content for engineering patterns, security guidelines, and custom conventions.

### Design Goals

1. **Always-fresh framework docs** — library-specific context comes from Context7's live documentation instead of potentially outdated local files
2. **Preserve Forge curation** — engineering patterns, security guidelines, and custom conventions remain locally curated
3. **Graceful degradation** — if Context7 is unavailable, fall back seamlessly to local files
4. **Cache-aware** — results cached via CachedContextProvider to avoid redundant MCP calls

---

## Tool Mapping

### Context7 MCP Tools

| Context7 Tool | ContextProvider Method(s) | Usage |
|---------------|--------------------------|-------|
| `resolve-library-id` | `detectProjectType()` | Resolve library names to Context7 IDs for downstream queries |
| `query-docs` | `getConditionalContext()`, `materialize()`, `search()` | Fetch live documentation for specific libraries/frameworks |

### Method-to-Tool Mapping

| ContextProvider Method | Source | Rationale |
|----------------------|--------|-----------|
| `getCatalog(domain?)` | Local | Forge-curated catalog structure; Context7 has no catalog concept |
| `getDomainIndex(domain)` | Local | Forge navigation structure; not available from Context7 |
| `getLoadingProtocol()` | Local | Forge-specific protocol; not a Context7 concept |
| `getAlwaysLoadFiles(domain)` | Local | Always-load files are Forge-curated (common_issues, context_detection) |
| `detectProjectType(domain, signals)` | Local + Context7 | Use local detection logic; call `resolve-library-id` to verify library availability |
| `getConditionalContext(domain, detection)` | **Context7** (primary) + Local (fallback) | Framework docs from Context7; Forge patterns from local |
| `getCrossDomainContext(domain, triggers)` | Local | Cross-domain triggers are Forge-curated |
| `getReference(domain, file)` | Local | Metadata is Forge-curated |
| `materialize(reference)` | **Context7** (for framework files) + Local (for Forge files) | Route based on file classification |
| `materializeSections(reference, sections[])` | Local | Section-level loading requires Forge's section metadata |
| `search(query, domain?)` | Local + Context7 | Search both sources, merge and rank results |

---

## Hybrid Architecture

### File Classification: Replaceable vs Forge-Curated

#### Replaceable by Context7 (~12 files)

These files contain framework-specific documentation that Context7 can provide fresher:

| Domain | File | Context7 Library | Rationale |
|--------|------|-----------------|-----------|
| python | `fastapi_patterns.md` | FastAPI | Framework-specific patterns available in live docs |
| python | `django_patterns.md` | Django | Framework-specific patterns |
| python | `flask_patterns.md` | Flask | Framework-specific patterns |
| python | `datascience_patterns.md` | pandas, numpy | Library-specific patterns |
| python | `ml_patterns.md` | scikit-learn, pytorch | ML library patterns |
| angular | `ngrx_patterns.md` | NgRx | State management library docs |
| angular | `rxjs_patterns.md` | RxJS | Reactive library docs |
| angular | `primeng_patterns.md` | PrimeNG | UI component library docs |
| dotnet | `ef_patterns.md` | Entity Framework | ORM-specific patterns |
| dotnet | `blazor_patterns.md` | Blazor | Framework-specific patterns |
| dotnet | `aspnet_patterns.md` | ASP.NET Core | Framework-specific patterns |
| dotnet | `linq_patterns.md` | .NET LINQ | Language feature docs |

#### Supplementable (~6 files)

These files mix Forge-curated content with framework-specific content:

| Domain | File | Supplement Strategy |
|--------|------|-------------------|
| python | `testing_frameworks.md` | Supplement with pytest/unittest latest docs |
| python | `mocking_patterns.md` | Supplement with unittest.mock latest |
| angular | `jest_testing_standards.md` | Supplement with Jest latest docs |
| angular | `component_patterns.md` | Supplement with Angular latest |
| azure | `azure_functions_overview.md` | Supplement with Azure Functions latest |
| azure | `azure_pipelines_overview.md` | Supplement with Azure DevOps latest |

#### Not Replaceable — Forge-Curated (~63 files)

These files contain Forge-specific content that Context7 cannot provide:

- All `index.md` files (navigation structure)
- All `context_detection.md` files (Forge detection logic)
- All `common_issues.md` files (curated issue databases)
- All `engineering/` files (Forge engineering patterns)
- All `commands/` files (Forge command patterns)
- All `security/` files (Forge security guidelines)
- All `schema/` files (Forge schema patterns)
- All `git/` files (Forge git patterns)
- `cross_domain.md` and `loading_protocol.md`

---

## Fallback Strategy

```
1. Check: Is the requested file classified as "Replaceable" or "Supplementable"?
   |-- No  --> Use MarkdownFileContextProvider (local file)
   +-- Yes --> Continue to step 2

2. Resolve: Call Context7 `resolve-library-id` for the library
   |-- Not found --> Fall back to MarkdownFileContextProvider
   +-- Found     --> Continue to step 3

3. Query: Call Context7 `query-docs` with relevant topic
   |-- Error/timeout --> Fall back to MarkdownFileContextProvider
   +-- Success       --> Continue to step 4

4. Cache: Store result via CachedContextProvider (Tier 3 content cache)

5. Return: Merged result (Context7 content + any Forge-only sections)
```

---

## Comparison: Local Markdown vs Context7

| Dimension | MarkdownFileContextProvider | Context7MCPContextProvider |
|-----------|---------------------------|--------------------------|
| **Availability** | Always (local files) | Requires MCP server running |
| **Freshness** | Static (updated manually) | Live (always current) |
| **Curation** | Hand-curated for Forge patterns | Raw library documentation |
| **Token cost** | Known (estimatedTokens in frontmatter) | Variable (depends on query) |
| **Latency** | Instant (file read) | Network round-trip (~100-500ms) |
| **Offline support** | Full | None |
| **Section-level loading** | Supported (frontmatter sections) | Not supported |
| **Search** | Tag/keyword based | Library-aware semantic |
| **Coverage** | 81 curated files across 9 domains | Thousands of libraries |

---

## Related Documents

- **Interface**: [`context_provider.md`](../context_provider.md) — ContextProvider interface this adapter implements
- **Current Adapter**: [`markdown_file_context_provider.md`](markdown_file_context_provider.md) — current filesystem adapter
- **Cache Layer**: [`cached_context_provider.md`](cached_context_provider.md) — caching decorator
- **MCP Docs**: [`../../mcps/servers/context7.md`](../../mcps/servers/context7.md) — Context7 MCP server documentation

---

*Last Updated: 2026-02-11*
