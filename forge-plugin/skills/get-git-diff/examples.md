# Git Diff Analyzer Examples

This file contains example scenarios demonstrating how to use the get-git-diff skill for various diff analysis tasks.

---

## Example 1: Comparing Two Specific Commits

### Scenario
Developer wants to see what changed between two feature commits.

### User Prompt
```
I need to see the diff between commits a1b2c3d and e4f5g6h
```

### Skill Execution

**Step 1 - Commit Identification**:
- Commits provided: `a1b2c3d` and `e4f5g6h`
- Validate: `git rev-parse a1b2c3d e4f5g6h`
- Get metadata: `git log -1 --format="%H|%h|%an|%ae|%ad|%s" [commit]`

**Step 2 - Execute Diff**:
```bash
git diff a1b2c3d...e4f5g6h
git diff --stat a1b2c3d...e4f5g6h
git diff --name-status a1b2c3d...e4f5g6h
```

**Step 3 - Analysis**:
```
Commit Metadata:
- From: a1b2c3d (John Doe, 2025-11-01, "Add user authentication")
- To: e4f5g6h (Jane Smith, 2025-11-13, "Refactor auth module")
- Commits between: 15

Statistics:
- Files changed: 8
- Insertions: 234
- Deletions: 156
- Net change: +78

File Operations:
- Modified: src/auth/login.py, src/auth/session.py, tests/test_auth.py
- Added: src/auth/jwt_handler.py, src/auth/validators.py
- Deleted: src/auth/legacy_auth.py
```

**Step 4 - Output**:
File: `/claudedocs/diff_a1b2c3d_e4f5g6h.md`

---

## Example 2: Comparing Current Branch to Main

### Scenario
Developer wants to review all changes in feature branch before creating a PR.

### User Prompt
```
Show me the diff for my feature branch compared to main
```

### Skill Response
Since no specific commits provided, ask user:
- Option A: Compare specific commit hashes
- Option B: Compare HEAD of current branch to main ← **User selects this**
- Option C: Compare two branch names
- Option D: Compare current changes to a specific commit

**Step 1 - Commit Identification**:
```bash
# Get current branch
git rev-parse --abbrev-ref HEAD  # Returns: feature/new-api

# Get commit hashes
git rev-parse main              # Returns: d7e8f9a...
git rev-parse HEAD              # Returns: m3n4o5p...
```

**Step 2 - Execute Diff**:
```bash
git diff main...HEAD
git diff --stat main...HEAD
git diff --name-status main...HEAD
```

**Step 3 - Analysis**:
```
Comparing: main (d7e8f9a) → feature/new-api (m3n4o5p)

Statistics:
- Files changed: 12
- Insertions: 567
- Deletions: 89
- Net change: +478

File Operations:
- Added: src/api/v2/endpoints.py, src/api/v2/schemas.py, tests/api/test_v2.py
- Modified: src/api/router.py, src/main.py, README.md
- Deleted: (none)

Change Categorization:
- Source code: 8 files (src/api/*, src/main.py)
- Tests: 3 files (tests/api/*)
- Documentation: 1 file (README.md)

Impact Areas:
- API routing layer
- Request/response schemas
- Test coverage
```

**Step 4 - Output**:
File: `/claudedocs/diff_d7e8f9a_m3n4o5p.md`

---

## Example 3: Large Diff Handling

### Scenario
Comparing two commits with extensive changes (e.g., major refactoring or dependency update).

### User Prompt
```
Compare commit abc1234 to def5678
```

**Step 2 - Execute Diff**:
```bash
git diff --stat abc1234...def5678
# Output shows: 87 files changed, 15234 insertions(+), 12456 deletions(-)
```

**Large Diff Detected**: Total lines = 27,690

**Skill Response**:
⚠️ **Large Diff Warning**

This diff contains 27,690 lines across 87 files. This is a substantial change set.

Would you like to:
- **Option A**: Proceed with full diff (will be very long)
- **Option B**: Summary only (statistics and file list, no line-by-line diff)

**User selects**: Option B - Summary only

**Step 3 - Analysis**:
```
Commit Metadata:
- From: abc1234 (Team Lead, 2025-10-15, "Update dependencies to Python 3.12")
- To: def5678 (Team Lead, 2025-11-13, "Complete Python 3.12 migration")

Statistics:
- Files changed: 87
- Insertions: 15,234
- Deletions: 12,456
- Net change: +2,778

Top Changed Files:
1. requirements.txt (+45, -32)
2. src/core/utils.py (+234, -189)
3. tests/test_compatibility.py (+456, -123)
... (84 more files)

Change Categorization:
- Dependency files: 3 files
- Source code: 62 files
- Tests: 18 files
- Documentation: 4 files

Impact Assessment:
⚠️ Major refactoring detected
⚠️ Breaking changes likely
⚠️ Extensive test updates
```

**Step 4 - Output**:
File: `/claudedocs/diff_abc1234_def5678.md`

**Note in output**: "Full unified diff omitted due to size (27,690 lines). Use `git diff abc1234...def5678` to view complete diff."

---

## Example 4: Renamed Files Detection

### Scenario
Developer refactored project structure, moving files to new directories.

### User Prompt
```
Show me what changed in the refactoring commit x9y8z7w
```

**Step 1 - Commit Identification**:
- Comparing: x9y8z7w^ (parent) → x9y8z7w (the refactoring commit)

**Step 2 - Execute Diff with Rename Detection**:
```bash
git diff -M x9y8z7w^...x9y8z7w
git diff --name-status -M x9y8z7w^...x9y8z7w
```

Output:
```
R100    src/utils.py → src/core/utils.py
R100    src/helpers.py → src/core/helpers.py
R085    src/auth.py → src/auth/main.py
M       src/main.py
A       src/core/__init__.py
```

**Step 3 - Analysis**:
```
Commit Metadata:
- Commit: x9y8z7w (Developer, 2025-11-12, "Refactor: reorganize project structure")

Statistics:
- Files changed: 6
- Insertions: 45
- Deletions: 12
- Net change: +33

File Operations:
- Renamed (no changes):
  • src/utils.py → src/core/utils.py
  • src/helpers.py → src/core/helpers.py

- Renamed + Modified (85% similarity):
  • src/auth.py → src/auth/main.py

- Modified:
  • src/main.py (updated imports)

- Added:
  • src/core/__init__.py (new package init)

Change Type: Refactoring
Risk Assessment: Medium (import paths changed, may break external references)
```

**Step 4 - Output**:
File: `/claudedocs/diff_w6v5u4t_x9y8z7w.md`

---

## Example 5: Merge Commit Analysis

### Scenario
Developer wants to understand what a merge commit introduced.

### User Prompt
```
Analyze the merge commit m1e2r3g4
```

**Step 1 - Commit Identification**:
```bash
git rev-list --merges m1e2r3g4^..m1e2r3g4
# Confirms: m1e2r3g4 is a merge commit

git log -1 --format="%P" m1e2r3g4
# Returns: a1b2c3d e4f5g6h (two parents)
```

**Skill Response**:
⚠️ **Merge Commit Detected**

This is a merge commit with two parents:
- Parent 1: a1b2c3d (main branch)
- Parent 2: e4f5g6h (feature branch)

**Step 2 - Execute Diff**:
```bash
# Show changes introduced by the merge (against first parent)
git diff m1e2r3g4^1...m1e2r3g4
git diff --stat m1e2r3g4^1...m1e2r3g4
```

**Step 3 - Analysis**:
```
Merge Commit Metadata:
- Commit: m1e2r3g4
- Author: John Doe
- Date: 2025-11-13
- Message: "Merge feature/user-profiles into main"
- Parent 1 (base): a1b2c3d (main)
- Parent 2 (merged): e4f5g6h (feature/user-profiles)

Statistics:
- Files changed: 15
- Insertions: 892
- Deletions: 134
- Net change: +758

Merged Branch Summary:
- Branch: feature/user-profiles
- Commits merged: 23
- Primary changes:
  • New user profile management system
  • Profile API endpoints
  • Profile database models
  • Associated tests

Change Categorization:
- Source code: 9 files (src/profiles/*, src/api/profiles.py)
- Database: 2 files (migrations/*, models/profile.py)
- Tests: 3 files (tests/profiles/*)
- Documentation: 1 file (docs/api.md)

Merge Notes:
✓ No merge conflicts (clean merge)
✓ All tests passing (based on commit message)
```

**Step 4 - Output**:
File: `/claudedocs/diff_a1b2c3d_m1e2r3g4.md`

Special note in file: "This is a merge commit analysis showing changes introduced by merging feature/user-profiles into main."

---

## Example 6: Comparing Branches by Name

### Scenario
Developer wants to see differences between two branches without knowing commit hashes.

### User Prompt
```
Compare the staging branch to the production branch
```

**Skill Response**:
No specific commits provided. Asking user for comparison target...

User selects: **Option C - Compare two branch names**

Please provide:
- First branch: **production**
- Second branch: **staging**

**Step 1 - Commit Identification**:
```bash
git rev-parse production  # Returns: p1r2o3d...
git rev-parse staging     # Returns: s4t5a6g...

git log --oneline production..staging
# Shows: 8 commits ahead
```

**Step 3 - Analysis**:
```
Comparing Branches:
- production (p1r2o3d): "Release v2.1.0" (2025-11-01)
- staging (s4t5a6g): "Add feature X" (2025-11-13)
- Commits ahead: 8
- Commits behind: 0

Statistics:
- Files changed: 24
- Insertions: 1,234
- Deletions: 456
- Net change: +778

File Operations:
- Added: 8 files (new features)
- Modified: 14 files (enhancements)
- Deleted: 2 files (deprecated code)

Impact Assessment:
✓ Ready for production deployment
✓ All features tested in staging
⚠️ Database migration required (see migrations/0023_add_feature_x.py)
```

**Step 4 - Output**:
File: `/claudedocs/diff_p1r2o3d_s4t5a6g.md`

---

## Example 7: Current Working Directory Changes

### Scenario
Developer has uncommitted changes and wants to see diff against last commit.

### User Prompt
```
Show me my current uncommitted changes
```

**Skill Response**:
No specific commits provided. Asking user...

User selects: **Option D - Compare current changes to a specific commit**

Please provide the commit to compare against (or press Enter for HEAD): **[User presses Enter]**

**Step 1 - Commit Identification**:
```bash
# Comparing working directory against HEAD
git rev-parse HEAD  # Returns: h3e4a5d...
```

**Step 2 - Execute Diff**:
```bash
git diff HEAD
git diff --stat HEAD
git diff --name-status HEAD
```

**Step 3 - Analysis**:
```
Working Directory Changes:
- Base commit: h3e4a5d (HEAD, "Latest commit")
- Status: Uncommitted changes

Statistics:
- Files changed: 3
- Insertions: 67
- Deletions: 23
- Net change: +44

File Operations:
- Modified:
  • src/api/endpoints.py (+45, -12)
  • tests/test_api.py (+18, -8)
  • README.md (+4, -3)

Change Type: Feature development (in progress)
Status: ⚠️ Uncommitted - not yet in version control
```

**Step 4 - Output**:
File: `/claudedocs/diff_h3e4a5d_working.md`

---

## Example 8: Binary Files in Diff

### Scenario
Diff includes binary file changes (images, PDFs, compiled files).

### User Prompt
```
Compare commit old123 to new456
```

**Step 2 - Execute Diff**:
```bash
git diff --stat old123...new456
git diff --name-status old123...new456
```

Output includes:
```
M   docs/architecture.pdf
M   static/images/logo.png
A   static/images/hero.jpg
```

**Step 3 - Analysis**:
```
Statistics:
- Files changed: 15
- Text files: 12 (analyzed in diff)
- Binary files: 3 (listed separately)

Text File Changes:
- Insertions: 234
- Deletions: 156
- Net change: +78

Binary File Changes:
- Modified:
  • docs/architecture.pdf (binary file changed)
  • static/images/logo.png (binary file changed)
- Added:
  • static/images/hero.jpg (new binary file)

Note: Binary file content changes not shown in diff.
Use `git show old123:path` and `git show new456:path` to extract binary files.
```

**Step 4 - Output**:
File includes note: "⚠️ This diff contains 3 binary files. Binary content not displayed. See summary for list of affected binary files."

---

## Summary of Use Cases

1. **Two specific commits** - Direct comparison with full metadata
2. **Branch to main** - Pre-PR review workflow
3. **Large diffs** - Summary-only option for massive changes
4. **Renamed files** - Detect and document file restructuring
5. **Merge commits** - Special handling with parent information
6. **Branch comparison** - Compare branch tips by name
7. **Working directory** - Review uncommitted changes
8. **Binary files** - Special notation for non-text files

## Best Practices

- Always validate commits exist before running diff
- For large diffs, offer summary option first
- Clearly indicate merge commits with special notation
- Show both old and new paths for renamed files
- Categorize changes by file type and impact area
- Provide actionable insights in the summary
- Save output with descriptive filenames
- Include enough metadata for audit trail
