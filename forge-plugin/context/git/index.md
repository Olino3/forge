# Git Context Files

Context files for git diff analysis, version control patterns, and commit analysis.

## Files in this Directory

### `git_diff_reference.md`

**Purpose**: Complete reference for unified diff format and git diff behavior

**Use when**: 
- Parsing diff output
- Understanding diff syntax
- Explaining diff metadata
- Handling special cases (binary files, permission changes, renames)

**Key sections**:
- Unified diff format specification
- Hunk headers and line markers
- File mode changes
- Rename and copy detection
- Binary file handling
- Git-specific extensions

**Load for**: Every `skill:get-git-diff` invocation to ensure proper parsing

---

### `diff_patterns.md`

**Purpose**: Common patterns and categories of code changes

**Use when**:
- Classifying types of changes
- Identifying change intent
- Summarizing modifications
- Detecting risky changes

**Key sections**:
- Feature additions (new functions, classes, endpoints)
- Bug fixes (error handling, validation, logic fixes)
- Refactoring (code restructuring, naming, organization)
- Dependency updates (version bumps, new libraries)
- Security fixes (injection, auth, XSS)
- Database migrations (schema changes, data migrations)
- Configuration changes (environment, settings, infrastructure)
- Performance optimizations (algorithms, caching, queries)
- Breaking changes (API modifications, signature changes)

**Load for**: Analyzing change intent and summarizing modifications

---

## Typical Usage Pattern

```markdown
# Standard git diff analysis workflow

1. Load git_diff_reference.md
   - Understand diff format
   - Reference special cases
   
2. Parse diff using format knowledge
   - Extract hunks
   - Identify file operations
   - Calculate statistics
   
3. Load diff_patterns.md
   - Classify change types
   - Match patterns
   - Identify risks
   
4. Generate analysis
   - Summarize by pattern
   - Highlight important changes
   - Flag potential issues
```

## Quick Reference

| Task | File to Load | Section |
|------|--------------|---------|
| Parse diff syntax | `git_diff_reference.md` | "Unified Diff Format" |
| Handle renames | `git_diff_reference.md` | "Rename Detection" |
| Identify feature | `diff_patterns.md` | "Feature Addition" |
| Spot security fix | `diff_patterns.md` | "Security Fix" |
| Detect refactoring | `diff_patterns.md` | "Refactoring" |
| Find breaking change | `diff_patterns.md` | "Breaking Change" |

## Related Skills

- **get-git-diff**: Primary consumer of these context files
- **python-code-review**: Uses git diff output for targeted review

## Maintenance Notes

- `git_diff_reference.md`: Update when git diff format changes (rare)
- `diff_patterns.md`: Add new patterns as common change types emerge
