# Email Gateway Examples

This file demonstrates typical usage scenarios for the `email-gateway` skill.

---

## Example 1: Resend on Cloudflare Workers with React Email Templates

### Scenario

A SaaS application running on Cloudflare Workers needs transactional emails (welcome, password reset, invoice) using Resend with React Email templates for type-safe, component-based email design.

### User Prompt

"Set up email sending in my Cloudflare Workers app using Resend. I want to use React Email for templates. I need welcome emails, password reset emails, and invoice emails."

### Skill Execution

**Step 1: Initial Analysis**

- Environment: Cloudflare Workers (no Node.js runtime — uses `fetch` API)
- Provider: Resend (native React Email support)
- Templates needed: welcome, password-reset, invoice
- Framework detected: Hono on Workers
- Project name: `saas-platform`

**Step 2: Load Memory**

- No existing memory for `saas-platform` — first-time setup

**Step 3: Load Context**

- Load engineering domain context for Cloudflare Workers patterns
- Note: Workers environment has no `node:fs` or `node:net` — must use `fetch`-based API calls

**Step 4: Configure Provider**

- Provider: Resend
- API endpoint: `https://api.resend.com/emails`
- API key: bound via `env.RESEND_API_KEY` (Workers secret)
- From address: `notifications@saasplatform.com`
- React Email: installed as dependency, templates compiled at build time

Configuration:
```typescript
const config = {
  provider: 'resend',
  apiKey: env.RESEND_API_KEY,
  defaults: {
    from: 'SaaS Platform <notifications@saasplatform.com>',
    replyTo: 'support@saasplatform.com',
  },
};
```

**Step 5: Generate Email Integration**

Generated files:
```
src/
├── email/
│   ├── provider.ts          # Resend provider adapter using fetch
│   ├── types.ts             # EmailMessage, EmailResult types
│   ├── send.ts              # Unified send function with retry
│   └── templates/
│       ├── welcome.tsx       # React Email welcome template
│       ├── password-reset.tsx
│       ├── invoice.tsx
│       └── components/
│           ├── layout.tsx    # Shared email layout
│           └── button.tsx    # Reusable CTA button
```

Provider adapter uses Workers-compatible `fetch`:
```typescript
async send(message: EmailMessage): Promise<EmailResult> {
  const response = await fetch('https://api.resend.com/emails', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${this.apiKey}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      from: message.from,
      to: message.to,
      subject: message.subject,
      react: message.react,
      text: message.text,
    }),
  });
  // ... error handling and response mapping
}
```

**Step 6: Implement Delivery Tracking**

- Webhook endpoint at `POST /webhooks/resend`
- Svix signature verification using `wrangler secret put RESEND_WEBHOOK_SECRET`
- Delivery events stored in Workers KV namespace `EMAIL_EVENTS`

**Step 7: Generate Output**

- Output saved to `/claudedocs/email-gateway_saas-platform_2025-07-18.md`
- Includes: file manifest, Resend dashboard setup instructions, DNS verification steps

**Step 8: Update Memory**

- Stored Resend + Workers configuration pattern in `provider_config.md`
- Stored React Email template component patterns in `template_patterns.md`

---

## Example 2: SendGrid with Node.js Express for Transactional Emails

### Scenario

An Express.js API server needs SendGrid integration for order confirmation, shipping notification, and account verification emails with HTML templates and plain text fallbacks.

### User Prompt

"Add SendGrid email sending to my Express app. I need order confirmation, shipping notification, and account verification emails. Use HTML templates with plain text fallbacks."

### Skill Execution

**Step 1: Initial Analysis**

- Environment: Node.js with Express
- Provider: SendGrid
- Templates needed: order-confirmation, shipping-notification, account-verification
- Existing dependencies: `express`, `dotenv`
- Project name: `ecommerce-api`

**Step 2: Load Memory**

- No existing memory — first-time setup

**Step 3: Load Context**

- Load engineering domain context for Node.js API patterns

**Step 4: Configure Provider**

- Provider: SendGrid
- API endpoint: `https://api.sendgrid.com/v3/mail/send`
- API key: loaded from `process.env.SENDGRID_API_KEY`
- From address: `orders@shopexample.com`
- Tracking: open tracking enabled, click tracking enabled

Configuration:
```typescript
const config = {
  provider: 'sendgrid',
  apiKey: process.env.SENDGRID_API_KEY,
  defaults: {
    from: { email: 'orders@shopexample.com', name: 'Shop Example' },
    replyTo: 'support@shopexample.com',
    trackingSettings: {
      openTracking: { enable: true },
      clickTracking: { enable: true },
    },
  },
};
```

**Step 5: Generate Email Integration**

Generated files:
```
src/
├── email/
│   ├── provider.ts           # SendGrid provider adapter
│   ├── types.ts              # Unified email types
│   ├── send.ts               # Send function with retry and logging
│   ├── retry.ts              # Exponential backoff retry utility
│   └── templates/
│       ├── order-confirmation.html
│       ├── order-confirmation.txt
│       ├── shipping-notification.html
│       ├── shipping-notification.txt
│       ├── account-verification.html
│       ├── account-verification.txt
│       └── render.ts         # Template variable interpolation
```

SendGrid adapter handles personalizations and categories:
```typescript
async send(message: EmailMessage): Promise<EmailResult> {
  const response = await fetch('https://api.sendgrid.com/v3/mail/send', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${this.apiKey}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      personalizations: [{ to: [{ email: message.to }] }],
      from: { email: message.from },
      subject: message.subject,
      content: [
        { type: 'text/plain', value: message.text },
        { type: 'text/html', value: message.html },
      ],
      categories: message.tags,
    }),
  });
  // ... error handling
}
```

Retry utility with exponential backoff:
```typescript
async function withRetry<T>(
  fn: () => Promise<T>,
  { maxRetries = 3, baseDelay = 1000 } = {}
): Promise<T> {
  for (let attempt = 0; attempt <= maxRetries; attempt++) {
    try {
      return await fn();
    } catch (error) {
      if (!isRetryable(error) || attempt === maxRetries) throw error;
      await sleep(baseDelay * Math.pow(2, attempt));
    }
  }
}
```

**Step 6: Implement Delivery Tracking**

- Webhook endpoint at `POST /webhooks/sendgrid`
- Event webhook signature verification using SendGrid's public key
- Events stored in database via existing ORM
- Bounce handler adds addresses to suppression table

**Step 7: Generate Output**

- Output saved to `/claudedocs/email-gateway_ecommerce-api_2025-07-18.md`
- Includes: SendGrid API key setup, sender authentication, event webhook configuration

**Step 8: Update Memory**

- Stored SendGrid + Express configuration pattern in `provider_config.md`
- Stored HTML/text template pair pattern in `template_patterns.md`

---

## Example 3: Multi-Provider Setup with Failover (Mailgun Primary, SMTP2Go Fallback)

### Scenario

A high-availability notification service requires guaranteed email delivery. Mailgun is the primary provider with SMTP2Go as automatic fallback if Mailgun returns errors or is unreachable.

### User Prompt

"Set up email sending with Mailgun as primary and SMTP2Go as fallback. If Mailgun fails, automatically retry with SMTP2Go. This is a Node.js service that sends critical alert notifications."

### Skill Execution

**Step 1: Initial Analysis**

- Environment: Node.js (standalone service, no web framework)
- Providers: Mailgun (primary), SMTP2Go (fallback)
- Multi-provider failover required
- Template needs: alert notification (HTML + text)
- Project name: `alert-service`

**Step 2: Load Memory**

- No existing memory — first-time setup

**Step 3: Load Context**

- Load engineering domain context for Node.js service patterns

**Step 4: Configure Provider**

- Primary: Mailgun (`https://api.mailgun.net/v3/{domain}/messages`)
- Fallback: SMTP2Go (`https://api.smtp2go.com/v3/email/send`)
- Failover triggers: HTTP 500, 502, 503, 429, network timeout, connection refused

Configuration:
```typescript
const config = {
  strategy: 'failover',
  providers: [
    {
      name: 'mailgun',
      priority: 1,
      apiKey: process.env.MAILGUN_API_KEY,
      domain: process.env.MAILGUN_DOMAIN,
      endpoint: `https://api.mailgun.net/v3/${process.env.MAILGUN_DOMAIN}/messages`,
    },
    {
      name: 'smtp2go',
      priority: 2,
      apiKey: process.env.SMTP2GO_API_KEY,
      endpoint: 'https://api.smtp2go.com/v3/email/send',
    },
  ],
  defaults: {
    from: 'Alert Service <alerts@alertservice.com>',
  },
  retry: { maxRetries: 2, baseDelay: 500 },
};
```

**Step 5: Generate Email Integration**

Generated files:
```
src/
├── email/
│   ├── types.ts               # Unified types
│   ├── providers/
│   │   ├── interface.ts       # EmailProvider interface
│   │   ├── mailgun.ts         # Mailgun adapter (Basic auth, form data)
│   │   └── smtp2go.ts         # SMTP2Go adapter (JSON, api-key header)
│   ├── failover.ts            # Failover orchestrator
│   ├── retry.ts               # Retry with exponential backoff
│   ├── send.ts                # Unified send entry point
│   └── templates/
│       ├── alert-notification.html
│       ├── alert-notification.txt
│       └── render.ts
```

Failover orchestrator tries providers in priority order:
```typescript
async send(message: EmailMessage): Promise<EmailResult> {
  const errors: Error[] = [];
  for (const provider of this.providers) {
    try {
      const result = await withRetry(
        () => provider.send(message),
        this.retryConfig,
      );
      return { ...result, provider: provider.name };
    } catch (error) {
      errors.push(error);
      logger.warn(`Provider ${provider.name} failed, trying next`, { error });
    }
  }
  throw new AllProvidersFailedError(errors);
}
```

Mailgun adapter uses form-encoded data with Basic auth:
```typescript
async send(message: EmailMessage): Promise<EmailResult> {
  const form = new URLSearchParams();
  form.append('from', message.from);
  form.append('to', message.to);
  form.append('subject', message.subject);
  form.append('html', message.html);
  form.append('text', message.text);

  const response = await fetch(this.endpoint, {
    method: 'POST',
    headers: {
      'Authorization': `Basic ${btoa(`api:${this.apiKey}`)}`,
    },
    body: form,
  });
  // ... error handling and response mapping
}
```

**Step 6: Implement Delivery Tracking**

- Separate webhook endpoints for each provider:
  - `POST /webhooks/mailgun` — Mailgun signing key verification
  - `POST /webhooks/smtp2go` — SMTP2Go callback verification
- Unified delivery event type normalizes events from both providers
- Dead letter log for emails that failed on all providers

**Step 7: Generate Output**

- Output saved to `/claudedocs/email-gateway_alert-service_2025-07-18.md`
- Includes: both provider setup instructions, failover testing guide, monitoring recommendations

**Step 8: Update Memory**

- Stored multi-provider failover pattern in `provider_config.md`
- Stored alert notification template pattern in `template_patterns.md`

---

## Common Patterns Across Examples

### Provider Selection

| Provider | Best For | Auth Style | Body Format |
|----------|----------|------------|-------------|
| Resend | Modern apps, React Email, Workers | Bearer token | JSON |
| SendGrid | Enterprise, high volume, analytics | Bearer token | JSON |
| Mailgun | Transactional, EU compliance | Basic auth | Form data |
| SMTP2Go | Reliability, fallback provider | API key header | JSON |

### Environment Considerations

| Feature | Cloudflare Workers | Node.js |
|---------|-------------------|---------|
| HTTP client | `fetch` (native) | `fetch` (Node 18+) or `node-fetch` |
| Secrets | `env.SECRET_NAME` (wrangler) | `process.env.SECRET_NAME` (.env) |
| Webhook storage | Workers KV / D1 | Database (PostgreSQL, etc.) |
| Template rendering | Build-time (React Email) | Runtime (string interpolation) |

### Retry Strategy

All examples use the same retry approach:
1. Retry on transient errors (429, 500, 502, 503)
2. Do not retry on client errors (400, 401, 403)
3. Exponential backoff with configurable base delay
4. Multi-provider: exhaust retries on primary before failing over
