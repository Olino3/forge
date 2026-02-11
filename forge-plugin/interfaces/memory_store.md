# MemoryStore Interface

**Version**: 0.1.0-alpha
**Status**: Phase 1 - Interface Definition
**Schema**: `schemas/memory_entry.schema.json`

## Purpose

The MemoryStore interface formalizes and automates the rules defined in `memory/lifecycle.md` and `memory/quality_guidance.md`. It provides a unified API for all memory operations across the Forge plugin, replacing ad-hoc file path construction and manual timestamp management with structured, validated operations.

### Relationship to Existing Documents

| Document | Role | How MemoryStore Automates It |
|----------|------|------------------------------|
| `memory/lifecycle.md` | Freshness thresholds, pruning rules, size limits | Auto-timestamps on create/update, auto-prune on append, size limit enforcement |
| `memory/quality_guidance.md` | Completeness, accuracy, specificity, growth checks | `validate()` method runs all checks, returns structured results |
| `memory/index.md` | Memory structure documentation | Path construction rules formalize the directory layout |

---

## Path Construction Rules

All memory files are markdown files stored under `forge-plugin/memory/`. The MemoryStore constructs paths from entry metadata:

| Layer | Path Pattern | Example |
|-------|-------------|---------|
| `shared-project` | `memory/projects/{projectName}/{fileType}.md` | `memory/projects/my-api/project_profile.md` |
| `skill-specific` | `memory/skills/{skillName}/{projectName}/{fileType}.md` | `memory/skills/python-code-review/my-api/project_overview.md` |
| `command` | `memory/commands/{projectName}/{fileType}.md` | `memory/commands/my-api/command_history.md` |
| `agent` | `memory/agents/{agentName}/{fileType}.md` | `memory/agents/hephaestus/forge_insights.md` |

All paths are relative to `forge-plugin/`. Skills currently use `../../memory/` relative paths from their `SKILL.md` location; the MemoryStore normalizes these to a single root.

---

## Methods

### 1. `create(entry)`

Create a new memory file with automatic timestamp injection.

**Parameters**:

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `entry` | `MemoryEntry` | Yes | Memory entry metadata conforming to `memory_entry.schema.json` |

**Returns**: `{ id: string, path: string, created: boolean }`

**Auto-behaviors**:
- Injects `<!-- Last Updated: YYYY-MM-DD -->` as first line of content
- Creates parent directories if they do not exist
- Sets `createdAt` and `updatedAt` to current date
- Sets `staleness` to `"fresh"`
- Validates entry against `memory_entry.schema.json`
- Rejects creation if file already exists (use `update()` instead)

**Before** (current approach in skills):
```markdown
# In SKILL.md workflow step:
# 1. Manually construct path: ../../memory/skills/python-code-review/{project}/project_overview.md
# 2. Manually add timestamp: <!-- Last Updated: 2026-02-10 -->
# 3. Write file content
# 4. Hope the directory exists
```

**After** (with MemoryStore):
```
create({
  id: "skill-specific/python-code-review/my-api/project_overview",
  layer: "skill-specific",
  skillName: "python-code-review",
  projectName: "my-api",
  fileType: "project_overview",
  content: "# Project Overview - My API\n\n## Framework\n- FastAPI 0.104..."
})
→ File created at memory/skills/python-code-review/my-api/project_overview.md
→ Timestamp auto-injected as first line
→ Directories auto-created
```

---

### 2. `read(layer, projectName, fileType, skillName?, commandName?, agentName?)`

Read a memory file and auto-compute its staleness status.

**Parameters**:

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `layer` | `string` | Yes | Memory layer: `"shared-project"`, `"skill-specific"`, `"command"`, `"agent"` |
| `projectName` | `string` | Yes | Project name |
| `fileType` | `string` | Yes | File type (e.g., `"project_overview"`, `"known_issues"`) |
| `skillName` | `string` | When layer is `"skill-specific"` | Skill name |
| `commandName` | `string` | When layer is `"command"` | Command name |
| `agentName` | `string` | When layer is `"agent"` | Agent name |

**Returns**: `MemoryEntry | null` (null if file does not exist)

**Auto-behaviors**:
- Parses `<!-- Last Updated: YYYY-MM-DD -->` from first line to extract `updatedAt`
- Computes `staleness` from `updatedAt` using lifecycle.md thresholds
- Computes `lineCount` from content
- If `staleness` is `"stale"`, adds `[POTENTIALLY STALE]` advisory to returned metadata

**Before**:
```markdown
# In SKILL.md workflow:
# 1. Construct path manually: ../../memory/skills/python-code-review/{project}/project_overview.md
# 2. Read file
# 3. Manually check if stale (usually skipped)
# 4. No structured metadata available
```

**After**:
```
read("skill-specific", "my-api", "project_overview", skillName: "python-code-review")
→ Returns MemoryEntry with content, staleness: "fresh", lineCount: 45, updatedAt: "2026-02-01"
```

---

### 3. `update(id, content)`

Replace content of an existing memory file with automatic timestamp refresh and size enforcement.

**Parameters**:

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `id` | `string` | Yes | Memory entry ID (e.g., `"skill-specific/python-code-review/my-api/project_overview"`) |
| `content` | `string` | Yes | New markdown content (timestamp line will be auto-managed) |

**Returns**: `{ id: string, updated: boolean, lineCount: number, warning?: string }`

**Auto-behaviors**:
- Updates `<!-- Last Updated: YYYY-MM-DD -->` timestamp to current date
- Resets `staleness` to `"fresh"`
- Checks line count against size limits from lifecycle.md:
  - Any file: warns if > 500 lines
  - `project_overview`: warns if > 200 lines
  - `review_history`: warns if > 300 lines
- Returns warning string if size limit exceeded (does not block the write)

**Before**:
```markdown
# 1. Manually read file, modify content
# 2. Remember to update <!-- Last Updated: ... --> (often forgotten)
# 3. No size limit checking
# 4. Write file back
```

**After**:
```
update("skill-specific/python-code-review/my-api/project_overview", newContent)
→ { id: "...", updated: true, lineCount: 187, warning: null }
→ Timestamp auto-refreshed
```

---

### 4. `append(id, content)`

Append content to an existing memory file with automatic timestamp refresh and pruning.

**Parameters**:

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `id` | `string` | Yes | Memory entry ID |
| `content` | `string` | Yes | Content to append |

**Returns**: `{ id: string, appended: boolean, lineCount: number, pruned: boolean, pruneDetails?: string }`

**Auto-behaviors**:
- Updates `<!-- Last Updated: YYYY-MM-DD -->` timestamp
- Applies automatic pruning rules based on `fileType` (from lifecycle.md):
  - **`review_history`**: Counts `## Review` entries; if > 10, moves oldest entries to `{fileType}_archive.md` in same directory
  - **`known_issues`**: Scans for entries marked "Resolved"; removes entries resolved 30+ days ago
  - **`test_results_history`**: Keeps last 15 test sessions; summarizes older into "Historical Summary"
- Checks size limits after append; returns warning if exceeded

**Before**:
```markdown
# In SKILL.md post-review workflow:
# 1. Read review_history.md
# 2. Append new review entry
# 3. Manually count entries (usually skipped)
# 4. Manually archive old entries (usually skipped)
# 5. Manually update timestamp
```

**After**:
```
append("skill-specific/python-code-review/my-api/review_history", newReviewEntry)
→ { appended: true, lineCount: 285, pruned: true, pruneDetails: "Archived 3 reviews older than entry #10" }
→ Timestamp auto-refreshed, oldest reviews auto-archived
```

---

### 5. `delete(id)`

Remove a memory file.

**Parameters**:

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `id` | `string` | Yes | Memory entry ID |

**Returns**: `{ id: string, deleted: boolean }`

**Auto-behaviors**:
- Removes the file from the filesystem
- Does not remove parent directories (they may contain other files)
- Returns `deleted: false` if file did not exist

---

### 6. `getProjectProfile(projectName)`

Convenience method to read the shared project profile.

**Parameters**:

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `projectName` | `string` | Yes | Project name |

**Returns**: `MemoryEntry | null`

**Auto-behaviors**:
- Reads `memory/projects/{projectName}/project_profile.md`
- Equivalent to `read("shared-project", projectName, "project_profile")`
- Auto-computes staleness

---

### 7. `getSharedProjectMemory(projectName)`

Read all memory files in the shared project layer.

**Parameters**:

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `projectName` | `string` | Yes | Project name |

**Returns**: `MemoryEntry[]`

**Auto-behaviors**:
- Lists all `.md` files in `memory/projects/{projectName}/`
- Reads each file and computes staleness
- Returns empty array if directory does not exist
- Excludes `index.md` files (they are structural, not memory content)

**Before**:
```markdown
# In SKILL.md Step 2:
# 1. Read ../../memory/projects/{project}/project_profile.md
# 2. Read ../../memory/projects/{project}/technology_stack.md
# 3. Read ../../memory/projects/{project}/cross_skill_insights.md
# 4. Each read is a separate manual operation with manual path construction
```

**After**:
```
getSharedProjectMemory("my-api")
→ Returns array of all MemoryEntry objects for the project, each with staleness computed
```

---

### 8. `getSkillMemory(skillName, projectName)`

Read all memory files for a specific skill and project.

**Parameters**:

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `skillName` | `string` | Yes | Skill name (e.g., `"python-code-review"`) |
| `projectName` | `string` | Yes | Project name |

**Returns**: `MemoryEntry[]`

**Auto-behaviors**:
- Lists all `.md` files in `memory/skills/{skillName}/{projectName}/`
- Reads each file with staleness computation
- Returns empty array if directory does not exist (first invocation for this project)
- Excludes `index.md` files

**Before**:
```markdown
# In python-code-review SKILL.md Step 2:
# 1. Check ../../memory/skills/python-code-review/{project-name}/ exists
# 2. Read project_overview.md
# 3. Read common_patterns.md
# 4. Read known_issues.md
# 5. Read review_history.md
# Each file is a separate manual read with relative path construction
```

**After**:
```
getSkillMemory("python-code-review", "my-api")
→ Returns all memory files with staleness, line counts, and structured metadata
→ Empty array signals first-time project analysis
```

---

### 9. `getCommandMemory(projectName)`

Read all memory files for command execution tracking.

**Parameters**:

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `projectName` | `string` | Yes | Project name |

**Returns**: `MemoryEntry[]`

**Auto-behaviors**:
- Lists all `.md` files in `memory/commands/{projectName}/`
- Reads each file with staleness computation
- Returns empty array if directory does not exist

**Before**:
```markdown
# In /analyze COMMAND.md Step 2:
# 1. Check ../../memory/commands/{project}/command_history.md
# 2. Load ../../memory/commands/{project}/analyze_insights.md if exists
# Manual path construction, no staleness checking
```

**After**:
```
getCommandMemory("my-api")
→ Returns all command memory entries with staleness metadata
```

---

### 10. `prune(policy)`

Apply lifecycle.md pruning rules across memory files.

**Parameters**:

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `policy` | `object` | Yes | Pruning policy configuration |
| `policy.scope` | `string` | Yes | `"project"`, `"skill"`, or `"all"` |
| `policy.projectName` | `string` | When scope includes project | Project to prune |
| `policy.skillName` | `string` | When scope is `"skill"` | Skill to prune |
| `policy.dryRun` | `boolean` | No | If true, report what would be pruned without acting (default: false) |

**Returns**: `{ pruned: PruneAction[], warnings: string[] }`

Where `PruneAction` is `{ id: string, action: "archived" | "removed" | "flagged", reason: string }`

**Auto-behaviors** (from lifecycle.md):
- **`review_history`**: Keeps last 10 `## Review` entries, moves older to `review_history_archive.md`
- **`known_issues`**: Removes entries marked "Resolved" for 30+ days; keeps "In Progress" regardless of age; adds `[VERIFY STATUS]` to entries with no status update for 90+ days
- **`common_patterns`**: Flags for verification every 5th invocation (tracks invocation count internally)
- **`test_results_history`**: Keeps last 15 sessions, summarizes older into "Historical Summary"
- Reports size limit violations as warnings

---

### 11. `validate(id)`

Run quality_guidance.md checks against a memory entry.

**Parameters**:

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `id` | `string` | Yes | Memory entry ID to validate |

**Returns**: `{ id: string, checks: QualityChecks, suggestions: string[] }`

Where `QualityChecks` matches the schema's `qualityChecks` object:
```
{
  completeness: boolean,  // Does project_overview cover language, framework, architecture, conventions, testing?
  specificity: boolean,   // Does the entry reference specific file paths rather than vague descriptions?
  growthRate: "healthy" | "stagnant" | "unknown"
}
```

**Auto-behaviors** (from quality_guidance.md):
- **Completeness check**: For `project_overview` files, verifies presence of: language/version, framework/version, architecture pattern, key conventions, testing approach. Returns `false` if any are missing.
- **Accuracy check**: Every 5th invocation, flags that 2-3 claims should be spot-checked. Returns a suggestion to verify specific file paths and conventions mentioned in the entry.
- **Specificity check**: Scans content for vague patterns (e.g., "uses custom auth" without file path). Returns `false` if more than 30% of claims lack specific references.
- **Growth check**: Compares current line count against historical count (if tracked). Returns `"stagnant"` if no growth in 5+ invocations, `"healthy"` if growing, `"unknown"` if insufficient history.

---

### 12. `getStalenessReport()`

Generate a staleness report across all memory files.

**Parameters**: None

**Returns**: `{ fresh: StalenessEntry[], aging: StalenessEntry[], stale: StalenessEntry[] }`

Where `StalenessEntry` is `{ id: string, path: string, updatedAt: string, daysSinceUpdate: number }`

**Auto-behaviors**:
- Scans all memory files across all layers
- Parses `<!-- Last Updated: YYYY-MM-DD -->` from each file
- Categorizes per lifecycle.md thresholds:
  - `fresh`: 0-30 days since update
  - `aging`: 31-90 days since update
  - `stale`: 90+ days since update
- Files without a timestamp are categorized as `stale`

---

### 13. `getByProject(projectName)`

Retrieve all memory across all layers for a specific project.

**Parameters**:

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `projectName` | `string` | Yes | Project name |

**Returns**: `{ shared: MemoryEntry[], skills: { [skillName: string]: MemoryEntry[] }, commands: MemoryEntry[] }`

**Auto-behaviors**:
- Reads `memory/projects/{projectName}/` (shared layer)
- Scans all `memory/skills/*/` directories for subdirectories matching `{projectName}/`
- Reads `memory/commands/{projectName}/` (command layer)
- Returns structured result grouped by layer
- Each entry includes staleness computation

---

### 14. `search(pattern)`

Search across all memory files for content matching a pattern.

**Parameters**:

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `pattern` | `string` | Yes | Search pattern (supports basic regex) |
| `layer` | `string` | No | Restrict search to a specific layer |
| `projectName` | `string` | No | Restrict search to a specific project |

**Returns**: `{ matches: SearchMatch[] }`

Where `SearchMatch` is `{ id: string, path: string, lineNumber: number, lineContent: string, context: string }`

**Auto-behaviors**:
- Searches all `.md` files under `memory/`
- Returns matching lines with surrounding context (2 lines before/after)
- Respects layer and project filters if provided
- Excludes `index.md` structural files from search results

---

### 15. `getAgentMemory(agentName)`

Read all memory files for a specific agent.

**Parameters**:

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `agentName` | `string` | Yes | Agent name (e.g., `"hephaestus"`, `"prometheus"`) |

**Returns**: `MemoryEntry[]`

**Auto-behaviors**:
- Lists all `.md` files in `memory/agents/{agentName}/`
- Reads each file with staleness computation
- Returns empty array if directory does not exist

---

## Staleness Rules

Derived from `memory/lifecycle.md`:

| Days Since Update | Status | MemoryStore Behavior |
|-------------------|--------|---------------------|
| 0-30 | `fresh` | Return entry as-is, no warnings |
| 31-90 | `aging` | Return entry with `staleness: "aging"`; consumers should verify critical claims |
| 90+ | `stale` | Return entry with `staleness: "stale"` and advisory `[POTENTIALLY STALE]`; consumers should not rely on without verification |

Staleness is computed on every `read()` call from the `<!-- Last Updated: YYYY-MM-DD -->` timestamp. Files without this timestamp are treated as `stale`.

---

## Pruning Rules

Derived from `memory/lifecycle.md`. Applied automatically by `append()` and on-demand by `prune()`.

### review_history.md
- **Trigger**: Entry count exceeds 10 (`## Review` headings)
- **Action**: Move oldest entries (beyond the 10 most recent) to `review_history_archive.md` in the same directory
- **Archive**: No size limit; never loaded automatically by skills

### known_issues.md
- **Trigger**: Entries marked "Resolved" older than 30 days
- **Action**: Remove resolved entries that are 30+ days old
- **Preservation**: Keep all entries marked "In Progress" regardless of age
- **Flagging**: Add `[VERIFY STATUS]` to entries with no status update for 90+ days

### common_patterns.md
- **Trigger**: Every 5th skill invocation (tracked by MemoryStore)
- **Action**: Flag entire file for verification review
- **Guidance**: Remove patterns that no longer appear in the codebase; consolidate similar patterns

### test_results_history.md
- **Trigger**: Session count exceeds 15
- **Action**: Keep last 15 test sessions; summarize older sessions into a "Historical Summary" section

---

## Quality Checks

Derived from `memory/quality_guidance.md`. Run by `validate()` and optionally by `create()`/`update()`.

### Completeness
Applies to `project_overview` file type. Checks for presence of:
- Language and version
- Framework and version
- Architecture pattern
- Key conventions (naming, file organization)
- Testing approach

Returns `false` if any section is missing after 3+ invocations.

### Accuracy
Every 5th invocation, generates suggestions to:
1. Pick a file path mentioned in memory and verify it still exists
2. Pick a convention claim and verify it matches current code
3. Pick a known issue and verify its status is current

### Specificity
Scans memory content for vague descriptions. Flags entries that use general language without specific file paths, line numbers, or function names. Compares against patterns from quality_guidance.md:

| Flagged (vague) | Expected (specific) |
|-----------------|---------------------|
| "Uses custom auth" | "Custom JWT auth in `app/auth/middleware.py`, 15min expiry" |
| "Has N+1 queries" | "N+1 in `OrdersController.cs:GetHistory()`, loads reviews in loop" |
| "Tests use fixtures" | "Shared fixtures in `tests/conftest.py`: `sample_user`, `mock_db`" |

### Growth
Tracks line count across invocations. Flags `"stagnant"` if `common_patterns.md` has not grown in 5+ invocations.

---

## Size Limits

Derived from `memory/lifecycle.md`. Enforced as warnings by `update()` and `append()`.

| File Type | Max Lines | Action When Exceeded |
|-----------|-----------|---------------------|
| Any single memory file | 500 | Warning: "Split into focused sub-files" |
| `project_overview` | 200 | Warning: "Move detailed sections to separate files" |
| `review_history` | 300 | Warning: "Archive older entries" (auto-pruning handles this) |

Size limits produce warnings, not hard failures. The MemoryStore reports the violation but completes the write operation.

---

## Related Documents

- **Schema**: `schemas/memory_entry.schema.json` - JSON Schema for memory entry validation
- **Adapter**: `adapters/markdown_file_memory_adapter.md` - Filesystem implementation details
- **Source Rules**: `memory/lifecycle.md` - Freshness, pruning, and size limit definitions
- **Source Rules**: `memory/quality_guidance.md` - Quality check definitions
- **Memory Index**: `memory/index.md` - Memory system structure and per-skill documentation

---

## Future Adapters

The MemoryStore interface is designed to support multiple adapter implementations beyond the current `MarkdownFileMemoryAdapter`:

- **SQLiteMemoryAdapter** (`adapters/sqlite_memory_adapter.md`): Database-backed storage with FTS5 full-text search, SQL-based staleness computation, and indexed cross-project queries. Designed for large-scale projects with 100+ memory files.
- **VectorStoreAdapter** (`adapters/vector_store_adapter.md`): Semantic search augmentation using vector embeddings. Enhances `search()` with similarity-based retrieval alongside keyword matching.

These are **design specifications only** — see each adapter's documentation for schema design, migration paths, and comparison tables.

---

*Last Updated: 2026-02-11*
