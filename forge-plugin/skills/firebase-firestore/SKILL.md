---
name: firebase-firestore
description: Build with Firestore NoSQL database — real-time sync, offline support, and scalable document storage. Use when creating collections, querying documents, setting up security rules, handling real-time updates. Prevents 10 common Firestore errors.
version: "1.0.0"
context:
  primary_domain: "schema"
  always_load_files: []
  detection_required: false
  file_budget: 4
memory:
  scopes:
    - type: "skill-specific"
      files: [collection_structure.md, security_rules.md, query_patterns.md, data_model.md, performance_config.md]
    - type: "shared-project"
      usage: "reference"
---

# Skill: firebase-firestore

**Version**: 1.0.0
**Purpose**: Build with Firestore NoSQL database — real-time sync, offline support, and scalable document storage
**Author**: The Forge
**Last Updated**: 2025-07-14

---

## Title

**Firebase Firestore** - Design, implement, and optimize Firestore NoSQL databases with real-time sync, security rules, and scalable document storage

---

## File Structure

```
forge-plugin/skills/firebase-firestore/
├── SKILL.md                  # This file - mandatory workflow
└── examples.md               # Usage scenarios and examples
```

---

## Required Reading

**Before executing this skill**, load context and memory via interfaces:

1. **Context**: Use `contextProvider.getDomainIndex("schema")` for relevant domain context. See [ContextProvider Interface](../../interfaces/context_provider.md).

2. **Skill memory**: Use `memoryStore.getSkillMemory("firebase-firestore", "{project-name}")` for previous Firestore configurations. See [MemoryStore Interface](../../interfaces/memory_store.md).

## Interface References

- **Context**: Loaded via [ContextProvider Interface](../../interfaces/context_provider.md)
- **Memory**: Accessed via [MemoryStore Interface](../../interfaces/memory_store.md)
- **Shared Patterns**: [Shared Loading Patterns](../../interfaces/shared_loading_patterns.md)
- **Schemas**: Validated against [context_metadata.schema.json](../../interfaces/schemas/context_metadata.schema.json) and [memory_entry.schema.json](../../interfaces/schemas/memory_entry.schema.json)

---

## Design Requirements

### Core Functionality

This skill must:
1. **Design collection and document structures** (hierarchies, subcollections, denormalization)
2. **Build queries** (simple, compound, collection group, pagination, ordering)
3. **Write security rules** (authentication, field-level validation, role-based access)
4. **Implement real-time listeners** (onSnapshot, query listeners, presence)
5. **Configure offline persistence** (cache size, multi-tab, sync strategies)
6. **Handle transactions and batch writes** (atomic operations, distributed counters)
7. **Model data for NoSQL** (embedding vs referencing, fan-out, aggregation)
8. **Optimize performance** (indexing, pagination cursors, query planning)
9. **Store Firestore configuration** in memory for future reference

### Output Requirements

Generate **complete, production-ready Firestore implementations** with:
- Collection and document schema definitions
- Security rules (firestore.rules)
- Query implementations (Web, Admin, Mobile SDKs)
- Real-time listener setup with error handling
- Offline persistence configuration
- Transaction and batch write patterns
- Composite index definitions (firestore.indexes.json)
- Data migration scripts when applicable

### Quality Requirements

Generated implementations must:
- **Follow Firestore best practices** (document size limits, query constraints)
- **Include comprehensive security rules** (never deploy with open rules)
- **Handle edge cases** (offline scenarios, concurrent writes, pagination boundaries)
- **Be SDK-appropriate** (Web v9 modular, Admin SDK, Flutter, iOS, Android)
- **Include error handling** (permission denied, not found, quota exceeded)
- **Be well-documented** (collection schemas, query patterns, rule logic)

---

## 10 Common Firestore Errors Prevented

This skill actively prevents these frequently encountered Firestore mistakes:

### 1. Missing Composite Index
**Error**: `FAILED_PRECONDITION: The query requires an index`
**Prevention**: Generate `firestore.indexes.json` for all compound queries. Always check if a query combines multiple `where()` clauses or mixes `where()` with `orderBy()` on different fields.

### 2. Insecure Security Rules
**Error**: Data breach from `allow read, write: if true;`
**Prevention**: Never generate open rules. Always require authentication and validate data structure. Generate role-based rules with field-level validation.

### 3. Unbounded Queries
**Error**: Reading entire collections, excessive reads, cost explosion
**Prevention**: Always implement pagination with `limit()` and cursor-based pagination using `startAfter()`. Never query without a limit in production.

### 4. Incorrect Data Modeling (SQL Thinking)
**Error**: Over-normalized data requiring excessive JOINs (Firestore has no JOINs)
**Prevention**: Design for query patterns, not normalization. Denormalize strategically. Embed frequently-accessed related data within documents.

### 5. Document Size Limit Exceeded
**Error**: `INVALID_ARGUMENT: maximum document size is 1 MiB`
**Prevention**: Monitor document growth. Use subcollections for unbounded lists. Never store arrays that can grow indefinitely inside a document.

### 6. Hot Spots from Sequential IDs
**Error**: Write throttling from auto-incrementing or timestamp-based document IDs
**Prevention**: Use Firestore auto-generated IDs. Avoid sequential document IDs that cause write hot spots on a single tablet.

### 7. Missing Offline Handling
**Error**: App crashes or hangs when offline, stale data displayed without indication
**Prevention**: Configure persistence settings, handle `fromCache` metadata, implement connectivity state listeners, and design UI for offline states.

### 8. Transaction Contention
**Error**: `ABORTED: Transaction was aborted due to contention`
**Prevention**: Keep transactions small and fast. Avoid transactions on frequently updated documents. Use distributed counters for high-write scenarios.

### 9. Inefficient Real-Time Listeners
**Error**: Excessive reads from poorly scoped listeners, memory leaks from undetached listeners
**Prevention**: Scope listeners to minimal data sets. Always unsubscribe when components unmount. Use query listeners instead of document listeners when possible.

### 10. Missing Error Handling on Writes
**Error**: Silent data loss when writes fail (offline queue overflow, permission denied)
**Prevention**: Always handle write errors. Implement retry logic. Monitor pending writes count. Handle `permission-denied` errors gracefully with user feedback.

---

## Instructions

### MANDATORY STEPS (Must Execute in Order)

---

#### **Step 1: Initial Analysis**

**Purpose**: Understand the Firestore implementation requirements

**Actions**:
1. Identify the application type (web, mobile, server-side)
2. Determine the SDK environment (Web v9 modular, Admin SDK, Flutter, iOS, Android)
3. Review existing Firestore configuration if present (firebase.json, firestore.rules, firestore.indexes.json)
4. Understand the data access patterns and query requirements
5. Identify real-time requirements (which data needs live updates)
6. Note any existing data models or migration needs

**Output**: Clear understanding of Firestore requirements and constraints

---

#### **Step 2: Load Memory**

**Purpose**: Retrieve previous Firestore configurations for this project

> Follow [Standard Memory Loading](../../interfaces/shared_loading_patterns.md#pattern-1-standard-memory-loading) with `skill="firebase-firestore"` and `domain="schema"`.

**Actions**:
1. Use `memoryStore.getSkillMemory("firebase-firestore", "{project-name}")` to load project memory. See [MemoryStore Interface](../../interfaces/memory_store.md).
2. If memory exists, review:
   - `collection_structure.md` - Existing collection hierarchies and document schemas
   - `security_rules.md` - Current security rules and access patterns
   - `query_patterns.md` - Established query patterns and indexes
   - `data_model.md` - Data modeling decisions and trade-offs
   - `performance_config.md` - Performance tuning and optimization settings
3. If not exists, note this is first-time Firestore setup

**Output**: Understanding of project Firestore history or recognition of new project

---

#### **Step 3: Load Context**

**Purpose**: Load relevant NoSQL and Firestore knowledge

> Follow [Standard Context Loading](../../interfaces/shared_loading_patterns.md#pattern-2-standard-context-loading) for the `schema` domain. Stay within the file budget declared in frontmatter.

**Actions**:
1. Use `contextProvider.getDomainIndex("schema")` for database design context
2. Load relevant context files based on requirements:
   - NoSQL data modeling patterns
   - Security best practices
   - Performance optimization guidelines
3. Note any best practices for Firestore implementation

**Output**: Comprehensive understanding of Firestore patterns and best practices

---

#### **Step 4: Firestore Implementation**

**Purpose**: Design and implement the Firestore solution

**Actions**:

**A. Collection and Document Design:**

1. **Design collection hierarchy**:
   - Map entities to collections and subcollections
   - Decide embedding vs referencing strategy
   - Define document schemas with field types
   - Plan for document size limits (1 MiB max)
   - Design document ID strategy (auto-generated vs custom)

2. **Data modeling for queries**:
   - Identify all query patterns the application needs
   - Denormalize data to support queries without client-side JOINs
   - Design fan-out writes for feed-style data
   - Plan aggregation fields (counters, sums, averages)
   - Handle many-to-many relationships

**B. Security Rules:**

1. **Design security rules** (firestore.rules):
   - Authentication requirements per collection
   - Field-level validation (type, format, range)
   - Role-based access control (RBAC)
   - Data ownership rules (user can only access own data)
   - Rate limiting patterns
   - Cross-collection validation (when needed)

2. **Security rules testing**:
   - Provide test scenarios for rules
   - Cover allow and deny cases
   - Test edge cases (missing fields, wrong types)

**C. Query Implementation:**

1. **Simple queries**: Single field filters, ordering, limiting
2. **Compound queries**: Multiple `where()` clauses (equality + range)
3. **Collection group queries**: Querying across subcollections
4. **Pagination**: Cursor-based with `startAfter()`, `limit()`
5. **Real-time queries**: `onSnapshot()` with error handling
6. **Aggregation queries**: `count()`, `sum()`, `average()`

**D. Real-Time Listeners:**

1. **Document listeners**: Single document change monitoring
2. **Query listeners**: Filtered collection monitoring
3. **Snapshot metadata**: Handle `fromCache` and `hasPendingWrites`
4. **Listener lifecycle**: Attach on mount, detach on unmount
5. **Error recovery**: Handle listener errors gracefully

**E. Offline and Transactions:**

1. **Offline persistence**: Configure cache size, multi-tab support
2. **Transactions**: Read-then-write atomic operations
3. **Batch writes**: Atomic multi-document writes (max 500 operations)
4. **Distributed counters**: Shard counters for high-write scenarios
5. **Optimistic concurrency**: Handle contention gracefully

**F. Indexing and Performance:**

1. **Single-field indexes**: Automatic, manage exemptions
2. **Composite indexes**: Generate `firestore.indexes.json`
3. **Query planning**: Optimize for read-heavy vs write-heavy
4. **Connection management**: Configure SDK settings

**Output**: Complete Firestore implementation

---

#### **Step 5: Generate Output**

**Purpose**: Produce deliverable artifacts

**Actions**:
1. Save output to `/claudedocs/firebase-firestore_{project}_{YYYY-MM-DD}.md`
2. Follow naming conventions in `../OUTPUT_CONVENTIONS.md`
3. Generate deliverable files:
   - `firestore.rules` - Security rules
   - `firestore.indexes.json` - Composite index definitions
   - Collection schema documentation
   - Query implementation code (appropriate SDK)
   - Real-time listener setup code
   - Data migration scripts (if applicable)
4. Include the 10-error prevention checklist in output

**Output**: Complete, production-ready Firestore implementation artifacts

---

#### **Step 6: Update Memory**

**Purpose**: Store configuration for future reference

> Follow [Standard Memory Update](../../interfaces/shared_loading_patterns.md#pattern-3-standard-memory-update) for `skill="firebase-firestore"`. Store any newly learned patterns, conventions, or project insights.

**Actions**:
1. Use `memoryStore.update(layer="skill-specific", skill="firebase-firestore", project="{project-name}", ...)` to store:
2. **collection_structure.md**:
   - Collection hierarchy and subcollections
   - Document schemas with field types
   - Document ID strategies
   - Denormalization decisions
3. **security_rules.md**:
   - Current security rules
   - Access control patterns
   - Validation logic
   - Rule testing results
4. **query_patterns.md**:
   - Implemented query patterns
   - Composite indexes required
   - Pagination strategies
   - Real-time listener scopes
5. **data_model.md**:
   - Embedding vs referencing decisions
   - Fan-out write patterns
   - Aggregation strategies
   - Relationship modeling
6. **performance_config.md**:
   - Cache configuration
   - Index optimizations
   - Read/write distribution
   - Cost optimization notes

**Output**: Memory stored for future skill invocations

---

## Best Practices

### Collection Design

1. **Model for queries**: Design collections around how data is read, not how it's related
2. **Use subcollections**: For one-to-many relationships with large cardinality
3. **Denormalize strategically**: Duplicate data that is read together frequently
4. **Keep documents small**: Aim for under 100 KiB, never exceed 1 MiB
5. **Avoid unbounded arrays**: Use subcollections instead of growing arrays

### Security Rules

1. **Never deploy open rules**: Always require authentication
2. **Validate all writes**: Check field types, ranges, and required fields
3. **Use custom claims**: For role-based access control
4. **Test rules thoroughly**: Use the Firebase Emulator for rule testing
5. **Keep rules DRY**: Use functions for reusable validation logic

### Query Optimization

1. **Create indexes proactively**: Don't wait for errors to create composite indexes
2. **Paginate all list queries**: Never fetch unbounded collections
3. **Use cursor pagination**: `startAfter()` over `offset()` for efficiency
4. **Scope listeners tightly**: Listen to the minimum data set needed
5. **Use aggregation queries**: Prefer server-side `count()` over client-side counting

### Real-Time Listeners

1. **Always unsubscribe**: Detach listeners when no longer needed
2. **Handle errors in listeners**: Network failures, permission changes
3. **Use metadata**: Check `fromCache` to indicate stale data to users
4. **Debounce rapid updates**: Avoid re-rendering on every snapshot
5. **Prefer query listeners**: Over individual document listeners for lists

---

## Error Handling

### Common Issues

1. **Permission denied**: Check security rules and user authentication state
2. **Missing index**: Create composite index from error link or `firestore.indexes.json`
3. **Document not found**: Handle gracefully with fallback UI
4. **Quota exceeded**: Implement backoff and monitor usage
5. **Network errors**: Leverage offline persistence, show connectivity state

### Debugging

1. **Use Firebase Emulator**: Test locally without affecting production
2. **Check rules in console**: Use the Rules Playground for testing
3. **Monitor in Firebase Console**: Track reads, writes, and deletes
4. **Enable debug logging**: `firebase.firestore.setLogLevel('debug')`
5. **Review index usage**: Check for unnecessary or missing indexes

---

## Compliance Checklist

Before completing, verify:

- [ ] All mandatory workflow steps executed in order
- [ ] Standard Memory Loading pattern followed (Step 2)
- [ ] Standard Context Loading pattern followed (Step 3)
- [ ] Output saved with standard naming convention
- [ ] Standard Memory Update pattern followed (Step 6)
- [ ] Security rules require authentication (no open rules)
- [ ] All compound queries have composite indexes defined
- [ ] Pagination implemented for all list queries
- [ ] Real-time listeners have proper unsubscribe handling
- [ ] 10-error prevention checklist verified

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2025-07-14 | Initial release with interface-based patterns, 10-error prevention, comprehensive Firestore workflow |

---

## Related Skills

- **database-schema-analysis**: For analyzing existing database schemas before migration
- **generate-api-spec**: For designing APIs that interact with Firestore
- **security-audit**: For comprehensive security rule review

---

## References

- [Firestore Documentation](https://firebase.google.com/docs/firestore)
- [Firestore Security Rules](https://firebase.google.com/docs/firestore/security/get-started)
- [Firestore Data Modeling](https://firebase.google.com/docs/firestore/manage-data/structure-data)
- [Firestore Best Practices](https://firebase.google.com/docs/firestore/best-practices)
- [Firestore Pricing](https://firebase.google.com/pricing)
- [Firebase Emulator Suite](https://firebase.google.com/docs/emulator-suite)
