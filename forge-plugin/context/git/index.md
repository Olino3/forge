# Git Context Files (Compact)

Compact, link‑heavy context for git diff analysis, version control patterns, and commit analysis.

## Files in this Directory

### `git_diff_reference.md`

- **Purpose**: Minimal reminders + links for unified diff format and `git diff` usage.
- **Use when**:
  - Parsing diff output.
  - Explaining diff syntax or status codes.
  - Handling renames, binary files, or large diffs.
- **Contents**: Pointers to official Git docs and Pro Git sections; no command cheatsheet.
- **Load for**: Every `skill:get-git-diff` invocation that needs to interpret raw diff text.

---

### `diff_patterns.md`

- **Purpose**: Compact patterns to classify change types and spot risk in diffs.
- **Use when**:
  - Inferring change intent (feature, bugfix, refactor, etc.).
  - Highlighting risky areas (security, DB, breaking changes).
  - Providing a short checklist for diff review.
- **Contents**: Small tables of patterns/red flags and links to code review, SemVer, OWASP, etc.
- **Load for**: Summarizing modifications and reasoning about risk level.

---

## Typical Usage Pattern

1. Load `git_diff_reference.md` for structure and links if you need to interpret diff syntax.
2. Parse and summarize the diff in code.
3. Load `diff_patterns.md` to classify the changes and spot red flags.
4. Generate the final summary and risk notes.

## Quick Reference

| Task | File to Load |
|------|--------------|
| Understand diff syntax/headers | `git_diff_reference.md` |
| Classify change type | `diff_patterns.md` |
| Spot security / breaking change risk | `diff_patterns.md` |

## Related Skills

- **get-git-diff**: Primary consumer of these context files.
- **python-code-review**: Uses git diff output for targeted review.

## Maintenance Notes

- `git_diff_reference.md`: Only update links or high‑level notes when Git docs move or change.
- `diff_patterns.md`: Extend pattern tables if new common change types emerge.
