---
name: "jquery-4"
description: "Migrate jQuery 3.x to 4.0.0 safely in WordPress and legacy web projects. Covers all breaking changes: removed APIs ($.isArray, $.trim, $.parseJSON, $.type, $.isFunction, $.isNumeric, $.isWindow, $.now, $.proxy), focus event order changes, Deferreds/Promises alignment with native Promises, slim build differences, and deprecated method removal."
version: "1.0.0"
context:
  primary_domain: "engineering"
  always_load_files: []
  detection_required: true
  file_budget: 6
memory:
  scopes:
    - type: "skill-specific"
      files: [migration_progress.md, codebase_patterns.md]
    - type: "shared-project"
      usage: "reference"
## tags: [jquery, migration, wordpress, legacy, breaking-changes, javascript, upgrade]

# skill:jquery-4 — Migrate jQuery 3.x to 4.0.0

## Version: 1.0.0

## Purpose

Safely migrate jQuery 3.x codebases to jQuery 4.0.0, with first-class support for WordPress themes, plugins, and legacy web applications. This skill systematically audits every breaking change introduced in jQuery 4.0, generates a prioritized migration plan with exact code replacements, and produces safe, reviewable patches.

Use this skill when:
- Upgrading a WordPress site or plugin from jQuery 3.x to 4.0
- Migrating a legacy web application that depends on removed jQuery APIs
- Auditing a codebase for jQuery 4.0 compatibility before upgrading
- Resolving jQuery Migrate plugin warnings in preparation for jQuery 4.0

## File Structure

```
skills/jquery-4/
├── SKILL.md (this file)
└── examples.md
```

## jQuery 4.0 Breaking Changes Reference

### Removed Static Methods

| Removed API | Replacement |
|-------------|-------------|
| `$.isArray(x)` | `Array.isArray(x)` |
| `$.trim(str)` | `str.trim()` or `String.prototype.trim.call(str)` |
| `$.parseJSON(str)` | `JSON.parse(str)` |
| `$.type(obj)` | `typeof obj` or custom type-checking |
| `$.isFunction(fn)` | `typeof fn === "function"` |
| `$.isNumeric(val)` | `!isNaN(parseFloat(val)) && isFinite(val)` |
| `$.isWindow(obj)` | `obj != null && obj === obj.window` |
| `$.now()` | `Date.now()` |
| `$.proxy(fn, ctx)` | `fn.bind(ctx)` |

### Other Breaking Changes

- **Focus event order**: `focus`/`blur` now fire before `focusin`/`focusout` (reversed from 3.x)
- **Deferred/Promise alignment**: `.then()` follows native Promise semantics (async resolution, error swallowing changes)
- **Slim build removed**: Only one build; AJAX and effects are always included
- **`:even` / `:odd` selectors**: Now 0-based (`:even` selects 1st, 3rd, 5th elements)
- **`jQuery.holdReady()` removed**: Use `$.when()` or native module loading instead
- **`jQuery.unique()` removed**: Use `jQuery.uniqueSort()` instead
- **`.andSelf()` removed**: Use `.addBack()` instead
- **`.size()` removed**: Use `.length` property instead
- **`jQuery.cssNumber` reduced**: Several properties removed from the unitless list

## Interface References

- **Context**: Loaded via [ContextProvider Interface](../../interfaces/context_provider.md)
- **Memory**: Accessed via [MemoryStore Interface](../../interfaces/memory_store.md)
- **Shared Patterns**: [Shared Loading Patterns](../../interfaces/shared_loading_patterns.md)
- **Schemas**: Validated against [context_metadata.schema.json](../../interfaces/schemas/context_metadata.schema.json) and [memory_entry.schema.json](../../interfaces/schemas/memory_entry.schema.json)

## Mandatory Workflow

> **⚠️ IMPORTANT**: Execute ALL steps in order. Do not skip any step.

### Step 1: Initial Analysis

- Detect jQuery version in use (check `package.json`, CDN references, `wp_enqueue_script` calls, bundled files)
- Identify all jQuery plugin dependencies and their jQuery version requirements
- Detect custom jQuery extensions (`$.fn.*` additions, `$.extend` usage)
- Determine WordPress context: theme, plugin, mu-plugin, or standalone
- Catalog all JS files that reference `jQuery` or `$`
- Check for existing jQuery Migrate plugin usage

### Step 2: Load Memory

> Follow [Standard Memory Loading](../../interfaces/shared_loading_patterns.md#pattern-1-standard-memory-loading) with `skill="jquery-4"` and `domain="engineering"`.

Load project-specific memory:
- `migration_progress.md` — previous migration state, completed files, blockers
- `codebase_patterns.md` — known jQuery usage patterns, custom abstractions, plugin inventory

### Step 3: Load Context

> Follow [Standard Context Loading](../../interfaces/shared_loading_patterns.md#pattern-2-standard-context-loading) for the `engineering` domain. Stay within the file budget declared in frontmatter.

### Step 4: Audit Breaking Changes

Systematically scan every JS file for jQuery 4.0 incompatibilities:

**Removed Static Methods** — grep for each removed API:
- `$.isArray`, `jQuery.isArray`
- `$.trim`, `jQuery.trim`
- `$.parseJSON`, `jQuery.parseJSON`
- `$.type`, `jQuery.type`
- `$.isFunction`, `jQuery.isFunction`
- `$.isNumeric`, `jQuery.isNumeric`
- `$.isWindow`, `jQuery.isWindow`
- `$.now`, `jQuery.now`
- `$.proxy`, `jQuery.proxy`

**Removed Instance Methods** — scan for:
- `.andSelf()` → `.addBack()`
- `.size()` → `.length`

**Removed Utilities**:
- `jQuery.unique()` → `jQuery.uniqueSort()`
- `jQuery.holdReady()` → remove or replace with module loading

**Behavioral Changes**:
- Focus/blur event handlers that depend on event order relative to focusin/focusout
- `.then()` chains on `$.Deferred()` that rely on synchronous resolution
- `:even` / `:odd` selector usage that assumes 1-based indexing
- Slim build references (`jquery.slim.min.js`) that must switch to the full build

**WordPress-Specific**:
- `jQuery.noConflict()` usage and `$` wrapper patterns
- `wp-includes/js/jquery/` bundled version references
- `wp_enqueue_script('jquery')` dependency chains

Produce a categorized audit report with file paths, line numbers, and severity.

### Step 5: Generate Migration Plan

Produce a prioritized, file-by-file migration plan:

1. **Critical** — Code that will break immediately (removed APIs, removed methods)
2. **High** — Behavioral changes that may cause subtle bugs (focus events, Deferred semantics)
3. **Medium** — Deprecated patterns that should be modernized (slim build refs, selector changes)
4. **Low** — Optional improvements (replace jQuery utilities with modern JS equivalents)

For each finding, specify:
- File path and line number(s)
- Current code snippet
- Exact replacement code
- Risk level and testing notes

### Step 6: Apply Safe Transformations

Generate code patches/diffs for each file:
- Produce unified diff format for each change
- Group related changes per file
- Include rollback instructions (original code in comments or git revert guidance)
- Handle WordPress-specific patterns:
  - Preserve `jQuery(document).ready(function($) { ... })` wrapper pattern
  - Maintain `wp.hooks` integration points
  - Respect `jQuery.noConflict()` mode — never use bare `$` outside wrapper

### Step 7: Validate Migration

Produce a test checklist:

- [ ] All removed API calls replaced with native equivalents
- [ ] Focus/blur event handlers tested for correct order
- [ ] Deferred/Promise chains tested for async behavior changes
- [ ] `:even`/`:odd` selectors verified for 0-based indexing
- [ ] Slim build references updated to full build
- [ ] WordPress admin pages load without JS console errors
- [ ] Front-end interactions (forms, modals, tabs) function correctly
- [ ] Third-party jQuery plugins tested for compatibility

Include jQuery Migrate plugin strategy:
- Install jQuery Migrate 3.x to catch runtime warnings before upgrading
- Run application with Migrate plugin and capture all warnings
- Address all warnings, then remove Migrate and upgrade to jQuery 4.0

### Step 8: Generate Output

- Save output to `/claudedocs/jquery-4_{project}_{YYYY-MM-DD}.md`
- Follow naming conventions in `../OUTPUT_CONVENTIONS.md`
- Include: audit report, migration plan, generated patches, test checklist

### Step 9: Update Memory

> Follow [Standard Memory Update](../../interfaces/shared_loading_patterns.md#pattern-3-standard-memory-update) for `skill="jquery-4"`.

Update memory with:
- Migration progress (files completed, files remaining, blockers)
- Discovered codebase patterns (custom jQuery abstractions, plugin versions)
- WordPress-specific findings (theme structure, enqueue patterns)

## Compliance Checklist

Before completing, verify:

- [ ] All mandatory workflow steps executed in order
- [ ] Standard Memory Loading pattern followed (Step 2)
- [ ] Standard Context Loading pattern followed (Step 3)
- [ ] Every jQuery 4.0 breaking change category audited (Step 4)
- [ ] Migration plan includes exact code replacements (Step 5)
- [ ] Patches include rollback notes (Step 6)
- [ ] Test checklist covers all behavioral changes (Step 7)
- [ ] Output saved with standard naming convention (Step 8)
- [ ] Standard Memory Update pattern followed (Step 9)

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2025-06-27 | Initial release — full jQuery 3.x → 4.0 migration support |
