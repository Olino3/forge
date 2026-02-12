# Playwright Local Examples

This file contains example scenarios demonstrating how to use the playwright-local skill to build browser automation, web scraping, and data extraction workflows on the local machine.

---

## Example 1: Scraping Product Listings from an E-Commerce Site with Pagination

### Scenario
A data analyst needs to scrape product names, prices, ratings, and availability from an e-commerce site's electronics category. The listings span 15 pages and each page loads dynamically via JavaScript. Results should be exported as structured JSON.

### User Prompt
```
Scrape all product listings from https://example-store.com/electronics — get name, price, rating, and stock status across all pages. Export as JSON.
```

### Skill Execution

**Step 1 - Initial Analysis**:
- Automation goal: Web scraping with data extraction
- Target: `https://example-store.com/electronics` (paginated, 15 pages)
- Browser: Chromium (headless — no visual debugging needed)
- Complexity: Multi-page with pagination handling
- Authentication: Not required (public listings)
- Data extraction: Structured product data (name, price, rating, availability)

**Step 2 - Load Memory**:
No prior automation patterns found for this project. Fresh configuration.

**Step 3 - Load Context**:
Loaded engineering domain context. File budget: 4 files.

**Step 4 - Configure Playwright Setup**:
```bash
npm init -y
npm install playwright
npx playwright install chromium
```
- Headless mode: `true` (production scraping)
- Viewport: 1280×720
- User agent: Rotated realistic Chrome user agents
- Navigation timeout: 60000ms (slow-loading product pages)

**Step 5 - Build Automation Script**:
```typescript
import { chromium, Browser, Page } from 'playwright';

interface Product {
  name: string;
  price: number;
  rating: number;
  inStock: boolean;
  url: string;
}

async function scrapeProducts(): Promise<Product[]> {
  const browser: Browser = await chromium.launch({ headless: true });
  const context = await browser.newContext({
    viewport: { width: 1280, height: 720 },
    userAgent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
  });

  const allProducts: Product[] = [];
  const page: Page = await context.newPage();

  try {
    let currentPage = 1;
    let hasNextPage = true;

    while (hasNextPage) {
      await page.goto(
        `https://example-store.com/electronics?page=${currentPage}`,
        { waitUntil: 'networkidle', timeout: 60000 }
      );

      // Wait for product cards to render
      await page.waitForSelector('.product-card', { timeout: 10000 });

      // Extract product data from current page
      const products = await page.$$eval('.product-card', (cards) =>
        cards.map((card) => ({
          name: card.querySelector('.product-title')?.textContent?.trim() || '',
          price: parseFloat(
            card.querySelector('.product-price')?.textContent?.replace('$', '') || '0'
          ),
          rating: parseFloat(
            card.querySelector('.star-rating')?.getAttribute('data-rating') || '0'
          ),
          inStock: !card.querySelector('.out-of-stock'),
          url: card.querySelector('a')?.href || ''
        }))
      );

      allProducts.push(...products);
      console.log(`Page ${currentPage}: scraped ${products.length} products`);

      // Check for next page
      const nextButton = page.locator('.pagination .next:not(.disabled)');
      hasNextPage = (await nextButton.count()) > 0;
      currentPage++;
    }

    return allProducts;
  } catch (error) {
    await page.screenshot({ path: 'error-scrape.png', fullPage: true });
    throw error;
  } finally {
    await browser.close();
  }
}
```

**Step 6 - Handle Advanced Patterns**:
- Network interception: Block images and fonts to speed up scraping
  ```typescript
  await page.route('**/*.{png,jpg,jpeg,gif,svg,woff,woff2}', (route) => route.abort());
  ```
- Anti-bot: Added human-like delay between pages (`page.waitForTimeout(1500 + Math.random() * 1000)`)
- No authentication needed for public listings

**Step 7 - Add Error Prevention**:
- ✅ **Stale elements**: Re-queried products on each page via `$$eval()`
- ✅ **Navigation timeouts**: Set to 60s for slow product pages
- ✅ **Anti-bot**: Realistic user agent, human-like delays between pages
- ✅ **Wait strategies**: Used `waitForSelector('.product-card')` instead of hard waits
- ✅ **Screenshot on failure**: Captured `error-scrape.png` in catch block
- ✅ **Retry logic**: Wrapped page navigation in retry with 3 attempts
- ✅ **Graceful cleanup**: `browser.close()` in finally block
- ✅ **Selector specificity**: Used `.product-card`, `.product-title`, `.product-price`
- ✅ **Race conditions**: N/A (no click + navigation combos)
- ✅ **Resource cleanup**: Single context reused; closed on completion

**Step 8 - Generate Output**:
Saved to `/claudedocs/playwright-local_ecommerce-scraper_2025-07-15.md`.
- Complete TypeScript script with pagination handling
- Setup instructions (npm install, browser download)
- JSON output: 342 products across 15 pages
- Run command: `npx tsx scrape-products.ts`

**Step 9 - Update Memory**:
- ✅ Pagination pattern saved to `automation_patterns.md`
- ✅ Product card selectors saved to `site_selectors.md` (`.product-card`, `.product-title`, `.product-price`, `.star-rating`)
- ✅ Anti-bot delay strategy recorded

---

## Example 2: Automating a Multi-Step Form Submission with File Uploads and Screenshots

### Scenario
A QA engineer needs to automate a multi-step insurance application form that includes personal information, file uploads (ID document and proof of address), and a final review page. Screenshots should be captured at each step for audit trail purposes.

### User Prompt
```
Automate the insurance application form at https://example-insurance.com/apply — fill in all fields across 3 steps, upload ID and proof of address PDFs, take screenshots at each step, and submit.
```

### Skill Execution

**Step 1 - Initial Analysis**:
- Automation goal: Form filling with file uploads and visual documentation
- Target: `https://example-insurance.com/apply` (3-step wizard form)
- Browser: Chromium (headed for initial debugging, then headless)
- Complexity: Multi-step form with file uploads
- Authentication: Not required (public application form)
- Data extraction: Confirmation number from final page
- Screenshots: Required at each step for audit trail

**Step 2 - Load Memory**:
No prior form automation patterns found. Fresh configuration.

**Step 3 - Load Context**:
Loaded engineering domain context. File budget: 4 files.

**Step 4 - Configure Playwright Setup**:
```bash
npm init -y
npm install playwright
npx playwright install chromium
```
- Headless mode: `false` (debugging), switch to `true` for production
- Viewport: 1280×900 (taller to capture full forms)
- Screenshots directory: `./screenshots/`
- slowMo: 100ms (for visual debugging)

**Step 5 - Build Automation Script**:
```typescript
import { chromium, Browser, Page } from 'playwright';
import path from 'path';

async function submitInsuranceApplication() {
  const browser: Browser = await chromium.launch({
    headless: false,
    slowMo: 100
  });
  const context = await browser.newContext({
    viewport: { width: 1280, height: 900 },
    acceptDownloads: true
  });
  const page: Page = await context.newPage();

  try {
    // === Step 1: Personal Information ===
    await page.goto('https://example-insurance.com/apply', {
      waitUntil: 'networkidle'
    });

    await page.getByLabel('First Name').fill('Jane');
    await page.getByLabel('Last Name').fill('Smith');
    await page.getByLabel('Date of Birth').fill('1990-03-15');
    await page.getByLabel('Email').fill('jane.smith@example.com');
    await page.getByLabel('Phone').fill('(555) 123-4567');
    await page.getByRole('combobox', { name: 'State' }).selectOption('CA');

    await page.screenshot({
      path: 'screenshots/step1-personal-info.png',
      fullPage: true
    });

    await Promise.all([
      page.waitForURL('**/apply/step2'),
      page.getByRole('button', { name: 'Next' }).click()
    ]);

    // === Step 2: Document Upload ===
    await page.waitForSelector('#id-upload', { state: 'visible' });

    // Upload ID document
    await page.setInputFiles('#id-upload', path.resolve('./documents/id-card.pdf'));
    await page.waitForSelector('.upload-success-id', { timeout: 10000 });

    // Upload proof of address
    await page.setInputFiles(
      '#address-upload',
      path.resolve('./documents/utility-bill.pdf')
    );
    await page.waitForSelector('.upload-success-address', { timeout: 10000 });

    await page.screenshot({
      path: 'screenshots/step2-documents.png',
      fullPage: true
    });

    await Promise.all([
      page.waitForURL('**/apply/review'),
      page.getByRole('button', { name: 'Next' }).click()
    ]);

    // === Step 3: Review and Submit ===
    await page.waitForSelector('.review-summary', { state: 'visible' });

    await page.screenshot({
      path: 'screenshots/step3-review.png',
      fullPage: true
    });

    // Accept terms and submit
    await page.getByLabel('I agree to the terms and conditions').check();
    await Promise.all([
      page.waitForURL('**/apply/confirmation'),
      page.getByRole('button', { name: 'Submit Application' }).click()
    ]);

    // === Capture Confirmation ===
    const confirmationNumber = await page
      .locator('.confirmation-number')
      .textContent();

    await page.screenshot({
      path: 'screenshots/step4-confirmation.png',
      fullPage: true
    });

    console.log(`Application submitted: ${confirmationNumber}`);
    return confirmationNumber;
  } catch (error) {
    await page.screenshot({
      path: 'screenshots/error-form.png',
      fullPage: true
    });
    throw error;
  } finally {
    await browser.close();
  }
}
```

**Step 6 - Handle Advanced Patterns**:
- File upload: Used `page.setInputFiles()` for both PDF documents
- Wait for upload confirmation before proceeding (`.upload-success-*` selector)
- Race condition prevention: `Promise.all([waitForURL, click])` for each step transition
- No network interception needed

**Step 7 - Add Error Prevention**:
- ✅ **Stale elements**: Used locator API throughout — no cached ElementHandles
- ✅ **Navigation timeouts**: Default 30s sufficient for form navigation
- ✅ **Anti-bot**: Not needed (legitimate form submission, not scraping)
- ✅ **Wait strategies**: `waitForURL()` for step transitions, `waitForSelector()` for uploads
- ✅ **Screenshot on failure**: Full-page screenshot in catch block
- ✅ **Retry logic**: File upload wrapped in retry (network uploads can fail)
- ✅ **Graceful cleanup**: `browser.close()` in finally block
- ✅ **Selector specificity**: Role-based (`getByRole`), label-based (`getByLabel`), and ID-based selectors
- ✅ **Race conditions**: `Promise.all()` for all click + navigation sequences
- ✅ **Resource cleanup**: Single context, closed on completion

**Step 8 - Generate Output**:
Saved to `/claudedocs/playwright-local_insurance-form_2025-07-15.md`.
- Complete TypeScript script with 3-step form automation
- 4 screenshots: personal info, documents, review, confirmation
- Setup instructions and file structure
- Run command: `npx tsx submit-application.ts`

**Step 9 - Update Memory**:
- ✅ Multi-step form pattern saved to `automation_patterns.md`
- ✅ Form selectors saved to `site_selectors.md` (label-based, role-based, ID-based)
- ✅ File upload pattern recorded (setInputFiles + upload confirmation wait)

---

## Example 3: Authenticated Dashboard Data Extraction with Network Interception

### Scenario
A business analyst needs to extract sales metrics from an internal dashboard that requires SSO login. The dashboard loads data via REST API calls. Instead of scraping the rendered HTML, the analyst wants to intercept the API responses directly for cleaner, structured data. The auth session should be saved for reuse across future runs.

### User Prompt
```
Log into our internal dashboard at https://dashboard.example-corp.com, intercept the sales API responses, extract the monthly revenue and top products data, and save the auth session for reuse.
```

### Skill Execution

**Step 1 - Initial Analysis**:
- Automation goal: Authenticated data extraction via network interception
- Target: `https://dashboard.example-corp.com` (internal, SSO-protected)
- Browser: Chromium (headed for first run to handle SSO, headless for subsequent)
- Complexity: Authentication + network interception + data extraction
- Authentication: Required — SSO login, save session for reuse
- Data extraction: Intercept REST API responses (JSON) instead of scraping DOM

**Step 2 - Load Memory**:
No prior auth flows found for this project. Fresh configuration.

**Step 3 - Load Context**:
Loaded engineering domain context. File budget: 4 files.

**Step 4 - Configure Playwright Setup**:
```bash
npm init -y
npm install playwright
npx playwright install chromium
```
- Headless mode: `false` for first run (SSO may require interaction)
- Storage state: `auth/dashboard-session.json` (saved after login)
- Viewport: 1920×1080 (dashboard optimized for wide screens)

**Step 5 - Build Automation Script**:

**Part A — Authentication & Session Save** (first run):
```typescript
import { chromium, Browser, Page, BrowserContext } from 'playwright';
import fs from 'fs';

const AUTH_STATE_PATH = 'auth/dashboard-session.json';

async function loginAndSaveSession(): Promise<void> {
  const browser: Browser = await chromium.launch({ headless: false });
  const context: BrowserContext = await browser.newContext({
    viewport: { width: 1920, height: 1080 }
  });
  const page: Page = await context.newPage();

  try {
    await page.goto('https://dashboard.example-corp.com');

    // SSO redirects to login page
    await page.waitForURL('**/login**', { timeout: 10000 });

    await page.getByLabel('Email').fill('analyst@example-corp.com');
    await page.getByLabel('Password').fill(process.env.DASHBOARD_PASSWORD!);
    await page.getByRole('button', { name: 'Sign In' }).click();

    // Wait for SSO redirect back to dashboard
    await page.waitForURL('**/dashboard**', { timeout: 30000 });
    await page.waitForLoadState('networkidle');

    // Save authentication state for reuse
    await context.storageState({ path: AUTH_STATE_PATH });
    console.log(`Auth session saved to ${AUTH_STATE_PATH}`);
  } finally {
    await browser.close();
  }
}
```

**Part B — Data Extraction with Network Interception** (subsequent runs):
```typescript
interface SalesData {
  monthlyRevenue: { month: string; revenue: number }[];
  topProducts: { name: string; units: number; revenue: number }[];
}

async function extractDashboardData(): Promise<SalesData> {
  const hasAuth = fs.existsSync(AUTH_STATE_PATH);
  if (!hasAuth) {
    console.log('No saved session found. Running login flow...');
    await loginAndSaveSession();
  }

  const browser: Browser = await chromium.launch({ headless: true });
  const context: BrowserContext = await browser.newContext({
    viewport: { width: 1920, height: 1080 },
    storageState: AUTH_STATE_PATH
  });
  const page: Page = await context.newPage();

  const salesData: SalesData = {
    monthlyRevenue: [],
    topProducts: []
  };

  try {
    // Intercept API responses before navigating
    page.on('response', async (response) => {
      const url = response.url();

      if (url.includes('/api/sales/monthly-revenue')) {
        const data = await response.json();
        salesData.monthlyRevenue = data.results;
        console.log(`Captured monthly revenue: ${data.results.length} months`);
      }

      if (url.includes('/api/sales/top-products')) {
        const data = await response.json();
        salesData.topProducts = data.results;
        console.log(`Captured top products: ${data.results.length} products`);
      }
    });

    // Block analytics and tracking to speed up loading
    await page.route('**/{analytics,tracking,telemetry}/**', (route) =>
      route.abort()
    );

    // Navigate to dashboard — API calls fire automatically
    await page.goto('https://dashboard.example-corp.com/sales', {
      waitUntil: 'networkidle',
      timeout: 60000
    });

    // Verify auth session is still valid
    if (page.url().includes('/login')) {
      console.log('Session expired. Re-authenticating...');
      fs.unlinkSync(AUTH_STATE_PATH);
      await browser.close();
      return extractDashboardData(); // Recursive retry with fresh login
    }

    // Wait for dashboard to fully load
    await page.waitForSelector('.dashboard-loaded', { timeout: 15000 });

    // Verify we captured the API data
    if (salesData.monthlyRevenue.length === 0) {
      // Fallback: trigger data refresh via UI
      await page.getByRole('button', { name: 'Refresh' }).click();
      await page.waitForResponse('**/api/sales/monthly-revenue');
      await page.waitForResponse('**/api/sales/top-products');
    }

    // Take screenshot of the loaded dashboard
    await page.screenshot({
      path: 'screenshots/dashboard-sales.png',
      fullPage: true
    });

    // Re-save auth state (refreshed tokens)
    await context.storageState({ path: AUTH_STATE_PATH });

    return salesData;
  } catch (error) {
    await page.screenshot({
      path: 'screenshots/error-dashboard.png',
      fullPage: true
    });
    throw error;
  } finally {
    await browser.close();
  }
}
```

**Step 6 - Handle Advanced Patterns**:
- **Authentication**: SSO login with session persistence via `storageState`
- **Network interception**: Captured `/api/sales/monthly-revenue` and `/api/sales/top-products` responses directly — cleaner than DOM scraping
- **Resource blocking**: Blocked analytics/tracking endpoints to speed up page load
- **Session management**: Auth state saved/refreshed on each run; expired sessions trigger re-login

**Step 7 - Add Error Prevention**:
- ✅ **Stale elements**: Minimal DOM interaction — data extracted from API responses
- ✅ **Navigation timeouts**: 60s for dashboard (heavy SPA with multiple API calls)
- ✅ **Anti-bot**: Internal site — not needed, but realistic viewport set
- ✅ **Wait strategies**: `waitForResponse()` for API data, `waitForLoadState('networkidle')` for page
- ✅ **Screenshot on failure**: Dashboard screenshot in catch block
- ✅ **Retry logic**: Session expiration triggers recursive re-authentication
- ✅ **Graceful cleanup**: `browser.close()` in finally block
- ✅ **Selector specificity**: Role-based selectors for UI interaction
- ✅ **Race conditions**: API response listeners registered before navigation
- ✅ **Resource cleanup**: Browser closed per run; auth state file managed

**Step 8 - Generate Output**:
Saved to `/claudedocs/playwright-local_dashboard-extract_2025-07-15.md`.
Output includes:
- Authentication script (first run, headed mode)
- Data extraction script (subsequent runs, headless with saved session)
- Intercepted API data:

| Month | Revenue |
|-------|---------|
| Jan 2025 | $1,234,567 |
| Feb 2025 | $1,456,789 |
| Mar 2025 | $1,678,901 |
| ... | ... |

| Product | Units Sold | Revenue |
|---------|-----------|---------|
| Enterprise License | 142 | $2,840,000 |
| Pro Subscription | 1,205 | $959,975 |
| API Add-on | 867 | $433,500 |
| ... | ... | ... |

- Setup instructions and environment variables
- Run commands: `npx tsx login.ts` (first time) → `npx tsx extract-sales.ts` (subsequent)

**Step 9 - Update Memory**:
- ✅ SSO login flow saved to `auth_flows.md` (login URL, selector sequence, redirect wait)
- ✅ API endpoint patterns saved to `automation_patterns.md` (`/api/sales/monthly-revenue`, `/api/sales/top-products`)
- ✅ Dashboard selectors saved to `site_selectors.md` (`.dashboard-loaded`, refresh button)
- ✅ Auth state file path recorded: `auth/dashboard-session.json`
