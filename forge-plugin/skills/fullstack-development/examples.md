# Full-Stack Development Examples

This file contains example scenarios demonstrating how to use the fullstack-development skill to provide architectural oversight and design guidance across all application layers.

---

## Example 1: Designing a SaaS Dashboard

### Scenario
A team is building a SaaS analytics dashboard with React on the frontend, Node.js/Express on the backend, and PostgreSQL for data storage. They need architectural guidance for the initial project setup.

### User Prompt
```
Help me architect a SaaS dashboard application using React, Node.js, and PostgreSQL
```

### Skill Execution

**Step 1 - Analyze Project Stack**:
- **Frontend**: React 18, TypeScript, Vite, TanStack Query, Zustand (state), React Router v6
- **Backend**: Node.js 20, Express 4, TypeScript, Prisma ORM
- **Database**: PostgreSQL 16, Redis (session cache)
- **Infrastructure**: Docker Compose (local), AWS ECS (production), GitHub Actions CI/CD

**Step 2 - Evaluate Architecture**:
- **Pattern**: Modular monolith — single Express server with domain-separated modules
- **Issues identified**:
  - No API versioning strategy defined
  - Authentication flow not yet designed
  - No shared type definitions between frontend and backend
- **Scalability**: Read-heavy dashboard workload suits connection pooling + Redis cache
- **Security**: Needs JWT-based auth with refresh tokens, role-based access control

**Step 3 - Load Project Memory**:
```
memoryStore.getSkillMemory("fullstack-development", "saas-dashboard")
→ No prior memory found. First-time analysis.
```

**Step 4 - Design & Implement**:

**API Contract**:
```typescript
// Shared types (packages/shared/types.ts)
interface DashboardWidget {
  id: string;
  type: 'chart' | 'table' | 'metric';
  title: string;
  dataSource: string;
  config: WidgetConfig;
}

// GET /api/v1/dashboards/:id
interface DashboardResponse {
  id: string;
  name: string;
  widgets: DashboardWidget[];
  createdAt: string;
  updatedAt: string;
}

// Error format (consistent across all endpoints)
interface ApiError {
  code: string;
  message: string;
  details?: Record<string, string[]>;
}
```

**Data Flow**:
```
User interaction → React component → TanStack Query →
  GET /api/v1/dashboards/:id → Express route → Auth middleware →
    Controller → Service layer → Prisma ORM → PostgreSQL
      ↓ (cache miss path)
    Redis cache ← Service layer → Response serialization →
  JSON response → TanStack Query cache → React re-render
```

**Architecture Decisions**:
- Monorepo with shared types package for end-to-end type safety
- API versioned via URL prefix (`/api/v1/`)
- Prisma for type-safe database access with generated types
- TanStack Query for server state; Zustand for client-only UI state
- Row-level security in PostgreSQL for multi-tenant data isolation

**Step 5 - Review & Output**:
- ✅ All layers addressed: frontend, backend, database, infrastructure
- ✅ Shared type system eliminates contract drift
- ✅ Multi-tenancy handled at database level
- ✅ Caching strategy defined for read-heavy workload
- ✅ Output written to `/claudedocs/fullstack_saas_dashboard.md`
- ✅ Memory updated with stack inventory and architecture decisions

---

## Example 2: E-Commerce Platform Architecture

### Scenario
A startup is building an e-commerce platform using Next.js for the storefront, Python/FastAPI for the backend services, and MongoDB for product catalog storage. They need guidance on cross-layer integration and API design.

### User Prompt
```
Design the architecture for an e-commerce platform with Next.js frontend, FastAPI backend, and MongoDB
```

### Skill Execution

**Step 1 - Analyze Project Stack**:
- **Frontend**: Next.js 14 (App Router), TypeScript, Tailwind CSS, SWR for data fetching
- **Backend**: Python 3.12, FastAPI, Pydantic v2, Motor (async MongoDB driver)
- **Database**: MongoDB 7 (product catalog), PostgreSQL 16 (orders/users), Redis (sessions + cart)
- **Infrastructure**: Vercel (frontend), AWS ECS (backend), MongoDB Atlas, CloudFront CDN

**Step 2 - Evaluate Architecture**:
- **Pattern**: Backend-for-frontend with service separation — Next.js server components call FastAPI services
- **Issues identified**:
  - Two databases (MongoDB + PostgreSQL) require careful transaction management for orders that reference products
  - Type safety gap between TypeScript frontend and Python backend
  - Need clear strategy for image/asset management
- **Scalability**: Product catalog reads are high-frequency; orders are write-heavy with consistency requirements
- **Security**: Payment processing requires PCI compliance considerations; input sanitization on both layers

**Step 3 - Load Project Memory**:
```
memoryStore.getSkillMemory("fullstack-development", "ecommerce-platform")
→ No prior memory found. First-time analysis.
```

**Step 4 - Design & Implement**:

**API Contract** (OpenAPI-first design):
```yaml
# Products API (MongoDB-backed)
/api/v1/products:
  get:
    parameters:
      - name: category
        in: query
        schema: { type: string }
      - name: page
        in: query
        schema: { type: integer, default: 1 }
    responses:
      200:
        content:
          application/json:
            schema:
              type: object
              properties:
                items: { type: array, items: { $ref: '#/components/schemas/Product' } }
                pagination: { $ref: '#/components/schemas/Pagination' }

# Orders API (PostgreSQL-backed)
/api/v1/orders:
  post:
    requestBody:
      content:
        application/json:
          schema: { $ref: '#/components/schemas/CreateOrder' }
    responses:
      201:
        content:
          application/json:
            schema: { $ref: '#/components/schemas/Order' }
```

**Cross-Layer Data Flow** (checkout process):
```
Next.js storefront → Server Component fetch → FastAPI /api/v1/cart/checkout
  → Validate cart items against MongoDB product catalog (stock check)
  → Create order in PostgreSQL (ACID transaction)
  → Decrement inventory in MongoDB
  → Publish OrderCreated event → Payment service
  → Return order confirmation → Next.js → Client hydration
```

**Architecture Decisions**:
- OpenAPI spec as single source of truth; generate TypeScript client and Pydantic models
- MongoDB for product catalog (flexible schema, fast reads); PostgreSQL for orders/users (ACID)
- Saga pattern for cross-database consistency (order creation + inventory decrement)
- Next.js Server Components for SEO-critical pages; client components for interactive cart
- Redis for cart persistence (survives session) and product cache (5-min TTL)

**Step 5 - Review & Output**:
- ✅ Dual-database strategy justified with clear domain boundaries
- ✅ Cross-database consistency addressed via saga pattern
- ✅ Type safety gap mitigated with OpenAPI code generation
- ✅ SSR strategy aligned with SEO requirements for product pages
- ✅ Output written to `/claudedocs/fullstack_ecommerce_platform.md`
- ✅ Memory updated with stack decisions and integration patterns

---

## Example 3: Real-Time Collaboration Tool Stack Assessment

### Scenario
A team has an existing real-time collaboration tool built with Vue.js, Go backend, Redis for pub/sub, and WebSocket connections. They are experiencing scaling issues and need a full-stack architecture review.

### User Prompt
```
Review the architecture of our real-time collaboration tool — Vue.js frontend, Go backend, Redis pub/sub, WebSocket — we're hitting scaling limits at 10K concurrent users
```

### Skill Execution

**Step 1 - Analyze Project Stack**:
- **Frontend**: Vue.js 3 (Composition API), TypeScript, Pinia (state), native WebSocket client
- **Backend**: Go 1.22, Gin framework, gorilla/websocket, custom Redis pub/sub layer
- **Database**: PostgreSQL 15 (document storage), Redis 7 (pub/sub + presence + cache)
- **Infrastructure**: Kubernetes (GKE), single Go binary per pod, Redis Cluster (3 nodes), Nginx ingress

**Step 2 - Evaluate Architecture**:
- **Pattern**: Monolithic Go server handling both REST API and WebSocket connections
- **Issues identified**:
  - WebSocket connections are memory-intensive; each Go goroutine per connection consumes ~8KB stack
  - Redis pub/sub fan-out is bottlenecked — all messages go through a single channel pattern
  - No connection draining during deployments — users get disconnected on rollout
  - Frontend reconnection logic is naive (fixed 5s retry, no exponential backoff)
  - No message ordering guarantees after reconnection
- **Scalability bottleneck**: At 10K concurrent users, ~80K goroutines active (WebSocket + message handlers), Redis pub/sub latency spikes to 200ms+
- **Security**: WebSocket auth uses initial HTTP upgrade token but no periodic re-validation

**Step 3 - Load Project Memory**:
```
memoryStore.getSkillMemory("fullstack-development", "collab-tool")
→ Previous analysis found (2025-11-15):
  - Stack: Vue 3 + Go + Redis + PostgreSQL
  - Known issue: Redis pub/sub scaling at 5K users (partially addressed with Redis Cluster)
  - Previous recommendation: Evaluate NATS for pub/sub (not yet implemented)
```

**Step 4 - Design & Implement**:

**WebSocket Architecture Redesign**:
```
Current (bottleneck):
  Client → WebSocket → Go server → Redis PUBLISH → Go server → WebSocket → Client
                        (single channel per document)

Proposed:
  Client → WebSocket → Go server → NATS JetStream → Go server → WebSocket → Client
                        (partitioned by document-id, ordered streams)
```

**Scaling Improvements**:
```go
// Connection pooling with bounded goroutines
type ConnectionPool struct {
    maxConns    int
    workerPool  chan struct{}  // semaphore pattern
    connections sync.Map
}

// Message batching to reduce Redis/NATS round-trips
type MessageBatcher struct {
    buffer    []Message
    flushInterval time.Duration  // 50ms batch window
    maxBatch  int               // 100 messages per flush
}
```

**Frontend Reconnection Strategy**:
```typescript
// Exponential backoff with jitter
const reconnect = (attempt: number) => {
  const baseDelay = Math.min(1000 * Math.pow(2, attempt), 30000)
  const jitter = baseDelay * 0.5 * Math.random()
  const delay = baseDelay + jitter

  // Request missed messages since last known sequence
  ws.onopen = () => {
    ws.send(JSON.stringify({
      type: 'sync',
      lastSeq: lastMessageSequence,
      documentId: currentDocumentId
    }))
  }

  setTimeout(() => connectWebSocket(), delay)
}
```

**Architecture Decisions**:
- Replace Redis pub/sub with NATS JetStream for ordered, persistent message streams
- Implement connection draining: Kubernetes preStop hook sends "reconnect" frame, then 30s grace period
- Add message sequence numbers for gap detection and replay after reconnection
- Partition WebSocket connections across pods using consistent hashing on document ID
- Frontend: exponential backoff with jitter, automatic gap detection and sync
- Monitor with Prometheus metrics: active connections, message latency p99, reconnection rate

**Step 5 - Review & Output**:
- ✅ Scaling bottleneck identified: Redis pub/sub fan-out + goroutine memory pressure
- ✅ NATS JetStream solves ordering and persistence requirements
- ✅ Graceful deployment strategy prevents user disconnections
- ✅ Frontend reconnection hardened with backoff and gap detection
- ✅ Historical context from memory informed recommendations (NATS was previously suggested)
- ✅ Output written to `/claudedocs/fullstack_collab_tool_review.md`
- ✅ Memory updated with new findings and scaling thresholds

---

## Summary of Full-Stack Patterns

1. **SaaS Dashboard** — Monorepo with shared types, read-heavy caching, multi-tenant isolation
2. **E-Commerce Platform** — Dual-database strategy, saga pattern, OpenAPI contract-first, SSR for SEO
3. **Real-Time Collaboration** — WebSocket scaling, message ordering, graceful deployments, connection management

## Best Practices

- Always define shared types or contracts between frontend and backend layers
- Choose database technology based on access patterns, not familiarity
- Design API versioning strategy before the first endpoint ships
- Plan for graceful degradation: what happens when each layer fails?
- Use infrastructure as code from day one — never configure servers manually
- Monitor cross-layer metrics: end-to-end latency, error rates by layer, data consistency
- Document architecture decisions with rationale and trade-offs — future you will thank present you
