---
name: graphql-design
description: "Design GraphQL schemas with proper type hierarchies, resolver patterns, and federation strategies. Covers schema-first design, query complexity analysis, N+1 prevention with DataLoader, pagination (Relay connections), error handling, and authorization patterns. Prevents common pitfalls including over-fetching at the resolver level, missing input validation, and unbounded queries."
version: "1.0.0"
context:
  primary_domain: "engineering"
  always_load_files: []
  detection_required: false
  file_budget: 4
memory:
  scopes:
    - type: "skill-specific"
      files: [project_overview.md, schema_conventions.md]
    - type: "shared-project"
      usage: "reference"
tags: [graphql, schema, resolvers, federation, api, relay, dataloader, subscriptions]
---

# skill:graphql-design — GraphQL Schema Design, Resolvers, and Federation

## Version: 1.0.0

## Purpose

Design production-grade GraphQL APIs with well-structured schemas, efficient resolvers, and scalable federation strategies. This skill guides the design of type systems, query structures, mutation patterns, and subscription models — producing schema definitions, resolver architecture maps, and performance optimization recommendations.

Use when:
- Designing a new GraphQL API from scratch
- Migrating from REST to GraphQL
- Implementing schema federation across multiple services
- Optimizing an existing GraphQL API for performance
- Establishing GraphQL design standards for an organization
- Adding real-time features with GraphQL subscriptions

## File Structure

```
skills/graphql-design/
├── SKILL.md (this file)
└── examples.md
```

## Interface References

- **Context**: Loaded via [ContextProvider Interface](../../interfaces/context_provider.md)
- **Memory**: Accessed via [MemoryStore Interface](../../interfaces/memory_store.md)
- **Shared Patterns**: [Shared Loading Patterns](../../interfaces/shared_loading_patterns.md)
- **Schemas**: Validated against [context_metadata.schema.json](../../interfaces/schemas/context_metadata.schema.json) and [memory_entry.schema.json](../../interfaces/schemas/memory_entry.schema.json)

---

## MANDATORY WORKFLOW (MUST FOLLOW EXACTLY)

> **IMPORTANT**: Execute ALL steps in order. Do not skip any step.

### Step 1: Identify GraphQL API Requirements

**YOU MUST:**
1. Determine the **API scope**:
   - New GraphQL API (greenfield)
   - REST-to-GraphQL migration
   - Schema extension (adding types/fields to existing schema)
   - Federation design (multi-service graph)
2. Identify **consumers**:
   - Web SPA (React, Vue, Angular)
   - Mobile apps (iOS/Android)
   - Server-to-server
   - Third-party developers (public API)
3. Determine **data characteristics**:
   - Entity types and their relationships
   - Read vs. write ratio
   - Real-time requirements (subscriptions needed?)
   - Data volume and query complexity expectations
4. Clarify **constraints**:
   - Existing data sources (databases, REST APIs, microservices)
   - Authentication mechanism
   - Rate limiting and query complexity budget
   - Schema federation requirements

**DO NOT PROCEED WITHOUT A CLEAR SCOPE**

### Step 2: Load Memory

> Follow [Standard Memory Loading](../../interfaces/shared_loading_patterns.md#pattern-1-standard-memory-loading) with `skill="graphql-design"` and `domain="engineering"`.

**YOU MUST:**
1. Use `memoryStore.getSkillMemory("graphql-design", "{project-name}")` to load existing schema conventions
2. Use `memoryStore.getByProject("{project-name}")` for cross-skill insights
3. If memory exists, adopt established naming conventions, pagination patterns, and error handling
4. If no memory exists, proceed and create it in Step 8

### Step 3: Load Context

> Follow [Standard Context Loading](../../interfaces/shared_loading_patterns.md#pattern-2-standard-context-loading) for the `engineering` domain. Stay within the file budget declared in frontmatter.

### Step 4: Design Schema Types

**YOU MUST:**
1. **Define entity types** (schema-first approach):
   ```graphql
   type User {
     id: ID!
     email: String!
     name: String!
     role: UserRole!
     createdAt: DateTime!
     orders(first: Int, after: String): OrderConnection!
   }

   enum UserRole {
     ADMIN
     EDITOR
     VIEWER
   }
   ```
2. **Follow naming conventions**:
   - Types: `PascalCase` (`User`, `OrderItem`)
   - Fields: `camelCase` (`firstName`, `createdAt`)
   - Enums: `SCREAMING_SNAKE_CASE` (`USER_ROLE`, `ORDER_STATUS`)
   - Mutations: verb + noun (`createUser`, `updateOrder`, `cancelSubscription`)
   - Queries: noun for single (`user`), plural or connection for lists (`users`, `ordersConnection`)
3. **Use explicit nullability**:
   - `String!` — non-nullable (guaranteed to be present)
   - `String` — nullable (may be null)
   - Default to non-nullable; use nullable only when null has semantic meaning
4. **Define custom scalars** where needed:
   - `DateTime` — ISO 8601 timestamps
   - `URL` — Validated URL strings
   - `EmailAddress` — Validated email format
   - `JSON` — Arbitrary JSON (use sparingly)

### Step 5: Design Queries, Mutations, and Subscriptions

**YOU MUST:**
1. **Queries** — Read operations:
   ```graphql
   type Query {
     # Single entity by ID
     user(id: ID!): User
     # Connection-based pagination (Relay spec)
     users(first: Int, after: String, filter: UserFilter): UserConnection!
     # Search
     searchUsers(query: String!, first: Int): UserConnection!
   }
   ```
2. **Mutations** — Write operations with input types and payload types:
   ```graphql
   input CreateUserInput {
     email: String!
     name: String!
     role: UserRole = VIEWER
   }

   type CreateUserPayload {
     user: User
     errors: [UserError!]!
   }

   type Mutation {
     createUser(input: CreateUserInput!): CreateUserPayload!
     updateUser(id: ID!, input: UpdateUserInput!): UpdateUserPayload!
     deleteUser(id: ID!): DeleteUserPayload!
   }
   ```
3. **Subscriptions** — Real-time updates:
   ```graphql
   type Subscription {
     orderStatusChanged(orderId: ID!): Order!
     newMessage(channelId: ID!): Message!
   }
   ```
4. **Pagination** — Relay Connection specification:
   ```graphql
   type UserConnection {
     edges: [UserEdge!]!
     pageInfo: PageInfo!
     totalCount: Int!
   }

   type UserEdge {
     cursor: String!
     node: User!
   }

   type PageInfo {
     hasNextPage: Boolean!
     hasPreviousPage: Boolean!
     startCursor: String
     endCursor: String
   }
   ```
5. **Error handling** — Typed errors in mutation payloads:
   ```graphql
   interface UserError {
     message: String!
     path: [String!]
   }

   type ValidationError implements UserError {
     message: String!
     path: [String!]
     field: String!
     constraint: String!
   }

   type AuthorizationError implements UserError {
     message: String!
     path: [String!]
     requiredRole: UserRole!
   }
   ```

### Step 6: Design Resolver Architecture

**YOU MUST address:**
1. **N+1 Prevention** — DataLoader pattern:
   - Batch all database lookups by parent type
   - One DataLoader per entity type per request
   - DataLoader instances are request-scoped (never shared)
2. **Authorization** — Field-level and type-level:
   - Directive-based: `@auth(requires: ADMIN)`
   - Resolver middleware for complex authorization logic
   - Never expose unauthorized data even if the field is requested
3. **Query complexity analysis**:
   - Assign cost to each field (default 1, connections higher)
   - Set maximum query complexity budget (e.g., 1000)
   - Reject queries exceeding the budget before execution
   - Limit query depth (e.g., max 10 levels)
4. **Federation** (if multi-service):
   - Define entity ownership: which service is the source of truth
   - Use `@key` directive for entity references across services
   - Extend types from other services with `extend type`
   - Gateway composes the unified graph

### Step 7: Generate Output

- Save output to `/claudedocs/graphql-design_{project}_{YYYY-MM-DD}.md`
- Follow naming conventions in `../OUTPUT_CONVENTIONS.md`
- Include:
  - Complete SDL (Schema Definition Language) file
  - Type inventory with descriptions
  - Resolver architecture (DataLoader strategy, auth rules)
  - Query complexity budget
  - Example queries and mutations with expected responses
  - Federation entity map (if applicable)

### Step 8: Update Memory

> Follow [Standard Memory Update](../../interfaces/shared_loading_patterns.md#pattern-3-standard-memory-update) for `skill="graphql-design"`.

Store:
1. **schema_conventions.md**: Naming rules, pagination style, error handling pattern, custom scalars
2. **project_overview.md**: Schema scope, entity inventory, federation topology, data sources

---

## GraphQL Design Principles

| Principle | Guideline |
|-----------|-----------|
| **Schema-first** | Design the schema before writing resolvers |
| **Client-driven** | Schema should serve client needs, not mirror database tables |
| **Explicit nullability** | Every field's nullability should be a deliberate decision |
| **Single source of truth** | Each entity type is owned by exactly one service (federation) |
| **Demand-driven** | Only add fields that clients actually need |
| **Evolvable** | Deprecate fields instead of removing them; add new fields freely |

## Common Anti-Patterns to Prevent

| Anti-Pattern | Correct Approach |
|-------------|-----------------|
| CRUD-mapped mutations (`createUser`, `getUser`) | Design around domain operations (`registerUser`, `inviteTeamMember`) |
| Returning raw database errors | Use typed error unions in mutation payloads |
| Unbounded list queries | Always paginate with connections |
| N+1 queries in resolvers | Use DataLoader for batched data fetching |
| Nullable everything | Default to non-nullable; null means "intentionally absent" |
| Generic `JSON` scalar overuse | Define proper types; `JSON` hides schema information |
| No query depth/complexity limits | Set max depth (10) and complexity budget (1000) |

---

## Compliance Checklist

Before completing, verify:

- [ ] Step 1: API scope, consumers, data characteristics, and constraints identified
- [ ] Step 2: Standard Memory Loading pattern followed
- [ ] Step 3: Standard Context Loading pattern followed
- [ ] Step 4: Schema types designed with proper naming, nullability, and custom scalars
- [ ] Step 5: Queries, mutations, subscriptions, pagination, and error handling defined
- [ ] Step 6: Resolver architecture — DataLoader, auth, complexity analysis, federation addressed
- [ ] Step 7: Output saved with standard naming convention
- [ ] Step 8: Standard Memory Update pattern followed

**FAILURE TO COMPLETE ALL STEPS INVALIDATES THE DESIGN**

---

## Further Reading

- **GraphQL Specification**: https://spec.graphql.org/
- **Relay Connection Specification**: https://relay.dev/graphql/connections.htm
- **Apollo Federation**: https://www.apollographql.com/docs/federation/
- **GraphQL Best Practices**: https://graphql.org/learn/best-practices/
- **Production GraphQL** by Marc-André Giroux

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-02-12 | Initial release — schema design, resolvers, federation, pagination, error handling, N+1 prevention |
