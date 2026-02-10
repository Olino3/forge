# Memory Lifecycle Management

Rules for memory freshness, pruning, and archival to keep memory accurate and efficient.

## Freshness Indicators

Every memory file must include a timestamp comment as its first line:

```markdown
<!-- Last Updated: 2026-02-10 -->
```

Skills must update this timestamp whenever they modify a memory file.

## Staleness Thresholds

| Age | Status | Action |
|-----|--------|--------|
| 0-30 days | Fresh | Use as-is |
| 31-90 days | Aging | Use but verify critical claims against current code |
| 90+ days | Potentially stale | Add `[POTENTIALLY STALE]` note, verify before relying on |

## Pruning Rules

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

## Reset Protocol

To start fresh for a project:

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

---

*Last Updated: 2026-02-10*
