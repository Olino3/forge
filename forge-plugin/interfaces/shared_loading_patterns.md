# Shared Loading Patterns

Version: 1.0.0
Status: Phase 5 - Optimization
Last Updated: 2026-02-11

---

## Overview

Three reusable patterns that skills reference instead of repeating inline. Each pattern replaces 15-35 lines of boilerplate with a ~5-line reference, reducing total boilerplate across 22 skills by approximately 66%.

---

## Pattern 1: Standard Memory Loading

**Replaces**: Steps 2.1-2.5 in SKILL_TEMPLATE.md (~15-25 lines per skill)
**Reduced to**: ~5 lines

### Steps

1. Determine project name from git repository root or user input
2. Load skill memory: `memoryStore.getSkillMemory("{this-skill}", "{project}")`
3. Load shared project memory: `memoryStore.getSharedProjectMemory("{project}")`
4. Optionally load cross-project memory: `memoryStore.getByProject("{project}")`
5. Check staleness of loaded entries; flag stale entries for verification

### Interface Calls

| Step | Method | Returns |
|------|--------|---------|
| 1 | (project detection from git root or user input) | `projectName: string` |
| 2 | `memoryStore.getSkillMemory(skill, project)` | `MemoryEntry[]` |
| 3 | `memoryStore.getSharedProjectMemory(project)` | `MemoryEntry[]` |
| 4 | `memoryStore.getByProject(project)` (optional) | `{ shared, skills, commands }` |
| 5 | (check `.staleness` field on returned entries) | Advisory only |

### Before/After

**Before** (~20 lines in each SKILL.md):
```markdown
### Step 2: Load Indexes & Memory

1. Determine project name from git repository or directory
2. Load skill memory: `memoryStore.getSkillMemory("{this-skill}", "{project}")`
3. Load shared project memory: `memoryStore.getSharedProjectMemory("{project}")`
4. Load context protocol: `contextProvider.getLoadingProtocol()`
5. Load domain index: `contextProvider.getDomainIndex("{domain}")`

**YOU MUST:**
1. **CHECK PROJECT MEMORY FIRST**:
   - Identify the project name from the repository root or ask the user
   - Use `memoryStore.getSkillMemory("{this-skill}", "{project-name}")` to load project-specific patterns
   - **Cross-skill discovery**: Use `memoryStore.getByProject("{project-name}")` to check for insights from other skills
   - If memory exists: Review previously learned patterns, frameworks, and project-specific context
   - If no memory exists: Note this is first invocation, memory will be created later
2. **USE CONTEXT INDEXES FOR EFFICIENT LOADING**:
   - Use `contextProvider.getDomainIndex("{domain}")` to understand context files
   - Determine which specific files to load based on the index
```

**After** (~5 lines in each SKILL.md):
```markdown
### Step 2: Load Memory
> Follow [Standard Memory Loading](../../interfaces/shared_loading_patterns.md#pattern-1-standard-memory-loading)
> with `skill="{this-skill}"` and `project` detected from git root.
```

---

## Pattern 2: Standard Context Loading

**Replaces**: Steps 3.1-3.5 in SKILL_TEMPLATE.md (~20-35 lines per skill)
**Reduced to**: ~5 lines

### Steps

1. Load domain index: `contextProvider.getDomainIndex("{domain}")`
2. Load always-load files: `contextProvider.getAlwaysLoadFiles("{domain}")`
3. Detect project type: `contextProvider.detectProjectType("{domain}", signals)`
4. Load conditional context: `contextProvider.getConditionalContext("{domain}", detection)`
5. Check cross-domain needs: `contextProvider.getCrossDomainContext("{domain}", triggers)`

### Interface Calls

| Step | Method | Returns |
|------|--------|---------|
| 1 | `contextProvider.getDomainIndex(domain)` | `DomainIndex` |
| 2 | `contextProvider.getAlwaysLoadFiles(domain)` | `ContextFile[]` |
| 3 | `contextProvider.detectProjectType(domain, signals)` | `ProjectTypeDetection` |
| 4 | `contextProvider.getConditionalContext(domain, detection)` | `ContextFile[]` |
| 5 | `contextProvider.getCrossDomainContext(domain, triggers)` | `ContextFile[]` |

### Token Budget Enforcement

Total loaded files should stay within the 4-6 file budget declared in skill frontmatter. The ContextProvider respects the `file_budget` value from YAML frontmatter and prioritizes files by relevance.

### Before/After

**Before** (~25 lines in each SKILL.md):
```markdown
### Step 3: Read Relevant Context Files

**YOU MUST use the indexes to load only relevant files**:

1. **ALWAYS**: Use `contextProvider.getAlwaysLoadFiles("{domain}")` to load universal patterns
2. **Based on framework detected**: Use `contextProvider.getConditionalContext("{domain}", detection)`:
   - **If Django detected**: Loads `django_patterns.md`
   - **If Flask detected**: Loads `flask_patterns.md`
   - **If FastAPI detected**: Loads `fastapi_patterns.md`
   - **If data science detected**: Loads `datascience_patterns.md`
3. **For security-sensitive code**: Use `contextProvider.getCrossDomainContext("{domain}", triggers)`:
   - Auth/authorization code: Loads security files
   - User input handling: Loads `security_guidelines.md`
   - Database queries: Loads `security_guidelines.md`
4. **Stay within file budget** declared in frontmatter

**Progressive loading**: Only load files relevant to the detected framework.
```

**After** (~5 lines in each SKILL.md):
```markdown
### Step 3: Load Context
> Follow [Standard Context Loading](../../interfaces/shared_loading_patterns.md#pattern-2-standard-context-loading)
> for the `{domain}` domain. Stay within the file budget declared in frontmatter.
```

---

## Pattern 3: Standard Memory Update

**Replaces**: Step N in SKILL_TEMPLATE.md (~15-25 lines per skill)
**Reduced to**: ~5 lines

### Steps

1. Update skill-specific memory: `memoryStore.update(layer="skill-specific", skill="{this-skill}", project="{project}", ...)`
2. Update shared project memory if new project-level insights were learned: `memoryStore.update(layer="shared-project", project="{project}", ...)`
3. Timestamps and staleness tracking are handled automatically by MemoryStore

### Interface Calls

| Step | Method | Parameters |
|------|--------|-----------|
| 1 | `memoryStore.update(layer, skill, project, filename, content)` | `layer="skill-specific"` |
| 2 | `memoryStore.update(layer, project, filename, content)` | `layer="shared-project"` (conditional) |
| 3 | (automatic) | Timestamps injected by MemoryStore |

### What to Store

Skills should update memory with:
- **Skill-specific memory**: Patterns discovered, conventions learned, review history, framework configuration
- **Shared project memory**: Project-level insights that benefit other skills (architecture, deployment info, coding conventions)

### Before/After

**Before** (~20 lines in each SKILL.md):
```markdown
### Step N: Update Memory

**After completing the review, UPDATE PROJECT MEMORY**:

Use `memoryStore.update("{this-skill}", "{project-name}", ...)` to create or update memory files:

1. **project_overview**: Framework, architecture patterns, deployment info
2. **common_patterns**: Project-specific coding patterns and conventions discovered
3. **known_issues**: Recurring issues or anti-patterns found in this project
4. **review_history**: Summary of reviews performed with dates and key findings

Timestamps and staleness tracking are managed automatically by MemoryStore.
See [MemoryStore Interface](../../interfaces/memory_store.md) for `update()` and `append()` method details.
```

**After** (~5 lines in each SKILL.md):
```markdown
### Step N: Update Memory
> Follow [Standard Memory Update](../../interfaces/shared_loading_patterns.md#pattern-3-standard-memory-update)
> for `skill="{this-skill}"`. Store any newly learned patterns, conventions, or project insights.
```

---

## Usage in Skills

Skills reference these patterns instead of repeating the steps:

### Step 2: Load Memory
> Follow [Standard Memory Loading](../../interfaces/shared_loading_patterns.md#pattern-1-standard-memory-loading) with `skill="{this-skill}"` and `domain="{domain}"`.

### Step 3: Load Context
> Follow [Standard Context Loading](../../interfaces/shared_loading_patterns.md#pattern-2-standard-context-loading) for the `{domain}` domain. Stay within the file budget declared in frontmatter.

### Step N: Update Memory
> Follow [Standard Memory Update](../../interfaces/shared_loading_patterns.md#pattern-3-standard-memory-update) for `skill="{this-skill}"`.

---

## Impact Metrics

| Metric | Before | After | Improvement |
|--------|--------|-------|-------------|
| Avg boilerplate per complex skill | ~55 lines | ~15 lines | -73% |
| Avg boilerplate per medium skill | ~35 lines | ~12 lines | -66% |
| Total boilerplate across 22 skills | ~770 lines | ~264 lines | -66% |
| Consistency across skills | Variable | Uniform | Standardized |
| Time to add memory/context to new skill | ~30 min | ~5 min | -83% |

---

## Interface References

- **MemoryStore**: [memory_store.md](memory_store.md) -- all memory operations
- **ContextProvider**: [context_provider.md](context_provider.md) -- all context operations
- **Migration Guide**: [migration_guide.md](migration_guide.md) -- full migration patterns
- **Performance Benchmarks**: [performance_benchmarks.md](performance_benchmarks.md) -- token and boilerplate baselines
