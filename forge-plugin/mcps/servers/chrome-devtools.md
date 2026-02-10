# chrome-devtools

> *Chrome DevTools Protocol access for performance and debugging*

## Configuration

```json
{
  "command": "npx",
  "args": ["-y", "chrome-devtools-mcp@latest"]
}
```

**Transport**: npx | **API Key**: None | **Runtime**: Node.js 18+

## Purpose

Provides direct access to Chrome DevTools Protocol for performance analysis, debugging, and real-time browser inspection. Enables profiling, network analysis, and console interaction.

## Available Tools

- **devtools_evaluate**: Execute JavaScript in the DevTools console
- **devtools_screenshot**: Capture screenshots via DevTools
- **devtools_network**: Monitor network requests
- **devtools_performance**: Run performance profiling

## Forge Integration

**When to activate:**
- Performance auditing (LCP, CLS, FID metrics)
- Debugging layout and rendering issues
- Network request analysis
- Console error investigation
- Memory leak detection

**Recommended with Forge commands:**
- `/analyze` - Performance-focused code analysis
- `/test` - Performance regression testing
- `/improve` - Performance optimization guidance

**Pairs well with:** playwright (browser automation), sequential-thinking (analysis of results)

## When Not to Use

- Backend performance (no browser involved)
- Static code analysis
- Unit testing

## Fallback

If unavailable, suggest the user run Lighthouse, Chrome DevTools, or `web-vitals` library manually and share the results.

---

*Last Updated: 2026-02-10*
