# Clerk Auth - Usage Examples

This document provides practical examples of how to use the `clerk-auth` skill in various scenarios.

---

## Example 1: Setting Up Clerk Auth in a Next.js App Router Project

**Scenario**: A new Next.js 15 App Router project needs Clerk authentication with sign-in, sign-up, and protected dashboard routes.

**Command**:
```
skill:clerk-auth

Set up Clerk authentication in my Next.js 15 App Router project. I need sign-in and sign-up pages, and all /dashboard routes should be protected. Marketing pages (/, /about, /pricing) should be public.
```

**What Happens**:
1. Skill detects Next.js 15 App Router from `next.config.ts` and `app/` directory
2. Loads memory — no existing memory found, creates new project directory
3. Loads security domain context for authentication and session management patterns
4. Installs `@clerk/nextjs` and configures environment variables
5. Wraps root layout with `<ClerkProvider>`:
   ```tsx
   // app/layout.tsx
   import { ClerkProvider } from '@clerk/nextjs'

   export default function RootLayout({ children }: { children: React.ReactNode }) {
     return (
       <ClerkProvider>
         <html lang="en">
           <body>{children}</body>
         </html>
       </ClerkProvider>
     )
   }
   ```
6. Creates `middleware.ts` in project root with route protection:
   ```ts
   // middleware.ts
   import { clerkMiddleware, createRouteMatcher } from '@clerk/nextjs/server'

   const isPublicRoute = createRouteMatcher([
     '/',
     '/about',
     '/pricing',
     '/sign-in(.*)',
     '/sign-up(.*)',
   ])

   export default clerkMiddleware(async (auth, request) => {
     if (!isPublicRoute(request)) {
       await auth.protect()
     }
   })

   export const config = {
     matcher: [
       '/((?!_next|[^?]*\\.(?:html?|css|js(?!on)|jpe?g|webp|png|gif|svg|ttf|woff2?|ico|csv|docx?|xlsx?|zip|webmanifest)).*)',
       '/(api|trpc)(.*)',
     ],
   }
   ```
7. Creates sign-in and sign-up pages:
   ```tsx
   // app/sign-in/[[...sign-in]]/page.tsx
   import { SignIn } from '@clerk/nextjs'
   export default function SignInPage() {
     return <SignIn />
   }
   ```
8. Saves output to `/claudedocs/clerk-auth_myapp_2026-02-12.md`
9. Creates memory with project overview and auth patterns

**Expected Output**:
```markdown
# Clerk Auth Implementation: MyApp
**Date**: 2026-02-12

## SDK Configuration
- Package: @clerk/nextjs v5.x
- Next.js: 15.x (App Router)
- Provider: <ClerkProvider> in app/layout.tsx

## Route Protection
- Public: /, /about, /pricing, /sign-in, /sign-up
- Protected: /dashboard/*, all other routes
- Middleware: clerkMiddleware() with createRouteMatcher()

## Files Created/Modified
- middleware.ts — clerkMiddleware() with route matchers
- app/layout.tsx — ClerkProvider wrapper
- app/sign-in/[[...sign-in]]/page.tsx — Sign-in page
- app/sign-up/[[...sign-up]]/page.tsx — Sign-up page
- .env.local — Clerk environment variables

## Environment Variables
- NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY — Client-side publishable key
- CLERK_SECRET_KEY — Server-side secret key
- NEXT_PUBLIC_CLERK_SIGN_IN_URL=/sign-in
- NEXT_PUBLIC_CLERK_SIGN_UP_URL=/sign-up
```

---

## Example 2: Configuring clerkMiddleware() with Route Protection and API Keys

**Scenario**: An existing Next.js project with Clerk needs advanced middleware configuration with protected API routes and API Keys beta for M2M authentication.

**Command**:
```
skill:clerk-auth

Configure clerkMiddleware() with these requirements:
1. Public routes: /, /api/health, /api/webhooks/clerk
2. Protected routes: /dashboard/*, /api/users/*, /api/projects/*
3. Enable API Keys beta for /api/external/* routes (M2M auth)
4. Admin-only routes: /admin/*
```

**What Happens**:
1. Skill detects existing Clerk setup from `@clerk/nextjs` in `package.json`
2. Loads memory — finds existing project with basic Clerk auth configured
3. Loads security context for API authentication and M2M patterns
4. Updates `middleware.ts` with advanced route matching:
   ```ts
   // middleware.ts
   import { clerkMiddleware, createRouteMatcher } from '@clerk/nextjs/server'

   const isPublicRoute = createRouteMatcher([
     '/',
     '/api/health',
     '/api/webhooks/clerk',
     '/sign-in(.*)',
     '/sign-up(.*)',
   ])

   const isAdminRoute = createRouteMatcher(['/admin(.*)'])

   export default clerkMiddleware(async (auth, request) => {
     if (isAdminRoute(request)) {
       await auth.protect((has) => {
         return has({ role: 'org:admin' })
       })
     }

     if (!isPublicRoute(request)) {
       await auth.protect()
     }
   })

   export const config = {
     matcher: [
       '/((?!_next|[^?]*\\.(?:html?|css|js(?!on)|jpe?g|webp|png|gif|svg|ttf|woff2?|ico|csv|docx?|xlsx?|zip|webmanifest)).*)',
       '/(api|trpc)(.*)',
     ],
   }
   ```
5. Configures API Keys beta for M2M endpoints:
   ```ts
   // app/api/external/[...route]/route.ts
   import { auth } from '@clerk/nextjs/server'

   export async function GET(request: Request) {
     const { userId, sessionClaims } = await auth()
     if (!userId) {
       return new Response('Unauthorized', { status: 401 })
     }
     // Handle M2M API key authenticated requests
   }
   ```
6. Saves output and updates memory with advanced middleware patterns

**Expected Output**:
```markdown
# Clerk Auth - Advanced Middleware: MyApp
**Date**: 2026-02-12

## Route Protection Matrix
| Route Pattern       | Access Level      | Auth Method        |
|---------------------|-------------------|--------------------|
| /                   | Public            | None               |
| /api/health         | Public            | None               |
| /api/webhooks/clerk | Public            | Svix verification  |
| /dashboard/*        | Authenticated     | clerkMiddleware()  |
| /api/users/*        | Authenticated     | clerkMiddleware()  |
| /api/projects/*     | Authenticated     | clerkMiddleware()  |
| /api/external/*     | M2M / API Key     | API Keys beta      |
| /admin/*            | Admin role only   | Role-based protect |

## API Keys Beta
- Enabled via CLERK_API_KEYS_BETA=true
- M2M routes: /api/external/*
- API key verification via Clerk SDK

## Files Modified
- middleware.ts — Advanced route matchers with role-based protection
- app/api/external/[...route]/route.ts — API Keys beta handler
- .env.local — Added CLERK_API_KEYS_BETA=true
```

---

## Example 3: Setting Up Clerk Webhooks with svix Verification

**Scenario**: A Next.js project needs to sync Clerk user events to a local PostgreSQL database. Webhook handlers must verify signatures using svix.

**Command**:
```
skill:clerk-auth

Set up Clerk webhooks to sync user data to my PostgreSQL database. I need to handle user.created, user.updated, and user.deleted events. Use svix for signature verification.
```

**What Happens**:
1. Skill detects Next.js App Router project with existing Clerk auth
2. Loads memory — finds existing project with Clerk middleware configured
3. Loads security context for webhook security and signature verification patterns
4. Installs `svix` package for webhook signature verification
5. Creates webhook API route:
   ```ts
   // app/api/webhooks/clerk/route.ts
   import { Webhook } from 'svix'
   import { headers } from 'next/headers'
   import { WebhookEvent } from '@clerk/nextjs/server'

   export async function POST(req: Request) {
     const WEBHOOK_SECRET = process.env.CLERK_WEBHOOK_SECRET
     if (!WEBHOOK_SECRET) {
       throw new Error('Missing CLERK_WEBHOOK_SECRET environment variable')
     }

     const headerPayload = await headers()
     const svixId = headerPayload.get('svix-id')
     const svixTimestamp = headerPayload.get('svix-timestamp')
     const svixSignature = headerPayload.get('svix-signature')

     if (!svixId || !svixTimestamp || !svixSignature) {
       return new Response('Missing svix headers', { status: 400 })
     }

     const payload = await req.json()
     const body = JSON.stringify(payload)

     const wh = new Webhook(WEBHOOK_SECRET)
     let event: WebhookEvent

     try {
       event = wh.verify(body, {
         'svix-id': svixId,
         'svix-timestamp': svixTimestamp,
         'svix-signature': svixSignature,
       }) as WebhookEvent
     } catch (err) {
       console.error('Webhook signature verification failed:', err)
       return new Response('Invalid signature', { status: 400 })
     }

     switch (event.type) {
       case 'user.created':
         await handleUserCreated(event.data)
         break
       case 'user.updated':
         await handleUserUpdated(event.data)
         break
       case 'user.deleted':
         await handleUserDeleted(event.data)
         break
       default:
         console.log(`Unhandled webhook event: ${event.type}`)
     }

     return new Response('Webhook processed', { status: 200 })
   }

   async function handleUserCreated(data: any) {
     // Insert user into PostgreSQL database
   }

   async function handleUserUpdated(data: any) {
     // Update user in PostgreSQL database
   }

   async function handleUserDeleted(data: any) {
     // Delete or soft-delete user from PostgreSQL database
   }
   ```
6. Ensures webhook route is listed as public in `clerkMiddleware()`:
   ```ts
   const isPublicRoute = createRouteMatcher([
     '/',
     '/sign-in(.*)',
     '/sign-up(.*)',
     '/api/webhooks/clerk',  // Webhook endpoint must be public
   ])
   ```
7. Saves output with Clerk Dashboard webhook configuration checklist
8. Updates memory with webhook patterns and svix verification flow

**Expected Output**:
```markdown
# Clerk Auth - Webhooks: MyApp
**Date**: 2026-02-12

## Webhook Configuration
- Endpoint: /api/webhooks/clerk
- Verification: svix signature verification
- Secret: CLERK_WEBHOOK_SECRET environment variable

## Events Handled
| Event            | Action                          |
|------------------|---------------------------------|
| user.created     | Insert user into PostgreSQL     |
| user.updated     | Update user profile in database |
| user.deleted     | Soft-delete user from database  |

## Clerk Dashboard Setup Checklist
- [ ] Navigate to Clerk Dashboard → Webhooks
- [ ] Add endpoint: https://yourdomain.com/api/webhooks/clerk
- [ ] Select events: user.created, user.updated, user.deleted
- [ ] Copy signing secret to CLERK_WEBHOOK_SECRET env var
- [ ] Test with Clerk's "Send test event" button

## Files Created/Modified
- app/api/webhooks/clerk/route.ts — Webhook handler with svix verification
- middleware.ts — Added /api/webhooks/clerk to public routes
- .env.local — Added CLERK_WEBHOOK_SECRET

## Security Notes
- Raw body used for signature verification (not parsed JSON)
- svix headers validated before processing
- Failed verification returns 400 (not 401) per svix convention
- Webhook secret never exposed to client-side code
```

---

## Common Usage Patterns

### Pattern 1: Basic Clerk Setup
```
skill:clerk-auth
Set up Clerk auth in my Next.js App Router project with sign-in and sign-up pages
```
Use for new projects needing basic Clerk authentication.

### Pattern 2: Middleware + Webhooks
```
skill:clerk-auth
Configure clerkMiddleware() with protected routes and add webhook handlers for user sync
```
Use when you need route protection and database synchronization.

### Pattern 3: API Keys for M2M
```
skill:clerk-auth
Enable Clerk API Keys beta for machine-to-machine authentication on my API routes
```
Use for projects with external API consumers that need programmatic access.

### Pattern 4: Next.js 16 Migration
```
skill:clerk-auth
Migrate my Clerk auth setup to Next.js 16 with proxy.ts configuration
```
Use when upgrading to Next.js 16 and needing proxy.ts for Clerk.

### Pattern 5: API Version Migration
```
skill:clerk-auth
Migrate my Clerk integration to API version 2025-11-10
```
Use when updating to the latest Clerk API version with breaking changes.

---

## Tips for Effective Usage

1. **Have Clerk keys ready** — obtain `NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY` and `CLERK_SECRET_KEY` from Clerk Dashboard before running the skill
2. **Place middleware correctly** — `middleware.ts` must be in the project root, not inside `app/` or `src/`
3. **Use `auth()` for lightweight checks** — only call `currentUser()` when you need the full user object
4. **Mark webhook routes as public** — webhook endpoints must bypass `clerkMiddleware()` auth checks
5. **Test webhooks locally** — use Clerk CLI or ngrok to test webhook delivery during development
6. **Specify your Next.js version** — mention your version to get the right middleware and proxy.ts configuration

---

## When to Use This Skill

**Ideal Scenarios**:
- Next.js projects using Clerk for authentication
- Projects needing clerkMiddleware() route protection
- Webhook-driven user synchronization with external databases
- M2M authentication via API Keys beta
- Next.js 16 proxy.ts configuration for Clerk
- Migrating to Clerk API version 2025-11-10

**Not Ideal For**:
- Self-hosted authentication (use `better-auth` skill)
- Non-Next.js frameworks (Clerk supports others, but this skill focuses on Next.js)
- Azure AD / Entra ID authentication (use `azure-auth` skill)
- Simple API key authentication without Clerk (overkill for this use case)
