# Memory Lifecycle Management

Rules for memory freshness, pruning, and archival to keep memory accurate and efficient.

> **Interface**: These rules are formalized and automated by the [MemoryStore interface](../interfaces/memory_store.md). Skills and commands should use `memoryStore` methods rather than implementing lifecycle logic manually.

## Freshness Indicators

Every memory file must include a timestamp comment as its first line:

```markdown
<!-- Last Updated: 2026-02-10 -->
```

**Automation**: `memoryStore.create()` and `memoryStore.update()` inject/refresh this timestamp automatically. Skills no longer need to manage timestamps manually.

## Staleness Thresholds

| Age | Status | Action |
|-----|--------|--------|
| 0-30 days | Fresh | Use as-is |
| 31-90 days | Aging | Use but verify critical claims against current code |
| 90+ days | Potentially stale | Add `[POTENTIALLY STALE]` note, verify before relying on |

**Automation**: `memoryStore.read()` auto-computes staleness from the `<!-- Last Updated -->` timestamp. `memoryStore.getStalenessReport()` returns staleness status for all memory files in a project.

## Pruning Rules

Pruning removes or archives entries that are no longer relevant. `memoryStore.prune(policy)` automates these rules — pass a policy object to control which file types to prune and their retention thresholds.

### review_history.md
- Keep the **last 10 entries** in the main file
- Move older entries to `review_history_archive.md`
- Archive file has no size limit but is never loaded automatically

### known_issues.md
- Remove issues marked **"Resolved"** for 30+ days
- Keep issues marked **"In Progress"** regardless of age
- Issues with no status update for 90+ days get `[VERIFY STATUS]` tag

### common_patterns.md
- Flag for verification every **5th skill invocation**
- Remove patterns that no longer appear in the codebase
- Consolidate similar patterns into single entries

### test_results_history.md (test-cli-tools)
- Keep the **last 15 test sessions**
- Summarize older sessions into a "Historical Summary" section

## Size Limits

| File | Max Lines | Action When Exceeded |
|------|-----------|---------------------|
| Any single memory file | 500 | Split into focused sub-files |
| project_overview.md | 200 | Move detailed sections to separate files |
| review_history.md | 300 | Archive older entries |

**Automation**: `memoryStore.update()` and `memoryStore.append()` check line counts against these limits and return a `warning` string if exceeded. The write still succeeds — warnings are advisory.

## Reset Protocol

To start fresh for a project, use `memoryStore.delete()` for individual entries or the following commands:

```bash
# Delete skill-specific memory
rm -rf memory/skills/{skill-name}/{project-name}/

# Delete shared project memory
rm -rf memory/projects/{project-name}/

# Skills will rebuild automatically on next invocation
```

## Verification Prompt

On every 5th invocation of any skill, include this self-check:

> **Memory verification**: Spot-check 2-3 claims from `project_overview.md` against actual code. Update or remove any inaccurate entries.

**Automation**: `memoryStore.validate(id)` performs automated checks (completeness, accuracy, specificity, growth) as defined in [quality_guidance.md](quality_guidance.md). Use it in conjunction with manual spot-checks.

---

*Last Updated: 2026-02-10*
