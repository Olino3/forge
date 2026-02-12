# nextjs Memory

Project-specific memory for Next.js application architecture and patterns.

## Purpose

This memory helps `skill:nextjs` remember:
- Next.js version and router type (App Router / Pages Router)
- Route structure and data fetching patterns
- Server/Client Component boundaries
- Caching strategy and revalidation patterns
- Authentication approach and middleware configuration
- Deployment target and edge runtime usage

## Memory Files Per Project

Each project gets its own directory: `{project-name}/`

### Required Files

#### `project_overview.md`
- Next.js version and React version
- Router type (App Router, Pages Router, or hybrid)
- Deployment target (Vercel, self-hosted, Docker, Cloudflare)
- Database and ORM (Prisma, Drizzle, direct SQL)
- Authentication provider and pattern (proxy.ts, middleware)
- CSS approach (Tailwind, CSS Modules, styled-components)

#### `common_patterns.md`
- Server vs. Client Component conventions
- Data fetching patterns (Server Components, Server Actions, Route Handlers)
- Caching strategy (`"use cache"`, `revalidateTag`, `revalidatePath`)
- Error boundary and loading state patterns
- Route organization and naming conventions

### Optional Files

#### `known_issues.md`
- Known hydration mismatches and workarounds
- Performance bottlenecks and planned optimizations
- Third-party library compatibility issues

#### `route_map.md`
- Application route structure and page hierarchy
- Dynamic routes and generateStaticParams configuration
- Middleware route matching patterns

## Related Documentation

- **Skill**: `../../skills/nextjs/SKILL.md`
- **Memory System**: `../index.md`
