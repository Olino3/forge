# Forge Interfaces

This directory contains the **interface contracts** that decouple consumers (skills, commands, agents) from direct filesystem paths. By introducing a formal interface layer, the Forge gains consistent access patterns, validated metadata, and a path toward future enhancements -- all without changing any existing consumer code.

## Architecture

```
+---------------------------------------------------------+
|                      Consumers                          |
|  +----------+  +----------+  +----------+              |
|  |  Skills   |  | Commands |  |  Agents  |              |
|  |  (22)     |  |  (12)    |  |  (11)    |              |
|  +-----+----+  +-----+----+  +-----+----+              |
|        |              |              |                   |
|        v              v              v                   |
|  +--------------------------------------------------+  |
|  |                 Interfaces                        |  |
|  |  +----------------+  +--------------+             |  |
|  |  |ContextProvider  |  | MemoryStore  |             |  |
|  |  +-------+--------+  +------+-------+             |  |
|  |  +----------------+  +------------------+         |  |
|  |  |SkillInvoker    |  |ExecutionContext  |         |  |
|  |  +-------+--------+  +--------+---------+         |  |
|  +----------+-----------------+--+-------------------+  |
|             |                 |                          |
|             v                 v                          |
|  +--------------------------------------------------+  |
|  |              Adapters (Current)                   |  |
|  |  +------------------------+                       |  |
|  |  |MarkdownFileContext     |                       |  |
|  |  |    Provider            |                       |  |
|  |  +-----------+------------+                       |  |
|  |  +------------------------+                       |  |
|  |  |MarkdownFileMemory     |                       |  |
|  |  |    Adapter             |                       |  |
|  |  +-----------+------------+                       |  |
|  |  +------------------------+                       |  |
|  |  |CachedContext          |                       |  |
|  |  |    Provider            |                       |  |
|  |  +-----------+------------+                       |  |
|  +--------------------------------------------------+  |
|  +- - - - - - - - - - - - - - - - - - - - - - - - - +  |
|  |           Future Adapters (Designed)               |  |
|  |  +--------------------+ +---------------------+   |  |
|  |  |SQLiteMemory        | |Context7 MCP         |   |  |
|  |  |    Adapter          | |    Provider          |   |  |
|  |  +--------------------+ +---------------------+   |  |
|  |  +--------------------+                            |  |
|  |  |VectorStore         |                            |  |
|  |  |    Adapter          |                            |  |
|  |  +--------------------+                            |  |
|  +- - - - - - - - - - - - - - - - - - - - - - - - - +  |
|             |                                           |
|             v                                           |
|  +--------------------------------------------------+  |
|  |                  Filesystem                       |  |
|  |  context/   |   memory/   |   skills/             |  |
|  +--------------------------------------------------+  |
+---------------------------------------------------------+
```

**Consumers** call **Interfaces** using documented method contracts. **Adapters** translate those method contracts into concrete filesystem operations against the existing `context/`, `memory/`, and `skills/` directories.

## How Convention-Based Interfaces Work

This is not a runtime system. There is no code, no compiler, no package manager. Interfaces are **documented contracts in markdown** that Claude Code follows as instructions.

The "methods" described in each interface spec (e.g., `ContextProvider.getCatalog()`) are conceptual operations. When Claude Code encounters a skill or command that needs context, it performs the equivalent file reads and writes according to the documented contract. The interface specs standardize *what* information is available and *how* to access it, while the adapter docs map those operations to specific file paths and formats.

This approach works because Claude Code is an instruction-following system. The interface specs are instructions that formalize patterns already present in `loading_protocol.md`, `lifecycle.md`, and `SKILL_TEMPLATE.md`.

## Relationship to Existing Documentation

Each interface wraps and extends existing Forge documentation:

| Interface | Wraps | Extends With |
|-----------|-------|-------------|
| **ContextProvider** | `context/loading_protocol.md` (5-step protocol) | Zero-token metadata via `getReference()`, partial loading via `materializeSections()`, keyword search via `search()` |
| **MemoryStore** | `memory/lifecycle.md` + `memory/quality_guidance.md` | Structured CRUD operations, automatic timestamp management, staleness queries |
| **SkillInvoker** | `skills/SKILL_TEMPLATE.md` (delegation patterns) | Structured `SkillResult` return type, skill discovery via `getAvailableSkills()`, domain-based filtering |
| **Schemas** | YAML frontmatter in context/agent files | Formal JSON Schema validation for `context_metadata`, `memory_entry`, `agent_config` |

## Backward Compatibility

Phase 1 uses a **dual-path approach** that guarantees zero breakage:

1. **Old paths continue to work.** Skills that reference `../../context/python/common_issues.md` or `../../memory/projects/` will find those files unchanged (body content is preserved; only YAML frontmatter is added to 5 pilot files).

2. **New interface calls are semantically equivalent.** A call to `ContextProvider.materialize("python/common_issues")` performs the same file read as the old relative path. The interface adds structure but not behavior changes.

3. **Phase 2+ will migrate consumers.** Future phases will update skills, commands, and agents to reference interface terminology. This migration will be incremental -- one consumer at a time.

4. **Zero consumer changes in Phase 1.** No SKILL.md, COMMAND.md, agent .md, plugin.json, or settings.local.json files are modified.

## Directory Structure

```
interfaces/
├── README.md                              This file - architecture overview
├── context_provider.md                    ContextProvider interface spec
├── memory_store.md                        MemoryStore interface spec
├── skill_invoker.md                       SkillInvoker interface spec
├── execution_context.md                   ExecutionContext interface spec (Phase 4)
├── shared_loading_patterns.md             Reusable loading patterns for skills (Phase 5)
├── performance_benchmarks.md              Token usage and boilerplate metrics (Phase 5)
├── deprecation_rules.md                   Deprecated pattern detection + linting (Phase 5)
├── migration_guide.md                     Consumer migration guide (Phase 2)
├── verification.md                        Phase 1 verification checklist
├── phase2_verification.md                 Phase 2 verification checklist
├── phase3_verification.md                 Phase 3 verification checklist
├── phase4_verification.md                 Phase 4 verification checklist
├── phase5_verification.md                 Phase 5 verification checklist
├── schemas/
│   ├── context_metadata.schema.json       Context file frontmatter schema
│   ├── memory_entry.schema.json           Memory entry metadata schema
│   └── agent_config.schema.json           Agent configuration schema
└── adapters/
    ├── markdown_file_context_provider.md   ContextProvider -> filesystem mapping (current)
    ├── markdown_file_memory_adapter.md     MemoryStore -> filesystem mapping (current)
    ├── cached_context_provider.md          Caching decorator for ContextProvider (Phase 5)
    ├── sqlite_memory_adapter.md            SQLite-backed MemoryStore adapter spec (Phase 5, design only)
    ├── context7_mcp_context_provider.md    Context7 MCP hybrid adapter spec (Phase 5, design only)
    └── vector_store_adapter.md             Vector embedding search adapter spec (Phase 5, design only)
```

## Specs Reference

### Core Interfaces

| File | Description |
|------|-------------|
| [context_provider.md](./context_provider.md) | Defines the ContextProvider interface: catalog browsing, domain indexes, project type detection, cross-domain loading, reference-based lazy loading, and keyword search |
| [memory_store.md](./memory_store.md) | Defines the MemoryStore interface: CRUD operations across 4 memory layers, staleness management, pruning rules, quality checks, and timestamp automation |
| [skill_invoker.md](./skill_invoker.md) | Defines the SkillInvoker interface: skill invocation with structured results, delegation patterns for code review and test generation, and skill discovery |
| [execution_context.md](./execution_context.md) | Defines the ExecutionContext interface: command chaining with shared state, context caching across commands, and shared data passing |

### Schemas

| File | Description |
|------|-------------|
| [schemas/context_metadata.schema.json](./schemas/context_metadata.schema.json) | JSON Schema (draft-07) validating YAML frontmatter on context files: id, domain, title, type, estimatedTokens, loadingStrategy |
| [schemas/memory_entry.schema.json](./schemas/memory_entry.schema.json) | JSON Schema (draft-07) validating memory entry metadata: project, skill, timestamps, staleness thresholds |
| [schemas/agent_config.schema.json](./schemas/agent_config.schema.json) | JSON Schema (draft-07) validating agent configuration: name, version, context domains, memory categories, skill bindings |

### Adapters — Current

| File | Description |
|------|-------------|
| [adapters/markdown_file_context_provider.md](./adapters/markdown_file_context_provider.md) | Maps ContextProvider methods to filesystem operations against `forge-plugin/context/` |
| [adapters/markdown_file_memory_adapter.md](./adapters/markdown_file_memory_adapter.md) | Maps MemoryStore methods to filesystem operations against `forge-plugin/memory/` |

### Adapters — Phase 5 (Optimization & Future)

| File | Description |
|------|-------------|
| [adapters/cached_context_provider.md](./adapters/cached_context_provider.md) | Caching decorator wrapping any ContextProvider with three-tier cache (catalog, reference, content). Session-scoped invalidation. Integrates with ExecutionContext for command chain optimization. |
| [adapters/sqlite_memory_adapter.md](./adapters/sqlite_memory_adapter.md) | *Design only.* SQLite-backed MemoryStore with FTS5 full-text search, SQL-based staleness computation, indexed cross-project queries, and automated pruning via triggers. |
| [adapters/context7_mcp_context_provider.md](./adapters/context7_mcp_context_provider.md) | *Design only.* Hybrid adapter routing framework-specific queries to Context7 MCP server for live docs, with fallback to local files. Identifies ~12 replaceable, ~6 supplementable, ~63 Forge-curated files. |
| [adapters/vector_store_adapter.md](./adapters/vector_store_adapter.md) | *Design only.* Semantic search augmentation using vector embeddings. Adds `searchSemantic()` as fallback for ContextProvider.search() and MemoryStore.search(). |

### Optimization & Migration

| File | Description |
|------|-------------|
| [shared_loading_patterns.md](./shared_loading_patterns.md) | Three reusable patterns (Standard Memory Loading, Standard Context Loading, Standard Memory Update) that replace 15-35 lines of boilerplate per skill with ~5-line references |
| [performance_benchmarks.md](./performance_benchmarks.md) | Token usage baselines across 81 context files, boilerplate metrics for 22 skills, context loading cost analysis, and success metrics tracking |
| [deprecation_rules.md](./deprecation_rules.md) | 12 deprecated patterns with detection regex, severity levels, replacements, bash linting commands, and full lint script design |
| [migration_guide.md](./migration_guide.md) | Step-by-step migration guide for converting skills, commands, and agents to interface-based patterns |

### Verification

| File | Description |
|------|-------------|
| [verification.md](./verification.md) | Phase 1 verification checklist |
| [phase2_verification.md](./phase2_verification.md) | Phase 2 verification checklist |
| [phase3_verification.md](./phase3_verification.md) | Phase 3 verification checklist |
| [phase4_verification.md](./phase4_verification.md) | Phase 4 verification checklist |
| [phase5_verification.md](./phase5_verification.md) | Phase 5 verification checklist |

## Current State (Phases 1-5 Complete)

| Phase | Deliverables | Status |
|-------|-------------|--------|
| **Phase 1**: Foundation | 4 interfaces, 2 adapters, 3 schemas | ✅ Complete |
| **Phase 2**: Pilot Migration | 3 skills + 1 command + 1 agent migrated, migration guide | ✅ Complete |
| **Phase 3**: Core Migration | 6 components migrated, 81 context files with full frontmatter | ✅ Complete |
| **Phase 4**: Complete Migration | All 22 skills, 12 commands, 11 agents migrated; ExecutionContext | ✅ Complete |
| **Phase 5**: Optimization | Performance baselines, shared loading patterns, 4 adapter specs, deprecation rules | ✅ Complete |
| **Phase 6**: Hooks | 20 hooks across 9 events, 4 layers (Shield, Chronicle, Foreman, Town Crier) | ✅ Complete |
| **Phase 7**: Documentation | Grand Reforging of all public-facing docs | ✅ Complete |
