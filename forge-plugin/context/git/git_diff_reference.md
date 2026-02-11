---
id: "git/git_diff_reference"
domain: git
title: "Git Diff Reference - Quick Links"
type: reference
estimatedTokens: 150
loadingStrategy: onDemand
version: "0.1.0-alpha"
lastUpdated: "2026-02-10"
sections:
  - name: "Diff Format & Syntax"
    estimatedTokens: 50
    keywords: [unified-diff, format, headers, hunks]
  - name: "Status Codes"
    estimatedTokens: 30
    keywords: [added, modified, deleted, renamed, copied]
  - name: "Special Cases"
    estimatedTokens: 40
    keywords: [binary, rename, merge, large-diff]
tags: [git, diff, format, reference]
crossDomainTriggers: []
---

# Git Diff Reference – Quick Links

Minimal reference for where to look up git diff format and commands. Use external docs for details.

**Load this file** when parsing or explaining git diff output.

---

## 1. Diff Format & Syntax

- Unified diff format overview:  
  https://git-scm.com/docs/diff-format
- Git diff command reference:  
  https://git-scm.com/docs/git-diff
- Pro Git – diff & revision selection:  
  https://git-scm.com/book/en/v2/Git-Tools-Diffing

What to remember:
- `diff --git a/path b/path`: file header
- `@@ -old_start,old_count +new_start,new_count @@ context`: hunk header
- Line prefixes: space = context, `-` = removed, `+` = added.

---

## 2. File Operations & Status Codes

- Official status/diff filters:  
  https://git-scm.com/docs/git-diff#_other_diff_formats

Key reminders:
- Status codes: `A` (added), `M` (modified), `D` (deleted), `R` (renamed), `C` (copied), `U` (unmerged).
- New/deleted files use `/dev/null` in diff headers.
- Binary files show `Binary files a/... b/... differ`.

---

## 3. Common Usage Patterns

Look up exact flags in the git diff docs, but typical tasks map to:

| Task | Concept | Docs |
|------|---------|------|
| Compare commits/branches | `git diff <a> <b>` / `a...b` | https://git-scm.com/docs/git-diff#_examples |
| See per‑file stats | `--stat`, `--numstat`, `--shortstat` | https://git-scm.com/docs/git-diff#_other_diff_formats |
| List file names + status | `--name-only`, `--name-status` | https://git-scm.com/docs/git-diff#_other_diff_formats |
| Detect renames/copies | `-M`, `-C` | https://git-scm.com/docs/git-diff#_detect_renames |
| Ignore whitespace | `-w`, `--ignore-all-space`, `--ignore-blank-lines` | https://git-scm.com/docs/git-diff#_generating_patches_with_p |

---

## 4. Algorithms & Large Diffs

- Diff algorithms:  
  https://git-scm.com/docs/git-diff#_generating_patches_with_p  
  (see `--histogram`, `--patience`, `--minimal`)

Use cases (remember, look up syntax in docs):
- `--histogram`: often better for code.
- `--patience`: when diffs are noisy.
- `--minimal`: smallest diff, may be slower.

---

## 5. Helpful References

- Git diff main docs: https://git-scm.com/docs/git-diff
- Diff format: https://git-scm.com/docs/diff-format
- Pro Git (Diffing): https://git-scm.com/book/en/v2/Git-Tools-Diffing

---

**Version**: 0.1.0-alpha (Compact Reference Format)
**Last Updated**: 2025-11-14
**Maintained For**: get-git-diff skill
