---
id: "engineering/error_recovery"
domain: engineering
title: "Error Recovery Patterns"
type: reference
estimatedTokens: 350
loadingStrategy: onDemand
version: "0.1.0-alpha"
lastUpdated: "2026-02-10"
sections:
  - name: "Git Access Failures"
    estimatedTokens: 60
    keywords: [git, access, failures]
  - name: "Memory Read/Write Failures"
    estimatedTokens: 57
    keywords: [memory, readwrite, failures]
  - name: "Context File Failures"
    estimatedTokens: 41
    keywords: [context, file, failures]
  - name: "Large Diff Handling"
    estimatedTokens: 55
    keywords: [large, diff, handling]
  - name: "Permission Issues"
    estimatedTokens: 19
    keywords: [permission, issues]
  - name: "General Recovery Principles"
    estimatedTokens: 49
    keywords: [recovery, principles]
tags: [engineering, error-recovery, git, memory, context, permissions]
---

# Error Recovery Patterns

Compact guide for skills to handle failures gracefully during execution.

## Git Access Failures

| Error | Recovery |
|-------|----------|
| `fatal: not a git repository` | Fall back to manual file listing via `ls`/`find`. Note limitation in output. |
| `fatal: bad revision` | Verify commit hashes exist. Try `git log --oneline -5` to find valid commits. |
| `Permission denied` on git commands | Add required permissions to `.claude/settings.local.json`. List exact command needed. |
| Empty diff (no changes) | Confirm commit range. Report "no changes detected" rather than failing silently. |

## Memory Read/Write Failures

| Error | Recovery |
|-------|----------|
| Memory directory doesn't exist | Expected for new projects. Proceed with context-only analysis. |
| Memory file corrupted or unparseable | Log warning, skip the file, proceed without it. Note in output. |
| Cannot write memory (permissions) | Complete the analysis, output results. Warn user about memory write failure. |
| Memory file exceeds 500 lines | Don't fail. Archive old entries per `lifecycle.md` rules, then write. |

## Context File Failures

| Error | Recovery |
|-------|----------|
| Context file not found | Skip gracefully. Note which context was unavailable in output. |
| Context index missing | Fall back to loading known files for the domain (common_issues.md, etc.). |
| Multiple context files missing | Proceed with available context. Add prominent warning in output. |

## Large Diff Handling

| Threshold | Action |
|-----------|--------|
| > 2000 lines changed | Switch to summary mode: file-level stats, focus on critical files only |
| > 5000 lines changed | Summary mode + ask user to narrow scope to specific files/directories |
| > 50 files changed | Group by directory, analyze top 10 most-changed files in detail |
| Rename-heavy diffs | Separate renames from content changes, focus analysis on content changes |

## Permission Issues

When a bash command is denied, provide the user with the exact permission string to add:

```
Permission required. Add to .claude/settings.local.json:
"Bash(git diff HEAD~1:*)"
```

## General Recovery Principles

1. **Never fail silently** - always report what went wrong and what was skipped
2. **Degrade gracefully** - partial results are better than no results
3. **Preserve output** - save whatever was completed before the failure
4. **Suggest fixes** - tell the user exactly how to resolve the issue
5. **Don't retry blindly** - if an operation fails, try an alternative approach

---

*Last Updated: 2026-02-10*
