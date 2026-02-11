# ContextProvider Interface

Version: 1.0.0
Status: Specification
Last Updated: 2026-02-10

---

## Overview

The `ContextProvider` interface defines how Forge skills and commands discover, query, and load context files. It wraps and extends the existing 5-step [Context Loading Protocol](../context/loading_protocol.md), replacing hardcoded file paths with structured method calls.

### Design Goals

1. **Decouple skills from filesystem paths** -- Skills call `ContextProvider.getAlwaysLoadFiles("python")` instead of `Read ../../context/python/common_issues.md`.
2. **Enable selective loading** -- Load metadata first (0 tokens), then materialize only what is needed.
3. **Preserve the 5-step protocol** -- Every method maps to a protocol step; the protocol remains the authoritative workflow.
4. **Support search and discovery** -- Skills can find context by keyword or tag without knowing file locations.

### Relationship to Loading Protocol

| Protocol Step | ContextProvider Method(s) |
|---|---|
| Step 1: Read Domain Index | `getDomainIndex(domain)` |
| Step 2: Load "Always" Files | `getAlwaysLoadFiles(domain)` |
| Step 3: Detect Project Type | `detectProjectType(domain, signals)` |
| Step 4: Load Conditional Context | `getConditionalContext(domain, detection)` |
| Step 5: Check Cross-Domain | `getCrossDomainContext(domain, triggers)` |
| (New) Metadata-only access | `getReference(domain, file)` |
| (New) Deferred materialization | `materialize(reference)`, `materializeSections(ref, sections[])` |
| (New) Discovery | `search(query, domain?)`, `getCatalog(domain?)` |

---

## Methods

### 1. getCatalog(domain?)

Scan context directories and return a catalog of all context files with their metadata.

**Purpose**: Provide a complete inventory of available context for planning which files to load.

**Parameters**:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `domain` | `string` | No | If provided, limit catalog to this domain. If omitted, return all domains. |

**Returns**: `ContextCatalogEntry[]`

| Field | Type | Description |
|---|---|---|
| `id` | `string` | Unique identifier (e.g., `python/common_issues`) |
| `domain` | `string` | Domain this file belongs to |
| `title` | `string` | Human-readable title |
| `type` | `string` | File type: `always`, `framework`, `reference`, `pattern`, `index`, `detection` |
| `estimatedTokens` | `integer` | Approximate token cost to load |
| `loadingStrategy` | `string` | When to load: `always`, `onDemand`, `lazy` |
| `path` | `string` | Relative path from `context/` root |
| `tags` | `string[]` | Searchable tags |

**Before/After**:

```
BEFORE:
  Read ../../context/python/index.md
  (manually parse the index to find all files)
  Read ../../context/python/common_issues.md
  Read ../../context/python/fastapi_patterns.md
  ...

AFTER:
  catalog = ContextProvider.getCatalog("python")
  // Returns structured list of all 14 Python context files with metadata
  // No file content loaded yet -- just metadata
```

---

### 2. getDomainIndex(domain)

Return the structured domain index, providing navigation guidance for a specific domain.

**Purpose**: Maps to Protocol Step 1. Returns the domain's `index.md` content as structured data including file descriptions, loading workflows, and detection hints.

**Parameters**:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `domain` | `string` | Yes | Domain to retrieve index for. One of: `engineering`, `angular`, `azure`, `commands`, `dotnet`, `git`, `python`, `schema`, `security` |

**Returns**: `DomainIndex`

| Field | Type | Description |
|---|---|---|
| `domain` | `string` | Domain name |
| `files` | `FileEntry[]` | All files in this domain with purpose descriptions |
| `workflows` | `WorkflowEntry[]` | Recommended loading workflows |
| `detectionHints` | `DetectionHint[]` | Code patterns that map to specific files |

**Before/After**:

```
BEFORE:
  Read ../../context/python/index.md
  (manually scan the document for relevant sections)

AFTER:
  index = ContextProvider.getDomainIndex("python")
  // Returns structured index with file list, workflows, and detection hints
```

---

### 3. getLoadingProtocol()

Return the standardized 5-step loading protocol.

**Purpose**: Provide the loading protocol as structured data so skills can programmatically follow the steps.

**Parameters**: None.

**Returns**: `LoadingProtocol`

| Field | Type | Description |
|---|---|---|
| `steps` | `ProtocolStep[]` | Ordered list of protocol steps with descriptions and actions |
| `tokenBudget` | `integer` | Recommended max files per invocation (4-6) |
| `priorityOrder` | `string[]` | Priority for file selection when over budget |

**Before/After**:

```
BEFORE:
  Read ../../context/loading_protocol.md
  (manually follow the prose instructions)

AFTER:
  protocol = ContextProvider.getLoadingProtocol()
  // Returns structured steps, token budget, and priority rules
```

---

### 4. getAlwaysLoadFiles(domain)

Load all context files marked with `loadingStrategy: "always"` for a given domain.

**Purpose**: Maps to Protocol Step 2. Returns the content of files that every invocation in this domain should load (e.g., `common_issues.md` for Python).

**Parameters**:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `domain` | `string` | Yes | Domain to load always-load files for |

**Returns**: `ContextFile[]`

| Field | Type | Description |
|---|---|---|
| `id` | `string` | File identifier (e.g., `python/common_issues`) |
| `title` | `string` | Human-readable title |
| `content` | `string` | Full file content (body only, frontmatter stripped) |
| `estimatedTokens` | `integer` | Token cost of the returned content |
| `metadata` | `object` | Full YAML frontmatter as structured data |

**Before/After**:

```
BEFORE:
  Read ../../context/python/common_issues.md
  Read ../../context/python/context_detection.md

AFTER:
  files = ContextProvider.getAlwaysLoadFiles("python")
  // Returns content of common_issues.md and context_detection.md
  // Both are loadingStrategy: "always" in the python domain
```

---

### 5. detectProjectType(domain, signals)

Run detection logic to identify the project's framework, libraries, and architecture.

**Purpose**: Maps to Protocol Step 3. Uses the domain's `context_detection.md` logic to classify the project based on provided code signals.

**Parameters**:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `domain` | `string` | Yes | Domain to run detection for |
| `signals` | `DetectionSignals` | Yes | Code signals to analyze |

`DetectionSignals`:

| Field | Type | Description |
|---|---|---|
| `imports` | `string[]` | Import statements found in the code |
| `filePatterns` | `string[]` | File names/paths in the project |
| `codePatterns` | `string[]` | Code snippets or patterns detected |
| `configFiles` | `string[]` | Configuration files present (e.g., `pyproject.toml`, `angular.json`) |

**Returns**: `DetectionResult`

| Field | Type | Description |
|---|---|---|
| `framework` | `string` | Detected framework (e.g., `fastapi`, `django`, `angular`) |
| `libraries` | `string[]` | Detected libraries (e.g., `sqlalchemy`, `pydantic`) |
| `architecture` | `string` | Detected architecture pattern |
| `testingFramework` | `string` | Detected testing framework |
| `recommendedFiles` | `string[]` | Context file IDs recommended for loading |

**Before/After**:

```
BEFORE:
  Read ../../context/python/context_detection.md
  (manually check each detection pattern against the code)
  # Found: "from fastapi import" -> load fastapi_patterns.md

AFTER:
  detection = ContextProvider.detectProjectType("python", {
    imports: ["from fastapi import FastAPI", "from pydantic import BaseModel"],
    filePatterns: ["main.py", "models.py", "routers/"],
    configFiles: ["pyproject.toml"]
  })
  // Returns: { framework: "fastapi", libraries: ["pydantic"], recommendedFiles: ["python/fastapi_patterns"] }
```

---

### 6. getConditionalContext(domain, detection)

Load framework-specific and library-specific context files based on detection results.

**Purpose**: Maps to Protocol Step 4. Loads the context files recommended by `detectProjectType()`, respecting the 4-6 file token budget.

**Parameters**:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `domain` | `string` | Yes | Domain to load conditional context from |
| `detection` | `DetectionResult` | Yes | Result from `detectProjectType()` |

**Returns**: `ContextFile[]`

Same structure as `getAlwaysLoadFiles()` return type. Returns at most 4-6 files, prioritized by relevance.

**Before/After**:

```
BEFORE:
  # Based on manual detection of FastAPI...
  Read ../../context/python/fastapi_patterns.md
  # Manually decide if I need more files...
  Read ../../context/python/datascience_patterns.md  (maybe not needed?)

AFTER:
  files = ContextProvider.getConditionalContext("python", detection)
  // Returns exactly the files needed based on detection, within token budget
  // e.g., [fastapi_patterns.md] -- only what was detected
```

---

### 7. getCrossDomainContext(domain, triggers)

Load secondary context files from other domains based on cross-domain trigger conditions.

**Purpose**: Maps to Protocol Step 5. Uses `cross_domain.md` logic to determine which files from other domains should also be loaded.

**Parameters**:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `domain` | `string` | Yes | Primary domain being analyzed |
| `triggers` | `string[]` | Yes | Detected trigger conditions (e.g., `["auth_code", "sql_queries"]`) |

**Returns**: `ContextFile[]`

Same structure as `getAlwaysLoadFiles()` return type.

**Before/After**:

```
BEFORE:
  Read ../../context/cross_domain.md
  (manually check: "Python + auth code -> load security_guidelines.md")
  Read ../../context/security/security_guidelines.md

AFTER:
  files = ContextProvider.getCrossDomainContext("python", ["auth_code", "sql_queries"])
  // Returns: [security_guidelines.md] -- automatically resolved from cross_domain.md
```

---

### 8. getReference(domain, file)

Return metadata for a context file without loading its content.

**Purpose**: Enable zero-cost inspection of context files. Skills can check file metadata (token count, sections, tags) before deciding whether to load the full content.

**Parameters**:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `domain` | `string` | Yes | Domain the file belongs to |
| `file` | `string` | Yes | Filename without extension (e.g., `fastapi_patterns`) |

**Returns**: `ContextReference`

| Field | Type | Description |
|---|---|---|
| `id` | `string` | File identifier |
| `domain` | `string` | Domain |
| `title` | `string` | Human-readable title |
| `type` | `string` | File type |
| `estimatedTokens` | `integer` | Token cost if materialized |
| `loadingStrategy` | `string` | Loading strategy |
| `sections` | `SectionRef[]` | Available sections with names, token costs, and keywords |
| `tags` | `string[]` | Searchable tags |
| `crossDomainTriggers` | `string[]` | Related files in other domains |
| `detectionTriggers` | `string[]` | Code patterns that trigger this file |
| `path` | `string` | Resolved filesystem path |

**Before/After**:

```
BEFORE:
  Read ../../context/python/fastapi_patterns.md
  // Loaded entire file (400 tokens) just to check if it's relevant

AFTER:
  ref = ContextProvider.getReference("python", "fastapi_patterns")
  // Returns metadata only (0 tokens of content loaded)
  // ref.estimatedTokens = 400, ref.tags = ["python", "fastapi", "pydantic", "async", "api"]
  // Now decide: do I need this file?
```

---

### 9. materialize(reference)

Load the full content of a context file from its reference.

**Purpose**: Deferred loading. After inspecting a reference from `getReference()`, load the full content when ready.

**Parameters**:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `reference` | `ContextReference` | Yes | Reference obtained from `getReference()` |

**Returns**: `ContextFile`

Same structure as individual entries in `getAlwaysLoadFiles()` return type. Content is the full file body with frontmatter stripped.

**Before/After**:

```
BEFORE:
  Read ../../context/python/fastapi_patterns.md
  // Always loads entire file immediately

AFTER:
  ref = ContextProvider.getReference("python", "fastapi_patterns")
  // Check: ref.estimatedTokens = 400, relevant tags found
  file = ContextProvider.materialize(ref)
  // Now load the content -- deliberate, informed decision
```

---

### 10. materializeSections(reference, sections[])

Load only specific named sections from a context file.

**Purpose**: Fine-grained loading. When a file has multiple sections but only some are relevant, load just those sections to reduce token usage.

**Parameters**:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `reference` | `ContextReference` | Yes | Reference obtained from `getReference()` |
| `sections` | `string[]` | Yes | Names of sections to load (must match section names in frontmatter) |

**Returns**: `PartialContextFile`

| Field | Type | Description |
|---|---|---|
| `id` | `string` | File identifier |
| `title` | `string` | Human-readable title |
| `sections` | `SectionContent[]` | Loaded sections with name and content |
| `totalTokens` | `integer` | Token cost of the loaded sections |
| `metadata` | `object` | Full YAML frontmatter |

**Before/After**:

```
BEFORE:
  Read ../../context/python/fastapi_patterns.md
  // Loaded all 400 tokens, but only needed the "Security Issues" section (~60 tokens)

AFTER:
  ref = ContextProvider.getReference("python", "fastapi_patterns")
  partial = ContextProvider.materializeSections(ref, ["Security Issues"])
  // Loaded only the "Security Issues" section -- ~60 tokens instead of 400
```

---

### 11. search(query, domain?)

Search context files by keyword, tag, or content pattern.

**Purpose**: Discovery. Find relevant context files without knowing their names or locations. Searches across tags, section keywords, titles, and detection triggers.

**Parameters**:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `query` | `string` | Yes | Search query (matches against tags, keywords, titles, detection triggers) |
| `domain` | `string` | No | If provided, limit search to this domain |

**Returns**: `SearchResult[]`

| Field | Type | Description |
|---|---|---|
| `reference` | `ContextReference` | Reference to the matching file |
| `relevance` | `float` | Relevance score (0.0 to 1.0) |
| `matchedOn` | `string[]` | What matched: `tag`, `keyword`, `title`, `detectionTrigger` |

Results are sorted by relevance score, descending.

**Before/After**:

```
BEFORE:
  Read ../../context/python/index.md
  (manually scan index for "security" or "auth" related files)
  (check cross_domain.md for additional security context)
  Read ../../context/security/security_guidelines.md

AFTER:
  results = ContextProvider.search("sql injection security")
  // Returns ranked results:
  //   1. security/security_guidelines (relevance: 0.95, matched: tag, keyword)
  //   2. python/fastapi_patterns (relevance: 0.6, matched: section keyword "sql-injection")
  //   3. dotnet/security_patterns (relevance: 0.55, matched: tag)
```

---

## Complete 5-Step Workflow Example

Demonstrates how a skill uses `ContextProvider` to follow the full loading protocol.

```
// Step 1: Read Domain Index
index = ContextProvider.getDomainIndex("python")

// Step 2: Load Always Files
alwaysFiles = ContextProvider.getAlwaysLoadFiles("python")
// Loaded: common_issues.md, context_detection.md

// Step 3: Detect Project Type
detection = ContextProvider.detectProjectType("python", {
  imports: ["from fastapi import FastAPI", "from sqlalchemy import Column"],
  filePatterns: ["app/main.py", "app/models/user.py"],
  configFiles: ["pyproject.toml"]
})
// Detected: framework=fastapi, libraries=[sqlalchemy, pydantic]

// Step 4: Load Conditional Context
conditionalFiles = ContextProvider.getConditionalContext("python", detection)
// Loaded: fastapi_patterns.md

// Step 5: Cross-Domain Context
crossDomainFiles = ContextProvider.getCrossDomainContext("python", ["sql_queries", "auth_code"])
// Loaded: security/security_guidelines.md

// Total files loaded: 4 (within 4-6 budget)
// Total tokens: ~1400 (common_issues=350 + context_detection=200 + fastapi=400 + security=250)
```

---

## Error Handling

| Scenario | Behavior |
|---|---|
| Domain not found | Return empty result with warning |
| File missing frontmatter | Derive metadata from file footer (see adapter docs) |
| Section name not found | Return empty section list with warning |
| No detection file for domain | Skip detection, return empty `DetectionResult` |
| Token budget exceeded | Truncate to highest-priority files, attach warning |

---

## Implementation Notes

- The current implementation is `MarkdownFileContextProvider` (see `adapters/markdown_file_context_provider.md`).
- All file paths are resolved relative to `forge-plugin/context/`.
- YAML frontmatter is parsed from the `---` delimiters at the start of each file.
- Files without frontmatter fall back to footer-based metadata extraction.
- The `ContextReference` is lightweight and carries no file content -- it is safe to hold many references without token cost.

### Caching

Context loading can be accelerated with the `CachedContextProvider` adapter (see `adapters/cached_context_provider.md`), which wraps any ContextProvider implementation with a three-tier cache:
- **Tier 1 (Catalog)**: Domain metadata cached after first `getCatalog()` or `getDomainIndex()` call
- **Tier 2 (Reference)**: File metadata cached after first `getReference()` call
- **Tier 3 (Content)**: Materialized content cached after first `materialize()` or `getAlwaysLoadFiles()` call

Cache is session-scoped (discarded at session end) and integrates with `ExecutionContext.recordContextLoad()`/`getCachedContext()` for command chain optimization. See the [CachedContextProvider adapter spec](adapters/cached_context_provider.md) for full details.

---

*Last Updated: 2026-02-11*
