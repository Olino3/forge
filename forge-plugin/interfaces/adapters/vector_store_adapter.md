# VectorStore Adapter

**Version**: 0.1.0-alpha
**Status**: Future Adapter Specification (Design Only)

---

## Overview

The VectorStoreAdapter augments the existing `ContextProvider.search()` and `MemoryStore.search()` methods with semantic similarity search using vector embeddings. It does **not replace** either interface — it provides an optional semantic fallback when keyword search yields insufficient results.

### Design Goals

1. **Semantic discovery** — find relevant context/memory even when exact keywords don't match
2. **Augmentation, not replacement** — keyword search remains primary; vectors provide fallback
3. **Offline-capable** — pre-computed embeddings stored locally; no runtime API calls for search
4. **Minimal setup** — embeddings generated once, updated incrementally on file changes

---

## Embedding Strategy

### What Gets Embedded

| Source | Granularity | Estimated Vectors | Update Frequency |
|--------|-------------|-------------------|-----------------|
| Context file sections | Per-section (~3-5 per file) | ~300 (from 81 files) | Rare (context is static) |
| Memory entries | Per-entry (full content) | Variable (grows with usage) | Every memory write |
| Skill metadata | Per-skill (frontmatter + description) | 22 | Rare (skill definitions are static) |
| Agent metadata | Per-agent (config.json fields) | 11 | Rare (agent configs are static) |

### Embedding Model

| Option | Dimensions | Token Limit | Recommended For |
|--------|-----------|-------------|----------------|
| `text-embedding-3-small` | 1536 | 8191 | Default: good balance of quality and cost |
| `text-embedding-3-large` | 3072 | 8191 | High-precision semantic matching |
| Local model (e.g., `all-MiniLM-L6-v2`) | 384 | 512 | Offline, zero-cost, lower quality |

---

## Vector Index Schema

### VectorEntry

```
VectorEntry {
  id: string              // Unique identifier (e.g., "context:python/fastapi_patterns:Security Issues")
  source: string           // "context", "memory", "skill", "agent"
  domain: string           // Domain if applicable (e.g., "python", "dotnet")
  text: string             // Original text that was embedded
  embedding: float[]       // Vector embedding
  metadata: {
    file: string           // Source file path
    section: string?       // Section name (for context files)
    project: string?       // Project name (for memory entries)
    skill: string?         // Skill name (for skill-specific memory)
    tags: string[]         // Searchable tags
    estimatedTokens: int   // Token cost of the source text
    updatedAt: string      // Last embedding update
  }
}
```

### Storage Options

| Storage | Format | Pros | Cons |
|---------|--------|------|------|
| SQLite + blob | `.forge/vectors.db` | Single file, SQL queries on metadata | Requires SQLite |
| JSON file | `.forge/vectors.json` | Portable, human-readable | Slow for large indices |
| Binary file | `.forge/vectors.bin` | Fast loading, compact | Not human-readable |

**Recommended**: SQLite for metadata + binary blob for vectors (hybrid approach).

---

## Query Interface

### `searchSemantic(query, options?) → SemanticResult[]`

Search context files using semantic similarity.

**Parameters**:

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `query` | `string` | Yes | Natural language query |
| `options.domain` | `string` | No | Restrict to specific domain |
| `options.source` | `string` | No | Restrict to "context", "memory", "skill" |
| `options.topK` | `integer` | No | Number of results (default: 5) |
| `options.minSimilarity` | `float` | No | Minimum cosine similarity threshold (default: 0.7) |

**Returns**: `SemanticResult[]`

```
SemanticResult {
  entry: VectorEntry       // The matched vector entry
  similarity: float        // Cosine similarity score (0.0 to 1.0)
  reference: ContextReference | MemoryEntry  // Interface-compatible reference for loading
}
```

### `searchMemorySemantic(query, options?) → SemanticResult[]`

Search memory entries using semantic similarity.

**Parameters**: Same structure as `searchSemantic`, restricted to memory vectors.

**Returns**: `SemanticResult[]` (same structure, with `reference` always being a `MemoryEntry`).

### `findRelevantContext(codeSnippet, domain?) → SemanticResult[]`

Given a code snippet, find the most relevant context files.

**Parameters**:

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `codeSnippet` | `string` | Yes | Code snippet to find relevant context for |
| `domain` | `string` | No | Restrict to specific domain |

**Returns**: `SemanticResult[]`

**Use case**: Automatically determine which context files are relevant based on code being analyzed, without relying on keyword matching or detection triggers.

---

## Integration Points

### With ContextProvider

```
// Current: keyword search
results = contextProvider.search("sql injection security")

// Enhanced: keyword search with semantic fallback
results = contextProvider.search("sql injection security")
if results.length < 3:
  semanticResults = vectorStore.searchSemantic("sql injection security", {source: "context"})
  results = merge(results, semanticResults)
```

### With MemoryStore

```
// Current: pattern search
results = memoryStore.search("FastAPI authentication")

// Enhanced: pattern search with semantic fallback
results = memoryStore.search("FastAPI authentication")
if results.matches.length == 0:
  semanticResults = vectorStore.searchMemorySemantic("FastAPI authentication")
  results.matches = semanticResults.map(toSearchMatch)
```

### With detectProjectType

```
// Current: rule-based detection
detection = contextProvider.detectProjectType("python", signals)

// Enhanced: supplement with semantic matching
if detection.framework == null:
  codeContext = signals.imports.join("\n") + signals.codePatterns.join("\n")
  semanticResults = vectorStore.findRelevantContext(codeContext, "python")
  // Use top semantic results to inform framework detection
```

---

## Comparison: Keyword Search vs Vector Search

| Dimension | Keyword Search (Current) | Vector Search (VectorStore) |
|-----------|------------------------|---------------------------|
| **Exact match** | Excellent | Poor (may miss exact terms) |
| **Semantic similarity** | Poor (requires exact keywords) | Excellent (understands meaning) |
| **Typo tolerance** | None | High (embedding captures meaning) |
| **Cross-language** | None | Moderate (if multilingual model) |
| **Setup cost** | Zero | Requires embedding generation |
| **Runtime cost** | Low (string matching) | Medium (vector comparison) |
| **Index size** | Zero (no index) | ~2-10MB for Forge-scale |
| **Update cost** | Zero | Re-embed on file change |
| **Offline support** | Full | Full (pre-computed embeddings) |
| **Ranking quality** | Binary (match/no match) | Continuous (similarity score) |

---

## Related Documents

- **ContextProvider**: [`context_provider.md`](../context_provider.md) — augmented by semantic search
- **MemoryStore**: [`memory_store.md`](../memory_store.md) — augmented by semantic search
- **CachedContextProvider**: [`cached_context_provider.md`](cached_context_provider.md) — caches semantic results
- **Context7**: [`context7_mcp_context_provider.md`](context7_mcp_context_provider.md) — complementary live docs

---

*Last Updated: 2026-02-11*
