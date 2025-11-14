# Git Diff Reference Guide

This file provides comprehensive reference information about git diff formats, commands, and best practices for diff analysis.

---

## Unified Diff Format

The unified diff format is the standard output format for `git diff`. Understanding this format is essential for accurate diff analysis.

### Basic Structure

```diff
diff --git a/path/to/file.py b/path/to/file.py
index abc123..def456 100644
--- a/path/to/file.py
+++ b/path/to/file.py
@@ -10,7 +10,8 @@ def my_function():
     # This line is unchanged (context)
     old_line = "removed"
-    this_line_was_removed = True
+    this_line_was_added = True
+    another_added_line = "new"
     # More context
```

### Header Components

1. **Diff Header**:
   ```diff
   diff --git a/old_path b/new_path
   ```
   - Shows the file being compared
   - `a/` prefix = old version
   - `b/` prefix = new version

2. **Index Line**:
   ```diff
   index abc123..def456 100644
   ```
   - `abc123` = old blob hash
   - `def456` = new blob hash
   - `100644` = file mode (regular file, permissions)

3. **File Path Markers**:
   ```diff
   --- a/path/to/file.py
   +++ b/path/to/file.py
   ```
   - `---` indicates the old version path
   - `+++` indicates the new version path

### Hunk Headers

```diff
@@ -10,7 +10,8 @@ def my_function():
```

Format: `@@ -old_start,old_count +new_start,new_count @@ context`

- `-10,7` = In old file, starting at line 10, showing 7 lines
- `+10,8` = In new file, starting at line 10, showing 8 lines
- `def my_function():` = Context (function/class name)

### Line Prefixes

- ` ` (space) = Unchanged line (context)
- `-` (minus) = Line removed from old version
- `+` (plus) = Line added to new version
- `\` (backslash) = Special case (e.g., "No newline at end of file")

---

## Special Diff Cases

### File Operations

#### New File
```diff
diff --git a/new_file.py b/new_file.py
new file mode 100644
index 0000000..abc123
--- /dev/null
+++ b/new_file.py
@@ -0,0 +1,10 @@
+def new_function():
+    pass
```

#### Deleted File
```diff
diff --git a/old_file.py b/old_file.py
deleted file mode 100644
index abc123..0000000
--- a/old_file.py
+++ /dev/null
@@ -1,10 +0,0 @@
-def old_function():
-    pass
```

#### Renamed File (No Changes)
```diff
diff --git a/old_name.py b/new_name.py
similarity index 100%
rename from old_name.py
rename to new_name.py
```

#### Renamed File (With Changes)
```diff
diff --git a/old_name.py b/new_name.py
similarity index 87%
rename from old_name.py
rename to new_name.py
index abc123..def456 100644
--- a/old_name.py
+++ b/new_name.py
@@ -5,3 +5,4 @@ def function():
     line1 = "same"
-    old_line = "removed"
+    new_line = "added"
```

#### Mode Change
```diff
diff --git a/script.sh b/script.sh
old mode 100644
new mode 100755
```

### Binary Files
```diff
diff --git a/image.png b/image.png
index abc123..def456 100644
Binary files a/image.png and b/image.png differ
```

---

## Git Diff Command Options

### Basic Comparison Commands

```bash
# Compare two commits
git diff commit1 commit2
git diff commit1..commit2         # Same as above
git diff commit1...commit2        # Common ancestor to commit2

# Compare branches
git diff branch1 branch2
git diff main...feature-branch    # Changes in feature-branch since diverging

# Compare working directory
git diff                          # Unstaged changes
git diff --staged                 # Staged changes
git diff HEAD                     # All uncommitted changes
```

### Useful Options

```bash
# Statistics
git diff --stat                   # File change summary
git diff --numstat                # Numeric format
git diff --shortstat              # Brief summary

# File operations
git diff --name-only              # List changed files
git diff --name-status            # List with operation (A/M/D/R)
git diff -M                       # Detect renames (default 50% similarity)
git diff -M90%                    # Detect renames (90% similarity threshold)
git diff -C                       # Detect copies

# Context control
git diff -U3                      # Show 3 context lines (default)
git diff -U0                      # No context lines
git diff -U10                     # Show 10 context lines

# Filtering
git diff -- path/to/file          # Specific file
git diff -- '*.py'                # All Python files
git diff --diff-filter=A          # Only added files
git diff --diff-filter=M          # Only modified files
git diff --diff-filter=D          # Only deleted files
git diff --diff-filter=R          # Only renamed files

# Output format
git diff --word-diff              # Word-level diff
git diff --color-words            # Colored word diff
git diff --no-color               # Disable color output
git diff --patch                  # Show patches (default)
```

### Advanced Options

```bash
# Merge commits
git diff commit^1 commit          # Diff against first parent
git diff commit^2 commit          # Diff against second parent

# Ignore whitespace
git diff -w                       # Ignore whitespace changes
git diff --ignore-all-space       # Ignore all whitespace
git diff --ignore-blank-lines     # Ignore blank line changes

# Performance
git diff --histogram              # Use histogram diff algorithm
git diff --minimal                # Try harder to find smaller diff

# Function context
git diff --function-context       # Show entire function where change occurred
git diff -W                       # Short for --function-context
```

---

## Diff Statistics Interpretation

### `--stat` Output
```
 path/to/file1.py  |  45 +++++++++++------
 path/to/file2.py  | 123 +++++++++++++++++++++++++++++++++++++++++
 path/to/file3.py  |  12 ----
 3 files changed, 165 insertions(+), 20 deletions(-)
```

Reading this:
- `file1.py`: 45 lines changed (mix of additions and deletions)
- `file2.py`: 123 lines added
- `file3.py`: 12 lines deleted
- Summary: 3 files, 165 additions, 20 deletions

### `--numstat` Output
```
45  20  path/to/file1.py
123 0   path/to/file2.py
0   12  path/to/file3.py
```

Format: `additions deletions filename`
- Easier to parse programmatically
- Numbers are exact, not scaled like in `--stat`

### `--shortstat` Output
```
3 files changed, 165 insertions(+), 20 deletions(-)
```

Just the summary line, no per-file breakdown.

---

## Diff Filters

Use with `--diff-filter=` option:

- **A** = Added
- **C** = Copied
- **D** = Deleted
- **M** = Modified
- **R** = Renamed
- **T** = Type changed (file/symlink/submodule)
- **U** = Unmerged
- **X** = Unknown
- **B** = Broken pairing

Can combine: `--diff-filter=AM` (added or modified)
Can negate: `--diff-filter=d` (lowercase = exclude deleted)

---

## Reading Context Lines

Context lines help understand the location of changes:

```diff
@@ -42,7 +42,8 @@ class UserManager:
     def authenticate(self, username, password):
         """Authenticate a user."""
         user = self.get_user(username)
-        if user.check_password(password):
+        hashed = hash_password(password)
+        if user.password_hash == hashed:
             return user
         return None
```

The `class UserManager:` in the hunk header tells you the change is inside this class.

---

## Common Diff Patterns

### Refactoring
- High rename count (`R` in `--name-status`)
- Similar content in renamed files (high similarity %)
- Import statement updates
- Relative path changes

### Bug Fix
- Small number of changed lines
- Typically in single function/method
- Often adds error handling or edge case logic
- May include test additions

### Feature Addition
- Multiple new files (`A` in `--name-status`)
- Significant insertions (high `+` count)
- New test files
- Documentation updates

### Dependency Update
- Changes in `requirements.txt`, `package.json`, etc.
- Potential API usage changes throughout codebase
- Lock file updates

### Security Fix
- Authentication/authorization code changes
- Input validation additions
- Crypto/hashing changes
- Sensitive data handling modifications

---

## Best Practices for Diff Analysis

### 1. Start with Statistics
Always run `git diff --stat` first to get overview:
- How many files changed?
- How extensive are the changes?
- What types of files are affected?

### 2. Check File Operations
Run `git diff --name-status` to see operations:
- New files indicate feature addition
- Deleted files indicate cleanup or deprecation
- Renamed files indicate refactoring

### 3. Look for Patterns
- All changes in tests/* = test updates
- Changes in migrations/* = database schema changes
- Changes in config files = configuration updates
- Changes in docs/* = documentation updates

### 4. Identify Risk Areas
High-risk changes:
- Authentication/authorization code
- Database queries (SQL injection risk)
- Input validation
- API contracts (breaking changes)
- Configuration files (environment-specific)

### 5. Consider Context
- Is this a merge commit? (multiple parents)
- Is this a revert? (check commit message)
- Is this a squash commit? (many changes at once)
- Is this part of a larger feature? (related commits)

### 6. Validate Assumptions
- Ensure commits exist before running diff
- Check if branches are up to date
- Verify you're comparing the right refs
- Consider the direction of comparison (A to B vs B to A)

---

## Troubleshooting Common Issues

### "fatal: ambiguous argument"
- Commit hash doesn't exist
- Branch name doesn't exist
- Solution: `git rev-parse [ref]` to validate

### "Binary files differ"
- Diff can't show text comparison
- Solution: Use external tools or `git show commit:path`

### "No differences found"
- Comparing identical commits
- Wrong comparison direction
- Solution: Double-check commit refs

### Diff too large
- Thousands of lines changed
- Solution: Use `--stat` only, or filter by path

### Renames not detected
- Files changed too much (< 50% similar)
- Solution: Lower threshold with `-M40%`

---

## Git Diff Algorithms

Git supports different diff algorithms:

1. **Myers** (default): Fast, good for most cases
2. **Minimal**: Tries to find smallest diff (slower)
3. **Patience**: Better for code with many short lines
4. **Histogram**: Fast variant of patience (recommended for code)

Usage: `git diff --histogram` or `git diff --patience`

---

## Useful Git Diff Aliases

Add to `.gitconfig`:

```ini
[alias]
  # Quick stats
  ds = diff --stat

  # File list only
  dl = diff --name-only

  # File list with status
  dls = diff --name-status

  # Word diff for prose
  dw = diff --word-diff

  # Rename-aware diff
  dr = diff -M

  # Ignore whitespace
  dws = diff -w

  # Staged changes
  dstaged = diff --staged

  # Show function context
  df = diff -W
```

---

## References

- **Official Git Diff Documentation**: https://git-scm.com/docs/git-diff
- **Diff Format Specification**: https://git-scm.com/docs/diff-format
- **Pro Git Book - Chapter 7.1**: https://git-scm.com/book/en/v2/Git-Tools-Revision-Selection
- **Git Diff Algorithms**: https://luppeng.wordpress.com/2020/10/10/when-to-use-each-of-the-git-diff-algorithms/

---

## Quick Reference Card

```bash
# Basic comparisons
git diff commit1 commit2           # Compare two commits
git diff branch1...branch2         # Compare branch tips from common ancestor
git diff HEAD                      # Uncommitted changes

# Statistics
git diff --stat                    # Summary with bar graph
git diff --numstat                 # Numeric summary
git diff --shortstat               # One-line summary

# File operations
git diff --name-status             # List files with A/M/D/R status
git diff -M                        # Detect renames

# Filtering
git diff -- path/to/file           # Specific file
git diff --diff-filter=A           # Only added files

# Output control
git diff -U0                       # No context
git diff --word-diff               # Word-level diff
git diff -w                        # Ignore whitespace

# Advanced
git diff commit^1 commit           # Merge commit against parent 1
git diff --histogram               # Use histogram algorithm
```
