# Better Auth - Memory System

This file documents the memory structure for the `better-auth` skill. Memory is project-specific knowledge that accumulates over time through repeated authentication implementations.

---

## Purpose

The memory system enables the skill to:
- **Learn project patterns** — understand project-specific auth configurations and plugin choices
- **Avoid repeat work** — reuse established Drizzle/Kysely schemas and better-auth configurations
- **Track decisions** — record why specific adapters, plugins, or roles were chosen
- **Prevent errors** — remember project-specific D1 bindings, OAuth credentials, and RBAC structures
- **Improve accuracy** — better recommendations based on project history

---

## Memory vs Context

**Memory** (this directory):
- Project-specific
- Dynamic (changes with each implementation)
- Per-project subdirectories
- Example: "This project uses Drizzle ORM with D1, has GitHub and Google social login, and 3 organization roles"

**Context** (`../../context/security/`):
- Universal security and authentication knowledge
- Static (changes rarely)
- Shared across all projects
- Example: "OAuth 2.0 best practices and session management patterns"

---

## Memory Structure

```
memory/skills/better-auth/
├── index.md (this file)
└── {project-name}/
    ├── project_overview.md        # CRITICAL — auth config, adapter, plugins, D1 binding
    └── common_patterns.md         # Project-specific auth patterns and conventions
```

---

## Per-Project Memory Files

### 1. project_overview.md (CRITICAL)

**Purpose**: High-level understanding of the project's authentication setup.

**Always Update On First Run**:
- Database adapter (Drizzle ORM or Kysely)
- D1 database binding name
- better-auth version
- Enabled plugins (social auth, 2FA, passkeys, organizations, etc.)
- Social providers configured (GitHub, Google, Discord, etc.)
- Organization roles and permissions (if RBAC enabled)
- Frontend framework (React, Svelte, Vue, etc.)
- Backend platform (Cloudflare Workers, Pages Functions)
- Auth handler mount path (e.g., `/api/auth/*`)
- Session strategy (cookie-based, token-based)

**Update Incrementally**:
- Add new social providers as they are configured
- Record new organization roles or permission changes
- Document additional plugins enabled over time
- Note migration history and schema changes
- Track environment-specific configuration (dev, staging, production)

**Example Structure**:
```markdown
# Project Overview: MySaaSApp

## better-auth Configuration
- **Version**: 1.x
- **Base URL**: https://mysaasapp.com
- **Auth Handler**: /api/auth/*
- **Session Strategy**: Cookie-based

## Database
- **Adapter**: Drizzle ORM
- **Database**: Cloudflare D1
- **D1 Binding**: DB
- **Schema Tables**: user, session, account, verification, organization, member, invitation

## Social Providers
- GitHub — callback: /api/auth/callback/github
- Google — callback: /api/auth/callback/google

## Plugins Enabled
- socialProviders (GitHub, Google)
- twoFactor (TOTP, 6-digit, 30s period)
- organization (roles: owner, admin, member)

## Frontend Stack
- **Framework**: React 19 with Vite
- **Auth Client**: @better-auth/client

## Backend Stack
- **Platform**: Cloudflare Workers
- **ORM**: Drizzle ORM with d1 driver
- **Migrations**: drizzle-kit generate + wrangler d1 migrations apply
```

### 2. common_patterns.md

**Purpose**: Document recurring auth patterns specific to this project.

**What to Document**:
- Drizzle/Kysely schema patterns for auth tables
- better-auth plugin configuration patterns
- Social provider setup conventions
- Organization and RBAC patterns
- Session handling and middleware patterns
- Migration workflow for D1
- Client-side auth integration patterns
- Error handling approaches

**Example**:
```markdown
# Common Patterns: MySaaSApp

## Database Adapter
Drizzle ORM with D1 driver:
1. Schema defined in src/db/schema/auth.ts
2. Migrations generated via drizzle-kit generate
3. Applied via wrangler d1 migrations apply DB

## Auth Middleware
All protected routes use this pattern:
1. Extract session from request via auth.api.getSession()
2. If no session → return 401
3. If session valid → attach user and session to request context
4. For org routes → check membership and role via organization plugin

## Social Auth Flow
- OAuth redirect initiated via authClient.signIn.social({ provider })
- Callback handled by better-auth at /api/auth/callback/{provider}
- Account linked to existing user if email matches

## Organization Access Pattern
- User creates org → automatically assigned "owner" role
- Owner invites members → invitation email with accept link
- Role checked via requirePermission() middleware before route handler
- Active organization stored in session context

## Environment Variables
- AUTH_SECRET — via wrangler secret put (never in wrangler.toml)
- AUTH_BASE_URL — in wrangler.toml [vars]
- GITHUB_CLIENT_ID / GITHUB_CLIENT_SECRET — via wrangler secret put
- GOOGLE_CLIENT_ID / GOOGLE_CLIENT_SECRET — via wrangler secret put
```

---

## Workflow

### First Use on a Project

1. **Check for existing memory**: Does `{project-name}/` directory exist?
2. **If NO**: Create memory directory and both files
3. **If YES**: Load existing memory files

### Subsequent Uses

1. **Load all existing memory files** (Step 2 of skill workflow)
2. **Use memory to inform implementation** (understand existing auth setup)
3. **After implementation**: Update ALL memory files with new insights

---

## Memory Update Guidelines

### project_overview.md Updates
- **First run**: Create comprehensive overview of better-auth configuration
- **Subsequent runs**: Add new plugins, providers, or schema changes
- **Update when**: New social providers added, plugins enabled, roles changed, migrations applied

### common_patterns.md Updates
- **Add patterns** observed or implemented in this session
- **Don't remove patterns** unless they are no longer applicable
- **Refine patterns** as the auth setup evolves
- **Document workarounds** for D1-specific or adapter-specific issues

---

## Benefits of Memory System

1. **Consistency**
   - Same auth patterns applied across the project
   - Plugin configurations maintained coherently

2. **Speed**
   - Subsequent auth changes are faster (context already loaded)
   - Known D1 binding names and schema structures readily available

3. **Error Prevention**
   - OAuth callback URLs stored — prevents mismatch errors
   - RBAC roles and permissions documented — prevents access control gaps

4. **Traceability**
   - Auth decisions recorded with rationale
   - Plugin and schema changes tracked over time

---

## Memory File Size

**Keep memory files concise**:
- project_overview.md: ~100-300 lines
- common_patterns.md: ~200-400 lines

**If memory grows too large**:
- Consolidate similar patterns
- Archive outdated plugin configurations
- Summarize historical changes

---

## Related Documentation

- **Skill Workflow**: `../../skills/better-auth/SKILL.md`
- **Context System**: `../../context/security/index.md`
- **Main Memory Index**: `../index.md`

---

**Version**: 1.0.0
**Last Updated**: 2026-02-12
