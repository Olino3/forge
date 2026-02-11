# Performance Benchmarks

Version: 1.0.0
Status: Phase 5 - Optimization
Last Updated: 2026-02-11

---

## Overview

Performance baselines for the Forge interface layer, measuring token efficiency, boilerplate reduction, and context loading costs across all 81 context files and 22 skills. All data gathered from actual YAML frontmatter `estimatedTokens` values and SKILL.md boilerplate line counts.

---

## 1. Token Usage Baseline

### Per-Domain Token Inventory

| Domain | File Count | Total Estimated Tokens | Avg Tokens/File | Always-Load Cost | On-Demand Cost |
|--------|-----------|----------------------|-----------------|-----------------|----------------|
| Root (index, loading_protocol, cross_domain) | 3 | 2,500 | 833 | 2,100 (index + loading_protocol) | 400 (cross_domain) |
| Angular | 16 | 11,400 | 713 | 3,300 (index + common_issues) | 8,100 |
| Azure | 10 | 22,250 | 2,225 | 1,550 (index) | 20,700 |
| Commands | 8 | 6,750 | 844 | 300 (index) | 6,450 |
| .NET | 11 | 16,150 | 1,468 | 4,650 (index + common_issues) | 11,500 |
| Engineering | 6 | 1,850 | 308 | 250 (index) | 1,600 |
| Git | 3 | 550 | 183 | 200 (index) | 350 |
| Python | 14 | 12,950 | 925 | 1,150 (index + common_issues) | 11,800 |
| Schema | 4 | 5,850 | 1,463 | 2,200 (index + common_patterns) | 3,650 |
| Security | 3 | 1,800 | 600 | 1,200 (index) | 600 |
| **TOTAL** | **78** | **82,050** | **1,052** | **16,900** | **65,150** |

> **Note**: 78 domain-specific files + 3 root files = 81 total context files. The root files (index.md, loading_protocol.md, cross_domain.md) are cross-domain and always-load.

### Skill Complexity Tiers

| Tier | Skills | Typical Context Files Loaded | Estimated Token Range |
|------|--------|------------------------------|----------------------|
| Simple | commit-helper, get-git-diff, email-writer, slack-message-composer | 0-2 | 0-400 |
| Medium | generate-python-unit-tests, generate-jest-unit-tests, documentation-generator, generate-mock-service, python-dependency-management | 3-5 | 400-800 |
| Complex | python-code-review, dotnet-code-review, angular-code-review, generate-azure-functions, generate-azure-pipelines, generate-azure-bicep | 4-6 | 800-1,200 |
| Heavy | generate-tilt-dev-environment (azure + engineering cross-domain) | 6-8 | 1,200-2,000 |

---

## 2. Boilerplate Metrics

### Current State: Lines per Skill (Steps 2, 3, N)

| Skill | Step 2 Lines (Memory) | Step 3 Lines (Context) | Step N Lines (Update) | Total Boilerplate | Notes |
|-------|----------------------|----------------------|----------------------|-------------------|-------|
| SKILL_TEMPLATE.md | 5 | 5 | 5 | 15 | Minimal reference template |
| python-code-review | 22 | 21 | 10 | 53 | Complex; 2 domains + cross-domain |
| generate-python-unit-tests | 27 | 28 | 30 | 85 | 8-step workflow; verbose memory update |
| generate-jest-unit-tests | 25 | 26 | 28 | 79 | Similar to python-unit-tests |
| commit-helper | 1 | 0 | 8 | 9 | Lightweight; minimal context loading |
| documentation-generator | 12 | 14 | 10 | 36 | Moderate complexity |
| dotnet-code-review | 20 | 22 | 10 | 52 | Similar to python-code-review |
| angular-code-review | 20 | 22 | 10 | 52 | Similar to python-code-review |

**Summary Statistics**:
- **Average boilerplate across complex skills**: ~55 lines per skill
- **Average boilerplate across medium skills**: ~35 lines per skill
- **Average boilerplate across simple skills**: ~10 lines per skill
- **Estimated total boilerplate across 22 skills**: ~770 lines

### Target State: With Shared Loading Patterns

| Skill | Current Boilerplate | Target (with shared_loading_patterns.md) | Reduction |
|-------|--------------------|-----------------------------------------|-----------|
| python-code-review | 53 lines | ~15 lines (3 pattern refs + domain-specific notes) | -72% |
| generate-python-unit-tests | 85 lines | ~20 lines (3 pattern refs + skill-specific steps) | -76% |
| commit-helper | 9 lines | ~8 lines (1 pattern ref + light customization) | -11% |
| documentation-generator | 36 lines | ~12 lines (3 pattern refs) | -67% |
| **Average complex skill** | **~55 lines** | **~15 lines** | **-73%** |
| **Average across all skills** | **~35 lines** | **~12 lines** | **-66%** |

---

## 3. Context Loading Patterns

### Domain Analysis

| Domain | File Count | Total Tokens | Avg Tokens/File | Always-Load Files | Always-Load Cost |
|--------|-----------|-------------|-----------------|-------------------|-----------------|
| Root | 3 | 2,500 | 833 | index.md, loading_protocol.md | 2,100 |
| Angular | 16 | 11,400 | 713 | index.md, common_issues.md | 3,300 |
| Azure | 10 | 22,250 | 2,225 | index.md | 1,550 |
| Commands | 8 | 6,750 | 844 | index.md | 300 |
| .NET | 11 | 16,150 | 1,468 | index.md, common_issues.md | 4,650 |
| Engineering | 6 | 1,850 | 308 | index.md | 250 |
| Git | 3 | 550 | 183 | index.md | 200 |
| Python | 14 | 12,950 | 925 | index.md, common_issues.md | 1,150 |
| Schema | 4 | 5,850 | 1,463 | index.md, common_patterns.md | 2,200 |
| Security | 3 | 1,800 | 600 | index.md | 1,200 |

### Loading Strategy Distribution

| Strategy | File Count | Percentage | Total Tokens | Notes |
|----------|-----------|-----------|-------------|-------|
| `always` | 15 | 19% | 16,900 | Index files + critical references |
| `onDemand` | 66 | 81% | 65,150 | Loaded based on project detection |
| `lazy` | 0 | 0% | 0 | Not currently used |

> **Insight**: 81% of context files are on-demand, meaning a well-implemented ContextProvider can avoid loading ~65,000 tokens in most invocations. A typical skill loads 4-6 files (its domain index + 3-5 conditional files), consuming 800-1,200 tokens rather than the full domain cost.

---

## 4. Memory Query Efficiency

### Comparison: Current vs Cached vs SQLite

| Metric | Directory Scan (current) | CachedContextProvider | SQLiteMemoryAdapter |
|--------|------------------------|----------------------|---------------------|
| First query latency | ~50-100ms (filesystem glob) | ~50-100ms (cold cache) | ~10-20ms (indexed) |
| Repeated query latency | ~50-100ms (no caching) | ~1-5ms (warm cache) | ~5-10ms (indexed) |
| Memory overhead | None (stateless) | ~2-5 MB (in-memory index) | ~1-2 MB (SQLite file) |
| Cross-project search | O(n) directory walk | O(1) cached lookup | O(log n) indexed query |
| Full-text search | Not supported | Not supported natively | Supported (FTS5) |
| Staleness detection | Manual timestamp check | Automatic TTL-based | Automatic with triggers |
| Concurrent access | File-level locking | Read-only cache safe | WAL mode safe |

### Memory File Sizes (Typical Project)

| Memory Layer | Files per Project | Avg File Size | Total per Project |
|-------------|------------------|--------------|-------------------|
| Shared Project | 2-3 files | ~100 lines | ~250 lines |
| Skill-Specific | 2-4 files per skill | ~80 lines | ~500 lines (across 3 skills) |
| Command | 1-2 files | ~50 lines | ~75 lines |
| Agent | 1-2 files | ~30 lines | ~50 lines |
| **Total** | **~15 files** | — | **~875 lines** |

---

## 5. Success Metrics Tracking

### Representative Skills: Before/After

| Metric | commit-helper (Simple) | generate-python-unit-tests (Medium) | python-code-review (Complex) |
|--------|----------------------|-------------------------------------|------------------------------|
| **Context tokens before** | 0 | ~600 (4 files) | ~1,000 (5 files) |
| **Context tokens after (projected)** | 0 | ~500 (smarter loading) | ~800 (pattern-based) |
| **Boilerplate lines before** | 9 | 85 | 53 |
| **Boilerplate lines after (projected)** | 8 | 20 | 15 |
| **Memory loads before** | 1 | 2 | 3 |
| **Memory loads after (projected)** | 1 | 2 | 2 |
| **Est. time to add similar skill before** | ~30 min | ~2 hours | ~2.5 hours |
| **Est. time to add similar skill after (projected)** | ~20 min | ~45 min | ~50 min |

### Phase 5 Success Criteria

| Metric | Baseline | Target | Status |
|--------|----------|--------|--------|
| Context tokens per skill invocation | 800-1,200 | 400-700 | TBD |
| Skill boilerplate lines (steps 2,3,N) | ~35-85/skill | ~8-20/skill | TBD |
| Time to add new skill | ~2 hours | ~45 min | TBD |
| Always-load token budget | 16,900 (all domains) | 2,000-4,000 (per invocation) | TBD |
| Memory query latency (repeated) | ~50-100ms | ~1-5ms (cached) | TBD |
| Cross-project memory search | O(n) walk | O(1) or O(log n) | TBD |

---

## 6. Optimization Opportunities

### Highest Impact

1. **Shared Loading Patterns** (`shared_loading_patterns.md`): Reduces ~770 lines of boilerplate across 22 skills to ~264 lines (-66%).
2. **CachedContextProvider**: Eliminates repeated filesystem scans, reducing repeated query latency from ~100ms to ~5ms.
3. **SQLiteMemoryAdapter**: Enables indexed memory queries and full-text search across projects.

### Medium Impact

4. **Context7 MCP Integration**: Offloads library-specific documentation to external MCP, reducing context file maintenance burden.
5. **Deprecation Rules**: Provides structured migration path for removing legacy patterns.

### Lower Impact (Future)

6. **Vector Store Adapter**: Enables semantic search across memory and context, useful at scale (50+ projects).

---

## Interface References

- **ContextProvider**: [context_provider.md](context_provider.md)
- **MemoryStore**: [memory_store.md](memory_store.md)
- **Migration Guide**: [migration_guide.md](migration_guide.md)
