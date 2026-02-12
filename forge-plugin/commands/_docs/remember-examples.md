# /remember Examples

## Example 1: Store Architectural Decision

```
/remember "Using PostgreSQL instead of MongoDB for primary database" --category decision
```

**What happens**:
1. Prompts for additional context:
   - "What alternatives were considered?"
   - "Why was PostgreSQL chosen?"
   - "What are the trade-offs?"
2. Stores decision in `../../memory/commands/{project}/decisions.md`:
   ```
   ## 2026-02-10: Database Selection
   **Decision**: Use PostgreSQL instead of MongoDB
   **Alternatives**: MongoDB, MySQL
   **Rationale**: Need ACID transactions and complex joins for reporting
   **Trade-offs**: Less flexible schema, but better data integrity
   ```
3. Updates memory index with new entry

## Example 2: Record Coding Pattern

```
/remember --category pattern
```

**What happens** (interactive):
1. Asks: "What problem does this pattern solve?"
   - User: "Handling async errors in Angular components"
2. Asks: "When should this pattern be used?"
   - User: "Any component with HTTP calls"
3. Asks: "What are the key implementation details?"
   - User: "Use catchError with throwError, show toast notification"
4. Stores pattern in `../../memory/commands/{project}/patterns.md`:
   ```
   ## Async Error Handling (Angular)
   **Problem**: Consistent error handling for HTTP calls
   **Use Case**: All components making API requests
   **Implementation**: 
   - Use RxJS catchError operator
   - Log to console and show user-friendly message
   - Return throwError to allow component-level handling
   ```

## Example 3: Document Convention

```
/remember "All API endpoints use kebab-case for URLs" --category convention
```

**What happens**:
1. Prompts: "Where does this apply?"
   - User: "All REST API routes"
2. Prompts: "Are there exceptions?"
   - User: "None - applies to all new endpoints"
3. Stores in `../../memory/commands/{project}/conventions.md`:
   ```
   ### URL Naming
   - **Convention**: Use kebab-case for all API endpoint URLs
   - **Example**: `/api/user-profile`, `/api/order-history`
   - **Scope**: All REST routes
   - **Exceptions**: None
   ```

## Example 4: Capture Lesson Learned

```
/remember "Avoid N+1 queries in user dashboard" --category lesson
```

**What happens**:
1. Prompts: "What was the challenge?"
   - User: "Dashboard was slow, loading 1000+ separate user queries"
2. Prompts: "How was it resolved?"
   - User: "Used select_related and prefetch_related in Django ORM"
3. Prompts: "What should be preferred in the future?"
   - User: "Always use eager loading for list views with relationships"
4. Stores in `../../memory/commands/{project}/lessons_learned.md`:
   ```
   ## 2026-02-10: Query Optimization
   **Challenge**: N+1 queries causing slow dashboard load
   **Solution**: Applied select_related() for foreign keys, prefetch_related() for many-to-many
   **Performance**: Reduced queries from 1000+ to 5, load time from 3s to 200ms
   **Takeaway**: Always analyze query patterns for list views, use eager loading
   ```

## Example 5: Skill-Specific Memory

```
/remember "This project uses Conventional Commits with Angular style" --scope skill --category convention
```

**What happens**:
1. Identifies current skill context (e.g., commit-helper)
2. Stores in `../../memory/skills/commit-helper/{project}/notes.md`:
   ```
   ## Commit Convention
   - Style: Conventional Commits (Angular)
   - Required format: `type(scope): description`
   - Types: feat, fix, docs, style, refactor, test, chore
   - Breaking changes: Use BREAKING CHANGE: in footer
   ```
3. Future invocations of commit-helper skill will reference this

## Example 6: Multi-line Decision Record

```
/remember --category decision
```

**What happens** (interactive for complex decision):
1. User provides full decision record through prompts
2. Stores comprehensive ADR-style entry:
   ```
   ## 2026-02-10: Microservices Communication Pattern
   **Decision**: Use asynchronous message queues (RabbitMQ) for service-to-service communication
   **Context**: 
   - 5 microservices need to communicate
   - Some operations can be eventual consistency
   - Need to handle service failures gracefully
   **Alternatives Considered**:
   1. Synchronous REST calls - rejected due to coupling and cascade failures
   2. Event bus (Kafka) - overkill for current scale
   3. RabbitMQ - chosen for reliability and team familiarity
   **Consequences**:
   - Pros: Decoupling, retry logic, better resilience
   - Cons: Eventual consistency, debugging complexity
   - Trade-offs: Complexity for reliability
   ```
