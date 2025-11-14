# Git Diff: [SHORT_HASH_1] → [SHORT_HASH_2]

**Generated**: [YYYY-MM-DD HH:MM:SS]
**Skill**: get-git-diff v1.0.0

---

## Commit Information

### From Commit
- **Hash**: `[FULL_HASH_1]` ([SHORT_HASH_1])
- **Author**: [AUTHOR_NAME] <[AUTHOR_EMAIL]>
- **Date**: [COMMIT_DATE_1]
- **Message**: [COMMIT_MESSAGE_1]

### To Commit
- **Hash**: `[FULL_HASH_2]` ([SHORT_HASH_2])
- **Author**: [AUTHOR_NAME] <[AUTHOR_EMAIL]>
- **Date**: [COMMIT_DATE_2]
- **Message**: [COMMIT_MESSAGE_2]

### Comparison Details
- **Commits Between**: [N] commits
- **Branch Context**: [BRANCH_INFO] (if applicable)
- **Merge Commit**: [Yes/No] (if applicable)

---

## Summary

### Change Statistics

| Metric | Count |
|--------|-------|
| Files Changed | [N] |
| Insertions | [N] (+) |
| Deletions | [N] (-) |
| Net Change | [±N] |

### File Operations

#### Added Files ([N])
[If any files were added, list them here]
- `path/to/new_file.py`
- `path/to/another_file.js`

#### Modified Files ([N])
[If any files were modified, list them here]
- `src/module.py` (+[N], -[N])
- `tests/test_module.py` (+[N], -[N])

#### Deleted Files ([N])
[If any files were deleted, list them here]
- `old/deprecated_file.py`

#### Renamed Files ([N])
[If any files were renamed, list them here]
- `old/path/file.py` → `new/path/file.py` ([SIMILARITY]%)

#### Binary Files ([N])
[If any binary files changed, list them here]
- `static/images/logo.png` (binary)
- `docs/manual.pdf` (binary)

---

## Change Categorization

### By File Type

| Category | Files | Insertions | Deletions |
|----------|-------|------------|-----------|
| Source Code | [N] | [N] | [N] |
| Tests | [N] | [N] | [N] |
| Documentation | [N] | [N] | [N] |
| Configuration | [N] | [N] | [N] |
| Database | [N] | [N] | [N] |
| Other | [N] | [N] | [N] |

### Change Type Assessment
[Based on patterns identified]
- **Primary Type**: [Feature Addition / Bug Fix / Refactoring / etc.]
- **Impact Areas**:
  - [Area 1 - e.g., Authentication system]
  - [Area 2 - e.g., User API endpoints]
  - [Area 3 - e.g., Test coverage]

### Risk Assessment
[Based on change patterns and areas affected]
- **Risk Level**: [Low / Medium / High / Critical]
- **Risk Factors**:
  - [Factor 1 - e.g., Database schema changes]
  - [Factor 2 - e.g., Breaking API changes]
  - [Factor 3 - e.g., Security-sensitive code modified]

---

## Special Notes

[Include any special considerations or warnings]

### Large Diff Warning
[If applicable]
⚠️ **This diff contains [N] lines across [M] files.** This is a substantial change set.
[If summary only: "Full unified diff omitted due to size. Use `git diff [hash1]...[hash2]` to view complete diff."]

### Merge Commit
[If applicable]
⚠️ **This is a merge commit** merging [BRANCH_NAME] into [BASE_BRANCH].
- Parent 1: [HASH] ([BRANCH])
- Parent 2: [HASH] ([BRANCH])

### Binary Changes
[If applicable]
⚠️ **This diff includes [N] binary files.** Binary content is not displayed in the diff below.

### Renamed Files
[If applicable]
ℹ️ **[N] files were renamed or moved.** Old and new paths are shown above with similarity percentages.

---

## Detailed Diff

[If full diff is included, otherwise note that it was omitted]

```diff
[FULL_UNIFIED_DIFF_OUTPUT]

Example format:
diff --git a/src/module.py b/src/module.py
index abc123..def456 100644
--- a/src/module.py
+++ b/src/module.py
@@ -10,7 +10,8 @@ def my_function():
     # Unchanged line
-    old_line = "removed"
+    new_line = "added"
+    another_line = "also added"
     # More context

diff --git a/tests/test_module.py b/tests/test_module.py
index 111222..333444 100644
--- a/tests/test_module.py
+++ b/tests/test_module.py
@@ -5,3 +5,6 @@ def test_my_function():
     assert my_function() is not None
+
+def test_new_behavior():
+    assert new_line == "added"
```

---

## Recommendations

[Optional section with actionable recommendations based on diff analysis]

### Testing
- [ ] Verify all tests pass with these changes
- [ ] Add tests for any new functionality
- [ ] Check test coverage for modified areas

### Code Review Focus
- [ ] Review [specific area] for correctness
- [ ] Validate [specific concern] is addressed
- [ ] Ensure backward compatibility for [specific component]

### Deployment Considerations
- [ ] Update environment variables if config changed
- [ ] Run database migrations if schema changed
- [ ] Update documentation if API changed
- [ ] Coordinate with [team] if [specific area] changed

---

## Related Commands

```bash
# View this diff locally
git diff [SHORT_HASH_1]...[SHORT_HASH_2]

# View with file names only
git diff --name-status [SHORT_HASH_1]...[SHORT_HASH_2]

# View with statistics
git diff --stat [SHORT_HASH_1]...[SHORT_HASH_2]

# View specific file from this diff
git diff [SHORT_HASH_1]...[SHORT_HASH_2] -- path/to/file

# View commit messages in range
git log --oneline [SHORT_HASH_1]..[SHORT_HASH_2]
```

---

## Metadata

- **Analyzed by**: Claude Code get-git-diff skill v1.0.0
- **Analysis date**: [YYYY-MM-DD HH:MM:SS]
- **Repository**: [REPO_PATH or REPO_URL if available]
- **Output format**: Standard Unified Diff with Summary

---

<!--
Template Usage Instructions:

Replace all placeholders in [BRACKETS] with actual values:
- [SHORT_HASH_1/2] - 7-character commit hash
- [FULL_HASH_1/2] - Full 40-character commit hash
- [AUTHOR_NAME] - Commit author name
- [AUTHOR_EMAIL] - Commit author email
- [COMMIT_DATE_1/2] - Commit date
- [COMMIT_MESSAGE_1/2] - Commit message (first line)
- [N] - Numeric values (file counts, line counts, etc.)
- [BRANCH_INFO] - Branch context information
- [SIMILARITY] - Similarity percentage for renames
- [FULL_UNIFIED_DIFF_OUTPUT] - Complete git diff output

Conditional Sections:
- Include "Large Diff Warning" only if diff > 1000 lines
- Include "Merge Commit" only if commit is a merge
- Include "Binary Changes" only if binary files present
- Include "Renamed Files" only if renames detected
- Omit empty categories (e.g., if no files deleted, omit that section)

Formatting:
- Use proper markdown syntax
- Wrap code/paths in backticks: `path/to/file`
- Use tables for structured data
- Use bullet lists for items
- Use checkboxes [ ] for action items
- Use emoji/symbols sparingly: ⚠️ for warnings, ℹ️ for info

Output Location:
- Save to: /claudedocs/diff_{short_hash1}_{short_hash2}.md
- Ensure /claudedocs directory exists
- Use filesystem-safe characters only
-->
