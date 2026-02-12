# jquery-4 Memory

Project-specific memory for jQuery 3.x → 4.0 migration, including migration progress, codebase patterns, plugin inventories, and WordPress-specific findings.

## Purpose

This memory helps the `skill:jquery-4` remember:
- Migration progress per project (files completed, files remaining, blockers)
- Codebase-specific jQuery usage patterns and custom abstractions
- Third-party jQuery plugin compatibility status
- WordPress theme/plugin structure and enqueue patterns
- Discovered edge cases and project-specific workarounds

## Directory Structure

Each project gets its own directory: `{project-name}/`

### `migration_progress.md` ⭐ CRITICAL

**Purpose**: Track the state of a jQuery 4.0 migration across sessions.

**Must contain**:
- **Migration status**: Not started, in progress, completed
- **jQuery version**: Source and target versions
- **Files audited**: List of files scanned with breaking change counts
- **Files migrated**: List of files with patches applied
- **Files remaining**: List of files still needing migration
- **Blockers**: Third-party plugin incompatibilities, unresolvable patterns
- **jQuery Migrate status**: Whether Migrate plugin is in use, warnings resolved

**Example structure**:
```markdown
# Migration Progress — Acme Corp Theme

**Last Updated**: 2025-06-27
**Status**: In Progress
**Source Version**: jQuery 3.6.4
**Target Version**: jQuery 4.0.0

## Completed Files
- `js/theme.js` — 3 changes ($.trim ×2, $.isFunction ×1)
- `js/navigation.js` — 1 change (focus event order reviewed, no change needed)

## Remaining Files
- `js/admin-dashboard.js` — 8 changes ($.Deferred chains, $.proxy ×3, $.type ×2)
- `js/form-validation.js` — 5 changes ($.isNumeric ×2, $.trim ×3)

## Blockers
- `vendor/jquery.fancybox.js` v3.5 — not compatible with jQuery 4.0; awaiting upstream update
- Custom `$.fn.tooltip` extension uses `$.isFunction` internally — needs rewrite

## jQuery Migrate Status
- Migrate 3.5.2 installed, running in development
- 12 warnings captured, 7 resolved, 5 remaining
```

### `codebase_patterns.md` ⭐ CRITICAL

**Purpose**: Document project-specific jQuery usage patterns to avoid re-analysis.

**Must contain**:
- **jQuery loading method**: CDN, npm, WordPress bundled, concatenated
- **noConflict mode**: Whether `jQuery.noConflict()` is used and the wrapper pattern
- **Custom extensions**: Any `$.fn.*` plugins or `$.extend` usage
- **Plugin inventory**: Third-party jQuery plugins with versions and compatibility status
- **Deferred usage patterns**: How the project uses `$.Deferred()`, `.then()`, `.when()`
- **Event delegation patterns**: Common `.on()` delegation roots, custom events

**Example structure**:
```markdown
# Codebase Patterns — Acme Corp Theme

**Last Updated**: 2025-06-27

## jQuery Loading
- Loaded via `wp_enqueue_script('jquery')` — WordPress bundled
- All theme scripts declare `'jquery'` as dependency
- No CDN fallback

## noConflict Pattern
- All files use: `jQuery(document).ready(function($) { ... })`
- Admin scripts use: `(function($) { ... })(jQuery)`
- NEVER use bare `$` at global scope

## Custom Extensions
- `$.fn.acmeModal` — custom modal (uses $.isFunction for callbacks)
- `$.fn.acmeValidate` — form validation (uses $.trim, $.isNumeric)

## Plugin Inventory
| Plugin | Version | jQuery 4.0 Compatible | Notes |
|--------|---------|----------------------|-------|
| Select2 | 4.1.0 | ✅ Yes | Tested |
| jQuery UI | 1.13.2 | ⚠️ Partial | Datepicker OK, Dialog needs testing |
| Fancybox | 3.5.7 | ❌ No | Uses $.isFunction, $.type internally |

## Deferred Usage
- `api-client.js` chains 3-4 Deferreds for dashboard data loading
- Custom `$.when()` wrapper in `utils.js` for parallel API calls
- No direct `.pipe()` usage (already migrated to `.then()`)
```

## Why This Skill Needs Memory

jQuery migrations are multi-session tasks. A typical WordPress project has dozens of JavaScript files, third-party plugins with unknown compatibility, and complex event handler chains. Memory enables:

1. **Incremental migration** — Resume where the last session left off instead of re-auditing the entire codebase
2. **Pattern recognition** — Remember that `$.fn.acmeModal` uses `$.isFunction` so it's flagged immediately in future sessions
3. **Plugin tracking** — Track which third-party plugins have been verified compatible and which are blockers
4. **Consistency** — Apply the same replacement patterns across all files in the project

## Memory Growth Pattern

| Session | Memory Activity |
|---------|----------------|
| 1st migration session | Create `migration_progress.md` with full audit results; create `codebase_patterns.md` with jQuery loading patterns and plugin inventory |
| Subsequent sessions | Update `migration_progress.md` — move files from "Remaining" to "Completed"; update blocker status |
| Plugin resolution | Update `codebase_patterns.md` plugin inventory when compatibility is confirmed or alternatives are found |
| Migration complete | Mark `migration_progress.md` status as "Completed"; record final notes and lessons learned |
