# playwright

> *Browser automation and E2E testing*

## Configuration

```json
{
  "command": "npx",
  "args": ["@playwright/mcp@latest"]
}
```

**Transport**: npx | **API Key**: None | **Runtime**: Node.js 18+

## Purpose

Provides real browser automation capabilities through the Playwright framework. Enables navigation, interaction, screenshot capture, and E2E test execution in actual browser environments.

## Available Tools

- **browser_navigate**: Navigate to a URL
- **browser_screenshot**: Capture page screenshots
- **browser_click**: Click elements on the page
- **browser_type**: Type text into input fields
- **browser_hover**: Hover over elements
- **browser_select_option**: Select dropdown options
- **browser_evaluate**: Execute JavaScript in the browser
- **browser_wait_for_selector**: Wait for elements to appear

## Forge Integration

**When to activate:**
- E2E test creation and execution
- Visual validation of UI components
- Browser-based debugging
- Accessibility testing in real browsers

**Recommended with Forge commands:**
- `/test` - E2E and integration testing
- `/analyze` - Visual regression analysis
- `/implement` - Verify UI implementation in browser

**Pairs well with:** chrome-devtools (performance), magic (UI generation), context7 (test patterns)

## When Not to Use

- Unit testing (no browser needed)
- Backend/API testing
- Static code analysis

## Fallback

If unavailable, provide manual test instructions for the user to execute, or suggest running Playwright tests from the command line.

---

*Last Updated: 2026-02-10*
