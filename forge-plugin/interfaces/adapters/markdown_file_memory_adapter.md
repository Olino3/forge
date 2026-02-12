# MarkdownFileMemoryAdapter

**Version**: 0.2.0-alpha
**Status**: Phase 1 - Interface Definition
**Implements**: `memory_store.md` (MemoryStore interface)

## Purpose

The MarkdownFileMemoryAdapter maps every MemoryStore method to concrete filesystem operations on markdown files. This is the default (and currently only) adapter for the Forge memory system. It documents how the MemoryStore interface translates to the existing `forge-plugin/memory/` directory structure, including path construction, timestamp management, auto-pruning, and staleness computation.

---

## Path Construction

All paths are relative to `forge-plugin/memory/`. The adapter constructs paths from the `layer`, `projectName`, `skillName`/`commandName`/`agentName`, and `fileType` fields of a `MemoryEntry`.

### Layer: `shared-project`

```
memory/projects/{projectName}/{fileType}.md
```

**Examples**:
| Entry Fields | Resolved Path |
|-------------|--------------|
| `projectName: "my-api"`, `fileType: "project_profile"` | `memory/projects/my-api/project_profile.md` |
| `projectName: "my-api"`, `fileType: "technology_stack"` | `memory/projects/my-api/technology_stack.md` |
| `projectName: "e-commerce"`, `fileType: "cross_skill_insights"` | `memory/projects/e-commerce/cross_skill_insights.md` |

### Layer: `skill-specific`

```
memory/skills/{skillName}/{projectName}/{fileType}.md
```

**Examples**:
| Entry Fields | Resolved Path |
|-------------|--------------|
| `skillName: "python-code-review"`, `projectName: "my-api"`, `fileType: "project_overview"` | `memory/skills/python-code-review/my-api/project_overview.md` |
| `skillName: "python-code-review"`, `projectName: "my-api"`, `fileType: "review_history"` | `memory/skills/python-code-review/my-api/review_history.md` |
| `skillName: "generate-python-unit-tests"`, `projectName: "my-api"`, `fileType: "testing_patterns"` | `memory/skills/generate-python-unit-tests/my-api/testing_patterns.md` |
| `skillName: "dotnet-code-review"`, `projectName: "e-commerce"`, `fileType: "known_issues"` | `memory/skills/dotnet-code-review/e-commerce/known_issues.md` |

### Layer: `command`

```
memory/commands/{projectName}/{fileType}.md
```

**Examples**:
| Entry Fields | Resolved Path |
|-------------|--------------|
| `projectName: "my-api"`, `fileType: "command_history"` | `memory/commands/my-api/command_history.md` |
| `projectName: "my-api"`, `fileType: "analyze_insights"` | `memory/commands/my-api/analyze_insights.md` |

### Layer: `agent`

```
memory/agents/{agentName}/{fileType}.md
```

**Examples**:
| Entry Fields | Resolved Path |
|-------------|--------------|
| `agentName: "hephaestus"`, `fileType: "forge_insights"` | `memory/agents/hephaestus/forge_insights.md` |
| `agentName: "prometheus"`, `fileType: "strategic_notes"` | `memory/agents/prometheus/strategic_notes.md` |

---

## Timestamp Format

Every memory file must have the following as its **first line**:

```
<!-- Last Updated: YYYY-MM-DD -->
```

**Concrete example**:
```
<!-- Last Updated: 2026-02-10 -->
```

This timestamp is:
- **Injected** automatically by the adapter on `create()`
- **Updated** automatically by the adapter on `update()` and `append()`
- **Parsed** by the adapter on `read()` for staleness computation
- **Required** by `memory/lifecycle.md` for all memory files

### Timestamp Parsing

The adapter extracts the timestamp using this pattern:
```
Line 1: <!-- Last Updated: (\d{4}-\d{2}-\d{2}) -->
```

If the first line does not match this pattern, the file is treated as having no timestamp (staleness = `"stale"`).

---

## Method-to-Filesystem Mapping

### `create(entry)` → mkdir + write

**Filesystem operations**:
1. Construct path from entry metadata (see Path Construction above)
2. Check if parent directory exists; if not, create it recursively (equivalent to `mkdir -p`)
3. Check if file exists; if yes, reject with error (use `update()` instead)
4. Prepend `<!-- Last Updated: {today} -->` followed by blank line to `entry.content`
5. Write file to constructed path

**Example**:
```
create({
  layer: "skill-specific",
  skillName: "python-code-review",
  projectName: "my-api",
  fileType: "project_overview",
  content: "# Project Overview - My API\n\n## Framework\n- FastAPI 0.104"
})

→ mkdir -p memory/skills/python-code-review/my-api/
→ Write to memory/skills/python-code-review/my-api/project_overview.md:

<!-- Last Updated: 2026-02-10 -->

# Project Overview - My API

## Framework
- FastAPI 0.104
```

### `read(...)` → read file + parse timestamp + compute staleness

**Filesystem operations**:
1. Construct path from parameters
2. Check if file exists; if not, return `null`
3. Read file contents
4. Parse first line for `<!-- Last Updated: YYYY-MM-DD -->` timestamp
5. Compute days since update: `today - updatedAt`
6. Determine staleness enum:
   - 0-30 days → `"fresh"`
   - 31-90 days → `"aging"`
   - 90+ days or no timestamp → `"stale"`
7. Count lines for `lineCount`
8. Return populated `MemoryEntry` object

### `update(id, content)` → read + write

**Filesystem operations**:
1. Parse `id` to construct file path
2. Verify file exists; if not, return error
3. Replace or prepend `<!-- Last Updated: {today} -->` as first line
4. Write new content (with updated timestamp) to file
5. Count lines and check against size limits:
   - All files: warn if > 500 lines
   - `project_overview`: warn if > 200 lines
   - `review_history`: warn if > 300 lines

### `append(id, content)` → read + append + conditional prune + write

**Filesystem operations**:
1. Parse `id` to construct file path
2. Read existing file content
3. Update `<!-- Last Updated: {today} -->` on first line
4. Append new content to end of file
5. **Apply auto-pruning based on `fileType`** (see Auto-Pruning below)
6. Write modified content back to file
7. Count lines and check size limits

### `delete(id)` → rm

**Filesystem operations**:
1. Parse `id` to construct file path
2. Check if file exists; if not, return `{ deleted: false }`
3. Remove the file (equivalent to `rm`)
4. Do not remove parent directories

### `getProjectProfile(projectName)` → read single file

**Filesystem operations**:
1. Read `memory/projects/{projectName}/project_profile.md`
2. Delegates to `read("shared-project", projectName, "project_profile")`

### `getSharedProjectMemory(projectName)` → list directory + read each file

**Filesystem operations**:
1. List all `.md` files in `memory/projects/{projectName}/`
2. Exclude files named `index.md`
3. Read each file and construct `MemoryEntry` with staleness

### `getSkillMemory(skillName, projectName)` → list directory + read each file

**Filesystem operations**:
1. List all `.md` files in `memory/skills/{skillName}/{projectName}/`
2. Exclude files named `index.md`
3. Read each file and construct `MemoryEntry` with staleness

### `getCommandMemory(projectName)` → list directory + read each file

**Filesystem operations**:
1. List all `.md` files in `memory/commands/{projectName}/`
2. Exclude files named `index.md`
3. Read each file and construct `MemoryEntry` with staleness

### `getAgentMemory(agentName)` → list directory + read each file

**Filesystem operations**:
1. List all `.md` files in `memory/agents/{agentName}/`
2. Exclude files named `index.md`
3. Read each file and construct `MemoryEntry` with staleness

### `prune(policy)` → read + parse + conditional write/archive

See Auto-Pruning section below.

### `validate(id)` → read + content analysis

**Filesystem operations**:
1. Read the memory file
2. Analyze content against quality_guidance.md rules (string matching, section detection)
3. Return structured `QualityChecks` result (no filesystem writes)

### `getStalenessReport()` → recursive list + read timestamps

**Filesystem operations**:
1. Recursively list all `.md` files under `memory/`
2. Exclude `index.md`, `lifecycle.md`, `quality_guidance.md` (structural files)
3. Read only the first line of each file for timestamp extraction
4. Compute staleness for each file
5. Group by staleness category

### `getByProject(projectName)` → multi-directory list + read

**Filesystem operations**:
1. List `memory/projects/{projectName}/` → shared layer
2. For each subdirectory in `memory/skills/*/`, check for `{projectName}/` subdirectory → skill layer
3. List `memory/commands/{projectName}/` → command layer
4. Read all found files with staleness computation

### `search(pattern)` → recursive grep

**Filesystem operations**:
1. Recursively search all `.md` files under `memory/` for `pattern`
2. Exclude `index.md` structural files
3. Return matching lines with 2 lines of surrounding context
4. Apply `layer` and `projectName` filters to restrict search scope

---

## Auto-Pruning Implementation

The adapter applies pruning rules automatically during `append()` and on-demand via `prune()`. Rules come from `memory/lifecycle.md`.

### review_history.md

**Detection**: Count headings matching `## Review` pattern.

**Pruning logic**:
1. Parse the file into sections split by `## Review` headings
2. Count sections; if count <= 10, no pruning needed
3. If count > 10, separate the oldest sections (those beyond the 10 most recent)
4. Check if `review_history_archive.md` exists in the same directory; create if not
5. Append the oldest sections to the archive file (preserving their content)
6. Remove the oldest sections from the main file
7. Update timestamps on both files

**Example**:
```
# Before: review_history.md has 13 ## Review entries
#   → Reviews #1, #2, #3 are oldest

# After append + prune:
# review_history.md: Reviews #4 through #13 (10 entries) + new Review #14
# review_history_archive.md: Reviews #1, #2, #3 appended
```

### known_issues.md

**Detection**: Scan for entries containing status markers.

**Pruning logic**:
1. Parse the file into issue sections (split by `###` headings within severity groups)
2. For each section, check for status markers:
   - Look for `**Status**:` lines containing "Resolved" (or status emoji patterns)
   - Look for date patterns near the "Resolved" status
3. If an issue is marked "Resolved" and the resolution date is 30+ days ago, remove it
4. If an issue has "In Progress" status, keep it regardless of age
5. If an issue has no status update for 90+ days, add `[VERIFY STATUS]` tag
6. Write updated content back

**Example**:
```
# Before: known_issues.md
### N+1 Query in Order History
**Status**: Resolved (2026-01-05)
→ Resolved 36 days ago → REMOVED

### Missing CancellationToken
**Status**: In Progress
→ In Progress → KEPT (regardless of age)

### Old Singleton Issue
**Status**: Investigating (2025-10-15)
→ No update for 118 days → [VERIFY STATUS] tag added
```

### test_results_history.md

**Detection**: Count headings matching `## Session` or `## Test Session` pattern.

**Pruning logic**:
1. Parse the file into session sections
2. Count sections; if count <= 15, no pruning needed
3. If count > 15, separate sessions beyond the 15 most recent
4. Summarize older sessions into a "Historical Summary" section at the bottom
5. Replace individual old session sections with the summary

---

## Auto-Staleness Computation

Performed on every `read()` call.

**Algorithm**:
1. Read the first line of the file
2. Match against pattern: `<!-- Last Updated: (\d{4}-\d{2}-\d{2}) -->`
3. If no match: return `staleness: "stale"` (no valid timestamp)
4. Parse the date: `updatedAt = parse(match[1])`
5. Compute days: `daysSinceUpdate = today - updatedAt`
6. Map to staleness enum:

| Days Since Update | Staleness |
|-------------------|-----------|
| 0-30 | `"fresh"` |
| 31-90 | `"aging"` |
| 91+ | `"stale"` |

---

## Before/After: Path Replacement Patterns

The adapter replaces the relative `../../memory/` paths currently used throughout skill and command files with structured MemoryStore calls.

### Pattern 1: Skill loading project memory

**Before** (from `python-code-review` SKILL.md, Step 2):
```markdown
1. CHECK PROJECT MEMORY FIRST:
   - Identify the project name from the repository root or ask the user
   - READ `../../memory/skills/python-code-review/index.md` to understand the memory system
   - Check `../../memory/skills/python-code-review/{project-name}/` for existing project memory
   - If memory exists, read the memory files to understand previously learned patterns
```

**After**:
```
skillMemory = MemoryStore.getSkillMemory("python-code-review", projectName)
// Returns all memory files with staleness computed
// Empty array signals first-time project analysis

sharedMemory = MemoryStore.getSharedProjectMemory(projectName)
// Cross-skill knowledge for this project
```

### Pattern 2: Command loading execution history

**Before** (from `/analyze` COMMAND.md, Step 2):
```markdown
**Memory Loading**:
1. Determine project name (from git repo name or directory)
2. Check `../../memory/commands/{project}/command_history.md` for past analyses
3. Load `../../memory/commands/{project}/analyze_insights.md` if exists
4. Check skill memory for deeper context (e.g., `../../memory/skills/python-code-review/{project}/`)
```

**After**:
```
commandMemory = MemoryStore.getCommandMemory(projectName)
// All command memory for the project

skillMemory = MemoryStore.getSkillMemory("python-code-review", projectName)
// Deeper context from skill executions
```

### Pattern 3: Skill updating memory after analysis

**Before** (from skill workflow Step 5):
```markdown
# Manually construct paths and write files:
# 1. Write ../../memory/skills/python-code-review/{project}/project_overview.md
# 2. Append to ../../memory/skills/python-code-review/{project}/review_history.md
# 3. Update ../../memory/skills/python-code-review/{project}/known_issues.md
# 4. Remember to add <!-- Last Updated: YYYY-MM-DD --> (often forgotten)
# 5. Remember to check file sizes (usually skipped)
# 6. Remember to prune old reviews (usually skipped)
```

**After**:
```
// Create or update project overview
MemoryStore.update("skill-specific/python-code-review/my-api/project_overview", overviewContent)
// → Timestamp auto-refreshed, size limit auto-checked

// Append review entry with auto-pruning
MemoryStore.append("skill-specific/python-code-review/my-api/review_history", reviewEntry)
// → Timestamp auto-refreshed, old reviews auto-archived if > 10

// Update known issues with auto-cleanup
MemoryStore.update("skill-specific/python-code-review/my-api/known_issues", issuesContent)
// → Timestamp auto-refreshed, resolved issues auto-removed after 30 days on next prune
```

### Pattern 4: Shared project memory workflow

**Before** (from `memory/index.md` workflow):
```markdown
**Workflow change for all skills**:
1. On start: Read `memory/projects/{project}/project_profile.md` first (if exists)
2. Then read skill-specific memory as before
3. On end: Create or update shared project memory with new project-level info
4. Add freshness timestamp to modified files
```

**After**:
```
// On start
profile = MemoryStore.getProjectProfile(projectName)
// → Null if first time, MemoryEntry with staleness if exists

allShared = MemoryStore.getSharedProjectMemory(projectName)
// → All shared knowledge files

// On end
MemoryStore.update("shared-project/my-api/project_profile", updatedProfile)
// → Timestamp auto-managed, staleness auto-reset
```

---

## Related Documents

- **Interface**: `memory_store.md` - The MemoryStore interface this adapter implements
- **Schema**: `schemas/memory_entry.schema.json` - JSON Schema for memory entries
- **Source Rules**: `memory/lifecycle.md` - Freshness thresholds, pruning rules, size limits
- **Source Rules**: `memory/quality_guidance.md` - Quality check definitions
- **Memory Index**: `memory/index.md` - Memory system structure and documentation

---

*Last Updated: 2026-02-10*
