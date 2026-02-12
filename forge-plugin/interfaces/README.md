# Forge Interfaces

This directory contains the **interface contracts** that decouple all Forge consumers (skills, commands, agents) from direct filesystem paths. The interface layer provides consistent access patterns, validated metadata, and extensibility through swappable adapters.

All 102 skills, 12 commands, and 19 agents use these interfaces. The 3 JSON schemas are validated automatically by the [test suite](../tests/README.md).

## Architecture

```
+---------------------------------------------------------+
|                      Consumers                          |
|  +----------+  +----------+  +----------+              |
|  |  Skills   |  | Commands |  |  Agents  |              |
|  |  (102)    |  |  (12)    |  |  (19)    |              |
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
|  |              Adapters (Active)                    |  |
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

**Consumers** call **Interfaces** using documented method contracts. **Adapters** translate those contracts into concrete filesystem operations against `context/`, `memory/`, and `skills/`.

## How Convention-Based Interfaces Work

This is not a runtime system. There is no code, no compiler, no package manager. Interfaces are **documented contracts in markdown** that Claude Code follows as instructions.

The "methods" described in each interface spec (e.g., `ContextProvider.getCatalog()`) are conceptual operations. When Claude Code encounters a skill or command that needs context, it performs the equivalent file reads and writes according to the documented contract. The interface specs standardize *what* information is available and *how* to access it, while the adapter docs map those operations to specific file paths and formats.

This approach works because Claude Code is an instruction-following system. The interface specs formalize patterns defined in `loading_protocol.md`, `lifecycle.md`, and `SKILL_TEMPLATE.md`.

## Interface–Documentation Mapping

Each interface formalizes and extends existing Forge documentation:

| Interface | Formalizes | Adds |
|-----------|------------|------|
| **ContextProvider** | `context/loading_protocol.md` (5-step protocol) | Zero-token metadata via `getReference()`, partial loading via `materializeSections()`, keyword search via `search()` |
| **MemoryStore** | `memory/lifecycle.md` + `memory/quality_guidance.md` | Structured CRUD operations, automatic timestamp management, staleness queries |
| **SkillInvoker** | `skills/SKILL_TEMPLATE.md` (delegation patterns) | Structured `SkillResult` return type, skill discovery via `getAvailableSkills()`, domain-based filtering |
| **Schemas** | YAML frontmatter in context/agent files | Formal JSON Schema validation for `context_metadata`, `memory_entry`, `agent_config` |

## Directory Structure

```
interfaces/
├── README.md                              This file — architecture overview
├── context_provider.md                    ContextProvider interface spec
├── memory_store.md                        MemoryStore interface spec
├── skill_invoker.md                       SkillInvoker interface spec
├── execution_context.md                   ExecutionContext interface spec
├── schemas/
│   ├── context_metadata.schema.json       Context file frontmatter schema
│   ├── memory_entry.schema.json           Memory entry metadata schema
│   └── agent_config.schema.json           Agent configuration schema
└── adapters/
    ├── markdown_file_context_provider.md   ContextProvider → filesystem mapping
    ├── markdown_file_memory_adapter.md     MemoryStore → filesystem mapping
    ├── cached_context_provider.md          Caching decorator for ContextProvider
    ├── sqlite_memory_adapter.md            SQLite-backed MemoryStore (design only)
    ├── context7_mcp_context_provider.md    Context7 MCP hybrid adapter (design only)
    └── vector_store_adapter.md             Vector embedding search (design only)
```

## Specs Reference

### Core Interfaces

| File | Description |
|------|-------------|
| [context_provider.md](./context_provider.md) | ContextProvider interface: catalog browsing, domain indexes, project type detection, cross-domain loading, reference-based lazy loading, and keyword search |
| [memory_store.md](./memory_store.md) | MemoryStore interface: CRUD operations across 4 memory layers, staleness management, pruning rules, quality checks, and timestamp automation |
| [skill_invoker.md](./skill_invoker.md) | SkillInvoker interface: skill invocation with structured results, delegation patterns for code review and test generation, and skill discovery |
| [execution_context.md](./execution_context.md) | ExecutionContext interface: command chaining with shared state, context caching across commands, and shared data passing |

### Schemas

| File | Description |
|------|-------------|
| [schemas/context_metadata.schema.json](./schemas/context_metadata.schema.json) | JSON Schema (draft-07) validating YAML frontmatter on context files: id, domain, title, type, estimatedTokens, loadingStrategy |
| [schemas/memory_entry.schema.json](./schemas/memory_entry.schema.json) | JSON Schema (draft-07) validating memory entry metadata: project, skill, timestamps, staleness thresholds |
| [schemas/agent_config.schema.json](./schemas/agent_config.schema.json) | JSON Schema (draft-07) validating agent configuration: name, version, context domains, memory categories, skill bindings |

### Adapters — Active

| File | Description |
|------|-------------|
| [adapters/markdown_file_context_provider.md](./adapters/markdown_file_context_provider.md) | Maps ContextProvider methods to filesystem operations against `forge-plugin/context/` |
| [adapters/markdown_file_memory_adapter.md](./adapters/markdown_file_memory_adapter.md) | Maps MemoryStore methods to filesystem operations against `forge-plugin/memory/` |
| [adapters/cached_context_provider.md](./adapters/cached_context_provider.md) | Caching decorator wrapping any ContextProvider with three-tier cache (catalog, reference, content). Session-scoped invalidation. Integrates with ExecutionContext for command chain optimization. |

### Adapters — Future (Design Only)

| File | Description |
|------|-------------|
| [adapters/sqlite_memory_adapter.md](./adapters/sqlite_memory_adapter.md) | SQLite-backed MemoryStore with FTS5 full-text search, SQL-based staleness computation, indexed cross-project queries, and automated pruning via triggers. |
| [adapters/context7_mcp_context_provider.md](./adapters/context7_mcp_context_provider.md) | Hybrid adapter routing framework-specific queries to Context7 MCP server for live docs, with fallback to local files. |
| [adapters/vector_store_adapter.md](./adapters/vector_store_adapter.md) | Semantic search augmentation using vector embeddings. Adds `searchSemantic()` as fallback for ContextProvider.search() and MemoryStore.search(). |

## Testing & Validation

The interface layer is validated by the Forge's [test suite](../tests/README.md) (~1,993 total checks across 2 layers + E2E):

| What's Validated | Test Layer | Test Files |
|------------------|------------|------------|
| All 3 JSON schemas against agent configs, context frontmatter, memory entries | Layer 1 (Static) | `test_json_schemas.py`, `test_yaml_frontmatter.py` |
| Cross-references: skills in agent configs exist, domains exist, memory paths exist | Layer 1 (Static) | `test_cross_references.py` |
| Context loading protocol: domain indexes, `loadingStrategy`, `estimatedTokens` | Layer 2 (Integration) | `test_loading_protocol.py` |
| Cross-domain triggers: format, target resolution, circular reference detection | Layer 2 (Integration) | `test_cross_domain_triggers.py` |
| Memory lifecycle: freshness (0-90+ days), pruning limits, timestamp injection | Layer 2 (Integration) | `test_freshness_lifecycle.py`, `test_pruning_behavior.py`, `test_line_limits.py` |
| Hook enforcement of interface contracts (frontmatter, agent config, memory quality) | Layer 2 (Integration) | 20 hook test modules in `layer2/hooks/` |

Run the full validation:

```bash
# From forge-plugin/
bash tests/run_all.sh --layer2
```

See [tests/README.md](../tests/README.md) for how to run tests.
