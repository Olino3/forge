---
name: firecrawl-scraper
description: "Convert websites into LLM-ready data with Firecrawl API. Features: scrape single pages, crawl entire sites, map site structure, search content, extract structured data, agent-based autonomous scraping, batch operations, and change tracking. Handles JavaScript rendering, anti-bot bypass, and rate limiting."
version: "1.0.0"
context:
  primary_domain: "engineering"
  always_load_files: []
  detection_required: false
  file_budget: 4
memory:
  scopes:
    - type: "skill-specific"
      files: [scrape_config.md, extraction_schemas.md, crawl_history.md]
    - type: "shared-project"
      usage: "reference"
## tags: [firecrawl, web-scraping, crawling, llm-data, extraction, sitemap, batch, change-tracking]

# skill:firecrawl-scraper - Convert Websites into LLM-Ready Data

## Version: 1.0.0

## Purpose

Convert websites into clean, LLM-ready data using the Firecrawl API. Supports six operation modes: scrape single pages, crawl entire sites, map site structure, search content, extract structured data with schemas, and agent-based autonomous scraping. Includes batch operations for high-volume scraping and change tracking to monitor content updates over time. Use when you need to ingest web content for AI processing, build training datasets, monitor competitor pages, or extract structured information from websites.

## File Structure

```
skills/firecrawl-scraper/
├── SKILL.md (this file)
└── examples.md
```

## Interface References

- **Context**: Loaded via [ContextProvider Interface](../../interfaces/context_provider.md)
- **Memory**: Accessed via [MemoryStore Interface](../../interfaces/memory_store.md)
- **Shared Patterns**: [Shared Loading Patterns](../../interfaces/shared_loading_patterns.md)
- **Schemas**: Validated against [context_metadata.schema.json](../../interfaces/schemas/context_metadata.schema.json) and [memory_entry.schema.json](../../interfaces/schemas/memory_entry.schema.json)

## Mandatory Workflow

> **IMPORTANT**: Execute ALL steps in order. Do not skip any step.

### Step 1: Initial Analysis

- Determine operation type: `scrape` (single page), `crawl` (entire site), `map` (site structure), `search` (content search), `extract` (structured data), or `batch` (bulk operations)
- Identify target URLs and validate they are reachable
- Determine desired output format: markdown, HTML, links, screenshot, or raw HTML
- Assess scope: single page, specific paths, or full domain crawl
- Check if change tracking is needed (compare with previous scrapes)

### Step 2: Load Memory

> Follow [Standard Memory Loading](../../interfaces/shared_loading_patterns.md#pattern-1-standard-memory-loading) with `skill="firecrawl-scraper"` and `domain="engineering"`.

### Step 3: Load Context

> Follow [Standard Context Loading](../../interfaces/shared_loading_patterns.md#pattern-2-standard-context-loading) for the `engineering` domain. Stay within the file budget declared in frontmatter.

### Step 4: Configure Firecrawl Operation

1. Verify Firecrawl API key is available (environment variable `FIRECRAWL_API_KEY`)
2. Select the appropriate endpoint based on operation type:
   - `/scrape` — single page extraction
   - `/crawl` — recursive site crawling
   - `/map` — site structure discovery
   - `/search` — content search across a domain
   - `/extract` — structured data extraction with schema
   - `/batch/scrape` — bulk page scraping
3. Configure output format(s): `markdown`, `html`, `links`, `screenshot`, `rawHtml`
4. Set include/exclude URL patterns (glob syntax: `blog/*`, `!*/admin/*`)
5. Configure wait strategies for JavaScript-heavy sites:
   - `waitFor`: CSS selector or milliseconds to wait before capture
   - `timeout`: maximum page load time
6. Set crawl depth, page limits, and rate limiting parameters
7. Define extraction schema (JSON Schema format) if using `/extract`

### Step 5: Execute Scraping Operation

1. Call the appropriate Firecrawl endpoint with configured parameters
2. For `/crawl` and `/batch/scrape`: poll the async job status until completion
3. Handle rate limiting with exponential backoff (respect `429` responses)
4. Capture response metadata: status codes, page count, execution time
5. For `/map`: collect all discovered URLs and their hierarchy
6. For `/search`: rank and filter results by relevance
7. For `/extract`: validate extracted data against the provided schema

### Step 6: Process and Transform Results

1. Clean extracted content: remove navigation chrome, ads, cookie banners
2. Apply extraction schemas to structure raw content into typed fields
3. Format output for LLM consumption:
   - Markdown with preserved heading hierarchy
   - Code blocks with language annotations
   - Tables converted to markdown format
   - Images as alt-text descriptions or URLs
4. Handle pagination: aggregate multi-page crawl results into unified output
5. Deduplicate content across crawled pages
6. Add source metadata (URL, scrape timestamp, content hash)

### Step 7: Implement Change Tracking

1. Generate content hash (MD5/SHA-256) for each scraped page
2. Compare current hashes against stored hashes in `crawl_history.md`
3. For changed pages, generate a content diff showing additions and removals
4. Classify changes: content update, structural change, new page, removed page
5. Record change frequency to inform future monitoring schedules
6. Flag significant changes (pricing updates, new features, policy changes)

### Step 8: Generate Output

- Save output to `/claudedocs/firecrawl-scraper_{project}_{YYYY-MM-DD}.md`
- Follow naming conventions in `../OUTPUT_CONVENTIONS.md`
- Output includes:
  - Scraped content in requested format (markdown/HTML/structured)
  - Source URLs with timestamps
  - Extraction results (if schema was used)
  - Change tracking report (if comparing with previous scrapes)
  - Error log for any failed pages

### Step 9: Update Memory

> Follow [Standard Memory Update](../../interfaces/shared_loading_patterns.md#pattern-3-standard-memory-update) for `skill="firecrawl-scraper"`. Store scrape configurations, extraction schemas, and crawl history for future sessions.

## 10 Common Errors to Prevent

1. **Missing API key** — Always verify `FIRECRAWL_API_KEY` is set before making requests. Fail fast with a clear message if missing.
2. **Ignoring rate limits** — Firecrawl enforces rate limits. Implement exponential backoff on `429` responses instead of hammering the API.
3. **Unbounded crawls** — Always set `maxDepth` and `limit` parameters on `/crawl` to prevent runaway jobs that scrape thousands of pages.
4. **No wait strategy for SPAs** — JavaScript-rendered sites return empty content without `waitFor`. Use CSS selectors or delay to ensure content loads.
5. **Scraping login-protected pages without auth** — Pages behind authentication return login forms. Use `headers` to pass session cookies or tokens.
6. **Overly broad include patterns** — Patterns like `*` crawl everything including admin panels, CDN assets, and API endpoints. Be specific.
7. **Ignoring robots.txt** — Respect `robots.txt` directives. Firecrawl handles this by default, but custom configurations can override it.
8. **Not validating extraction schemas** — Invalid JSON Schemas cause silent failures. Validate schemas before passing them to `/extract`.
9. **Storing raw HTML when markdown suffices** — Raw HTML is noisy and wastes tokens. Default to markdown unless HTML structure is explicitly needed.
10. **No deduplication on crawl results** — Sites with multiple URL paths to the same content produce duplicates. Hash content to detect and remove duplicates.

## Compliance Checklist

Before completing, verify:

- [ ] All mandatory workflow steps executed in order
- [ ] Standard Memory Loading pattern followed (Step 2)
- [ ] Standard Context Loading pattern followed (Step 3)
- [ ] Firecrawl API key verified before first request
- [ ] Rate limiting and backoff strategy implemented
- [ ] Crawl boundaries set (maxDepth, limit, include/exclude patterns)
- [ ] Output saved with standard naming convention
- [ ] Change tracking hashes recorded (if applicable)
- [ ] Standard Memory Update pattern followed (Step 9)

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2025-07-15 | Initial release — scrape, crawl, map, search, extract, batch, change tracking |
