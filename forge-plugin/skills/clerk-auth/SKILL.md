---
name: clerk-auth
description: "Clerk auth with API Keys beta (Dec 2025), Next.js 16 proxy.ts (March 2025 CVE context), API version 2025-11-10 breaking changes, clerkMiddleware() options, webhooks, production considerations. Prevents 15 errors."
version: "1.0.0"
context:
  primary_domain: "security"
  always_load_files: []
  detection_required: true
  file_budget: 4
memory:
  scopes:
    - type: "skill-specific"
      files: [project_overview.md, common_patterns.md]
    - type: "shared-project"
##       usage: "reference"

# skill:clerk-auth - Clerk Authentication Integration

## Version: 1.0.0

## Purpose

Implements Clerk authentication integration for Next.js applications using `@clerk/nextjs`. This skill covers the full Clerk auth lifecycle: `clerkMiddleware()` configuration, API Keys beta (Dec 2025), Next.js 16 `proxy.ts` (March 2025 CVE context), API version `2025-11-10` breaking changes, webhook handlers with svix verification, and production deployment considerations.

**Use this skill when**:
- Setting up Clerk authentication in a Next.js project (App Router or Pages Router)
- Configuring `clerkMiddleware()` with route protection and public routes
- Enabling API Keys beta for machine-to-machine authentication
- Setting up `proxy.ts` for Next.js 16 satellite domain requirements
- Implementing Clerk webhook handlers with svix signature verification
- Migrating to API version `2025-11-10` breaking changes
- Resolving common Clerk auth errors and misconfigurations

**What it produces**:
- `@clerk/nextjs` SDK setup and configuration
- `clerkMiddleware()` with route matchers and protection rules
- API Keys beta configuration for M2M auth
- `proxy.ts` setup for Next.js 16 proxy requirements
- Webhook endpoint with svix verification
- API version migration guide for `2025-11-10` changes
- Environment variable configuration for dev and production
- Client-side auth integration with `<ClerkProvider>`, `<SignIn>`, `<SignUp>` components

**Triggers**: `clerk`, `clerk auth`, `@clerk/nextjs`

### 15 Common Errors Prevented

| # | Error | Prevention |
|---|-------|------------|
| 1 | Middleware not running on API routes | Configure `matcher` in `middleware.ts` to include `/api/(.*)` |
| 2 | `auth()` returning null in Server Components | Ensure `clerkMiddleware()` runs before the route; check matcher config |
| 3 | `auth()` vs `currentUser()` confusion | Use `auth()` for session/userId, `currentUser()` for full user object |
| 4 | Missing `publicRoutes` causing auth loops | Define public routes via `createRouteMatcher()` in middleware |
| 5 | Webhook signature verification failures | Use `svix` library with correct `CLERK_WEBHOOK_SECRET`; pass raw body |
| 6 | Webhook raw body parsing issues | Disable Next.js body parsing for webhook route; use `Readable` stream |
| 7 | CORS errors on cross-origin requests | Configure `allowedOrigins` in `clerkMiddleware()` options |
| 8 | API version deprecation breaking changes | Pin `CLERK_API_VERSION=2025-11-10`; update response handling |
| 9 | `clerkClient` import confusion (v5 vs v4) | Use `import { clerkClient } from '@clerk/nextjs/server'` in v5 |
| 10 | `publishableKey` vs `secretKey` mix-up | `NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY` for client, `CLERK_SECRET_KEY` for server |
| 11 | JWT token not forwarded to API routes | Use `auth().getToken()` and pass as `Authorization: Bearer` header |
| 12 | `<ClerkProvider>` missing in root layout | Wrap `{children}` in `<ClerkProvider>` in `app/layout.tsx` |
| 13 | Middleware file in wrong location | Place `middleware.ts` in project root (same level as `app/`) |
| 14 | API Keys beta not enabling M2M auth | Set `CLERK_API_KEYS_BETA=true` and configure API key verification |
| 15 | Next.js 16 proxy.ts CVE misconfiguration | Follow Clerk proxy.ts guide; validate origin headers to prevent SSRF |

## File Structure

```
skills/clerk-auth/
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

- Gather inputs: auth requirements, route protection needs, webhook events
- Detect **Next.js version** (13/14/15/16) — determines proxy.ts needs and App Router vs Pages Router
- Detect **Clerk SDK version** (`@clerk/nextjs` v4 vs v5) — determines import paths and API shape
- Check for existing auth setup (Clerk or other) to avoid conflicts
- Check `package.json` for `@clerk/nextjs`, `svix`, and related dependencies
- Determine project name for memory lookup

### Step 2: Load Memory

> Follow [Standard Memory Loading](../../interfaces/shared_loading_patterns.md#pattern-1-standard-memory-loading) with `skill="clerk-auth"` and `domain="security"`.

- Load `project_overview.md` — understand project's Clerk auth history and config
- Load `common_patterns.md` — reuse previously established middleware and webhook patterns
- If first run: create memory directory for the project

### Step 3: Load Context

> Follow [Standard Context Loading](../../interfaces/shared_loading_patterns.md#pattern-2-standard-context-loading) for the `security` domain. Stay within the file budget declared in frontmatter.

- Load security domain context relevant to authentication, OAuth, and webhook security
- Cross-reference with any framework-specific context (Next.js middleware, API routes)
- Respect the file budget of 4 context files maximum

### Step 4: Implement Authentication

This is the core action. Set up Clerk auth with `@clerk/nextjs`:

#### 4a: @clerk/nextjs Setup

- Install `@clerk/nextjs` package
- Add `<ClerkProvider>` wrapper in `app/layout.tsx` (App Router) or `_app.tsx` (Pages Router)
- Configure environment variables:
  - `NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY` — client-side publishable key
  - `CLERK_SECRET_KEY` — server-side secret key
  - `NEXT_PUBLIC_CLERK_SIGN_IN_URL` — sign-in page route
  - `NEXT_PUBLIC_CLERK_SIGN_UP_URL` — sign-up page route

#### 4b: clerkMiddleware() Configuration

- Create `middleware.ts` in project root (same level as `app/` directory)
- Configure `clerkMiddleware()` with route protection:
  - Use `createRouteMatcher()` for public routes (sign-in, sign-up, marketing pages)
  - Use `createRouteMatcher()` for protected routes (dashboard, API routes)
  - Call `auth().protect()` for routes requiring authentication
- Configure middleware `matcher` in `config` export to include relevant paths
- Set `allowedOrigins` for cross-origin requests if needed

#### 4c: API Keys Beta Setup

- Enable API Keys beta with `CLERK_API_KEYS_BETA=true`
- Configure API key verification for M2M authentication endpoints
- Set up API key scoping and permissions
- Create server-side API key validation middleware

#### 4d: proxy.ts for Next.js 16

- Configure Clerk proxy for satellite domain requirements
- Set `CLERK_PROXY_URL` environment variable
- Create `proxy.ts` handler following Clerk's proxy guide
- Validate origin headers to prevent SSRF (March 2025 CVE context)

#### 4e: Webhook Handlers with svix Verification

- Install `svix` package for webhook signature verification
- Create webhook API route at `/api/webhooks/clerk`
- Configure webhook endpoint in Clerk Dashboard
- Implement signature verification using `Webhook` from `svix`:
  - Extract `svix-id`, `svix-timestamp`, `svix-signature` headers
  - Verify payload with `CLERK_WEBHOOK_SECRET`
  - Parse and validate webhook event type
- Handle key webhook events:
  - `user.created` — provision user in local database
  - `user.updated` — sync user profile changes
  - `user.deleted` — clean up user data
  - `session.created` / `session.ended` — audit logging
  - `organization.created` / `organization.membership.created` — org sync

#### 4f: API Version 2025-11-10 Migration

- Pin `CLERK_API_VERSION=2025-11-10` in environment variables
- Update deprecated API response handling:
  - `User` object shape changes
  - Pagination response format changes
  - Webhook event payload structure updates
- Test all Clerk API integrations against new version
- Update `clerkClient` usage for v5 import paths

### Step 5: Generate Output

- Save output to `/claudedocs/clerk-auth_{project}_{YYYY-MM-DD}.md`
- Follow naming conventions in `../OUTPUT_CONVENTIONS.md`
- Include:
  - Clerk SDK setup and configuration code
  - `clerkMiddleware()` configuration with route matchers
  - Webhook handler implementation
  - API Keys beta configuration (if applicable)
  - proxy.ts setup (if Next.js 16)
  - Environment variable list (publishable key, secret key, webhook secret)
  - Client-side component integration
  - Testing instructions for auth flows

### Step 6: Update Memory

> Follow [Standard Memory Update](../../interfaces/shared_loading_patterns.md#pattern-3-standard-memory-update) for `skill="clerk-auth"`. Store any newly learned patterns, conventions, or project insights.

- Update `project_overview.md` with Clerk configuration details
- Update `common_patterns.md` with middleware patterns, webhook patterns, and API key configurations
- Record any project-specific auth customizations or workarounds

## Compliance Checklist

Before completing, verify:

- [ ] All mandatory workflow steps executed in order
- [ ] Standard Memory Loading pattern followed (Step 2)
- [ ] Standard Context Loading pattern followed (Step 3)
- [ ] `<ClerkProvider>` wraps the application root layout
- [ ] `clerkMiddleware()` configured with correct route matchers
- [ ] `middleware.ts` placed in project root (not inside `app/`)
- [ ] Webhook handler verifies signatures with svix
- [ ] Environment variables use correct `NEXT_PUBLIC_` prefix for client-side keys
- [ ] `auth()` vs `currentUser()` used appropriately
- [ ] Output saved with standard naming convention
- [ ] Standard Memory Update pattern followed (Step 6)

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-02-12 | Initial release — Clerk auth with clerkMiddleware(), API Keys beta, Next.js 16 proxy.ts, webhooks with svix, API version 2025-11-10 migration |
