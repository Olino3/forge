# Playwright Local - Project Memory System

## Purpose

This directory stores project-specific knowledge learned during browser automation sessions with Playwright. Each project gets its own subdirectory containing automation patterns, site-specific selectors, and authentication flows discovered during scripting sessions.

## Directory Structure

```
memory/skills/playwright-local/
├── index.md (this file)
└── {project-name}/
    ├── automation_patterns.md
    ├── site_selectors.md
    └── auth_flows.md
```

## Project Memory Contents

### automation_patterns.md
- Pagination strategies used for each target site (URL params, infinite scroll, "Load More" buttons)
- Wait strategies per site (CSS selectors, network idle, custom delays)
- Data extraction patterns (DOM scraping, API interception, hybrid)
- Retry configurations and backoff parameters
- Network interception rules (blocked resources, mocked APIs, captured endpoints)
- Browser launch options that work for specific sites (headless, channel, args)
- Script execution order for multi-step workflows

### site_selectors.md
- Working CSS, role, text, label, and test-id selectors per target site
- Selector-to-URL mappings (which selectors work on which pages)
- Selector evolution history (when sites change their DOM structure)
- Fragile selectors flagged for monitoring (class-name-based, index-based)
- Shadow DOM and iframe selectors with access patterns
- Pagination element selectors (next button, page numbers, load-more triggers)

### auth_flows.md
- Login sequences per site (URL, form selectors, submit flow, redirect expectations)
- Auth state file paths (`storageState` JSON locations)
- Session expiration patterns (how long sessions last, refresh triggers)
- Cookie and localStorage keys required for authentication
- SSO redirect chains (identity provider URLs, callback patterns)
- Multi-factor authentication handling notes (TOTP, SMS, manual intervention required)

## Why This Skill Needs Memory

Browser automation benefits from persistent memory because:

1. **Selector stability** — Working selectors are hard-won through trial and error. Sites change their DOM structure over time, so remembering which selectors work (and which broke) saves significant debugging effort across sessions.
2. **Authentication persistence** — Login flows involve multiple steps (SSO redirects, MFA, cookie consent). Memory stores the exact sequence and saved auth state paths so subsequent runs skip login entirely.
3. **Pattern reuse** — Pagination strategies, wait configurations, and data extraction patterns are site-specific. Once a working pattern is discovered, memory preserves it for instant reuse in future automation scripts.
4. **Anti-bot tuning** — Different sites require different evasion techniques (user agent rotation, delay tuning, viewport settings). Memory records what works per site to avoid re-discovering these settings.

## Memory Lifecycle

### Creation
Memory is created the FIRST time a site is automated for a project. The project name is either:
1. Extracted from the repository root directory name
2. Specified by the user
3. Derived from the target domain name

### Updates
Memory is UPDATED every time the skill builds or modifies automation scripts:
- Working selectors are confirmed or updated when sites change
- New automation patterns are added (pagination, interception, file handling)
- Auth flow sequences are refined (faster login paths, session refresh)
- Failed selectors are flagged with timestamps and replacements
- New API endpoints discovered via network interception are recorded

### Usage
Memory is READ at the START of every automation session:
- Recalls working selectors for known target sites
- Loads saved auth state paths to skip login flows
- Applies proven wait strategies and pagination patterns
- Warns about previously fragile selectors that may need updating

## Memory Growth Pattern

```
Session 1: automation_patterns.md created with first site's wait strategy and pagination
           site_selectors.md created with initial working selectors

Session 2: auth_flows.md created when first authenticated site is automated
           site_selectors.md expanded with new page selectors

Session 3: automation_patterns.md updated with network interception patterns
           auth_flows.md updated with session expiration timing

Session N: All files grow incrementally — prune stale selectors and expired
           auth flows per memory/lifecycle.md freshness rules
```

## Best Practices

### DO:
- ✅ Update memory after every automation session
- ✅ Store working selectors with their target URLs and page context
- ✅ Save auth state file paths and login sequences
- ✅ Record which wait strategies work for each site
- ✅ Flag fragile selectors with timestamps for monitoring
- ✅ Note anti-bot techniques that work per site

### DON'T:
- ❌ Store passwords or authentication credentials
- ❌ Store scraped data content (link to output files instead)
- ❌ Duplicate Playwright API documentation
- ❌ Keep selectors for sites that have been fully redesigned
- ❌ Store session cookies or auth tokens directly

## Memory vs Context

### Context (`../../context/engineering/`)
- **Universal knowledge**: Applies to ALL projects
- **Playwright API reference**: Launch options, locator methods, wait strategies
- **Best practices**: Selector priority, error handling patterns, cleanup
- **Static**: Updated by Forge maintainers

### Memory (this directory)
- **Project-specific**: Only for ONE project's automation targets
- **Learned selectors**: Discovered during automation sessions
- **Evolving**: Changes as target sites update their DOM
- **Dynamic**: Updated by the skill automatically

## Privacy and Security

### DO Store:
- Target URLs and page structures
- Working selectors and automation patterns
- Auth flow sequences (steps, not credentials)
- Wait strategy configurations
- Network interception rules (endpoints, blocked resources)

### DON'T Store:
- Passwords or API keys
- Session cookies or auth tokens
- Scraped user data or PII
- Screenshots containing sensitive information
- Auth state JSON file contents (only store the file path)

---

**Memory System Version**: 1.0.0
**Last Updated**: 2025-07-15
**Maintained by**: playwright-local skill
