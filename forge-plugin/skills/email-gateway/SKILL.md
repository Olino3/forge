---
name: "email-gateway"
description: "Multi-provider email sending for Cloudflare Workers and Node.js applications. Supports Resend, SendGrid, Mailgun, and SMTP2Go providers with unified API, template rendering, and delivery tracking."
version: "1.0.0"
context:
  primary_domain: "engineering"
  always_load_files: []
  detection_required: false
  file_budget: 4
memory:
  scopes:
    - type: "skill-specific"
      files: [provider_config.md, template_patterns.md]
    - type: "shared-project"
      usage: "reference"
---

# skill:email-gateway - Multi-Provider Email Gateway

## Version: 1.0.0

## Purpose

Generate production-ready email sending integrations for Cloudflare Workers and Node.js applications. This skill produces a unified email interface that abstracts provider-specific APIs (Resend, SendGrid, Mailgun, SMTP2Go), includes template rendering, error handling with retry logic, and delivery tracking via webhooks. Use this skill when a project needs transactional or notification email capabilities with provider flexibility.

## File Structure

```
skills/email-gateway/
├── SKILL.md (this file)
├── examples.md
├── scripts/ (optional)
│   └── [helper scripts]
└── templates/ (optional)
    └── [output templates]
```

## Interface References

- **Context**: Loaded via [ContextProvider Interface](../../interfaces/context_provider.md)
- **Memory**: Accessed via [MemoryStore Interface](../../interfaces/memory_store.md)
- **Shared Patterns**: [Shared Loading Patterns](../../interfaces/shared_loading_patterns.md)
- **Schemas**: Validated against [context_metadata.schema.json](../../interfaces/schemas/context_metadata.schema.json) and [memory_entry.schema.json](../../interfaces/schemas/memory_entry.schema.json)

## Mandatory Workflow

> **IMPORTANT**: Execute ALL steps in order. Do not skip any step.

### Step 1: Initial Analysis

- Gather inputs: provider choice (Resend, SendGrid, Mailgun, SMTP2Go), target environment (Cloudflare Workers vs Node.js), template needs (plain text, HTML, React Email)
- Detect project type: runtime, framework (Express, Hono, itty-router), existing email dependencies
- Determine project name for memory lookup
- Identify if multi-provider failover is required
- Note any existing email infrastructure or provider accounts

### Step 2: Load Memory

> Follow [Standard Memory Loading](../../interfaces/shared_loading_patterns.md#pattern-1-standard-memory-loading) with `skill="email-gateway"` and `domain="engineering"`.

- Load `provider_config.md` — previous provider configurations, API key patterns, from-address conventions
- Load `template_patterns.md` — previously used email templates, rendering approaches, design patterns

### Step 3: Load Context

> Follow [Standard Context Loading](../../interfaces/shared_loading_patterns.md#pattern-2-standard-context-loading) for the `engineering` domain. Stay within the file budget declared in frontmatter.

- Load relevant engineering context for the target runtime (Cloudflare Workers API, Node.js patterns)
- Load API integration patterns if available

### Step 4: Configure Provider

**Purpose**: Set up the chosen email provider(s) with proper configuration

**Actions**:
1. Define API key management strategy (environment variables, secrets binding)
2. Configure provider endpoints and authentication:
   - **Resend**: `https://api.resend.com/emails` with Bearer token
   - **SendGrid**: `https://api.sendgrid.com/v3/mail/send` with Bearer token
   - **Mailgun**: `https://api.mailgun.net/v3/{domain}/messages` with Basic auth
   - **SMTP2Go**: `https://api.smtp2go.com/v3/email/send` with api-key header
3. Set default from addresses, reply-to addresses, and sender names
4. Configure provider-specific options (tracking, tags, metadata)
5. For multi-provider setups, define primary/fallback order and failover triggers

**Output**: Complete provider configuration ready for code generation

### Step 5: Generate Email Integration

**Purpose**: Produce the email sending code with unified interface

**Actions**:
1. **Generate unified email interface**:
   - `EmailMessage` type (to, from, subject, html, text, cc, bcc, replyTo, attachments)
   - `EmailResult` type (id, provider, status, timestamp)
   - `EmailProvider` interface (send, sendBatch, validateAddress)

2. **Generate provider adapter(s)**:
   - Provider-specific API client implementing `EmailProvider`
   - Request/response mapping to unified types
   - Authentication header construction
   - Rate limit awareness per provider

3. **Generate template rendering**:
   - HTML template rendering (string interpolation or React Email for Resend)
   - Plain text fallback generation
   - Template variable validation
   - Reusable layout components (header, footer, button)

4. **Generate error handling**:
   - Provider-specific error code mapping to unified error types
   - Retry logic with exponential backoff for transient failures (429, 500, 502, 503)
   - Non-retryable error identification (400, 401, 403, invalid recipient)
   - Structured error logging

5. **Generate retry logic**:
   - Configurable max retries and backoff multiplier
   - Provider failover on persistent failure (if multi-provider)
   - Dead letter handling for permanently failed sends

**Output**: Complete email integration module with all components

### Step 6: Implement Delivery Tracking

**Purpose**: Add webhook handling for email delivery lifecycle

**Actions**:
1. **Generate webhook endpoint**:
   - Route handler for provider webhook callbacks
   - Signature verification per provider (Resend uses svix, SendGrid uses event webhook signing, Mailgun uses signing key)
   - Event payload parsing to unified delivery event type

2. **Generate delivery status tracking**:
   - Event types: delivered, bounced, complained, opened, clicked, unsubscribed
   - Status persistence strategy (KV store for Workers, database for Node.js)
   - Bounce classification (hard bounce vs soft bounce)

3. **Generate complaint handling**:
   - Automatic suppression list management
   - Complaint notification to administrators
   - Unsubscribe link generation and handling

**Output**: Webhook handlers and delivery tracking integration

### Step 7: Generate Output

- Save output to `/claudedocs/email-gateway_{project}_{YYYY-MM-DD}.md`
- Follow naming conventions in `../OUTPUT_CONVENTIONS.md`
- Include: generated file manifest, configuration checklist, provider setup instructions, testing guide
- Use templates from `templates/` directory if available

### Step 8: Update Memory

> Follow [Standard Memory Update](../../interfaces/shared_loading_patterns.md#pattern-3-standard-memory-update) for `skill="email-gateway"`. Store any newly learned patterns, conventions, or project insights.

- Update `provider_config.md` with provider choices, configuration patterns, API quirks encountered
- Update `template_patterns.md` with template designs, rendering approaches, reusable components

## Compliance Checklist

Before completing, verify:

- [ ] All mandatory workflow steps executed in order
- [ ] Standard Memory Loading pattern followed (Step 2)
- [ ] Standard Context Loading pattern followed (Step 3)
- [ ] Provider configured with secure API key management (Step 4)
- [ ] Unified email interface generated with provider adapter (Step 5)
- [ ] Template rendering implemented with plain text fallback (Step 5)
- [ ] Error handling includes retry logic and structured logging (Step 5)
- [ ] Webhook signature verification implemented per provider (Step 6)
- [ ] Delivery tracking covers bounces and complaints (Step 6)
- [ ] Output saved with standard naming convention (Step 7)
- [ ] Standard Memory Update pattern followed (Step 8)

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2025-07-18 | Initial release — Resend, SendGrid, Mailgun, SMTP2Go support; unified API; template rendering; delivery tracking |
