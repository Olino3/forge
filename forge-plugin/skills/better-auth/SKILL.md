---
name: better-auth
description: "Self-hosted auth for TypeScript/Cloudflare Workers with social auth, 2FA, passkeys, organizations, RBAC, and 15+ plugins. Requires Drizzle ORM or Kysely for D1 (no direct adapter)."
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
      usage: "reference"
---

# skill:better-auth - Self-Hosted TypeScript Authentication

## Version: 1.0.0

## Purpose

Implements self-hosted authentication for TypeScript applications using better-auth — a comprehensive, framework-agnostic auth library with 15+ plugins. This skill configures better-auth for Cloudflare Workers with Cloudflare D1 as the database, using Drizzle ORM or Kysely as the database adapter (better-auth has no direct D1 adapter).

**Use this skill when**:
- Setting up self-hosted authentication in a TypeScript project
- Building auth for Cloudflare Workers with D1 as the database
- Configuring social authentication providers (GitHub, Google, etc.)
- Adding 2FA/TOTP or passkey/WebAuthn support
- Implementing organizations with role-based access control (RBAC)
- Integrating better-auth plugins for extended functionality

**What it produces**:
- better-auth server configuration with Drizzle ORM or Kysely for D1
- Social authentication provider setup (GitHub, Google, Discord, etc.)
- 2FA/TOTP configuration and enrollment flow
- Passkey/WebAuthn registration and authentication
- Organization and RBAC plugin configuration
- Database schema and migration files for auth tables
- Client-side auth integration code

**Triggers**: `better-auth`, `authentication with D1`, `Cloudflare D1 auth setup`

## File Structure

```
skills/better-auth/
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

- Gather inputs: auth requirements, social providers, plugin selection
- Detect project type: confirm TypeScript project targeting Cloudflare Workers
- Detect ORM usage: determine whether project uses Drizzle ORM or Kysely for D1 access
- Determine project name for memory lookup
- Check for existing auth setup (if any) to avoid conflicts
- Check for existing `better-auth`, `drizzle-orm`, or `kysely` dependencies in `package.json`

### Step 2: Load Memory

> Follow [Standard Memory Loading](../../interfaces/shared_loading_patterns.md#pattern-1-standard-memory-loading) with `skill="better-auth"` and `domain="security"`.

- Load `project_overview.md` — understand project's auth history and stack
- Load `common_patterns.md` — reuse previously established auth patterns
- If first run: create memory directory for the project

### Step 3: Load Context

> Follow [Standard Context Loading](../../interfaces/shared_loading_patterns.md#pattern-2-standard-context-loading) for the `security` domain. Stay within the file budget declared in frontmatter.

- Load security domain context relevant to authentication, OAuth, and session management
- Cross-reference with any framework-specific context (Cloudflare Workers, D1 patterns)
- Respect the file budget of 4 context files maximum

### Step 4: Implement Authentication

This is the core action. Set up better-auth with the appropriate adapter and plugins:

#### 4a: Database Adapter Configuration (Drizzle ORM or Kysely)

- **Drizzle ORM adapter**:
  - Configure `drizzle-orm` with `d1` driver
  - Define auth schema tables (`user`, `session`, `account`, `verification`)
  - Generate and run migrations via `drizzle-kit`
- **Kysely adapter**:
  - Configure `kysely` with D1 dialect
  - Define auth table types and migrations
  - Set up Kysely instance bound to D1
- Ensure schema includes all columns required by better-auth and enabled plugins

#### 4b: better-auth Server Setup

- Install `better-auth` package
- Create auth instance with `betterAuth()`:
  - Configure `database` with the chosen adapter (Drizzle or Kysely)
  - Set `baseURL` and `secret` from environment variables
  - Configure `trustedOrigins` for CORS
- Mount auth handler in Cloudflare Workers request handler
- Bind D1 database in `wrangler.toml`

#### 4c: Social Authentication Providers

- Configure OAuth providers via `socialProviders`:
  - GitHub: `clientId` and `clientSecret` from environment
  - Google: `clientId` and `clientSecret` from environment
  - Additional providers as needed (Discord, Apple, etc.)
- Set callback URLs matching provider app registrations
- Handle OAuth state and PKCE where supported

#### 4d: Two-Factor Authentication (2FA/TOTP)

- Enable `twoFactor` plugin in better-auth config
- Configure TOTP settings (issuer name, digits, period)
- Implement enrollment flow: QR code generation → verification
- Handle 2FA challenge during sign-in
- Provide backup/recovery code generation

#### 4e: Passkeys / WebAuthn

- Enable `passkey` plugin with WebAuthn configuration
- Configure relying party ID and name
- Implement passkey registration flow
- Implement passkey authentication flow
- Handle platform authenticator vs cross-platform authenticator

#### 4f: Organizations and RBAC

- Enable `organization` plugin in better-auth config
- Define roles and permissions schema
- Configure organization creation and membership management
- Set up role-based access control for API routes
- Implement invitation flow for organization members

### Step 5: Generate Output

- Save output to `/claudedocs/better-auth_{project}_{YYYY-MM-DD}.md`
- Follow naming conventions in `../OUTPUT_CONVENTIONS.md`
- Include:
  - Database schema and migration instructions
  - better-auth server configuration code
  - Social provider setup checklist
  - 2FA/TOTP enrollment and verification flow
  - Passkey registration and authentication flow
  - Organization and RBAC configuration
  - Environment variable list (secrets, client IDs, D1 binding)
  - Client-side integration code
  - Testing instructions for the auth flows

### Step 6: Update Memory

> Follow [Standard Memory Update](../../interfaces/shared_loading_patterns.md#pattern-3-standard-memory-update) for `skill="better-auth"`. Store any newly learned patterns, conventions, or project insights.

- Update `project_overview.md` with better-auth configuration details
- Update `common_patterns.md` with adapter patterns and plugin configurations used
- Record any project-specific auth customizations or workarounds

## Compliance Checklist

Before completing, verify:

- [ ] All mandatory workflow steps executed in order
- [ ] Standard Memory Loading pattern followed (Step 2)
- [ ] Standard Context Loading pattern followed (Step 3)
- [ ] Database adapter configured (Drizzle ORM or Kysely — not direct D1)
- [ ] Auth schema includes all required tables and columns
- [ ] Social providers configured with environment-based secrets
- [ ] Plugins enabled and configured as requested
- [ ] Output saved with standard naming convention
- [ ] Standard Memory Update pattern followed (Step 6)

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-02-12 | Initial release — better-auth with Drizzle/Kysely + D1, social auth, 2FA, passkeys, organizations, RBAC |
