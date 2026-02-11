---
name: get-git-diff
description: Examines git diffs between commits or branches with intelligent analysis. Provides unified diff format with comprehensive summaries including file statistics, rename detection, and merge commit handling. Outputs formatted diffs to /claudedocs for documentation and review purposes.
---

# Git Diff Analyzer

## � MANDATORY COMPLIANCE �

**CRITICAL**: The 4-step workflow outlined in this document MUST be followed in exact order for EVERY diff analysis. Skipping steps or deviating from the procedure will result in incomplete analysis. This is non-negotiable.

## File Structure

- **SKILL.md** (this file): Main instructions and MANDATORY workflow
- **examples.md**: Usage scenarios with different diff types
- **Context**: Git domain context loaded via `contextProvider.getDomainIndex("git")`. See [ContextProvider Interface](../../interfaces/context_provider.md).
  - `git_diff_reference.md`: Unified diff format reference and best practices
  - `diff_patterns.md`: Common patterns to identify in code changes
- **Memory**: Project-specific memory accessed via `memoryStore.getSkillMemory("get-git-diff", "{project-name}")`. See [MemoryStore Interface](../../interfaces/memory_store.md).
- **scripts/**:
  - `README.md`: Complete documentation for all helper scripts
  - `validate.sh`: Git repository and commit validation functions
  - `commit_info.sh`: Commit metadata retrieval (hash, author, date, message)
  - `diff_stats.sh`: Diff statistics and line count analysis
  - `file_operations.sh`: File operation detection (add, modify, delete, rename)
  - `utils.sh`: General utilities (branch detection, formatting, repo info)
- **templates/**:
  - `output_template.md`: Standard output format template

## Analysis Focus Areas

Git diff analysis evaluates 7 critical dimensions:

1. **Change Scope**: Files affected, lines modified, overall impact radius
2. **Change Type**: Feature addition, bug fix, refactoring, configuration change
3. **Structural Changes**: File renames, moves, deletions, additions
4. **Risk Assessment**: Breaking changes, API modifications, database migrations
5. **Code Quality Impact**: Complexity changes, test coverage changes
6. **Merge Conflicts**: Merge commit analysis, conflict resolution patterns
7. **Performance Impact**: Algorithm changes, database query modifications, resource usage

**Note**: Analysis depth is summary-level, focusing on what changed and high-level impact.

---

## MANDATORY WORKFLOW (MUST FOLLOW EXACTLY)

### � STEP 1: Commit Identification (REQUIRED)

**YOU MUST:**
1. Check if commit hashes/branch names were provided in the triggering prompt
2. If NOT provided, ask the user with these options:
   - **Option A**: Compare specific commit hashes (ask for two commit SHAs)
   - **Option B**: Compare HEAD of current branch to main/master
   - **Option C**: Compare two branch names
   - **Option D**: Compare current changes to a specific commit
3. Validate that provided commits/branches exist in the repository
4. Use `git rev-parse` to verify and get full commit hashes
5. Get commit metadata (author, date, message) for both commits

**DO NOT PROCEED WITHOUT VALID COMMITS**

### ⚠️ STEP 2: Load Context & Memory, Then Execute Git Diff (REQUIRED)

**FIRST: Load indexes and memory to understand available resources**
1. **Load domain index**: Use `contextProvider.getDomainIndex("git")` to discover available git context files
2. **Load skill memory**: Use `memoryStore.getSkillMemory("get-git-diff", "{project-name}")` to load project-specific patterns
   - If memory exists: Review project patterns from previous analyses
   - If not: Note this is first analysis of this project

**THEN: Execute git diff with special handling**
1. Execute `git diff [commit1]...[commit2]` to get the unified diff
2. Check for and handle special cases:
   - **Large diffs** (>1000 lines): Warn user, offer to summarize only or proceed
   - **Renamed files**: Use `git diff -M` to detect renames
   - **Merge commits**: Use `git diff [commit]^...[commit]` for merge commit analysis
   - **Binary files**: Note binary file changes separately
3. Get diff statistics with `git diff --stat`
4. Get file list with `git diff --name-status` to identify A/M/D/R operations

**DO NOT SKIP SPECIAL CASE DETECTION**

### � STEP 3: Analyze and Summarize (REQUIRED)

**FIRST: Load relevant context files (use indexes from Step 2 for guidance)**
1. **Load context**: Use `contextProvider.getConditionalContext("git", detection)` to load relevant context files (`git_diff_reference.md`, `diff_patterns.md`)

**THEN: Analyze and document**:
1. **Commit Metadata**:
   - Commit hashes (full and short)
   - Author and date for both commits
   - Commit messages
   - Number of commits between the two refs (if applicable)

2. **Change Statistics**:
   - Total files changed
   - Total insertions (+)
   - Total deletions (-)
   - Net change

3. **File Operations**:
   - Added files (A)
   - Modified files (M)
   - Deleted files (D)
   - Renamed files (R) - show old vs new
   - Copied files (C)

4. **Change Categorization**:
   - Group files by type (source code, tests, docs, config)
   - Identify potential areas of impact
   - Flag potentially risky changes

5. **Special Notes**:
   - Merge commit indicator (if applicable)
   - Large diff warning (if >1000 lines)
   - Binary file changes
   - Submodule changes

**DO NOT SKIP ANALYSIS**

### � STEP 4: Generate Output & Update Project Memory (REQUIRED)

**YOU MUST:**
1. Use the template from `templates/output_template.md`
2. Create filename: `diff_{short_hash1}_{short_hash2}.md`
3. Include all components:
   - Header with commit information
   - Summary section with all statistics and analysis
   - Full unified diff wrapped in markdown code blocks
4. Save to `/claudedocs/` directory
5. Confirm file was written successfully

**Output Format Requirements**:
- Unified diff must be in triple-backtick code blocks with `diff` language tag
- Summary must be in clear markdown sections
- File paths must use code formatting
- Statistics must be in tables or lists
- All sections must be clearly labeled

**DO NOT OMIT ANY REQUIRED SECTIONS**

**OPTIONAL: Update Project Memory**

If patterns emerge during analysis, consider storing insights via `memoryStore.update("get-git-diff", "{project-name}", ...)`:
- Common file change patterns
- Frequently modified areas
- Notable commit patterns or conventions

---

## Special Case Handling

### Large Diffs (>1000 lines)

When encountering large diffs:
1. Calculate total line count
2. Warn user: "This diff contains [N] lines across [M] files"
3. Ask user: "Would you like to proceed with full diff or summary only?"
4. If summary only:
   - Include all metadata and statistics
   - List all changed files with their line counts
   - Omit the detailed unified diff
   - Note: "Full diff omitted due to size. Use `git diff [hash1]...[hash2]` to view."

### Renamed/Moved Files

For file renames:
1. Use `git diff -M` flag to detect renames (default similarity index: 50%)
2. In summary, clearly show: `old/path/file.py � new/path/file.py`
3. Indicate if content was also modified: `R+M` (renamed and modified)
4. In unified diff, show rename header: `rename from/to`

### Merge Commits

For merge commits:
1. Detect with `git rev-list --merges`
2. Note in summary: "This is a merge commit"
3. Show both parent commits
4. Use `git diff [commit]^...[commit]` to show changes introduced by merge
5. Optionally offer to show diff against each parent separately

---

## Compliance Checklist

Before completing ANY diff analysis, verify:
- [ ] Step 1: Commits identified and validated
- [ ] Step 2: Git diff executed with special case detection
- [ ] Step 3: Complete analysis with all statistics and categorization
- [ ] Step 4: Output generated in correct format and saved to /claudedocs

**FAILURE TO COMPLETE ALL STEPS INVALIDATES THE ANALYSIS**

---

## Output File Naming Convention

**Format**: `diff_{short1}_{short2}.md`

Where:
- `{short1}` = First 7 characters of first commit hash
- `{short2}` = First 7 characters of second commit hash

**Examples**:
- `diff_a1b2c3d_e4f5g6h.md` (commit to commit)
- `diff_main_feature-branch.md` (branch comparison, if hashes not available)

**Alternative for branches**: If comparing branch tips, you may use branch names if they're short and filesystem-safe.

---

## Git Commands Reference

### Core Commands Used:
```bash
# Get commit info
git rev-parse [commit]
git log -1 --format="%H|%h|%an|%ae|%ad|%s" [commit]

# Generate diff
git diff [commit1]...[commit2]
git diff --stat [commit1]...[commit2]
git diff --name-status [commit1]...[commit2]
git diff -M [commit1]...[commit2]  # Detect renames

# Special cases
git rev-list --merges [commit]  # Check if merge commit
git diff [commit]^1..[commit]   # Merge commit against first parent
```

---

## Further Reading

Refer to official documentation:
- **Git Documentation**:
  - Git Diff: https://git-scm.com/docs/git-diff
  - Diff Format: https://git-scm.com/docs/diff-format
- **Best Practices**:
  - Pro Git Book: https://git-scm.com/book/en/v2
  - Understanding Git Diff: https://git-scm.com/docs/git-diff#_generating_patches_with_p

---

## Version History

- v1.2.0 (2026-02-10): Migrated to interface-based context and memory access
  - Replaced hardcoded context paths with ContextProvider interface calls
  - Replaced hardcoded memory paths with MemoryStore interface calls
  - Added references to interface documentation
- v1.1.0 (2025-01-XX): Centralized context and project memory
  - Context files moved to shared git domain context
  - Project-specific memory system added for get-git-diff skill
  - Optional memory updates for common patterns
- v1.0.0 (2025-11-13): Initial release
  - Mandatory 4-step workflow
  - Summary-level analysis with statistics
  - Special handling for large diffs, renames, and merge commits
  - Unified diff output to /claudedocs
