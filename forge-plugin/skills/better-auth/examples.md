# Better Auth - Usage Examples

This document provides practical examples of how to use the `better-auth` skill in various scenarios.

---

## Example 1: Setting Up better-auth with Drizzle ORM and Cloudflare D1

**Scenario**: A new Cloudflare Workers project needs self-hosted authentication with Cloudflare D1 as the database. The project already uses Drizzle ORM for database access.

**Command**:
```
skill:better-auth

Set up better-auth in my Cloudflare Workers project. I'm using Drizzle ORM with D1. I need email/password authentication with session management.
```

**What Happens**:
1. Skill detects a Cloudflare Workers project from `wrangler.toml` and Drizzle ORM from `drizzle.config.ts`
2. Loads memory — no existing memory found, creates new project directory
3. Loads security domain context for authentication and session management patterns
4. Defines auth schema tables in Drizzle (`user`, `session`, `account`, `verification`)
5. Configures better-auth server instance:
   - Sets `database` to use the Drizzle adapter with D1 binding
   - Configures `baseURL` and `secret` from environment variables
   - Sets `trustedOrigins` for allowed client origins
6. Mounts auth handler at `/api/auth/*` in the Workers request handler
7. Generates D1 migration SQL via `drizzle-kit generate`
8. Creates client-side auth helper using `createAuthClient`
9. Saves output to `/claudedocs/better-auth_myapp_2026-02-12.md`
10. Creates memory with project overview and auth patterns

**Expected Output**:
```markdown
# Better Auth Implementation: MyApp
**Date**: 2026-02-12

## Database Configuration
- Adapter: Drizzle ORM with D1
- Tables: user, session, account, verification
- Migration: 0001_auth_tables.sql applied

## Auth Server Configuration
- Handler mounted at /api/auth/*
- Session strategy: cookie-based
- Email/password authentication enabled

## Files Created/Modified
- src/db/schema/auth.ts — Drizzle auth schema
- src/auth.ts — better-auth server instance
- src/worker.ts — Auth handler mounted
- drizzle/0001_auth_tables.sql — D1 migration
- wrangler.toml — D1 binding added

## Environment Variables
- AUTH_SECRET — Session signing secret
- AUTH_BASE_URL — Public URL of the Workers API
```

---

## Example 2: Adding Social Authentication (GitHub, Google) with better-auth

**Scenario**: An existing Cloudflare Workers project with better-auth needs social login via GitHub and Google OAuth providers. The base auth setup is already in place.

**Command**:
```
skill:better-auth

Add GitHub and Google social login to my existing better-auth setup. My GitHub OAuth app client ID is "gh-client-123" and Google OAuth client ID is "google-client-456".
```

**What Happens**:
1. Skill detects existing better-auth setup from `src/auth.ts`
2. Loads memory — finds existing project with email/password auth configured
3. Loads security context for OAuth 2.0 and social authentication patterns
4. Adds `socialProviders` configuration to the existing better-auth instance:
   - **GitHub**: configures `clientId` and `clientSecret` from environment variables
   - **Google**: configures `clientId` and `clientSecret` from environment variables
   - Sets callback URLs: `/api/auth/callback/github`, `/api/auth/callback/google`
5. Updates Drizzle schema to ensure `account` table supports OAuth provider data
6. Generates updated migration if schema changes are needed
7. Creates client-side social login buttons with `authClient.signIn.social()`
8. Saves output to `/claudedocs/better-auth_myapp_2026-02-12.md`
9. Updates memory with social provider configuration patterns

**Expected Output**:
```markdown
# Better Auth - Social Providers: MyApp
**Date**: 2026-02-12

## Social Providers Configured
- GitHub OAuth — callback: /api/auth/callback/github
- Google OAuth — callback: /api/auth/callback/google

## OAuth App Registration Checklist
### GitHub
- [x] Client ID configured
- [x] Client Secret in environment variables
- [ ] Callback URL registered: https://myapp.com/api/auth/callback/github

### Google
- [x] Client ID configured
- [x] Client Secret in environment variables
- [ ] Callback URL registered: https://myapp.com/api/auth/callback/google
- [ ] OAuth consent screen configured

## Files Modified
- src/auth.ts — Added socialProviders configuration
- wrangler.toml — Added GITHUB_CLIENT_ID, GITHUB_CLIENT_SECRET, GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET

## Client-Side Integration
- authClient.signIn.social({ provider: "github" })
- authClient.signIn.social({ provider: "google" })

## Environment Variables (New)
- GITHUB_CLIENT_ID
- GITHUB_CLIENT_SECRET
- GOOGLE_CLIENT_ID
- GOOGLE_CLIENT_SECRET
```

---

## Example 3: Implementing Organizations with RBAC Using better-auth Plugins

**Scenario**: A SaaS application needs multi-tenant organizations where users can create organizations, invite members, and assign roles with granular permissions.

**Command**:
```
skill:better-auth

Add organizations with RBAC to my better-auth setup. I need roles: owner, admin, and member. Owners can manage billing, admins can manage members, and members have read-only access. Users should be able to create organizations and invite others via email.
```

**What Happens**:
1. Skill detects existing better-auth setup with Drizzle ORM and D1
2. Loads memory — finds existing project with email/password and social auth configured
3. Loads security context for authorization, RBAC, and multi-tenancy patterns
4. Enables `organization` plugin in better-auth configuration:
   - Defines roles: `owner`, `admin`, `member`
   - Configures permissions per role:
     - `owner`: `["org:manage", "billing:manage", "member:manage", "member:invite", "content:read", "content:write"]`
     - `admin`: `["member:manage", "member:invite", "content:read", "content:write"]`
     - `member`: `["content:read"]`
   - Sets up organization creation defaults
5. Updates Drizzle schema with organization tables:
   - `organization` — org name, slug, metadata
   - `member` — user-to-org mapping with role
   - `invitation` — pending invitations with expiration
6. Generates migration for new organization tables
7. Creates API middleware for permission checking:
   - `requireRole("admin")` — route-level role guard
   - `requirePermission("billing:manage")` — granular permission check
8. Implements invitation flow:
   - Generate invitation link with expiration
   - Accept invitation → add user to organization with role
9. Creates client-side organization management helpers
10. Saves output to `/claudedocs/better-auth_myapp_2026-02-12.md`
11. Updates memory with organization and RBAC patterns

**Expected Output**:
```markdown
# Better Auth - Organizations & RBAC: MyApp
**Date**: 2026-02-12

## Organization Plugin Configuration
- Roles: owner, admin, member
- Default role on join: member
- Invitation expiration: 7 days

## Permissions Matrix
| Permission        | Owner | Admin | Member |
|-------------------|-------|-------|--------|
| org:manage        | ✅    | ❌    | ❌     |
| billing:manage    | ✅    | ❌    | ❌     |
| member:manage     | ✅    | ✅    | ❌     |
| member:invite     | ✅    | ✅    | ❌     |
| content:read      | ✅    | ✅    | ✅     |
| content:write     | ✅    | ✅    | ❌     |

## Database Tables Added
- organization — org name, slug, logo, metadata, created_at
- member — user_id, organization_id, role, joined_at
- invitation — email, organization_id, role, token, expires_at, status

## Files Created/Modified
- src/auth.ts — Added organization plugin with roles and permissions
- src/db/schema/auth.ts — Added organization, member, invitation tables
- src/middleware/rbac.ts — Role and permission guard middleware
- drizzle/0002_organizations.sql — D1 migration

## API Endpoints (via better-auth)
- POST /api/auth/organization/create — Create new organization
- POST /api/auth/organization/invite — Invite member by email
- POST /api/auth/organization/accept-invitation — Accept invitation
- GET /api/auth/organization/list — List user's organizations
- PATCH /api/auth/organization/update-member-role — Change member role
- DELETE /api/auth/organization/remove-member — Remove member
```

---

## Common Usage Patterns

### Pattern 1: Email/Password Only
```
skill:better-auth
Set up basic email/password auth with better-auth and Drizzle ORM on D1
```
Use for simple projects that only need credential-based authentication.

### Pattern 2: Social Auth + 2FA
```
skill:better-auth
Set up better-auth with GitHub/Google social login and TOTP two-factor authentication
```
Use when you need social login with an additional security layer.

### Pattern 3: Full SaaS Auth Stack
```
skill:better-auth
Set up better-auth with social login, organizations, RBAC, passkeys, and 2FA for my SaaS app
```
Use for multi-tenant SaaS applications requiring comprehensive auth.

### Pattern 4: Kysely Instead of Drizzle
```
skill:better-auth
Set up better-auth using Kysely as the database adapter for Cloudflare D1
```
Use when the project uses Kysely instead of Drizzle ORM.

---

## Tips for Effective Usage

1. **Choose your ORM first** — better-auth requires Drizzle ORM or Kysely for D1 (no direct adapter)
2. **Have OAuth app registrations ready** — create GitHub/Google OAuth apps before configuring social providers
3. **Set AUTH_SECRET securely** — use `wrangler secret put AUTH_SECRET` for production, never commit to code
4. **Plan your roles early** — organization RBAC roles and permissions are easier to define upfront
5. **Run migrations** — always apply Drizzle migrations to D1 after schema changes
6. **Specify existing setup** — mention if auth is already partially configured to avoid duplicating work

---

## When to Use This Skill

**Ideal Scenarios**:
- Self-hosted auth for TypeScript / Cloudflare Workers projects
- Cloudflare D1 as the authentication database
- Social login with GitHub, Google, Discord, or other OAuth providers
- Multi-tenant SaaS with organizations and role-based access control
- Adding 2FA/TOTP or passkey/WebAuthn support
- Projects using Drizzle ORM or Kysely

**Not Ideal For**:
- Third-party auth services (Auth0, Clerk, Firebase Auth — use those directly)
- Non-TypeScript backends (use language-specific auth libraries)
- Databases without Drizzle/Kysely support (use better-auth's other adapters)
- Simple API key authentication (overkill for this use case)
