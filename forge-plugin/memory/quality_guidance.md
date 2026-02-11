# Memory Quality Guidance

Practical guidance for skills to maintain high-quality memory files.

> **Interface**: These quality checks are formalized by `memoryStore.validate(id)` in the [MemoryStore interface](../interfaces/memory_store.md). The `validate()` method runs completeness, accuracy, specificity, and growth checks automatically and returns structured results. Skills can supplement automated checks with the manual guidance below.

## Quality Checks

### Completeness Check

Does `project_overview.md` cover these essentials?

- [ ] Language and version
- [ ] Framework and version
- [ ] Architecture pattern
- [ ] Key conventions (naming, file organization)
- [ ] Testing approach

If any are missing after 3+ invocations, the skill should actively investigate and fill gaps.

**Automation**: `memoryStore.validate(id)` checks for these required fields and returns a `completeness` score with a list of missing items.

### Accuracy Check

**Every 5th invocation**, spot-check 2-3 memory claims:

1. Pick a file path mentioned in memory → verify it still exists
2. Pick a convention claim → verify it matches current code
3. Pick a known issue → verify its status is current

Update or remove inaccurate entries immediately.

**Automation**: `memoryStore.validate(id)` flags entries whose `updatedAt` exceeds staleness thresholds (see [lifecycle.md](lifecycle.md)). Manual spot-checks remain essential for semantic accuracy.

### Specificity Check

Memory entries should reference **specific files and paths**, not vague descriptions:

| Bad | Good |
|-----|------|
| "Uses custom auth" | "Custom JWT auth in `app/auth/middleware.py`, 15min expiry" |
| "Has N+1 queries" | "N+1 in `OrdersController.cs:GetHistory()`, loads reviews in loop" |
| "Tests use fixtures" | "Shared fixtures in `tests/conftest.py`: `sample_user`, `mock_db`" |

### Growth Check

If `common_patterns.md` hasn't grown in 5+ invocations, consider:

- Is the skill analyzing different parts of the codebase each time?
- Are patterns too general? (Should be project-specific)
- Is the skill actually learning? (Check that analysis produces new insights)

## Writing Good Memory Entries

### Do
- Use specific file paths and line numbers
- Include dates for time-sensitive information
- Prefix status with emoji: ✅ Resolved, ⚠️ In Progress, 🔴 Critical
- Link related entries across memory files

### Don't
- Store general knowledge (belongs in context/)
- Include full code snippets (store locations instead)
- Use absolute file paths (use paths relative to repo root)
- Duplicate information across memory files

## Memory File Health Indicators

| Indicator | Healthy | Unhealthy |
|-----------|---------|-----------|
| Last Updated | Within 30 days | 90+ days old |
| Line count | 50-300 lines | <10 or >500 lines |
| Specificity | File paths, line numbers | Vague descriptions |
| Growth rate | New insights each invocation | Static for 5+ invocations |

## Using MemoryStore for Quality

Skills should call `memoryStore.validate(id)` periodically (e.g., every 5th invocation) to get automated quality feedback:

```
memoryStore.validate("skill-specific/python-code-review/my-api/project_overview")
→ {
    completeness: { score: 0.8, missing: ["testing approach"] },
    staleness: "fresh",
    lineCount: 145,
    warnings: ["approaching size limit for project_overview (200 lines)"]
  }
```

For project-wide quality assessment, combine with `memoryStore.getStalenessReport()` to identify all entries needing attention.

---

*Last Updated: 2026-02-10*
