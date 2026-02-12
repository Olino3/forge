# Firecrawl Scraper Examples

This file contains example scenarios demonstrating how to use the firecrawl-scraper skill to convert websites into LLM-ready data, extract structured information, and track content changes.

---

## Example 1: Scraping a Documentation Site for LLM-Ready Markdown

### Scenario
A developer is building a RAG (Retrieval-Augmented Generation) pipeline and needs to ingest the entire Stripe API documentation as clean markdown for embedding into a vector database.

### User Prompt
```
Crawl the Stripe API docs at https://docs.stripe.com/api and convert all pages to clean markdown for my RAG pipeline
```

### Skill Execution

**Step 1 - Initial Analysis**:
- Operation type: `crawl` (multi-page site)
- Target URL: `https://docs.stripe.com/api`
- Output format: Markdown (optimized for LLM consumption)
- Scope: All pages under `/api` path
- Change tracking: Not needed (first scrape)

**Step 2 - Load Memory**:
No prior scrape history found for this project. Fresh configuration.

**Step 3 - Load Context**:
Loaded engineering domain context. File budget: 4 files.

**Step 4 - Configure Firecrawl Operation**:
- Endpoint: `/crawl`
- Parameters:
  ```json
  {
    "url": "https://docs.stripe.com/api",
    "maxDepth": 3,
    "limit": 200,
    "includePaths": ["api/*"],
    "excludePaths": ["api/changelog/*", "api/upgrades/*"],
    "scrapeOptions": {
      "formats": ["markdown"],
      "waitFor": 2000
    }
  }
  ```
- Rate limiting: Default (Firecrawl managed)
- Wait strategy: 2000ms for JavaScript rendering

**Step 5 - Execute Scraping Operation**:
- Submitted crawl job → received job ID `crawl_abc123`
- Polled status every 10 seconds until completion
- Crawl completed: 147 pages scraped in 4m 32s
- 3 pages returned 403 (login-required) — logged and skipped

**Step 6 - Process and Transform Results**:
- Stripped navigation headers, footers, and sidebar menus
- Preserved code blocks with language annotations (curl, python, ruby, node)
- Converted HTML tables to markdown tables
- Added source URL as metadata header to each page
- Deduplicated 12 pages that appeared under multiple URL paths
- Final output: 135 unique pages, ~420K tokens total

**Step 7 - Implement Change Tracking**:
- Generated SHA-256 content hash for each page
- Stored hashes in `crawl_history.md` for future comparison

**Step 8 - Generate Output**:
Saved to `/claudedocs/firecrawl-scraper_rag-pipeline_2025-07-15.md`.
Output structure:
```markdown
# Stripe API Documentation — Crawl Results
- Pages scraped: 135 (unique)
- Total tokens: ~420K
- Crawl date: 2025-07-15

## /api/charges
[clean markdown content...]

## /api/customers
[clean markdown content...]

## /api/payment-intents
[clean markdown content...]
```

**Step 9 - Update Memory**:
- ✅ Crawl configuration saved to `scrape_config.md`
- ✅ Content hashes stored in `crawl_history.md` (135 entries)
- ✅ Include/exclude patterns recorded for reuse

---

## Example 2: Extracting Structured Product Data with Schemas

### Scenario
An e-commerce analyst needs to extract structured product data (name, price, rating, availability) from a competitor's product listing page for price comparison analysis.

### User Prompt
```
Extract product names, prices, ratings, and stock status from https://example-store.com/products/electronics using a structured schema
```

### Skill Execution

**Step 1 - Initial Analysis**:
- Operation type: `extract` (structured data extraction)
- Target URL: `https://example-store.com/products/electronics`
- Output format: Structured JSON matching a defined schema
- Scope: Single page with multiple product entries
- Change tracking: Not needed initially

**Step 2 - Load Memory**:
No prior extraction schemas found. Fresh configuration.

**Step 3 - Load Context**:
Loaded engineering domain context. File budget: 4 files.

**Step 4 - Configure Firecrawl Operation**:
- Endpoint: `/extract`
- Extraction schema (JSON Schema):
  ```json
  {
    "url": "https://example-store.com/products/electronics",
    "prompt": "Extract all product listings from this page",
    "schema": {
      "type": "object",
      "properties": {
        "products": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "name": { "type": "string" },
              "price": { "type": "number" },
              "currency": { "type": "string" },
              "rating": { "type": "number" },
              "review_count": { "type": "integer" },
              "in_stock": { "type": "boolean" },
              "url": { "type": "string" }
            },
            "required": ["name", "price", "in_stock"]
          }
        }
      }
    }
  }
  ```
- Wait strategy: `waitFor: ".product-card"` (CSS selector for product cards)

**Step 5 - Execute Scraping Operation**:
- Called `/extract` endpoint with schema
- Firecrawl rendered the JavaScript-heavy page (React SPA)
- Extraction completed in 8.2 seconds
- 24 products extracted successfully

**Step 6 - Process and Transform Results**:
- Validated all 24 products against the schema — all pass
- Extracted data:

| Product | Price | Rating | Reviews | In Stock |
|---------|-------|--------|---------|----------|
| Sony WH-1000XM5 | $348.00 | 4.7 | 2,341 | ✅ |
| Apple AirPods Pro 2 | $249.00 | 4.8 | 5,102 | ✅ |
| Samsung Galaxy Buds3 | $179.99 | 4.3 | 891 | ✅ |
| Bose QC Ultra | $429.00 | 4.6 | 1,205 | ❌ |
| ... (20 more) | ... | ... | ... | ... |

- Sorted by price ascending for analysis
- Flagged out-of-stock items (3 of 24)

**Step 7 - Implement Change Tracking**:
- Generated content hash for the product listing page
- Stored product prices as baseline for future price monitoring

**Step 8 - Generate Output**:
Saved to `/claudedocs/firecrawl-scraper_price-comparison_2025-07-15.md`.
Output includes:
- Full product data table (24 items)
- JSON export of structured data
- Price distribution summary (min, max, median, average)
- Out-of-stock alerts

**Step 9 - Update Memory**:
- ✅ Extraction schema saved to `extraction_schemas.md` (reusable for future runs)
- ✅ Product URL and scrape config stored in `scrape_config.md`
- ✅ Baseline prices and content hash stored in `crawl_history.md`

---

## Example 3: Setting Up Change Tracking for Competitor Pricing

### Scenario
A product manager wants to monitor a competitor's pricing page weekly. They need to detect when prices change, new products appear, or products are removed, and receive a diff report highlighting the changes.

### User Prompt
```
Set up change tracking on https://competitor.com/pricing — I want to know whenever they change their plans or prices
```

### Skill Execution

**Step 1 - Initial Analysis**:
- Operation type: `scrape` (single page) with change tracking enabled
- Target URL: `https://competitor.com/pricing`
- Output format: Markdown + structured diff report
- Scope: Single pricing page
- Change tracking: Yes — compare against previous scrape in memory

**Step 2 - Load Memory**:
Found existing crawl history for `competitor.com/pricing`:
- Last scrape: 2025-07-08
- Content hash: `a3f2b8c1...`
- Previous prices: Starter ($29), Pro ($79), Enterprise ($199)

**Step 3 - Load Context**:
Loaded engineering domain context. File budget: 4 files.

**Step 4 - Configure Firecrawl Operation**:
- Endpoint: `/scrape`
- Parameters:
  ```json
  {
    "url": "https://competitor.com/pricing",
    "formats": ["markdown"],
    "waitFor": ".pricing-table",
    "timeout": 15000
  }
  ```
- Also configure `/extract` for structured price data:
  ```json
  {
    "url": "https://competitor.com/pricing",
    "prompt": "Extract all pricing plans with their names, prices, billing periods, and feature lists",
    "schema": {
      "type": "object",
      "properties": {
        "plans": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "name": { "type": "string" },
              "monthly_price": { "type": "number" },
              "annual_price": { "type": "number" },
              "features": { "type": "array", "items": { "type": "string" } }
            }
          }
        }
      }
    }
  }
  ```

**Step 5 - Execute Scraping Operation**:
- Scraped pricing page in 3.1 seconds
- Extracted structured pricing data via `/extract`
- Current prices: Starter ($29), Pro ($99), Enterprise ($199), Team ($149)

**Step 6 - Process and Transform Results**:
- Cleaned markdown output — removed header, footer, testimonials section
- Structured extraction returned 4 pricing plans (previously 3)

**Step 7 - Implement Change Tracking**:
- Generated new content hash: `d7e4f1a9...` (differs from stored `a3f2b8c1...`)
- Compared current data against previous scrape:

```diff
 Competitor Pricing — Change Report (2025-07-08 → 2025-07-15)

 ## Starter Plan
   Monthly: $29/mo (unchanged)
   Annual: $290/yr (unchanged)

 ## Pro Plan
-  Monthly: $79/mo
+  Monthly: $99/mo  ⚠️ PRICE INCREASE (+$20/mo, +25.3%)
-  Annual: $790/yr
+  Annual: $990/yr  ⚠️ PRICE INCREASE (+$200/yr)

 ## Enterprise Plan
   Monthly: $199/mo (unchanged)
   Custom pricing: Contact sales (unchanged)

+## Team Plan  🆕 NEW PLAN DETECTED
+  Monthly: $149/mo
+  Annual: $1,490/yr
+  Features: 10 seats, shared dashboard, team analytics, priority support
```

- Changes detected:
  - **Price increase**: Pro plan $79 → $99/mo (+25.3%)
  - **New plan**: Team plan added at $149/mo (positioned between Pro and Enterprise)
  - **No removals**: All previous plans still present

**Step 8 - Generate Output**:
Saved to `/claudedocs/firecrawl-scraper_competitor-monitor_2025-07-15.md`.
Output includes:
- Full current pricing page (markdown)
- Structured diff report with change classification
- Price change summary with percentage calculations
- New plan alert with full feature list
- Recommendation: Re-check in 7 days (weekly cadence maintained)

**Step 9 - Update Memory**:
- ✅ Updated content hash in `crawl_history.md` (`a3f2b8c1...` → `d7e4f1a9...`)
- ✅ Recorded price changes with timestamps and percentages
- ✅ Added Team plan to baseline data for future comparisons
- ✅ Extraction schema confirmed working — stored in `extraction_schemas.md`
- ✅ Scrape config unchanged — retained in `scrape_config.md`
