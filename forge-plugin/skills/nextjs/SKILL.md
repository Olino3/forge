---
name: nextjs
version: "1.0.0"
description: "Build Next.js 16 apps with App Router, Server Components/Actions, Cache Components (\"use cache\"), and async route params. Includes proxy.ts and React 19.2. Prevents 25 errors."
context:
  primary_domain: "engineering"
  always_load_files: []
  detection_required: true
  file_budget: 6
memory:
  scopes:
    - type: "skill-specific"
      files: [project_overview.md, common_patterns.md]
    - type: "shared-project"
      usage: "reference"
tags: [nextjs, next16, react, server-components, server-actions, app-router, cache-components, rsc, typescript]
---

# skill:nextjs - Next.js 16 Expert

## Version: 1.0.0

## Purpose

Build production-grade Next.js 16 applications using App Router, React Server Components, Server Actions, Cache Components (`"use cache"`), and async route params. This skill covers the full Next.js 16 development lifecycle including routing, data fetching, caching, authentication (proxy.ts), middleware, and deployment. Use when building new Next.js apps, migrating from Pages Router, upgrading to Next.js 16, or implementing complex data fetching patterns.

## File Structure

```
skills/nextjs/
├── SKILL.md (this file)
└── examples.md
```

## Interface References

- **Context**: Loaded via [ContextProvider Interface](../../interfaces/context_provider.md)
- **Memory**: Accessed via [MemoryStore Interface](../../interfaces/memory_store.md)
- **Shared Patterns**: [Shared Loading Patterns](../../interfaces/shared_loading_patterns.md)
- **Schemas**: Validated against [context_metadata.schema.json](../../interfaces/schemas/context_metadata.schema.json) and [memory_entry.schema.json](../../interfaces/schemas/memory_entry.schema.json)

## Next.js 16 Focus Areas

1. **App Router**: File-based routing with layouts, loading states, error boundaries, and parallel routes
2. **Server Components**: Default rendering model — no client JS unless `"use client"` is declared
3. **Server Actions**: Mutations via `"use server"` functions — form handling, data writes, revalidation
4. **Cache Components**: `"use cache"` directive for granular caching at component and function level
5. **Async Route Params**: `params` and `searchParams` are now Promises — must be awaited
6. **proxy.ts**: Auth proxy pattern for secure API route handling (replaces middleware-based auth)
7. **React 19.2**: `use()` hook, `<Suspense>` boundaries, `useActionState`, `useOptimistic`
8. **Metadata API**: Static and dynamic metadata generation for SEO
9. **Streaming**: Progressive rendering with Suspense boundaries for improved TTFB

## Common Errors Prevented

1. Using `"use client"` unnecessarily — defaulting to Server Components reduces bundle size
2. Accessing `params` synchronously (Next.js 16 requires `await params`)
3. Importing client-only code in Server Components (window, localStorage, hooks)
4. Using `fetch()` in Server Actions instead of direct database access
5. Missing `revalidatePath()` or `revalidateTag()` after mutations
6. Incorrect `"use cache"` placement (must be top of file or top of function)
7. Passing non-serializable props from Server to Client Components
8. Missing `loading.tsx` for routes with async data fetching
9. Using `router.push()` for mutations instead of Server Actions
10. Incorrect `generateStaticParams()` return type
11. Missing `error.tsx` boundary causing full-page crashes
12. Cookie/header access in cached components (breaks caching)
13. Circular dependencies between Server and Client Components
14. Missing `Suspense` boundary around `use()` hook calls
15. `redirect()` called inside try/catch blocks (throws NEXT_REDIRECT error)
16. Using `useSearchParams()` without `<Suspense>` boundary (blocks static rendering)
17. Middleware matching too broadly (applying to static assets)
18. Missing `proxy.ts` for third-party auth providers in production
19. Stale closures in Server Actions capturing outdated state
20. Setting `dynamic = "force-static"` on routes that read cookies/headers
21. Using `Date.now()` in Server Components causing hydration mismatch
22. Forgetting `export const runtime = "edge"` for edge-deployed routes
23. Nesting `<form action={serverAction}>` inside client-side form libraries
24. Missing `key` prop when rendering dynamic route segments
25. Using `next/image` without configured `remotePatterns` in next.config

---

## MANDATORY WORKFLOW (MUST FOLLOW EXACTLY)

### Step 1: Initial Analysis

**YOU MUST:**
1. Detect the Next.js version and router type (App Router vs. Pages Router)
2. Identify the scope:
   - New Next.js 16 application setup
   - Feature implementation (routing, data fetching, forms, auth)
   - Migration from Pages Router or older Next.js
   - Performance optimization or caching strategy
3. Check `next.config.js`/`next.config.ts` for configuration
4. Identify deployment target (Vercel, self-hosted, Docker, Cloudflare)
5. Ask clarifying questions if ambiguous

### Step 2: Load Memory

> Follow [Standard Memory Loading](../../interfaces/shared_loading_patterns.md#pattern-1-standard-memory-loading) with `skill="nextjs"` and `domain="engineering"`.

**YOU MUST:**
1. Use `memoryStore.getSkillMemory("nextjs", "{project-name}")` to load project patterns
2. Use `memoryStore.getByProject("{project-name}")` for cross-skill context
3. Review previously documented route structure, caching strategy, and auth patterns

### Step 3: Load Context

> Follow [Standard Context Loading](../../interfaces/shared_loading_patterns.md#pattern-2-standard-context-loading) for the `engineering` domain. Stay within the file budget declared in frontmatter.

### Step 4: Implement Next.js Patterns

**YOU MUST follow these rules:**

**Server Components (Default):**
- All components are Server Components unless marked `"use client"`
- Can directly access databases, file systems, and environment variables
- Cannot use hooks (`useState`, `useEffect`), event handlers, or browser APIs
- Props passed to Client Components must be serializable (no functions, classes, or Dates)

**Client Components:**
- Only add `"use client"` when you need interactivity, hooks, or browser APIs
- Push `"use client"` boundary as deep as possible in the component tree
- Prefer composition: pass Server Component as `children` to Client Component

**Server Actions:**
```typescript
"use server"
// Must be async, can only be called from client-side or form actions
export async function createItem(formData: FormData) {
  // Direct database/API access
  // Always revalidate after mutation
  revalidatePath("/items")
}
```

**Cache Components (Next.js 16):**
```typescript
"use cache"
// Caches the component/function output
// Cannot access cookies, headers, or other dynamic APIs
export default async function ProductList() {
  const products = await db.query("SELECT * FROM products")
  return <ul>{products.map(p => <li key={p.id}>{p.name}</li>)}</ul>
}
```

**Async Route Params (Next.js 16):**
```typescript
// params is now a Promise - must await
export default async function Page({
  params,
}: {
  params: Promise<{ slug: string }>
}) {
  const { slug } = await params
  // ...
}
```

**DO NOT use `"use client"` unless strictly necessary**

### Step 5: Generate Output

- Save to `/claudedocs/nextjs_{project}_{YYYY-MM-DD}.md`
- Follow naming conventions in `../OUTPUT_CONVENTIONS.md`
- Include file paths, code changes, and configuration updates

### Step 6: Update Memory

> Follow [Standard Memory Update](../../interfaces/shared_loading_patterns.md#pattern-3-standard-memory-update) for `skill="nextjs"`.

Store route structure, caching strategy, auth patterns, deployment config, and component boundaries.

---

## Compliance Checklist

Before completing, verify:

- [ ] Step 1: Next.js version, router type, and scope identified
- [ ] Step 2: Standard Memory Loading pattern followed
- [ ] Step 3: Standard Context Loading pattern followed
- [ ] Step 4: Next.js patterns correctly applied (Server/Client boundaries, caching, async params)
- [ ] Step 5: Output saved with standard naming convention
- [ ] Step 6: Standard Memory Update pattern followed

## Further Reading

- **Next.js 16 Docs**: https://nextjs.org/docs
- **React Server Components**: https://react.dev/reference/rsc/server-components
- **Server Actions**: https://nextjs.org/docs/app/building-your-application/data-fetching/server-actions-and-mutations
- **Caching in Next.js**: https://nextjs.org/docs/app/building-your-application/caching

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-02-12 | Initial release with interface-based architecture |
