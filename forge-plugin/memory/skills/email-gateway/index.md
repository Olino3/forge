# Memory Structure: email-gateway

## Purpose

This directory stores **project-specific** email provider configurations, template patterns, and integration decisions learned during email gateway setup. Memory enables the skill to recall provider preferences, template designs, and delivery tracking strategies across invocations for the same project.

## Directory Structure

```
email-gateway/
├── index.md                    # This file - explains memory structure
└── {project-name}/             # Per-project memory (created on first use)
    ├── provider_config.md      # Provider choices, API patterns, failover setup
    └── template_patterns.md    # Email template designs, rendering approaches
```

## Memory Files

### 1. `provider_config.md`

**What to store**:
- Provider chosen (Resend, SendGrid, Mailgun, SMTP2Go)
- Environment type (Cloudflare Workers, Node.js)
- API key management approach (env vars, secrets binding, vault)
- From/reply-to address conventions
- Multi-provider failover configuration (if applicable)
- Provider-specific options (tracking settings, tags, metadata)
- Rate limit observations and retry configuration
- Webhook endpoints and signature verification details
- Generation timestamp and skill version

### 2. `template_patterns.md`

**What to store**:
- Template rendering approach (React Email, HTML string interpolation, plain text)
- Template names and their purposes (welcome, reset, invoice, alert, etc.)
- Reusable components (layouts, buttons, headers, footers)
- Design conventions (colors, fonts, spacing from project brand)
- Plain text fallback generation strategy
- Template variable naming conventions
- Attachment handling patterns

## Why This Skill Needs Memory

Email integrations involve **choices that must remain consistent** across a project's lifetime:

1. **Provider lock-in awareness**: Switching providers mid-project requires adapter changes — memory tracks which provider is active and why it was chosen
2. **Template consistency**: Email templates share brand elements (colors, logos, layouts) — memory captures these patterns so new templates match existing ones
3. **Configuration continuity**: API key naming, from-address conventions, and webhook URLs must stay consistent when adding new email types
4. **Failover history**: For multi-provider setups, memory records which provider combinations were tested and which failover triggers were configured

## Memory Growth Pattern

### First Invocation
- Record provider choice and configuration
- Store initial template designs and rendering approach
- Document environment setup (Workers vs Node.js, secrets management)

### Subsequent Invocations
- Add new template patterns to `template_patterns.md`
- Update `provider_config.md` if provider settings change
- Record provider API quirks or rate limit observations
- Track failover events and reliability patterns

### Maintenance
- Update when provider API versions change
- Refresh template patterns when brand guidelines update
- Archive deprecated template designs
- Update webhook configurations when endpoints change

## Memory vs Context

- **Context** (`../../../context/engineering/`): **Shared, static** engineering patterns — API integration best practices, error handling conventions, retry strategies
- **Memory** (this directory): **Project-specific, dynamic** email configuration — which provider this project uses, what templates exist, how delivery tracking is implemented

**Example**:
- Context says: "Use exponential backoff with jitter for API retries"
- Memory records: "This project uses Resend as primary provider with React Email templates, from address `notifications@myapp.com`, webhook at `/webhooks/resend`, and KV namespace `EMAIL_EVENTS` for delivery tracking"

## Related Files

- `../../../skills/email-gateway/SKILL.md` — Skill workflow
- `../../../skills/email-gateway/examples.md` — Usage examples
- `/claudedocs/` — Detailed generation reports (if created)
