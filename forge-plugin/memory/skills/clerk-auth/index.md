# Clerk Auth - Memory System

This file documents the memory structure for the `clerk-auth` skill. Memory is project-specific knowledge that accumulates over time through repeated Clerk authentication implementations.

---

## Purpose

The memory system enables the skill to:
- **Learn project patterns** — understand project-specific Clerk configurations, middleware rules, and webhook handlers
- **Avoid repeat work** — reuse established clerkMiddleware() configurations and webhook patterns
- **Track decisions** — record why specific route matchers, API versions, or webhook events were chosen
- **Prevent errors** — remember project-specific public routes, webhook secrets, and API key scoping
- **Improve accuracy** — better recommendations based on project history

---

## Memory vs Context

**Memory** (this directory):
- Project-specific
- Dynamic (changes with each implementation)
- Per-project subdirectories
- Example: "This project uses clerkMiddleware() with 3 public routes and handles user.created webhooks"

**Context** (`../../context/security/`):
- Universal security and authentication knowledge
- Static (changes rarely)
- Shared across all projects
- Example: "Webhook signature verification best practices and OAuth 2.0 patterns"

---

## Memory Structure

```
memory/skills/clerk-auth/
├── index.md (this file)
└── {project-name}/
    ├── project_overview.md        # CRITICAL — Clerk config, SDK version, middleware setup
    └── common_patterns.md         # Project-specific auth patterns and conventions
```

---

## Per-Project Memory Files

### 1. project_overview.md (CRITICAL)

**Purpose**: High-level understanding of the project's Clerk authentication setup.

**Always Update On First Run**:
- `@clerk/nextjs` SDK version (v4 or v5)
- Next.js version (13/14/15/16) and router type (App Router or Pages Router)
- Clerk API version (e.g., `2025-11-10`)
- `clerkMiddleware()` configuration (public routes, protected routes, role-based routes)
- Webhook endpoint and events handled
- API Keys beta status (enabled/disabled)
- proxy.ts configuration (if Next.js 16)
- Sign-in and sign-up page routes
- Environment variables configured

**Update Incrementally**:
- Add new webhook events as they are handled
- Record new protected or public routes
- Document API version migrations
- Note middleware configuration changes
- Track environment-specific configuration (dev, staging, production)

**Example Structure**:
```markdown
# Project Overview: MySaaSApp

## Clerk Configuration
- **SDK**: @clerk/nextjs v5.x
- **API Version**: 2025-11-10
- **Publishable Key**: pk_live_... (in NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY)
- **Sign-in URL**: /sign-in
- **Sign-up URL**: /sign-up

## Next.js Setup
- **Version**: Next.js 15.x
- **Router**: App Router
- **Middleware**: middleware.ts in project root

## Route Protection
- **Public**: /, /about, /pricing, /sign-in, /sign-up, /api/webhooks/clerk
- **Protected**: /dashboard/*, /api/users/*, /api/projects/*
- **Admin-only**: /admin/* (role: org:admin)

## Webhooks
- **Endpoint**: /api/webhooks/clerk
- **Events**: user.created, user.updated, user.deleted
- **Verification**: svix with CLERK_WEBHOOK_SECRET
- **Database Sync**: PostgreSQL via Prisma

## API Keys Beta
- **Status**: Enabled
- **M2M Routes**: /api/external/*

## Environment Variables
- NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY
- CLERK_SECRET_KEY
- CLERK_WEBHOOK_SECRET
- CLERK_API_KEYS_BETA=true
```

### 2. common_patterns.md

**Purpose**: Document recurring Clerk auth patterns specific to this project.

**What to Document**:
- clerkMiddleware() configuration patterns
- Route matcher patterns and conventions
- Webhook handler implementation patterns
- `auth()` and `currentUser()` usage patterns
- API key verification patterns
- Error handling approaches
- Client-side component integration patterns
- Testing and development workflow patterns

**Example**:
```markdown
# Common Patterns: MySaaSApp

## Middleware Pattern
clerkMiddleware() with createRouteMatcher():
1. Public routes defined via createRouteMatcher()
2. Admin routes checked with role-based protect()
3. All other routes require authentication via auth.protect()

## Auth in Server Components
All server components use this pattern:
1. Call auth() to get session and userId
2. If no userId → redirect to /sign-in
3. If userId needed with full profile → call currentUser()
4. For API routes → use auth() for lightweight session check

## Webhook Processing
1. Verify svix signature before processing
2. Switch on event.type for routing
3. Idempotent handlers — safe to replay
4. Return 200 quickly; queue heavy work

## Client-Side Auth
- <SignIn /> and <SignUp /> components for auth pages
- <UserButton /> in navbar for user menu
- useAuth() hook for client-side auth state
- useUser() hook for user profile data

## Environment Management
- Dev: .env.local with Clerk test keys
- Staging: Vercel environment variables
- Production: Vercel environment variables with live keys
- CLERK_WEBHOOK_SECRET: separate per environment
```

---

## Workflow

### First Use on a Project

1. **Check for existing memory**: Does `{project-name}/` directory exist?
2. **If NO**: Create memory directory and both files
3. **If YES**: Load existing memory files

### Subsequent Uses

1. **Load all existing memory files** (Step 2 of skill workflow)
2. **Use memory to inform implementation** (understand existing Clerk setup)
3. **After implementation**: Update ALL memory files with new insights

---

## Memory Update Guidelines

### project_overview.md Updates
- **First run**: Create comprehensive overview of Clerk configuration
- **Subsequent runs**: Add new routes, webhook events, or configuration changes
- **Update when**: New public/protected routes added, webhook events handled, API version migrated, API Keys beta enabled

### common_patterns.md Updates
- **Add patterns** observed or implemented in this session
- **Don't remove patterns** unless they are no longer applicable
- **Refine patterns** as the Clerk setup evolves
- **Document workarounds** for version-specific or framework-specific issues

---

## Benefits of Memory System

1. **Consistency**
   - Same middleware patterns applied across the project
   - Webhook handlers follow established conventions

2. **Speed**
   - Subsequent auth changes are faster (context already loaded)
   - Known route matchers and webhook events readily available

3. **Error Prevention**
   - Public routes stored — prevents auth loop on webhooks and marketing pages
   - Webhook secrets documented — prevents signature verification failures

4. **Traceability**
   - Auth decisions recorded with rationale
   - API version migrations tracked over time

---

## Memory File Size

**Keep memory files concise**:
- project_overview.md: ~100-300 lines
- common_patterns.md: ~200-400 lines

**If memory grows too large**:
- Consolidate similar patterns
- Archive outdated route configurations
- Summarize historical changes

---

## Related Documentation

- **Skill Workflow**: `../../skills/clerk-auth/SKILL.md`
- **Context System**: `../../context/security/index.md`
- **Main Memory Index**: `../index.md`

---

**Version**: 1.0.0
**Last Updated**: 2026-02-12
