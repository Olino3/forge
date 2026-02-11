# Phase 1 Verification Checklist

This document provides a comprehensive checklist for verifying that Phase 1 of the Forge interface layer is complete, correct, and backward-compatible.

## 1. File Existence (10 new files)

All files are relative to `forge-plugin/interfaces/`.

- [ ] `schemas/context_metadata.schema.json`
- [ ] `schemas/memory_entry.schema.json`
- [ ] `schemas/agent_config.schema.json`
- [ ] `context_provider.md`
- [ ] `memory_store.md`
- [ ] `skill_invoker.md`
- [ ] `adapters/markdown_file_context_provider.md`
- [ ] `adapters/markdown_file_memory_adapter.md`
- [ ] `README.md`
- [ ] `verification.md`

```bash
# Verification: check all 10 files exist
for f in \
  schemas/context_metadata.schema.json \
  schemas/memory_entry.schema.json \
  schemas/agent_config.schema.json \
  context_provider.md \
  memory_store.md \
  skill_invoker.md \
  adapters/markdown_file_context_provider.md \
  adapters/markdown_file_memory_adapter.md \
  README.md \
  verification.md; do
  if [ -f "forge-plugin/interfaces/$f" ]; then
    echo "OK   $f"
  else
    echo "MISSING $f"
  fi
done
```

## 2. Schema Validity

Each JSON Schema must be parseable and structurally correct.

### context_metadata.schema.json
- [ ] Valid JSON (parseable with `python3 -m json.tool`)
- [ ] Uses `$schema: "http://json-schema.org/draft-07/schema#"`
- [ ] Has `required` fields defined (id, domain, title, type, estimatedTokens, loadingStrategy)
- [ ] Has proper type constraints on all properties
- [ ] Includes `enum` for domain and type fields

### memory_entry.schema.json
- [ ] Valid JSON (parseable with `python3 -m json.tool`)
- [ ] Uses `$schema: "http://json-schema.org/draft-07/schema#"`
- [ ] Has `required` fields defined
- [ ] Has proper type constraints on all properties
- [ ] Includes staleness thresholds and size limits

### agent_config.schema.json
- [ ] Valid JSON (parseable with `python3 -m json.tool`)
- [ ] Uses `$schema: "http://json-schema.org/draft-07/schema#"`
- [ ] Has `required` fields defined (name, version, context, memory, skills)
- [ ] Has proper type constraints on all properties
- [ ] `context.primaryDomains` enum matches the 9 context domains
- [ ] `memory.categories` uses `[{name, description}]` array format (not map)
- [ ] `permissionMode` enum includes auto, manual, plan

```bash
# Verification: validate all schemas as valid JSON
python3 -m json.tool forge-plugin/interfaces/schemas/context_metadata.schema.json > /dev/null && echo "context_metadata: VALID" || echo "context_metadata: INVALID"
python3 -m json.tool forge-plugin/interfaces/schemas/memory_entry.schema.json > /dev/null && echo "memory_entry: VALID" || echo "memory_entry: INVALID"
python3 -m json.tool forge-plugin/interfaces/schemas/agent_config.schema.json > /dev/null && echo "agent_config: VALID" || echo "agent_config: INVALID"
```

## 3. YAML Frontmatter Validation (5 pilot files)

Five context files receive YAML frontmatter as a pilot demonstration. The body content of each file must remain unchanged.

### forge-plugin/context/python/common_issues.md
- [ ] Starts with `---` on line 1
- [ ] Has closing `---` delimiter
- [ ] Contains `id`, `domain`, `title`, `type`, `estimatedTokens`, `loadingStrategy`
- [ ] `domain` is `"python"`
- [ ] Body content unchanged after frontmatter

### forge-plugin/context/python/fastapi_patterns.md
- [ ] Starts with `---` on line 1
- [ ] Has closing `---` delimiter
- [ ] Contains `id`, `domain`, `title`, `type`, `estimatedTokens`, `loadingStrategy`
- [ ] `domain` is `"python"`
- [ ] Body content unchanged after frontmatter

### forge-plugin/context/security/security_guidelines.md
- [ ] Starts with `---` on line 1
- [ ] Has closing `---` delimiter
- [ ] Contains `id`, `domain`, `title`, `type`, `estimatedTokens`, `loadingStrategy`
- [ ] `domain` is `"security"`
- [ ] Body content unchanged after frontmatter

### forge-plugin/context/engineering/code_review_principles.md
- [ ] Starts with `---` on line 1
- [ ] Has closing `---` delimiter
- [ ] Contains `id`, `domain`, `title`, `type`, `estimatedTokens`, `loadingStrategy`
- [ ] `domain` is `"engineering"`
- [ ] Body content unchanged after frontmatter

### forge-plugin/context/python/index.md
- [ ] Starts with `---` on line 1
- [ ] Has closing `---` delimiter
- [ ] Contains `id`, `domain`, `title`, `type`, `estimatedTokens`, `loadingStrategy`
- [ ] `domain` is `"python"`
- [ ] `type` is `"index"`
- [ ] Body content unchanged after frontmatter

```bash
# Verification: check frontmatter delimiters
for f in \
  forge-plugin/context/python/common_issues.md \
  forge-plugin/context/python/fastapi_patterns.md \
  forge-plugin/context/security/security_guidelines.md \
  forge-plugin/context/engineering/code_review_principles.md \
  forge-plugin/context/python/index.md; do
  FIRST_LINE=$(head -1 "$f")
  if [ "$FIRST_LINE" = "---" ]; then
    echo "OK   $f (starts with ---)"
  else
    echo "FAIL $f (first line: $FIRST_LINE)"
  fi
done
```

## 4. Interface Coverage - ContextProvider

The ContextProvider interface must map to the existing 5-step loading protocol while adding new capabilities.

### Existing protocol coverage (loading_protocol.md)
- [ ] `getCatalog()` maps to scanning `context/` directories for available files
- [ ] `getDomainIndex(domain)` maps to loading_protocol.md Step 1 (read domain index)
- [ ] `getAlwaysLoadFiles()` maps to loading_protocol.md Step 2 (load essential files)
- [ ] `detectProjectType(projectPath)` maps to loading_protocol.md Step 3 (detect language/framework)
- [ ] `getConditionalContext(triggers)` maps to loading_protocol.md Step 4 (load conditional files)
- [ ] `getCrossDomainContext(primaryDomain)` maps to loading_protocol.md Step 5 (cross-domain triggers)

### New capabilities (Phase 1 additions)
- [ ] `getReference(fileId)` enables zero-token metadata access without loading full content
- [ ] `materialize(fileId)` loads full content from a reference
- [ ] `materializeSections(fileId, sections)` loads partial content by section headers
- [ ] `search(keywords, options)` enables keyword-based discovery across context files

## 5. Interface Coverage - MemoryStore

The MemoryStore interface must cover all rules from `lifecycle.md` and `quality_guidance.md`.

### Staleness management (lifecycle.md)
- [ ] Covers staleness thresholds: fresh (<7 days), aging (7-30 days), stale (>30 days)
- [ ] Covers pruning rules for `review_history` (keep last 10 entries)
- [ ] Covers pruning rules for `known_issues` (remove resolved >30 days)
- [ ] Covers pruning rules for `common_patterns` (merge duplicates, cap at 20)
- [ ] Covers pruning rules for `test_results_history` (keep last 5 runs)
- [ ] Covers size limits: 500 lines total, 200 for overview, 300 for history

### Quality checks (quality_guidance.md)
- [ ] Covers completeness check (all required sections present)
- [ ] Covers accuracy check (information matches current codebase)
- [ ] Covers specificity check (entries contain concrete examples)
- [ ] Covers growth check (memory should expand with new insights)

### Memory layers
- [ ] Covers shared-project layer (`memory/projects/{project}/`)
- [ ] Covers skill-specific layer (`memory/skills/{skill}/{project}/`)
- [ ] Covers command layer (`memory/commands/{project}/`)
- [ ] Covers agent layer (`memory/agents/{agent}/`)

### Timestamp management
- [ ] Covers auto-add timestamps on write operations
- [ ] Covers auto-update timestamps on modifications

## 6. Interface Coverage - SkillInvoker

The SkillInvoker interface must formalize skill delegation patterns from `SKILL_TEMPLATE.md`.

### Core methods
- [ ] `invoke(skillName, params)` returns structured `SkillResult` with status, output path, summary, and findings
- [ ] `delegateAnalysis(skillName, target, options)` covers code review delegation (python-code-review, dotnet-code-review, angular-code-review)
- [ ] `delegateTestGeneration(skillName, target, options)` covers test generation delegation (generate-python-unit-tests, generate-jest-unit-tests)

### Discovery methods
- [ ] `getSkillMetadata(skillName)` provides skill version, description, required context, and supported project types
- [ ] `getAvailableSkills(filter)` lists skills filterable by domain (review, testing, infrastructure, analysis, productivity, data-science, meta)

## 7. Backward Compatibility

Phase 1 must not modify any existing consumer files.

### No modifications to consumers
- [ ] No existing `skills/*/SKILL.md` files modified
- [ ] No existing `commands/*/COMMAND.md` files modified
- [ ] No existing `agents/*.md` files modified
- [ ] No `plugin.json` modified
- [ ] No `settings.local.json` modified

### Context file body preservation
- [ ] `context/python/common_issues.md` body content unchanged (only frontmatter prepended)
- [ ] `context/python/fastapi_patterns.md` body content unchanged (only frontmatter prepended)
- [ ] `context/security/security_guidelines.md` body content unchanged (only frontmatter prepended)
- [ ] `context/engineering/code_review_principles.md` body content unchanged (only frontmatter prepended)
- [ ] `context/python/index.md` body content unchanged (only frontmatter prepended)

```bash
# Verification: check that only expected files changed
git diff --name-only
# Expected output should include only:
#   forge-plugin/context/python/common_issues.md         (frontmatter added)
#   forge-plugin/context/python/fastapi_patterns.md      (frontmatter added)
#   forge-plugin/context/security/security_guidelines.md (frontmatter added)
#   forge-plugin/context/engineering/code_review_principles.md (frontmatter added)
#   forge-plugin/context/python/index.md                 (frontmatter added)
# Plus 10 new files in forge-plugin/interfaces/
```

```bash
# Verification: confirm body content is unchanged (frontmatter adds lines at top only)
# For each pilot file, the diff should show only added lines (no deletions or modifications)
git diff forge-plugin/context/python/common_issues.md | head -30
git diff forge-plugin/context/python/fastapi_patterns.md | head -30
git diff forge-plugin/context/security/security_guidelines.md | head -30
git diff forge-plugin/context/engineering/code_review_principles.md | head -30
git diff forge-plugin/context/python/index.md | head -30
```

## 8. Adapter Completeness

Both adapters must fully map their parent interface to filesystem operations.

### MarkdownFileContextProvider
- [ ] Maps ALL ContextProvider methods to file operations
- [ ] Documents path construction rules (e.g., `context/{domain}/{filename}`)
- [ ] Includes before/after examples showing old path vs. interface call
- [ ] Describes YAML frontmatter parsing for metadata extraction
- [ ] Explains fallback behavior when frontmatter is absent

### MarkdownFileMemoryAdapter
- [ ] Maps ALL MemoryStore methods to file operations
- [ ] Documents path construction rules for all 4 memory layers
- [ ] Includes before/after examples showing old path vs. interface call
- [ ] Describes timestamp format and auto-management
- [ ] Explains staleness calculation from file timestamps

## Summary

| Category | Items | Description |
|----------|-------|-------------|
| File Existence | 10 | All interface files created |
| Schema Validity | 3 | All JSON schemas parse and validate |
| YAML Frontmatter | 5 | Pilot files have valid frontmatter |
| ContextProvider | 10 | All methods documented and mapped |
| MemoryStore | 15 | All rules, layers, and operations covered |
| SkillInvoker | 5 | All methods documented |
| Backward Compatibility | 10 | Zero consumer changes verified |
| Adapter Completeness | 8 | Both adapters fully map their interface |
| **Total** | **66** | **Verification items** |
