# Feature Forge Examples

This file contains example scenarios demonstrating how to use the feature-forge skill to orchestrate complete feature development workflows across different types of applications.

---

## Example 1: User Authentication Feature (Full-Stack)

### Scenario
A team needs to add email/password authentication with JWT tokens to a Node.js/React application that currently has no auth system.

### User Prompt
```
I need to implement user authentication for our app. Users should be able to register, login, and access protected routes. We're using Express on the backend and React on the frontend.
```

### Skill Execution

**Step 1 - Analyze Feature Requirements**:
- **Scope**: Full-stack authentication — registration, login, logout, protected routes
- **Acceptance Criteria**:
  - Users can register with email and password
  - Passwords are hashed and never stored in plain text
  - Login returns a JWT token with configurable expiration
  - Protected API routes reject requests without valid tokens
  - Frontend stores tokens securely and redirects unauthenticated users
- **Dependencies**: bcrypt for hashing, jsonwebtoken for JWT, existing User model
- **Edge Cases**: Duplicate email registration, expired tokens, concurrent sessions, SQL injection

**Step 2 - Plan Implementation Architecture**:
- **Components**: AuthController, AuthService, AuthMiddleware, UserModel (extend), LoginForm, RegisterForm, AuthContext (React)
- **Patterns**: Repository pattern for user data access, middleware pattern for route protection, context pattern for frontend auth state
- **Data Flow**: Client → AuthController → AuthService → UserRepository → Database; JWT issued on success, validated on subsequent requests
- **API Surface**:
  - `POST /api/auth/register` — create account
  - `POST /api/auth/login` — authenticate and receive token
  - `POST /api/auth/logout` — invalidate session
  - `GET /api/auth/me` — get current user profile

**Step 3 - Load Project Memory**:
- Loaded `feature_patterns.md` — project uses controller/service/repository layering
- Loaded `implementation_conventions.md` — TypeScript strict mode, Zod for validation, Jest for testing
- Applied conventions: all new files use `.ts` extension, validation schemas co-located with routes

**Step 4 - Implement Feature**:
- **Scaffolding**: Created `src/auth/` directory with controller, service, middleware, and route files
- **Core Logic**: Implemented registration with bcrypt hashing, login with JWT generation, middleware for token verification
- **Integration**: Wired routes into Express app, added AuthContext provider in React, created protected route wrapper component
- **Tests**: 14 unit tests (service layer), 8 integration tests (API endpoints), 5 frontend tests (auth flow)
- **Documentation**: Updated API docs with auth endpoints, added authentication section to README

**Step 5 - Review & Output**:
- ✅ All acceptance criteria verified
- ✅ Password hashing confirmed (bcrypt, 12 rounds)
- ✅ JWT expiration configurable via environment variable
- ✅ Protected routes return 401 without valid token
- ✅ Frontend redirects to login page when unauthenticated

### Generated Output
```markdown
# Feature: User Authentication
# Output: /claudedocs/feature_user-auth_2026-02-12.md

## Summary
Implemented full-stack email/password authentication with JWT tokens.

## Files Created (9)
- src/auth/auth.controller.ts
- src/auth/auth.service.ts
- src/auth/auth.middleware.ts
- src/auth/auth.routes.ts
- src/auth/auth.validation.ts
- client/src/contexts/AuthContext.tsx
- client/src/components/LoginForm.tsx
- client/src/components/RegisterForm.tsx
- client/src/components/ProtectedRoute.tsx

## Files Modified (4)
- src/app.ts (added auth routes)
- src/models/user.model.ts (added password field)
- client/src/App.tsx (wrapped with AuthProvider)
- docs/api.md (added auth endpoints)

## Test Coverage
- 27 tests passing (14 unit, 8 integration, 5 frontend)
- Auth service: 95% coverage
- Auth middleware: 100% coverage

## Deployment Notes
- Set JWT_SECRET and JWT_EXPIRATION environment variables
- Run database migration for password column
- Consider rate limiting on auth endpoints (follow-up)
```

---

## Example 2: Search and Filter Capability

### Scenario
An existing e-commerce application needs a search and filter system for its product catalog. The app uses Django REST Framework on the backend and Vue.js on the frontend.

### User Prompt
```
Add search and filtering to our product listing page. Users should be able to search by name, filter by category, price range, and rating, and sort results. We need this to be performant with 50k+ products.
```

### Skill Execution

**Step 1 - Analyze Feature Requirements**:
- **Scope**: Backend search API with filtering, frontend filter UI with live results
- **Acceptance Criteria**:
  - Full-text search on product name and description
  - Filter by category (multi-select), price range (min/max), minimum rating
  - Sort by relevance, price (asc/desc), rating, newest
  - Pagination with configurable page size
  - Response time under 200ms for 50k+ products
- **Dependencies**: Existing Product model, django-filter, database indexes
- **Edge Cases**: Empty search results, invalid price ranges, concurrent filter changes, URL state persistence

**Step 2 - Plan Implementation Architecture**:
- **Components**: ProductSearchView, ProductFilterSet, SearchSerializer, ProductSearchService; Vue: SearchBar, FilterPanel, ProductGrid, useProductSearch composable
- **Patterns**: Filter chain pattern for composable filters, debounce pattern for search input, URL query parameter sync for shareable filter state
- **Data Flow**: User input → debounce (300ms) → API call with query params → Django FilterSet → QuerySet → Paginated JSON response → Vue reactive state → ProductGrid render
- **Performance**: Database indexes on `name`, `category_id`, `price`, `rating`; trigram index for full-text search

**Step 3 - Load Project Memory**:
- Loaded `feature_patterns.md` — project uses ViewSet pattern with serializers, Vue Composition API
- Loaded `implementation_conventions.md` — pytest for testing, OpenAPI schema auto-generation enabled
- No prior search patterns found — this will establish the pattern for future search features

**Step 4 - Implement Feature**:
- **Scaffolding**: Created `products/search/` module, Vue `composables/useProductSearch.ts` and filter components
- **Core Logic**: Implemented `ProductFilterSet` with `django-filter`, added `SearchFilter` with trigram similarity, built composable with debounced API calls
- **Integration**: Added `/api/products/search/` endpoint, connected FilterPanel to URL query params, integrated ProductGrid with loading states
- **Tests**: 11 unit tests (filter combinations), 6 integration tests (API with test data), 4 frontend tests (filter interaction), 1 performance test (50k products < 200ms)
- **Documentation**: Added search endpoint to API docs, documented filter parameters

**Step 5 - Review & Output**:
- ✅ Full-text search working on name and description
- ✅ All filter types functional (category, price range, rating)
- ✅ Sort by relevance, price, rating, and date confirmed
- ✅ Pagination with configurable page size
- ✅ Performance: 50k products query completes in ~85ms with indexes

### Generated Output
```markdown
# Feature: Product Search & Filter
# Output: /claudedocs/feature_search-filter_2026-02-12.md

## Summary
Implemented full-text search with composable filters for the product catalog.

## Files Created (8)
- products/search/views.py
- products/search/filters.py
- products/search/serializers.py
- products/migrations/0018_add_search_indexes.py
- frontend/src/composables/useProductSearch.ts
- frontend/src/components/SearchBar.vue
- frontend/src/components/FilterPanel.vue
- frontend/src/components/PriceRangeSlider.vue

## Files Modified (3)
- products/urls.py (added search endpoint)
- frontend/src/views/ProductList.vue (integrated search and filters)
- docs/api.md (added search endpoint documentation)

## Test Coverage
- 22 tests passing (11 unit, 6 integration, 4 frontend, 1 perf)
- Filter logic: 92% coverage
- Search composable: 88% coverage

## Deployment Notes
- Run migration 0018 to create trigram and composite indexes
- Index creation on 50k+ rows may take 30-60 seconds (non-blocking)
- Consider Elasticsearch integration for future full-text needs (follow-up)
```

---

## Example 3: Real-Time Notification System

### Scenario
A SaaS project management application needs a notification system that delivers real-time updates when tasks are assigned, comments are posted, or deadlines approach. The app uses FastAPI, PostgreSQL, and React with TypeScript.

### User Prompt
```
Build a notification system for our project management app. Users need to get real-time notifications when they're assigned tasks, someone comments on their work, or a deadline is approaching. We want both in-app notifications and optional email digests.
```

### Skill Execution

**Step 1 - Analyze Feature Requirements**:
- **Scope**: Backend notification service with WebSocket delivery, in-app notification center, email digest system
- **Acceptance Criteria**:
  - Real-time in-app notifications via WebSocket connection
  - Notification types: task assignment, comment mention, deadline reminder (24h, 1h)
  - Persistent notification storage with read/unread status
  - Notification center UI with badge count, mark as read, and bulk actions
  - Optional email digest (daily/weekly) with user preference control
  - Notifications respect user preference settings (mute per project, per type)
- **Dependencies**: WebSocket support (FastAPI native), Celery for async tasks, existing Task and Comment models, SMTP service for email
- **Edge Cases**: User offline when notification fires, WebSocket reconnection, notification deduplication, timezone handling for deadline reminders, high-volume notification bursts

**Step 2 - Plan Implementation Architecture**:
- **Components**:
  - Backend: NotificationService, NotificationRepository, WebSocketManager, EmailDigestWorker, DeadlineScheduler
  - Frontend: NotificationCenter, NotificationBell, NotificationItem, useNotifications hook, useWebSocket hook
  - Database: `notifications` table, `notification_preferences` table
- **Patterns**: Observer pattern for event-driven notification creation, strategy pattern for delivery channels (WebSocket, email), pub/sub for real-time distribution
- **Data Flow**:
  1. Domain event (task assigned) → NotificationService.create()
  2. Persist to database → Dispatch to WebSocketManager
  3. WebSocketManager → Push to connected client(s)
  4. If offline → queued for next connection or email digest
  5. DeadlineScheduler (Celery beat) → periodic scan → create reminder notifications
- **API Surface**:
  - `GET /api/notifications` — list notifications (paginated, filterable)
  - `PATCH /api/notifications/{id}/read` — mark as read
  - `POST /api/notifications/read-all` — mark all as read
  - `GET /api/notifications/preferences` — get notification preferences
  - `PUT /api/notifications/preferences` — update preferences
  - `WS /ws/notifications` — real-time WebSocket connection

**Step 3 - Load Project Memory**:
- Loaded `feature_patterns.md` — project uses event-driven patterns with domain events, SQLAlchemy ORM
- Loaded `implementation_conventions.md` — Pydantic v2 for schemas, pytest-asyncio for async tests, Storybook for component development
- Loaded `delivery_checklist.md` — requires load testing for real-time features, feature flag for gradual rollout
- Applied: WebSocket implementation follows existing event-driven patterns, Pydantic models for all notification schemas

**Step 4 - Implement Feature**:
- **Scaffolding**: Created `src/notifications/` package with models, schemas, service, repository, router, and websocket modules; React `features/notifications/` directory
- **Core Logic**:
  - NotificationService with create/read/bulk-read operations
  - WebSocketManager with connection tracking and targeted delivery
  - DeadlineScheduler Celery task scanning for approaching deadlines
  - EmailDigestWorker aggregating unread notifications into HTML digest
- **Integration**:
  - Domain event hooks in TaskService and CommentService to trigger notifications
  - WebSocket endpoint with JWT authentication
  - NotificationCenter component with real-time updates via useWebSocket hook
  - User preferences panel integrated into account settings
- **Tests**:
  - 18 unit tests (notification service, preference logic, digest aggregation)
  - 10 integration tests (API endpoints, WebSocket connection, event-to-notification flow)
  - 6 frontend tests (notification center, bell badge, mark as read)
  - 2 load tests (100 concurrent WebSocket connections, burst of 1000 notifications)
- **Documentation**: Added notification API docs, WebSocket protocol documentation, email template README

**Step 5 - Review & Output**:
- ✅ Real-time notifications delivered within 50ms via WebSocket
- ✅ All three notification types functional (assignment, comment, deadline)
- ✅ Read/unread status persists across sessions
- ✅ Email digest sends daily/weekly based on user preference
- ✅ Notification preferences respected per project and per type
- ✅ Load test: 100 concurrent WebSocket connections sustained with <100ms latency

### Generated Output
```markdown
# Feature: Real-Time Notification System
# Output: /claudedocs/feature_notification-system_2026-02-12.md

## Summary
Implemented real-time notification system with WebSocket delivery,
persistent storage, user preferences, and optional email digests.

## Files Created (16)
- src/notifications/models.py
- src/notifications/schemas.py
- src/notifications/service.py
- src/notifications/repository.py
- src/notifications/router.py
- src/notifications/websocket.py
- src/notifications/events.py
- src/notifications/workers/deadline_scheduler.py
- src/notifications/workers/email_digest.py
- src/notifications/templates/digest_email.html
- migrations/versions/0042_add_notifications.py
- frontend/src/features/notifications/NotificationCenter.tsx
- frontend/src/features/notifications/NotificationBell.tsx
- frontend/src/features/notifications/NotificationItem.tsx
- frontend/src/features/notifications/hooks/useNotifications.ts
- frontend/src/features/notifications/hooks/useWebSocket.ts

## Files Modified (5)
- src/tasks/service.py (added notification event on assignment)
- src/comments/service.py (added notification event on mention)
- src/celery_config.py (registered deadline and digest workers)
- frontend/src/components/AppHeader.tsx (added NotificationBell)
- frontend/src/pages/AccountSettings.tsx (added preferences panel)

## Test Coverage
- 36 tests passing (18 unit, 10 integration, 6 frontend, 2 load)
- Notification service: 94% coverage
- WebSocket manager: 91% coverage
- Frontend components: 85% coverage

## Deployment Notes
- Run migration 0042 for notifications and preferences tables
- Configure SMTP credentials for email digest functionality
- Set CELERY_BEAT_SCHEDULE for deadline scanner (runs every 15 min)
- Feature flag `NOTIFICATIONS_ENABLED` controls rollout
- Monitor WebSocket connection count in production dashboard
- Consider Redis pub/sub for multi-instance WebSocket scaling (follow-up)
```

---

## Summary of Feature Types

1. **Full-stack authentication** — Cross-cutting security feature spanning backend services, middleware, and frontend state management
2. **Search and filter** — Data access feature requiring performance optimization, composable query patterns, and responsive UI
3. **Real-time notifications** — Event-driven feature with WebSocket communication, background workers, and user preference management

## Best Practices

- Always start with clear acceptance criteria before writing any code
- Plan architecture before implementation — identify components, patterns, and data flow
- Load project memory to maintain consistency with existing conventions
- Implement incrementally: scaffolding → core logic → integration → tests → documentation
- Validate every acceptance criterion before declaring the feature complete
- Update project memory with patterns and conventions discovered during implementation
- Include deployment notes and follow-up items in the output summary
- Keep features behind feature flags for gradual rollout when possible
- Write tests at every layer — unit, integration, and end-to-end
- Document API surfaces with request/response examples
