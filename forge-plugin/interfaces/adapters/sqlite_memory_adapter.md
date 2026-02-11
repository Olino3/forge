# SQLiteMemoryAdapter

**Version**: 1.0.0
**Status**: Future Adapter Specification (Design Only)
**Implements**: [`memory_store.md`](../memory_store.md) (MemoryStore interface)

## Purpose

The SQLiteMemoryAdapter is a future alternative adapter that implements the MemoryStore interface using a SQLite database instead of markdown files. It provides the same API as the MarkdownFileMemoryAdapter but with advantages in query performance, full-text search, and concurrent access. This document is a **design specification** — implementation is deferred until demand warrants it.

---

## SQL Schema

### Core Table: `memory_entries`

```sql
CREATE TABLE memory_entries (
  id TEXT PRIMARY KEY,                    -- e.g., "skill-specific/python-code-review/my-api/project_overview"
  layer TEXT NOT NULL,                    -- "shared-project", "skill-specific", "command", "agent"
  project_name TEXT,                      -- project identifier
  skill_name TEXT,                        -- skill name (for skill-specific layer)
  agent_name TEXT,                        -- agent name (for agent layer)
  file_type TEXT NOT NULL,                -- "project_overview", "review_history", etc.
  content TEXT NOT NULL,                  -- full markdown content
  created_at TEXT NOT NULL DEFAULT (date('now')),  -- ISO 8601
  updated_at TEXT NOT NULL DEFAULT (date('now')),  -- ISO 8601
  line_count INTEGER DEFAULT 0,
  staleness TEXT DEFAULT 'fresh'          -- computed: "fresh", "aging", "stale"
);

CREATE INDEX idx_layer_project ON memory_entries(layer, project_name);
CREATE INDEX idx_skill_project ON memory_entries(skill_name, project_name);
CREATE INDEX idx_agent ON memory_entries(agent_name);
CREATE INDEX idx_staleness ON memory_entries(staleness);
CREATE INDEX idx_updated_at ON memory_entries(updated_at);
```

### Full-Text Search: FTS5 Virtual Table

```sql
CREATE VIRTUAL TABLE memory_fts USING fts5(
  id,
  content,
  content=memory_entries,
  content_rowid=rowid
);

-- Triggers to keep FTS in sync
CREATE TRIGGER memory_fts_insert AFTER INSERT ON memory_entries BEGIN
  INSERT INTO memory_fts(rowid, id, content) VALUES (new.rowid, new.id, new.content);
END;

CREATE TRIGGER memory_fts_delete AFTER DELETE ON memory_entries BEGIN
  INSERT INTO memory_fts(memory_fts, rowid, id, content) VALUES ('delete', old.rowid, old.id, old.content);
END;

CREATE TRIGGER memory_fts_update AFTER UPDATE ON memory_entries BEGIN
  INSERT INTO memory_fts(memory_fts, rowid, id, content) VALUES ('delete', old.rowid, old.id, old.content);
  INSERT INTO memory_fts(rowid, id, content) VALUES (new.rowid, new.id, new.content);
END;
```

### Pruning History Table

```sql
CREATE TABLE prune_history (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  entry_id TEXT NOT NULL,
  action TEXT NOT NULL,                   -- "archived", "removed", "flagged"
  reason TEXT,
  pruned_at TEXT NOT NULL DEFAULT (date('now')),
  content_snapshot TEXT                   -- archived content for recovery
);
```

---

## Method-to-SQL Mapping

### `create(entry)` → INSERT

```sql
INSERT INTO memory_entries (id, layer, project_name, skill_name, agent_name, file_type, content, created_at, updated_at, line_count, staleness)
VALUES (?, ?, ?, ?, ?, ?, ?, date('now'), date('now'), ?, 'fresh');
```

**Auto-behaviors**: Rejects if `id` already exists (PRIMARY KEY constraint). Computes `line_count` from content before insert.

### `read(...)` → SELECT + staleness computation

```sql
SELECT *,
  CASE
    WHEN julianday('now') - julianday(updated_at) <= 30 THEN 'fresh'
    WHEN julianday('now') - julianday(updated_at) <= 90 THEN 'aging'
    ELSE 'stale'
  END AS computed_staleness
FROM memory_entries
WHERE layer = ? AND project_name = ? AND file_type = ?
  AND (skill_name = ? OR ? IS NULL)
  AND (agent_name = ? OR ? IS NULL);
```

**Auto-behaviors**: Staleness computed at query time via CASE expression. Returns `NULL` if no matching row.

### `update(id, content)` → UPDATE

```sql
UPDATE memory_entries
SET content = ?, updated_at = date('now'), line_count = ?, staleness = 'fresh'
WHERE id = ?;
```

**Auto-behaviors**: Timestamp auto-refreshed via `auto_update_timestamp` trigger. Returns row count to confirm update. Checks `line_count` against size limits post-update (application logic).

### `append(id, content)` → SELECT + UPDATE + conditional prune

```sql
-- Step 1: Read current content
SELECT content FROM memory_entries WHERE id = ?;

-- Step 2: Append and update
UPDATE memory_entries
SET content = content || char(10) || ?,
    updated_at = date('now'),
    line_count = line_count + ?
WHERE id = ?;

-- Step 3: Auto-prune if needed (see Pruning via SQL section)
```

**Auto-behaviors**: Concatenates new content. Triggers pruning rules based on `file_type`. Updates line count incrementally.

### `delete(id)` → DELETE

```sql
DELETE FROM memory_entries WHERE id = ?;
```

**Auto-behaviors**: Returns row count (0 = file did not exist, 1 = deleted). FTS cleanup handled by `memory_fts_delete` trigger.

### `getProjectProfile(projectName)` → SELECT

```sql
SELECT * FROM memory_with_staleness
WHERE layer = 'shared-project' AND project_name = ? AND file_type = 'project_profile';
```

Equivalent to `read("shared-project", projectName, "project_profile")`.

### `getSharedProjectMemory(projectName)` → SELECT

```sql
SELECT * FROM memory_with_staleness
WHERE layer = 'shared-project' AND project_name = ?
ORDER BY file_type;
```

Returns all shared-project entries for the given project with computed staleness.

### `getSkillMemory(skillName, projectName)` → SELECT

```sql
SELECT * FROM memory_with_staleness
WHERE layer = 'skill-specific' AND skill_name = ? AND project_name = ?
ORDER BY file_type;
```

Returns all skill-specific entries for the given skill and project.

### `getCommandMemory(projectName)` → SELECT

```sql
SELECT * FROM memory_with_staleness
WHERE layer = 'command' AND project_name = ?
ORDER BY file_type;
```

Returns all command-layer entries for the given project.

### `getAgentMemory(agentName)` → SELECT

```sql
SELECT * FROM memory_with_staleness
WHERE layer = 'agent' AND agent_name = ?
ORDER BY file_type;
```

Returns all agent-layer entries for the given agent.

### `prune(policy)` → SELECT + DELETE + INSERT into prune_history

```sql
-- Scope filter (applied to all pruning queries)
-- policy.scope = "project": WHERE project_name = ?
-- policy.scope = "skill": WHERE skill_name = ? AND project_name = ?
-- policy.scope = "all": no additional filter

-- See "Pruning via SQL" section for file_type-specific queries
```

When `policy.dryRun = true`, wraps all operations in a transaction that is rolled back after collecting results.

### `validate(id)` → SELECT + content analysis

```sql
SELECT * FROM memory_entries WHERE id = ?;
```

Content analysis (completeness, specificity, growth) performed in application logic after retrieval. No writes.

### `getStalenessReport()` → SELECT with grouping

```sql
SELECT id,
  updated_at,
  CAST(julianday('now') - julianday(updated_at) AS INTEGER) AS days_since_update,
  CASE
    WHEN julianday('now') - julianday(updated_at) <= 30 THEN 'fresh'
    WHEN julianday('now') - julianday(updated_at) <= 90 THEN 'aging'
    ELSE 'stale'
  END AS computed_staleness
FROM memory_entries
ORDER BY computed_staleness DESC, days_since_update DESC;
```

Groups results by staleness category in application logic.

### `getByProject(projectName)` → SELECT across layers

```sql
SELECT * FROM memory_with_staleness
WHERE project_name = ?
ORDER BY layer, file_type;
```

Returns all entries across shared-project, skill-specific, and command layers for the project. Application logic groups results by layer.

### `search(pattern)` → FTS5 MATCH

```sql
-- Full-text search
SELECT me.*, mf.rank
FROM memory_fts mf
JOIN memory_entries me ON me.rowid = mf.rowid
WHERE memory_fts MATCH ?
  AND (me.layer = ? OR ? IS NULL)
  AND (me.project_name = ? OR ? IS NULL)
ORDER BY mf.rank;
```

**Auto-behaviors**: Uses FTS5 ranking for relevance ordering. Supports AND, OR, NOT, and phrase queries via FTS5 syntax. Returns matching entries with surrounding context extracted in application logic.

---

## Auto-Behaviors

### Timestamp Triggers

```sql
CREATE TRIGGER auto_update_timestamp
AFTER UPDATE ON memory_entries
BEGIN
  UPDATE memory_entries SET updated_at = date('now') WHERE id = new.id;
END;
```

### Staleness Computation (View)

```sql
CREATE VIEW memory_with_staleness AS
SELECT *,
  CASE
    WHEN julianday('now') - julianday(updated_at) <= 30 THEN 'fresh'
    WHEN julianday('now') - julianday(updated_at) <= 90 THEN 'aging'
    ELSE 'stale'
  END AS computed_staleness,
  CAST(julianday('now') - julianday(updated_at) AS INTEGER) AS days_since_update
FROM memory_entries;
```

### Pruning via SQL

```sql
-- Archive review_history entries beyond the 10 most recent
INSERT INTO prune_history (entry_id, action, reason, content_snapshot)
SELECT id, 'archived', 'Review history exceeds 10 entries', content
FROM memory_entries
WHERE file_type = 'review_history'
  AND id NOT IN (
    SELECT id FROM memory_entries
    WHERE file_type = 'review_history'
    ORDER BY updated_at DESC LIMIT 10
  );

-- Remove resolved known_issues older than 30 days
DELETE FROM memory_entries
WHERE file_type = 'known_issues'
  AND content LIKE '%Resolved%'
  AND julianday('now') - julianday(updated_at) > 30;
```

---

## Migration Path

### 5-Step Migration: Markdown → SQLite

1. **Export**: Read all markdown files from `forge-plugin/memory/` using MarkdownFileMemoryAdapter
2. **Parse**: Extract timestamps (`<!-- Last Updated: YYYY-MM-DD -->`), metadata, and content from each file
3. **Load**: INSERT parsed entries into `memory_entries` table with computed staleness
4. **Build FTS**: Trigger FTS5 index population via INSERT triggers
5. **Validate**: Compare row count vs file count; spot-check 10% of entries for content fidelity

### Migration Script (Pseudocode)

```
for each .md file in memory/:
  entry = MarkdownFileMemoryAdapter.read(file)
  SQLiteMemoryAdapter.create(entry)

assert count(memory_entries) == count(markdown_files)
for sample in random_sample(memory_entries, 10%):
  assert sample.content == MarkdownFileMemoryAdapter.read(sample.id).content
```

---

## Comparison: Markdown vs SQLite

| Dimension | MarkdownFileAdapter | SQLiteMemoryAdapter |
|-----------|--------------------|--------------------|
| **Human readability** | Excellent (native markdown) | Poor (binary database) |
| **Git integration** | Excellent (diff-friendly) | Poor (binary blob) |
| **Query performance** | O(n) directory scan | O(1) indexed lookup |
| **Full-text search** | grep (slow for large datasets) | FTS5 (fast, ranked) |
| **Concurrent access** | File locking (fragile) | WAL mode (robust) |
| **Cross-project search** | Multiple directory scans | Single indexed query |
| **Portability** | Any text editor | Requires SQLite library |
| **Staleness computation** | Parse timestamp per read | SQL view (pre-computed) |
| **Pruning** | Complex file manipulation | SQL DELETE + INSERT |
| **Storage overhead** | Low (text files) | Low (compressed binary) |
| **Setup cost** | Zero (files exist) | Requires migration |
| **Debugging** | Read files directly | Requires SQL client |

### Recommended Use Cases

- **MarkdownFileAdapter**: Small-to-medium projects (< 100 memory files), solo usage, git-centric workflows
- **SQLiteMemoryAdapter**: Large projects (100+ memory files), cross-project search needs, high-frequency memory access

---

## Related Documents

- **Interface**: [`memory_store.md`](../memory_store.md) — MemoryStore interface this adapter implements
- **Current Adapter**: [`markdown_file_memory_adapter.md`](markdown_file_memory_adapter.md) — current filesystem adapter
- **Schema**: [`schemas/memory_entry.schema.json`](../schemas/memory_entry.schema.json) — memory entry validation
- **Source Rules**: [`memory/lifecycle.md`](../../memory/lifecycle.md) — freshness and pruning rules

---

*Last Updated: 2026-02-11*
