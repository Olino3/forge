# Firecrawl Scraper - Project Memory System

## Purpose

This directory stores project-specific knowledge learned during web scraping sessions with Firecrawl. Each project gets its own subdirectory containing scrape configurations, reusable extraction schemas, and crawl history with content hashes for change tracking.

## Directory Structure

```
memory/skills/firecrawl-scraper/
├── index.md (this file)
└── {project-name}/
    ├── scrape_config.md
    ├── extraction_schemas.md
    └── crawl_history.md
```

## Project Memory Contents

### scrape_config.md
- Target URLs and their operation types (scrape/crawl/map/search/extract)
- Include/exclude URL patterns used for each target
- Wait strategies per site (CSS selectors, delay values, timeouts)
- Output format preferences (markdown, HTML, structured)
- Crawl parameters: maxDepth, page limits, rate limiting settings
- Authentication headers or cookies required for protected sites

### extraction_schemas.md
- JSON Schema definitions used with the `/extract` endpoint
- Schema-to-URL mappings (which schema works for which site)
- Schema evolution history (field additions, type changes)
- Extraction prompts paired with each schema
- Validation results and field coverage statistics

### crawl_history.md
- Content hashes (SHA-256) for each scraped URL with timestamps
- Change detection log: what changed, when, and classification
- Price and content baselines for monitored pages
- Crawl job IDs and completion statistics (pages scraped, duration, errors)
- Page inventory for crawled sites (URL list with last-seen dates)

## Why This Skill Needs Memory

Web scraping benefits from persistent memory because:

1. **Configuration reuse** — Scrape configurations (include/exclude patterns, wait strategies, auth headers) are tedious to rediscover. Memory preserves working configurations across sessions.
2. **Schema evolution** — Extraction schemas are refined over multiple runs as site structures change. Memory tracks schema versions and which fields were added or deprecated.
3. **Change tracking** — Detecting content changes requires comparing current scrapes against previous baselines. Memory stores content hashes and structured data snapshots for diffing.
4. **Crawl efficiency** — Remembering which pages were already scraped, which returned errors, and which require special handling avoids redundant work and speeds up incremental crawls.

## Memory Lifecycle

### Creation
Memory is created the FIRST time a site is scraped for a project. The project name is either:
1. Extracted from the repository root directory name
2. Specified by the user
3. Derived from the target domain name

### Updates
Memory is UPDATED every time the skill scrapes, crawls, or extracts:
- Scrape configurations are confirmed or refined
- New extraction schemas are added to the library
- Content hashes are updated with fresh timestamps
- Change detection results are appended to history
- Failed URLs and error patterns are recorded

### Usage
Memory is READ at the START of every scraping operation:
- Recalls working configurations for known target sites
- Loads matching extraction schemas automatically
- Retrieves previous content hashes for change comparison
- Applies learned wait strategies to avoid empty-content failures

## Memory Growth Pattern

```
Session 1: scrape_config.md created with first target URL and settings
           crawl_history.md created with initial content hashes

Session 2: extraction_schemas.md created with first JSON Schema
           crawl_history.md appended with new scrape results

Session 3: scrape_config.md updated with refined include/exclude patterns
           crawl_history.md appended with change detection results

Session N: All files grow incrementally — prune old entries
           per memory/lifecycle.md freshness rules
```

## Best Practices

### DO:
- ✅ Update memory after every scrape operation
- ✅ Store working scrape configurations with their target URLs
- ✅ Save extraction schemas for reuse across sessions
- ✅ Record content hashes for every monitored page
- ✅ Log change detection results with timestamps

### DON'T:
- ❌ Store full scraped content (link to output files instead)
- ❌ Store API keys or authentication credentials
- ❌ Duplicate Firecrawl API documentation
- ❌ Keep hashes for one-off scrapes that won't be re-monitored
- ❌ Leave stale configurations for sites that have changed structure

## Memory vs Context

### Context (`../../context/engineering/`)
- **Universal knowledge**: Applies to ALL projects
- **Firecrawl API reference**: Endpoint signatures, parameter options
- **Best practices**: Rate limiting, robots.txt compliance, output formatting
- **Static**: Updated by Forge maintainers

### Memory (this directory)
- **Project-specific**: Only for ONE project's scraping targets
- **Learned configurations**: Discovered during scraping sessions
- **Evolving**: Changes with each scrape
- **Dynamic**: Updated by the skill automatically

## Privacy and Security

### DO Store:
- Target URLs and scrape configurations
- Extraction schemas and prompts
- Content hashes and change logs
- Crawl statistics and error patterns

### DON'T Store:
- API keys or authentication tokens
- Scraped content or raw HTML
- User PII found in scraped data
- Credentials for login-protected sites

---

**Memory System Version**: 1.0.0
**Last Updated**: 2025-07-15
**Maintained by**: firecrawl-scraper skill
