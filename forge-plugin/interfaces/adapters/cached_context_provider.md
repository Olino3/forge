# CachedContextProvider Adapter

Version: 0.1.0-alpha
Status: Specification
Last Updated: 2026-02-11

---

## Overview

The `CachedContextProvider` is a caching decorator that wraps any `ContextProvider` implementation (typically `MarkdownFileContextProvider`) to eliminate redundant file reads within a session. It implements the same `ContextProvider` interface, adding three tiers of caching with session-scoped invalidation.

### Design Goals

1. **Zero redundant file reads** — within a session, each context file is read at most once
2. **Transparent integration** — consumers call the same ContextProvider methods; caching is invisible
3. **Session-scoped lifecycle** — cache is discarded at session end; no stale cross-session data
4. **ExecutionContext alignment** — maps to `recordContextLoad()`/`getCachedContext()` in ExecutionContext

---

## Three-Tier Cache Architecture

### Tier 1: Catalog Cache (Domain Metadata)

**What**: Complete domain catalogs (list of files with metadata, no content)
**Populated by**: `getCatalog()`, `getDomainIndex()`
**Invalidated by**: Session end, explicit `invalidate(domain)`
**Token cost**: 0 (metadata only)

### Tier 2: Reference Cache (File Metadata)

**What**: Individual file references (frontmatter metadata, no content)
**Populated by**: `getReference()`, as side effect of `getAlwaysLoadFiles()`, `getConditionalContext()`
**Invalidated by**: Session end, explicit `invalidate(domain, file)`
**Token cost**: 0 (metadata only)

### Tier 3: Content Cache (Materialized Text)

**What**: Full or partial file content (the actual context text)
**Populated by**: `materialize()`, `materializeSections()`, `getAlwaysLoadFiles()`, `getConditionalContext()`, `getCrossDomainContext()`
**Invalidated by**: Session end, explicit `invalidate(domain, file)`
**Token cost**: Full token cost of cached content

---

## Method-by-Method Cacheability

| Method | Cacheable | Cache Tier | Notes |
|--------|-----------|------------|-------|
| `getCatalog(domain?)` | Yes | Tier 1 | Domain metadata rarely changes mid-session |
| `getDomainIndex(domain)` | Yes | Tier 1 | Index structure is static |
| `getLoadingProtocol()` | Yes | Tier 1 | Protocol never changes mid-session |
| `getAlwaysLoadFiles(domain)` | Yes | Tier 3 | Files are static; cache full content |
| `detectProjectType(domain, signals)` | No | — | Depends on runtime signals; must re-evaluate |
| `getConditionalContext(domain, detection)` | Partial | Tier 3 | Individual files cached; selection logic re-runs |
| `getCrossDomainContext(domain, triggers)` | Partial | Tier 3 | Individual files cached; trigger matching re-runs |
| `getReference(domain, file)` | Yes | Tier 2 | Metadata is static |
| `materialize(reference)` | Yes | Tier 3 | Content is static |
| `materializeSections(ref, sections[])` | Yes | Tier 3 | Keyed by ref + sections combination |
| `search(query, domain?)` | No | — | Must re-evaluate against current query |

---

## Cache Key Design

| Cache Tier | Key Format | Example |
|------------|-----------|---------|
| Tier 1 | `catalog:{domain}` or `catalog:*` | `catalog:python`, `catalog:*` |
| Tier 1 | `index:{domain}` | `index:python` |
| Tier 2 | `ref:{domain}/{file}` | `ref:python/fastapi_patterns` |
| Tier 3 | `content:{domain}/{file}` | `content:python/fastapi_patterns` |
| Tier 3 | `sections:{domain}/{file}:{section1,section2}` | `sections:python/fastapi_patterns:Security Issues` |

---

## Session-Scoped Invalidation

### Automatic Invalidation

The cache is **completely discarded** at session end. No cache state persists between Claude Code sessions. This eliminates the risk of serving stale context from modified files.

### Manual Invalidation

For mid-session context edits (e.g., a user modifies a context file while the session is active):

`invalidate(domain?, file?)`:
- `invalidate()` — clears ALL caches (all tiers)
- `invalidate("python")` — clears all Python domain caches (all tiers)
- `invalidate("python", "fastapi_patterns")` — clears caches for one file (Tier 2 + Tier 3)

### Invalidation Propagation

| Action | Tier 1 Impact | Tier 2 Impact | Tier 3 Impact |
|--------|---------------|---------------|---------------|
| `invalidate()` | Cleared | Cleared | Cleared |
| `invalidate(domain)` | Domain entry cleared | All domain refs cleared | All domain content cleared |
| `invalidate(domain, file)` | Unchanged | File ref cleared | File content cleared |

---

## ExecutionContext Integration

The CachedContextProvider maps directly to the `ExecutionContext` interface methods:

| CachedContextProvider | ExecutionContext Equivalent |
|----------------------|----------------------------|
| Write to Tier 3 cache | `executionContext.recordContextLoad(state, domain, topic, content)` |
| Read from Tier 3 cache | `executionContext.getCachedContext(state, domain, topic)` |
| Invalidate cache | (no equivalent — ExecutionContext does not invalidate) |

**When both are active**: The CachedContextProvider operates at the adapter level (per-file), while ExecutionContext operates at the command level (per-chain). In a command chain:

1. First command: CachedContextProvider populates its cache → ExecutionContext records loads
2. Second command: ExecutionContext cache hit → skip CachedContextProvider entirely
3. Third command: ExecutionContext cache hit → skip CachedContextProvider entirely

**Net effect**: CachedContextProvider optimizes within a single command invocation; ExecutionContext optimizes across chained commands.

---

## Token Savings Estimates

### Scenario 1: Single Skill Invocation

| Component | Without Cache | With Cache | Savings |
|-----------|--------------|------------|---------|
| Domain index | 1 read | 1 read | 0% |
| Always-load files | 2 reads | 2 reads | 0% |
| Conditional context | 2 reads | 2 reads | 0% |
| Cross-domain | 1 read | 1 read | 0% |
| **Total** | **6 reads** | **6 reads** | **0%** |

*No savings for a single invocation — cache hasn't been populated yet.*

### Scenario 2: Command Chain (`/analyze` → `/improve`)

| Component | Without Cache | With Cache | Savings |
|-----------|--------------|------------|---------|
| /analyze: full load | 6 reads | 6 reads | 0% |
| /improve: domain index | 1 read | 0 reads (cached) | 100% |
| /improve: always-load | 2 reads | 0 reads (cached) | 100% |
| /improve: detection | 1 read | 1 read (not cached) | 0% |
| /improve: conditional | 2 reads | 0 reads (cached) | 100% |
| /improve: cross-domain | 1 read | 0 reads (cached) | 100% |
| **Total** | **13 reads** | **7 reads** | **~46%** |

### Scenario 3: Three-Command Chain (`/analyze` → `/improve` → `/test`)

| Component | Without Cache | With Cache | Savings |
|-----------|--------------|------------|---------|
| Total reads | ~19 | ~8 | **~58%** |

---

## Implementation Notes

- The CachedContextProvider wraps `MarkdownFileContextProvider` using the decorator pattern
- Cache is implemented as in-memory maps (no filesystem caching)
- Cache size is bounded by the number of context files (81 max, ~50KB total)
- Thread safety is not required (Claude Code is single-threaded per session)
- Cache hit/miss statistics can be logged for performance analysis

---

*Last Updated: 2026-02-11*
