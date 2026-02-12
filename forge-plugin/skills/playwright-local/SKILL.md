---
name: playwright-local
description: "Build browser automation and web scraping with Playwright on your local machine. Covers page navigation, element interaction, form filling, screenshot capture, PDF generation, network interception, authentication flows, and multi-page workflows. Prevents 10 common errors."
version: "1.0.0"
context:
  primary_domain: "engineering"
  always_load_files: []
  detection_required: false
  file_budget: 4
memory:
  scopes:
    - type: "skill-specific"
      files: [automation_patterns.md, site_selectors.md, auth_flows.md]
    - type: "shared-project"
      usage: "reference"
tags: [playwright, browser-automation, web-scraping, testing, e2e, screenshots, pdf, network-interception]
---

# skill:playwright-local - Browser Automation & Web Scraping with Playwright

## Version: 1.0.0

## Purpose

Build browser automation and web scraping scripts using Playwright on the local machine. Supports all three browser engines (Chromium, Firefox, WebKit) in headless or headed mode. Covers page navigation, element interaction, form filling, screenshot capture, PDF generation, network interception, authentication flows, file upload/download, iframe handling, and multi-page workflows. Use when you need to automate browser tasks, scrape dynamic websites, capture visual snapshots, or build end-to-end test flows locally.

## File Structure

```
skills/playwright-local/
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

- Determine automation goal: scraping, testing, form filling, screenshots/PDF, or monitoring
- Identify target site(s) and pages to automate
- Determine browser preference: Chromium (default), Firefox, or WebKit
- Decide headless vs headed mode (headed for debugging, headless for CI/production)
- Assess complexity: single page, multi-step flow, or multi-tab workflow
- Check if authentication is required (cookies, localStorage, login forms)
- Identify data extraction needs: text content, structured data, images, files

### Step 2: Load Memory

> Follow [Standard Memory Loading](../../interfaces/shared_loading_patterns.md#pattern-1-standard-memory-loading) with `skill="playwright-local"` and `domain="engineering"`.

### Step 3: Load Context

> Follow [Standard Context Loading](../../interfaces/shared_loading_patterns.md#pattern-2-standard-context-loading) for the `engineering` domain. Stay within the file budget declared in frontmatter.

### Step 4: Configure Playwright Setup

1. Generate project setup commands:
   ```bash
   npm init -y
   npm install playwright
   npx playwright install chromium  # or firefox, webkit, or all
   ```
2. Configure TypeScript or JavaScript project as appropriate
3. Set browser launch options:
   - `headless`: true/false
   - `slowMo`: milliseconds between actions (for debugging)
   - `args`: browser arguments (e.g., `--disable-gpu`, `--no-sandbox`)
4. Set browser context options:
   - `viewport`: width and height (default: 1280×720)
   - `locale`: language/region (e.g., `en-US`)
   - `permissions`: geolocation, notifications, camera, microphone
   - `userAgent`: custom user agent string
   - `storageState`: path to saved auth state
5. Configure timeouts: navigation (30s default), action (5s), assertion (5s)

### Step 5: Build Automation Script

1. **Page navigation**: `page.goto()` with wait strategies (`load`, `domcontentloaded`, `networkidle`)
2. **Wait strategies**: `page.waitForSelector()`, `page.waitForLoadState()`, `page.waitForURL()`, `page.waitForResponse()`
3. **Element selectors** (in priority order):
   - Role selectors: `page.getByRole('button', { name: 'Submit' })`
   - Text selectors: `page.getByText('Welcome')`
   - Label selectors: `page.getByLabel('Email')`
   - Placeholder selectors: `page.getByPlaceholder('Enter email')`
   - Test ID selectors: `page.getByTestId('submit-btn')`
   - CSS selectors: `page.locator('.product-card')`
   - XPath selectors: `page.locator('xpath=//div[@class="item"]')`
4. **Interaction sequences**: click, fill, type, select, check, hover, drag-and-drop
5. **Data extraction**: `textContent()`, `innerText()`, `getAttribute()`, `inputValue()`, `$$eval()`
6. **Error handling**: try/catch blocks, screenshot on failure, graceful cleanup

### Step 6: Handle Advanced Patterns

Implement as needed based on Step 1 analysis:

1. **Authentication flows**:
   - Login form automation (fill credentials, submit, wait for redirect)
   - Save auth state with `context.storageState({ path: 'auth.json' })`
   - Reuse auth state in subsequent runs to skip login
   - Cookie injection via `context.addCookies()`
   - localStorage/sessionStorage manipulation via `page.evaluate()`

2. **Network interception**:
   - Mock API responses with `page.route()` to return custom data
   - Block resource types (images, fonts, analytics) to speed up scraping
   - Capture API responses with `page.on('response')` for data extraction
   - Modify request headers (auth tokens, custom headers)

3. **File handling**:
   - File upload: `page.setInputFiles()` or `fileChooser` event
   - File download: configure `downloadsPath`, wait for `download` event
   - PDF generation: `page.pdf({ path, format, printBackground })`

4. **Complex interactions**:
   - iframe handling: `page.frameLocator()` or `frame()` for cross-frame interaction
   - Multi-tab workflows: `context.on('page')` to capture new tabs/popups
   - Shadow DOM: `page.locator()` pierces shadow DOM by default
   - Drag and drop: `page.dragAndDrop(source, target)`

### Step 7: Add Error Prevention

> **CRITICAL**: Implement these 10 common error preventions to ensure robust automation.

1. **Stale element handling** — Always re-query elements before interaction. Use Playwright's auto-waiting locators instead of storing element references. Playwright's locator API auto-retries, but avoid caching `ElementHandle` objects.

2. **Navigation timeouts** — Set appropriate timeouts for `page.goto()` and `page.waitForNavigation()`. Default 30s is too short for slow sites; too long delays failure detection. Use `page.goto(url, { timeout: 60000 })` for known slow pages.

3. **Anti-bot detection avoidance** — Rotate user agents, set realistic viewport sizes, add human-like delays with `page.waitForTimeout()` between actions, and avoid headless detection by using `chromium.launch({ channel: 'chrome' })` for a real browser fingerprint.

4. **Proper wait strategies** — Never use hard-coded `waitForTimeout()` as the primary wait. Use event-driven waits: `waitForSelector()`, `waitForLoadState('networkidle')`, `waitForResponse()`, or `waitForURL()`. Hard waits are fragile and slow.

5. **Screenshot on failure** — Wrap automation in try/catch and capture `page.screenshot({ path: 'error.png', fullPage: true })` on failure. This provides visual debugging context that logs alone cannot.

6. **Retry logic** — Implement retry wrappers for flaky operations (network requests, element interactions on dynamic pages). Use exponential backoff: 1s, 2s, 4s delays between retries, with a maximum of 3 attempts.

7. **Graceful cleanup** — Always close browser and context in a `finally` block. Leaked browser processes consume memory and can cause port conflicts. Use `browser.close()` even when the script fails.

8. **Selector specificity** — Avoid overly broad selectors like `div` or `.item` that match multiple elements. Prefer role-based, text-based, or test-id selectors. When using CSS, be specific enough to match exactly one element.

9. **Race condition prevention** — When clicking a button that triggers navigation, use `Promise.all([page.waitForNavigation(), page.click()])` to avoid race conditions between the click and the navigation event listener registration.

10. **Resource cleanup for long-running scripts** — For scripts that process many pages, close and reopen contexts periodically to prevent memory leaks. Monitor `page.on('crash')` and `page.on('pageerror')` to detect and recover from browser crashes.

### Step 8: Generate Output

- Save output to `/claudedocs/playwright-local_{project}_{YYYY-MM-DD}.md`
- Follow naming conventions in `../OUTPUT_CONVENTIONS.md`
- Output includes:
  - Complete Playwright script (TypeScript or JavaScript)
  - Setup instructions (install commands, browser downloads)
  - Configuration files (tsconfig.json if TypeScript)
  - Extracted data or screenshots (if applicable)
  - Error handling and retry logic
  - Run instructions (command to execute the script)

### Step 9: Update Memory

> Follow [Standard Memory Update](../../interfaces/shared_loading_patterns.md#pattern-3-standard-memory-update) for `skill="playwright-local"`. Store working selectors, authentication flows, and automation patterns for future sessions.

## 10 Common Errors to Prevent

1. **Stale element handling** — Re-query elements before interaction; use locators, not cached ElementHandles.
2. **Navigation timeouts** — Set appropriate timeouts; adjust for slow sites, don't rely on defaults blindly.
3. **Anti-bot detection avoidance** — Use real browser channels, rotate user agents, add human-like delays.
4. **Proper wait strategies** — Use event-driven waits, not hard-coded `waitForTimeout()`.
5. **Screenshot on failure** — Always capture screenshots in catch blocks for visual debugging.
6. **Retry logic** — Wrap flaky operations with exponential backoff retries (max 3 attempts).
7. **Graceful cleanup** — Close browser in `finally` block to prevent leaked processes.
8. **Selector specificity** — Use role/text/test-id selectors; avoid overly broad CSS selectors.
9. **Race condition prevention** — Use `Promise.all()` for click + navigation combinations.
10. **Resource cleanup for long-running scripts** — Periodically close/reopen contexts; monitor for crashes.

## Compliance Checklist

Before completing, verify:

- [ ] All mandatory workflow steps executed in order
- [ ] Standard Memory Loading pattern followed (Step 2)
- [ ] Standard Context Loading pattern followed (Step 3)
- [ ] Browser install commands included in setup
- [ ] Wait strategies use event-driven waits, not hard-coded timeouts
- [ ] Error handling includes screenshot on failure
- [ ] Graceful cleanup with browser.close() in finally block
- [ ] All 10 error preventions reviewed and applied where relevant
- [ ] Output saved with standard naming convention
- [ ] Standard Memory Update pattern followed (Step 9)

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2025-07-15 | Initial release — navigation, interaction, scraping, screenshots, PDF, network interception, auth flows, 10 error preventions |
